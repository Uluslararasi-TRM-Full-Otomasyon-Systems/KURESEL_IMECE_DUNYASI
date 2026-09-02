#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TRM Sales Dashboard v5.0 - Madde 7+11: Tıklama takibi, komisyon kayıt,
gerçek kazanç dashboard, performans analizi.
"""

import json
import logging
import os
import sqlite3
from contextlib import contextmanager
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Tuple

logger = logging.getLogger('TRMDashboard')

BASE_DIR = Path(__file__).parent.resolve()
DATA_DIR = BASE_DIR / 'data'
DATA_DIR.mkdir(exist_ok=True)
DB_PATH  = DATA_DIR / 'trm_tracking.db'

@contextmanager
def get_db():
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

def init_db():
    with get_db() as conn:
        conn.executescript("""
        CREATE TABLE IF NOT EXISTS clicks (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id  TEXT,
            platform    TEXT,
            affiliate_link TEXT,
            clicked_at  TEXT DEFAULT (datetime('now','localtime')),
            ip_hash     TEXT,
            converted   INTEGER DEFAULT 0
        );
        CREATE TABLE IF NOT EXISTS commissions (
            id              INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id      TEXT,
            platform        TEXT,
            sale_amount     REAL,
            commission_rate REAL,
            commission_earn REAL,
            currency        TEXT DEFAULT 'TRY',
            status          TEXT DEFAULT 'pending',
            recorded_at     TEXT DEFAULT (datetime('now','localtime')),
            paid_at         TEXT,
            note            TEXT
        );
        CREATE TABLE IF NOT EXISTS daily_stats (
            date        TEXT PRIMARY KEY,
            clicks      INTEGER DEFAULT 0,
            conversions INTEGER DEFAULT 0,
            revenue     REAL DEFAULT 0,
            commission  REAL DEFAULT 0,
            posts       INTEGER DEFAULT 0,
            platforms   TEXT
        );
        CREATE INDEX IF NOT EXISTS idx_clicks_date     ON clicks(clicked_at);
        CREATE INDEX IF NOT EXISTS idx_comm_date       ON commissions(recorded_at);
        CREATE INDEX IF NOT EXISTS idx_comm_status     ON commissions(status);
        """)

def record_click(product_id: str, platform: str, affiliate_link: str = '') -> int:
    with get_db() as conn:
        c = conn.execute(
            "INSERT INTO clicks (product_id, platform, affiliate_link) VALUES (?,?,?)",
            (product_id, platform, affiliate_link)
        )
        return c.lastrowid

def record_commission(product_id: str, platform: str, sale_amount: float,
                      commission_rate: float, status: str = 'pending',
                      note: str = '') -> int:
    earn = round(sale_amount * commission_rate / 100, 2)
    with get_db() as conn:
        c = conn.execute(
            """INSERT INTO commissions
               (product_id, platform, sale_amount, commission_rate, commission_earn, status, note)
               VALUES (?,?,?,?,?,?,?)""",
            (product_id, platform, sale_amount, commission_rate, earn, status, note)
        )
        return c.lastrowid

def update_commission_status(comm_id: int, status: str):
    paid_at = datetime.now().isoformat() if status == 'paid' else None
    with get_db() as conn:
        conn.execute(
            "UPDATE commissions SET status=?, paid_at=? WHERE id=?",
            (status, paid_at, comm_id)
        )

def record_post(platform: str, product_id: str = ''):
    today = datetime.now().strftime('%Y-%m-%d')
    with get_db() as conn:
        conn.execute(
            """INSERT INTO daily_stats (date, posts, platforms) VALUES (?,1,?)
               ON CONFLICT(date) DO UPDATE SET
               posts = posts + 1,
               platforms = CASE
                 WHEN platforms IS NULL THEN excluded.platforms
                 WHEN instr(platforms, excluded.platforms) > 0 THEN platforms
                 ELSE platforms || ',' || excluded.platforms
               END""",
            (today, platform)
        )

def get_summary(days: int = 30) -> Dict:
    since = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')
    with get_db() as conn:
        clicks = conn.execute(
            "SELECT COUNT(*) FROM clicks WHERE clicked_at >= ?", (since,)
        ).fetchone()[0]
        conversions = conn.execute(
            "SELECT COUNT(*) FROM clicks WHERE clicked_at >= ? AND converted=1", (since,)
        ).fetchone()[0]
        revenue = conn.execute(
            "SELECT COALESCE(SUM(sale_amount),0) FROM commissions WHERE recorded_at >= ?", (since,)
        ).fetchone()[0]
        earned = conn.execute(
            "SELECT COALESCE(SUM(commission_earn),0) FROM commissions WHERE recorded_at >= ?", (since,)
        ).fetchone()[0]
        pending = conn.execute(
            "SELECT COALESCE(SUM(commission_earn),0) FROM commissions WHERE status='pending'"
        ).fetchone()[0]
        paid = conn.execute(
            "SELECT COALESCE(SUM(commission_earn),0) FROM commissions WHERE status='paid'"
        ).fetchone()[0]
        posts = conn.execute(
            "SELECT COALESCE(SUM(posts),0) FROM daily_stats WHERE date >= ?", (since,)
        ).fetchone()[0]

    cr = round(conversions / clicks * 100, 1) if clicks > 0 else 0
    return {
        'period_days': days,
        'clicks':      clicks,
        'conversions': conversions,
        'conversion_rate': f'{cr}%',
        'total_revenue': round(revenue, 2),
        'total_earned':  round(earned, 2),
        'pending_earn':  round(pending, 2),
        'paid_earn':     round(paid, 2),
        'posts':         posts,
        'avg_daily_posts': round(posts / max(days,1), 1),
    }

def get_platform_breakdown(days: int = 30) -> List[Dict]:
    since = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')
    with get_db() as conn:
        rows = conn.execute(
            """SELECT platform,
                      COUNT(*) as cnt,
                      COALESCE(SUM(commission_earn),0) as earned
               FROM commissions WHERE recorded_at >= ?
               GROUP BY platform ORDER BY earned DESC""",
            (since,)
        ).fetchall()
    return [dict(r) for r in rows]

def print_dashboard(days: int = 30):
    init_db()
    s = get_summary(days)
    now = datetime.now().strftime('%d.%m.%Y %H:%M')
    print(f"""
╔══════════════════════════════════════════════════════╗
║    TRM SATIŞ DASHBOARD — {now}
╠══════════════════════════════════════════════════════╣
║  DÖNEM: Son {s['period_days']} gün
╠══════════════════════════════════════════════════════╣
║  TRAFIK
║   Toplam Tıklama    : {s['clicks']:>10,}
║   Dönüşüm           : {s['conversions']:>10,}  ({s['conversion_rate']})
╠══════════════════════════════════════════════════════╣
║  KOMİSYON GELİRİ
║   Toplam Satış Hac. : {s['total_revenue']:>10,.2f} TRY
║   Toplam Kazanç     : {s['total_earned']:>10,.2f} TRY
║   Bekleyen          : {s['pending_earn']:>10,.2f} TRY
║   Ödenen            : {s['paid_earn']:>10,.2f} TRY
╠══════════════════════════════════════════════════════╣
║  PAYLAŞIM
║   Toplam Post       : {s['posts']:>10,}
║   Günlük Ort.       : {s['avg_daily_posts']:>10}
╚══════════════════════════════════════════════════════╝""")

    breakdown = get_platform_breakdown(days)
    if breakdown:
        print('\n  Platform Bazlı Kazanç:')
        for row in breakdown:
            print(f"    {row['platform']:12s}  {row['cnt']:4d} satış  {row['earned']:8.2f} TRY")


if __name__ == '__main__':
    init_db()
    print_dashboard(30)

    # Demo veri ekle (test için)
    import sys
    if '--demo' in sys.argv:
        for i in range(5):
            record_click(f'PROD_{i}', ['instagram','facebook','telegram'][i%3], 'https://ty.gl/DEMO')
            record_commission(f'PROD_{i}', ['instagram','facebook','telegram'][i%3],
                              float((i+1)*200), 25.0, 'pending')
        print('\nDemo veri eklendi. Tekrar çalıştırın.')
