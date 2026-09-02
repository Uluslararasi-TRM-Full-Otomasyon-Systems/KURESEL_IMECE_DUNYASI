# social_media_scheduler.py
import schedule
import time
from datetime import datetime
import random

# Ürün listesi (telegram_bot.py'den alınır)
URUNLER = [
    {
        'ad': 'Xiaomi Akıllı Bileklik',
        'fiyat': 449,
        'link': 'https://www.trendyol.com/pd/xiaomi/mi-smart-band-6-akilli-bileklik-6024890',
        'aciklama': 'Kalp atışı, adım sayar, uyku takibi',
        'resim': 'bileklik.jpg'
    },
    {
        'ad': 'ChefMax Doğrayıcı',
        'fiyat': 449,
        'link': 'https://www.trendyol.com/chefmax/1000-watt-3-5-lt-cam-hazneli-dograyici-seti-p-52965241',
        'aciklama': '1000W güç, 3.5L cam hazne',
        'resim': 'dograyici.jpg'
    },
    {
        'ad': 'Korkmaz Titanium Tava',
        'fiyat': 199,
        'link': 'https://www.trendyol.com/korkmaz/a530-bella-titanium-tava-26-cm-p-2525668',
        'aciklama': '26 cm titanyum tava, yapışmaz yüzey',
        'resim': 'tava.jpg'
    }
]

def instagram_paylas():
    """Instagram için paylaşım hazırla"""
    urun = random.choice(URUNLER)
    print(f"\n[{datetime.now().strftime('%H:%M')}] 📱 INSTAGRAM paylaşım hazırlanıyor...")
    
    # instagram_simple.py'yi kullan
    from instagram_simple import InstagramSimpleBot
    insta = InstagramSimpleBot("trend.urunlermarket")
    insta.paylasim_hazirla(
        urun['ad'], 
        urun['fiyat'], 
        urun['link'],
        urun['resim']
    )

def facebook_paylas():
    """Facebook için paylaşım hazırla"""
    urun = random.choice(URUNLER)
    print(f"\n[{datetime.now().strftime('%H:%M')}] 📘 FACEBOOK paylaşım hazırlanıyor...")
    
    from facebook_simple import FacebookSimpleBot
    fb = FacebookSimpleBot("Trend Ürünler Market", "Mehmet Güzel")
    fb.paylasim_hazirla(
        urun['ad'],
        urun['fiyat'],
        urun['link'],
        urun['aciklama']
    )

def telegram_paylas():
    """Telegram zaten çalışıyor, sadece rapor ver"""
    print(f"\n[{datetime.now().strftime('%H:%M')}] 🤖 TELEGRAM çalışıyor...")

# Zamanlama ayarları
schedule.every(2).hours.do(instagram_paylas)    # 2 saatte bir Instagram
schedule.every(3).hours.do(facebook_paylas)     # 3 saatte bir Facebook
schedule.every(1).hour.do(telegram_paylas)      # Her saat Telegram

print("""
🚀 SOSYAL MEDYA OTOMASYONU BAŞLATILDI
=======================================
📱 Instagram: @trend.urunlermarket (2 saatte bir)
📘 Facebook: Trend Ürünler Market (3 saatte bir)
🤖 Telegram: Zaten aktif (her saat başı)

⏰ İlk paylaşım 5 dakika sonra başlayacak...
=======================================
""")

# 5 dakika bekle, sonra başla
time.sleep(300)

# Sonsuz döngü
while True:
    schedule.run_pending()
    time.sleep(60)
