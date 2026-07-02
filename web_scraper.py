#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TRM Otonom Ekosistemi - Web Scraper (Ana Veri Cekici) Modulu
"""

import logging
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from typing import Dict, List, Optional
import random
import time

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class TRMWebScraper:
    def __init__(self):
        self.base_url = "https://trendurunlermarket.com" # magazanolsun altyapili ana magazaniz
        
        # 🎯 GUCLU SANS MASKESI: Sisteme %100 gercek insan tarayicisi susu veren Headers ayari
        self.headers_base = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "Accept-Language": "tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "Referer": "https://www.google.com/",
            "DNT": "1",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "cross-site",
            "Sec-Fetch-User": "?1",
            "Cache-Control": "max-age=0"
        }
        self.user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:127.0) Gecko/20100101 Firefox/127.0",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.5 Safari/605.1.15",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
        ]
        self.proxy_pool = [
            # Free proxy examples (can be extended with API calls like PubProxy)
            # Format: "http://ip:port" or "https://ip:port"
        ]
        self.max_retries = 3
        # Initialize proxy pool from API
        self.refresh_proxy_pool()

    def refresh_proxy_pool(self) -> None:
        """Fetches fresh proxies from PubProxy API (free) to update proxy pool"""
        try:
            pubproxy_url = "http://pubproxy.com/api/proxy?limit=5&format=json&type=http&level=anonymous"
            response = requests.get(pubproxy_url, timeout=10)
            if response.status_code == 200:
                data = response.json()
                new_proxies = [f"http://{proxy['ipPort']}" for proxy in data.get('data', [])]
                self.proxy_pool.extend(new_proxies)
                # Remove duplicates
                self.proxy_pool = list(set(self.proxy_pool))
                logger.info(f"✅ Proxy havuzu guncellendi! Toplam proxy sayisi: {len(self.proxy_pool)}")
            else:
                logger.warning("⚠️ PubProxy API'den proxy cekilemedi. Mevcut havuz kullanilacak.")
        except Exception as e:
            logger.error(f"❌ Proxy havuzu guncellenirken hata: {str(e)}")

    def get_random_headers(self) -> Dict:
        """Returns random User-Agent headers for each request"""
        headers = self.headers_base.copy()
        headers["User-Agent"] = random.choice(self.user_agents)
        return headers

    def get_random_proxy(self) -> Optional[Dict]:
        """Returns random proxy from pool, or None if pool is empty"""
        if not self.proxy_pool:
            return None
        proxy = random.choice(self.proxy_pool)
        return {"http": proxy, "https": proxy}

    def urun_verisi_cek(self, urun_id: str) -> Optional[Dict]:
        """Belirtilen urunun verilerini gercek insan maskesiyle guvenli bir sekilde ceker"""
        hedef_url = f"{self.base_url}/urun/{urun_id}"
        logger.info(f"🚀 TRM Ajani istek baslatiyor: {hedef_url}")

        for attempt in range(self.max_retries):
            headers = self.get_random_headers()
            proxies = self.get_random_proxy()
            
            try:
                time.sleep(random.uniform(1, 4))  # Istege kucuk bir gecikme ekle
                logger.info(f"Deneme {attempt+1}/{self.max_retries} | Proxy: {proxies['http'] if proxies else 'YOK'}")
                
                response = requests.get(
                    hedef_url, 
                    headers=headers, 
                    proxies=proxies,
                    timeout=20
                )
                
                if response.status_code == 200:
                    logger.info("🎯 Baglanti Basarili! Gercek insan maskesi dogrulandi, veri okunuyor.")
                    soup = BeautifulSoup(response.content, 'html.parser')
                    
                    # Ornek veri yapisi (Magaza sablonunuza gore otonom islenir)
                    urun_detay = {
                        "urun_id": urun_id,
                        "title": soup.find("h1").text.strip() if soup.find("h1") else "TRM Trend Urun",
                        "price": "Otonom Belirlenecek",
                        "fetched_at": datetime.now().isoformat(),
                        "mask_status": "VERIFIED_HUMAN"
                    }
                    return urun_detay
                elif response.status_code == 403 or response.status_code == 429:
                    logger.warning(f"⚠️ HTTP {response.status_code} Hatasi! (Deneme {attempt+1}/{self.max_retries}) Yeni proxy/user-agent denenecek.")
                    continue  # Retry with new proxy
                else:
                    logger.error(f"❌ Baglanti Hatasi! Kod: {response.status_code}")
                    if attempt == self.max_retries - 1:
                        return None
                    continue
                    
            except Exception as e:
                logger.error(f"❌ Scraper calisirken beklenmedik hata olustu (Deneme {attempt+1}/{self.max_retries}): {str(e)}")
                if attempt == self.max_retries - 1:
                    return None
                continue
        return None

if __name__ == "__main__":
    # Guvenlik ve Calisma Testi
    scraper = TRMWebScraper()
    print("--- TRM WEB SCRAPER GERCEK INSAN MASKESI TESTI ---")
    print(f"Kullanilabilir User-Agent Sayisi: {len(scraper.user_agents)}\n")
    print(f"Kullanilabilir Proxy Sayisi: {len(scraper.proxy_pool)}\n")
    # Simule test calistirmasi
    test_sonuc = scraper.urun_verisi_cek("test-urun-123")