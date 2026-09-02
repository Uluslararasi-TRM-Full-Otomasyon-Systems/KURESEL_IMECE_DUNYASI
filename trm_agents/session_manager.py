import os
import json
import time
import random
from datetime import datetime, timedelta
from typing import Dict, Any, Optional
from trm_agents.vault_agent import VaultAgent
from trm_agents.fingerprint_manager import FingerprintManager

class SessionManager:
    """
    Proxy + Session persistence. 
    Her ajan için sabit bir profil ve uzun ömürlü session sağlar.
    """
    def __init__(self, session_dir: str = "sessions", vault: Optional[VaultAgent] = None):
        self.session_dir = session_dir
        os.makedirs(self.session_dir, exist_ok=True)
        self.vault = vault or VaultAgent()
        self.fingerprint = FingerprintManager()
        self.session_lifetime_hours = random.randint(24, 72)  # 1-3 gün

    def _get_session_file(self, agent_name: str) -> str:
        return os.path.join(self.session_dir, f"{agent_name}_session.json")

    def create_session(self, agent_name: str, proxy: Dict[str, str] = None) -> Dict[str, Any]:
        """Yeni bir session oluşturur."""
        profile = self.fingerprint.get_profile(agent_name)
        session_id = f"session_{agent_name}_{int(time.time())}"
        session = {
            "session_id": session_id,
            "agent_name": agent_name,
            "created_at": datetime.now().isoformat(),
            "expires_at": (datetime.now() + timedelta(hours=self.session_lifetime_hours)).isoformat(),
            "profile": profile,
            "proxy": proxy or {},
            "cookies": {},
            "local_storage": {},
            "active": True
        }
        # Şifrele ve kaydet
        encrypted = self.vault.encrypt(json.dumps(session))
        with open(self._get_session_file(agent_name), "w", encoding="utf-8") as f:
            json.dump({"encrypted": encrypted}, f)
        return session

    def get_session(self, agent_name: str) -> Optional[Dict[str, Any]]:
        """Ajanın mevcut session'ını getirir, süresi dolmuşsa yeniler."""
        session_file = self._get_session_file(agent_name)
        if not os.path.exists(session_file):
            return self.create_session(agent_name)

        try:
            with open(session_file, "r", encoding="utf-8") as f:
                data = json.load(f)
            session_json = self.vault.decrypt(data["encrypted"])
            session = json.loads(session_json)
            # Süre kontrolü
            expires = datetime.fromisoformat(session["expires_at"])
            if datetime.now() > expires:
                # Session süresi dolmuş, yenile
                return self.refresh_session(agent_name)
            return session
        except Exception as e:
            # Hata durumunda yeni session
            return self.create_session(agent_name)

    def refresh_session(self, agent_name: str) -> Dict[str, Any]:
        """Mevcut session'ı yeniler (yeni IP/User-Agent alabilir)."""
        # Önce eski session'ı kapat
        self.close_session(agent_name)
        # Yeni profil oluştur (farklı fingerprint)
        return self.create_session(agent_name)

    def close_session(self, agent_name: str):
        """Session'ı kapat (karantina veya sistem kapatma)."""
        session_file = self._get_session_file(agent_name)
        if os.path.exists(session_file):
            os.remove(session_file)

    def update_cookies(self, agent_name: str, cookies: Dict[str, str]):
        """Session'a cookie ekler/günceller."""
        session = self.get_session(agent_name)
        if not session:
            return
        session["cookies"].update(cookies)
        self._save_session(agent_name, session)

    def _save_session(self, agent_name: str, session: Dict[str, Any]):
        encrypted = self.vault.encrypt(json.dumps(session))
        with open(self._get_session_file(agent_name), "w", encoding="utf-8") as f:
            json.dump({"encrypted": encrypted}, f)