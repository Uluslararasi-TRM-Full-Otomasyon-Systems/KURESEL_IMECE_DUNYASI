#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TRM Email Automation v5.0
Otomatik urun tanitim e-postalari, liste yonetimi, kampanya takibi.
secrets.env: EMAIL_ADDRESS, EMAIL_PASSWORD, SMTP_HOST, SMTP_PORT
"""

import asyncio
import csv
import json
import logging
import os
import smtplib
import time
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path
from typing import Dict, List, Optional

logger = logging.getLogger('TRMEmail')

BASE_DIR  = Path(__file__).parent.resolve()
DATA_DIR  = BASE_DIR / 'data'
DATA_DIR.mkdir(exist_ok=True)

SUBSCRIBER_FILE = DATA_DIR / 'email_subscribers.json'
CAMPAIGN_LOG    = DATA_DIR / 'email_campaigns.jsonl'

SHOP_LINK = os.getenv('TRENDYOL_AFFILIATE_LINK', 'https://trendurunlermarket.com')


# ── Abone Yoneticisi ──────────────────────────────────────────────────────

class SubscriberManager:
    def __init__(self):
        self._subs: List[Dict] = []
        self._load()

    def _load(self):
        if SUBSCRIBER_FILE.exists():
            try:
                self._subs = json.loads(SUBSCRIBER_FILE.read_text('utf-8'))
            except Exception:
                self._subs = []

    def _save(self):
        SUBSCRIBER_FILE.write_text(
            json.dumps(self._subs, ensure_ascii=False, indent=2), 'utf-8')

    def add(self, email: str, name: str = '') -> bool:
        email = email.strip().lower()
        if any(s['email'] == email for s in self._subs):
            return False
        self._subs.append({'email': email, 'name': name,
                           'added_at': datetime.now().isoformat(), 'active': True})
        self._save()
        return True

    def import_csv(self, csv_path: str) -> int:
        count = 0
        with open(csv_path, newline='', encoding='utf-8') as f:
            for row in csv.DictReader(f):
                email = row.get('email', row.get('Email', ''))
                name  = row.get('name', row.get('Name', ''))
                if email and self.add(email, name):
                    count += 1
        return count

    def active_list(self) -> List[Dict]:
        return [s for s in self._subs if s.get('active', True)]

    def count(self) -> int:
        return len(self.active_list())


# ── E-posta Sablonlari ───────────────────────────────────────────────────

def product_email_html(product: Dict, subscriber_name: str = '') -> str:
    title      = product.get('title', 'Ozel Firsat')
    price      = product.get('price', '')
    commission = product.get('commission_rate', 0)
    link       = product.get('product_url', product.get('url', SHOP_LINK))
    image_url  = product.get('image_url', '')
    greeting   = f"Merhaba {subscriber_name}," if subscriber_name else "Merhaba,"

    img_html = f'<img src="{image_url}" alt="{title}" style="max-width:500px;border-radius:8px;">' \
               if image_url else ''

    return f"""
<!DOCTYPE html>
<html>
<head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title></head>
<body style="font-family:Arial,sans-serif;background:#f5f5f5;margin:0;padding:20px;">
  <div style="max-width:600px;margin:0 auto;background:#fff;border-radius:12px;overflow:hidden;box-shadow:0 2px 8px rgba(0,0,0,.1)">
    <div style="background:#E63946;padding:20px;text-align:center;">
      <h1 style="color:#fff;margin:0;font-size:22px;">🛍️ trendurunlermarket.com</h1>
      <p style="color:#fff;margin:5px 0;font-size:14px;">Ozel Firsat Bildirimi</p>
    </div>
    <div style="padding:30px;">
      <p style="font-size:16px;color:#333;">{greeting}</p>
      <h2 style="color:#E63946;">{title}</h2>
      {img_html}
      <div style="background:#fff3f3;border-left:4px solid #E63946;padding:15px;margin:20px 0;border-radius:4px;">
        <p style="margin:0;font-size:18px;font-weight:bold;color:#333;">💰 Fiyat: {price}</p>
        {'<p style="margin:5px 0;color:#666;">Komisyon: %' + str(commission) + '</p>' if commission else ''}
      </div>
      <div style="text-align:center;margin:30px 0;">
        <a href="{link}" style="background:#E63946;color:#fff;padding:14px 32px;text-decoration:none;border-radius:8px;font-size:16px;font-weight:bold;display:inline-block;">
          🛒 Hemen Incele
        </a>
      </div>
      <hr style="border:none;border-top:1px solid #eee;margin:20px 0;">
      <p style="font-size:12px;color:#999;text-align:center;">
        trendurunlermarket.com • Bu e-postayi almak istemiyorsaniz <a href="#">abonelikten cikin</a>
      </p>
    </div>
  </div>
</body>
</html>"""


# ── SMTP Gonderici ──────────────────────────────────────────────────────

class EmailSender:
    def __init__(self):
        self.host     = os.getenv('SMTP_HOST', 'smtp.gmail.com')
        self.port     = int(os.getenv('SMTP_PORT', '587'))
        self.address  = os.getenv('EMAIL_ADDRESS', '')
        self.password = os.getenv('EMAIL_PASSWORD', '')
        self.ready    = bool(self.address and self.password)

    def send(self, to: str, subject: str, html_body: str) -> bool:
        if not self.ready:
            logger.warning('E-posta kimlik bilgileri eksik (secrets.env: EMAIL_ADDRESS, EMAIL_PASSWORD)')
            return False
        try:
            msg = MIMEMultipart('alternative')
            msg['From']    = f'trendurunlermarket.com <{self.address}>'
            msg['To']      = to
            msg['Subject'] = subject
            msg.attach(MIMEText(html_body, 'html', 'utf-8'))
            with smtplib.SMTP(self.host, self.port) as s:
                s.ehlo(); s.starttls(); s.login(self.address, self.password)
                s.sendmail(self.address, to, msg.as_string())
            return True
        except smtplib.SMTPAuthenticationError:
            logger.error('Gmail sifre hatasi — Uygulama Sifresi kullanin (Google 2FA gerektiriyor)')
            return False
        except Exception as e:
            logger.error(f'E-posta gonderilemedi: {e}')
            return False

    def send_bulk(self, subscribers: List[Dict], subject: str,
                   product: Dict, delay_sec: float = 1.0) -> Dict:
        sent = failed = 0
        for sub in subscribers:
            html = product_email_html(product, sub.get('name',''))
            if self.send(sub['email'], subject, html):
                sent += 1
            else:
                failed += 1
            if delay_sec > 0:
                time.sleep(delay_sec)  # Spam limiti asmamak icin

        result = {'sent': sent, 'failed': failed,
                  'total': len(subscribers), 'at': datetime.now().isoformat()}
        with open(CAMPAIGN_LOG, 'a', encoding='utf-8') as f:
            f.write(json.dumps({**result, 'subject': subject}, ensure_ascii=False) + '\n')
        logger.info(f'E-posta kampanyasi: {sent} basarili / {failed} basarisiz')
        return result


# ── Ana Kampanya Yoneticisi ──────────────────────────────────────────────

class EmailCampaignManager:
    def __init__(self):
        self.subscribers = SubscriberManager()
        self.sender      = EmailSender()

    async def send_product_campaign(self, product: Dict) -> Dict:
        subs = self.subscribers.active_list()
        if not subs:
            logger.warning('Abone listesi bos — data/email_subscribers.json dosyasina ekleyin')
            return {'sent': 0, 'failed': 0, 'total': 0}
        subject = f"🔥 Yeni Firsat: {product.get('title','Ozel Urun')[:50]}"
        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(
            None, lambda: self.sender.send_bulk(subs, subject, product)
        )
        return result

    def status(self) -> Dict:
        return {
            'smtp_ready':   self.sender.ready,
            'subscribers':  self.subscribers.count(),
            'smtp_host':    self.sender.host,
            'from_address': self.sender.address or '(secrets.env doldurun)',
        }


email_manager = EmailCampaignManager()

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s [%(levelname)s] %(message)s')
    st = email_manager.status()
    print('\n=== E-posta Sistemi Durumu ===')
    for k, v in st.items():
        print(f"  {k:18s}: {v}")
    # Test gonderimi
    import sys
    if '--test' in sys.argv:
        test_product = {'title':'Test Urun','price':'299 TL',
                        'commission_rate':25,'product_url':SHOP_LINK}
        email_manager.subscribers.add('test@example.com','Test Kullanici')
        asyncio.run(email_manager.send_product_campaign(test_product))
