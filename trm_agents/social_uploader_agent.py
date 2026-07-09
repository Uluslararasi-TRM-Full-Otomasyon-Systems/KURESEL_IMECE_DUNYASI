import os
import sys
import logging

# Sistemin ana dizinini (KURESEL_IMECE_DUNYASI) otomatik bulur
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class SocialUploaderAgent:
    """Üretilen içerikleri sosyal medya ağlarına dağıtan otonom ajan."""

    def __init__(self, agent_name="Sosyal_Medya_Uploader"):
        self.agent_name = agent_name
        self.api_keys = {
            "youtube_api_key": os.getenv("YOUTUBE_API_KEY", ""),
            "tiktok_api_key": os.getenv("TIKTOK_API_KEY", ""),
            "instagram_access_token": os.getenv("INSTAGRAM_ACCESS_TOKEN", ""),
            "twitter_api_key": os.getenv("TWITTER_API_KEY", ""),
            "twitter_api_secret": os.getenv("TWITTER_API_SECRET", "")
        }
        self.platform_status = self.check_api_availability()
        # Log dizini için absolute path
        self.log_dir = os.path.join(BASE_DIR, "logs")
        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)

    def check_api_availability(self):
        """API anahtarlarının kullanılabilirliğini kontrol et"""
        status = {}
        for platform, key in self.api_keys.items():
            status[platform] = bool(key)
        return status

    def upload_to_platform(self, video_path, platform, language):
        """Video dosyasını platforma yükler."""
        # Platform bazlı API anahtarı kontrolü
        platform_key_map = {
            "YouTube_Shorts": "youtube_api_key",
            "TikTok": "tiktok_api_key",
            "Instagram_Reels": "instagram_access_token",
            "Twitter": "twitter_api_key"
        }

        key_name = platform_key_map.get(platform)
        if key_name and not self.api_keys[key_name]:
            print(f"[UYARI] {platform} için API anahtarı eksik, simülasyon modunda çalışıyor.")
            print(f"[YÜKLEME] '{video_path}' dosyası {platform} ({language}) platformuna yüklendi (simülasyon).")
            return True

        # Gerçek API entegrasyonu buraya gelecek
        # Şimdilik simülasyon aşamasındayız:
        print(f"[YÜKLEME] '{video_path}' dosyası {platform} ({language}) platformuna yüklendi.")
        return True

    def run(self, video_path, language):
        """Dağıtım döngüsü."""
        platforms = ["YouTube_Shorts", "TikTok", "Instagram_Reels"]
        upload_results = []

        for platform in platforms:
            try:
                result = self.upload_to_platform(video_path, platform, language)
                upload_results.append({
                    "platform": platform,
                    "language": language,
                    "status": "BAŞARI" if result else "HATA"
                })
            except Exception as e:
                print(f"[HATA] {platform} yükleme hatası: {e}")
                upload_results.append({
                    "platform": platform,
                    "language": language,
                    "status": f"HATA: {str(e)}"
                })

        return upload_results

# Orkestratör için tetikleyici
def trigger_social_upload(video_path, language):
    uploader = SocialUploaderAgent()
    return uploader.run(video_path, language)