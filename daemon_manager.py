#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TRM - DAEMON / SERVICE YONETICISI v1.0
========================================
Linux: systemd servisi VEYA standalone daemon
Windows: Task Scheduler XML veya NSSM komutu

Komutlar:
  python DAEMON_MANAGER.py start      - Arka planda baslat
  python DAEMON_MANAGER.py stop       - Durdur
  python DAEMON_MANAGER.py restart    - Yeniden baslat
  python DAEMON_MANAGER.py status     - Durum goster
  python DAEMON_MANAGER.py run        - On planda calistir (debug)
  python DAEMON_MANAGER.py install    - Sistem servisi olarak kur
  python DAEMON_MANAGER.py uninstall  - Servisi kaldir
  python DAEMON_MANAGER.py health     - Health check ping
"""

import os
import sys
import signal
import time
import socket
import logging
import argparse
import subprocess
import threading
from pathlib import Path
from datetime import datetime

# ── TEMEL YAPILANDIRMA ────────────────────────────────────────────────
BASE_DIR     = Path(__file__).parent.resolve()
PID_FILE     = BASE_DIR / "trm_daemon.pid"
LOG_DIR      = BASE_DIR / "logs"
DAEMON_LOG   = LOG_DIR  / "daemon.log"
HEALTH_PORT  = int(os.getenv("TRM_HEALTH_PORT", "9099"))
SERVICE_NAME = "trm-otomasyon"

LOG_DIR.mkdir(exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler(str(DAEMON_LOG), encoding="utf-8"),
    ],
)
logger = logging.getLogger("TRMDaemon")


# ── PID YONETIMI ─────────────────────────────────────────────────────

def write_pid() -> None:
    PID_FILE.write_text(str(os.getpid()), encoding="utf-8")


def read_pid() -> int:
    try:
        return int(PID_FILE.read_text(encoding="utf-8").strip())
    except (FileNotFoundError, ValueError):
        return 0


def remove_pid() -> None:
    PID_FILE.unlink(missing_ok=True)


def is_process_running(pid: int) -> bool:
    if pid <= 0:
        return False
    try:
        os.kill(pid, 0)
        return True
    except (ProcessLookupError, PermissionError):
        return False


# ── HEALTH CHECK (TCP) ────────────────────────────────────────────────

def _health_server_thread() -> None:
    """Basit TCP health-check server — baglanti gelince 'OK\n' yazar."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as srv:
            srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            srv.bind(("0.0.0.0", HEALTH_PORT))
            srv.listen(5)
            srv.settimeout(1.0)
            logger.info(f"🏥 Health-check :{HEALTH_PORT} dinleniyor")
            while True:
                try:
                    conn, addr = srv.accept()
                    with conn:
                        conn.sendall(b"OK\n")
                except socket.timeout:
                    continue
                except OSError:
                    break
    except Exception as e:
        logger.warning(f"Health-check baslatilamadi: {e}")


def ping_health(host: str = "127.0.0.1", timeout: float = 3.0) -> bool:
    """Health-check portuna baglan, OK donuyor mu kontrol et."""
    try:
        with socket.create_connection((host, HEALTH_PORT), timeout=timeout) as s:
            data = s.recv(8)
            return data.startswith(b"OK")
    except Exception:
        return False


# ── ANA DAEMON SINIFI ─────────────────────────────────────────────────

class TRMDaemon:
    def __init__(self):
        self._shutdown   = False
        self._start_time = None

    # ── Signal yonetimi ──────────────────────────────────────────────

    def _handle_stop(self, signum, frame):
        logger.info(f"Signal {signum} alindi → graceful shutdown basliyor...")
        self._shutdown = True

    def _handle_reload(self, signum, frame):
        logger.info("SIGHUP → yapilandirma yeniden yukleniyor...")
        try:
            import config as cfg
            cfg.config.load_environment()
            logger.info("✅ Config yeniden yuklendi")
        except Exception as e:
            logger.error(f"Config reload hatasi: {e}")

    def _setup_signals(self):
        signal.signal(signal.SIGTERM, self._handle_stop)
        signal.signal(signal.SIGINT,  self._handle_stop)
        if hasattr(signal, "SIGHUP"):
            signal.signal(signal.SIGHUP, self._handle_reload)

    # ── Calistirma ────────────────────────────────────────────────────

    def run(self):
        """On planda calistir (systemd veya debug icin)."""
        write_pid()
        self._setup_signals()
        self._start_time = datetime.now()

        # Health-check thread
        t = threading.Thread(target=_health_server_thread, daemon=True)
        t.start()

        logger.info(f"🚀 TRM Daemon baslatildi | PID {os.getpid()} | Surum v1.0")
        logger.info(f"   Calisma dizini : {BASE_DIR}")
        logger.info(f"   Log            : {DAEMON_LOG}")
        logger.info(f"   Health port    : {HEALTH_PORT}")

        try:
            import asyncio
            # Config'i ilk yukle
            sys.path.insert(0, str(BASE_DIR))
            import config  # noqa: F401

            from main_orchestrator_yedek import TRMOrchestrator
            orchestrator = TRMOrchestrator()

            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                loop.run_until_complete(orchestrator.run())
            except KeyboardInterrupt:
                pass
            finally:
                loop.close()

        except ImportError as e:
            logger.error(f"Orchestrator import hatasi: {e} — heartbeat modunda devam")
            # Orchestrator yoksa basit heartbeat
            self._heartbeat_loop()
        except Exception as e:
            logger.error(f"Daemon hatasi: {e}")
        finally:
            remove_pid()
            logger.info("🔴 TRM Daemon kapatildi")

    def _heartbeat_loop(self):
        """Orchestrator yuklenemediginde basit yasam dongusu."""
        while not self._shutdown:
            uptime = datetime.now() - self._start_time
            logger.info(f"💓 Heartbeat | Calisma: {str(uptime).split('.')[0]}")
            for _ in range(60):
                if self._shutdown:
                    break
                time.sleep(1)

    # ── Arka plan baslatma (subprocess) ───────────────────────────────

    def start_background(self):
        """Sureci arka planda baslat."""
        pid = read_pid()
        if is_process_running(pid):
            print(f"⚠️  Daemon zaten calisiyor (PID {pid})")
            return

        python = sys.executable
        script = str(BASE_DIR / "DAEMON_MANAGER.py")
        kwargs = {}
        if sys.platform != "win32":
            kwargs["start_new_session"] = True
        else:
            kwargs["creationflags"] = subprocess.CREATE_NEW_PROCESS_GROUP

        with open(str(DAEMON_LOG), "a", encoding="utf-8") as log_f:
            proc = subprocess.Popen(
                [python, script, "run"],
                stdout=log_f, stderr=log_f,
                cwd=str(BASE_DIR), **kwargs
            )

        time.sleep(2)
        if is_process_running(proc.pid):
            print(f"✅ Daemon baslatildi (PID {proc.pid})")
        else:
            print("❌ Daemon baslatilamadi — log dosyasini kontrol et")
            print(f"   {DAEMON_LOG}")


# ── CLI KOMUTLARI ─────────────────────────────────────────────────────

def cmd_start():
    daemon = TRMDaemon()
    daemon.start_background()


def cmd_stop():
    pid = read_pid()
    if not is_process_running(pid):
        print("ℹ️  Daemon zaten calismiyor")
        remove_pid()
        return
    print(f"🛑 Daemon durduruluyor (PID {pid})...")
    try:
        os.kill(pid, signal.SIGTERM)
        for _ in range(30):
            time.sleep(1)
            if not is_process_running(pid):
                break
        if is_process_running(pid):
            os.kill(pid, signal.SIGKILL)
            print("⚠️  SIGKILL gonderildi (SIGTERM yeterli olmadi)")
        remove_pid()
        print("✅ Daemon durduruldu")
    except Exception as e:
        print(f"❌ Durdurma hatasi: {e}")


def cmd_restart():
    cmd_stop()
    time.sleep(2)
    cmd_start()


def cmd_status():
    pid = read_pid()
    running = is_process_running(pid)
    health  = ping_health() if running else False

    print("=" * 50)
    print("  TRM Daemon Durumu")
    print("=" * 50)
    if running:
        print(f"  Durum     : 🟢 CALISIYOR")
        print(f"  PID       : {pid}")
        print(f"  Health    : {'✅ OK' if health else '⚠️ Yanit vermiyor'}")
    else:
        print("  Durum     : 🔴 DURDU")
    print(f"  PID dosya : {PID_FILE}")
    print(f"  Log       : {DAEMON_LOG}")
    print(f"  Health    : :{HEALTH_PORT}")
    print("=" * 50)


def cmd_health():
    if ping_health():
        print("✅ Daemon saglikli calisiyor")
        sys.exit(0)
    else:
        print("❌ Daemon yanit vermiyor")
        sys.exit(1)


# ── SYSTEMD / WINDOWS KURULUM ─────────────────────────────────────────

SYSTEMD_UNIT = """\
[Unit]
Description=TRM Full Otomasyon Sistemi
After=network-online.target
Wants=network-online.target
StartLimitIntervalSec=120
StartLimitBurst=5

[Service]
Type=simple
User={user}
WorkingDirectory={workdir}
ExecStart={python} {script} run
ExecReload=/bin/kill -HUP $MAINPID
Restart=on-failure
RestartSec=15s
StandardOutput=append:{logdir}/daemon.log
StandardError=append:{logdir}/daemon_error.log
Environment=PYTHONIOENCODING=utf-8
Environment=PYTHONUNBUFFERED=1
KillMode=process
TimeoutStopSec=30

[Install]
WantedBy=multi-user.target
"""

WINDOWS_NSSM_BAT = """\
@echo off
chcp 65001 > nul
echo TRM Daemon - NSSM ile Windows Servisi Kurulumu
echo ================================================
where nssm >nul 2>&1
if %errorlevel% neq 0 (
    echo HATA: nssm.exe bulunamadi.
    echo Indirin: https://nssm.cc/download
    echo nssm.exe dosyasini bu klasore koyun.
    pause & exit /b 1
)
set SVC=TRM-Otomasyon
set PY={python}
set SCRIPT={script}
nssm install %SVC% "%PY%" "%SCRIPT%" run
nssm set %SVC% AppDirectory {workdir}
nssm set %SVC% AppStdout {logdir}\\daemon.log
nssm set %SVC% AppStderr {logdir}\\daemon_error.log
nssm set %SVC% AppRestartDelay 15000
nssm set %SVC% Start SERVICE_AUTO_START
nssm start %SVC%
echo Servis kuruldu ve baslatildi.
pause
"""


def cmd_install():
    python  = sys.executable
    script  = str(BASE_DIR / "DAEMON_MANAGER.py")
    workdir = str(BASE_DIR)
    logdir  = str(LOG_DIR)

    if sys.platform.startswith("linux"):
        unit = SYSTEMD_UNIT.format(
            user=os.getenv("USER", "root"),
            workdir=workdir, python=python,
            script=script, logdir=logdir,
        )
        unit_path = Path(f"/etc/systemd/system/{SERVICE_NAME}.service")
        try:
            unit_path.write_text(unit, encoding="utf-8")
            subprocess.run(["systemctl", "daemon-reload"], check=True)
            subprocess.run(["systemctl", "enable", SERVICE_NAME], check=True)
            print(f"✅ systemd servisi kuruldu: {unit_path}")
            print(f"   Baslatmak icin : sudo systemctl start {SERVICE_NAME}")
            print(f"   Durum          : sudo systemctl status {SERVICE_NAME}")
        except PermissionError:
            print("❌ Root yetkisi gerekli: sudo python DAEMON_MANAGER.py install")
        except FileNotFoundError:
            # systemd yok, unit dosyasini yaz
            local_unit = BASE_DIR / f"{SERVICE_NAME}.service"
            local_unit.write_text(unit, encoding="utf-8")
            print(f"ℹ️  systemctl bulunamadi. Unit dosyasi olusturuldu: {local_unit}")

    elif sys.platform == "win32":
        nssm_bat = BASE_DIR / "NSSM_SERVIS_KUR.bat"
        content = WINDOWS_NSSM_BAT.format(
            python=python, script=script,
            workdir=workdir, logdir=logdir,
        )
        nssm_bat.write_text(content, encoding="utf-8")
        # Task Scheduler XML de olustur (NSSM yoksa alternatif)
        xml_path = BASE_DIR / "TRM_TaskScheduler.xml"
        xml_path.write_text(_task_scheduler_xml(python, script, workdir), encoding="utf-16")
        print(f"✅ Windows kurulum dosyalari olusturuldu:")
        print(f"   NSSM ile       : {nssm_bat}")
        print(f"   Task Scheduler : {xml_path}")
        print("   Task Scheduler ice aktarma:")
        print("   schtasks /Create /XML TRM_TaskScheduler.xml /TN TRM-Otomasyon")
    else:
        print(f"⚠️  Bu isletim sistemi ({sys.platform}) icin kurulum sablonu hazir degil")
        print("   'run' komutuyla on planda calistirabilirsiniz")


def _task_scheduler_xml(python, script, workdir):
    return f"""<?xml version="1.0" encoding="UTF-16"?>
<Task version="1.4" xmlns="http://schemas.microsoft.com/windows/2004/02/mit/task">
  <Triggers>
    <BootTrigger><Enabled>true</Enabled></BootTrigger>
  </Triggers>
  <Actions Context="Author">
    <Exec>
      <Command>{python}</Command>
      <Arguments>{script} run</Arguments>
      <WorkingDirectory>{workdir}</WorkingDirectory>
    </Exec>
  </Actions>
  <Settings>
    <MultipleInstancesPolicy>IgnoreNew</MultipleInstancesPolicy>
    <RestartOnFailure>
      <Interval>PT1M</Interval><Count>10</Count>
    </RestartOnFailure>
    <ExecutionTimeLimit>PT0S</ExecutionTimeLimit>
    <Priority>7</Priority>
  </Settings>
</Task>"""


def cmd_uninstall():
    if sys.platform.startswith("linux"):
        try:
            subprocess.run(["systemctl", "stop",    SERVICE_NAME], check=False)
            subprocess.run(["systemctl", "disable", SERVICE_NAME], check=False)
            unit = Path(f"/etc/systemd/system/{SERVICE_NAME}.service")
            unit.unlink(missing_ok=True)
            subprocess.run(["systemctl", "daemon-reload"], check=False)
            print(f"✅ Servis kaldirildi: {SERVICE_NAME}")
        except PermissionError:
            print("❌ Root yetkisi gerekli")
    elif sys.platform == "win32":
        subprocess.run(["nssm", "stop",   "TRM-Otomasyon"], check=False)
        subprocess.run(["nssm", "remove", "TRM-Otomasyon", "confirm"], check=False)
        print("✅ Windows servisi kaldirildi")


# ── MAIN ──────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="TRM Daemon Yoneticisi",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument("command", choices=[
        "start", "stop", "restart", "status", "run",
        "install", "uninstall", "health",
    ])
    args = parser.parse_args()

    dispatch = {
        "start":     cmd_start,
        "stop":      cmd_stop,
        "restart":   cmd_restart,
        "status":    cmd_status,
        "health":    cmd_health,
        "install":   cmd_install,
        "uninstall": cmd_uninstall,
        "run":       TRMDaemon().run,
    }
    dispatch[args.command]()


if __name__ == "__main__":
    main()
