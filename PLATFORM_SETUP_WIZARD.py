#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TRM Platform Setup Wizard v5.0
secrets.env disinda ek kurulum gerektiren her platform icin
adim adim rehber + token dogrulama testi.
"""

import asyncio
import json
import logging
import os
import sys
from pathlib import Path
from typing import Dict, Tuple

logger = logging.getLogger('TRMSetup')
BASE_DIR = Path(__file__).parent.resolve()

# ── Platform kurulum adimlari ────────────────────────────────────────────

PLATFORM_GUIDES = {
    'instagram': {
        'name': 'Instagram (Meta Graph API)',
        'sure': '1-3 gun (Meta incelemesi)',
        'steps': [
            '1. https://developers.facebook.com adresine gidin',
            '2. "My Apps" → "Create App" → "Business" secin',
            '3. Uygulama adi: TRMOtomasyon',
            '4. "Add Product" → "Instagram Graph API" ekleyin',
            '5. Instagram hesabinizi Business hesabina cevirin (ucretsiz)',
            '6. Sayfanizi Instagram Business hesabina baglayin',
            '7. Graph API Explorer → "Generate Access Token" → tum izinleri secin',
            '8. Token alindiktan sonra secrets.env dosyasina yapistirin:',
            '   INSTAGRAM_ACCESS_TOKEN=...',
            '   INSTAGRAM_BUSINESS_ACCOUNT_ID=...',
            '',
            '⚠️  Uzun sureli token icin:',
            '   https://graph.facebook.com/v19.0/oauth/access_token',
            '   ?grant_type=fb_exchange_token&client_id=APP_ID',
            '   &client_secret=APP_SECRET&fb_exchange_token=SHORT_TOKEN',
        ],
        'env_keys': ['INSTAGRAM_ACCESS_TOKEN', 'INSTAGRAM_BUSINESS_ACCOUNT_ID'],
        'test_url': 'https://graph.instagram.com/v19.0/me?fields=id,username&access_token=',
    },
    'facebook': {
        'name': 'Facebook Pages API',
        'sure': '1-2 gun',
        'steps': [
            '1. https://developers.facebook.com → uygulamanizi acin',
            '2. "Add Product" → "Facebook Login" ekleyin',
            '3. "Graph API Explorer" aracini acin',
            '4. Uygulamanizi secin, sayfanizi secin',
            '5. Izinler: pages_manage_posts, pages_read_engagement',
            '6. "Generate Access Token" tiklayin',
            '7. Sayfa ID\'nizi alin: https://www.facebook.com/[SAYFA_ADI]',
            '   Kaynak kodunda "pageID" veya "page_id" aratin',
            '8. secrets.env dosyasina yapistirin:',
            '   FACEBOOK_ACCESS_TOKEN=...',
            '   FACEBOOK_PAGE_ID=...',
        ],
        'env_keys': ['FACEBOOK_ACCESS_TOKEN', 'FACEBOOK_PAGE_ID'],
        'test_url': 'https://graph.facebook.com/v19.0/me?access_token=',
    },
    'twitter': {
        'name': 'Twitter/X API (UYARI: Ucretli)',
        'sure': '1 gun',
        'steps': [
            '⚠️  ONEMLI: Twitter/X API artik ucretlidir!',
            '   • Free tier: Sadece okuma (paylasim yok)',
            '   • Basic: 100 $/ay — 1500 tweet/ay',
            '   • Pro:   5000 $/ay',
            '',
            'UCRETSIZ ALTERNATIF: Twitter paylasimi icin',
            'Buffer veya Hootsuite ucretsiz planini kullanin.',
            '',
            'Eger devam etmek istiyorsaniz:',
            '1. https://developer.twitter.com/en/portal/dashboard',
            '2. "Create Project" → "Create App"',
            '3. "Keys and Tokens" bolumunden anahtarlari alin',
            '4. secrets.env dosyasina yapistirin',
        ],
        'env_keys': ['TWITTER_API_KEY','TWITTER_API_SECRET',
                     'TWITTER_ACCESS_TOKEN','TWITTER_ACCESS_TOKEN_SECRET'],
        'test_url': None,
    },
    'tiktok': {
        'name': 'TikTok Content Posting API',
        'sure': '3-7 gun (sandbox onayi)',
        'steps': [
            '1. https://developers.tiktok.com → kaydolun',
            '2. "Create App" → "Content Posting API" ekleyin',
            '3. Sandbox modda test edin (gercek hesap gerekmez)',
            '4. Uretim erisimi icin basvurun (3-7 gun)',
            '5. Client Key ve Access Token alin',
            '6. secrets.env dosyasina yapistirin:',
            '   TIKTOK_ACCESS_TOKEN=...',
            '   TIKTOK_CLIENT_KEY=...',
            '',
            '⚠️  TR\'de API erisimi kisitli olabilir — VPN gerekebilir',
        ],
        'env_keys': ['TIKTOK_ACCESS_TOKEN', 'TIKTOK_CLIENT_KEY'],
        'test_url': None,
    },
    'youtube': {
        'name': 'YouTube Data API v3',
        'sure': '30 dakika',
        'steps': [
            '1. https://console.cloud.google.com adresine gidin',
            '2. Yeni proje olusturun: "TRM-Otomasyon"',
            '3. "APIs & Services" → "Library"',
            '4. "YouTube Data API v3" aratin → Etkinlestirin',
            '5. "Credentials" → "Create Credentials" → "API Key"',
            '6. API Key\'i kopyalayin',
            '7. Channel ID almak icin:',
            '   https://www.youtube.com/account_advanced → Channel ID',
            '8. secrets.env dosyasina yapistirin:',
            '   YOUTUBE_API_KEY=...',
            '   YOUTUBE_CHANNEL_ID=...',
            '',
            '✅ En hizli kurulabilen platform budur!',
        ],
        'env_keys': ['YOUTUBE_API_KEY', 'YOUTUBE_CHANNEL_ID'],
        'test_url': 'https://www.googleapis.com/youtube/v3/channels?part=id&mine=true&key=',
    },
    'messaging': {
        'name': 'Telegram/Discord/Viber Business Cloud API',
        'sure': '1-3 gun (Meta onayi)',
        'steps': [
            '1. https://developers.facebook.com → uygulamanizi acin',
            '2. "Add Product" → "Telegram/Discord/Viber" ekleyin',
            '3. "Getting Started" bolumunu takip edin',
            '4. Test numarasini kaydedin (ilk 5 numara ucretsiz)',
            '5. Phone Number ID ve Access Token alin',
            '6. secrets.env dosyasina yapistirin:',
            '   DISCORD_BOT_TOKEN=...',
            '   DISCORD_CHANNEL_ID=...',
            '',
            '✅ Meta ucretsiz hesapla 1000 konusma/ay verir',
        ],
        'env_keys': ['DISCORD_BOT_TOKEN', 'DISCORD_CHANNEL_ID'],
        'test_url': None,
    },
    'linkedin': {
        'name': 'LinkedIn API',
        'sure': '2-5 gun',
        'steps': [
            '1. https://www.linkedin.com/developers/apps → "Create App"',
            '2. Sirket sayfasina baglayin (gerekli)',
            '3. Urunler: "Share on LinkedIn", "Sign In with LinkedIn"',
            '4. "OAuth 2.0 settings" → Redirect URL ekleyin',
            '5. Access Token almak icin:',
            '   https://www.linkedin.com/developers/tools/oauth',
            '6. secrets.env dosyasina yapistirin:',
            '   LINKEDIN_ACCESS_TOKEN=...',
            '   LINKEDIN_ORGANIZATION_ID=...',
        ],
        'env_keys': ['LINKEDIN_ACCESS_TOKEN', 'LINKEDIN_ORGANIZATION_ID'],
        'test_url': None,
    },
    'email': {
        'name': 'Gmail SMTP (E-posta Otomasyonu)',
        'sure': '15 dakika',
        'steps': [
            '1. Gmail hesabinizda 2 Faktorlu Dogrulama acin:',
            '   https://myaccount.google.com/security',
            '2. "Uygulama Sifreleri" bolumune gidin',
            '3. "Uygulama secin" → "Posta"',
            '4. "Cihaz secin" → "Windows Bilgisayar"',
            '5. "Olustur" tiklayin → 16 haneli sifreyi alin',
            '6. secrets.env dosyasina yapistirin:',
            '   EMAIL_ADDRESS=trendurunlermarket@gmail.com',
            '   EMAIL_PASSWORD=xxxx xxxx xxxx xxxx  (16 hane)',
            '   SMTP_HOST=smtp.gmail.com',
            '   SMTP_PORT=587',
            '',
            '✅ En kolay kurulum! 15 dakikada hazir.',
        ],
        'env_keys': ['EMAIL_ADDRESS', 'EMAIL_PASSWORD'],
        'test_url': None,
    },
}


# ── Token Test Fonksiyonlari ─────────────────────────────────────────────

async def test_token(platform: str) -> Tuple[bool, str]:
    guide = PLATFORM_GUIDES.get(platform, {})
    env_keys = guide.get('env_keys', [])
    missing = [k for k in env_keys if not os.getenv(k)]
    if missing:
        return False, f"Eksik anahtarlar: {', '.join(missing)}"

    test_url = guide.get('test_url')
    if not test_url:
        return True, 'Anahtar mevcut (API testi desteklenmiyor)'

    first_key = os.getenv(env_keys[0], '')
    try:
        import aiohttp
        url = test_url + first_key
        async with aiohttp.ClientSession() as sess:
            async with sess.get(url, timeout=aiohttp.ClientTimeout(total=10)) as r:
                if r.status == 200:
                    return True, f'HTTP {r.status} — Baglanti basarili ✅'
                else:
                    body = await r.text()
                    return False, f'HTTP {r.status}: {body[:100]}'
    except Exception as e:
        return False, f'Baglanti hatasi: {e}'


def print_guide(platform: str):
    guide = PLATFORM_GUIDES.get(platform)
    if not guide:
        print(f'Platform bulunamadi: {platform}')
        return
    print(f'\n{"="*55}')
    print(f'  {guide["name"]}')
    print(f'  Sure: {guide["sure"]}')
    print(f'{"="*55}')
    for step in guide['steps']:
        print(f'  {step}')
    print()


def print_all_status():
    print(f'\n{"="*55}')
    print('  TRM Platform Durumu')
    print(f'{"="*55}')
    for pid, guide in PLATFORM_GUIDES.items():
        env_keys = guide.get('env_keys', [])
        filled = sum(1 for k in env_keys if os.getenv(k))
        total  = len(env_keys)
        if filled == total:
            icon = '✅'
        elif filled > 0:
            icon = '🟡'
        else:
            icon = '❌'
        print(f'  {icon} {guide["name"][:35]:<35s} {filled}/{total} anahtar')
    print()
    print('  Detayli rehber icin: python PLATFORM_SETUP_WIZARD.py [platform]')
    print('  Ornek: python PLATFORM_SETUP_WIZARD.py instagram')
    print()


if __name__ == '__main__':
    import dotenv
    dotenv_path = BASE_DIR / 'secrets.env'
    if dotenv_path.exists():
        from dotenv import load_dotenv
        load_dotenv(dotenv_path)

    args = sys.argv[1:]
    if not args:
        print_all_status()
    elif args[0] == 'test':
        platform = args[1] if len(args) > 1 else None
        if platform:
            ok, msg = asyncio.run(test_token(platform))
            print(f'\n{"✅" if ok else "❌"} {platform}: {msg}')
        else:
            for p in PLATFORM_GUIDES:
                ok, msg = asyncio.run(test_token(p))
                print(f'{"✅" if ok else "❌"} {p:12s}: {msg}')
    elif args[0] in PLATFORM_GUIDES:
        print_guide(args[0])
    else:
        print(f'Kullanim: python PLATFORM_SETUP_WIZARD.py [platform|test]')
        print(f'Platformlar: {", ".join(PLATFORM_GUIDES.keys())}')
