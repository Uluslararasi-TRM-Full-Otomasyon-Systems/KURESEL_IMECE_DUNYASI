#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TRM Security Manager v5.0 - Madde 12: API limit koruması, spam koruması,
ban risk azaltma, secret/token güvenliği.
"""

import asyncio
import hashlib
import hmac
import json
import logging
import os
import re
import time
from collections import defaultdict, deque
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, Optional, Tuple

logger = logging.getLogger('TRMSecurity')

BASE_DIR = Path(__file__).parent.resolve()
DATA_DIR = BASE_DIR / 'data'
DATA_DIR.mkdir(exist_ok=True)

# ── Platform API limit tanımları ────────────────────────────────────────

PLATFORM_LIMITS = {
    'instagram':  {'posts_per_hour': 2,  'posts_per_day': 10,  'min_gap_sec': 1800},
    'facebook':   {'posts_per_hour': 5,  'posts_per_day': 25,  'min_gap_sec': 720},
    'twitter':    {'posts_per_hour': 3,  'posts_per_day': 15,  'min_gap_sec': 1200},
    'tiktok':     {'posts_per_hour': 2,  'posts_per_day': 8,   'min_gap_sec': 1800},
    'linkedin':   {'posts_per_hour': 2,  'posts_per_day': 10,  'min_gap_sec': 1800},
    'youtube':    {'posts_per_hour': 1,  'posts_per_day': 5,   'min_gap_sec': 3600},
    'messaging':   {'posts_per_hour': 5,  'posts_per_day': 30,  'min_gap_sec': 720},
    'telegram':   {'posts_per_hour': 10, 'posts_per_day': 50,  'min_gap_sec': 360},
    'blog':       {'posts_per_hour': 3,  'posts_per_day': 15,  'min_gap_sec': 1200},
    'deepseek':   {'posts_per_hour': 60, 'posts_per_day': 1000,'min_gap_sec': 1},
    'openai':     {'posts_per_hour': 60, 'posts_per_day': 1000,'min_gap_sec': 1},
}

# ── Rate Limiter ─────────────────────────────────────────────────────────

class RateLimiter:
    """Token bucket + sliding window rate limiter."""

    def __init__(self):
        self._windows: Dict[str, deque] = defaultdict(deque)
        self._last_post: Dict[str, float] = {}

    def can_post(self, platform: str) -> Tuple[bool, str]:
        """Bu platforma şimdi paylaşılabilir mi? (bool, neden)"""
        limits = PLATFORM_LIMITS.get(platform, PLATFORM_LIMITS['telegram'])
        now = time.time()
        window = self._windows[platform]

        # Min gap kontrolü
        last = self._last_post.get(platform, 0)
        gap = now - last
        if gap < limits['min_gap_sec']:
            wait = int(limits['min_gap_sec'] - gap)
            return False, f'{platform}: son paylaşımdan {wait}s daha bekle'

        # Sliding window — eski kayıtları temizle
        hour_ago = now - 3600
        day_ago  = now - 86400
        while window and window[0] < day_ago:
            window.popleft()

        hourly = sum(1 for t in window if t > hour_ago)
        daily  = len(window)

        if hourly >= limits['posts_per_hour']:
            return False, f'{platform}: saatlik limit ({limits["posts_per_hour"]}) doldu'
        if daily >= limits['posts_per_day']:
            return False, f'{platform}: günlük limit ({limits["posts_per_day"]}) doldu'

        return True, 'ok'

    def record_post(self, platform: str):
        now = time.time()
        self._windows[platform].append(now)
        self._last_post[platform] = now

    async def wait_and_post(self, platform: str, max_wait_sec: int = 3600) -> bool:
        """Uygun olana kadar bekle, sonra izin ver."""
        waited = 0
        while waited < max_wait_sec:
            ok, reason = self.can_post(platform)
            if ok:
                return True
            limits = PLATFORM_LIMITS.get(platform, {})
            sleep = min(limits.get('min_gap_sec', 60), max_wait_sec - waited)
            logger.info(f'Rate limit bekleniyor ({reason}) — {sleep}s uyku')
            await asyncio.sleep(sleep)
            waited += sleep
        return False

    def status(self) -> Dict:
        now = time.time()
        result = {}
        for platform in PLATFORM_LIMITS:
            can, reason = self.can_post(platform)
            hour_ago = now - 3600
            hourly = sum(1 for t in self._windows[platform] if t > hour_ago)
            daily  = len(self._windows[platform])
            limits = PLATFORM_LIMITS[platform]
            result[platform] = {
                'can_post': can,
                'reason': reason if not can else None,
                'hourly': f'{hourly}/{limits["posts_per_hour"]}',
                'daily': f'{daily}/{limits["posts_per_day"]}',
            }
        return result


# ── Spam / İçerik Koruması ──────────────────────────────────────────────

class SpamGuard:
    """Tekrarlayan içerikleri ve spam'i engelle."""

    SPAM_PHRASES = [
        r'ücretsiz kazan',r'0 yatırım',r'garantili kazanç',
        r'anında para',r'sınırsız gelir',r'hızlı zengin',
        r'100% garantili',r'risk yok',r'dolar kazan',
    ]

    def __init__(self):
        self._hashes: deque = deque(maxlen=1000)  # son 1000 içerik hash'i
        self._spam_patterns = [re.compile(p, re.I|re.U) for p in self.SPAM_PHRASES]

    def is_duplicate(self, content: str) -> bool:
        h = hashlib.sha256(content.strip().encode()).hexdigest()[:16]
        if h in self._hashes:
            return True
        self._hashes.append(h)
        return False

    def has_spam(self, content: str) -> Tuple[bool, Optional[str]]:
        for pattern in self._spam_patterns:
            m = pattern.search(content)
            if m:
                return True, m.group(0)
        return False, None

    def sanitize(self, content: str) -> str:
        """Spam ifadeleri kaldır, Türkçe encoding düzelt."""
        for pattern in self._spam_patterns:
            content = pattern.sub('', content)
        # Çift boşlukları temizle
        content = re.sub(r'\n{3,}', '\n\n', content)
        content = re.sub(r' {2,}', ' ', content)
        return content.strip()


# ── Token / Secret Güvenliği ────────────────────────────────────────────

SENSITIVE_KEYS = [
    'API_KEY', 'API_SECRET', 'ACCESS_TOKEN', 'TOKEN', 'SECRET',
    'PASSWORD', 'HASH', 'IBAN', 'PRIVATE', 'CLIENT_SECRET',
]

def mask_secret(value: str) -> str:
    if len(value) <= 8:
        return '***'
    return value[:4] + '...' + value[-4:]

def audit_secrets_file(env_path: str) -> Dict:
    """secrets.env dosyasını denetle — doldurulan/boş anahtarlar."""
    path = Path(env_path)
    if not path.exists():
        return {'error': f'{env_path} bulunamadı'}

    filled, empty, total = [], [], 0
    for line in path.read_text(encoding='utf-8').splitlines():
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        if '=' not in line:
            continue
        total += 1
        key, _, val = line.partition('=')
        key = key.strip()
        val = val.strip()
        if val:
            filled.append(key)
        else:
            empty.append(key)

    return {
        'total': total,
        'filled': len(filled),
        'empty': len(empty),
        'empty_keys': empty,
        'fill_rate': f'{len(filled)/total*100:.0f}%' if total else '0%',
    }

def validate_token_format(key: str, value: str) -> Tuple[bool, str]:
    """Temel format kontrolü."""
    if not value:
        return False, 'Boş değer'
    if key in ('TELEGRAM_API_ID',) and not value.isdigit():
        return False, 'Sayı olmalı'
    if 'IBAN' in key and not re.match(r'^TR\d{24}$', value.replace(' ','')):
        return False, "IBAN formatı: TR + 24 rakam"
    if len(value) < 10 and key not in ('TELEGRAM_API_ID','TRM_LOG_LEVEL','TRM_CHECK_INTERVAL'):
        return False, 'Çok kısa değer'
    return True, 'ok'


# ── Singleton örnekler ──────────────────────────────────────────────────

rate_limiter = RateLimiter()
spam_guard   = SpamGuard()


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    env = str(Path(__file__).parent / 'secrets.env')
    report = audit_secrets_file(env)
    print('\n=== Secrets Denetim Raporu ===')
    print(f"Toplam anahtar : {report.get('total')}")
    print(f"Doldurulmuş    : {report.get('filled')} ({report.get('fill_rate')})")
    print(f"Boş anahtarlar : {report.get('empty')}")
    if report.get('empty_keys'):
        print('  ' + '\n  '.join(report['empty_keys']))
    print('\n=== Rate Limit Durumu ===')
    for platform, st in rate_limiter.status().items():
        print(f"  {platform:12s} {st['hourly']:8s}  {st['daily']}")
