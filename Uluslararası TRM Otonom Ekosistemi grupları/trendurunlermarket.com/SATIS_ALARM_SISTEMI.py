#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TRM Nirvana v3.0 - Satış Alarm ve Uyarı Sistemi
Panel üzerinden satış hareketlerini takip eder
"""

import asyncio
import logging
import json
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional

# Sistem modülleri
from google_drive_integration import AnalyticsManager, GoogleDriveManager
from ai_integration import AIContentGenerator

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SalesAlarmSystem:
    def __init__(self):
        self.drive_manager = GoogleDriveManager()
        self.analytics_manager = AnalyticsManager(self.drive_manager)
        self.ai_generator = AIContentGenerator()
        
        # Satış takibi
        self.sales_data = []
        self.alerts = []
        self.last_check = datetime.now()
        
        # Alarm ayarları
        self.alert_settings = {
            'min_commission': 20.0,  # Minimum komisyon oranı
            'min_price': 100.0,      # Minimum fiyat
            'success_threshold': 5,   # Başarılı paylaşım eşiği
            'check_interval': 300,    # Kontrol aralığı (saniye)
            'telegram_alerts': True,   # Telegram bildirimleri
            'panel_alerts': True      # Panel bildirimleri
        }
    
    async def track_sales_activity(self):
        """Satış aktivitesini takip et"""
        try:
            # Analitik verilerini al
            dashboard_stats = self.analytics_manager.get_dashboard_stats()
            
            # Günlük satışları kontrol et
            today = datetime.now().strftime('%Y-%m-%d')
            daily_stats = self.analytics_manager.analytics_data.get('daily_stats', {}).get(today, {})
            
            # Satış hareketlerini analiz et
            sales_activity = {
                'timestamp': datetime.now().isoformat(),
                'products_captured': dashboard_stats.get('today_products', 0),
                'high_commission': dashboard_stats.get('today_high_commission', 0),
                'social_published': dashboard_stats.get('today_social_published', 0),
                'estimated_commission': dashboard_stats.get('today_estimated_commission', 0),
                'success_rate': dashboard_stats.get('success_rate', 0)
            }
            
            self.sales_data.append(sales_activity)
            
            # Alarm kontrolü yap
            await self.check_alerts(sales_activity)
            
            return sales_activity
            
        except Exception as e:
            logger.error(f"Satış takibi hatası: {e}")
            return None
    
    async def check_alerts(self, sales_activity: Dict):
        """Alarm kontrollerini yap"""
        alerts = []
        
        # Yüksek komisyonlu ürün alarmı
        if sales_activity.get('high_commission', 0) >= 3:
            alerts.append({
                'type': 'high_commission',
                'level': 'success',
                'title': '🔥 Yüksek Komisyonlu Ürünler!',
                'message': f"Bugün {sales_activity['high_commission']} adet %20+ komisyonlu ürün yakalandı!",
                'timestamp': datetime.now().isoformat(),
                'data': sales_activity
            })
        
        # Başarılı paylaşım alarmı
        if sales_activity.get('social_published', 0) >= 5:
            alerts.append({
                'type': 'social_success',
                'level': 'success',
                'title': '📱 Sosyal Medya Başarısı!',
                'message': f"Bugün {sales_activity['social_published']} adet sosyal medya paylaşımı yapıldı!",
                'timestamp': datetime.now().isoformat(),
                'data': sales_activity
            })
        
        # Tahmini komisyon alarmı
        if sales_activity.get('estimated_commission', 0) >= 50:
            alerts.append({
                'type': 'commission_alert',
                'level': 'warning',
                'title': '💰 Komisyon Hedefi!',
                'message': f"Tahmini günlük komisyon: {sales_activity['estimated_commission']:.2f} TL",
                'timestamp': datetime.now().isoformat(),
                'data': sales_activity
            })
        
        # Başarı oranı alarmı
        if sales_activity.get('success_rate', 0) >= 80:
            alerts.append({
                'type': 'success_rate',
                'level': 'info',
                'title': '📊 Yüksek Başarı Oranı!',
                'message': f"Sistem başarı oranı: {sales_activity['success_rate']:.1f}%",
                'timestamp': datetime.now().isoformat(),
                'data': sales_activity
            })
        
        # Alert'leri kaydet
        for alert in alerts:
            self.alerts.append(alert)
            await self.send_alert(alert)
    
    async def send_alert(self, alert: Dict):
        """Alert gönder"""
        try:
            # Panel alert'i
            if self.alert_settings['panel_alerts']:
                await self.add_panel_alert(alert)
            
            # Telegram alert'i
            if self.alert_settings['telegram_alerts']:
                await self.send_telegram_alert(alert)
            
            logger.info(f"Alert gönderildi: {alert['title']}")
            
        except Exception as e:
            logger.error(f"Alert gönderme hatası: {e}")
    
    async def add_panel_alert(self, alert: Dict):
        """Panel'e alert ekle"""
        try:
            # Alert'i JSON dosyasına kaydet
            alert_file = 'panel_alerts.json'
            
            # Mevcut alert'leri oku
            alerts = []
            if os.path.exists(alert_file):
                with open(alert_file, 'r', encoding='utf-8') as f:
                    alerts = json.load(f)
            
            # Yeni alert'i ekle
            alerts.append(alert)
            
            # Son 50 alert'i tut
            if len(alerts) > 50:
                alerts = alerts[-50:]
            
            # Kaydet
            with open(alert_file, 'w', encoding='utf-8') as f:
                json.dump(alerts, f, ensure_ascii=False, indent=2)
            
        except Exception as e:
            logger.error(f"Panel alert ekleme hatası: {e}")
    
    async def send_telegram_alert(self, alert: Dict):
        """Telegram alert'i gönder"""
        try:
            # Telegram mesajı oluştur
            message = f"""
🚨 {alert['title']}

{alert['message']}

📊 Detaylar:
• Yakalanan Ürün: {alert['data'].get('products_captured', 0)}
• %20+ Ürün: {alert['data'].get('high_commission', 0)}
• Sosyal Paylaşım: {alert['data'].get('social_published', 0)}
• Tahmini Komisyon: {alert['data'].get('estimated_commission', 0):.2f} TL
• Başarı Oranı: {alert['data'].get('success_rate', 0):.1f}%

⏰ {alert['timestamp']}
            """
            
            # Telegram gönderimi (mock)
            logger.info(f"Telegram alert: {message}")
            
        except Exception as e:
            logger.error(f"Telegram alert gönderme hatası: {e}")
    
    def get_recent_alerts(self, limit: int = 10) -> List[Dict]:
        """Son alert'leri al"""
        return self.alerts[-limit:]
    
    def get_sales_summary(self) -> Dict:
        """Satış özetini al"""
        if not self.sales_data:
            return {
                'total_products': 0,
                'total_high_commission': 0,
                'total_social_published': 0,
                'total_commission': 0,
                'avg_success_rate': 0,
                'last_update': None
            }
        
        # Son 24 saatlik veriler
        last_24h = datetime.now() - timedelta(hours=24)
        recent_sales = [s for s in self.sales_data if datetime.fromisoformat(s['timestamp']) > last_24h]
        
        if not recent_sales:
            recent_sales = self.sales_data[-10:]  # Son 10 kayıt
        
        total_products = sum(s.get('products_captured', 0) for s in recent_sales)
        total_high_commission = sum(s.get('high_commission', 0) for s in recent_sales)
        total_social_published = sum(s.get('social_published', 0) for s in recent_sales)
        total_commission = sum(s.get('estimated_commission', 0) for s in recent_sales)
        avg_success_rate = sum(s.get('success_rate', 0) for s in recent_sales) / max(len(recent_sales), 1)
        
        return {
            'total_products': total_products,
            'total_high_commission': total_high_commission,
            'total_social_published': total_social_published,
            'total_commission': total_commission,
            'avg_success_rate': avg_success_rate,
            'last_update': datetime.now().isoformat()
        }

class SalesAlertAPI:
    """Satış alert API'si"""
    def __init__(self):
        self.alarm_system = SalesAlarmSystem()
    
    async def start_monitoring(self):
        """İzlemeyi başlat"""
        logger.info("🚨 Satış alarm sistemi başlatılıyor...")
        
        while True:
            try:
                # Satış aktivitesini takip et
                await self.alarm_system.track_sales_activity()
                
                # Belirtilen aralıkta bekle
                await asyncio.sleep(self.alarm_system.alert_settings['check_interval'])
                
            except Exception as e:
                logger.error(f"Satış izleme hatası: {e}")
                await asyncio.sleep(60)  # Hata durumunda 1 dakika bekle
    
    def get_alerts(self, limit: int = 10) -> List[Dict]:
        """Alert'leri al"""
        return self.alarm_system.get_recent_alerts(limit)
    
    def get_sales_summary(self) -> Dict:
        """Satış özetini al"""
        return self.alarm_system.get_sales_summary()

# Test ve örnek kullanım
async def test_sales_alarm():
    """Satış alarm sistemini test et"""
    alarm_system = SalesAlarmSystem()
    
    logger.info("🚨 Satış alarm sistemi test ediliyor...")
    
    # Test satış verisi
    test_sales = {
        'timestamp': datetime.now().isoformat(),
        'products_captured': 15,
        'high_commission': 5,
        'social_published': 8,
        'estimated_commission': 75.50,
        'success_rate': 85.5
    }
    
    # Alert kontrolü
    await alarm_system.check_alerts(test_sales)
    
    # Alert'leri göster
    alerts = alarm_system.get_recent_alerts()
    for alert in alerts:
        print(f"🚨 {alert['title']}: {alert['message']}")
    
    # Satış özeti
    summary = alarm_system.get_sales_summary()
    print(f"📊 Satış özeti: {summary}")

if __name__ == "__main__":
    asyncio.run(test_sales_alarm())
