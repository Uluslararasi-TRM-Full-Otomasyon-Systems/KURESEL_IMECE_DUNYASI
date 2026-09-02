#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TRM Tracking Database - Para kazanma kanıt zinciri için SQLite tabanlı takip

Akış: Telegram ürün → AI içerik → Sosyal paylaşım → Satış linki → Komisyon takibi
Tüm aşamaları kayıt altına alır, raporlanabilir hale getirir.
"""

import sqlite3
import logging
import json
from contextlib import contextmanager
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)

DB_PATH = Path(__file__).parent / "data" / "trm_tracking.db"


def init_db():
    """Veritabanını ve tabloları oluştur"""
    DB_PATH.parent.mkdir(exist_ok=True)
    with get_conn() as conn:
        c = conn.cursor()
        c.executescript("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            source TEXT NOT NULL,                -- telegram kanal adı / web url
            source_message_id TEXT,              -- Telegram message_id
            title TEXT NOT NULL,
            description TEXT,
            price REAL,
            currency TEXT DEFAULT 'TRY',
            commission_rate REAL,                -- yüzde olarak (örn 25.0)
            product_url TEXT,                    -- satış/affiliate linki
            image_urls TEXT,                     -- JSON liste
            raw_message TEXT,                    -- orijinal Telegram mesajı
            captured_at TEXT NOT NULL,
            status TEXT DEFAULT 'captured',      -- captured/processed/published/sold
            UNIQUE(source, source_message_id, title)
        );

        CREATE TABLE IF NOT EXISTS ai_content (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id INTEGER NOT NULL,
            content_text TEXT NOT NULL,
            hashtags TEXT,
            ai_model TEXT,                       -- deepseek/claude/mock
            ai_confidence REAL,
            created_at TEXT NOT NULL,
            FOREIGN KEY(product_id) REFERENCES products(id)
        );

        CREATE TABLE IF NOT EXISTS social_posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id INTEGER NOT NULL,
            content_id INTEGER,
            platform TEXT NOT NULL,              -- facebook/instagram/twitter/youtube/tiktok/blog
            post_id TEXT,                        -- platform tarafındaki post id
            post_url TEXT,
            success INTEGER NOT NULL,            -- 0/1
            error_message TEXT,
            published_at TEXT NOT NULL,
            FOREIGN KEY(product_id) REFERENCES products(id),
            FOREIGN KEY(content_id) REFERENCES ai_content(id)
        );

        CREATE TABLE IF NOT EXISTS sales_events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id INTEGER NOT NULL,
            post_id INTEGER,                     -- referrer social post
            sale_amount REAL NOT NULL,
            commission_earned REAL NOT NULL,
            currency TEXT DEFAULT 'TRY',
            buyer_info TEXT,                     -- isteğe bağlı (anonim)
            sold_at TEXT NOT NULL,
            FOREIGN KEY(product_id) REFERENCES products(id),
            FOREIGN KEY(post_id) REFERENCES social_posts(id)
        );

        CREATE INDEX IF NOT EXISTS idx_products_status ON products(status);
        CREATE INDEX IF NOT EXISTS idx_products_captured ON products(captured_at);
        CREATE INDEX IF NOT EXISTS idx_sales_sold_at ON sales_events(sold_at);
        """)
        conn.commit()
    logger.info(f"📊 Tracking DB hazır: {DB_PATH}")


@contextmanager
def get_conn():
    """Bağlantı context manager (otomatik commit/close)"""
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()


# ============================================
# Ürün Kaydı
# ============================================

def record_product(product_data: Dict) -> Optional[int]:
    """Yeni ürün kaydet, ID döndür. Aynı ürün varsa mevcut ID'yi döndür."""
    try:
        with get_conn() as conn:
            c = conn.cursor()
            # Önce var mı kontrol et
            c.execute("""
                SELECT id FROM products
                WHERE source=? AND source_message_id=? AND title=?
            """, (
                product_data.get('source', ''),
                str(product_data.get('message_id', '')),
                product_data.get('title', '')
            ))
            row = c.fetchone()
            if row:
                return row['id']

            # Fiyatı numeric'e çevir
            price = product_data.get('price', '')
            try:
                price_num = float(''.join(ch for ch in str(price) if ch.isdigit() or ch == '.'))
            except (ValueError, TypeError):
                price_num = 0.0

            c.execute("""
                INSERT INTO products (source, source_message_id, title, description, price,
                                      commission_rate, product_url, image_urls, raw_message,
                                      captured_at, status)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'captured')
            """, (
                product_data.get('source', ''),
                str(product_data.get('message_id', '')),
                product_data.get('title', '')[:500],
                product_data.get('description', ''),
                price_num,
                float(product_data.get('commission_rate', 0)),
                (product_data.get('links') or [None])[0] if isinstance(product_data.get('links'), list) else product_data.get('url', ''),
                json.dumps(product_data.get('media_urls', []), ensure_ascii=False),
                product_data.get('raw_text', ''),
                product_data.get('captured_at', datetime.now().isoformat())
            ))
            return c.lastrowid
    except Exception as e:
        logger.error(f"Ürün kayıt hatası: {e}")
        return None


def record_ai_content(product_id: int, content: Dict, model: str = "mock") -> Optional[int]:
    """AI tarafından üretilen içeriği kaydet"""
    try:
        with get_conn() as conn:
            c = conn.cursor()
            c.execute("""
                INSERT INTO ai_content (product_id, content_text, hashtags, ai_model,
                                        ai_confidence, created_at)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                product_id,
                content.get('content', ''),
                json.dumps(content.get('hashtags', []), ensure_ascii=False),
                model,
                float(content.get('ai_confidence', 0)),
                datetime.now().isoformat()
            ))
            # Ürün durumunu güncelle
            c.execute("UPDATE products SET status='processed' WHERE id=?", (product_id,))
            return c.lastrowid
    except Exception as e:
        logger.error(f"AI içerik kayıt hatası: {e}")
        return None


def record_social_post(product_id: int, content_id: Optional[int], platform: str, result: Dict) -> Optional[int]:
    """Sosyal medya paylaşımını kaydet"""
    try:
        with get_conn() as conn:
            c = conn.cursor()
            c.execute("""
                INSERT INTO social_posts (product_id, content_id, platform, post_id, post_url,
                                          success, error_message, published_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                product_id,
                content_id,
                platform,
                result.get('post_id', ''),
                result.get('url', ''),
                1 if result.get('success') else 0,
                result.get('error', '') or result.get('message', '') if not result.get('success') else None,
                datetime.now().isoformat()
            ))
            if result.get('success'):
                c.execute("UPDATE products SET status='published' WHERE id=?", (product_id,))
            return c.lastrowid
    except Exception as e:
        logger.error(f"Sosyal medya kayıt hatası: {e}")
        return None


def record_sale(product_id: int, sale_amount: float, commission: float,
                post_id: Optional[int] = None, buyer_info: str = "") -> Optional[int]:
    """Satış olayını kaydet"""
    try:
        with get_conn() as conn:
            c = conn.cursor()
            c.execute("""
                INSERT INTO sales_events (product_id, post_id, sale_amount, commission_earned,
                                          buyer_info, sold_at)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (product_id, post_id, sale_amount, commission, buyer_info,
                  datetime.now().isoformat()))
            c.execute("UPDATE products SET status='sold' WHERE id=?", (product_id,))
            return c.lastrowid
    except Exception as e:
        logger.error(f"Satış kayıt hatası: {e}")
        return None


# ============================================
# Raporlama
# ============================================

def get_full_chain(product_id: int) -> Dict:
    """Bir ürünün tam zinciri: ürün → AI içerik → paylaşımlar → satışlar"""
    with get_conn() as conn:
        c = conn.cursor()
        product = c.execute("SELECT * FROM products WHERE id=?", (product_id,)).fetchone()
        if not product:
            return {}
        contents = c.execute("SELECT * FROM ai_content WHERE product_id=?", (product_id,)).fetchall()
        posts = c.execute("SELECT * FROM social_posts WHERE product_id=?", (product_id,)).fetchall()
        sales = c.execute("SELECT * FROM sales_events WHERE product_id=?", (product_id,)).fetchall()

        return {
            'product': dict(product),
            'ai_contents': [dict(r) for r in contents],
            'social_posts': [dict(r) for r in posts],
            'sales': [dict(r) for r in sales],
            'total_revenue': sum(s['commission_earned'] for s in sales)
        }


def get_summary(days: int = 7) -> Dict:
    """Son N gün için özet"""
    with get_conn() as conn:
        c = conn.cursor()
        cutoff = datetime.now().isoformat()[:10]

        total_products = c.execute("SELECT COUNT(*) c FROM products").fetchone()['c']
        published = c.execute("SELECT COUNT(*) c FROM products WHERE status IN ('published','sold')").fetchone()['c']
        sold = c.execute("SELECT COUNT(*) c FROM products WHERE status='sold'").fetchone()['c']
        total_revenue = c.execute("SELECT COALESCE(SUM(commission_earned),0) r FROM sales_events").fetchone()['r']

        # Platform bazında başarı
        platform_stats = c.execute("""
            SELECT platform,
                   SUM(CASE WHEN success=1 THEN 1 ELSE 0 END) ok,
                   COUNT(*) total
            FROM social_posts GROUP BY platform
        """).fetchall()

        # En çok kazandıran ürünler
        top_products = c.execute("""
            SELECT p.id, p.title, p.commission_rate,
                   COALESCE(SUM(s.commission_earned),0) revenue,
                   COUNT(s.id) sales_count
            FROM products p
            LEFT JOIN sales_events s ON s.product_id = p.id
            GROUP BY p.id
            ORDER BY revenue DESC
            LIMIT 5
        """).fetchall()

        return {
            'as_of': cutoff,
            'total_products_captured': total_products,
            'total_published': published,
            'total_sold': sold,
            'conversion_rate_pct': round((sold / total_products * 100) if total_products else 0, 2),
            'total_revenue_try': round(total_revenue, 2),
            'platform_stats': [dict(r) for r in platform_stats],
            'top_products': [dict(r) for r in top_products],
        }


def list_recent_products(limit: int = 20) -> List[Dict]:
    """Son ürünleri listele"""
    with get_conn() as conn:
        c = conn.cursor()
        rows = c.execute(
            "SELECT * FROM products ORDER BY captured_at DESC LIMIT ?", (limit,)
        ).fetchall()
        return [dict(r) for r in rows]


# İlk import'ta DB'yi hazırla
init_db()


if __name__ == "__main__":
    # CLI: özet raporu yazdır
    summary = get_summary()
    print("\n" + "=" * 60)
    print("📊 TRM PARA KAZANMA RAPORU")
    print("=" * 60)
    print(f"Toplam Yakalanan Ürün: {summary['total_products_captured']}")
    print(f"Yayınlanan:            {summary['total_published']}")
    print(f"Satılan:               {summary['total_sold']}")
    print(f"Dönüşüm Oranı:         %{summary['conversion_rate_pct']}")
    print(f"Toplam Komisyon:       {summary['total_revenue_try']} TL")
    print("\nPlatform Performansı:")
    for p in summary['platform_stats']:
        print(f"  {p['platform']:12s} → {p['ok']}/{p['total']}")
    print("\nEn Çok Kazandıran Ürünler:")
    for p in summary['top_products']:
        print(f"  [{p['id']}] {p['title'][:40]:40s} → {p['revenue']:.2f} TL ({p['sales_count']} satış)")
    print("=" * 60)
