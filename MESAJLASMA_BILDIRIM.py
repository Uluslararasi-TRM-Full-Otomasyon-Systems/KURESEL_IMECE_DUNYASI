#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TRM Mesajlaşma Bildirim Sistemi v5.2
Telegram, Discord ve Viber üzerinden otomatik bildirim gönderir.
(Telegram/Discord/Viber Business API yerine ücretsiz ve kolay alternatifler)

Hangi platform ne zaman kullanılır:
  - Telegram  → anlık satış/hata bildirimleri (en hızlı)
  - Discord   → ekip bildirimleri, webhook ile kolay
  - Viber     → müşteri iletişimi, Türkiye'de yaygın
"""

import asyncio
import json
import logging
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional

logger = logging.getLogger('TRMBildirim')

SHOP_LINK = os.getenv('TRENDYOL_AFFILIATE_LINK', 'https://trendurunlermarket.com')


async def _post_json(url: str, payload: dict, headers: dict = None,
                     timeout: int = 10) -> tuple:
    """Genel async HTTP POST."""
    try:
        import aiohttp
        async with aiohttp.ClientSession() as sess:
            async with sess.post(
                url, json=payload,
                headers=headers or {},
                timeout=aiohttp.ClientTimeout(total=timeout),
            ) as r:
                return r.status, await r.text()
    except Exception as e:
        return 0, str(e)


# ── Telegram Bildirimi ────────────────────────────────────────────────

async def telegram_bildir(mesaj: str, parse_mode: str = 'HTML') -> bool:
    """Telegram bot ile bildirim gönder."""
    token   = os.getenv('TELEGRAM_BOT_TOKEN', '')
    chat_id = os.getenv('TELEGRAM_CHAT_ID', '')
    if not (token and chat_id):
        logger.debug('Telegram token/chat_id eksik')
        return False
    url = f'https://api.telegram.org/bot{token}/sendMessage'
    status, _ = await _post_json(url, {
        'chat_id': chat_id,
        'text': mesaj[:4096],
        'parse_mode': parse_mode,
    })
    return status == 200


# ── Discord Webhook Bildirimi ─────────────────────────────────────────

async def discord_bildir(mesaj: str) -> bool:
    """Discord webhook ile bildirim gönder (en kolay kurulum)."""
    webhook_url = os.getenv('DISCORD_WEBHOOK_URL', '')
    if not webhook_url:
        logger.debug('DISCORD_WEBHOOK_URL eksik')
        return False
    status, _ = await _post_json(webhook_url, {
        'content':  mesaj[:2000],
        'username': '🛍️ TRM Otomasyon',
    })
    return status in (200, 204)


# ── Viber Bildirimi ───────────────────────────────────────────────────

async def viber_bildir(mesaj: str, alici_id: str = '') -> bool:
    """Viber bot ile bildirim gönder."""
    token    = os.getenv('VIBER_BOT_TOKEN', '')
    alici_id = alici_id or os.getenv('VIBER_RECIPIENT_ID', '')
    if not (token and alici_id):
        logger.debug('VIBER_BOT_TOKEN veya VIBER_RECIPIENT_ID eksik')
        return False
    status, _ = await _post_json(
        'https://chatapi.viber.com/pa/send_message',
        {
            'receiver': alici_id,
            'type':     'text',
            'text':     mesaj[:7000],
            'sender':   {'name': 'TRM Otomasyon'},
        },
        headers={'X-Viber-Auth-Token': token, 'Content-Type': 'application/json'},
    )
    return status == 200


# ── Tüm kanallara gönder ─────────────────────────────────────────────

async def herkese_bildir(mesaj: str) -> Dict[str, bool]:
    """Telegram + Discord + Viber üçüne birden gönder."""
    sonuclar = {}
    sonuclar['telegram'] = await telegram_bildir(mesaj)
    sonuclar['discord']  = await discord_bildir(mesaj)
    sonuclar['viber']    = await viber_bildir(mesaj)

    basarili = sum(sonuclar.values())
    logger.info(f'Bildirim gönderildi: {basarili}/3 kanal başarılı')
    return sonuclar


# ── Hazır bildirim şablonları ─────────────────────────────────────────

async def satis_bildirimi(urun_adi: str, fiyat: str,
                           komisyon: float, platform: str) -> Dict:
    mesaj = (
        f"💰 <b>YENİ SATIŞ!</b>\n"
        f"━━━━━━━━━━━━━━━━\n"
        f"📦 Ürün: {urun_adi}\n"
        f"💲 Fiyat: {fiyat}\n"
        f"🏆 Komisyon: %{komisyon}\n"
        f"📱 Platform: {platform}\n"
        f"🕐 Zaman: {datetime.now().strftime('%d.%m.%Y %H:%M')}\n"
        f"━━━━━━━━━━━━━━━━\n"
        f"🔗 {SHOP_LINK}"
    )
    return await herkese_bildir(mesaj)


async def hata_bildirimi(hata: str, modul: str = '') -> Dict:
    mesaj = (
        f"🚨 <b>SİSTEM HATASI</b>\n"
        f"━━━━━━━━━━━━━━━━\n"
        f"⚠️ Modül: {modul or 'Bilinmiyor'}\n"
        f"❌ Hata: {hata[:300]}\n"
        f"🕐 {datetime.now().strftime('%d.%m.%Y %H:%M')}"
    )
    return await herkese_bildir(mesaj)


async def gunluk_ozet(istatistik: Dict) -> Dict:
    mesaj = (
        f"📊 <b>GÜNLÜK ÖZET</b>\n"
        f"━━━━━━━━━━━━━━━━\n"
        f"📤 Paylaşım: {istatistik.get('posts', 0)}\n"
        f"👆 Tıklama: {istatistik.get('clicks', 0)}\n"
        f"🛒 Satış: {istatistik.get('sales', 0)}\n"
        f"💰 Kazanç: {istatistik.get('earned', 0):.2f} TRY\n"
        f"🕐 {datetime.now().strftime('%d.%m.%Y')}"
    )
    return await herkese_bildir(mesaj)


def durum_goster():
    """Hangi platformların aktif olduğunu göster."""
    platformlar = {
        'Telegram': bool(os.getenv('TELEGRAM_BOT_TOKEN') and os.getenv('TELEGRAM_CHAT_ID')),
        'Discord Webhook': bool(os.getenv('DISCORD_WEBHOOK_URL')),
        'Discord Bot': bool(os.getenv('DISCORD_BOT_TOKEN')),
        'Viber': bool(os.getenv('VIBER_BOT_TOKEN')),
    }
    print('\n╔══════════════════════════════════════════╗')
    print('║   TRM Mesajlaşma Bildirim Sistemi         ║')
    print('╠══════════════════════════════════════════╣')
    for p, aktif in platformlar.items():
        ikon = '✅' if aktif else '⚠️ '
        print(f'║  {ikon} {p:<35s}║')
    print('╚══════════════════════════════════════════╝\n')
    print('Kurulum (kolaydan zora):')
    print('  1. Discord Webhook → Kanal Ayarları → Entegrasyonlar → Webhook (2 dakika!)')
    print('  2. Telegram Bot    → t.me/BotFather → /newbot (5 dakika)')
    print('  3. Viber Bot       → partners.viber.com (15 dakika)')


if __name__ == '__main__':
    import sys, dotenv
    from pathlib import Path
    env = Path(__file__).parent / 'secrets.env'
    if env.exists():
        from dotenv import load_dotenv
        load_dotenv(env)

    logging.basicConfig(level=logging.INFO)
    durum_goster()

    if '--test' in sys.argv:
        async def test():
            print('\nTest bildirimi gönderiliyor...')
            r = await herkese_bildir('✅ TRM Test Bildirimi — Sistem çalışıyor!')
            for p, ok in r.items():
                print(f"  {p}: {'✅ Gönderildi' if ok else '❌ Başarısız'}")
        asyncio.run(test())
