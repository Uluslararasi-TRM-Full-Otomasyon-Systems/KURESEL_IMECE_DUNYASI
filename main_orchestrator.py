#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TRM Ana Orkestratör Modülü - SADECE magazanolsun.com Odaklý Çalýþma Sürümü
"""

import asyncio
import logging
import os
import sys
from datetime import datetime

# Türkçe karakter desteði ve loglama ayarlarý
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

async def main():
    logger.info("===============================================")
    logger.info("    TRM FULL OTOMASYON SÝSTEMÝ ORKESTRATÖRÜ")
    logger.info("===============================================")
    logger.info("?? Sistem baþlatýlýyor...")
    logger.info("?? Hedef Platform: SADECE magazanolsun.com (trendurunlermarket.com)")
    
    try:
        # Web Scraper modülünü dahil et ve baþlat
        from web_scraper import WebScraper, ProductManager
        scraper = WebScraper()
        manager = ProductManager()
        
        logger.info("? Web scraper ve ürün yöneticisi hazýr.")
        logger.info("?? Ana çalýþma döngüsü aktif (7/24 dinleme modunda)...")
        
        while True:
            logger.info("?? Maðaza altyapýsý taranýyor...")
            products = await scraper.scrape_all_sources()
            await manager.process_products(products)
            
            # Sunucuyu yormamak için tarama aralýðý (Örn: 5 dakika bekler)
            await asyncio.sleep(300)
            
    except Exception as e:
        logger.error(f"? Orkestratör ana döngü hatasý: {e}")
        sys.exit(1)

if __name__ == "__main__":
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())