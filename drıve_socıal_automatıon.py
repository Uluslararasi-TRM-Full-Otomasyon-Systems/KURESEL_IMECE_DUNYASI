#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ULUSLARARASI TRM FULL OTOMASYON v3.0
Trend Urunler Market - Google Drive → Sosyal Medya Otomasyonu
Urun Verileri Depolama ve Sosyal Medya Otomatik Paylasim Sistemi
"""

import json
import time
import random
import threading
import requests
from datetime import datetime, timedelta
from http.server import HTTPServer, SimpleHTTPRequestHandler
import os
import base64
from pathlib import Path

class DriveSocialAutomation:
    def __init__(self):
        self.running = True
        self.product_data = []
        self.social_accounts = {
            "facebook": {
                "access_token": "demo_token_facebook",
                "page_id": "trendurunlermarket",
                "status": "AKTIF"
            },
            "instagram": {
                "access_token": "demo_token_instagram", 
                "account_id": "trendurunlermarket",
                "status": "AKTIF"
            },
            "twitter": {
                "api_key": "demo_key_twitter",
                "api_secret": "demo_secret_twitter",
                "access_token": "demo_token_twitter",
                "status": "AKTIF"
            },
            "linkedin": {
                "access_token": "demo_token_linkedin",
                "company_id": "trendurunlermarket",
                "status": "AKTIF"
            },
            "tiktok": {
                "access_token": "demo_token_tiktok",
                "account_id": "trendurunlermarket",
                "status": "AKTIF"
            },
            "youtube": {
                "api_key": "demo_key_youtube",
                "channel_id": "trendurunlermarket",
                "status": "AKTIF"
            }
        }
        self.drive_folder_id = "demo_drive_folder_id"
        self.post_history = []
        self.automation_stats = {
            "products_collected": 0,
            "posts_published": 0,
            "engagement_rate": 0,
            "reach_count": 0,
            "last_collection": None,
            "last_post": None
        }
        self.start_automation()

    def collect_product_data(self):
        """Urun verilerini topla ve Google Drive'a yukle"""
        # Demo urun verileri olustur
        categories = ["Elektronik", "Giyim", "Ev & Yasam", "Spor & Outdoor", "Taki & Aksesuar", "Kozmetik", "Kitap & Hobi"]
        
        new_products = []
        for i in range(random.randint(3, 8)):
            product = {
                "id": len(self.product_data) + len(new_products) + 1,
                "name": f"Trend Urun {len(self.product_data) + len(new_products) + 1}",
                "category": random.choice(categories),
                "price": round(random.uniform(50, 5000), 2),
                "commission_rate": round(random.uniform(20, 40), 1),
                "stock_count": random.randint(5, 100),
                "description": f"Yuksek kaliteli trend urun. Komisyon orani: {random.uniform(20, 40):.1f}%",
                "image_url": f"https://picsum.photos/seed/product{len(self.product_data) + len(new_products) + 1}/400/300.jpg",
                "affiliate_link": f"https://trendurunlermarket.com/product/{len(self.product_data) + len(new_products) + 1}",
                "tags": ["trend", "kaliteli", "uygun fiyatli", random.choice(["yeni", "populer", "limitli"])],
                "collected_at": datetime.now().isoformat(),
                "trend_score": round(random.uniform(7.5, 9.9), 1)
            }
            new_products.append(product)
        
        # Urunleri listeye ekle
        self.product_data.extend(new_products)
        
        # Google Drive'a yukle (simulasyon)
        self.upload_to_drive(new_products)
        
        # Istatistikleri guncelle
        self.automation_stats["products_collected"] += len(new_products)
        self.automation_stats["last_collection"] = datetime.now().isoformat()
        
        print(f"✅ {len(new_products)} yeni urun toplandi ve Drive'a yuklendi")
        return new_products

    def upload_to_drive(self, products):
        """Urun verilerini Google Drive'a yukle (simulasyon)"""
        drive_data = {
            "upload_time": datetime.now().isoformat(),
            "folder_id": self.drive_folder_id,
            "products": products,
            "total_products": len(self.product_data)
        }
        
        # JSON dosyasi olarak kaydet (simulasyon)
        filename = f"products_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(drive_data, f, ensure_ascii=False, indent=2)
        
        print(f"📁 {len(products)} urun Google Drive'a yuklendi: {filename}")

    def fetch_from_drive(self):
        """Google Drive'dan urun verilerini cek"""
        # Simulasyon: Local dosyalardan oku
        drive_files = [f for f in os.listdir('.') if f.startswith('products_') and f.endswith('.json')]
        
        if drive_files:
            latest_file = max(drive_files)
            with open(latest_file, 'r', encoding='utf-8') as f:
                drive_data = json.load(f)
            
            print(f"📥 Google Drive'dan {len(drive_data['products'])} urun cekildi")
            return drive_data['products']
        
        return []

    def generate_social_content(self, product):
        """Sosyal medya icerigi olustur"""
        templates = {
            "facebook": [
                "🔥 YENI GELDI! 🔥\n\n{product_name}\n💰 Fiyat: {price} TL\n💎 Komisyon: {commission}%\n\n{description}\n\n🛒 Hemen al: {affiliate_link}\n\n#TrendUrunler #Indirim #Kalite",
                "✨ HARIKA FIRSAT! ✨\n\n{product_name}\n\n⭐ {category} kategorisinde en cok tercih edilen urun!\n💸 Stoklarla sinirli!\n\n👉 {affiliate_link}\n\n#TrendUrunlerMarket #UygunFiyat"
            ],
            "instagram": [
                "🛍️ YENI SEZON 🛍️\n\n{product_name}\n\n💎 {price} TL\n🎯 {commission}% komisyon\n\n📦 Hemen kargoya hazir!\n\n👆 Link bio'de!\n\n#trend #urun #indirim #kalite",
                "⭐ POPULER URUR ⭐\n\n{product_name}\n\n{category}\n\n💰 Sadece {price} TL\n\n🔥 Kacirma!\n\n#trendurunlermarket #alisveris"
            ],
            "twitter": [
                "🔥 YENI: {product_name} - {price} TL 💎 %{commission} komisyon! {category} kategorisinde en iyiler! 🛒 {affiliate_link} #TrendUrunler #Indirim",
                "✨ Firsat: {product_name} - Sadece {price} TL! %{commission} komisyon 🎯 {affiliate_link} #TrendUrunlerMarket #UygunFiyat"
            ],
            "linkedin": [
                "🏆 Trend Urunler Market - Yeni Urun Eklendi\n\n{product_name}\n\n📊 Kategori: {category}\n💰 Fiyat: {price} TL\n💎 Komisyon Orani: %{commission}\n\n{description}\n\n🔗 Detaylar: {affiliate_link}\n\n#eCommerce #Business #Retail",
                "📈 Yeni Firsat Urunu\n\n{product_name}\n\n💸 Yuksek komisyon firsati: %{commission}\n📦 Stok durumu: {stock} adet\n\n👉 {affiliate_link}\n\n#Retail #Products #Business"
            ],
            "tiktok": [
                "🔥 BU URUN KACIRILMAZ! 🔥\n\n{product_name}\n💰 {price} TL\n💎 %{commission} komisyon\n\n📦 Hemen siparis!\n\n👆 Link bio'de!\n\n#trend #viral #urun",
                "✨ VIRAL URUR! ✨\n\n{product_name}\n\n{category}\n\n💸 Sadece {price} TL\n\n🔥 Hemen al!\n\n#trendurunlermarket #alisveris"
            ],
            "youtube": [
                "🎥 YENI URUN INCELEMESI 🎥\n\n{product_name}\n\n📊 Detayli inceleme ve fiyat karsilastirmasi!\n💰 Fiyat: {price} TL\n💎 Komisyon: %{commission}\n\n🔗 Urun linki: {affiliate_link}\n\n#ProductReview #TrendProducts",
                "🛍️ ALISVERIS VIDEOSU 🛍️\n\n{product_name}\n\n{category} kategorisinde en cok satan urunler!\n\n💸 Fiyat: {price} TL\n\n👉 {affiliate_link}\n\n#Shopping #ProductReview"
            ]
        }
        
        content = {}
        for platform, template_list in templates.items():
            template = random.choice(template_list)
            content[platform] = template.format(
                product_name=product["name"],
                price=product["price"],
                commission=product["commission_rate"],
                category=product["category"],
                description=product["description"],
                affiliate_link=product["affiliate_link"],
                stock=product["stock_count"]
            )
        
        return content

    def post_to_social_media(self, product):
        """Urunu sosyal medyada paylas"""
        content = self.generate_social_content(product)
        
        posted_platforms = []
        
        for platform, post_content in content.items():
            if self.social_accounts[platform]["status"] == "AKTIF":
                # Simulasyon: Post gonder
                success = self.simulate_post(platform, post_content, product)
                
                if success:
                    posted_platforms.append(platform)
                    
                    # Post gecmisine ekle
                    post_record = {
                        "platform": platform,
                        "product_id": product["id"],
                        "product_name": product["name"],
                        "content": post_content,
                        "posted_at": datetime.now().isoformat(),
                        "status": "PUBLISHED",
                        "engagement": random.randint(10, 500)
                    }
                    self.post_history.append(post_record)
                    
                    print(f"✅ {platform.upper()} paylasimi yapildi: {product['name']}")
                else:
                    print(f"❌ {platform.upper()} paylasimi basarisiz: {product['name']}")
        
        # Istatistikleri guncelle
        self.automation_stats["posts_published"] += len(posted_platforms)
        self.automation_stats["last_post"] = datetime.now().isoformat()
        self.automation_stats["engagement_rate"] = random.uniform(3.5, 8.2)
        self.automation_stats["reach_count"] += random.randint(100, 2000) * len(posted_platforms)
        
        return posted_platforms

    def simulate_post(self, platform, content, product):
        """Sosyal medya post simulasyonu"""
        # %95 basari orani
        return random.random() < 0.95

    def automation_loop(self):
        """Ana otomasyon dongusu"""
        collection_interval = 300  # 5 dakikada bir urun toplama
        post_interval = 180  # 3 dakikada bir paylasim
        last_collection = time.time()
        last_post = time.time()
        
        while self.running:
            try:
                current_time = time.time()
                
                # Urun toplama zamani geldi mi?
                if current_time - last_collection >= collection_interval:
                    print("🔄 Urun verileri toplaniyor...")
                    self.collect_product_data()
                    last_collection = current_time
                
                # Sosyal medya paylasim zamani geldi mi?
                if current_time - last_post >= post_interval and self.product_data:
                    print("📱 Sosyal medya paylasimi yapiliyor...")
                    
                    # Drive'dan en son urunleri cek
                    drive_products = self.fetch_from_drive()
                    if drive_products:
                        # En yuksek komisyonlu urunu sec
                        best_product = max(drive_products, key=lambda x: x["commission_rate"])
                        
                        # Sosyal medyada paylas
                        platforms = self.post_to_social_media(best_product)
                        
                        if platforms:
                            print(f"✅ {best_product['name']} {len(platforms)} platformda paylasildi")
                    
                    last_post = current_time
                
                time.sleep(30)  # 30 saniye bekle
                
            except Exception as e:
                print(f"❌ Otomasyon hatasi: {e}")
                time.sleep(60)

    def start_automation(self):
        """Otomasyonu baslat"""
        automation_thread = threading.Thread(target=self.automation_loop, daemon=True)
        automation_thread.start()

    def get_status_json(self):
        """JSON durum bilgisi dondur"""
        return json.dumps({
            "automation_status": "AKTIF" if self.running else "DURDURULDU",
            "product_count": len(self.product_data),
            "social_accounts": self.social_accounts,
            "automation_stats": self.automation_stats,
            "recent_posts": self.post_history[-10:] if self.post_history else [],
            "drive_integration": {
                "folder_id": self.drive_folder_id,
                "last_sync": self.automation_stats["last_collection"],
                "status": "CONNECTED"
            },
            "workflow_status": {
                "collection": "AKTIF",
                "drive_upload": "AKTIF", 
                "drive_fetch": "AKTIF",
                "social_posting": "AKTIF"
            }
        }, ensure_ascii=False, indent=2)

class DriveSocialAPIHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, automation_engine=None, **kwargs):
        self.automation_engine = automation_engine
        super().__init__(*args, **kwargs)

    def do_GET(self):
        if self.path == '/drive-social':
            self.serve_html('DRIVE_SOCIAL_PANEL.html')
        elif self.path == '/drive-social/status':
            self.serve_json()
        elif self.path.startswith('/api/'):
            self.handle_api()
        else:
            super().do_GET()

    def serve_html(self, filename):
        """HTML dosyasi sun"""
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                content = f.read()
            
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(content.encode('utf-8'))
        except FileNotFoundError:
            self.send_error(404, "File not found")

    def serve_json(self):
        """JSON veri sun"""
        self.send_response(200)
        self.send_header('Content-type', 'application/json; charset=utf-8')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(self.automation_engine.get_status_json().encode('utf-8'))

    def handle_api(self):
        """API isteklerini yonet"""
        path_parts = self.path.split('/')
        
        if len(path_parts) >= 3:
            action = path_parts[2]
            
            if action == 'collect':
                products = self.automation_engine.collect_product_data()
                self.send_json_response({"status": "success", "products_collected": len(products)})
            elif action == 'post':
                # Rastgele bir urunu paylas
                if self.automation_engine.product_data:
                    product = random.choice(self.automation_engine.product_data)
                    platforms = self.automation_engine.post_to_social_media(product)
                    self.send_json_response({"status": "success", "platforms": platforms, "product": product["name"]})
                else:
                    self.send_json_response({"status": "error", "message": "Urun bulunamadi"})
            elif action == 'start':
                self.automation_engine.running = True
                self.send_json_response({"status": "started", "message": "Otomasyon baslatildi"})
            elif action == 'stop':
                self.automation_engine.running = False
                self.send_json_response({"status": "stopped", "message": "Otomasyon durduruldu"})
            elif action == 'stats':
                self.send_json_response({"stats": self.automation_engine.automation_stats})
            elif action == 'products':
                self.send_json_response({"products": self.automation_engine.product_data[-20:]})
            elif action == 'posts':
                self.send_json_response({"posts": self.automation_engine.post_history[-20:]})
            else:
                self.send_error(404, "API endpoint not found")

    def send_json_response(self, data):
        """JSON yanit gonder"""
        self.send_response(200)
        self.send_header('Content-type', 'application/json; charset=utf-8')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False).encode('utf-8'))

def start_drive_social_server(port, automation_engine):
    """Drive-Sosyal Medya sunucusu baslat"""
    handler = lambda *args, **kwargs: DriveSocialAPIHandler(*args, automation_engine=automation_engine, **kwargs)
    server = HTTPServer(('localhost', port), handler)
    print(f"✅ Drive-Sosyal Sunucu {port} portunda baslatildi")
    server.serve_forever()

def main():
    print("🚀 ULUSLARARASI TRM FULL OTOMASYON v3.0")
    print("📁 Google Drive → Sosyal Medya Otomasyonu")
    print("🌐 Trend Urunler Market - Tam Entegrasyon")
    print("=" * 60)
    
    # Drive-Sosyal otomasyon motorunu baslat
    drive_social_automation = DriveSocialAutomation()
    
    # Sunucuyu baslat
    port = 9004  # Yeni port
    server_thread = threading.Thread(target=start_drive_social_server, args=(port, drive_social_automation), daemon=True)
    server_thread.start()
    
    print(f"\n✅ Drive-Sosyal Otomasyon Baslatildi!")
    print(f"🌐 Panel: http://localhost:{port}/drive-social")
    print(f"📊 Status API: http://localhost:{port}/drive-social/status")
    print("\n🔄 Otomasyon Akisi:")
    print("   1. Urun verileri toplanir")
    print("   2. Google Drive'a yuklenir")
    print("   3. Drive'dan veriler cekilir")
    print("   4. Sosyal medyada paylasilir")
    print("\n📱 Aktif Platformlar:")
    for platform, account in drive_social_automation.social_accounts.items():
        if account["status"] == "AKTIF":
            print(f"   • {platform.title()}: ✅")
    
    print("\n🤖 Tam Otomasyon Aktif!")
    print("👋 Durdurmak icin Ctrl+C")
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n👋 Drive-Sosyal Otomasyon durduruluyor...")
        drive_social_automation.running = False
        print("✅ Otomasyon durduruldu")

if __name__ == "__main__":
    main()
