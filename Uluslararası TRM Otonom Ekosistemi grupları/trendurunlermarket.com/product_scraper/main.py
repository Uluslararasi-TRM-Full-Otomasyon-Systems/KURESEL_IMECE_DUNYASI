import sys
import io
import time
import json
import os
from datetime import datetime
from product_scraperconfig import TARGET_URLS, SCRAPE_INTERVAL_HOURS
from magazanolsun_scraper import MagazaNolSunScraper

# UTF-8 encoding fix for Windows console
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def scrape_and_save():
    print(f"🕒 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - TRM Ürün Çekme Operasyonu BAŞLADI")
    print("=" * 60)
    
    scraper = MagazaNolSunScraper()
    all_products = []
    
    for url in TARGET_URLS:
        try:
            print(f"\n🎯 Hedef: {url}")
            products = scraper.get_products(url)
            
            for product in products:
                trm_json = scraper.to_trm_json(product)
                all_products.append(trm_json)
            
            print(f"✅ {len(products)} ürün başarıyla çekildi: {url}")
        except Exception as e:
            print(f"❌ Hata: {url} - {str(e)}")
    
    # Tüm ürünleri JSON dosyasına kaydet
    if all_products:
        output_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        output_file = os.path.join(output_dir, "toplanan_urunler.json")
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(all_products, f, ensure_ascii=False, indent=2)
        
        print(f"\n" + "=" * 60)
        print(f"🎉 İŞLEM TAMAMLANDI!")
        print(f"📊 Toplam {len(all_products)} ürün sisteme yüklendi")
        print(f"💾 Kayıt dosyası: {output_file}")
        print(f"⏰ Tamamlanma zamanı: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 60)
    else:
        print("\n⚠️ Hiç ürün bulunamadı!")

if __name__ == "__main__":
    print("🚀 TRM Ürün Toplayıcı AI Ajanı Başlatılıyor...")
    print("🎯 Hedef: trendurunlermarket.com ve affiliate firmalar")
    print("=" * 60)
    scrape_and_save()
