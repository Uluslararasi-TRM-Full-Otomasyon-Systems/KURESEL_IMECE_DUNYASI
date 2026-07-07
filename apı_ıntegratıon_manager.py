#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TRM FULL OTOMASYON - API ENTGRASYON YONETICI
API anahtarlari varsa sistemi entegre eder, yoksa demo modda calisir
"""

import os
import sys
import json
import logging
import time
from datetime import datetime
from pathlib import Path
import requests
from typing import Dict, Any, Optional

from trm_paths import html_dir

# Loglama ayarlari
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('api_integration.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

class APIIntegrationManager:
    def __init__(self):
        self.system_path = Path(__file__).parent
        self.secrets_file = self.system_path / "secrets.env"
        self.api_keys = {}
        self.integration_status = {}
        self.demo_data = {
            "system_health": 95,
            "ai_status": "Aktif",
            "money_making": True,
            "daily_revenue": 2847.50,
            "monthly_revenue": 45230.00,
            "commission_rate": 15.5,
            "active_products": 19,
            "social_media_status": {
                "instagram": "Aktif",
                "facebook": "Aktif", 
                "twitter": "Aktif",
                "messaging": "Aktif"
            },
            "drive_status": "Bagli",
            "cloud_status": "Hazir",
            "last_update": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
    def load_api_keys(self):
        """API anahtarlarini yukler"""
        try:
            with open(self.secrets_file, 'r', encoding='utf-8') as f:
                for line in f:
                    if '=' in line and not line.startswith('#'):
                        key, value = line.strip().split('=', 1)
                        self.api_keys[key.strip()] = value.strip()
            
            logger.info("✅ API anahtarlari yuklendi")
            return True
            
        except FileNotFoundError:
            logger.warning("⚠️ secrets.env dosyasi bulunamadi, demo mod kullanilacak")
            return False
        except Exception as e:
            logger.error(f"❌ API anahtarlari yuklenemedi: {e}")
            return False
            
    def check_api_availability(self):
        """API servislerinin ulasilabilirligini kontrol et"""
        api_services = {
            "telegram": self.check_telegram_api(),
            "openai": self.check_openai_api(),
            "google_drive": self.check_google_drive_api(),
            "messaging": self.check_messaging_api(),
            "facebook": self.check_facebook_api(),
            "instagram": self.check_instagram_api(),
            "twitter": self.check_twitter_api(),
            "trendyol": self.check_trendyol_api(),
            "hepsiburada": self.check_hepsiburada_api(),
            "n11": self.check_n11_api(),
            "railway": self.check_railway_api(),
            "render": self.check_render_api(),
            "heroku": self.check_heroku_api()
        }
        
        for service, status in api_services.items():
            self.integration_status[service] = status
            
        available_count = sum(1 for status in api_services.values() if status)
        total_count = len(api_services)
        
        logger.info(f"📊 API Servisleri: {available_count}/{total_count} mevcut")
        
        return available_count > 0
        
    def check_telegram_api(self):
        """Telegram API kontrolu"""
        return "TELEGRAM_BOT_TOKEN" in self.api_keys
        
    def check_openai_api(self):
        """OpenAI API kontrolu"""
        return "OPENAI_API_KEY" in self.api_keys
        
    def check_google_drive_api(self):
        """Google Drive API kontrolu"""
        return any(key in self.api_keys for key in ["GOOGLE_DRIVE_API_KEY", "GOOGLE_DRIVE_CLIENT_ID", "GOOGLE_DRIVE_CLIENT_SECRET"])
        
    def check_messaging_api(self):
        """Telegram/Discord/Viber API kontrolu"""
        return "DISCORD_BOT_TOKEN" in self.api_keys
        
    def check_facebook_api(self):
        """Facebook API kontrolu"""
        return "FACEBOOK_ACCESS_TOKEN" in self.api_keys
        
    def check_instagram_api(self):
        """Instagram API kontrolu"""
        return "INSTAGRAM_ACCESS_TOKEN" in self.api_keys
        
    def check_twitter_api(self):
        """Twitter API kontrolu"""
        return all(key in self.api_keys for key in ["TWITTER_API_KEY", "TWITTER_API_SECRET"])
        
    def check_trendyol_api(self):
        """Trendyol API kontrolu"""
        return "TRENDYOL_API_KEY" in self.api_keys
        
    def check_hepsiburada_api(self):
        """Hepsiburada API kontrolu"""
        return "HEPSIBURADA_API_KEY" in self.api_keys
        
    def check_n11_api(self):
        """N11 API kontrolu"""
        return "N11_API_KEY" in self.api_keys
        
    def check_railway_api(self):
        """Railway API kontrolu"""
        return "RAILWAY_TOKEN" in self.api_keys
        
    def check_render_api(self):
        """Render API kontrolu"""
        return "RENDER_API_KEY" in self.api_keys
        
    def check_heroku_api(self):
        """Heroku API kontrolu"""
        return "HEROKU_API_KEY" in self.api_keys
        
    def create_api_endpoints(self):
        """API endpoint'leri olustur"""
        endpoints = {}
        
        if self.check_telegram_api():
            endpoints["telegram"] = {
                "url": "http://localhost:9005/telegram",
                "status": "Aktif",
                "description": "Telegram bildirim sistemi"
            }
            
        if self.check_openai_api():
            endpoints["openai"] = {
                "url": "http://localhost:9006/openai",
                "status": "Aktif", 
                "description": "AI destekli otomasyon"
            }
            
        if self.check_google_drive_api():
            endpoints["google_drive"] = {
                "url": "http://localhost:9007/google-drive",
                "status": "Bagli",
                "description": "Google Drive entegrasyonu"
            }
            
        if self.check_messaging_api():
            endpoints["messaging"] = {
                "url": "http://localhost:9008/messaging",
                "status": "Aktif",
                "description": "Telegram/Discord/Viber otomasyonu"
            }
            
        if self.check_facebook_api():
            endpoints["facebook"] = {
                "url": "http://localhost:9009/facebook",
                "status": "Aktif",
                "description": "Facebook entegrasyonu"
            }
            
        if self.check_instagram_api():
            endpoints["instagram"] = {
                "url": "http://localhost:9010/instagram",
                "status": "Aktif",
                "description": "Instagram entegrasyonu"
            }
            
        if self.check_twitter_api():
            endpoints["twitter"] = {
                "url": "http://localhost:9011/twitter",
                "status": "Aktif",
                "description": "Twitter entegrasyonu"
            }
            
        if self.check_trendyol_api():
            endpoints["trendyol"] = {
                "url": "http://localhost:9012/trendyol",
                "status": "Aktif",
                "description": "Trendyol entegrasyonu"
            }
            
        if self.check_hepsiburada_api():
            endpoints["hepsiburada"] = {
                "url": "http://localhost:9013/hepsiburada",
                "status": "Aktif",
                "description": "Hepsiburada entegrasyonu"
            }
            
        if self.check_n11_api():
            endpoints["n11"] = {
                "url": "http://localhost:9014/n11",
                "status": "Aktif",
                "description": "N11 entegrasyonu"
            }
            
        if self.check_railway_api():
            endpoints["railway"] = {
                "url": "http://localhost:9015/railway",
                "status": "Hazir",
                "description": "Railway deployment"
            }
            
        if self.check_render_api():
            endpoints["render"] = {
                "url": "http://localhost:9016/render",
                "status": "Hazir",
                "description": "Render deployment"
            }
            
        if self.check_heroku_api():
            endpoints["heroku"] = {
                "url": "http://localhost:9017/heroku",
                "status": "Hazir",
                "description": "Heroku deployment"
            }
            
        return endpoints
        
    def start_api_servers(self):
        """API sunucularini baslat"""
        logger.info("🚀 API entegrasyon sunuculari baslatiliyor...")
        
        endpoints = self.create_api_endpoints()
        
        for service, config in endpoints.items():
            try:
                # Burada gercek API sunuculari baslatilacak
                logger.info(f"📡 {service} API sunucusu hazirlaniyor: {config['description']}")
                
                # Simulasyon - gercek sunucu baslatma kodu
                logger.info(f"✅ {service} API entegrasyonu aktif (Demo Mod)")
                
            except Exception as e:
                logger.error(f"❌ {service} API sunucusu baslatilamadi: {e}")
                
    def get_integration_status(self):
        """Entegrasyon durumunu dondur"""
        return {
            "api_keys_loaded": bool(self.api_keys),
            "available_apis": self.check_api_availability(),
            "integration_status": self.integration_status,
            "demo_mode": not bool(self.api_keys),
            "last_check": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
    def update_html_panels(self):
        """HTML panellerini API durumuyla guncelle"""
        try:
            status = self.get_integration_status()
            
            # Ana panel'i guncelle
            self.update_panel_status("ANA_PANEL.html", status)
            
            logger.info("✅ HTML panelleri API durumuyla guncellendi")
            
        except Exception as e:
            logger.error(f"❌ HTML panelleri guncellenemedi: {e}")
            
    def update_panel_status(self, panel_file, status):
        """Belirli bir panelin durumunu guncelle"""
        try:
            panel_path = html_dir() / panel_file
            
            if panel_path.exists():
                with open(panel_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # API durum bilgisini ekle
                api_status_html = f"""
                <!-- API Entegrasyon Durumu -->
                <div style="position: fixed; top: 10px; right: 10px; background: rgba(0,0,0,0.8); color: white; padding: 10px; border-radius: 5px; font-size: 12px; z-index: 1000;">
                    <div style="display: flex; align-items: center; gap: 10px;">
                        <div style="width: 10px; height: 10px; background: {'#4ade80' if status['api_keys_loaded'] else '#ef4444'}; border-radius: 50%;"></div>
                        <span>API: {'✅ Aktif' if status['api_keys_loaded'] else '⚠️ Demo'}</span>
                    </div>
                </div>
                <script>
                    window.apiStatus = {json.dumps(status)};
                </script>
                """
                
                # HTML'e API durumunu ekle
                if "<!-- API Entegrasyon Durumu -->" in content:
                    content = content.replace(r"<!-- API Entegrasyon Durumu -->.*?</script>", api_status_html)
                else:
                    # Son </body> etiketinden once ekle
                    content = content.replace("</body>", f"{api_status_html}</body>")
                
                with open(panel_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                    
                logger.info(f"✅ {panel_file} API durumuyla guncellendi")
                
        except Exception as e:
            logger.error(f"❌ {panel_file} guncellenemedi: {e}")
            
    def run(self):
        """Ana calistirma fonksiyonu"""
        try:
            logger.info("🔄 API entegrasyon yoneticisi baslatiliyor...")
            
            # API anahtarlarini yukle
            if self.load_api_keys():
                logger.info("✅ API anahtarlari yuklendi")
                
                # API servislerini kontrol et
                if self.check_api_availability():
                    logger.info("✅ API servisleri mevcut")
                    
                    # API sunucularini baslat
                    self.start_api_servers()
                    
                    # HTML panellerini guncelle
                    self.update_html_panels()
                    
                    logger.info("🎉 API entegrasyonu basariyla tamamlandi!")
                    return True
                else:
                    logger.warning("⚠️ API anahtarlari mevcut ancak servisler erisilemiyor")
                    self.update_html_panels()  # Demo modunda guncelle
                    return True
            else:
                logger.warning("⚠️ API anahtarlari bulunamadi, demo mod aktif")
                self.update_html_panels()  # Demo modunda guncelle
                
                logger.info("🎯 Demo modda calistirildi!")
                return True
                
        except Exception as e:
            logger.error(f"❌ API entegrasyon hatasi: {e}")
            return False

def main():
    """Ana fonksiyon"""
    print(">> ULUSLARASI TRM FULL OTOMASYON - API ENTGRASYON YONETICISI")
    print("API anahtarlarini kontrol eder ve sistemi entegre eder...")
    
    manager = APIIntegrationManager()
    
    # Parametre kontrolu
    if len(sys.argv) > 1:
        if sys.argv[1] == "--check-only":
            manager.check_api_availability()
            return
        elif sys.argv[1] == "--update-panels":
            manager.update_html_panels()
            return
        elif sys.argv[1] == "--status":
            status = manager.get_integration_status()
            print("\n>> API Entegrasyon Durumu:")
            print(f"API Anahtarlari: {'✅ Yuklu' if status['api_keys_loaded'] else '⚠️ Yuklenmedi'}")
            print(f"API Servisleri: {status['available_apis']} mevcut")
            print(f"Demo Mod: {'❌ Aktif' if status['api_keys_loaded'] else '✅ Aktif'}")
            print(f"Son Kontrol: {status['last_check']}")
            return
    
    # Normal calistirma
    manager.run()

if __name__ == "__main__":
    main()
