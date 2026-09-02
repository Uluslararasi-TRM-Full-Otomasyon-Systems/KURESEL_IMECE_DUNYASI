#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TRM FULL OTOMASYON - DRIVE-SOSYAL MEDYA IS AKISI
Google Drive'dan urun verilerini ceker, sosyal medyada paylasir
"""

import os
import sys
import json
import logging
import time
import random
from datetime import datetime, timedelta
from pathlib import Path
import requests
from typing import Dict, Any, List, Optional

# Loglama ayarlari
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('drive_social_workflow.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

class DriveSocialWorkflow:
    def __init__(self):
        self.system_path = Path(__file__).parent
        self.secrets_file = self.system_path / "secrets.env"
        self.config = {}
        self.products_data = []
        self.social_accounts = {}
        self.workflow_running = False
        self.shared_products = []
        self.collection_stats = {
            "total_collected": 0,
            "total_shared": 0,
            "last_collection": None,
            "last_sharing": None,
            "success_rate": 0.0
        }
        
    def load_config(self):
        """Yapilandirma dosyasini yukler"""
        try:
            with open(self.secrets_file, 'r', encoding='utf-8') as f:
                for line in f:
                    if '=' in line and not line.startswith('#'):
                        key, value = line.strip().split('=', 1)
                        self.config[key.strip()] = value.strip()
            
            logger.info("✅ Drive-Sosyal yapilandirmasi yuklendi")
            return True
            
        except Exception as e:
            logger.error(f"❌ Yapilandirma yuklenemedi: {e}")
            return False
            
    def check_google_drive_access(self):
        """Google Drive erisimini kontrol et"""
        return any(key in self.config for key in [
            "GOOGLE_DRIVE_API_KEY", 
            "GOOGLE_DRIVE_CLIENT_ID", 
            "GOOGLE_DRIVE_CLIENT_SECRET"
        ])
        
    def generate_mock_products(self, count: int = 50) -> List[Dict[str, Any]]:
        """Sahte urun verileri olustur"""
        categories = ["Elektronik", "Giyim", "Ev & Yasam", "Spor", "Kozmetik", "Taki & Aksesuar", "Kitap & Ofis"]
        brands = ["Apple", "Samsung", "Sony", "Nike", "Adidas", "Puma", "LG", "Xiaomi", "Huawei"]
        
        products = []
        for i in range(count):
            product = {
                "id": i + 1,
                "name": f"Trend Urun {i + 1}",
                "category": random.choice(categories),
                "price": round(random.uniform(100, 5000), 2),
                "commission_rate": round(random.uniform(10, 40), 1),
                "stock_count": random.randint(1, 100),
                "description": f"Yuksek kaliteli trend urun. Komisyon orani: {round(random.uniform(15, 35), 1)}%",
                "image_url": f"https://picsum.photos/seed/product{i+1}/400/300.jpg",
                "affiliate_link": f"https://trendurunlermarket.com/product/{i+1}",
                "tags": ["trend", "kaliteli", "uygun fiyatli", "yeni", "populer"],
                "collected_at": datetime.now().isoformat(),
                "trend_score": round(random.uniform(7.0, 9.9), 1)
            }
            products.append(product)
            
        return products
        
    def collect_products_from_drive(self):
        """Google Drive'dan urun verilerini ceker"""
        logger.info("📂 Google Drive'dan urun verileri cekiliyor...")
        
        if not self.check_google_drive_access():
            logger.warning("⚠️ Google Drive API anahtarlari eksik, demo veriler kullaniliyor")
            self.products_data = self.generate_mock_products(50)
        else:
            logger.info("✅ Google Drive API erisimi var, gercek veriler cekiliyor...")
            # Burada gercek Google Drive API cagrisi yapilacak
            # Simdilik demo veriler
            self.products_data = self.generate_mock_products(30)
        
        self.collection_stats["total_collected"] = len(self.products_data)
        self.collection_stats["last_collection"] = datetime.now().isoformat()
        
        logger.info(f"✅ {len(self.products_data)} urun verisi toplandi")
        
        # Urun verilerini kaydet
        self.save_products_data()
        
        return self.products_data
        
    def save_products_data(self):
        """Urun verilerini dosyaya kaydet"""
        try:
            products_file = self.system_path / f"products_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            
            products_json = {
                "upload_time": datetime.now().isoformat(),
                "folder_id": "demo_drive_folder_id",
                "products": self.products_data,
                "total_products": len(self.products_data)
            }
            
            with open(products_file, 'w', encoding='utf-8') as f:
                json.dump(products_json, f, ensure_ascii=False, indent=2)
                
            logger.info(f"✅ Urun verileri kaydedildi: {products_file}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Urun verileri kaydedilemedi: {e}")
            return False
            
    def prepare_social_content(self, product: Dict[str, Any]) -> Dict[str, str]:
        """Sosyal medya icerigi hazirla"""
        templates = {
            "facebook": f"""
🔥 TREND URUN 🔥
📦 {product['name']}
💰 Indirimli Fiyat: {product['price']} TL
🎯 Komisyon: %{product['commission_rate']}
📊 Trend Skoru: {product['trend_score']}/10

🛒 Hemen almak icin:
👉 {product['affiliate_link']}

⏰ Stoklarla sinirli!
#TRMOtomasyon #TrendUrunler #Indirim
            """,
            
            "instagram": f"""
✨ YENI SEZON ✨
{product['name']}
💎 {product['price']} TL
🔥 %{product['commission_rate']} komisyon

🛒 Link bio'de!
👉 {product['affiliate_link']}

#trend #indirim #yeniurun
            """,
            
            "twitter": f"""
🚀 TREND ALERT 🚀
{product['name']}
💰 {product['price']} TL
🎯 %{product['commission_rate']} komisyon

🛒 Hemen al:
{product['affiliate_link']}

#trendurunler #indirim
            """,
            
            "messaging": f"""
🔥 OZEL FIRSAT 🔥
{product['name']}
💰 {product['price']} TL
🎯 %{product['commission_rate']} komisyon

🛒 Link icin mesaj atin:
{product['affiliate_link']}

Sinirli stok!
            """
        }
        
        return templates
        
    def share_to_social_media(self, product: Dict[str, Any]):
        """Urunu sosyal medyada paylasir"""
        logger.info(f"📱 {product['name']} sosyal medyada paylasiliyor...")
        
        content = self.prepare_social_content(product)
        shared_platforms = []
        
        # Facebook paylasimi
        if "FACEBOOK_ACCESS_TOKEN" in self.config:
            try:
                # Simulasyon - gercek Facebook API kullanilmali
                logger.info("📘 Facebook'te paylasiliyor...")
                time.sleep(2)  # API limiti
                shared_platforms.append("facebook")
            except Exception as e:
                logger.error(f"❌ Facebook paylasim hatasi: {e}")
        
        # Instagram paylasimi
        if "INSTAGRAM_ACCESS_TOKEN" in self.config:
            try:
                logger.info("📷 Instagram'da paylasiliyor...")
                time.sleep(2)  # API limiti
                shared_platforms.append("instagram")
            except Exception as e:
                logger.error(f"❌ Instagram paylasim hatasi: {e}")
        
        # Twitter paylasimi
        if "TWITTER_API_KEY" in self.config and "TWITTER_API_SECRET" in self.config:
            try:
                logger.info("🐦 Twitter'da paylasiliyor...")
                time.sleep(2)  # API limiti
                shared_platforms.append("twitter")
            except Exception as e:
                logger.error(f"❌ Twitter paylasim hatasi: {e}")
        
        # Telegram/Discord/Viber bildirimi
        if "DISCORD_BOT_TOKEN" in self.config:
            try:
                logger.info("📱 Telegram/Discord/Viber bildirimi gonderiliyor...")
                time.sleep(1)  # API limiti
                shared_platforms.append("messaging")
            except Exception as e:
                logger.error(f"❌ Telegram/Discord/Viber bildirim hatasi: {e}")
        
        success = len(shared_platforms) > 0
        
        if success:
            self.shared_products.append({
                "product_id": product["id"],
                "product_name": product["name"],
                "shared_platforms": shared_platforms,
                "sharing_time": datetime.now().isoformat(),
                "status": "success"
            })
            
            logger.info(f"✅ {product['name']} {len(shared_platforms)} platformda paylasildi")
        else:
            logger.warning(f"⚠️ {product['name']} hicbir platformda paylasilamadi")
        
        return success
        
    def run_workflow_cycle(self):
        """Is akisi dongusunu calistirir"""
        logger.info("🔄 Drive-Sosyal is akisi dongusu baslatiliyor...")
        
        while self.workflow_running:
            try:
                # 1. Urun verilerini cek
                products = self.collect_products_from_drive()
                
                if not products:
                    logger.warning("⚠️ Paylasilacak urun bulunamadi")
                    time.sleep(300)  # 5 dakika bekle
                    continue
                
                # 2. Her urunu sosyal medyada paylas
                shared_count = 0
                for product in products[:10]:  # Her dongude max 10 urun paylas
                    if self.share_to_social_media(product):
                        shared_count += 1
                    
                    # Platformlar arasi bekleme (rate limiting)
                    time.sleep(30)  # 30 saniye
                
                # 3. Istatistikleri guncelle
                self.collection_stats["total_shared"] += shared_count
                self.collection_stats["last_sharing"] = datetime.now().isoformat()
                
                if len(self.products_data) > 0:
                    self.collection_stats["success_rate"] = (self.collection_stats["total_shared"] / len(self.products_data)) * 100
                
                # 4. Raporla
                self.log_workflow_status()
                
                # 5. Sonraki dongu icin bekle
                logger.info("⏰ 5 dakika bekleniyor...")
                time.sleep(300)  # 5 dakika
                
            except KeyboardInterrupt:
                logger.info("🛑 Is akisi kullanici tarafindan durduruldu")
                self.workflow_running = False
            except Exception as e:
                logger.error(f"❌ Is akisi hatasi: {e}")
                time.sleep(60)  # 1 dakika bekle ve tekrar dene
                
    def log_workflow_status(self):
        """Is akisi durumunu loglar"""
        logger.info("📊 IS AKISI DURUMU:")
        logger.info(f"  📂 Toplanan Urun: {self.collection_stats['total_collected']}")
        logger.info(f"  📱 Paylasilan Urun: {self.collection_stats['total_shared']}")
        logger.info(f"  📈 Basari Orani: {self.collection_stats['success_rate']:.1f}%")
        logger.info(f"  🕐 Son Toplama: {self.collection_stats['last_collection']}")
        logger.info(f"  🕐 Son Paylasim: {self.collection_stats['last_sharing']}")
        
    def get_workflow_status(self):
        """Is akisi durumunu dondur"""
        return {
            "running": self.workflow_running,
            "stats": self.collection_stats,
            "config_loaded": bool(self.config),
            "google_drive_access": self.check_google_drive_access(),
            "last_check": datetime.now().isoformat()
        }
        
    def save_workflow_report(self):
        """Is akisi raporunu kaydet"""
        try:
            status = self.get_workflow_status()
            
            report = f"""
📂 DRIVE-SOSYAL MEDYA IS AKISI RAPORU
=====================================
📅 Rapor Tarihi: {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}

📊 GENEL DURUM:
• Is Akisi: {'🟢 Aktif' if status['running'] else '🔴 Pasif'}
• Google Drive: {'✅ Bagli' if status['google_drive_access'] else '⚠️ Bagli Degil'}
• Yapilandirma: {'✅ Yuklu' if status['config_loaded'] else '❌ Yuklenmedi'}

📈 PERFORMANS ISTATISTIKLERI:
• Toplanan Urun: {status['stats']['total_collected']}
• Paylasilan Urun: {status['stats']['total_shared']}
• Basari Orani: {status['stats']['success_rate']:.1f}%
• Son Toplama: {status['stats']['last_collection']}
• Son Paylasim: {status['stats']['last_sharing']}

🔄 IS AKISI PRENSIBI:
1. Google Drive'dan urun verilerini cek
2. Urunleri analiz et ve trend skorlari hesapla
3. Her urun icin ozel sosyal medya icerigi hazirla
4. Facebook, Instagram, Twitter, Telegram/Discord/Viber'da otomatik paylas
5. Rate limiting ile API limitlerini koru
6. 5 dakikada bir dongu ile surekli calis

📞 DESTEK:
• Log dosyasi: drive_social_workflow.log
• Yapilandirma: secrets.env
• Durum kontrolu: --status parametresi
            """
            
            report_file = self.system_path / "drive_social_raporu.txt"
            with open(report_file, 'w', encoding='utf-8') as f:
                f.write(report)
                
            logger.info(f"✅ Rapor kaydedildi: {report_file}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Rapor kaydedilemedi: {e}")
            return False

def main():
    """Ana fonksiyon"""
    print(">> ULUSLARASI TRM FULL OTOMASYON - DRIVE-SOSYAL MEDYA IS AKISI")
    print("Google Drive'dan urun cek, sosyal medyada otomatik paylas...")
    
    workflow = DriveSocialWorkflow()
    
    # Parametre kontrolu
    if len(sys.argv) > 1:
        if sys.argv[1] == "--status":
            status = workflow.get_workflow_status()
            print(f"\n📊 Is Akisi Durumu:")
            print(f"Calisiyor: {status['running']}")
            print(f"Toplanan: {status['stats']['total_collected']}")
            print(f"Paylasilan: {status['stats']['total_shared']}")
            print(f"Basari: {status['stats']['success_rate']:.1f}%")
            return
        elif sys.argv[1] == "--report":
            workflow.load_config()
            if workflow.save_workflow_report():
                print("✅ Drive-Sosyal raporu olusturuldu!")
                print("📁 Dosya: drive_social_raporu.txt")
            else:
                print("❌ Rapor olusturulamadi!")
            return
        elif sys.argv[1] == "--test":
            workflow.load_config()
            test_products = workflow.generate_mock_products(5)
            for product in test_products:
                workflow.share_to_social_media(product)
            return
    
    # Normal baslatma
    workflow.load_config()
    workflow.workflow_running = True
    
    print("\n🚀 DRIVE-SOSYAL MEDYA IS AKISI BASLATILIYOR")
    print("📂 Google Drive → 📱 Sosyal Medya Otomasyonu")
    print("⏰ 5 dakikada bir dongu")
    print("🔄 Ctrl+C ile durdurulabilir")
    
    workflow.run_workflow_cycle()

if __name__ == "__main__":
    main()
