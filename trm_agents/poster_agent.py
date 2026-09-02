import asyncio
import json
import os
from datetime import datetime, timedelta

from social_media_automation import SocialMediaManager


class PosterAgent:
    """
    QueueAgent tarafından üretilen sosyal medya kuyruğunu okuyup
    zamanı gelen içerikleri Instagram ve Facebook'a yollar.
    """

    def __init__(self, queue_path=None):
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        self.queue_path = queue_path or os.path.join(base_dir, "sosyal_medya_kuyruk.json")
        self.social_manager = SocialMediaManager()
        self.retry_delay = timedelta(minutes=5)

    def _load_all_payloads(self):
        if not os.path.exists(self.queue_path):
            return []

        with open(self.queue_path, "r", encoding="utf-8") as f:
            payloads = json.load(f)

        return payloads if isinstance(payloads, list) else []

    def _save_all_payloads(self, payloads):
        with open(self.queue_path, "w", encoding="utf-8") as f:
            json.dump(payloads, f, ensure_ascii=False, indent=2)

    def _load_latest_queue_payload(self, context=None):
        if context and context.get("queue_payload"):
            return context.get("queue_payload")

        payloads = self._load_all_payloads()
        if not payloads:
            return None

        return payloads[-1]

    def _is_due(self, item):
        scheduled_for = item.get("scheduled_for")
        if not scheduled_for:
            return False
        scheduled_dt = datetime.strptime(scheduled_for, "%Y-%m-%d %H:%M:%S")
        return scheduled_dt <= datetime.now()

    def _is_retry_due(self, item):
        retry_after = item.get("retry_after")
        if not retry_after:
            return True
        retry_dt = datetime.strptime(retry_after, "%Y-%m-%d %H:%M:%S")
        return retry_dt <= datetime.now()

    def _build_publish_content(self, item):
        hashtags = " ".join(item.get("hashtags", []))
        link = item.get("product_url", "")
        text_parts = [item.get("post_text", "").strip(), hashtags.strip(), link.strip()]
        text = "\n\n".join(part for part in text_parts if part)
        return {
            "content": text,
            "link": link,
            "title": item.get("product_name", "TRM Sosyal Post"),
            "image_url": item.get("image_url", ""),
        }

    async def _publish_item(self, item):
        content = self._build_publish_content(item)
        results = dict(item.get("platform_results", {}))
        failed_platforms = []
        platforms_to_process = item.get("pending_platforms") or item.get("platforms", ["instagram", "facebook"])

        for platform in platforms_to_process:
            try:
                result = await self.social_manager.publish_single(platform, content)
            except Exception as exc:
                result = {"success": False, "platform": platform, "error": str(exc)}
            results[platform] = result
            if not result.get("success"):
                failed_platforms.append(platform)

        item["platform_results"] = results
        item["last_attempt_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        item["retry_count"] = int(item.get("retry_count", 0))

        if not failed_platforms:
            item["status"] = "posted"
            item["posted_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            item["retry_after"] = None
            item["pending_platforms"] = []
            item["last_error"] = None
        else:
            item["status"] = "pending_retry"
            item["retry_count"] += 1
            item["retry_after"] = (datetime.now() + self.retry_delay).strftime("%Y-%m-%d %H:%M:%S")
            item["pending_platforms"] = failed_platforms
            item["last_error"] = "; ".join(
                str(results[platform].get("error", "Bilinmeyen API hatasi")) for platform in failed_platforms
            )

        return item

    async def _publish_due_items(self, queue_payload):
        posted_items = []
        for item in queue_payload.get("items", []):
            status = item.get("status")
            if status == "posted":
                continue
            if status == "pending_retry":
                if not self._is_retry_due(item):
                    continue
            elif status != "queued":
                continue
            elif not self._is_due(item):
                continue
            posted_items.append(await self._publish_item(item))
        return posted_items

    def _run_async(self, coro):
        try:
            return asyncio.run(coro)
        except RuntimeError:
            loop = asyncio.new_event_loop()
            try:
                asyncio.set_event_loop(loop)
                return loop.run_until_complete(coro)
            finally:
                asyncio.set_event_loop(None)
                loop.close()

    def sync(self, context=None):
        queue_payload = self._load_latest_queue_payload(context)
        if not queue_payload:
            return None

        posted_items = self._run_async(self._publish_due_items(queue_payload))

        payloads = self._load_all_payloads()
        if payloads:
            payloads[-1] = queue_payload
            self._save_all_payloads(payloads)

        return {
            "processed_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "posted_count": len([item for item in posted_items if item.get("status") == "posted"]),
            "retry_count": len([item for item in posted_items if item.get("status") == "pending_retry"]),
            "failed_count": 0,
            "items": posted_items,
        }
