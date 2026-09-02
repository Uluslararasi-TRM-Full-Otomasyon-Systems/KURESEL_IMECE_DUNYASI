#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TRM Nirvana v3.0 - WhatsApp Otomatik Bildirim Sistemi
Sistemde, satışları ve gelen komisyonları, oluşabilecek hata,
arıza veya kritik durumlarda WhatsApp üzerinden otomatik bildirim gönderir
"""

import asyncio
import logging
import json
import os
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import requests
from urllib.parse import quote

# WhatsApp API ayarları
WHATSAPP_SETTINGS = {
    'phone_number': '+905426235116',  # WhatsApp bildirim numarası
    'api_url': 'https://api.whatsapp.com/v1/messages',  # WhatsApp Business API
    'token': 'YOUR_WHATSAPP_TOKEN',  # WhatsApp API token
    'webhook_url': 'http://localhost:9004/whatsapp-webhook',  # Webhook URL
    'message_types': ['sales', 'commission', 'error', 'critical', 'warning', 'info']
}

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/whatsapp_notifications.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class WhatsAppNotificationSystem:
    def __init__(self):
        self.running = False
        self.message_queue = []
        self.sent_messages = []
        self.failed_messages = []
        
        # Bildirim ayarları
        self.notification_settings = {
            'sales_notifications': True,      # Satış bildirimleri
            'commission_notifications': True,  # Komisyon bildirimleri
            'error_notifications': True,       # Hata bildirimleri
            'critical_notifications': True,    # Kritik bildirimler
            'warning_notifications': True,     # Uyarı bildirimleri
            'info_notifications': False,       # Bilgilendirme bildirimleri
            'rate_limit': 30,                  # Saat başına maksimum mesaj
            'retry_attempts': 3,                # Tekrar deneme sayısı
            'retry_delay': 60                   # Tekrar deneme gecikmesi (saniye)
        }
        
        # Banka bilgileri
        self.bank_info = {
            'iban': 'TR6700205000954078150003',
            'bank_name': 'TÜRKİYE İŞ BANKASI',
            'account_holder': 'TRM Nirvana Sistemi'
        }
    
    async def initialize(self):
        """WhatsApp bildirim sistemini başlat"""
        try:
            logger.info("📱 WhatsApp bildirim sistemi başlatılıyor...")
            
            # Log dizinini oluştur
            os.makedirs('logs', exist_ok=True)
            
            # Önceki mesajları yükle
            await self.load_previous_messages()
            
            self.running = True
            logger.info("✅ WhatsApp bildirim sistemi başlatıldı")
            return True
            
        except Exception as e:
            logger.error(f"❌ WhatsApp bildirim sistemi başlatma hatası: {e}")
            return False
    
    async def send_sales_notification(self, product_info: Dict):
        """Satış bildirimi gönder"""
        try:
            if not self.notification_settings['sales_notifications']:
                return False
            
            message = f"""
🛒 *YENİ SATIŞ!*

📦 *Ürün:* {product_info.get('name', 'Bilinmiyor')}
💰 *Fiyat:* {product_info.get('price', '0')} TL
🔥 *Komisyon:* {product_info.get('commission', '0')}%
💵 *Kazanç:* {product_info.get('earnings', '0')} TL
🛒 *Platform:* {product_info.get('platform', 'Bilinmiyor')}
⏰ *Zaman:* {datetime.now().strftime('%H:%M:%S')}

🎉 *TEBRİKLER!*
            """
            
            return await self.send_whatsapp_message(message, 'sales', product_info)
            
        except Exception as e:
            logger.error(f"❌ Satış bildirimi gönderme hatası: {e}")
            return False
    
    async def send_commission_notification(self, commission_info: Dict):
        """Komisyon bildirimi gönder"""
        try:
            if not self.notification_settings['commission_notifications']:
                return False
            
            message = f"""
💰 *KOMİSYON ÖDEMESİ!*

🏦 *Banka:* {self.bank_info['bank_name']}
💳 *IBAN:* {self.bank_info['iban']}
👤 *Hesap:* {self.bank_info['account_holder']}
💵 *Tutar:* {commission_info.get('amount', '0')} TL
📅 *Tarih:* {datetime.now().strftime('%d.%m.%Y')}
⏰ *Saat:* {datetime.now().strftime('%H:%M')}

📦 *Ürün:* {commission_info.get('product_name', 'Bilinmiyor')}
🔥 *Komisyon Oranı:* {commission_info.get('commission_rate', '0')}%

✅ *Ödeme Başarılı!*
            """
            
            return await self.send_whatsapp_message(message, 'commission', commission_info)
            
        except Exception as e:
            logger.error(f"❌ Komisyon bildirimi gönderme hatası: {e}")
            return False
    
    async def send_error_notification(self, error_info: Dict):
        """Hata bildirimi gönder"""
        try:
            if not self.notification_settings['error_notifications']:
                return False
            
            message = f"""
❌ *SİSTEM HATASI!*

🔴 *Hata Türü:* {error_info.get('type', 'Bilinmiyor')}
📁 *Modül:* {error_info.get('module', 'Bilinmiyor')}
📝 *Mesaj:* {error_info.get('message', 'Bilinmiyor')}
⏰ *Zaman:* {datetime.now().strftime('%H:%M:%S')}
🔄 *Tekrar Deneme:* {error_info.get('retry_count', '0')}

🔧 *Lütfen kontrol edin!*
            """
            
            return await self.send_whatsapp_message(message, 'error', error_info)
            
        except Exception as e:
            logger.error(f"❌ Hata bildirimi gönderme hatası: {e}")
            return False
    
    async def send_critical_notification(self, critical_info: Dict):
        """Kritik bildirim gönder"""
        try:
            if not self.notification_settings['critical_notifications']:
                return False
            
            message = f"""
🚨 *KRİTİK DURUM!*

⚠️ *Durum:* {critical_info.get('status', 'Bilinmiyor')}
📁 *Etkilen Modül:* {critical_info.get('module', 'Bilinmiyor')}
📝 *Açıklama:* {critical_info.get('description', 'Bilinmiyor')}
⏰ *Zaman:* {datetime.now().strftime('%H:%M:%S')}
🔄 *Otomatik Müdahale:* {critical_info.get('auto_action', 'Yok')}

🚨 *DERHAL EYLEM GEREKLİ!*
            """
            
            return await self.send_whatsapp_message(message, 'critical', critical_info)
            
        except Exception as e:
            logger.error(f"❌ Kritik bildirim gönderme hatası: {e}")
            return False
    
    async def send_warning_notification(self, warning_info: Dict):
        """Uyarı bildirimi gönder"""
        try:
            if not self.notification_settings['warning_notifications']:
                return False
            
            message = f"""
⚠️ *SİSTEM UYARISI!*

🔶 *Uyarı Türü:* {warning_info.get('type', 'Bilinmiyor')}
📁 *Modül:* {warning_info.get('module', 'Bilinmiyor')}
📝 *Mesaj:* {warning_info.get('message', 'Bilinmiyor')}
⏰ *Zaman:* {datetime.now().strftime('%H:%M:%S')}
📊 *Değer:* {warning_info.get('value', 'Bilinmiyor')}

🔍 *Lütfen kontrol edin!*
            """
            
            return await self.send_whatsapp_message(message, 'warning', warning_info)
            
        except Exception as e:
            logger.error(f"❌ Uyarı bildirimi gönderme hatası: {e}")
            return False
    
    async def send_daily_summary(self, summary_data: Dict):
        """Günlük özet bildirimi gönder"""
        try:
            message = f"""
📊 *GÜNLÜK ÖZET*

📅 *Tarih:* {datetime.now().strftime('%d.%m.%Y')}
📦 *Toplam Satış:* {summary_data.get('total_sales', 0)}
💰 *Toplam Kazanç:* {summary_data.get('total_earnings', 0)} TL
🔥 *Ortalama Komisyon:* {summary_data.get('avg_commission', 0)}%
📱 *Sosyal Paylaşım:* {summary_data.get('social_posts', 0)}
🤖 *AI İşlem:* {summary_data.get('ai_operations', 0)}
📊 *Başarı Oranı:* {summary_data.get('success_rate', 0)}%

🎯 *HEDEFLER:*
📦 Hedef Satış: {summary_data.get('sales_target', 0)}
💰 Hedef Kazanç: {summary_data.get('earnings_target', 0)} TL

📈 *PERFORMANS:*
{'✅ İYİ' if summary_data.get('success_rate', 0) >= 80 else '⚠️ İYİLEŞTİRİLMELİ'}
            """
            
            return await self.send_whatsapp_message(message, 'info', summary_data)
            
        except Exception as e:
            logger.error(f"❌ Günlük özet bildirimi gönderme hatası: {e}")
            return False
    
    async def send_whatsapp_message(self, message: str, message_type: str, data: Dict = None) -> bool:
        """WhatsApp mesajı gönder"""
        try:
            # Mesajı kuyruğa ekle
            message_data = {
                'id': str(int(time.time() * 1000)),
                'phone_number': WHATSAPP_SETTINGS['phone_number'],
                'message': message,
                'type': message_type,
                'data': data or {},
                'timestamp': datetime.now().isoformat(),
                'status': 'queued',
                'retry_count': 0
            }
            
            self.message_queue.append(message_data)
            
            # Rate limit kontrolü
            if await self.check_rate_limit():
                await self.process_message_queue()
            
            logger.info(f"📱 WhatsApp mesajı kuyruğa eklendi: {message_type}")
            return True
            
        except Exception as e:
            logger.error(f"❌ WhatsApp mesajı kuyruğa ekleme hatası: {e}")
            return False
    
    async def check_rate_limit(self) -> bool:
        """Rate limit kontrolü yap"""
        try:
            # Son 1 saatlik mesajları kontrol et
            one_hour_ago = datetime.now() - timedelta(hours=1)
            recent_messages = [m for m in self.sent_messages 
                              if datetime.fromisoformat(m['timestamp']) > one_hour_ago]
            
            return len(recent_messages) < self.notification_settings['rate_limit']
            
        except Exception as e:
            logger.error(f"❌ Rate limit kontrolü hatası: {e}")
            return False
    
    async def process_message_queue(self):
        """Mesaj kuyruğunu işle"""
        try:
            while self.message_queue and self.running:
                message_data = self.message_queue.pop(0)
                
                # WhatsApp API'ye gönder
                success = await self.send_to_whatsapp_api(message_data)
                
                if success:
                    message_data['status'] = 'sent'
                    self.sent_messages.append(message_data)
                    logger.info(f"✅ WhatsApp mesajı gönderildi: {message_data['type']}")
                else:
                    message_data['retry_count'] += 1
                    if message_data['retry_count'] < self.notification_settings['retry_attempts']:
                        # Tekrar deneme
                        await asyncio.sleep(self.notification_settings['retry_delay'])
                        self.message_queue.insert(0, message_data)  # Başa ekle
                    else:
                        message_data['status'] = 'failed'
                        self.failed_messages.append(message_data)
                        logger.error(f"❌ WhatsApp mesajı gönderilemedi: {message_data['type']}")
                
                # Mesajları kaydet
                await self.save_messages()
                
        except Exception as e:
            logger.error(f"❌ Mesaj kuyruğu işleme hatası: {e}")
    
    async def send_to_whatsapp_api(self, message_data: Dict) -> bool:
        """WhatsApp API'ye mesaj gönder"""
        try:
            # Bu mock bir implementasyondur
            # Gerçek WhatsApp Business API entegrasyonu gerekir
            
            # Mock başarılı gönderim
            await asyncio.sleep(1)  # API gecikmesi simülasyonu
            
            # %90 başarı oranı
            import random
            return random.random() > 0.1
            
        except Exception as e:
            logger.error(f"❌ WhatsApp API gönderme hatası: {e}")
            return False
    
    async def load_previous_messages(self):
        """Önceki mesajları yükle"""
        try:
            messages_file = 'whatsapp_messages.json'
            
            if os.path.exists(messages_file):
                with open(messages_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.sent_messages = data.get('sent_messages', [])
                    self.failed_messages = data.get('failed_messages', [])
                
                logger.info(f"✅ {len(self.sent_messages)} adet gönderilmiş mesaj yüklendi")
                
        except Exception as e:
            logger.error(f"❌ Önceki mesajları yükleme hatası: {e}")
    
    async def save_messages(self):
        """Mesajları kaydet"""
        try:
            messages_file = 'whatsapp_messages.json'
            
            # Son 100 mesajı tut
            recent_sent = self.sent_messages[-100:] if len(self.sent_messages) > 100 else self.sent_messages
            recent_failed = self.failed_messages[-50:] if len(self.failed_messages) > 50 else self.failed_messages
            
            data = {
                'sent_messages': recent_sent,
                'failed_messages': recent_failed,
                'last_update': datetime.now().isoformat()
            }
            
            with open(messages_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
                
        except Exception as e:
            logger.error(f"❌ Mesajları kaydetme hatası: {e}")
    
    async def get_notification_stats(self) -> Dict:
        """Bildirim istatistiklerini al"""
        try:
            stats = {
                'total_sent': len(self.sent_messages),
                'total_failed': len(self.failed_messages),
                'queue_size': len(self.message_queue),
                'success_rate': 0,
                'last_24h': {
                    'sent': 0,
                    'failed': 0
                },
                'by_type': {}
            }
            
            # Başarı oranı
            total = stats['total_sent'] + stats['total_failed']
            if total > 0:
                stats['success_rate'] = (stats['total_sent'] / total) * 100
            
            # Son 24 saatlik istatistikler
            one_day_ago = datetime.now() - timedelta(hours=24)
            
            recent_sent = [m for m in self.sent_messages 
                          if datetime.fromisoformat(m['timestamp']) > one_day_ago]
            recent_failed = [m for m in self.failed_messages 
                           if datetime.fromisoformat(m['timestamp']) > one_day_ago]
            
            stats['last_24h']['sent'] = len(recent_sent)
            stats['last_24h']['failed'] = len(recent_failed)
            
            # Türüne göre istatistikler
            for message in self.sent_messages:
                msg_type = message['type']
                if msg_type not in stats['by_type']:
                    stats['by_type'][msg_type] = 0
                stats['by_type'][msg_type] += 1
            
            return stats
            
        except Exception as e:
            logger.error(f"❌ Bildirim istatistikleri alma hatası: {e}")
            return {}
    
    async def run_notification_service(self):
        """Bildirim servisini çalıştır"""
        try:
            logger.info("📱 WhatsApp bildirim servisi çalışıyor...")
            
            while self.running:
                # Mesaj kuyruğunu işle
                await self.process_message_queue()
                
                # 30 saniyede bir kontrol et
                await asyncio.sleep(30)
                
        except Exception as e:
            logger.error(f"❌ Bildirim servisi çalışma hatası: {e}")
    
    def get_system_info(self) -> Dict:
        """Sistem bilgilerini al"""
        return {
            'running': self.running,
            'phone_number': WHATSAPP_SETTINGS['phone_number'],
            'notification_settings': self.notification_settings,
            'bank_info': self.bank_info,
            'queue_size': len(self.message_queue),
            'stats': self.get_notification_stats()
        }

# Ana başlatıcı
async def main():
    """Ana fonksiyon"""
    print("""
===============================================
    TRM NIRVANA v3.0 - WHATSAPP BİLDİRİM
===============================================
  📱 WhatsApp Otomatik Bildirim
  💰 Komisyon Ödeme Bildirimi
  ❌ Hata ve Kritik Uyarılar
  📊 Günlük Özet Bildirimleri
  🔄 Otomatik Tekrar Deneme
===============================================
    """)
    
    # WhatsApp bildirim sistemi oluştur
    whatsapp_system = WhatsAppNotificationSystem()
    
    try:
        # Sistemi başlat
        if await whatsapp_system.initialize():
            # Bildirim servisini çalıştır
            await whatsapp_system.run_notification_service()
        else:
            logger.error("❌ WhatsApp bildirim sistemi başlatılamadı")
            
    except KeyboardInterrupt:
        logger.info("👋 WhatsApp bildirim sistemi durduruldu")
    except Exception as e:
        logger.error(f"❌ Ana sistem hatası: {e}")

if __name__ == "__main__":
    asyncio.run(main())
