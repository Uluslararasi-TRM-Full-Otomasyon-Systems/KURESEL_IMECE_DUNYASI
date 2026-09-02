import os
import json
from datetime import datetime
from typing import Dict

class SecurityLogger:
    """Siber tehditleri security_threats.json dosyasına loglar."""
    def __init__(self, log_file: str = "security_threats.json"):
        self.log_file = log_file
        self._init_log()

    def _init_log(self):
        if not os.path.exists(self.log_file):
            with open(self.log_file, "w", encoding="utf-8") as f:
                json.dump([], f)

    def log_threat(self, threat_type: str, details: Dict, severity: str = "critical"):
        """Tehdit kaydı ekler."""
        try:
            with open(self.log_file, "r", encoding="utf-8") as f:
                data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            data = []

        entry = {
            "timestamp": datetime.now().isoformat(),
            "threat_type": threat_type,
            "details": details,
            "severity": severity,
            "resolved": False
        }
        data.append(entry)
        # Son 500 kayıt tut
        data = data[-500:]
        with open(self.log_file, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def get_active_threats(self, limit: int = 20) -> list:
        """Çözülmemiş tehditleri döndürür."""
        try:
            with open(self.log_file, "r", encoding="utf-8") as f:
                data = json.load(f)
            return [t for t in data if not t.get("resolved", False)][-limit:]
        except:
            return []