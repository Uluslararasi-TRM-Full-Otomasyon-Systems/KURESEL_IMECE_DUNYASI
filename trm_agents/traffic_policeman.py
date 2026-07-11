import os
import json
import time
from datetime import datetime, timedelta
from typing import Dict, List
from trm_agents.security_logger import SecurityLogger

class TrafficPoliceman:
    """
    Rate-limit (429) ve ban uyarılarını yakalar, karantina ve Emergency Stop yönetir.
    """
    def __init__(self, quarantine_file: str = "quarantine.json",
                 emergency_stop_file: str = "emergency_stop.flag"):
        self.quarantine_file = quarantine_file
        self.emergency_stop_file = emergency_stop_file
        self._init_files()

    def _init_files(self):
        if not os.path.exists(self.quarantine_file):
            with open(self.quarantine_file, "w", encoding="utf-8") as f:
                json.dump([], f)
        if not os.path.exists(self.emergency_stop_file):
            with open(self.emergency_stop_file, "w", encoding="utf-8") as f:
                json.dump({"active": False, "triggered_at": None, "reason": ""}, f)

    def _load_quarantine(self) -> List[Dict]:
        try:
            with open(self.quarantine_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return []

    def _save_quarantine(self, data: List[Dict]):
        with open(self.quarantine_file, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def quarantine_agent(self, agent_name: str, reason: str = "Rate limit (429)") -> Dict:
        """Ajanı karantinaya al (24 saat durdur)."""
        quarantine_list = self._load_quarantine()
        # Varsa eski karantinayı temizle
        quarantine_list = [q for q in quarantine_list if q.get("agent") != agent_name]
        
        entry = {
            "agent": agent_name,
            "reason": reason,
            "started_at": datetime.now().isoformat(),
            "expires_at": (datetime.now() + timedelta(hours=24)).isoformat(),
            "active": True
        }
        quarantine_list.append(entry)
        self._save_quarantine(quarantine_list)

        # SecurityLogger'a bildir
        sec_logger = SecurityLogger()
        sec_logger.log_threat(
            threat_type="rate_limit_ban_risk",
            details={
                "agent": agent_name,
                "reason": reason,
                "quarantine_until": entry["expires_at"]
            },
            severity="critical"
        )

        # Emergency Stop kontrolü – eğer 3+ ajan karantinadaysa
        active_quarantines = [q for q in quarantine_list if q.get("active", True)]
        if len(active_quarantines) >= 3:
            self.trigger_emergency_stop(f"Multiple agents (≥3) quarantined. High ban risk.")

        return entry

    def trigger_emergency_stop(self, reason: str):
        """Tüm sistemi durdur (Emergency Stop)."""
        with open(self.emergency_stop_file, "w", encoding="utf-8") as f:
            json.dump({
                "active": True,
                "triggered_at": datetime.now().isoformat(),
                "reason": reason
            }, f, ensure_ascii=False, indent=2)

        # SecurityLogger'a kritik uyarı
        sec_logger = SecurityLogger()
        sec_logger.log_threat(
            threat_type="emergency_stop",
            details={"reason": reason},
            severity="critical"
        )
        print(f"[EMERGENCY STOP] Sistem durduruldu! Sebep: {reason}")

    def is_emergency_stop(self) -> bool:
        """Emergency Stop aktif mi?"""
        try:
            with open(self.emergency_stop_file, "r", encoding="utf-8") as f:
                data = json.load(f)
            return data.get("active", False)
        except:
            return False

    def is_agent_quarantined(self, agent_name: str) -> bool:
        """Ajan karantinada mı?"""
        quarantine_list = self._load_quarantine()
        for entry in quarantine_list:
            if entry.get("agent") == agent_name and entry.get("active", True):
                expires = datetime.fromisoformat(entry["expires_at"])
                if datetime.now() < expires:
                    return True
                else:
                    # Süresi dolmuş, pasif yap
                    entry["active"] = False
                    self._save_quarantine(quarantine_list)
        return False

    def handle_429(self, agent_name: str, response_data: Dict = None) -> None:
        """429 yanıtı ile karşılaşıldığında çağrılır."""
        reason = "Rate limit (429) detected"
        if response_data:
            reason += f" - {response_data}"
        self.quarantine_agent(agent_name, reason)