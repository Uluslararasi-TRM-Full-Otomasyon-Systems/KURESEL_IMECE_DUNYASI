#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TRM Telegram Mesaj Parser - v2.0 STABLE
Gerçek e-ticaret/affiliate kanallarının mesaj formatlarını parse eder.

Düzeltmeler (v2.0):
  - Encoding: NFC normalize + cp1252→utf-8 otomatik onarım
  - Fiyat regex: binlik nokta (1.299 TL) vs kuruş virgül (1.299,50 TL) ayrımı
  - Komisyon regex: sıkı bağlam — indirim yüzdelerini yanlış eşlemez
  - URL temizleme: trailing noktalama kaldırma
  - parse_old_price: eski/çizili fiyatı da çıkar
  - Öncelik: kazanç potansiyeli = fiyat × komisyon/100
  - parse_batch: çoklu mesaj, öncelik sıralaması
"""

import re
import unicodedata
from datetime import datetime
from typing import Dict, List, Optional

# ── REGEX PANELİ ──────────────────────────────────────────────────────────

COMMISSION_PATTERNS = [
    re.compile(
        r'(?:komisyon|kazanç|kazanc|kâr|kar)\s*[:\-]?\s*%?\s*(\d{1,2}(?:[.,]\d+)?)\s*%?',
        re.IGNORECASE | re.UNICODE,
    ),
    re.compile(
        r'%\s*(\d{1,2}(?:[.,]\d+)?)\s*(?:komisyon|kazanç|kazanc|kâr)',
        re.IGNORECASE | re.UNICODE,
    ),
]

DISCOUNT_PATTERNS = [
    re.compile(
        r'(?:indirim|tasarruf|kampanya)\s*[:\-]?\s*%?\s*(\d{1,2})\s*%?',
        re.IGNORECASE | re.UNICODE,
    ),
    re.compile(
        r'%\s*(\d{1,2})\s*(?:indirim|İNDİRİM|kampanya|off)',
        re.IGNORECASE | re.UNICODE,
    ),
    re.compile(
        r'(?:^|\s)%(\d{1,2})\s+(?:indirim|İNDİRİM)',
        re.IGNORECASE | re.UNICODE | re.MULTILINE,
    ),
]

_AMOUNT = r'(\d{1,3}(?:[.\s]\d{3})*(?:,\d{1,2})?|\d+(?:,\d{1,2})?)'
PRICE_PATTERNS = [
    re.compile(_AMOUNT + r'\s*(?:tl|₺|try|türk\s*lirası|lira)\b', re.IGNORECASE | re.UNICODE),
    re.compile(r'(?:tl|₺|try)\s*' + _AMOUNT, re.IGNORECASE | re.UNICODE),
    re.compile(r'(?:fiyat|sadece|yalnızca|yalnizca)\s*[:\-]?\s*' + _AMOUNT, re.IGNORECASE | re.UNICODE),
]

OLD_PRICE_PATTERNS = [
    re.compile(r'(?:eski|normal|liste|was|before)\s*:?\s*' + _AMOUNT + r'\s*(?:tl|₺|try)?', re.IGNORECASE | re.UNICODE),
    re.compile(r'~~' + _AMOUNT + r'\s*(?:tl|₺|try)?~~', re.IGNORECASE | re.UNICODE),
    re.compile(r'\(' + _AMOUNT + r'\s*(?:tl|₺|try)\)', re.IGNORECASE | re.UNICODE),
]

URL_PATTERN  = re.compile(r'https?://[^\s<>"{}|\\^`\[\]]+')
TRAIL_PUNCT  = re.compile(r'[.,;!?)]+$')

ECOMMERCE_DOMAINS = [
    'trendyol.com', 'hepsiburada.com', 'n11.com', 'amazon.com.tr',
    'gittigidiyor.com', 'cimri.com', 'akakce.com', 'aliexpress.com',
    'tr.aliexpress.com', 'shopee.com', 'amazon.com', 'magazanolsun.com',
    'pttavm.com', 'ciceksepeti.com', 'ebay.com', 'sahibinden.com',
]

EMOJI_RE = re.compile(
    "[\U0001F300-\U0001F9FF\U0001FA00-\U0001FA9F\U00002600-\U000027BF\U0000FE00-\U0000FE0F]+",
    flags=re.UNICODE,
)

# ── YARDIMCILAR ───────────────────────────────────────────────────────────

def _normalize_amount(raw: str) -> Optional[float]:
    s = raw.strip().replace(' ', '')
    if ',' in s:
        int_part, dec_part = s.rsplit(',', 1)
        int_part = int_part.replace('.', '')
        s = f"{int_part}.{dec_part}"
    else:
        parts = s.split('.')
        if len(parts) == 2 and len(parts[1]) <= 2:
            pass  # gerçek kuruş
        else:
            s = s.replace('.', '')
    try:
        return float(s)
    except ValueError:
        return None


def _clean_url(url: str) -> str:
    return TRAIL_PUNCT.sub('', url)


def safe_str(text: str) -> str:
    """UTF-8 güvenliği + cp1252 bozulma onarımı + NFC normalize."""
    if not isinstance(text, str):
        try:
            text = text.decode('utf-8', errors='replace')
        except Exception:
            text = str(text)
    try:
        text = text.encode('latin-1').decode('utf-8')
    except (UnicodeEncodeError, UnicodeDecodeError):
        pass
    return unicodedata.normalize('NFC', text)

# ── PARSE FONKSİYONLARI ───────────────────────────────────────────────────

def parse_price(text: str) -> Optional[float]:
    text = safe_str(text)
    candidates = []
    for pat in PRICE_PATTERNS:
        for m in pat.finditer(text):
            v = _normalize_amount(m.group(1))
            if v and 1.0 <= v <= 1_000_000.0:
                candidates.append(v)
    return min(candidates) if candidates else None


def parse_old_price(text: str) -> Optional[float]:
    text = safe_str(text)
    for pat in OLD_PRICE_PATTERNS:
        for m in pat.finditer(text):
            v = _normalize_amount(m.group(1))
            if v and 1.0 <= v <= 1_000_000.0:
                return v
    return None


def parse_commission(text: str) -> Optional[float]:
    text = safe_str(text)
    for pat in COMMISSION_PATTERNS:
        for m in pat.finditer(text):
            try:
                v = float(m.group(1).replace(',', '.'))
                if 1.0 <= v <= 99.0:
                    return v
            except ValueError:
                pass
    return None


def parse_discount(text: str) -> Optional[float]:
    text = safe_str(text)
    for pat in DISCOUNT_PATTERNS:
        for m in pat.finditer(text):
            try:
                v = float(m.group(1))
                if 1.0 <= v <= 99.0:
                    return v
            except ValueError:
                pass
    return None


def parse_urls(text: str) -> List[str]:
    text = safe_str(text)
    raw = URL_PATTERN.findall(text)
    cleaned = list(dict.fromkeys(_clean_url(u) for u in raw if len(_clean_url(u)) > 10))
    def _key(u):
        for i, d in enumerate(ECOMMERCE_DOMAINS):
            if d in u.lower():
                return i
        return 999
    return sorted(cleaned, key=_key)


def parse_title(text: str) -> str:
    text = safe_str(text)
    lines = [ln.strip() for ln in text.split('\n') if ln.strip()]
    if not lines:
        return ""
    def _clean(ln):
        ln = EMOJI_RE.sub('', ln).strip()
        ln = URL_PATTERN.sub('', ln).strip()
        ln = re.sub(r'\s+', ' ', ln)
        return ln.strip('─—-:|•·').strip()
    for ln in lines:
        t = _clean(ln)
        if len(t) >= 5:
            return t[:250]
    return ""

# ── ANA PARSE ─────────────────────────────────────────────────────────────

def parse_telegram_message(
    text: str,
    channel: str = "",
    message_id: int = 0,
    media_urls: Optional[List[str]] = None,
) -> Optional[Dict]:
    if not text or len(text.strip()) < 5:
        return None
    text = safe_str(text)
    title      = parse_title(text)
    price      = parse_price(text)
    old_price  = parse_old_price(text)
    commission = parse_commission(text)
    discount   = parse_discount(text)
    urls       = parse_urls(text)

    if not title:
        return None
    if not (price or commission or urls):
        return None

    desc_lines = []
    for ln in text.split('\n')[1:]:
        c = EMOJI_RE.sub('', ln).strip()
        c = URL_PATTERN.sub('', c).strip()
        if c:
            desc_lines.append(c)
    description = '\n'.join(desc_lines)[:1000]

    earning = round((price or 0) * (commission or 0) / 100, 2)

    if earning >= 200:
        priority = 'urgent'
    elif commission and commission >= 25:
        priority = 'high'
    elif commission and commission >= 15:
        priority = 'medium'
    elif discount and discount >= 50:
        priority = 'medium'
    else:
        priority = 'low'

    return {
        'title':             title,
        'description':       description,
        'price':             str(price) if price else '',
        'price_numeric':     price,
        'old_price_numeric': old_price,
        'currency':          'TRY',
        'commission_rate':   commission if commission else 0.0,
        'discount_rate':     discount if discount else 0.0,
        'earning_potential': earning,
        'links':             urls,
        'media_urls':        media_urls or [],
        'source':            channel or 'unknown',
        'message_id':        message_id,
        'captured_at':       datetime.now().isoformat(),
        'raw_text':          text,
        'priority':          priority,
    }


def parse_batch(messages: List[Dict]) -> List[Dict]:
    """Çoklu mesaj parse et, önceliğe göre sırala."""
    ORDER = {'urgent': 0, 'high': 1, 'medium': 2, 'low': 3}
    results = [
        r for r in (
            parse_telegram_message(
                text=m.get('text', ''),
                channel=m.get('channel', ''),
                message_id=m.get('message_id', 0),
                media_urls=m.get('media_urls'),
            )
            for m in messages
        ) if r
    ]
    return sorted(results, key=lambda x: ORDER.get(x['priority'], 9))


# ── CLI TEST ──────────────────────────────────────────────────────────────
if __name__ == "__main__":
    tests = [
        ("🔥 Bluetooth Kulaklık Süper Bass\nFiyat: 299 TL (eski 599 TL)\n%50 İNDİRİM!\nKomisyon: %25\nhttps://www.trendyol.com/kulaklik-p-12345",
         "magazanolsunresmi", 101),
        ("⚡ Akıllı Saat X100\n💰 Sadece 1.299₺\n📊 %30 komisyon kazan\nhttps://hepsiburada.com/saat",
         "trendurunler", 102),
        ("TÃ¼rkÃ§e ürün: Spor Ayakkabı 159,99 TL\nhttps://n11.com/spor",
         "test", 103),
        ("Merhaba bugün hava güzel", "test", 104),
        ("💎 Laptop HP EliteBook\n₺12.500\nKomisyon: %15\nhttps://hepsiburada.com/hp",
         "techdeals", 105),
    ]
    print("=" * 70)
    print("🧪 TELEGRAM PARSER v2.0 STABLE")
    print("=" * 70)
    for msg, ch, mid in tests:
        r = parse_telegram_message(msg, channel=ch, message_id=mid)
        print(f"\n--- #{mid} [{ch}] ---")
        if r:
            print(f"✅ {r['title']}")
            print(f"   Fiyat: {r['price_numeric']} TRY | Eski: {r['old_price_numeric']}")
            print(f"   Komisyon: %{r['commission_rate']} | İndirim: %{r['discount_rate']}")
            print(f"   Kazanç: {r['earning_potential']} TRY | Öncelik: {r['priority']}")
            print(f"   URL: {r['links']}")
        else:
            print("⚠️  Parse edilemedi" + (" — BEKLENEN" if mid == 104 else ""))
    print("=" * 70)
