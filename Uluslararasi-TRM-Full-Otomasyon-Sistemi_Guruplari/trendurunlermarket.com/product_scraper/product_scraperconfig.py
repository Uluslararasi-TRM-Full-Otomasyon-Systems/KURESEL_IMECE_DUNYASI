import os
from dotenv import load_dotenv

load_dotenv()

# Dropbox
DROPBOX_ACCESS_TOKEN = os.getenv("DROPBOX_ACCESS_TOKEN")
DROPBOX_TARGET_PATH = "/Uluslararasi TRM Full Otomasyon Ürünler Deposu/01_MagazaNolSun"

# Hedef Siteler - Trendurunlermarket.com ve affiliate firmalar
TARGET_URLS = [
    # Trendurunlermarket.com (Ana hedef - doğrulanmış URL'ler)
    "https://www.trendurunlermarket.com/elektronik-C5/",
    "https://www.trendurunlermarket.com/spor-giyim--ayakkabi-C23/",
    "https://www.trendurunlermarket.com/yedek-parca-C313/",
    # Magazanolsun.com (Trendurunlermarket'in altyapı sağlayıcısı)
    "https://www.magazanolsun.com/",
    # Trendyol için örnek kategoriler
    "https://www.trendyol.com/gida-saglik-ve-ozel-bakim-x-c-143",
    "https://www.trendyol.com/kozmetik-x-c-109461",
    # N11 için örnek kategoriler
    "https://www.n11.com/gida-urunleri",
    "https://www.n11.com/kozmetik-ve-kisisel-bakim",
]

# Tarama Ayarları
SCRAPE_INTERVAL_HOURS = 6  # Her 6 saatte bir tara
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
