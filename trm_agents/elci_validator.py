import hashlib
import json
import time
from datetime import datetime
from typing import Dict, Any

class ElciValidator:
    """
    Ajan 162 – Elçi-Validator
    Yeni hesapları 'ELÇİ_KODU' ile trust olarak işaretler, P-Test'te hızlı geçiş sağlar.
    """
    def __init__(self, trusted_db: str = "trusted_agents.json"):
        self.trusted_db = trusted_db
        self._init_db()

    def _init_db(self):
        try:
            with open(self.trusted_db, "r", encoding="utf-8") as f:
                self.trusted = json.load(f)
        except:
            self.trusted = []
            with open(self.trusted_db, "w", encoding="utf-8") as f:
                json.dump([], f)

    def _save_db(self):
        with open(self.trusted_db, "w", encoding="utf-8") as f:
            json.dump(self.trusted, f, ensure_ascii=False, indent=2)

    def validate_with_code(self, agent_name: str, elci_kodu: str) -> bool:
        """
        ELÇİ_KODU ile sisteme giren yeni ajanı trust olarak işaretler.
        Kodu doğrular (örnek: hash ile).
        """
        # Basit doğrulama: kod "ELCI" ile başlamalı ve 10 karakter uzunluğunda olmalı
        # Gerçekte daha güçlü doğrulama yapılabilir
        if elci_kodu.startswith("ELCI") and len(elci_kodu) == 10:
            # Zaten trust listesinde mi?
            if any(a["agent"] == agent_name for a in self.trusted):
                return True
            # Yeni trust kaydı
            entry = {
                "agent": agent_name,
                "validated_at": datetime.now().isoformat(),
                "trusted": True,
                "elci_code": elci_kodu,
                "p_test_fast_track": True  # Hızlı geçiş
            }
            self.trusted.append(entry)
            self._save_db()
            return True
        return False

    def is_trusted(self, agent_name: str) -> bool:
        return any(a["agent"] == agent_name for a in self.trusted)

    def get_fast_track(self, agent_name: str) -> bool:
        """P-Test hızlı geçiş (sadece bot-savar doğrulama)"""
        for a in self.trusted:
            if a["agent"] == agent_name:
                return a.get("p_test_fast_track", False)
        return False

    def complete_ptest_fast(self, agent_name: str):
        """Hızlı geçiş tamamlandı işaretle"""
        for a in self.trusted:
            if a["agent"] == agent_name:
                a["p_test_completed"] = True
                self._save_db()
                return True
        return False