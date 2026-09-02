import sys
import io
import json
import os
import time
import hashlib
import re
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

# UTF-8 encoding fix for Windows console
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

class SeleniumProductScraper:
    def __init__(self):
        self.options = Options()
        self.options.add_argument('--headless')
        self.options.add_argument('--no-sandbox')
        self.options.add_argument('--disable-dev-shm-usage')
        self.options.add_argument('--disable-gpu')
        self.options.add_argument('--window-size=1920,1080')
        self.options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36')
        
    def _extract_text(self, element, default=""):
        """Güvenli metin çekme"""
        return element.get_text(strip=True) if element else default
    
    def _extract_price(self, text):
        """Fiyat metninden sayıyı çıkarma"""
        if not text:
            return ""
        price = re.sub(r'[^\d,\.]', '', text.replace('TL', '').strip())
        return price
    
    def get_products_selenium(self, url):
        """Selenium ile ürün çekme"""
        print(f"Taranıyor (Selenium): {url}")
        
        driver = None
        try:
            driver = webdriver.Chrome(options=self.options)
            driver.get(url)
            
            # Sayfanın yüklenmesini bekle
            WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            
            # JavaScript'in çalışması için ek bekleme
            time.sleep(5)
            
            # Sayfayı aşağı kaydır (lazy load için)
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            driver.execute_script("window.scrollTo(0, 0);")
            
            # Sayfa kaynağını al
            page_source = driver.page_source
            soup = BeautifulSoup(page_source, 'html.parser')
            
            # Çeşitli ürün seçicilerini dene
            product_selectors = [
                '.product-item', '.product-card', '.product',
                '.prdct-cntnr-wrppr', '.p-card-wrppr',
                '.column', '.product-list .product',
                '.productListContent-item',
                '.item', '.product-box', '[data-product-id]',
                '.col-sm-6', '.col-md-4', '.col-lg-3', '.col-xs-6',
                '.product-card-wrapper', '.product-item-wrapper',
                '[class*="product"]', '[class*="Product"]'
            ]
            
            products = []
            found_products = None
            
            for selector in product_selectors:
                found_products = soup.select(selector)
                if found_products:
                    print(f"   Ürünler bulundu (seçici: {selector}) - {len(found_products)} adet")
                    break
            
            if not found_products:
                print("   Hiç ürün bulunamadı! Site yapısı değişmiş olabilir.")
                return []
            
            for product_div in found_products[:20]:
                try:
                    # Ürün adı
                    title = self._extract_text(
                        product_div.select_one('h1, h2, h3, h4, .title, .product-title, .product-name, [itemprop="name"], .prdct-desc-cntnr-name, .productDescription')
                    )
                    
                    # Fiyat
                    price_elem = product_div.select_one('.price, .product-price, .current-price, [itemprop="price"], .fiyat, .prc-box-dscntd, .prc-dsc, .productPrice')
                    price = self._extract_price(self._extract_text(price_elem))
                    
                    # Görsel URL
                    img_elem = product_div.select_one('img')
                    image_url = img_elem.get('src') or img_elem.get('data-src') or img_elem.get('data-original') or ''
                    
                    # Ürün Linki
                    link_elem = product_div.select_one('a')
                    product_url = link_elem.get('href') if link_elem else ''
                    
                    if not title:
                        continue
                    
                    product = {
                        'id': hashlib.md5(f"{title}_{price}_{url}".encode()).hexdigest()[:16],
                        'title': title,
                        'price': price,
                        'image_url': image_url,
                        'product_url': product_url if product_url else url,
                        'source': url,
                        'scraped_at': datetime.now().isoformat()
                    }
                    products.append(product)
                    print(f"   Ürün bulundu: {title[:50]}")
                    
                except Exception as e:
                    print(f"   Ürün ayrıştırma hatası: {str(e)}")
                    continue
            
            print(f"   Toplam {len(products)} ürün bulundu.")
            return products
            
        except Exception as e:
            print(f"   Selenium hatası: {str(e)}")
            return []
        finally:
            if driver:
                driver.quit()
    
    def to_trm_json(self, product, source_name="Trendurunlermarket"):
        """TRM Full Otomasyon JSON formatına dönüştür"""
        return {
            "firma": source_name,
            "urun_adi": product['title'],
            "aciklama": f"{product['title']} 🔥 en uygun fiyat trendurunlermarket.com'da! #{source_name}",
            "gorsel_url": product['image_url'],
            "urun_linki": product['product_url'],
            "hashtagler": f"#{source_name} #kampanya #indirim #alışveriş #fırsat",
            "fiyat": product['price'],
            "kaynak": product['source'],
            "toplanma_tarihi": product['scraped_at']
        }

def main():
    print("🚀 TRM Selenium Ürün Toplayıcı AI Ajanı Başlatılıyor...")
    print("🎯 Hedef: trendurunlermarket.com ve affiliate firmalar")
    print("=" * 60)
    
    TARGET_URLS = [
        "https://www.trendurunlermarket.com/elektronik-C5/",
        "https://www.trendurunlermarket.com/spor-giyim--ayakkabi-C23/",
        "https://www.magazanolsun.com/",
    ]
    
    scraper = SeleniumProductScraper()
    all_products = []
    
    for url in TARGET_URLS:
        try:
            print(f"\n🎯 Hedef: {url}")
            products = scraper.get_products_selenium(url)
            
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
    main()
