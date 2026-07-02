#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TRM Tracking Database - Para kazanma kanit zinciri icin SQLite tabanli takip

Akis: Telegram urun → AI icerik → Sosyal paylasim → Satis linki → Komisyon takibi
Tum asamalari kayit altina alir, raporlanabilir hale getirir.
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
    """Veritabanini ve tablolari olustur"""
    DB_PATH.parent.mkdir(exist_ok=True)
    with get_conn() as conn:
        c = conn.cursor()
        c.executescript("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            source TEXT NOT NULL,                -- telegram kanal adi / web url
            source_message_id TEXT,              -- Telegram message_id
            title TEXT NOT NULL,
            description TEXT,
            price REAL,
            currency TEXT DEFAULT 'TRY',
            commission_rate REAL,                -- yuzde olarak (orn 25.0)
            product_url TEXT,                    -- satis/affiliate linki
            image_urls TEXT,                     -- JSON liste
            raw_message TEXT,                    -- orijinal Telegram mesaji
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
            post_id TEXT,                        -- platform tarafindaki post id
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
            buyer_info TEXT,                     -- istege bagli (anonim)
            sold_at TEXT NOT NULL,
            FOREIGN KEY(product_id) REFERENCES products(id),
            FOREIGN KEY(post_id) REFERENCES social_posts(id)
        );

        CREATE INDEX IF NOT EXISTS idx_products_status ON products(status);
        CREATE INDEX IF NOT EXISTS idx_products_captured ON products(captured_at);
        CREATE INDEX IF NOT EXISTS idx_sales_sold_at ON sales_events(sold_at);
        """)
        conn.commit()
    logger.info(f"📊 Tracking DB hazir: {DB_PATH}")


@contextmanager
def get_conn():
    """Baglanti context manager (otomatik commit/close)"""
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()


# ============================================
# Urun Kaydi
# ============================================

def record_product(product_data: Dict) -> Optional[int]:
    """Yeni urun kaydet, ID dondur. Ayni urun varsa mevcut ID'yi dondur."""
    try:
        with get_conn() as conn:
            c = conn.cursor()
            # Once var mi kontrol et
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

            # Fiyati numeric'e cevir
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
        logger.error(f"Urun kayit hatasi: {e}")
        return None


def record_ai_content(product_id: int, content: Dict, model: str = "mock") -> Optional[int]:
    """AI tarafindan uretilen icerigi kaydet"""
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
            # Urun durumunu guncelle
            c.execute("UPDATE products SET status='processed' WHERE id=?", (product_id,))
            return c.lastrowid
    except Exception as e:
        logger.error(f"AI icerik kayit hatasi: {e}")
        return None


def record_social_post(product_id: int, content_id: Optional[int], platform: str, result: Dict) -> Optional[int]:
    """Sosyal medya paylasimini kaydet"""
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
        logger.error(f"Sosyal medya kayit hatasi: {e}")
        return None


def record_sale(product_id: int, sale_amount: float, commission: float,
                post_id: Optional[int] = None, buyer_info: str = "") -> Optional[int]:
    """Satis olayini kaydet"""
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
        logger.error(f"Satis kayit hatasi: {e}")
        return None


# ============================================
# Raporlama
# ============================================

def get_full_chain(product_id: int) -> Dict:
    """Bir urunun tam zinciri: urun → AI icerik → paylasimlar → satislar"""
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
    """Son N gun icin ozet"""
    with get_conn() as conn:
        c = conn.cursor()
        cutoff = datetime.now().isoformat()[:10]

        total_products = c.execute("SELECT COUNT(*) c FROM products").fetchone()['c']
        published = c.execute("SELECT COUNT(*) c FROM products WHERE status IN ('published','sold')").fetchone()['c']
        sold = c.execute("SELECT COUNT(*) c FROM products WHERE status='sold'").fetchone()['c']
        total_revenue = c.execute("SELECT COALESCE(SUM(commission_earned),0) r FROM sales_events").fetchone()['r']

        # Platform bazinda basari
        platform_stats = c.execute("""
            SELECT platform,
                   SUM(CASE WHEN success=1 THEN 1 ELSE 0 END) ok,
                   COUNT(*) total
            FROM social_posts GROUP BY platform
        """).fetchall()

        # En cok kazandiran urunler
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
    """Son urunleri listele"""
    with get_conn() as conn:
        c = conn.cursor()
        rows = c.execute(
            "SELECT * FROM products ORDER BY captured_at DESC LIMIT ?", (limit,)
        ).fetchall()
        return [dict(r) for r in rows]


# Ilk import'ta DB'yi hazirla
init_db()


if __name__ == "__main__":
    # CLI: ozet raporu yazdir
    summary = get_summary()
    print("\n" + "=" * 60)
    print("📊 TRM PARA KAZANMA RAPORU")
    print("=" * 60)
    print(f"Toplam Yakalanan Urun: {summary['total_products_captured']}")
    print(f"Yayinlanan:            {summary['total_published']}")
    print(f"Satilan:               {summary['total_sold']}")
    print(f"Donusum Orani:         %{summary['conversion_rate_pct']}")
    print(f"Toplam Komisyon:       {summary['total_revenue_try']} TL")
    print("\nPlatform Performansi:")
    for p in summary['platform_stats']:
        print(f"  {p['platform']:12s} → {p['ok']}/{p['total']}")
    print("\nEn Cok Kazandiran Urunler:")
    for p in summary['top_products']:
        print(f"  [{p['id']}] {p['title'][:40]:40s} → {p['revenue']:.2f} TL ({p['sales_count']} satis)")
    print("=" * 60)
