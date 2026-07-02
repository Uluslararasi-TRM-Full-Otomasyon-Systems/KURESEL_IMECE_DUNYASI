#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TRM Banka Komisyon Bildirim Sistemi v5.2
Manuel/webhook ile komisyon takibi ve Telegram+Discord bildirimi.
Turk bankalari kamuya acik API sunmadigindan sistem:
  - Manuel komisyon kaydi
  - Webhook ile tetikleme
  - Telegram + Discord + Viber bildirimi
seklinde calisir.
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
ESIK_TRY      = float(os.getenv('KOMISYON_ESIK_TRY', '50'))  # min bildirim tutari

MODE = os.getenv('TRM_MODE', 'live')   # 'live' | 'test'


def komisyon_kaydet(tutar: float, kaynak: str = '', not_: str = '') -> Dict:
    """Komisyon kaydi olustur ve dosyaya yaz."""
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
    """Telegram + Discord + Viber'a bildirim gonder."""
    from MESAJLASMA_BILDIRIM import herkese_bildir
    return await herkese_bildir(mesaj)


async def yeni_komisyon(tutar: float, kaynak: str = '',
                         not_: str = '') -> Dict:
    """Yeni komisyon al → kaydet → bildir."""
    kayit = komisyon_kaydet(tutar, kaynak, not_)

    if tutar >= ESIK_TRY:
        mesaj = (
            f"💰 <b>YENI KOMISYON</b>\n"
            f"━━━━━━━━━━━━━\n"
            f"💲 Tutar: {tutar:.2f} TRY\n"
            f"📌 Kaynak: {kaynak or 'Belirtilmedi'}\n"
            f"📝 Not: {not_ or '-'}\n"
            f"🕐 {datetime.now().strftime('%d.%m.%Y %H:%M')}"
        )
        if MODE != 'test':
            await bildirim_gonder(mesaj)
        else:
            logger.info(f'[TEST MODU] Bildirim atlandi: {mesaj}')

    return kayit


def komisyon_ozeti(gun: int = 30) -> Dict:
    """Son N gunun komisyon ozeti."""
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


class BankCommissionSystem:
    """Banka komisyon bildirim sistemi - MASTER_CONTROLLER icin wrapper"""
    
    def __init__(self):
        self.running = False
        self.iban = IBAN
        self.hesap_sahibi = HESAP_SAHIBI
        self.esik_try = ESIK_TRY
        self.mode = MODE
    
    async def initialize(self):
        """Sistemi baslat"""
        logger.info("Banka komisyon sistemi baslatildi")
        return True
    
    async def run_monitoring(self):
        """Komisyon izleme dongusu"""
        self.running = True
        while self.running:
            await asyncio.sleep(60)
    
    def get_system_status(self):
        """Sistem durumu"""
        return {
            'running': self.running,
            'iban': self.iban,
            'hesap_sahibi': self.hesap_sahibi,
            'esik_try': self.esik_try,
            'mode': self.mode
        }
    
    async def yeni_komisyon_wrapper(self, tutar: float, kaynak: str = '', not_: str = '') -> Dict:
        """Yeni komisyon wrapper"""
        return await yeni_komisyon(tutar, kaynak, not_)
    
    def komisyon_ozeti_wrapper(self, gun: int = 30) -> Dict:
        """Komisyon ozeti wrapper"""
        return komisyon_ozeti(gun)


if __name__ == '__main__':
    import sys
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s [%(levelname)s] %(message)s')

    ozet = komisyon_ozeti(30)
    print(f"\n=== Son 30 Gunluk Komisyon Ozeti ===")
    print(f"  Adet  : {ozet['adet']}")
    print(f"  Toplam: {ozet['toplam_try']:.2f} TRY")
    print(f"  Ort.  : {ozet['ortalama_try']:.2f} TRY")

    if '--test' in sys.argv or '--demo' in sys.argv:
        async def demo():
            print("\n[TEST] Ornek komisyon kaydediliyor...")
            k = await yeni_komisyon(150.0, 'trendyol', 'Test kaydi')
            print(f"  Kaydedildi: {k}")
        asyncio.run(demo())
