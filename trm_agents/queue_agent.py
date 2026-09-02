import json
import os
from datetime import datetime, timedelta


class QueueAgent:
    """
    Content_Generator_Agent çıktısını okuyup sosyal medya paylaşım kuyruğuna aktarır.
    """

    def __init__(self, content_path=None, queue_path=None):
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        self.content_path = content_path or os.path.join(base_dir, "content_generator_outputs.json")
        self.queue_path = queue_path or os.path.join(base_dir, "sosyal_medya_kuyruk.json")
        self.retry_delay = timedelta(minutes=5)

    def _load_latest_content_payload(self, context=None):
        if context and context.get("content_payload"):
            return context.get("content_payload")

        if not os.path.exists(self.content_path):
            return None

        with open(self.content_path, "r", encoding="utf-8") as f:
            payloads = json.load(f)

        if isinstance(payloads, list) and payloads:
            return payloads[-1]

        return None

    def build_queue(self, content_payload):
        if not content_payload:
            return None

        created_at = datetime.now()
        queue_items = []
        for index, item in enumerate(content_payload.get("contents", []), start=1):
            scheduled_for = created_at + timedelta(minutes=(index - 1) * 30)
            queue_items.append(
                {
                    "queue_id": f"POST_{created_at.strftime('%Y%m%d_%H%M%S')}_{index}",
                    "created_at": created_at.strftime("%Y-%m-%d %H:%M:%S"),
                    "scheduled_for": scheduled_for.strftime("%Y-%m-%d %H:%M:%S"),
                    "status": "queued",
                    "product_name": item.get("product_name"),
                    "commission_rate": item.get("commission_rate", 0.0),
                    "estimated_commission": item.get("estimated_commission", 0.0),
                    "post_text": item.get("social_post"),
                    "hashtags": item.get("hashtags", []),
                    "product_url": item.get("product_url", ""),
                    "platforms": ["instagram", "facebook"],
                    "platform_results": {},
                    "posted_at": None,
                    "retry_count": 0,
                    "retry_after": None,
                    "last_error": None,
                }
            )

        queue_items.sort(key=lambda item: item["scheduled_for"])
        return {
            "generated_at": created_at.strftime("%Y-%m-%d %H:%M:%S"),
            "source_report_timestamp": content_payload.get("source_report_timestamp"),
            "status": "ready",
            "retry_count": 0,
            "retry_after": None,
            "last_error": None,
            "items": queue_items,
        }

    def save_queue(self, queue_payload):
        if not queue_payload:
            return False

        existing_payloads = []
        if os.path.exists(self.queue_path):
            try:
                with open(self.queue_path, "r", encoding="utf-8") as f:
                    existing_payloads = json.load(f)
                if not isinstance(existing_payloads, list):
                    existing_payloads = []
            except Exception:
                existing_payloads = []

        existing_payloads.append(queue_payload)
        existing_payloads = existing_payloads[-20:]

        with open(self.queue_path, "w", encoding="utf-8") as f:
            json.dump(existing_payloads, f, ensure_ascii=False, indent=2)

        return True

    def _mark_pending_retry(self, queue_payload, error_message):
        queue_payload["status"] = "pending_retry"
        queue_payload["retry_count"] = int(queue_payload.get("retry_count", 0)) + 1
        queue_payload["last_error"] = error_message
        queue_payload["retry_after"] = (datetime.now() + self.retry_delay).strftime("%Y-%m-%d %H:%M:%S")
        return queue_payload

    def _is_retry_due(self, queue_payload):
        retry_after = queue_payload.get("retry_after")
        if not retry_after:
            return True
        retry_dt = datetime.strptime(retry_after, "%Y-%m-%d %H:%M:%S")
        return retry_dt <= datetime.now()

    def get_latest_queue(self):
        if not os.path.exists(self.queue_path):
            return None

        with open(self.queue_path, "r", encoding="utf-8") as f:
            payloads = json.load(f)

        if isinstance(payloads, list) and payloads:
            return payloads[-1]

        return None

    def sync(self, context=None):
        content_payload = self._load_latest_content_payload(context)
        if not content_payload:
            return None

        latest_queue = self.get_latest_queue()
        if latest_queue and latest_queue.get("source_report_timestamp") == content_payload.get("source_report_timestamp"):
            if latest_queue.get("status") != "pending_retry" or not self._is_retry_due(latest_queue):
                return latest_queue

        queue_payload = self.build_queue(content_payload)
        if not queue_payload:
            return None

        try:
            self.save_queue(queue_payload)
            return queue_payload
        except Exception as exc:
            return self._mark_pending_retry(queue_payload, str(exc))
