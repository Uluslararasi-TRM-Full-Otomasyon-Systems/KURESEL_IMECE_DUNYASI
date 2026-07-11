import json
import os
import socket
from datetime import datetime, timedelta

from notification_utils import send_email_message
from social_media_automation import SocialMediaManager


class HealthCheckAgent:
    """
    Ajan zinciri, kuyruk ve API baglanti durumunu ozetleyip
    Notification katmani uzerinden periyodik saglik raporu yollar.
    """

    def __init__(self, queue_path=None, state_path=None, base_dir=None, interval_minutes=30):
        self.base_dir = base_dir or os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        self.queue_path = queue_path or os.path.join(self.base_dir, "sosyal_medya_kuyruk.json")
        self.state_path = state_path or os.path.join(self.base_dir, "healthcheck_status.json")
        self.interval = timedelta(minutes=interval_minutes)
        self.social_manager = SocialMediaManager()

    def _load_latest_queue(self):
        if not os.path.exists(self.queue_path):
            return None
        try:
            with open(self.queue_path, "r", encoding="utf-8") as f:
                payloads = json.load(f)
            if isinstance(payloads, list) and payloads:
                return payloads[-1]
        except Exception:
            return None
        return None

    def _load_state(self):
        if not os.path.exists(self.state_path):
            return {}
        try:
            with open(self.state_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}

    def _save_state(self, state):
        with open(self.state_path, "w", encoding="utf-8") as f:
            json.dump(state, f, ensure_ascii=False, indent=2)

    def _is_due(self):
        state = self._load_state()
        last_sent = state.get("last_sent_at")
        if not last_sent:
            return True
        last_dt = datetime.strptime(last_sent, "%Y-%m-%d %H:%M:%S")
        return datetime.now() - last_dt >= self.interval

    def _check_internet(self):
        try:
            socket.create_connection(("8.8.8.8", 53), timeout=3).close()
            return True
        except OSError:
            return False

    def _summarize_queue(self, queue_payload):
        if not queue_payload:
            return {"queued": 0, "posted": 0, "pending_retry": 0}

        items = queue_payload.get("items", [])
        return {
            "queued": len([item for item in items if item.get("status") == "queued"]),
            "posted": len([item for item in items if item.get("status") == "posted"]),
            "pending_retry": len([item for item in items if item.get("status") == "pending_retry"]),
        }

    def build_report(self, context=None):
        queue_payload = None
        security_status = {}
        sentinel_alerts = []
        market_reports = []
        bridge_reports = []
        capacity_snapshot = {}
        if context:
            queue_payload = context.get("queue_payload")
            security_status = context.get("security_status", {})
            sentinel_alerts = context.get("sentinel_alerts", [])
            market_reports = context.get("market_intelligence_reports", [])
            bridge_reports = context.get("bridge_network_reports", [])
            capacity_snapshot = context.get("agent_capacity_snapshot", {})
        if not queue_payload:
            queue_payload = self._load_latest_queue()

        agent_names = []
        if context:
            agent_names = context.get("active_agents", [])

        api_status = self.social_manager.get_platform_status()
        queue_summary = self._summarize_queue(queue_payload)
        internet_ok = self._check_internet()

        return {
            "checked_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "internet_ok": internet_ok,
            "active_agents": agent_names,
            "queue_summary": queue_summary,
            "api_status": api_status,
            "security_status": security_status,
            "sentinel_alerts": sentinel_alerts,
            "market_signal_count": len(market_reports),
            "bridge_sync_count": len(bridge_reports),
            "agent_capacity_snapshot": capacity_snapshot,
        }

    def _build_email_body(self, report):
        return (
            "TRM HealthCheckAgent Raporu\n\n"
            f"Kontrol Zamani: {report['checked_at']}\n"
            f"Internet: {'OK' if report['internet_ok'] else 'HATA'}\n"
            f"Aktif Ajanlar: {', '.join(report['active_agents']) or 'Bilinmiyor'}\n"
            f"Kuyruk - queued: {report['queue_summary']['queued']}, "
            f"posted: {report['queue_summary']['posted']}, "
            f"pending_retry: {report['queue_summary']['pending_retry']}\n"
            f"API Durumu: {report['api_status']}\n"
            f"Pazar Istihbarat Sinyali: {report['market_signal_count']}\n"
            f"Bridge Senkronu: {report['bridge_sync_count']}\n"
            f"Sentinel Uyari: {len(report['sentinel_alerts'])}\n"
            f"Toplam Ajan Kapasitesi: {report['agent_capacity_snapshot'].get('total_capacity', '-')}\n"
            f"Zero-Trust: {report['security_status'].get('zero_trust_enabled')}\n"
            f"Stealth Mode: {report['security_status'].get('stealth_mode_enabled')}\n"
            f"Sifreli Snapshot: {report['security_status'].get('encrypted_snapshots')}\n"
        )

    def sync(self, context=None):
        report = self.build_report(context)
        result = {
            "checked_at": report["checked_at"],
            "sent": False,
            "report": report,
        }

        if not self._is_due():
            return result

        subject = "TRM HealthCheck Ozeti"
        body = self._build_email_body(report)
        success, message = send_email_message(subject, body, self.base_dir)

        state = {
            "last_sent_at": report["checked_at"] if success else self._load_state().get("last_sent_at"),
            "last_status": "sent" if success else "pending_retry",
            "last_message": message,
        }
        self._save_state(state)

        result["sent"] = success
        result["message"] = message
        return result
