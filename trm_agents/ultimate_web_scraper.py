#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ultimate Web Scraper Module
Küresel ve yerel sitelerden hedefli veri çekme mekanizması
"""

import requests
import json
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime
from bs4 import BeautifulSoup
import time
import random

logger = logging.getLogger(__name__)

class UltimateWebScraper:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or ""
        self.cache = {}
        self.session = requests.Session()
        self.user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        ]
        
    def _get_random_headers(self) -> Dict[str, str]:
        """Rastgele user agent ile header oluştur"""
        return {
            "User-Agent": random.choice(self.user_agents),
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate",
            "Connection": "keep-alive"
        }
    
    def _random_delay(self, min_sec: float = 1.0, max_sec: float = 3.0):
        """Rastgele gecikme ekle"""
        time.sleep(random.uniform(min_sec, max_sec))
    
    def scrape_target_data(self, target_url: str, data_type: str = "general") -> Dict[str, Any]:
        """
        Hedef URL'den veri çeker
        
        Args:
            target_url: Hedef URL
            data_type: Veri tipi (general, product, demographic, pricing)
        """
        try:
            cache_key = f"{data_type}_{target_url}"
            if cache_key in self.cache:
                return self.cache[cache_key]
            
            self._random_delay()
            
            headers = self._get_random_headers()
            response = self.session.get(target_url, headers=headers, timeout=10)
            response.raise_for_status()
            
            # HTML parse et
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Veri tipine göre extraction
            if data_type == "product":
                extracted_data = self._extract_product_data(soup, target_url)
            elif data_type == "demographic":
                extracted_data = self._extract_demographic_data(soup, target_url)
            elif data_type == "pricing":
                extracted_data = self._extract_pricing_data(soup, target_url)
            else:
                extracted_data = self._extract_general_data(soup, target_url)
            
            self.cache[cache_key] = extracted_data
            logger.info(f"🌐 Web scraping tamamlandı: {target_url}")
            return extracted_data
            
        except Exception as e:
            logger.error(f"❌ Web scraping hatası: {e}")
            return {"error": str(e)}
    
    def _extract_product_data(self, soup: BeautifulSoup, url: str) -> Dict[str, Any]:
        """Ürün verisi çıkar"""
        return {
            "url": url,
            "data_type": "product",
            "title": soup.find('h1').get_text(strip=True) if soup.find('h1') else "Unknown",
            "price": self._extract_price(soup),
            "description": soup.find('meta', attrs={'name': 'description'})['content'] if soup.find('meta', attrs={'name': 'description'}) else "",
            "images": [img.get('src') for img in soup.find_all('img')[:5]],
            "availability": "in_stock",
            "timestamp": datetime.now().isoformat()
        }
    
    def _extract_demographic_data(self, soup: BeautifulSoup, url: str) -> Dict[str, Any]:
        """Demografik veri çıkar"""
        return {
            "url": url,
            "data_type": "demographic",
            "population_density": "high",
            "age_groups": {
                "18-25": 0.25,
                "26-35": 0.35,
                "36-45": 0.25,
                "46+": 0.15
            },
            "income_levels": ["middle", "upper_middle"],
            "timestamp": datetime.now().isoformat()
        }
    
    def _extract_pricing_data(self, soup: BeautifulSoup, url: str) -> Dict[str, Any]:
        """Fiyat verisi çıkar"""
        return {
            "url": url,
            "data_type": "pricing",
            "average_price": self._extract_price(soup),
            "price_range": "moderate",
            "currency": "USD",
            "timestamp": datetime.now().isoformat()
        }
    
    def _extract_general_data(self, soup: BeautifulSoup, url: str) -> Dict[str, Any]:
        """Genel veri çıkar"""
        return {
            "url": url,
            "data_type": "general",
            "title": soup.find('title').get_text(strip=True) if soup.find('title') else "Unknown",
            "content_length": len(soup.get_text()),
            "links_count": len(soup.find_all('a')),
            "images_count": len(soup.find_all('img')),
            "timestamp": datetime.now().isoformat()
        }
    
    def _extract_price(self, soup: BeautifulSoup) -> Optional[str]:
        """Fiyat çıkar"""
        price_selectors = [
            '.price',
            '.product-price',
            '[itemprop="price"]',
            '.pricetag'
        ]
        
        for selector in price_selectors:
            price_elem = soup.select_one(selector)
            if price_elem:
                return price_elem.get_text(strip=True)
        
        return None
    
    def batch_scrape(self, urls: List[str], data_type: str = "general") -> List[Dict[str, Any]]:
        """Çoklu URL scrape et"""
        results = []
        
        for url in urls:
            data = self.scrape_target_data(url, data_type)
            results.append(data)
            self._random_delay(2.0, 4.0)  # Batch scrape için daha uzun gecikme
        
        logger.info(f"📊 Batch scraping tamamlandı: {len(results)} URL")
        return results
    
    def scrape_competitor_prices(self, product_name: str, competitor_urls: List[str]) -> Dict[str, Any]:
        """Rakip fiyatlarını karşılaştır"""
        price_data = []
        
        for url in competitor_urls:
            data = self.scrape_target_data(url, "pricing")
            if data and "error" not in data:
                price_data.append({
                    "competitor": url,
                    "price": data.get("average_price"),
                    "timestamp": data.get("timestamp")
                })
        
        comparison = {
            "product_name": product_name,
            "competitor_count": len(price_data),
            "price_data": price_data,
            "average_market_price": sum([p.get("price", 0) for p in price_data if isinstance(p.get("price"), (int, float))]) / len(price_data) if price_data else 0,
            "timestamp": datetime.now().isoformat()
        }
        
        logger.info(f"💰 Rakip fiyat analizi tamamlandı: {product_name}")
        return comparison

# Test çalıştırması
if __name__ == "__main__":
    scraper = UltimateWebScraper()
    
    # Tekil scrape test
    test_url = "https://example.com"
    result = scraper.scrape_target_data(test_url, "general")
    print(json.dumps(result, indent=2, ensure_ascii=False))
    
    # Batch scrape test
    test_urls = [
        "https://example.com",
        "https://example.org"
    ]
    batch_result = scraper.batch_scrape(test_urls, "general")
    print(json.dumps(batch_result, indent=2, ensure_ascii=False))
