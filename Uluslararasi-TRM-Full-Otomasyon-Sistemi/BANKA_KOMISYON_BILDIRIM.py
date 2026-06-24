#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TRM Banka Komisyon Bildirim Sistemi v5.2
Manuel/webhook ile komisyon takibi ve Telegram+Discord bildirimi.
Türk bankaları kamuya açık API sunmadığından sistem:
  - Manuel komisyon kaydı
  - Webhook ile tetikleme
  - Telegram + Discord + Viber bildirimi
şeklinde çalışır.
"""

import asyncio
import json
import logging
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional

logger = logging.getLogger('TRMBanka')

BASE_DIR = Path(__file__).parent.resolve()
DATA_DIR = BASE_DIR / 'data'
DATA_DIR.mkdir(exist_ok=True)
KOMISYON_LOG = DATA_DIR / 'komisyon_log.jsonl'

IBAN          = os.getenv('BANKA_IBAN', '')          # secrets.env
HESAP_SAHIBI  = os.getenv('BANKA_HESAP_SAHIBI', 'TRM Sistemi')
ESIK_TRY      = float(os.getenv('KOMISYON_ESIK_TRY', '50'))  # min bildirim tutarı

MODE = os.getenv('TRM_MODE', 'live')   # 'live' | 'test'


def komisyon_kaydet(tutar: float, kaynak: str = '', not_: str = '') -> Dict:
    """Komisyon kaydı oluştur ve dosyaya yaz."""
    kayit = {
        'tutar': tutar,
        'kaynak': kaynak,
        'not': not_,
        'tarih': datetime.now().isoformat(),
        'durum': 'alindi',
    }
    with open(KOMISYON_LOG, 'a', encoding='utf-8') as f:
        f.write(json.dumps(kayit, ensure_ascii=False) + '\n')
    logger.info(f'Komisyon kaydedildi: {tutar:.2f} TRY | {kaynak}')
    return kayit


async def bildirim_gonder(mesaj: str) -> Dict:
    """Telegram + Discord + Viber'a bildirim gönder."""
    from MESAJLASMA_BILDIRIM import herkese_bildir
    return await herkese_bildir(mesaj)


async def yeni_komisyon(tutar: float, kaynak: str = '',
                         not_: str = '') -> Dict:
    """Yeni komisyon al → kaydet → bildir."""
    kayit = komisyon_kaydet(tutar, kaynak, not_)

    if tutar >= ESIK_TRY:
        mesaj = (
            f"💰 <b>YENİ KOMİSYON</b>\n"
            f"━━━━━━━━━━━━━\n"
            f"💲 Tutar: {tutar:.2f} TRY\n"
            f"📌 Kaynak: {kaynak or 'Belirtilmedi'}\n"
            f"📝 Not: {not_ or '-'}\n"
            f"🕐 {datetime.now().strftime('%d.%m.%Y %H:%M')}"
        )
        if MODE != 'test':
            await bildirim_gonder(mesaj)
        else:
            logger.info(f'[TEST MODU] Bildirim atlandı: {mesaj}')

    return kayit


def komisyon_ozeti(gun: int = 30) -> Dict:
    """Son N günün komisyon özeti."""
    from datetime import timedelta
    kayitlar = []
    if KOMISYON_LOG.exists():
        for satir in KOMISYON_LOG.read_text('utf-8').splitlines():
            try:
                k = json.loads(satir)
                tarih = datetime.fromisoformat(k['tarih'])
                if tarih >= datetime.now() - timedelta(days=gun):
                    kayitlar.append(k)
            except Exception:
                continue

    toplam = sum(k.get('tutar', 0) for k in kayitlar)
    return {
        'gun': gun,
        'adet': len(kayitlar),
        'toplam_try': round(toplam, 2),
        'ortalama_try': round(toplam / len(kayitlar), 2) if kayitlar else 0,
    }


if __name__ == '__main__':
    import sys
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s [%(levelname)s] %(message)s')

    ozet = komisyon_ozeti(30)
    print(f"\n=== Son 30 Günlük Komisyon Özeti ===")
    print(f"  Adet  : {ozet['adet']}")
    print(f"  Toplam: {ozet['toplam_try']:.2f} TRY")
    print(f"  Ort.  : {ozet['ortalama_try']:.2f} TRY")

    if '--test' in sys.argv or '--demo' in sys.argv:
        async def demo():
            print("\n[TEST] Örnek komisyon kaydediliyor...")
            k = await yeni_komisyon(150.0, 'trendyol', 'Test kaydı')
            print(f"  Kaydedildi: {k}")
        asyncio.run(demo())
