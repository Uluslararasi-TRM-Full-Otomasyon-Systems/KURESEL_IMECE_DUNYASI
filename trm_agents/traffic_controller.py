import os
import json
import time
from datetime import datetime, timedelta
from collections import defaultdict
from typing import Dict, Tuple

class TrafficController:
    """
    Rate-Limiting ve Anti-DDoS ajanı.
    IP bazlı istek sayısını izler, eşik aşılırsa engeller.
    """
    def __init__(self, log_file: str = "traffic_log.json", 
                 max_requests: int = 60, window_seconds: int = 60):
        self.log_file = log_file
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self._init_log()

    def _init_log(self):
        if not os.path.exists(self.log_file):
            with open(self.log_file, "w", encoding="utf-8") as f:
                json.dump({}, f)

    def _load_log(self) -> Dict:
        try:
            with open(self.log_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    def _save_log(self, data: Dict):
        with open(self.log_file, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def is_allowed(self, client_ip: str) -> Tuple[bool, str]:
        """
        IP'nin istek yapmasına izin verilip verilmediğini kontrol eder.
        Döner: (allow, message)
        """
        now = time.time()
        log = self._load_log()
        if client_ip not in log:
            log[client_ip] = {"requests": [], "blocked_until": 0}
        
        entry = log[client_ip]
        # Eğer blok süresi geçmemişse engelle
        if entry["blocked_until"] > now:
            return False, f"IP {client_ip} engelli, blok süresi: {datetime.fromtimestamp(entry['blocked_until'])}"

        # Zaman damgalarını temizle (pencere dışındakileri sil)
        requests = [ts for ts in entry["requests"] if ts > now - self.window_seconds]
        
        if len(requests) >= self.max_requests:
            # Eşik aşıldı, IP'yi 15 dakika blokla
            entry["blocked_until"] = now + 900
            entry["requests"] = []  # Sayaç sıfırla
            self._save_log(log)
            return False, f"Rate limit aşıldı, IP {client_ip} 15 dakika engellendi"

        # İstek ekle
        requests.append(now)
        entry["requests"] = requests
        self._save_log(log)
        return True, "İstek kabul edildi"

    def reset_block(self, client_ip: str):
        """IP'nin blokajını kaldır"""
        log = self._load_log()
        if client_ip in log:
            log[client_ip]["blocked_until"] = 0
            log[client_ip]["requests"] = []
            self._save_log(log)