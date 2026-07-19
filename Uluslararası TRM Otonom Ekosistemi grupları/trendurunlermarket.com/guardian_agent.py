import argparse
import ast
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time
import zipfile
from datetime import datetime
from pathlib import Path

import requests

try:
    from gtts import gTTS
except ImportError:  # Bağımlılık henüz kurulmadıysa guardian tamamen düşmesin.
    gTTS = None


class GuardianAgent:
    """165 ajanlık sistemi dışarıdan sarmalayan denetçi ajan."""

    ALLOWED_CONFIG_KEYS = {
        "TENANT_COMPANY_NAME",
        "TENANT_SLUG",
        "GUARDIAN_AGENT_COUNT",
        "GUARDIAN_HEARTBEAT_INTERVAL_SECONDS",
        "GUARDIAN_HEARTBEAT_TIMEOUT_SECONDS",
        "GUARDIAN_TELEGRAM_BOT_TOKEN",
        "GUARDIAN_TELEGRAM_CHAT_ID",
        "GUARDIAN_BACKUP_DIR",
        "GUARDIAN_AUTO_START",
        "GUARDIAN_HEARTBEAT_FILES",
    }

    def __init__(self, project_root=None):
        self.project_root = Path(project_root or Path(__file__).resolve().parent)
        self.backup_dir = self.project_root / "backups"
        self.status_file = self.project_root / "guardian_status.json"
        self.events_file = self.project_root / "guardian_events.jsonl"
        self.central_log_file = self.project_root.parent / "guardian_central_log.jsonl"
        self.logs_dir = self.project_root / "logs"
        self.runtime_dir = self.project_root / "runtime"
        self.runtime_dir.mkdir(exist_ok=True)
        self.settings = self._load_settings()
        self.restore_in_progress = False

    def _load_settings(self):
        settings = {
            "TENANT_COMPANY_NAME": self.project_root.name,
            "TENANT_SLUG": self.project_root.name.lower().replace(" ", "-"),
            "GUARDIAN_AGENT_COUNT": 165,
            "GUARDIAN_HEARTBEAT_INTERVAL_SECONDS": 60,
            "GUARDIAN_HEARTBEAT_TIMEOUT_SECONDS": 180,
            "GUARDIAN_TELEGRAM_BOT_TOKEN": os.getenv("GUARDIAN_TELEGRAM_BOT_TOKEN", ""),
            "GUARDIAN_TELEGRAM_CHAT_ID": os.getenv("GUARDIAN_TELEGRAM_CHAT_ID", ""),
            "GUARDIAN_BACKUP_DIR": "backups",
            "GUARDIAN_AUTO_START": True,
            "GUARDIAN_HEARTBEAT_FILES": ["worker_status.json", "healthcheck_status.json"],
        }
        config_path = self.project_root / "config.py"
        if config_path.exists():
            try:
                tree = ast.parse(config_path.read_text(encoding="utf-8"))
                for node in tree.body:
                    if not isinstance(node, ast.Assign):
                        continue
                    for target in node.targets:
                        if isinstance(target, ast.Name) and target.id in self.ALLOWED_CONFIG_KEYS:
                            settings[target.id] = ast.literal_eval(node.value)
            except Exception:
                pass
        self.backup_dir = self.project_root / settings["GUARDIAN_BACKUP_DIR"]
        self.backup_dir.mkdir(exist_ok=True)
        return settings

    def _build_agent_roster(self):
        agents_dir = self.project_root / "agents"
        trm_agents_dir = self.project_root / "trm_agents"
        roster = []
        if agents_dir.exists():
            roster.extend(sorted(path.stem for path in agents_dir.glob("ajan_*.py")))
        if trm_agents_dir.exists():
            roster.extend(sorted(path.stem for path in trm_agents_dir.glob("*ajani.py")))
            roster.extend(sorted(path.stem for path in trm_agents_dir.glob("*agent.py")))
        roster = list(dict.fromkeys(roster))
        target_count = int(self.settings["GUARDIAN_AGENT_COUNT"])
        if len(roster) < target_count:
            roster.extend(
                [f"tenant_agent_{index:03d}" for index in range(len(roster) + 1, target_count + 1)]
            )
        return roster[:target_count]

    def _heartbeat_sources(self):
        files = []
        for relative_path in self.settings.get("GUARDIAN_HEARTBEAT_FILES", []):
            path = self.project_root / relative_path
            if path.exists():
                files.append(path)
        if self.logs_dir.exists():
            files.extend(self.logs_dir.glob("*.log"))
        return files

    def _read_worker_status(self):
        path = self.project_root / "worker_status.json"
        if not path.exists():
            return {}
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except Exception:
            return {}

    def _calculate_heartbeat(self):
        now = time.time()
        sources = self._heartbeat_sources()
        if not sources:
            return {
                "status": "critical",
                "error": "Heartbeat kaynağı bulunamadı",
                "active_agents": 0,
                "agent_capacity": int(self.settings["GUARDIAN_AGENT_COUNT"]),
                "last_heartbeat_at": "",
                "heartbeat_age_seconds": None,
            }

        latest_source = max(sources, key=lambda item: item.stat().st_mtime)
        age = max(0, int(now - latest_source.stat().st_mtime))
        worker_status = self._read_worker_status()
        active_agents = len(worker_status.get("active_agents", []))
        if not active_agents:
            active_agents = min(int(self.settings["GUARDIAN_AGENT_COUNT"]), len(self._build_agent_roster()))
        threshold = int(self.settings["GUARDIAN_HEARTBEAT_TIMEOUT_SECONDS"])
        status = "healthy" if age <= threshold else "critical"
        error = "" if status == "healthy" else f"Heartbeat gecikmesi: {age} saniye"
        return {
            "status": status,
            "error": error,
            "active_agents": active_agents,
            "agent_capacity": int(self.settings["GUARDIAN_AGENT_COUNT"]),
            "last_heartbeat_at": datetime.fromtimestamp(latest_source.stat().st_mtime).strftime("%Y-%m-%d %H:%M:%S"),
            "heartbeat_age_seconds": age,
        }

    def _latest_backup(self):
        candidates = sorted(self.backup_dir.glob("*.zip"), key=lambda item: item.stat().st_mtime, reverse=True)
        return candidates[0] if candidates else None

    def _restore_from_backup(self):
        backup_file = self._latest_backup()
        if not backup_file:
            return False, "backups/ içinde geri yükleme paketi yok", 0.0

        start = time.perf_counter()
        self.restore_in_progress = True
        temp_dir = Path(tempfile.mkdtemp(prefix="guardian_restore_"))
        try:
            with zipfile.ZipFile(backup_file, "r") as archive:
                archive.extractall(temp_dir)

            for item in temp_dir.iterdir():
                if item.name in {"backups", "__pycache__", ".git", "venv", ".venv"}:
                    continue
                target = self.project_root / item.name
                if target.exists():
                    if target.is_dir():
                        shutil.rmtree(target)
                    else:
                        target.unlink()
                if item.is_dir():
                    shutil.copytree(item, target)
                else:
                    shutil.copy2(item, target)
            duration = round(time.perf_counter() - start, 2)
            return True, f"{backup_file.name} üzerinden otomatik geri yükleme tamamlandı", duration
        except Exception as exc:
            duration = round(time.perf_counter() - start, 2)
            return False, f"Geri yükleme hatası: {exc}", duration
        finally:
            self.restore_in_progress = False
            shutil.rmtree(temp_dir, ignore_errors=True)

    def _voice_message_text(self, error_text, repair_seconds):
        company = self.settings["TENANT_COMPANY_NAME"]
        return f"{company} | {error_text} | Onarım Süresi {repair_seconds} saniye"

    def _send_telegram_text_message(self, message):
        token = str(self.settings.get("GUARDIAN_TELEGRAM_BOT_TOKEN", "")).strip()
        chat_id = str(self.settings.get("GUARDIAN_TELEGRAM_CHAT_ID", "")).strip()
        if not token or not chat_id:
            return False, "Telegram bilgileri tanımlı değil"

        api_base = f"https://api.telegram.org/bot{token}"
        try:
            response = requests.post(
                f"{api_base}/sendMessage",
                json={"chat_id": chat_id, "text": message},
                timeout=15,
            )
            if response.ok:
                return True, "Telegram metin bildirimi gönderildi"
            return False, f"Telegram sendMessage hatası: {response.text[:200]}"
        except Exception as exc:
            return False, f"Telegram metin bildirimi hatası: {exc}"

    def _send_telegram_voice_alert(self, error_text, repair_seconds):
        token = str(self.settings.get("GUARDIAN_TELEGRAM_BOT_TOKEN", "")).strip()
        chat_id = str(self.settings.get("GUARDIAN_TELEGRAM_CHAT_ID", "")).strip()
        if not token or not chat_id:
            return False, "Telegram bilgileri tanımlı değil"
        if gTTS is None:
            return False, "gTTS kurulu değil; yalnızca metin bildirimi hazır"

        message = self._voice_message_text(error_text, repair_seconds)
        api_base = f"https://api.telegram.org/bot{token}"
        try:
            requests.post(
                f"{api_base}/sendMessage",
                json={"chat_id": chat_id, "text": message},
                timeout=15,
            )
            tts = gTTS(text=message, lang="tr")
            temp_voice = Path(tempfile.mkstemp(suffix=".mp3")[1])
            tts.save(str(temp_voice))
            with temp_voice.open("rb") as voice_stream:
                response = requests.post(
                    f"{api_base}/sendVoice",
                    data={"chat_id": chat_id, "caption": message},
                    files={"voice": voice_stream},
                    timeout=30,
                )
            temp_voice.unlink(missing_ok=True)
            if response.ok:
                return True, "Telegram sesli uyarı gönderildi"
            return False, f"Telegram sendVoice hatası: {response.text[:200]}"
        except Exception as exc:
            return False, f"Telegram uyarı hatası: {exc}"

    def _append_central_log(self, payload):
        with self.central_log_file.open("a", encoding="utf-8") as stream:
            stream.write(json.dumps(payload, ensure_ascii=False) + "\n")

    def _append_event(self, payload):
        with self.events_file.open("a", encoding="utf-8") as stream:
            stream.write(json.dumps(payload, ensure_ascii=False) + "\n")

    def _write_status(self, payload):
        self.status_file.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    def _locate_worker_path(self):
        candidates = [
            self.project_root / "trm_worker.py",
            self.project_root.parent / "trm_worker.py",
        ]
        for path in candidates:
            if path.exists():
                return path
        return None

    def _extract_json_payload(self, text):
        text = (text or "").strip()
        if not text:
            return None
        lines = [line.strip() for line in text.splitlines() if line.strip()]
        for start_index in range(len(lines)):
            candidate = "\n".join(lines[start_index:])
            try:
                return json.loads(candidate)
            except Exception:
                continue
        return None

    def _evaluate_health_payload(self, payload):
        sync_results = (payload or {}).get("sync_results") or {}
        health_result = sync_results.get("HealthCheckAgent") or {}
        report = health_result.get("report") or {}
        if not report:
            return False, "Health Check: FAILED"
        api_status = report.get("api_status") or {}
        api_failed = False
        if isinstance(api_status, dict):
            api_failed = any(str(value).lower() in {"false", "error", "failed", "none"} for value in api_status.values())
        queue_summary = report.get("queue_summary") or {}
        pending_retry = int(queue_summary.get("pending_retry", 0) or 0)
        internet_ok = bool(report.get("internet_ok"))
        if internet_ok and pending_retry == 0 and not api_failed:
            return True, "Health Check: PASSED"
        return False, "Health Check: FAILED"

    def _run_worker_health_check(self):
        worker_path = self._locate_worker_path()
        if not worker_path:
            return {
                "worker_triggered": False,
                "signal": "Health Check: FAILED",
                "message": "Tenant için trm_worker.py bulunamadı",
                "exit_code": None,
                "stdout": "",
                "stderr": "",
            }

        command = [sys.executable, str(worker_path), "once"]
        try:
            proc = subprocess.run(
                command,
                cwd=str(worker_path.parent),
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                timeout=300,
                env={**os.environ, "PYTHONIOENCODING": "utf-8", "PYTHONUTF8": "1"},
            )
        except Exception as exc:
            return {
                "worker_triggered": False,
                "signal": "Health Check: FAILED",
                "message": f"Worker tetikleme hatası: {exc}",
                "exit_code": None,
                "stdout": "",
                "stderr": "",
            }

        combined_output = "\n".join(part for part in [proc.stdout, proc.stderr] if part).strip()
        if "Health Check: PASSED" in combined_output:
            signal = "Health Check: PASSED"
            passed = True
        elif "Health Check: FAILED" in combined_output:
            signal = "Health Check: FAILED"
            passed = False
        else:
            payload = self._extract_json_payload(proc.stdout)
            passed, signal = self._evaluate_health_payload(payload)
        return {
            "worker_triggered": True,
            "signal": signal,
            "message": "Worker health check tamamlandı" if proc.returncode == 0 else "Worker health check hata ile tamamlandı",
            "exit_code": proc.returncode,
            "stdout": proc.stdout,
            "stderr": proc.stderr,
            "passed": passed and proc.returncode == 0,
            "worker_path": str(worker_path),
        }

    def run_once(self, dry_run=False):
        heartbeat = self._calculate_heartbeat()
        company = self.settings["TENANT_COMPANY_NAME"]
        roster = self._build_agent_roster()
        restore_summary = {
            "restored": False,
            "message": "",
            "repair_seconds": 0.0,
            "telegram_voice_sent": False,
            "telegram_message": "",
            "worker_triggered": False,
            "health_check_signal": "",
            "health_check_message": "",
            "health_check_passed": False,
            "worker_exit_code": None,
        }

        if heartbeat["status"] != "healthy":
            if dry_run:
                restore_summary["message"] = "Dry-run modunda restore simüle edildi"
            else:
                restored, restore_message, repair_seconds = self._restore_from_backup()
                restore_summary.update(
                    {
                        "restored": restored,
                        "message": restore_message,
                        "repair_seconds": repair_seconds,
                    }
                )
                telegram_sent, telegram_message = self._send_telegram_voice_alert(
                    heartbeat["error"] or "Sistem hatası", repair_seconds
                )
                restore_summary["telegram_voice_sent"] = telegram_sent
                restore_summary["telegram_message"] = telegram_message
                if restored:
                    worker_result = self._run_worker_health_check()
                    restore_summary["worker_triggered"] = worker_result.get("worker_triggered", False)
                    restore_summary["health_check_signal"] = worker_result.get("signal", "")
                    restore_summary["health_check_message"] = worker_result.get("message", "")
                    restore_summary["worker_exit_code"] = worker_result.get("exit_code")
                    restore_summary["health_check_passed"] = worker_result.get("passed", False)

                    if restore_summary["health_check_passed"]:
                        success_message = "ONARIM BAŞARILI VE SİSTEM TESTİ ONAYLANDI"
                        ok_sent, ok_message = self._send_telegram_text_message(success_message)
                        restore_summary["telegram_test_message_sent"] = ok_sent
                        restore_summary["telegram_test_message"] = ok_message
                        central_payload = {
                            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            "company_name": company,
                            "tenant_slug": self.settings["TENANT_SLUG"],
                            "event": "repair_validation_passed",
                            "status": "PASSED",
                            "message": success_message,
                            "worker_health_signal": worker_result.get("signal", "Health Check: PASSED"),
                            "worker_message": worker_result.get("message", ""),
                            "worker_exit_code": worker_result.get("exit_code"),
                        }
                        self._append_central_log(central_payload)
                    else:
                        critical_message = "CRITICAL: ONARIM YETERSİZ"
                        restore_summary["critical_message"] = critical_message
                        central_payload = {
                            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            "company_name": company,
                            "tenant_slug": self.settings["TENANT_SLUG"],
                            "event": "repair_validation_failed",
                            "status": "FAILED",
                            "message": critical_message,
                            "worker_health_signal": worker_result.get("signal", "Health Check: FAILED"),
                            "worker_message": worker_result.get("message", ""),
                            "worker_exit_code": worker_result.get("exit_code"),
                        }
                        self._append_central_log(central_payload)

        payload = {
            "company_name": company,
            "tenant_slug": self.settings["TENANT_SLUG"],
            "guardian_checked_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "heartbeat": heartbeat,
            "roster_size": len(roster),
            "restore": restore_summary,
            "project_root": str(self.project_root),
            "status": "healthy" if heartbeat["status"] == "healthy" else ("restored" if restore_summary["restored"] else "critical"),
        }
        self._write_status(payload)
        self._append_event(payload)
        return payload

    def run_forever(self, dry_run=False):
        interval = max(15, int(self.settings["GUARDIAN_HEARTBEAT_INTERVAL_SECONDS"]))
        while True:
            self.run_once(dry_run=dry_run)
            time.sleep(interval)


def main():
    parser = argparse.ArgumentParser(description="165 ajanı denetleyen Guardian Kalkanı")
    parser.add_argument("--once", action="store_true", help="Tek heartbeat döngüsü çalıştır")
    parser.add_argument("--daemon", action="store_true", help="Sürekli heartbeat döngüsü çalıştır")
    parser.add_argument("--dry-run", action="store_true", help="Restore ve Telegram akışını simüle et")
    args = parser.parse_args()

    agent = GuardianAgent()
    if args.once or not args.daemon:
        result = agent.run_once(dry_run=args.dry_run)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        agent.run_forever(dry_run=args.dry_run)


if __name__ == "__main__":
    main()
