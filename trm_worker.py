import argparse
import json
import logging
import os
import signal
import subprocess
import sys
import time
from datetime import datetime, timedelta
from pathlib import Path

BASE_DIR = Path(__file__).parent.resolve()
TRM_AGENTS_DIR = BASE_DIR / "trm_agents"
LOG_DIR = BASE_DIR / "logs"
LOG_DIR.mkdir(exist_ok=True)
PID_FILE = BASE_DIR / "trm_worker.pid"
STATUS_FILE = BASE_DIR / "worker_status.json"
INTELLIGENCE_LOG_FILE = BASE_DIR / "intelligence_log.json"
SENTINEL_ALERTS_FILE = BASE_DIR / "sentinel_alerts.json"
WORKER_LOG = LOG_DIR / "trm_worker.log"
TASK_NAME = "TRM-TamOtonom-Worker"

if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))
if str(TRM_AGENTS_DIR) not in sys.path:
    sys.path.insert(0, str(TRM_AGENTS_DIR))

os.environ.setdefault("PYTHONIOENCODING", "utf-8")
os.environ.setdefault("PYTHONUTF8", "1")
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler(str(WORKER_LOG), encoding="utf-8"),
    ],
)
logger = logging.getLogger("TRMWorker")

from trm_agents.CoreNexus import CoreNexus
from trm_agents.camouflage_agent import CamouflageAgent
from trm_agents.account_manager_agent import AccountManagerAgent
from trm_agents.analyst_agent import AnalystAgent
from trm_agents.content_generator_agent import ContentGeneratorAgent
from trm_agents.queue_agent import QueueAgent
from trm_agents.poster_agent import PosterAgent
from trm_agents.healthcheck_agent import HealthCheckAgent
from trm_agents.expansion_module import build_expansion_agents, get_capacity_snapshot


def _write_pid():
    PID_FILE.write_text(str(os.getpid()), encoding="utf-8")


def _remove_pid():
    PID_FILE.unlink(missing_ok=True)


def _read_pid():
    try:
        return int(PID_FILE.read_text(encoding="utf-8").strip())
    except Exception:
        return 0


def _is_running(pid):
    if pid <= 0:
        return False
    if sys.platform == "win32":
        result = subprocess.run(
            ["tasklist", "/FI", f"PID eq {pid}", "/FO", "CSV", "/NH"],
            capture_output=True,
            text=True,
            check=False,
        )
        return str(pid) in result.stdout
    try:
        os.kill(pid, 0)
        return True
    except Exception:
        return False


class TRMWorker:
    def __init__(self):
        self.factory_interval = timedelta(minutes=int(os.getenv("TRM_FACTORY_INTERVAL_MINUTES", "360")))
        self.loop_interval = int(os.getenv("TRM_WORKER_LOOP_SECONDS", "60"))
        self._shutdown = False
        self.last_factory_run = None
        self.capacity_snapshot = get_capacity_snapshot()

    def _build_sample_products(self):
        return [
            {"title": "Organik Zeytin Yagi 1L", "product_url": "https://www.trendyol.com/gida-saglik-ve-ozel-bakim/organik-urunler/organik-zeytin-yagi", "price": 349.90, "commission_rate": 28.0},
            {"title": "Kozmetik Cilt Bakim Seti", "product_url": "https://www.trendyol.com/kozmetik/cilt-bakim/cilt-bakim-seti", "price": 499.50, "commission_rate": 35.0},
            {"title": "Nemlendirici Krem", "product_url": "https://www.trendyol.com/kozmetik/cilt-bakim/nemlendirici-krem", "price": 189.90, "commission_rate": 22.0},
            {"title": "Sampuan 500ml", "product_url": "https://www.trendyol.com/kozmetik/sac-bakim/sampuan", "price": 159.90, "commission_rate": 18.0},
            {"title": "Bal 1kg", "product_url": "https://www.trendyol.com/gida-saglik-ve-ozel-bakim/tatli-urunler/bal", "price": 279.90, "commission_rate": 24.0},
        ]

    def _handle_stop(self, signum, frame):
        logger.info("Signal alindi, worker kapanisa geciyor: %s", signum)
        self._shutdown = True

    def _setup_signals(self):
        signal.signal(signal.SIGINT, self._handle_stop)
        signal.signal(signal.SIGTERM, self._handle_stop)

    def _build_core_nexus(self, include_pipeline=True):
        nexus = CoreNexus(zero_trust=True, stealth_mode=True)
        active_agents = []
        expansion_specs = build_expansion_agents()

        if include_pipeline:
            camou = CamouflageAgent()
            account_mgr = AccountManagerAgent()
            content_generator = ContentGeneratorAgent()
            queue_agent = QueueAgent()
            poster_agent = PosterAgent()
            health_agent = HealthCheckAgent(base_dir=str(BASE_DIR))

            nexus.connect_agent("CamouflageAgent", camou)
            nexus.connect_agent("AccountManagerAgent", account_mgr)
            for spec in expansion_specs[:10]:
                nexus.connect_agent(
                    spec["name"],
                    spec["instance"],
                    capabilities=spec["capabilities"],
                    context_allowlist=spec["context_allowlist"],
                )
            for spec in expansion_specs[10:25]:
                nexus.connect_agent(
                    spec["name"],
                    spec["instance"],
                    capabilities=spec["capabilities"],
                    context_allowlist=spec["context_allowlist"],
                )
            nexus.connect_agent("Content_Generator_Agent", content_generator)
            nexus.connect_agent("QueueAgent", queue_agent)
            nexus.connect_agent("PosterAgent", poster_agent)
            for spec in expansion_specs[25:]:
                nexus.connect_agent(
                    spec["name"],
                    spec["instance"],
                    capabilities=spec["capabilities"],
                    context_allowlist=spec["context_allowlist"],
                )
            nexus.connect_agent("HealthCheckAgent", health_agent)
            active_agents = list(nexus.agents.keys())
            return nexus, camou, account_mgr, active_agents

        poster_agent = PosterAgent()
        health_agent = HealthCheckAgent(base_dir=str(BASE_DIR))
        for spec in expansion_specs:
            nexus.connect_agent(
                spec["name"],
                spec["instance"],
                capabilities=spec["capabilities"],
                context_allowlist=spec["context_allowlist"],
            )
        nexus.connect_agent("PosterAgent", poster_agent)
        nexus.connect_agent("HealthCheckAgent", health_agent)
        active_agents = list(nexus.agents.keys())
        return nexus, None, None, active_agents

    def _create_sales_pool(self, sample_products, operator_identity, mask_id):
        output_path = BASE_DIR / "ACIL_SATIS_HAVUZU.txt"
        with open(output_path, "w", encoding="utf-8") as f:
            f.write("=========================================\n")
            f.write("TRM ACIL NAKIT OTOMASYONU - ACIL SATIS HAVUZU\n")
            f.write("=========================================\n")
            f.write(f"Baslama Zamani: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Maske ID: {mask_id}\n")
            f.write(f"Operator: {operator_identity['identity']}\n")
            f.write(f"E-posta: {operator_identity['email']}\n")
            f.write(f"Domain: {operator_identity['domain_authority']}\n")
            f.write(f"Toplam Urun: {len(sample_products)}\n")
            f.write("=========================================\n\n")

            affiliate_id = "trendurunlermarket"
            for product in sample_products:
                affiliate_link = product["product_url"]
                affiliate_link += f"&affiliate={affiliate_id}" if "?" in affiliate_link else f"?affiliate={affiliate_id}"
                f.write(f"{product['title']} - {affiliate_link}\n")

        return str(output_path)

    def _build_analysis_result(self, output_path, sample_products):
        analyst = AnalystAgent()
        analysis_result = analyst.analyze_pool(output_path)
        if not analysis_result:
            return None, "Trend analizi yapilamadi."

        product_map = {item["title"]: item for item in sample_products}
        enriched_details = []
        for product_name, score in analysis_result.get("scores", {}).items():
            product_meta = product_map.get(product_name, {})
            price = float(product_meta.get("price", 0.0))
            commission_rate = float(product_meta.get("commission_rate", 0.0))
            enriched_details.append(
                {
                    "product_name": product_name,
                    "trend_score": score,
                    "price": price,
                    "commission_rate": commission_rate,
                    "estimated_commission": round(price * commission_rate / 100, 2),
                    "product_url": product_meta.get("product_url", ""),
                }
            )

        analysis_result["product_details"] = enriched_details
        if enriched_details:
            best = max(
                enriched_details,
                key=lambda item: (item.get("commission_rate", 0.0), item.get("estimated_commission", 0.0)),
            )
            analysis_result["top_commission_product"] = best["product_name"]
            analysis_result["top_commission_rate"] = best["commission_rate"]

        trend_report_path = BASE_DIR / "trend_raporlari.json"
        analyst.save_trend_report(analysis_result, str(trend_report_path))
        return analysis_result, analyst.get_trend_summary(analysis_result)

    def _load_latest_queue(self):
        queue_path = BASE_DIR / "sosyal_medya_kuyruk.json"
        if not queue_path.exists():
            return None
        try:
            with open(queue_path, "r", encoding="utf-8") as f:
                payloads = json.load(f)
            if isinstance(payloads, list) and payloads:
                return payloads[-1]
        except Exception:
            return None
        return None

    def _queue_summary(self, queue_payload):
        if not queue_payload:
            return {"queued": 0, "posted": 0, "pending_retry": 0}
        items = queue_payload.get("items", [])
        return {
            "queued": len([item for item in items if item.get("status") == "queued"]),
            "posted": len([item for item in items if item.get("status") == "posted"]),
            "pending_retry": len([item for item in items if item.get("status") == "pending_retry"]),
        }

    def _write_status(self, status):
        with open(STATUS_FILE, "w", encoding="utf-8") as f:
            json.dump(status, f, ensure_ascii=False, indent=2)

    def _append_json_log(self, file_path, payload, keep_last=50):
        entries = []
        if file_path.exists():
            try:
                entries = json.loads(file_path.read_text(encoding="utf-8"))
                if not isinstance(entries, list):
                    entries = []
            except Exception:
                entries = []
        entries.append(payload)
        entries = entries[-keep_last:]
        file_path.write_text(json.dumps(entries, ensure_ascii=False, indent=2), encoding="utf-8")

    def _extract_agent_group(self, sync_results, prefix):
        return [value for key, value in (sync_results or {}).items() if key.startswith(prefix)]

    def _build_performance_metrics(self, sync_results, queue_summary):
        content_payload = (sync_results or {}).get("Content_Generator_Agent") or {}
        poster_payload = (sync_results or {}).get("PosterAgent") or {}
        lead_commission = float(content_payload.get("lead_estimated_commission", 0.0) or 0.0)
        total_posts = int(queue_summary.get("queued", 0) + queue_summary.get("posted", 0) + queue_summary.get("pending_retry", 0))
        posted_count = int(poster_payload.get("posted_count", 0) or queue_summary.get("posted", 0))
        heartbeat_speed = round(max(1, len(sync_results or {})) / max(1, self.loop_interval), 2)
        efficiency = round(lead_commission / max(1, total_posts), 2)
        success_rate = round((posted_count / max(1, total_posts)) * 100, 2)
        return {
            "heartbeat_speed_per_sec": heartbeat_speed,
            "earnings_efficiency": efficiency,
            "autonomous_success_rate": success_rate,
            "active_agent_count": len(sync_results or {}),
        }

    def _write_live_logs(self, result):
        sync_results = result.get("sync_results") or {}
        queue_summary = result.get("queue_summary") or {"queued": 0, "posted": 0, "pending_retry": 0}
        performance_metrics = self._build_performance_metrics(sync_results, queue_summary)

        intelligence_payload = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "mode": result.get("mode"),
            "market_intelligence": self._extract_agent_group(sync_results, "MarketIntelAgent_"),
            "bridge_network": self._extract_agent_group(sync_results, "BridgeAgent_"),
            "performance_metrics": performance_metrics,
            "capacity": self.capacity_snapshot,
        }
        sentinel_payload = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "mode": result.get("mode"),
            "sentinel_alerts": self._extract_agent_group(sync_results, "SentinelAgent_"),
            "security_status": ((sync_results.get("HealthCheckAgent") or {}).get("report", {}) or {}).get("security_status", {}),
            "queue_summary": queue_summary,
            "capacity": self.capacity_snapshot,
        }

        self._append_json_log(INTELLIGENCE_LOG_FILE, intelligence_payload)
        self._append_json_log(SENTINEL_ALERTS_FILE, sentinel_payload)
        return performance_metrics

    def _run_full_cycle(self):
        nexus, camou, account_mgr, active_agents = self._build_core_nexus(include_pipeline=True)
        sample_products = self._build_sample_products()
        operator_identity = account_mgr.assign_operator_identity("TR")
        mask_id = camou.mask_identity()
        output_path = self._create_sales_pool(sample_products, operator_identity, mask_id)
        analysis_result, trend_summary = self._build_analysis_result(output_path, sample_products)

        context = {
            "trend_report": analysis_result,
            "active_agents": active_agents,
            "worker_mode": "full_cycle",
            "agent_capacity_snapshot": self.capacity_snapshot,
        }
        sync_results = nexus.run_system_sync(context=context)
        queue_payload = sync_results.get("QueueAgent") or self._load_latest_queue()

        return {
            "mode": "full_cycle",
            "output_path": output_path,
            "trend_summary": trend_summary,
            "sync_results": sync_results,
            "queue_summary": self._queue_summary(queue_payload),
        }

    def _run_heartbeat_cycle(self):
        nexus, _, _, active_agents = self._build_core_nexus(include_pipeline=False)
        sync_results = nexus.run_system_sync(
            context={
                "active_agents": active_agents,
                "worker_mode": "heartbeat_cycle",
                "queue_payload": self._load_latest_queue(),
                "agent_capacity_snapshot": self.capacity_snapshot,
            }
        )
        queue_payload = self._load_latest_queue()
        return {
            "mode": "heartbeat_cycle",
            "sync_results": sync_results,
            "queue_summary": self._queue_summary(queue_payload),
        }

    def _run_cycle(self, force_full=False):
        now = datetime.now()
        if force_full or not self.last_factory_run or (now - self.last_factory_run) >= self.factory_interval:
            result = self._run_full_cycle()
            self.last_factory_run = now
            return result
        return self._run_heartbeat_cycle()

    def run_once(self, force_full=True):
        self._setup_signals()
        cycle_started = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        result = self._run_cycle(force_full=force_full)
        health_result = (result.get("sync_results") or {}).get("HealthCheckAgent") or {}
        performance_metrics = self._write_live_logs(result)
        status = {
            "worker_state": "alive",
            "cycle_started_at": cycle_started,
            "last_cycle_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "last_mode": result.get("mode"),
            "queue_summary": result.get("queue_summary"),
            "active_agents": list((result.get("sync_results") or {}).keys()),
            "security_status": health_result.get("report", {}).get("security_status", {}),
            "agent_capacity_snapshot": self.capacity_snapshot,
            "heartbeat_capacity_total": self.capacity_snapshot.get("total_capacity"),
            "performance_metrics": performance_metrics,
        }
        self._write_status(status)
        logger.info("Nabiz atisi kaydedildi: %s", status)
        return result

    def run_forever(self):
        _write_pid()
        self._setup_signals()
        logger.info("TRM worker baslatildi | loop=%ss | factory_interval=%s", self.loop_interval, self.factory_interval)
        try:
            while not self._shutdown:
                started_at = time.time()
                try:
                    result = self.run_once(force_full=False)
                    logger.info("Dongu tamamlandi | mod=%s | kuyruk=%s", result.get("mode"), result.get("queue_summary"))
                except Exception as exc:
                    logger.exception("Worker dongusu hata verdi: %s", exc)
                    self._write_status(
                        {
                            "worker_state": "error",
                            "last_error": str(exc),
                            "last_cycle_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        }
                    )
                elapsed = time.time() - started_at
                sleep_for = max(1, self.loop_interval - int(elapsed))
                for _ in range(sleep_for):
                    if self._shutdown:
                        break
                    time.sleep(1)
        finally:
            _remove_pid()
            logger.info("TRM worker kapatildi")


def cmd_start():
    pid = _read_pid()
    if _is_running(pid):
        print(f"Worker zaten calisiyor: PID {pid}")
        return

    pythonw = Path(sys.executable).with_name("pythonw.exe")
    executable = str(pythonw if pythonw.exists() else sys.executable)
    creationflags = 0
    if sys.platform == "win32":
        creationflags = (
            subprocess.CREATE_NEW_PROCESS_GROUP
            | getattr(subprocess, "DETACHED_PROCESS", 0)
            | getattr(subprocess, "CREATE_NO_WINDOW", 0)
        )

    with open(WORKER_LOG, "a", encoding="utf-8") as log_f:
        proc = subprocess.Popen(
            [executable, str(BASE_DIR / "trm_worker.py"), "run"],
            cwd=str(BASE_DIR),
            stdout=log_f,
            stderr=log_f,
            env={**os.environ, "PYTHONIOENCODING": "utf-8", "PYTHONUTF8": "1"},
            creationflags=creationflags,
        )
    print(f"Worker arka planda baslatildi: PID {proc.pid}")


def cmd_stop():
    pid = _read_pid()
    if not _is_running(pid):
        print("Worker zaten calismiyor")
        _remove_pid()
        return
    if sys.platform == "win32":
        subprocess.run(["taskkill", "/PID", str(pid), "/F"], check=False)
    else:
        os.kill(pid, signal.SIGTERM)
    print(f"Worker durdurma sinyali gonderildi: PID {pid}")


def cmd_status():
    pid = _read_pid()
    running = _is_running(pid)
    status = {}
    if STATUS_FILE.exists():
        try:
            status = json.loads(STATUS_FILE.read_text(encoding="utf-8"))
        except Exception:
            status = {}
    print(json.dumps({"running": running, "pid": pid, "status": status}, ensure_ascii=False, indent=2))


def cmd_install_task():
    launcher = f'powershell -WindowStyle Hidden -ExecutionPolicy Bypass -File "{BASE_DIR / "START_TRM_WORKER.ps1"}"'
    command = f'schtasks /Create /SC ONLOGON /TN "{TASK_NAME}" /TR "{launcher}" /F'
    result = subprocess.run(command, cwd=str(BASE_DIR), shell=True, check=False)

    startup_dir = Path(os.getenv("APPDATA", "")) / "Microsoft" / "Windows" / "Start Menu" / "Programs" / "Startup"
    startup_dir.mkdir(parents=True, exist_ok=True)
    startup_cmd = startup_dir / "TRM_Worker_Autostart.cmd"
    startup_cmd.write_text(
        f'@echo off\npowershell -WindowStyle Hidden -ExecutionPolicy Bypass -File "{BASE_DIR / "START_TRM_WORKER.ps1"}"\n',
        encoding="utf-8",
    )

    if result.returncode == 0:
        print(f"Scheduled task guncellendi: {TASK_NAME}")
    else:
        print("Scheduled task kurulumu icin yetki yetersizdi; Startup klasoru geri donusu olusturuldu.")
    print(f"Autostart dosyasi: {startup_cmd}")


def main():
    parser = argparse.ArgumentParser(description="TRM worker yoneticisi")
    parser.add_argument("command", choices=["run", "once", "start", "stop", "status", "install-task"])
    args = parser.parse_args()

    if args.command == "run":
        TRMWorker().run_forever()
    elif args.command == "once":
        result = TRMWorker().run_once(force_full=True)
        print(json.dumps(result, ensure_ascii=False, indent=2, default=str))
    elif args.command == "start":
        cmd_start()
    elif args.command == "stop":
        cmd_stop()
    elif args.command == "status":
        cmd_status()
    elif args.command == "install-task":
        cmd_install_task()


if __name__ == "__main__":
    main()
