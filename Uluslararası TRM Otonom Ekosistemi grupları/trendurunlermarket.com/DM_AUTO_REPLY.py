#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TRM DM Auto Reply v5.2
Telegram Bot, Discord, Viber ve Email üzerinden gelen
mesajlara otomatik akıllı yanıt sistemi.
(Telegram/Discord/Viber Business API yerine daha kolay ve ücretsiz alternatifler)

Kurulum kolaylığı sıralaması:
  1. Telegram Bot   → 5 dakika, tamamen ücretsiz
  2. Discord        → 10 dakika, tamamen ücretsiz
  3. Viber Bot      → 15 dakika, tamamen ücretsiz
  4. Email          → 15 dakika (Gmail Uygulama Şifresi)
"""

import asyncio
import json
import logging
import os
import smtplib
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path
from typing import Dict, List, Optional

logger = logging.getLogger('TRMAutoReply')

BASE_DIR = Path(__file__).parent.resolve()
DATA_DIR = BASE_DIR / 'data'
DATA_DIR.mkdir(exist_ok=True)

SHOP_LINK = os.getenv('TRENDYOL_AFFILIATE_LINK', 'https://trendurunlermarket.com')

# ── Anahtar kelime → yanıt şablonları ─────────────────────────────────

KEYWORD_MAP = {
    'fiyat':     ['fiyat','kaç lira','kaç tl','ne kadar','ücret'],
    'kargo':     ['kargo','teslimat','gönderim','kaç günde','ne zaman gelir'],
    'iade':      ['iade','geri','iptal','değişim'],
    'siparis':   ['sipariş','satın al','nasıl alırım','nereden'],
    'tesekkur':  ['teşekkür','teşekkürler','sağol','memnun'],
    'urun_soru': ['ürün','özellik','renk','beden','malzeme','nasıl','nedir'],
}

REPLY_TEMPLATES = {
    'fiyat':     "Merhaba! 💰 Güncel fiyat bilgisi için: {link} — Şu an çok uygun fiyatlar var!",
    'kargo':     "Merhaba! 📦 Kargo ücretsiz! Siparişler 1-3 iş günü içinde kargoya verilir.",
    'iade':      "Merhaba! 🔄 14 gün içinde koşulsuz iade garantimiz var. Detaylar: {link}",
    'siparis':   "Merhaba! 🛒 Sipariş için: {link} — Güvenli ödeme, hızlı teslimat!",
    'tesekkur':  "Rica ederiz! 🙏 Alışverişinizden memnun kalmayı umuyoruz. İyi günler!",
    'urun_soru': "Merhaba! ✨ Ürün detayları için: {link} — Başka sorunuz var mı?",
    'genel':     "Merhaba! 👋 trendurunlermarket.com olarak yardımcı olmaktan mutluluk duyarız. Daha fazlası için: {link}",
}

def classify_message(text: str) -> str:
    t = text.lower()
    for cat, keywords in KEYWORD_MAP.items():
        if any(kw in t for kw in keywords):
            return cat
    return 'genel'

def build_reply(text: str) -> str:
    cat = classify_message(text)
    return REPLY_TEMPLATES[cat].format(link=SHOP_LINK)

def _log_reply(platform: str, user_id: str, incoming: str, outgoing: str):
    entry = {
        'platform': platform, 'user_id': user_id,
        'incoming': incoming[:200], 'outgoing': outgoing[:200],
        'at': datetime.now().isoformat(),
    }
    with open(DATA_DIR / 'dm_replies.jsonl', 'a', encoding='utf-8') as f:
        f.write(json.dumps(entry, ensure_ascii=False) + '\n')


# ══════════════════════════════════════════════════════════════════════
# 1) TELEGRAM BOT — En kolay kurulum (5 dakika, ücretsiz)
# Kurulum: t.me/BotFather → /newbot → token al → secrets.env'e yaz
# ══════════════════════════════════════════════════════════════════════

class TelegramDMHandler:
    """
    Telegram bot üzerinden gelen DM'lere otomatik yanıt.
    secrets.env: TELEGRAM_BOT_TOKEN
    Kurulum: https://t.me/BotFather → /newbot → 5 dakika
    """
    def __init__(self):
        self.token  = os.getenv('TELEGRAM_BOT_TOKEN', '')
        self._base  = f'https://api.telegram.org/bot{self.token}'
        self._offset = 0

    @property
    def ready(self) -> bool:
        return bool(self.token)

    async def get_updates(self) -> List[Dict]:
        if not self.ready:
            return []
        try:
            import aiohttp
            async with aiohttp.ClientSession() as sess:
                async with sess.get(
                    f'{self._base}/getUpdates',
                    params={'offset': self._offset, 'timeout': 20},
                    timeout=aiohttp.ClientTimeout(total=25),
                ) as r:
                    if r.status == 200:
                        updates = (await r.json()).get('result', [])
                        if updates:
                            self._offset = updates[-1]['update_id'] + 1
                        return updates
        except Exception as e:
            logger.debug(f'Telegram getUpdates: {e}')
        return []

    async def send_message(self, chat_id: int, text: str) -> bool:
        if not self.ready:
            return False
        try:
            import aiohttp
            async with aiohttp.ClientSession() as sess:
                async with sess.post(
                    f'{self._base}/sendMessage',
                    json={'chat_id': chat_id, 'text': text},
                    timeout=aiohttp.ClientTimeout(total=10),
                ) as r:
                    return r.status == 200
        except Exception as e:
            logger.error(f'Telegram send hatası: {e}')
            return False

    async def handle_updates(self):
        for upd in await self.get_updates():
            msg     = upd.get('message', {})
            text    = msg.get('text', '').strip()
            chat_id = msg.get('chat', {}).get('id')
            if text and chat_id:
                reply = build_reply(text)
                if await self.send_message(chat_id, reply):
                    _log_reply('telegram', str(chat_id), text, reply)
                    logger.info(f'Telegram yanıt → chat_id={chat_id}')

    # Kanal/grup yayın mesajı gönder (bildirim için)
    async def broadcast(self, channel_id: str, text: str) -> bool:
        return await self.send_message(int(channel_id), text)


# ══════════════════════════════════════════════════════════════════════
# 2) DISCORD BOT — Türkiye'de çok yaygın, ücretsiz, kolay
# Kurulum: discord.com/developers → New Application → Bot → Token al
#          Sunucuya davet: OAuth2 → bot → mesajları oku/yaz izni
# secrets.env: DISCORD_BOT_TOKEN, DISCORD_CHANNEL_ID
# ══════════════════════════════════════════════════════════════════════

class DiscordDMHandler:
    """
    Discord bot üzerinden gelen DM ve kanal mesajlarına yanıt.
    secrets.env: DISCORD_BOT_TOKEN, DISCORD_CHANNEL_ID
    Kurulum: https://discord.com/developers/applications → 10 dakika
    """
    def __init__(self):
        self.token      = os.getenv('DISCORD_BOT_TOKEN', '')
        self.channel_id = os.getenv('DISCORD_CHANNEL_ID', '')
        self._api       = 'https://discord.com/api/v10'
        self._headers   = {
            'Authorization': f'Bot {self.token}',
            'Content-Type':  'application/json',
        }
        self._last_msg_id: Optional[str] = None

    @property
    def ready(self) -> bool:
        return bool(self.token and self.channel_id)

    async def get_new_messages(self) -> List[Dict]:
        if not self.ready:
            return []
        try:
            import aiohttp
            url    = f'{self._api}/channels/{self.channel_id}/messages'
            params = {'limit': 10}
            if self._last_msg_id:
                params['after'] = self._last_msg_id
            async with aiohttp.ClientSession() as sess:
                async with sess.get(
                    url, params=params, headers=self._headers,
                    timeout=aiohttp.ClientTimeout(total=10),
                ) as r:
                    if r.status == 200:
                        msgs = await r.json()
                        if msgs:
                            self._last_msg_id = msgs[0]['id']
                        return [m for m in msgs if not m.get('author', {}).get('bot', False)]
        except Exception as e:
            logger.debug(f'Discord getMessages: {e}')
        return []

    async def send_message(self, channel_id: str, text: str) -> bool:
        if not self.token:
            return False
        try:
            import aiohttp
            url = f'{self._api}/channels/{channel_id}/messages'
            async with aiohttp.ClientSession() as sess:
                async with sess.post(
                    url,
                    json={'content': text[:2000]},
                    headers=self._headers,
                    timeout=aiohttp.ClientTimeout(total=10),
                ) as r:
                    return r.status == 200
        except Exception as e:
            logger.error(f'Discord send hatası: {e}')
            return False

    # Webhook ile kolayca bildirim gönder (bot gerekmez)
    async def send_webhook(self, text: str) -> bool:
        """Discord Webhook — Bot bile gerekmez, sadece URL lazım."""
        webhook_url = os.getenv('DISCORD_WEBHOOK_URL', '')
        if not webhook_url:
            return False
        try:
            import aiohttp
            async with aiohttp.ClientSession() as sess:
                async with sess.post(
                    webhook_url,
                    json={'content': text[:2000], 'username': 'TRM Otomasyon'},
                    timeout=aiohttp.ClientTimeout(total=10),
                ) as r:
                    return r.status in (200, 204)
        except Exception as e:
            logger.error(f'Discord webhook hatası: {e}')
            return False

    async def handle_updates(self):
        for msg in await self.get_new_messages():
            text       = msg.get('content', '').strip()
            channel_id = msg.get('channel_id', self.channel_id)
            author     = msg.get('author', {}).get('username', '?')
            if text:
                reply = build_reply(text)
                if await self.send_message(channel_id, reply):
                    _log_reply('discord', author, text, reply)
                    logger.info(f'Discord yanıt → {author}')


# ══════════════════════════════════════════════════════════════════════
# 3) VIBER BOT — Türkiye'de yaygın, ücretsiz, webhook tabanlı
# Kurulum: partners.viber.com → Create Bot Account → Token al
# secrets.env: VIBER_BOT_TOKEN, VIBER_WEBHOOK_URL (sunucu URL'niz)
# ══════════════════════════════════════════════════════════════════════

class ViberDMHandler:
    """
    Viber Bot üzerinden gelen mesajlara otomatik yanıt.
    secrets.env: VIBER_BOT_TOKEN
    Kurulum: https://partners.viber.com → Create Bot → 15 dakika
    NOT: Webhook için Railway/Render üzerinde çalışması gerekir.
    """
    def __init__(self):
        self.token   = os.getenv('VIBER_BOT_TOKEN', '')
        self._api    = 'https://chatapi.viber.com/pa'
        self._headers = {
            'X-Viber-Auth-Token': self.token,
            'Content-Type': 'application/json',
        }

    @property
    def ready(self) -> bool:
        return bool(self.token)

    async def set_webhook(self, webhook_url: str) -> bool:
        """Webhook URL'yi Viber'a kaydet (ilk kurulumda bir kez çalıştır)."""
        if not self.ready:
            return False
        try:
            import aiohttp
            async with aiohttp.ClientSession() as sess:
                async with sess.post(
                    f'{self._api}/set_webhook',
                    json={'url': webhook_url, 'event_types': ['message']},
                    headers=self._headers,
                    timeout=aiohttp.ClientTimeout(total=10),
                ) as r:
                    data = await r.json()
                    ok = data.get('status') == 0
                    if ok:
                        logger.info(f'Viber webhook kuruldu: {webhook_url}')
                    return ok
        except Exception as e:
            logger.error(f'Viber webhook hatası: {e}')
            return False

    async def send_message(self, receiver: str, text: str) -> bool:
        if not self.ready:
            return False
        try:
            import aiohttp
            payload = {
                'receiver': receiver,
                'type':     'text',
                'text':     text[:7000],
                'sender':   {'name': 'TRM Otomasyon', 'avatar': ''},
            }
            async with aiohttp.ClientSession() as sess:
                async with sess.post(
                    f'{self._api}/send_message',
                    json=payload, headers=self._headers,
                    timeout=aiohttp.ClientTimeout(total=10),
                ) as r:
                    data = await r.json()
                    return data.get('status') == 0
        except Exception as e:
            logger.error(f'Viber send hatası: {e}')
            return False

    def process_webhook_event(self, event: Dict) -> Optional[Dict]:
        """Viber webhook POST verisi işle."""
        if event.get('event') != 'message':
            return None
        sender = event.get('sender', {}).get('id', '')
        text   = event.get('message', {}).get('text', '').strip()
        if text and sender:
            reply = build_reply(text)
            return {'sender': sender, 'reply': reply}
        return None


# ══════════════════════════════════════════════════════════════════════
# 4) E-POSTA — Gmail ile 15 dakikada hazır
# secrets.env: EMAIL_ADDRESS, EMAIL_PASSWORD (Gmail Uygulama Şifresi)
# ══════════════════════════════════════════════════════════════════════

class EmailAutoReply:
    """
    Gelen e-postalara otomatik yanıt.
    secrets.env: EMAIL_ADDRESS, EMAIL_PASSWORD
    Kurulum: Gmail → Hesabım → Güvenlik → Uygulama Şifreleri
    """
    def __init__(self):
        self.host     = os.getenv('SMTP_HOST', 'smtp.gmail.com')
        self.port     = int(os.getenv('SMTP_PORT', '587'))
        self.address  = os.getenv('EMAIL_ADDRESS', '')
        self.password = os.getenv('EMAIL_PASSWORD', '')

    @property
    def ready(self) -> bool:
        return bool(self.address and self.password)

    def send_reply(self, to_email: str, subject: str, incoming_text: str) -> bool:
        if not self.ready:
            logger.warning('E-posta bilgileri eksik — secrets.env doldurun')
            return False
        reply_body = build_reply(incoming_text)
        try:
            msg = MIMEMultipart('alternative')
            msg['From']    = f'trendurunlermarket.com <{self.address}>'
            msg['To']      = to_email
            msg['Subject'] = f'Re: {subject}'
            html = f"""<html><body>
            <p style="font-family:Arial;font-size:15px;">{reply_body}</p>
            <hr><p style="font-size:12px;color:#999;">
            trendurunlermarket.com | Otomatik yanıt</p>
            </body></html>"""
            msg.attach(MIMEText(html, 'html', 'utf-8'))
            with smtplib.SMTP(self.host, self.port) as s:
                s.ehlo(); s.starttls()
                s.login(self.address, self.password)
                s.sendmail(self.address, to_email, msg.as_string())
            _log_reply('email', to_email, incoming_text, reply_body)
            logger.info(f'E-posta yanıt gönderildi → {to_email}')
            return True
        except Exception as e:
            logger.error(f'E-posta hatası: {e}')
            return False


# ══════════════════════════════════════════════════════════════════════
# Facebook / Instagram DM (Meta Messenger API)
# secrets.env: FACEBOOK_ACCESS_TOKEN
# ══════════════════════════════════════════════════════════════════════

class MetaDMHandler:
    def __init__(self):
        self.token   = os.getenv('FACEBOOK_ACCESS_TOKEN', '')
        self._api    = 'https://graph.facebook.com/v19.0'

    @property
    def ready(self) -> bool:
        return bool(self.token)

    async def send_reply(self, recipient_id: str, text: str) -> bool:
        if not self.ready:
            return False
        try:
            import aiohttp
            async with aiohttp.ClientSession() as sess:
                async with sess.post(
                    f'{self._api}/me/messages',
                    json={'recipient': {'id': recipient_id},
                          'message': {'text': text[:2000]},
                          'access_token': self.token},
                    timeout=aiohttp.ClientTimeout(total=15),
                ) as r:
                    return r.status == 200
        except Exception as e:
            logger.error(f'Meta DM hatası: {e}')
            return False

    def process_webhook(self, event: Dict) -> Optional[Dict]:
        for entry in event.get('entry', []):
            for msg in entry.get('messaging', []):
                sid  = msg.get('sender', {}).get('id', '')
                text = msg.get('message', {}).get('text', '')
                if text and sid:
                    return {'sender_id': sid, 'reply': build_reply(text)}
        return None


# ══════════════════════════════════════════════════════════════════════
# Ana Sistem
# ══════════════════════════════════════════════════════════════════════

class AutoReplySystem:
    def __init__(self):
        self.telegram = TelegramDMHandler()
        self.discord  = DiscordDMHandler()
        self.viber    = ViberDMHandler()
        self.email    = EmailAutoReply()
        self.meta     = MetaDMHandler()

    def status(self) -> Dict:
        return {
            'telegram': '✅ Aktif' if self.telegram.ready else '⚠️  TELEGRAM_BOT_TOKEN eksik',
            'discord':  '✅ Aktif' if self.discord.ready  else '⚠️  DISCORD_BOT_TOKEN eksik',
            'viber':    '✅ Aktif' if self.viber.ready     else '⚠️  VIBER_BOT_TOKEN eksik',
            'email':    '✅ Aktif' if self.email.ready     else '⚠️  EMAIL_ADDRESS/PASSWORD eksik',
            'facebook': '✅ Aktif' if self.meta.ready      else '⚠️  FACEBOOK_ACCESS_TOKEN eksik',
        }

    async def run_loop(self, interval: int = 30):
        """Ana döngü — her 30 saniyede Telegram ve Discord mesajlarını kontrol et."""
        logger.info('DM Auto Reply başlatıldı')
        while True:
            try:
                await self.telegram.handle_updates()
            except Exception as e:
                logger.error(f'Telegram loop: {e}')
            try:
                await self.discord.handle_updates()
            except Exception as e:
                logger.error(f'Discord loop: {e}')
            await asyncio.sleep(interval)

    async def send_notification_all(self, message: str):
        """Tüm aktif kanallara bildirim gönder."""
        results = {}
        # Telegram kanal bildirimi
        channel_id = os.getenv('TELEGRAM_CHAT_ID', '')
        if channel_id:
            results['telegram'] = await self.telegram.broadcast(channel_id, message)
        # Discord webhook bildirimi (en kolay)
        results['discord'] = await self.discord.send_webhook(message)
        return results


auto_reply = AutoReplySystem()


if __name__ == '__main__':
    import sys
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s [%(levelname)s] %(message)s')

    print('\n╔══════════════════════════════════════════════╗')
    print('║   TRM DM Auto Reply v5.2 — Platform Durumu   ║')
    print('╠══════════════════════════════════════════════╣')
    for platform, durum in auto_reply.status().items():
        print(f'║  {platform:10s}: {durum:<34s}║')
    print('╚══════════════════════════════════════════════╝\n')

    print('Kurulum sıralaması (kolaydan zora):')
    print('  1. Telegram Bot  → t.me/BotFather → /newbot (5 dakika)')
    print('  2. Discord Bot   → discord.com/developers (10 dakika)')
    print('  3. Viber Bot     → partners.viber.com (15 dakika)')
    print('  4. Gmail E-posta → Uygulama Şifresi (15 dakika)')
    print('  5. Facebook DM   → developers.facebook.com (1-2 gün)')
    print()

    if '--run' in sys.argv:
        asyncio.run(auto_reply.run_loop())
