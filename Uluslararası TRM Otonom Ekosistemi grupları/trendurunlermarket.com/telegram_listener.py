#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TRM Telegram Dinleyici - Tedarikçi gruplarından ürün yakalama
"""

import asyncio
import logging
import re
import json
import os
from datetime import datetime
from typing import List, Dict, Optional

# Telethon import - eğer yoksa mock kullan
try:
    from telethon import TelegramClient, events
    from telethon.tl.types import MessageMediaPhoto, MessageMediaDocument
    TELETHON_AVAILABLE = True
except ImportError:
    TELETHON_AVAILABLE = False
    print("⚠️ Telethon kurulu değil. Mock mod kullanılacak.")
    # Stub'lar - mock modda NameError olmaması için
    class _StubEvents:
        class NewMessage: pass
    events = _StubEvents()
    class MessageMediaPhoto: pass
    class MessageMediaDocument: pass

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MockTelegramClient:
    """Mock Telegram client for testing"""
    def __init__(self, *args, **kwargs):
        self.session_name = kwargs.get('session', 'mock_session')
        
    async def start(self, phone=None):
        logger.info(f"Mock Telegram client başlatıldı: {self.session_name}")
        return True
        
    async def disconnect(self):
        logger.info("Mock Telegram client kapatıldı")
        
    def add_event_handler(self, handler, event_type=None):
        logger.info("Mock event handler eklendi")
        
    async def run_until_disconnected(self):
        while True:
            await asyncio.sleep(10)
            logger.info("Mock Telegram dinliyor...")

class TelegramProductListener:
    def __init__(self, api_id=None, api_hash=None, phone=None, session_name="trm_session"):
        self.api_id = api_id or os.getenv("TELEGRAM_API_ID", "")
        self.api_hash = api_hash or os.getenv("TELEGRAM_API_HASH", "")
        self.phone = phone or os.getenv("TELEGRAM_PHONE", "")
        self.session_name = session_name
        
        if TELETHON_AVAILABLE and self.api_id and self.api_hash:
            self.client = TelegramClient(session_name, self.api_id, self.api_hash)
        else:
            self.client = MockTelegramClient(session=session_name)
            
        self.captured_products = []
        self.commission_keywords = [
            r"%\d+",  # %25, %30 gibi
            r"komisyon",
            r"indirim", 
            r"fırsat",
            r"kampanya",
            r"yüzde",
            r"discount"
        ]
        
        # Telegram kaynak kanalları
        self.telegram_sources = [
            "magazanolsunresmi",
            "trendyolkampanya",
            "trendyolindirimleri",
            "hepsiburadakampanya",
            "amazonturkiyefirsat",
            "n11kampanyalari",
            "akakce_kampanya",
            "urunlerim_affiliate",
            "komisyonlu_urunler",
            "afiliyet_marketing_tr",
            "trendurunler", 
            "ucuzurunler",
            "indirimkosesi",
            "trendurunlermarket"
        ]
        
    async def start(self):
        """Telegram client'ını başlat"""
        try:
            await self.client.start(phone=self.phone)
            logger.info("Telegram client başlatıldı")
            
            # Mesaj dinleyicilerini kur
            self.client.add_event_handler(self.handle_new_message, events.NewMessage)
            
            logger.info(f"Takip edilen kanallar: {self.telegram_sources}")
            
        except Exception as e:
            logger.error(f"Telegram başlatma hatası: {e}")
            raise
    
    async def handle_new_message(self, event):
        """Yeni mesajları işle - gerçek parser kullanarak"""
        from telegram_parser import parse_telegram_message
        from trm_tracking import record_product

        message = event.message
        text = message.text or ""

        # Kanal kontrolü
        channel = "unknown"
        if hasattr(event, 'chat') and hasattr(event.chat, 'username'):
            channel = event.chat.username
            if channel not in self.telegram_sources:
                return
        elif hasattr(message, 'peer_id'):
            channel = str(getattr(message.peer_id, 'channel_id', 'unknown'))

        try:
            # Medya URL'lerini topla
            media_urls = []
            if hasattr(message, 'media') and message.media:
                if isinstance(message.media, MessageMediaPhoto):
                    media_urls.append(f"photo_{message.id}.jpg")
                elif isinstance(message.media, MessageMediaDocument):
                    media_urls.append(f"doc_{message.id}.mp4")

            # YENİ: Gelişmiş parser
            product_data = parse_telegram_message(
                text=text,
                channel=channel,
                message_id=message.id,
                media_urls=media_urls
            )

            if not product_data:
                return  # Ürün bilgisi yetersiz

            # Yüksek komisyonlu ürünleri logla
            if product_data['commission_rate'] >= 20.0:
                logger.info(
                    f"💰 Yüksek komisyonlu ürün: {product_data['title'][:50]} "
                    f"(%{product_data['commission_rate']}, {product_data['price']} TL)"
                )

            self.captured_products.append(product_data)

            # SQLite tracking DB'ye kaydet
            product_id = record_product(product_data)
            if product_id:
                product_data['db_id'] = product_id
                logger.info(f"📊 Tracking DB ID: {product_id}")

            # JSON kuyruğa da ekle (orchestrator için)
            await self.queue_product_for_processing(product_data)

        except Exception as e:
            logger.error(f"Mesaj işleme hatası: {e}", exc_info=True)
    
    async def extract_product_data(self, message) -> Optional[Dict]:
        """Mesajdan ürün bilgilerini çıkar"""
        if not message.text and not hasattr(message, 'media'):
            return None
            
        product_data = {
            'title': '',
            'description': '',
            'price': '',
            'media_urls': [],
            'links': []
        }
        
        # Metin içeriğini işle
        text = message.text or ""
        
        # Başlığı çıkar (ilk satır genellikle başlıktır)
        lines = text.split('\n')
        if lines:
            product_data['title'] = lines[0].strip()
            product_data['description'] = '\n'.join(lines[1:]).strip()
        
        # Fiyat bilgilerini çıkar
        price_patterns = [
            r'(\d+(?:\.\d+)?)\s*TL',
            r'(\d+(?:\.\d+)?)\s*₺',
            r'(\d+(?:\.\d+)?)\s*türk lirası',
            r'(\d+(?:\.\d+)?)\s*lira',
            r'(\d+(?:\.\d+)?)\s*try'
        ]
        
        for pattern in price_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                product_data['price'] = match.group(1)
                break
        
        # Linkleri çıkar
        url_pattern = r'https?://[^\s<>"{}|\\^`[\]]+'
        urls = re.findall(url_pattern, text)
        product_data['links'] = urls
        
        # Medya dosyalarını işle
        if hasattr(message, 'media') and message.media:
            if isinstance(message.media, MessageMediaPhoto):
                # Fotoğraf için mock URL
                product_data['media_urls'].append(f"photo_{message.id}.jpg")
                
            elif isinstance(message.media, MessageMediaDocument):
                # Video veya diğer dosyalar için mock URL
                product_data['media_urls'].append(f"doc_{message.id}.mp4")
        
        return product_data if product_data['title'] else None
    
    def extract_commission_rate(self, text: str) -> Optional[float]:
        """Metinden komisyon oranını çıkar"""
        text_lower = text.lower()
        
        for keyword in self.commission_keywords:
            if keyword in text_lower:
                # Sayısal değeri bul
                number_pattern = r'(\d+(?:\.\d+)?)'
                matches = re.findall(number_pattern, text)
                if matches:
                    try:
                        # Yüzde işareti varsa onu kullan
                        if '%' in text:
                            for match in matches:
                                if int(match) <= 100:  # %100'den küçük olmalı
                                    return float(match)
                        else:
                            # Komisyon kelimesi geçiyorsa ilk sayıyı al
                            return float(matches[0])
                    except ValueError:
                        continue
        return None
    
    async def queue_product_for_processing(self, product_data: Dict):
        """Ürünü işleme kuyruğuna ekle (file-lock korumalı)"""
        from trm_utils import safe_append_to_queue
        queue_file = "product_queue.json"

        if safe_append_to_queue(queue_file, product_data):
            logger.info(f"Ürün işleme kuyruğuna eklendi: {product_data['title']}")
        else:
            logger.error(f"Ürün kuyruğa eklenemedi: {product_data['title']}")
    
    async def run(self):
        """Ana çalışma döngüsü"""
        await self.start()
        logger.info("Telegram dinleyici çalışıyor...")
        
        try:
            await self.client.run_until_disconnected()
        except KeyboardInterrupt:
            logger.info("Telegram dinleyici durduruluyor")
        except Exception as e:
            logger.error(f"Telegram dinleyici hatası: {e}")
        finally:
            if hasattr(self.client, 'disconnect'):
                await self.client.disconnect()

# Test ve örnek kullanım
async def test_telegram_listener():
    """Telegram dinleyiciyi test et"""
    listener = TelegramProductListener()
    logger.info("Telegram dinleyici test ediliyor...")
    
    # Test ürünü ekle
    test_product = {
        'title': 'Test Ürünü - %25 Komisyon',
        'description': 'Harika bir test ürünü',
        'price': '299 TL',
        'commission_rate': 25,
        'priority': 'high',
        'captured_at': datetime.now().isoformat(),
        'source': 'test',
        'message_id': 999
    }
    
    await listener.queue_product_for_processing(test_product)
    logger.info("Test ürünü kuyruğa eklendi")

if __name__ == "__main__":
    asyncio.run(test_telegram_listener())
