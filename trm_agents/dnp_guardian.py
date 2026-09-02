import time
import json
import random
from datetime import datetime, timedelta
from typing import Dict, Any

class DNPGuardian:
    """
    Ajan 161 – DNP-Guardian
    Tüm ağ trafiğini Trust Score bazlı denetler, şüpheli hareketleri karantinaya alır.
    """
    def __init__(self, trust_threshold: int = 70, quarantine_duration: int = 60):
        self.trust_threshold = trust_threshold  # 0-100
        self.quarantine_duration = quarantine_duration  # dakika
        self.trust_scores = {}  # agent_name -> score
        self.quarantine_list = {}  # agent_name -> until_timestamp

    def evaluate_trust(self, agent_name: str, activity_log: Dict[str, Any]) -> int:
        """
        Ajanın aktivite geçmişine göre Trust Score hesaplar.
        """
        score = 100
        # Hata oranı düşürür
        errors = activity_log.get("error_count", 0)
        if errors > 5:
            score -= errors * 2
        # Ani trafik artışı düşürür
        traffic_spike = activity_log.get("traffic_spike", False)
        if traffic_spike:
            score -= 20
        # Sürekli başarılı işlemler artırır
        success_rate = activity_log.get("success_rate", 0.95)
        if success_rate > 0.98:
            score += 10
        # Yeni ajanlar daha düşük başlangıç skoru alır
        if activity_log.get("age_days", 0) < 7:
            score -= 15
        # Karantina geçmişi
        if agent_name in self.quarantine_list:
            score -= 30
        return max(0, min(100, score))

    def check_and_quarantine(self, agent_name: str, activity_log: Dict[str, Any]) -> bool:
        """
        Trust Score eşiğin altına düşerse ajanı karantinaya alır.
        Döner: True = karantina uygulandı
        """
        score = self.evaluate_trust(agent_name, activity_log)
        self.trust_scores[agent_name] = score
        if score < self.trust_threshold:
            until = datetime.now() + timedelta(minutes=self.quarantine_duration)
            self.quarantine_list[agent_name] = until.timestamp()
            # Karantina log'u
            with open("quarantine.json", "r+", encoding="utf-8") as f:
                try:
                    data = json.load(f)
                except:
                    data = []
                data.append({
                    "agent": agent_name,
                    "reason": f"Trust Score {score} < {self.trust_threshold}",
                    "started_at": datetime.now().isoformat(),
                    "expires_at": until.isoformat(),
                    "active": True
                })
                f.seek(0)
                json.dump(data, f, ensure_ascii=False, indent=2)
            return True
        return False

    def is_quarantined(self, agent_name: str) -> bool:
        if agent_name in self.quarantine_list:
            if time.time() < self.quarantine_list[agent_name]:
                return True
            else:
                del self.quarantine_list[agent_name]
        return False

    def run_guardian_cycle(self, agents_status: Dict[str, Dict]):
        """Tüm ajanların aktivite loglarını kontrol eder."""
        for agent_name, log in agents_status.items():
            if self.check_and_quarantine(agent_name, log):
                print(f"[DNP-Guardian] {agent_name} karantinaya alındı.")