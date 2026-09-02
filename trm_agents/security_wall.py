import os
import json
import time
from datetime import datetime
from typing import Tuple

class SecurityWall:
    """
    Brute-force saldırılarını önlemek için hatalı giriş denemelerini izler.
    5 başarısız denemeden sonra IP'yi 15 dakika yasaklar.
    """
    def __init__(self, log_file: str = "security_wall.json",
                 max_attempts: int = 5, block_minutes: int = 15):
        self.log_file = log_file
        self.max_attempts = max_attempts
        self.block_seconds = block_minutes * 60
        self._init_log()

    def _init_log(self):
        if not os.path.exists(self.log_file):
            with open(self.log_file, "w", encoding="utf-8") as f:
                json.dump({}, f)

    def _load_log(self) -> dict:
        try:
            with open(self.log_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    def _save_log(self, data: dict):
        with open(self.log_file, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def record_failed_attempt(self, client_ip: str) -> Tuple[bool, str]:
        """
        Başarısız giriş denemesini kaydeder.
        Eğer eşik aşılırsa IP'yi bloklar.
        Döner: (blocked, message)
        """
        now = time.time()
        log = self._load_log()
        if client_ip not in log:
            log[client_ip] = {"failed_attempts": 0, "blocked_until": 0, "last_attempt": 0}

        entry = log[client_ip]

        # Eğer blok süresi devam ediyorsa
        if entry["blocked_until"] > now:
            return True, f"IP {client_ip} hala engelli, süre: {datetime.fromtimestamp(entry['blocked_until'])}"

        # Deneme sayısını artır
        entry["failed_attempts"] += 1
        entry["last_attempt"] = now

        # Eğer eşik aşıldıysa blokla
        if entry["failed_attempts"] >= self.max_attempts:
            entry["blocked_until"] = now + self.block_seconds
            entry["failed_attempts"] = 0  # Sayaç sıfırla
            self._save_log(log)
            return True, f"Brute-force saldırısı tespit edildi, IP {client_ip} 15 dakika bloklandı."

        self._save_log(log)
        return False, f"{entry['failed_attempts']}/{self.max_attempts} başarısız deneme"

    def reset_attempts(self, client_ip: str):
        """Başarılı giriş durumunda sayaç sıfırlanır"""
        log = self._load_log()
        if client_ip in log:
            log[client_ip]["failed_attempts"] = 0
            self._save_log(log)