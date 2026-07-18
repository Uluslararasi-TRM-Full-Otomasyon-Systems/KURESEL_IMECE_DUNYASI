import requests
from bs4 import BeautifulSoup
import json
import hashlib
import re
from datetime import datetime
import time
import random

class MagazaNolSunScraper:
    def __init__(self):
        self.session = requests.Session()
        # 🔐 Geliştirilmiş Gerçek İnsan Maskesi (Anti-403)
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Accept-Language': 'tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7',
            'Accept-Encoding': 'gzip, deflate, br',
            'Referer': 'https://www.google.com/',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'cross-site',
            'Sec-Fetch-User': '?1',
            'Cache-Control': 'max-age=0',
        })
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:127.0) Gecko/20100101 Firefox/127.0',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.5 Safari/605.1.15',
        ]
    
    def _extract_text(self, element, default=""):
        """Güvenli metin çekme"""
        return element.get_text(strip=True) if element else default
    
    def _extract_price(self, text):
        """Fiyat metninden sayıyı çıkarma"""
        if not text:
            return ""
        # TL, USD, EUR gibi para birimlerini temizle, sadece sayı ve nokta/virgül bırak
        price = re.sub(r'[^\d,\.]', '', text.replace('TL', '').strip())
        return price
    
    def get_products(self, url):
        """Hedef sayfadan ürün bilgilerini çek"""
        print(f"Taranıyor: {url}")
        
        # Rastgele User-Agent seç (Anti-403 için)
        self.session.headers['User-Agent'] = random.choice(self.user_agents)
        
        try:
            time.sleep(random.uniform(1, 3))  # İsteğe küçük bir gecikme ekle (bot sanmaması için)
            response = self.session.get(url, timeout=20)
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 403:
                print(f"HTTP 403 - Erişim Engellendi: {url}")
            else:
                print(f"Sayfa açılamadı: {str(e)}")
            return []
        except Exception as e:
            print(f"Sayfa açılamadı: {str(e)}")
            return []
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Siteye özel ürün seçicileri (önce bunları dene)
        product_selectors = []
        
        # Magazanolsun özel seçicileri
        if "magazanolsun.com" in url:
            product_selectors.extend(['.product-item', '.product-card', '.product'])
        # Trendyol özel seçicileri
        elif "trendyol.com" in url:
            product_selectors.extend(['.prdct-cntnr-wrppr', '.product-card', '.p-card-wrppr'])
        # N11 özel seçicileri
        elif "n11.com" in url:
            product_selectors.extend(['.column', '.product-list .product'])
        # Hepsiburada özel seçicileri
        elif "hepsiburada.com" in url:
            product_selectors.extend(['.productListContent-item', '.product-card'])
        
        # Genel fallback seçicileri
        product_selectors.extend([
            '.item', '.product-box', '[data-product-id]', 
            '.col-sm-6', '.col-md-4', '.col-lg-3', '.col-xs-6'
        ])
        
        products = []
        found_products = None
        
        for selector in product_selectors:
            found_products = soup.select(selector)
            if found_products:
                print(f"Urunler bulundu (seçici: {selector})")
                break
        
        if not found_products:
            print("Hic urun bulunamadı! Site yapısı değişmiş olabilir.")
            return []
        
        for product_div in found_products[:20]:  # En fazla 20 ürün al
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
                if image_url and not image_url.startswith('http'):
                    image_url = url.rstrip('/') + '/' + image_url.lstrip('/')
                
                # Ürün Linki
                link_elem = product_div.select_one('a')
                product_url = link_elem.get('href') if link_elem else ''
                if product_url and not product_url.startswith('http'):
                    if product_url.startswith('/'):
                        from urllib.parse import urljoin
                        product_url = urljoin(url, product_url)
                    else:
                        product_url = url.rstrip('/') + '/' + product_url.lstrip('/')
                
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
                print(f"   Urun bulundu: {title[:50]}")
                
            except Exception as e:
                print(f"   Urun ayrıştırma hatası: {str(e)}")
                continue
        
        print(f"Toplam {len(products)} ürün bulundu.")
        return products
    
    def to_trm_json(self, product, source_name="MagazaNolSun"):
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
