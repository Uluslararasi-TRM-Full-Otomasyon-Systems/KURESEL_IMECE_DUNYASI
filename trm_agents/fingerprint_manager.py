import random
import json
import os
from typing import Dict, Any

class FingerprintManager:
    """Gelişmiş cihaz parmak izi yönetimi – her ajan için sabit bir profil."""
    def __init__(self, profile_dir: str = "fingerprints"):
        self.profile_dir = profile_dir
        os.makedirs(self.profile_dir, exist_ok=True)

    def _generate_random_profile(self) -> Dict[str, Any]:
        """Rastgele ama tutarlı bir profil oluşturur."""
        # Popüler User-Agent'ler (masaüstü ve mobil)
        user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/121.0",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_2_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Safari/605.1.15",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (iPhone; CPU iPhone OS 17_2_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Mobile/15E148 Safari/604.1",
            "Mozilla/5.0 (Android 14; Mobile; rv:109.0) Gecko/121.0 Firefox/121.0",
        ]
        # Ekran çözünürlükleri (yaygın)
        screen_resolutions = [
            "1920x1080", "1366x768", "1440x900", "1536x864", "2560x1440", "1280x720", "375x812"
        ]
        # Platformlar
        platforms = ["Windows", "macOS", "Linux", "iOS", "Android"]
        # Diller
        languages = ["tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7",
                     "en-US,en;q=0.9",
                     "tr-TR,tr;q=0.9,en;q=0.8",
                     "en-GB,en;q=0.9"]
        # Canvas fingerprint – rastgele bir hex string (32 karakter)
        canvas_fp = ''.join(random.choices('0123456789abcdef', k=32))

        return {
            "user_agent": random.choice(user_agents),
            "screen_resolution": random.choice(screen_resolutions),
            "platform": random.choice(platforms),
            "language": random.choice(languages),
            "canvas_fingerprint": canvas_fp,
            "timezone": random.choice(["Europe/Istanbul", "Europe/London", "America/New_York", "Asia/Dubai"]),
            "headers": {
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
                "Accept-Encoding": "gzip, deflate, br",
                "Accept-Language": random.choice(languages),
                "Cache-Control": "no-cache",
                "Sec-Ch-Ua": f'"Google Chrome";v="120", "Chromium";v="120", "Not=A?Brand";v="24"',
                "Sec-Ch-Ua-Mobile": "?0" if "Mobile" not in random.choice(user_agents) else "?1",
                "Sec-Ch-Ua-Platform": f'"{random.choice(platforms)}"',
            }
        }

    def get_profile(self, agent_name: str) -> Dict[str, Any]:
        """Ajan için sabit profili döndürür; yoksa oluşturur."""
        profile_path = os.path.join(self.profile_dir, f"{agent_name}.json")
        if os.path.exists(profile_path):
            with open(profile_path, "r", encoding="utf-8") as f:
                return json.load(f)
        else:
            profile = self._generate_random_profile()
            with open(profile_path, "w", encoding="utf-8") as f:
                json.dump(profile, f, ensure_ascii=False, indent=2)
            return profile

    def update_headers(self, agent_name: str, extra_headers: Dict[str, str] = None) -> Dict[str, str]:
        """Ajanın header'larını günceller (isteğe bağlı eklemeler)"""
        profile = self.get_profile(agent_name)
        headers = profile.get("headers", {}).copy()
        if extra_headers:
            headers.update(extra_headers)
        return headers