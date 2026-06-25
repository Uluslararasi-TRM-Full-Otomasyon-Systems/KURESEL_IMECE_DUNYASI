#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TRM Nirvana v3.0 - Master Controller
Tüm sistem modüllerini bir arada yönetir
"""

import asyncio
import logging
import json
import os
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import threading
import signal
import sys

# Sistem modülleri
from SYSTEM_MANAGER_24_7 import SystemManager24_7
from AUTO_RESTART_MANAGER import AutoRestartManager
from DRIVE_SOCIAL_MANAGER import DriveSocialManager
from ADVANCED_DASHBOARD import AdvancedDashboardManager
from MESAJLASMA_BILDIRIM import herkese_bildir, telegram_bildir, discord_bildir, viber_bildir
from BANKA_KOMISYON_BILDIRIM import BankCommissionSystem

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/master_controller.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class TRMMasterController:
    def __init__(self):
        self.running = False
        self.start_time = None
        
        # Alt sistemler
        self.system_manager_24_7 = None
        self.auto_restart_manager = None
        self.drive_social_manager = None
        self.advanced_dashboard = None
        self.messaging_system = None
        self.bank_system = None
        
        # Sistem durumu
        self.master_status = {
            'status': 'stopped',
            'uptime': 0,
            'total_restarts': 0,
            'last_restart': None,
            'active_modules': [],
            'system_health': 100,
            'last_update': None
        }
        
        # Port'lar
        self.ports = {
            'main_panel': 9000,
            'status_api': 9001,
            'sales_alarm': 9002,
            'advanced_dashboard': 9003,
            'messaging_webhook': 9004,
            'bank_webhook': 9005
        }
        
        # Signal handler'lar
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
    
    def _signal_handler(self, signum, frame):
        """Signal handler"""
        logger.info(f"Signal {signum} received, shutting down gracefully...")
        self.running = False
        asyncio.create_task(self.shutdown_gracefully())
    
    async def initialize_all_systems(self):
        """Tüm sistemleri başlat"""
        try:
            logger.info("🚀 TRM Nirvana v3.0 - Master Controller Başlatılıyor...")
            
            # Log dizinini oluştur
            os.makedirs('logs', exist_ok=True)
            
            # 7/24 sistem yöneticisi
            self.system_manager_24_7 = SystemManager24_7()
            await self.system_manager_24_7.initialize_system()
            
            # Otomatik yeniden başlatma yöneticisi
            self.auto_restart_manager = AutoRestartManager()
            await self.auto_restart_manager.initialize()
            
            # Drive ve sosyal medya yöneticisi
            self.drive_social_manager = DriveSocialManager()
            await self.drive_social_manager.initialize_drive_service()
            
            # Gelişmiş yönetim paneli
            self.advanced_dashboard = AdvancedDashboardManager()
            
            # Telegram/Discord/Viber bildirim sistemi
            self.messaging_system = type("MessagingSystem", (), {"send": staticmethod(lambda m: None)})()
            await self.messaging_system.initialize()
            
            # Banka komisyon sistemi
            self.bank_system = BankCommissionSystem()
            await self.bank_system.initialize()
            
            # Sistem durumunu güncelle
            self.start_time = datetime.now()
            self.master_status['last_restart'] = self.start_time.isoformat()
            self.master_status['uptime'] = 0
            self.master_status['status'] = 'starting'
            self.master_status['active_modules'] = [
                'system_manager_24_7',
                'auto_restart_manager', 
                'drive_social_manager',
                'advanced_dashboard',
                'messaging_system',
                'bank_system'
            ]
            
            logger.info("✅ Tüm sistemler başlatıldı")
            return True
            
        except Exception as e:
            logger.error(f"❌ Sistemler başlatma hatası: {e}")
            return False
    
    async def start_all_services(self):
        """Tüm servisleri başlat"""
        try:
            logger.info("🔄 Tüm servisler başlatılıyor...")
            
            # Servisleri ayrı task'lerde başlat
            tasks = []
            
            # 7/24 sistem yöneticisi
            if self.system_manager_24_7:
                task_24_7 = asyncio.create_task(self.system_manager_24_7.run_24_7())
                tasks.append(('system_manager_24_7', task_24_7))
            
            # Otomatik yeniden başlatma yöneticisi
            if self.auto_restart_manager:
                task_restart = asyncio.create_task(self.auto_restart_manager.monitor_system())
                tasks.append(('auto_restart_manager', task_restart))
            
            # Drive ve sosyal medya yöneticisi
            if self.drive_social_manager:
                task_drive = asyncio.create_task(self.drive_social_manager.run_continuous_collection())
                tasks.append(('drive_social_manager', task_drive))
            
            # Telegram/Discord/Viber bildirim sistemi
            if self.messaging_system:
                task_messaging = asyncio.create_task(self.messaging_system.run_notification_service())
                tasks.append(('messaging_system', task_messaging))
            
            # Banka komisyon sistemi
            if self.bank_system:
                task_bank = asyncio.create_task(self.bank_system.run_monitoring())
                tasks.append(('bank_system', task_bank))
            
            # Gelişmiş yönetim paneli
            if self.advanced_dashboard:
                task_dashboard = asyncio.create_task(self.advanced_dashboard.start(port=self.ports['advanced_dashboard']))
                tasks.append(('advanced_dashboard', task_dashboard))
            
            self.running = True
            self.master_status['status'] = 'running'
            self.master_status['last_update'] = datetime.now().isoformat()
            
            logger.info("✅ Tüm servisler başlatıldı")
            return tasks
            
        except Exception as e:
            logger.error(f"❌ Servisler başlatma hatası: {e}")
            return []
    
    async def monitor_system_health(self):
        """Sistem sağlığını izle"""
        try:
            while self.running:
                # Sistem durumunu güncelle
                await self.update_master_status()
                
                # Her bir servisin durumunu kontrol et
                health_issues = await self.check_all_services_health()
                
                if health_issues:
                    logger.warning(f"⚠️ Sağlık sorunları: {health_issues}")
                    self.master_status['system_health'] -= len(health_issues) * 5
                else:
                    self.master_status['system_health'] = min(100, self.master_status['system_health'] + 1)
                
                # Sistem sağlığını kaydet
                await self.save_system_health()
                
                # 30 saniye bekle
                await asyncio.sleep(30)
                
        except Exception as e:
            logger.error(f"❌ Sistem sağlığı izleme hatası: {e}")
    
    async def check_all_services_health(self) -> List[str]:
        """Tüm servislerin sağlığını kontrol et"""
        issues = []
        
        try:
            # 7/24 sistem yöneticisi
            if self.system_manager_24_7:
                status = self.system_manager_24_7.get_system_status()
                if status.get('system_state', {}).get('status') != 'running':
                    issues.append('7/24 Sistem Yöneticisi çalışmıyor')
            
            # Otomatik yeniden başlatma yöneticisi
            if self.auto_restart_manager:
                status = self.auto_restart_manager.get_system_status()
                if not status.get('running', False):
                    issues.append('Otomatik Yeniden Başlatma Yöneticisi çalışmıyor')
            
            # Drive ve sosyal medya yöneticisi
            if self.drive_social_manager:
                status = self.drive_social_manager.get_system_status()
                if not status.get('drive_service_active', False):
                    issues.append('Drive ve Sosyal Medya Yöneticisi çalışmıyor')
            
            # Telegram/Discord/Viber bildirim sistemi
            if self.messaging_system:
                status = self.messaging_system.get_system_info()
                if not status.get('running', False):
                    issues.append('Telegram/Discord/Viber Bildirim Sistemi çalışmıyor')
            
            # Banka komisyon sistemi
            if self.bank_system:
                status = self.bank_system.get_system_status()
                if not status.get('running', False):
                    issues.append('Banka Komisyon Sistemi çalışmıyor')
            
            # Gelişmiş yönetim paneli
            if self.advanced_dashboard:
                # Panel port'unu kontrol et
                try:
                    import requests
                    response = requests.get(f'http://localhost:{self.ports["advanced_dashboard"]}/api/system-status', timeout=5)
                    if response.status_code != 200:
                        issues.append('Gelişmiş Yönetim Paneli erişilemiyor')
                except:
                    issues.append('Gelişmiş Yönetim Paneli erişilemiyor')
            
        except Exception as e:
            logger.error(f"❌ Servis sağlığı kontrolü hatası: {e}")
            issues.append(f"Sağlık kontrolü hatası: {e}")
        
        return issues
    
    async def update_master_status(self):
        """Ana sistem durumunu güncelle"""
        try:
            # Uptime güncelle
            if self.start_time:
                uptime = datetime.now() - self.start_time
                self.master_status['uptime'] = int(uptime.total_seconds())
            
            # Son güncelleme zamanı
            self.master_status['last_update'] = datetime.now().isoformat()
            
        except Exception as e:
            logger.error(f"❌ Ana sistem durumu güncelleme hatası: {e}")
    
    async def save_system_health(self):
        """Sistem sağlığını kaydet"""
        try:
            health_file = 'master_system_health.json'
            
            health_data = {
                'master_status': self.master_status,
                'ports': self.ports,
                'active_services': self.master_status['active_modules'],
                'timestamp': datetime.now().isoformat()
            }
            
            with open(health_file, 'w', encoding='utf-8') as f:
                json.dump(health_data, f, ensure_ascii=False, indent=2)
                
        except Exception as e:
            logger.error(f"❌ Sistem sağlığı kaydetme hatası: {e}")
    
    async def shutdown_gracefully(self):
        """Zarafetli kapatma"""
        try:
            logger.info("🛑 Master Controller zarafetli kapatılıyor...")
            
            self.running = False
            self.master_status['status'] = 'shutdown'
            
            # Tüm servisleri durdur
            if self.system_manager_24_7:
                await self.system_manager_24_7.shutdown_gracefully()
            
            if self.auto_restart_manager:
                self.auto_restart_manager.running = False
            
            if self.drive_social_manager:
                self.drive_social_manager.running = False
            
            if self.messaging_system:
                self.messaging_system.running = False
            
            if self.bank_system:
                self.bank_system.running = False
            
            # Son durum kaydet
            await self.save_system_health()
            
            logger.info("✅ Master Controller zarafetli kapatıldı")
            
        except Exception as e:
            logger.error(f"❌ Zarafetli kapatma hatası: {e}")
    
    def get_master_status(self) -> Dict:
        """Ana sistem durumunu al"""
        return {
            'master_status': self.master_status,
            'ports': self.ports,
            'services': {
                'system_manager_24_7': self.system_manager_24_7.get_system_status() if self.system_manager_24_7 else None,
                'auto_restart_manager': self.auto_restart_manager.get_system_status() if self.auto_restart_manager else None,
                'drive_social_manager': self.drive_social_manager.get_system_status() if self.drive_social_manager else None,
                'advanced_dashboard': self.advanced_dashboard.get_system_status() if self.advanced_dashboard else None,
                'messaging_system': self.messaging_system.get_system_info() if self.messaging_system else None,
                'bank_system': self.bank_system.get_system_status() if self.bank_system else None
            },
            'uptime': self.master_status['uptime'],
            'last_restart': self.master_status['last_restart'],
            'system_health': self.master_status['system_health']
        }
    
    async def run_master_controller(self):
        """Ana controller döngüsü"""
        try:
            logger.info("🚀 Master Controller çalışmaya başlıyor...")
            
            while self.running:
                # Sistem sağlığını izle
                await self.monitor_system_health()
                
                # Hata durumunda yeniden başlatma kontrolü
                if self.master_status['system_health'] < 50:
                    logger.warning("⚠️ Sistem sağlığı kritik seviyede - yeniden başlatma düşünülebilir")
                
                # 1 dakika bekle
                await asyncio.sleep(60)
                
        except Exception as e:
            logger.error(f"❌ Master controller döngü hatası: {e}")
    
    def print_system_info(self):
        """Sistem bilgilerini yazdır"""
        print("""
===============================================
    TRM NIRVANA v3.0 - MASTER CONTROLLER
===============================================
  🚀 TÜM SİSTEMLERİ BİR ARADA YÖNETİR
  📊 GERÇEK ZAMANLI DURUM TAKİBİ
  🔄 7/24 KESİNTİSİZ ÇALIŞMA
  📱 ÇOKLU PANEL YAPISI
  💰 KOMİSYON VE BANKA BİLDİRİMİ
  🌐 GELİŞMİŞ YÖNETİM PANELİ
===============================================
        """)
        
        print("🌐 AKTİF PORTLAR:")
        for name, port in self.ports.items():
            print(f"  • {name}: http://localhost:{port}")
        
        print("\n🤖 AKTİF MODÜLLER:")
        for module in self.master_status['active_modules']:
            print(f"  • {module}")
        
        print(f"\n📊 SİSTEM SAĞLIĞI: {self.master_status['system_health']}%")
        print(f"⏰ ÇALIŞMA SÜRESİ: {self.master_status['uptime']} saniye")

# Ana başlatıcı
async def main():
    """Ana fonksiyon"""
    controller = TRMMasterController()
    
    try:
        # Sistem bilgilerini göster
        controller.print_system_info()
        
        # Tüm sistemleri başlat
        if await controller.initialize_all_systems():
            # Tüm servisleri başlat
            tasks = await controller.start_all_services()
            
            # Ana controller döngüsünü başlat
            await controller.run_master_controller()
        else:
            logger.error("❌ Sistemler başlatılamadı")
            
    except KeyboardInterrupt:
        logger.info("👋 Kullanıcı tarafından durduruldu")
    except Exception as e:
        logger.error(f"❌ Ana sistem hatası: {e}")
    finally:
        # Zarafetli kapatma
        await controller.shutdown_gracefully()

if __name__ == "__main__":
    asyncio.run(main())
