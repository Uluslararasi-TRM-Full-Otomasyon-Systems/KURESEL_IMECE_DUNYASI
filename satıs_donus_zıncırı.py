#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TRM - GERCEK SATIS DONUS ZINCIRI (v1.0)
=========================================
Akis: Urun yakalandi → AI icerik uretildi → Sosyal medyada yayinlandi
      → Affiliate linke tiklama → Satis gerceklesti → Komisyon kaydedildi
      → Raporlama

Bu modul:
  1. Affiliate link olusturma (Trendyol, Hepsiburada, Amazon TR, N11)
  2. Tiklama/conversion webhook alma (platform geri bildirimleri)
  3. Satis zincirini SQLite'a kaydetme (trm_tracking.py entegrasyonu)
  4. Gunluk/haftalik kazanc raporu
  5. Komisyon beklenti vs gerceklesme karsilastirmasi
"""

import os
import json
import logging
import sqlite3
from contextlib import contextmanager
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional
from urllib.parse import urlencode, urlparse, parse_qs, urljoin

logger = logging.getLogger(__name__)

DB_PATH = Path(__file__).parent / "data" / "trm_tracking.db"


@contextmanager
def get_conn():
    DB_PATH.parent.mkdir(exist_ok=True)
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


# ─────────────────────────────────────────────────────────────────────
# 1. AFFILIATE LINK OLUSTURMA
# ─────────────────────────────────────────────────────────────────────

class AffiliateLinkBuilder:
    """
    Platformlara gore affiliate parametresi ekler.
    Her platforma ozel UTM + affiliate ID yapisi.
    """

    def __init__(self):
        self.ids = {
            'trendyol':    os.getenv('TRENDYOL_AFFILIATE_ID', ''),
            'hepsiburada': os.getenv('HEPSIBURADA_AFFILIATE_ID', ''),
            'amazon':      os.getenv('AMAZON_ASSOCIATE_ID', ''),
            'n11':         os.getenv('N11_AFFILIATE_ID', ''),
        }
        self.utm_source  = 'trm_bot'
        self.utm_medium  = 'social'

    def build(self, raw_url: str, product_id: Optional[int] = None,
              campaign: str = '') -> str:
        """Ham URL'ye affiliate ve UTM parametreleri ekle."""
        if not raw_url:
            return raw_url

        parsed = urlparse(raw_url)
        domain = parsed.netloc.lower()
        params = {}

        # Platform tespiti
        if 'trendyol.com' in domain and self.ids['trendyol']:
            params['boutiqueId']  = self.ids['trendyol']
            params['merchantId']  = self.ids['trendyol']
        elif 'hepsiburada.com' in domain and self.ids['hepsiburada']:
            params['affiliateId'] = self.ids['hepsiburada']
        elif 'amazon.com.tr' in domain and self.ids['amazon']:
            params['tag'] = self.ids['amazon']
        elif 'n11.com' in domain and self.ids['n11']:
            params['partnerId'] = self.ids['n11']

        # UTM parametreleri
        params['utm_source']   = self.utm_source
        params['utm_medium']   = self.utm_medium
        params['utm_campaign'] = campaign or 'trm_auto'
        if product_id:
            params['utm_content'] = f'pid_{product_id}'

        # Mevcut query string'i koru ve ekle
        existing = parse_qs(parsed.query)
        for k, v in params.items():
            existing[k] = [v]
        new_query = urlencode({k: v[0] for k, v in existing.items()})

        return parsed._replace(query=new_query).geturl()

    def build_for_product(self, product: Dict) -> List[str]:
        """Urunun tum linklerini affiliate'e cevir."""
        pid = product.get('id') or product.get('product_id')
        return [self.build(url, product_id=pid) for url in (product.get('links') or [])]


# ─────────────────────────────────────────────────────────────────────
# 2. DONUS / CONVERSION KAYIT
# ─────────────────────────────────────────────────────────────────────

def ensure_sales_chain_tables():
    """Satis zinciri ve temel tablolari olustur (trm_tracking.py ile uyumlu)."""
    with get_conn() as conn:
        conn.executescript("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            source TEXT NOT NULL,
            source_message_id TEXT,
            title TEXT NOT NULL,
            description TEXT,
            price REAL,
            currency TEXT DEFAULT 'TRY',
            commission_rate REAL,
            product_url TEXT,
            image_urls TEXT,
            raw_message TEXT,
            captured_at TEXT NOT NULL,
            status TEXT DEFAULT 'captured',
            UNIQUE(source, source_message_id, title)
        );

        CREATE TABLE IF NOT EXISTS social_posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id INTEGER NOT NULL,
            content_id INTEGER,
            platform TEXT NOT NULL,
            post_id TEXT,
            post_url TEXT,
            success INTEGER NOT NULL,
            error_message TEXT,
            published_at TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS sales_events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id INTEGER NOT NULL,
            post_id INTEGER,
            sale_amount REAL NOT NULL,
            commission_earned REAL NOT NULL,
            currency TEXT DEFAULT 'TRY',
            buyer_info TEXT,
            platform TEXT DEFAULT '',
            sold_at TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS affiliate_clicks (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id  INTEGER,
            post_id     INTEGER,
            platform    TEXT,           -- trendyol / hepsiburada / amazon / n11
            affiliate_url TEXT,
            clicked_at  TEXT NOT NULL,
            ip_hash     TEXT,           -- anonim (MD5/SHA256 kisaltma)
            user_agent  TEXT
        );

        CREATE TABLE IF NOT EXISTS commission_payments (
            id              INTEGER PRIMARY KEY AUTOINCREMENT,
            sale_event_id   INTEGER,
            platform        TEXT NOT NULL,
            payment_date    TEXT,
            expected_amount REAL,
            actual_amount   REAL,
            status          TEXT DEFAULT 'pending',  -- pending/paid/rejected
            notes           TEXT,
            created_at      TEXT NOT NULL
        );

        CREATE INDEX IF NOT EXISTS idx_clicks_product ON affiliate_clicks(product_id);
        CREATE INDEX IF NOT EXISTS idx_commission_status ON commission_payments(status);
        """)


def record_click(product_id: int, affiliate_url: str,
                 platform: str = '', post_id: Optional[int] = None) -> int:
    """Affiliate link tiklamasini kaydet."""
    ensure_sales_chain_tables()
    with get_conn() as conn:
        c = conn.cursor()
        c.execute("""
            INSERT INTO affiliate_clicks
              (product_id, post_id, platform, affiliate_url, clicked_at)
            VALUES (?, ?, ?, ?, ?)
        """, (product_id, post_id, platform, affiliate_url, datetime.now().isoformat()))
        return c.lastrowid


def record_sale_full(
    product_id:      int,
    sale_amount:     float,
    commission_rate: float,
    platform:        str = '',
    post_id:         Optional[int] = None,
    click_id:        Optional[int] = None,
    buyer_info:      str = '',
) -> Dict:
    """
    Satisi kaydet, komisyon bekletisini hesapla.
    Returns: {sale_event_id, commission_event_id, commission_earned, status}
    """
    ensure_sales_chain_tables()
    commission_earned = round(sale_amount * commission_rate / 100, 2)
    now = datetime.now().isoformat()

    with get_conn() as conn:
        c = conn.cursor()

        # 1. sales_events (trm_tracking.py ile uyumlu)
        c.execute("""
            INSERT INTO sales_events
              (product_id, post_id, sale_amount, commission_earned, buyer_info, sold_at)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (product_id, post_id, sale_amount, commission_earned, buyer_info, now))
        sale_id = c.lastrowid

        # 2. Urun durumunu guncelle
        c.execute("UPDATE products SET status='sold' WHERE id=?", (product_id,))

        # 3. Komisyon beklenti kaydi
        c.execute("""
            INSERT INTO commission_payments
              (sale_event_id, platform, expected_amount, status, created_at)
            VALUES (?, ?, ?, 'pending', ?)
        """, (sale_id, platform, commission_earned, now))
        comm_id = c.lastrowid

    logger.info(
        f"✅ Satis kaydedildi | Urun #{product_id} | "
        f"{sale_amount:.2f} TRY | Komisyon: {commission_earned:.2f} TRY"
    )
    return {
        'sale_event_id':       sale_id,
        'commission_event_id': comm_id,
        'commission_earned':   commission_earned,
        'status':              'pending',
    }


def confirm_commission_payment(commission_event_id: int,
                                actual_amount: float,
                                notes: str = ''):
    """Platform tarafindan komisyon odemesi onaylandiginda cagir."""
    with get_conn() as conn:
        conn.execute("""
            UPDATE commission_payments
            SET actual_amount=?, status='paid', payment_date=?, notes=?
            WHERE id=?
        """, (actual_amount, datetime.now().isoformat(), notes, commission_event_id))
    logger.info(f"💰 Komisyon odendi: #{commission_event_id} → {actual_amount:.2f} TRY")


# ─────────────────────────────────────────────────────────────────────
# 3. RAPOR
# ─────────────────────────────────────────────────────────────────────

def get_chain_report(days: int = 30) -> Dict:
    """Son N gunluk satis zinciri raporu."""
    ensure_sales_chain_tables()
    since = (datetime.now() - timedelta(days=days)).isoformat()

    with get_conn() as conn:
        c = conn.cursor()

        # Toplam satis
        c.execute("""
            SELECT COUNT(*) as cnt,
                   COALESCE(SUM(sale_amount), 0) as total_sales,
                   COALESCE(SUM(commission_earned), 0) as total_commission
            FROM sales_events WHERE sold_at >= ?
        """, (since,))
        sales_row = c.fetchone()

        # Bekleyen komisyon
        c.execute("""
            SELECT COALESCE(SUM(cp.expected_amount), 0) as pending
            FROM commission_payments cp
            JOIN sales_events se ON cp.sale_event_id = se.id
            WHERE cp.status = 'pending' AND se.sold_at >= ?
        """, (since,))
        pending_row = c.fetchone()

        # Odenen komisyon
        c.execute("""
            SELECT COALESCE(SUM(actual_amount), 0) as paid
            FROM commission_payments
            WHERE status = 'paid' AND payment_date >= ?
        """, (since,))
        paid_row = c.fetchone()

        # Tiklama sayisi
        c.execute("SELECT COUNT(*) as cnt FROM affiliate_clicks WHERE clicked_at >= ?", (since,))
        clicks_row = c.fetchone()

        # Platform bazli
        c.execute("""
            SELECT platform,
                   COUNT(*) as sales,
                   SUM(sale_amount) as revenue,
                   SUM(commission_earned) as commission
            FROM sales_events
            WHERE sold_at >= ?
            GROUP BY platform
            ORDER BY commission DESC
        """, (since,))
        by_platform = [dict(r) for r in c.fetchall()]

    return {
        'period_days':        days,
        'total_sales':        sales_row['cnt'],
        'total_revenue_try':  round(sales_row['total_sales'], 2),
        'total_commission':   round(sales_row['total_commission'], 2),
        'pending_commission': round(pending_row['pending'], 2),
        'paid_commission':    round(paid_row['paid'], 2),
        'total_clicks':       clicks_row['cnt'],
        'conversion_rate':    (
            round(sales_row['cnt'] / clicks_row['cnt'] * 100, 2)
            if clicks_row['cnt'] else 0.0
        ),
        'by_platform':        by_platform,
        'generated_at':       datetime.now().isoformat(),
    }


def print_chain_report(days: int = 30):
    """Raporu konsola yazdir."""
    r = get_chain_report(days)
    print("\n" + "=" * 60)
    print(f"  📊 SATIS DONUS ZINCIRI RAPORU — Son {r['period_days']} Gun")
    print("=" * 60)
    print(f"  Toplam Satis       : {r['total_sales']} adet")
    print(f"  Toplam Ciro        : {r['total_revenue_try']:,.2f} TRY")
    print(f"  Toplam Komisyon    : {r['total_commission']:,.2f} TRY")
    print(f"  Bekleyen Komisyon  : {r['pending_commission']:,.2f} TRY")
    print(f"  Odenen Komisyon    : {r['paid_commission']:,.2f} TRY")
    print(f"  Tiklama Sayisi     : {r['total_clicks']}")
    print(f"  Donusum Orani      : %{r['conversion_rate']}")
    if r['by_platform']:
        print("\n  Platform Dagilimi:")
        for p in r['by_platform']:
            print(f"    {p['platform'] or 'bilinmiyor':15s} "
                  f"| {p['sales']} satis | {p['commission']:,.2f} TRY komisyon")
    print("=" * 60 + "\n")


# ─────────────────────────────────────────────────────────────────────
# WEBHOOK ENDPOINT (Flask ile kullanim icin)
# ─────────────────────────────────────────────────────────────────────

def handle_platform_webhook(payload: Dict) -> Dict:
    """
    Platform geri bildirimi (postback) isle.
    Trendyol, HB gibi platformlar satis sonrasi bu endpoint'i cagirir.

    Beklenen payload:
        {
          "platform": "trendyol",
          "event":    "sale",          # sale | click | cancel
          "product_id": 123,
          "sale_amount": 299.0,
          "commission_rate": 25.0,
          "order_id": "TY-99999"
        }
    """
    platform      = payload.get('platform', 'unknown')
    event         = payload.get('event', '')
    product_id    = payload.get('product_id')
    sale_amount   = float(payload.get('sale_amount', 0))
    commission_rate = float(payload.get('commission_rate', 0))
    order_id      = payload.get('order_id', '')

    if event == 'click':
        cid = record_click(product_id=product_id or 0,
                           affiliate_url=payload.get('url', ''),
                           platform=platform)
        return {'ok': True, 'click_id': cid}

    elif event == 'sale' and product_id and sale_amount:
        result = record_sale_full(
            product_id=product_id,
            sale_amount=sale_amount,
            commission_rate=commission_rate,
            platform=platform,
            buyer_info=order_id,
        )
        return {'ok': True, **result}

    elif event == 'cancel':
        logger.warning(f"❌ Iptal bildirimi: {payload}")
        return {'ok': True, 'note': 'cancel noted'}

    return {'ok': False, 'error': f'Unknown event: {event}'}


# ─────────────────────────────────────────────────────────────────────
# CLI
# ─────────────────────────────────────────────────────────────────────
if __name__ == '__main__':
    import sys
    ensure_sales_chain_tables()

    if len(sys.argv) > 1 and sys.argv[1] == 'test':
        print("🧪 Satis Zinciri Test")
        # Mock urun kayit testi
        result = record_sale_full(
            product_id=1,
            sale_amount=299.0,
            commission_rate=25.0,
            platform='trendyol',
        )
        print(f"Satis kaydedildi: {result}")

        # Affiliate link testi
        builder = AffiliateLinkBuilder()
        test_url = "https://www.trendyol.com/marka/urun-p-12345"
        aff_url = builder.build(test_url, product_id=1, campaign='test_camp')
        print(f"Affiliate URL: {aff_url}")

    print_chain_report(days=30)
