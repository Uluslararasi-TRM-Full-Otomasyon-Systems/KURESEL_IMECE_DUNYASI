#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TRM FULL OTOMASYON - SOSYAL MEDYA KONTROL SISTEMI
Sosyal medya hesaplarini ve API anahtarlarini kontrol eder
"""

import os
import sys
import json
import logging
from datetime import datetime
from pathlib import Path

# Loglama ayarlari
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('social_media_check.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

class SocialMediaController:
    def __init__(self):
        self.system_path = Path(__file__).parent
        self.secrets_file = self.system_path / "secrets.env"
        self.config = {}
        self.social_accounts = {
            "telegram": {"configured": False, "details": {}},
            "messaging": {"configured": False, "details": {}},
            "facebook": {"configured": False, "details": {}},
            "instagram": {"configured": False, "details": {}},
            "twitter": {"configured": False, "details": {}},
            "tiktok": {"configured": False, "details": {}},
            "youtube": {"configured": False, "details": {}}
        }
        
    def load_config(self):
        """Yapilandirma dosyasini yukler"""
        try:
            with open(self.secrets_file, 'r', encoding='utf-8') as f:
                for line in f:
                    if '=' in line and not line.startswith('#'):
                        key, value = line.strip().split('=', 1)
                        self.config[key.strip()] = value.strip()
            
            logger.info("✅ Sosyal medya yapilandirmasi yuklendi")
            return True
            
        except Exception as e:
            logger.error(f"❌ Yapilandirma yuklenemedi: {e}")
            return False
            
    def check_telegram(self):
        """Telegram hesabini kontrol et"""
        if "TELEGRAM_BOT_TOKEN" in self.config:
            self.social_accounts["telegram"] = {
                "configured": True,
                "details": {
                    "bot_token": self.config["TELEGRAM_BOT_TOKEN"],
                    "api_id": self.config.get("TELEGRAM_API_ID", ""),
                    "api_hash": self.config.get("TELEGRAM_API_HASH", ""),
                    "chat_id": self.config.get("TELEGRAM_CHAT_ID", ""),
                    "status": "Aktif"
                }
            }
            logger.info("✅ Telegram hesabi yapilandirilmis")
            return True
        else:
            logger.warning("⚠️ Telegram hesabi yapilandirilmamis")
            return False
            
    def check_messaging(self):
        """Telegram/Discord/Viber hesabini kontrol et"""
        if "DISCORD_BOT_TOKEN" in self.config:
            self.social_accounts["messaging"] = {
                "configured": True,
                "details": {
                    "api_token": self.config["DISCORD_BOT_TOKEN"],
                    "phone_number": self.config.get("TELEGRAM_CHAT_ID", ""),
                    "status": "Aktif"
                }
            }
            logger.info("✅ Telegram/Discord/Viber hesabi yapilandirilmis")
            return True
        else:
            logger.warning("⚠️ Telegram/Discord/Viber hesabi yapilandirilmamis")
            return False
            
    def check_facebook(self):
        """Facebook hesabini kontrol et"""
        if "FACEBOOK_ACCESS_TOKEN" in self.config:
            self.social_accounts["facebook"] = {
                "configured": True,
                "details": {
                    "access_token": self.config["FACEBOOK_ACCESS_TOKEN"],
                    "status": "Aktif"
                }
            }
            logger.info("✅ Facebook hesabi yapilandirilmis")
            return True
        else:
            logger.warning("⚠️ Facebook hesabi yapilandirilmamis")
            return False
            
    def check_instagram(self):
        """Instagram hesabini kontrol et"""
        if "INSTAGRAM_ACCESS_TOKEN" in self.config:
            self.social_accounts["instagram"] = {
                "configured": True,
                "details": {
                    "access_token": self.config["INSTAGRAM_ACCESS_TOKEN"],
                    "status": "Aktif"
                }
            }
            logger.info("✅ Instagram hesabi yapilandirilmis")
            return True
        else:
            logger.warning("⚠️ Instagram hesabi yapilandirilmamis")
            return False
            
    def check_twitter(self):
        """Twitter hesabini kontrol et"""
        if "TWITTER_API_KEY" in self.config and "TWITTER_API_SECRET" in self.config:
            self.social_accounts["twitter"] = {
                "configured": True,
                "details": {
                    "api_key": self.config["TWITTER_API_KEY"],
                    "api_secret": self.config["TWITTER_API_SECRET"],
                    "status": "Aktif"
                }
            }
            logger.info("✅ Twitter hesabi yapilandirilmis")
            return True
        else:
            logger.warning("⚠️ Twitter hesabi yapilandirilmamis")
            return False
            
    def check_all_accounts(self):
        """Tum sosyal medya hesaplarini kontrol et"""
        logger.info("🔍 Sosyal medya hesaplari kontrol ediliyor...")
        
        accounts_status = {
            "telegram": self.check_telegram(),
            "messaging": self.check_messaging(),
            "facebook": self.check_facebook(),
            "instagram": self.check_instagram(),
            "twitter": self.check_twitter()
        }
        
        configured_count = sum(1 for status in accounts_status.values() if status)
        total_count = len(accounts_status)
        
        logger.info(f"📊 Sosyal Medya Durumu: {configured_count}/{total_count} hesap yapilandirilmis")
        
        return {
            "total_accounts": total_count,
            "configured_accounts": configured_count,
            "accounts": self.social_accounts,
            "check_time": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
    def get_account_info(self, platform: str):
        """Belirli bir platformun bilgilerini dondur"""
        return self.social_accounts.get(platform, {"configured": False, "details": {}})
        
    def get_missing_credentials(self):
        """Eksik API anahtarlarini listeler"""
        missing = []
        
        required_credentials = {
            "telegram": ["TELEGRAM_BOT_TOKEN"],
            "messaging": ["DISCORD_BOT_TOKEN"],
            "facebook": ["FACEBOOK_ACCESS_TOKEN"],
            "instagram": ["INSTAGRAM_ACCESS_TOKEN"],
            "twitter": ["TWITTER_API_KEY", "TWITTER_API_SECRET"]
        }
        
        for platform, keys in required_credentials.items():
            if not self.social_accounts[platform]["configured"]:
                missing.extend(keys)
                
        return missing
        
    def generate_report(self):
        """Sosyal medya raporu olustur"""
        status = self.check_all_accounts()
        
        report = f"""
📱 SOSYAL MEDYA KONTROL RAPORU
=====================================
📅 Kontrol Tarihi: {status['check_time']}

📊 GENEL DURUM:
• Toplam Hesap: {status['configured_accounts']}/{status['total_accounts']}
• Yapilandirma Orani: {(status['configured_accounts']/status['total_accounts']*100):.1f}%

📋 HESAP DETAYLARI:
"""
        
        for platform, account in status['accounts'].items():
            status_icon = "✅" if account['configured'] else "⚠️"
            platform_name = platform.upper()
            account_status = account['details'].get('status', 'Yapilandirilmamis')
            
            report += f"""
{status_icon} {platform_name}
  Durum: {account_status}
  Yapilandirma: {'Evet' if account['configured'] else 'Hayir'}
"""
        
        missing = self.get_missing_credentials()
        if missing:
            report += f"""
⚠️ EKSIK API ANAHTARLARI:
"""
            for key in missing:
                report += f"  • {key}\n"
                
        report += f"""
📝 GEREKLI ISLEMLER:
1. Eksik API anahtarlarini tamamlayin
2. secrets.env dosyasini guncelleyin
3. Sistemi yeniden baslatin

🔗 YARDIM:
• Telegram: BotFather'dan bot token alin
• Telegram/Discord/Viber: Business API kaydi olun
• Facebook: Developer Console'dan access token alin
• Instagram: Basic Display API'dan token alin
• Twitter: Developer Portal'dan API key alin
"""
        
        return report
        
    def save_report(self):
        """Raporu dosyaya kaydet"""
        try:
            report = self.generate_report()
            
            report_file = self.system_path / "sosyal_medya_raporu.txt"
            with open(report_file, 'w', encoding='utf-8') as f:
                f.write(report)
                
            logger.info(f"✅ Rapor kaydedildi: {report_file}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Rapor kaydedilemedi: {e}")
            return False

def main():
    """Ana fonksiyon"""
    print(">> ULUSLARASI TRM FULL OTOMASYON - SOSYAL MEDYA KONTROL")
    print("Sosyal medya hesaplarini ve API anahtarlarini kontrol eder...")
    
    controller = SocialMediaController()
    
    # Parametre kontrolu
    if len(sys.argv) > 1:
        if sys.argv[1] == "--check":
            controller.load_config()
            status = controller.check_all_accounts()
            print(f"\n📊 Sosyal Medya Durumu: {status['configured_accounts']}/{status['total_accounts']} hesap hazir")
            return
        elif sys.argv[1] == "--report":
            controller.load_config()
            if controller.save_report():
                print("✅ Sosyal medya raporu olusturuldu!")
                print("📁 Dosya: sosyal_medya_raporu.txt")
            else:
                print("❌ Rapor olusturulamadi!")
            return
        elif sys.argv[1] == "--missing":
            controller.load_config()
            missing = controller.get_missing_credentials()
            if missing:
                print("⚠️ Eksik API anahtarlari:")
                for key in missing:
                    print(f"  • {key}")
            else:
                print("✅ Tum API anahtarlari mevcut!")
            return
    
    # Normal kontrol
    controller.load_config()
    status = controller.check_all_accounts()
    
    print(f"\n📱 SOSYAL MEDYA DURUMU")
    print("=" * 50)
    print(f"Toplam Hesap: {status['configured_accounts']}/{status['total_accounts']}")
    print(f"Yapilandirma: {(status['configured_accounts']/status['total_accounts']*100):.1f}%")
    
    print("\n📋 HESAP DETAYLARI:")
    for platform, account in status['accounts'].items():
        status_icon = "✅" if account['configured'] else "⚠️"
        platform_name = platform.upper()
        account_status = account['details'].get('status', 'Yapilandirilmamis')
        print(f"{status_icon} {platform_name}: {account_status}")
    
    missing = controller.get_missing_credentials()
    if missing:
        print("\n⚠️ EKSIK API ANAHTARLARI:")
        for key in missing:
            print(f"  • {key}")
    
    controller.save_report()

if __name__ == "__main__":
    main()
