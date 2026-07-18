#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TRM Otonom Ekosistemi - Web Scraper (Ana Veri Cekici) Modulu
"""

import logging
import requests
import json  # JSON dosyasına yazmak için eklendi
from bs4 import BeautifulSoup
from datetime import datetime
from typing import Dict, List, Optional
import random
import time

# Logging ayarları
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class TRMWebScraper:
    def __init__(self):
        self.base_url = "https://trendurunlermarket.com"
        self.headers_base = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "Accept-Language": "tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
        }
        self.max_retries = 3

    def get_random_headers(self) -> Dict:
        return self.headers_base.copy()

    def urun_verisi_cek(self, urun_id: str) -> Optional[Dict]:
        """Proxy kullanmadan dogrudan baglanti ile urun verisini ceker"""
        hedef_url = f"{self.base_url}/urun/{urun_id}"
        logger.info(f"🚀 TRM Ajani istek baslatiyor: {hedef_url}")

        for attempt in range(self.max_retries):
            try:
                time.sleep(random.uniform(1, 2))
                response = requests.get(hedef_url, headers=self.get_random_headers(), timeout=20)
                
                if response.status_code == 200:
                    logger.info("🎯 Baglanti Basarili! Veri okunuyor.")
                    soup = BeautifulSoup(response.content, 'html.parser')
                    
                    urun_detay = {
                        "urun_id": urun_id,
                        "title": soup.find("h1").text.strip() if soup.find("h1") else "TRM Trend Urun",
                        "price": "Otonom Belirlenecek",
                        "fetched_at": datetime.now().isoformat(),
                        "mask_status": "VERIFIED_DIRECT"
                    }
                    return urun_detay
                else:
                    logger.error(f"❌ Baglanti Hatasi! Kod: {response.status_code}")
            except Exception as e:
                logger.error(f"❌ Scraper calisirken hata: {str(e)}")
        return None

if __name__ == "__main__":
    scraper = TRMWebScraper()
    print("--- TRM WEB SCRAPER - GERCEK URUN TESTI ---")
    urun_id = "TKU1466744" 
    test_sonuc = scraper.urun_verisi_cek(urun_id)
    
    if test_sonuc:
        # Veriyi json dosyasına kaydet
        with open("trend_raporlari.json", "w", encoding="utf-8") as f:
            json.dump([test_sonuc], f, ensure_ascii=False, indent=4)
        print("✅ Veri trend_raporlari.json dosyasına yazıldı.")
    
    print(f"Test Sonucu: {test_sonuc}")