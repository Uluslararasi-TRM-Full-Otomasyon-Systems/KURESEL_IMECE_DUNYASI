#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TRM Sistem Birim Testleri
Kullanim: pytest test_trm.py -v
"""

import os
import sys
import json
import asyncio
import tempfile
import pytest

# Modulleri ekle
sys.path.insert(0, os.path.dirname(__file__))

# Config'i en basta yukle
import config


# ============================================
# Config Testleri
# ============================================

def test_config_loads_secrets():
    """secrets.env okunup os.environ'a aktariliyor mu?
    Not: secrets.env henuz doldurulmamissa bu test atlanir (beklenen durum).
    """
    api_id = os.environ.get("TELEGRAM_API_ID", "")
    openai_key = os.environ.get("OPENAI_API_KEY", "")
    if not api_id and not openai_key:
        pytest.skip("secrets.env henuz doldurulmamis — anahtarlari girdikten sonra calistirin")
    assert api_id, "TELEGRAM_API_ID os.environ'a yazilmamis"
    assert openai_key, "OPENAI_API_KEY os.environ'a yazilmamis"


def test_config_validation():
    """Validation calisiyor mu?"""
    v = config.config.validate_critical_configs()
    assert isinstance(v, dict)
    assert 'telegram' in v
    assert 'openai' in v


# ============================================
# Web Scraper Testleri
# ============================================

def test_commission_extraction_legitimate():
    """Komisyon regex'i gercek komisyon degerlerini yakaliyor mu?"""
    from web_scraper import WebScraper
    s = WebScraper()
    assert s.extract_commission_from_text("Bu urun %25 komisyon veriyor") == 25.0
    assert s.extract_commission_from_text("Indirim %30") == 30.0
    assert s.extract_commission_from_text("yuzde 15 firsat") == 15.0


def test_commission_extraction_ignores_random_numbers():
    """Telefon/fiyat gibi rastgele sayilari komisyon sanmiyor"""
    from web_scraper import WebScraper
    s = WebScraper()
    # Sadece fiyat var, komisyon yok → 0 donmeli
    result = s.extract_commission_from_text("Fiyat 1299 TL, telefon 0212 555 1234")
    assert result == 0.0, f"Beklenen 0.0, gelen {result}"


# ============================================
# AI Integration Testleri
# ============================================

@pytest.mark.asyncio
async def test_ai_pipeline_mock():
    """AI pipeline mock modda calisiyor mu?"""
    from ai_integration import AIContentGenerator
    ai = AIContentGenerator()
    product = {'title': 'Test', 'price': '100 TL', 'commission_rate': 25}
    result = await ai.process_product_pipeline(product)
    assert result['success'] is True
    assert 'content' in result['content']


def test_ai_finds_openai_fallback():
    """OpenAI key, DeepSeek icin fallback olarak bulunuyor mu?"""
    from ai_integration import AIContentGenerator
    ai = AIContentGenerator()
    stats = ai.get_statistics()
    # OPENAI_API_KEY varsa deepseek_available True olmali
    if os.environ.get("OPENAI_API_KEY"):
        assert stats['deepseek_available'] is True


# ============================================
# File-lock Kuyruk Testleri
# ============================================

def test_safe_queue_append_and_read():
    """File-lock kuyruk dogru calisiyor mu?"""
    from trm_utils import safe_append_to_queue, safe_read_queue, safe_write_queue

    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        tmp = f.name
        json.dump([], f)

    try:
        # Append
        safe_append_to_queue(tmp, {'id': 1, 'title': 'A'})
        safe_append_to_queue(tmp, {'id': 2, 'title': 'B'})

        data = safe_read_queue(tmp)
        assert len(data) == 2
        assert data[0]['title'] == 'A'
        assert data[1]['title'] == 'B'

        # Write (overwrite)
        safe_write_queue(tmp, [])
        data = safe_read_queue(tmp)
        assert data == []
    finally:
        os.unlink(tmp)
        lock_file = f"{tmp}.lock"
        if os.path.exists(lock_file):
            os.unlink(lock_file)


# ============================================
# Google Drive Integration
# ============================================

def test_google_drive_no_nameerror():
    """re import'u var mi, NameError vermiyor mu?"""
    from google_drive_integration import AnalyticsManager, GoogleDriveManager
    dm = GoogleDriveManager()
    am = AnalyticsManager(dm)
    stats = am.get_dashboard_stats()
    assert isinstance(stats, dict)


# ============================================
# Social Media
# ============================================

@pytest.mark.asyncio
async def test_social_media_mock_publish():
    """Sosyal medya mock yayini calisiyor mu?"""
    from social_media_automation import SocialMediaManager
    sm = SocialMediaManager()
    content = {
        'content': 'Test icerik',
        'title': 'Test',
        'link': 'https://example.com',
        'image_url': ''
    }
    result = await sm.publish_to_all_platforms(content)
    assert 'summary' in result
    assert result['summary']['total_platforms'] > 0


# ============================================
# Telegram Parser (Gercek mesaj formatlari)
# ============================================

def test_telegram_parser_real_message():
    """Gercek bir Telegram mesaji parse edilebiliyor mu?"""
    from telegram_parser import parse_telegram_message
    msg = """🔥 Bluetooth Kulaklik
Fiyat: 299 TL
Komisyon: %25
https://www.trendyol.com/test"""
    result = parse_telegram_message(msg, channel="magazanolsunresmi", message_id=1)
    assert result is not None
    assert "Bluetooth" in result['title']
    assert result['commission_rate'] == 25.0
    assert result['price_numeric'] == 299.0
    assert 'trendyol.com' in result['links'][0]
    assert result['priority'] == 'high'


def test_telegram_parser_rejects_garbage():
    """Urun bilgisi olmayan mesajlari reddediyor mu?"""
    from telegram_parser import parse_telegram_message
    result = parse_telegram_message("Merhaba arkadaslar, hava guzel", channel="test")
    assert result is None


def test_telegram_parser_handles_emoji_decorations():
    """Emoji ve dekorasyonlar basliktan temizleniyor mu?"""
    from telegram_parser import parse_telegram_message
    msg = """⚡ Akilli Saat - Smartwatch X100
💰 Sadece 1.299₺
📊 %30 komisyon"""
    result = parse_telegram_message(msg, channel="test", message_id=2)
    assert result is not None
    assert "⚡" not in result['title']
    assert "💰" not in result['title']
    assert result['commission_rate'] == 30.0


# ============================================
# Tracking DB (Para kazanma zinciri)
# ============================================

def test_tracking_full_chain():
    """Tam para kazanma zinciri (urun → AI → paylasim → satis) calisiyor mu?"""
    from trm_tracking import (
        record_product, record_ai_content, record_social_post,
        record_sale, get_full_chain, get_summary
    )
    product = {
        'title': 'Test Urun - Birim Test',
        'price': '500',
        'commission_rate': 30.0,
        'source': 'test_channel',
        'message_id': 99999,
        'captured_at': '2026-01-01T00:00:00',
        'links': ['https://example.com/test']
    }
    pid = record_product(product)
    assert pid is not None

    cid = record_ai_content(pid, {'content': 'Test', 'ai_confidence': 0.9}, model='mock')
    assert cid is not None

    spid = record_social_post(pid, cid, 'facebook',
                              {'success': True, 'post_id': 'fb_123', 'url': 'http://fb.com/p/123'})
    assert spid is not None

    sid = record_sale(pid, sale_amount=500.0, commission=150.0, post_id=spid)
    assert sid is not None

    chain = get_full_chain(pid)
    assert chain['product']['title'] == 'Test Urun - Birim Test'
    assert len(chain['ai_contents']) >= 1
    assert len(chain['social_posts']) >= 1
    assert len(chain['sales']) >= 1
    assert chain['total_revenue'] >= 150.0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
