import os
import json
from datetime import datetime, timedelta

LOG_FILE = "conversation_log.json"

class ConversationLog:
    @staticmethod
    def _load_logs():
        if not os.path.exists(LOG_FILE):
            return []
        try:
            with open(LOG_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []

    @staticmethod
    def _save_logs(logs):
        try:
            with open(LOG_FILE, "w", encoding="utf-8") as f:
                json.dump(logs, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Log kayıt hatası: {e}")

    @classmethod
    def add_turn(cls, user_msg, bot_resp, detected_language="tr", category="genel"):
        logs = cls._load_logs()
        entry = {
            "timestamp": datetime.now().isoformat(),
            "user_msg": user_msg,
            "bot_resp": bot_resp,
            "detected_language": detected_language.lower(),
            "category": category
        }
        logs.append(entry)
        # Son 1000 logu tut, şişmeyi önle
        if len(logs) > 1000:
            logs = logs[-1000:]
        cls._save_logs(logs)

    @classmethod
    def get_last_minute_rate(cls):
        logs = cls._load_logs()
        now = datetime.now()
        one_minute_ago = now - timedelta(seconds=60)
        count = 0
        for log in logs:
            try:
                t = datetime.fromisoformat(log["timestamp"])
                if t >= one_minute_ago:
                    count += 1
            except Exception:
                continue
        return count if count > 0 else 3  # Hiç yoksa osiloskop için hareketli demo taban

    @classmethod
    def get_last_24h_grouped_by_language(cls):
        logs = cls._load_logs()
        now = datetime.now()
        cutoff = now - timedelta(hours=24)
        counts = {"tr": 0, "en": 0, "de": 0}
        
        for log in logs:
            try:
                t = datetime.fromisoformat(log["timestamp"])
                if t >= cutoff:
                    lang = log.get("detected_language", "tr")
                    if lang in counts:
                        counts[lang] += 1
                    else:
                        counts["tr"] += 1
            except Exception:
                continue
        
        # Hiç veri yoksa başlangıç oranları verelim
        if sum(counts.values()) == 0:
            return {"tr": 72, "en": 18, "de": 10}
        return counts

    @classmethod
    def get_last_24h_hourly(cls):
        # 24 saatlik dilimler için örnek saatli döküm
        return [5, 3, 2, 1, 0, 1, 4, 8, 15, 25, 30, 42, 38, 45, 50, 48, 40, 35, 30, 22, 18, 12, 8, 6]

    @classmethod
    def get_recent(cls, limit=20):
        logs = cls._load_logs()
        return logs[-limit:]