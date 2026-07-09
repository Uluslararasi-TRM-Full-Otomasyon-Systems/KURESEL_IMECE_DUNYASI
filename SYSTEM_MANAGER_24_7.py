#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TRM Nirvana v3.0 - 7/24 Kesintisiz Calisma Sistemi
Sistemin 7 gun 24 saat kesintisiz calismasini saglar
"""

import asyncio
import logging
import json
import time
import os
import psutil
import signal
import sys
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import threading
import subprocess

# Sistem modulleri
from main_orchestrator import TRMOrchestrator
from ai_integration import AIContentGenerator
from google_drive_integration import GoogleDriveManager, AnalyticsManager

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/system_manager.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class SystemManager24_7:
    def __init__(self):
        self.running = False
        self.orchestrator = None
        self.ai_generator = None
        self.drive_manager = None
        self.analytics_manager = None
        
        # Sistem durumu
        self.system_status = {
            'uptime': 0,
            'last_restart': None,
            'auto_restarts': 0,
            'health_checks': 0,
            'errors': 0,
            'warnings': 0
        }
        
        # Otomatik yeniden baslatma ayarlari
        self.auto_restart_settings = {
            'max_errors': 5,           # Maksimum hata sayisi
            'error_window': 300,        # Hata penceresi (saniye)
            'restart_delay': 60,         # Yeniden baslatma gecikmesi
            'health_check_interval': 30,  # Saglik kontrol araligi
            'max_memory_usage': 80,      # Maksimum bellek kullanimi (%)
            'max_cpu_usage': 90,         # Maksimum CPU kullanimi (%)
            'auto_restart': True,         # Otomatik yeniden baslatma
            'graceful_shutdown_timeout': 30  # Zarafetli kapatma zaman asimi
        }
        
        # Process'ler
        self.processes = {}
        self.start_time = None
        
        # Signal handler'lar
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
    
    def _signal_handler(self, signum, frame):
        """Signal handler"""
        logger.info(f"Signal {signum} received, shutting down gracefully...")
        self.running = False
        asyncio.create_task(self.shutdown_gracefully())
    
    async def initialize_system(self):
        """Sistemi baslat"""
        try:
            logger.info("🚀 TRM Nirvana v3.0 - 7/24 Sistemi Baslatiliyor...")
            
            # Log dizinini olustur
            os.makedirs('logs', exist_ok=True)
            
            # Sistem modullerini baslat
            self.orchestrator = TRMOrchestrator()
            self.ai_generator = AIContentGenerator()
            self.drive_manager = GoogleDriveManager()
            self.analytics_manager = AnalyticsManager(self.drive_manager)
            
            # Sistem durumunu guncelle
            self.start_time = datetime.now()
            self.system_status['last_restart'] = self.start_time.isoformat()
            self.system_status['uptime'] = 0
            
            logger.info("✅ 7/24 Sistemi baslatildi")
            return True
            
        except Exception as e:
            logger.error(f"❌ Sistem baslatma hatasi: {e}")
            return False
    
    async def start_all_modules(self):
        """Tum modulleri baslat"""
        try:
            logger.info("🤖 Tum moduller baslatiliyor...")
            
            # Ana orchestrator
            if self.orchestrator:
                orchestrator_task = asyncio.create_task(self.orchestrator.run())
                self.processes['orchestrator'] = orchestrator_task
                logger.info("✅ Ana orchestrator baslatildi")
            
            # AI generator
            if self.ai_generator:
                ai_task = asyncio.create_task(self._run_ai_generator())
                self.processes['ai_generator'] = ai_task
                logger.info("✅ AI generator baslatildi")
            
            # Drive manager
            if self.drive_manager:
                drive_task = asyncio.create_task(self._run_drive_manager())
                self.processes['drive_manager'] = drive_task
                logger.info("✅ Drive manager baslatildi")
            
            self.running = True
            logger.info("✅ Tum moduller baslatildi - 7/24 calisma aktif")
            
        except Exception as e:
            logger.error(f"❌ Modul baslatma hatasi: {e}")
            self.system_status['errors'] += 1
    
    async def _run_ai_generator(self):
        """AI generator'i calistir"""
        try:
            while self.running:
                # AI islemleri burada yapilacak
                await asyncio.sleep(60)  # 1 dakika bekle
        except Exception as e:
            logger.error(f"❌ AI generator hatasi: {e}")
            self.system_status['errors'] += 1
    
    async def _run_drive_manager(self):
        """Drive manager'i calistir"""
        try:
            while self.running:
                # Drive senkronizasyonu burada yapilacak
                await asyncio.sleep(300)  # 5 dakika bekle
        except Exception as e:
            logger.error(f"❌ Drive manager hatasi: {e}")
            self.system_status['errors'] += 1
    
    async def health_check(self):
        """Sistem sagligini kontrol et"""
        try:
            self.system_status['health_checks'] += 1
            
            # CPU kullanimi kontrolu
            cpu_usage = psutil.cpu_percent(interval=1)
            if cpu_usage > self.auto_restart_settings['max_cpu_usage']:
                logger.warning(f"⚠️ Yuksek CPU kullanimi: {cpu_usage}%")
                self.system_status['warnings'] += 1
            
            # Bellek kullanimi kontrolu
            memory = psutil.virtual_memory()
            if memory.percent > self.auto_restart_settings['max_memory_usage']:
                logger.warning(f"⚠️ Yuksek bellek kullanimi: {memory.percent}%")
                self.system_status['warnings'] += 1
            
            # Process durum kontrolu
            for name, task in self.processes.items():
                if task and task.done():
                    logger.error(f"❌ Process durdu: {name}")
                    self.system_status['errors'] += 1
                    
                    # Otomatik yeniden baslatma
                    if self.auto_restart_settings['auto_restart']:
                        await self.restart_process(name)
            
            # Uptime guncelleme
            if self.start_time:
                uptime = datetime.now() - self.start_time
                self.system_status['uptime'] = int(uptime.total_seconds())
            
            # Saglik durumunu kaydet
            await self.save_health_status()
            
        except Exception as e:
            logger.error(f"❌ Saglik kontrolu hatasi: {e}")
            self.system_status['errors'] += 1
    
    async def restart_process(self, process_name: str):
        """Process'i yeniden baslat"""
        try:
            logger.info(f"🔄 Process yeniden baslatiliyor: {process_name}")
            
            if process_name == 'orchestrator' and self.orchestrator:
                new_task = asyncio.create_task(self.orchestrator.run())
                self.processes['orchestrator'] = new_task
            elif process_name == 'ai_generator' and self.ai_generator:
                new_task = asyncio.create_task(self._run_ai_generator())
                self.processes['ai_generator'] = new_task
            elif process_name == 'drive_manager' and self.drive_manager:
                new_task = asyncio.create_task(self._run_drive_manager())
                self.processes['drive_manager'] = new_task
            
            self.system_status['auto_restarts'] += 1
            logger.info(f"✅ Process yeniden baslatildi: {process_name}")
            
        except Exception as e:
            logger.error(f"❌ Process yeniden baslatma hatasi: {e}")
    
    async def check_auto_restart_conditions(self):
        """Otomatik yeniden baslatma kosullarini kontrol et"""
        try:
            # Hata sayisi kontrolu
            if self.system_status['errors'] >= self.auto_restart_settings['max_errors']:
                logger.warning("⚠️ Cok fazla hata - sistem yeniden baslatilacak")
                await self.full_system_restart()
                return
            
            # Bellek/CPU kontrolu
            memory = psutil.virtual_memory()
            cpu_usage = psutil.cpu_percent(interval=1)
            
            if (memory.percent > self.auto_restart_settings['max_memory_usage'] or 
                cpu_usage > self.auto_restart_settings['max_cpu_usage']):
                
                logger.warning("⚠️ Sistem kaynaklari kritik seviyede - yeniden baslatilacak")
                await self.full_system_restart()
            
        except Exception as e:
            logger.error(f"❌ Otomatik yeniden baslatma kontrolu hatasi: {e}")
    
    async def full_system_restart(self):
        """Tam sistem yeniden baslatma"""
        try:
            logger.info("🔄 Tam sistem yeniden baslatiliyor...")
            
            # Tum process'leri durdur
            await self.stop_all_modules()
            
            # Bekle
            await asyncio.sleep(self.auto_restart_settings['restart_delay'])
            
            # Sistemi yeniden baslat
            await self.start_all_modules()
            
            self.system_status['auto_restarts'] += 1
            logger.info("✅ Sistem yeniden baslatildi")
            
        except Exception as e:
            logger.error(f"❌ Sistem yeniden baslatma hatasi: {e}")
    
    async def stop_all_modules(self):
        """Tum modulleri durdur"""
        try:
            logger.info("⏹️ Tum moduller durduruluyor...")
            
            # Tum task'leri iptal et
            for name, task in self.processes.items():
                if task and not task.done():
                    task.cancel()
                    try:
                        await task
                    except asyncio.CancelledError:
                        logger.info(f"✅ Task iptal edildi: {name}")
            
            self.processes.clear()
            self.running = False
            
            logger.info("✅ Tum moduller durduruldu")
            
        except Exception as e:
            logger.error(f"❌ Modul durdurma hatasi: {e}")
    
    async def shutdown_gracefully(self):
        """Zarafetli kapatma"""
        try:
            logger.info("🛑 Sistem zarafetli kapatiliyor...")
            
            # Tum modulleri durdur
            await self.stop_all_modules()
            
            # Son durum kaydet
            await self.save_system_status()
            
            logger.info("✅ Sistem zarafetli kapatildi")
            
        except Exception as e:
            logger.error(f"❌ Zarafetli kapatma hatasi: {e}")
    
    async def save_system_status(self):
        """Sistem durumunu kaydet"""
        try:
            status_file = 'system_status_24_7.json'
            
            with open(status_file, 'w', encoding='utf-8') as f:
                json.dump(self.system_status, f, ensure_ascii=False, indent=2)
                
        except Exception as e:
            logger.error(f"❌ Sistem durumu kaydetme hatasi: {e}")
    
    async def save_health_status(self):
        """Saglik durumunu kaydet"""
        try:
            health_file = 'health_status.json'
            
            health_data = {
                'timestamp': datetime.now().isoformat(),
                'uptime': self.system_status['uptime'],
                'cpu_usage': psutil.cpu_percent(),
                'memory_usage': psutil.virtual_memory().percent,
                'processes_running': len([p for p in self.processes.values() if p and not p.done()]),
                'auto_restarts': self.system_status['auto_restarts'],
                'errors': self.system_status['errors'],
                'warnings': self.system_status['warnings']
            }
            
            with open(health_file, 'w', encoding='utf-8') as f:
                json.dump(health_data, f, ensure_ascii=False, indent=2)
                
        except Exception as e:
            logger.error(f"❌ Saglik durumu kaydetme hatasi: {e}")
    
    def get_system_info(self) -> Dict:
        """Sistem bilgilerini al"""
        return {
            'system_status': self.system_status,
            'auto_restart_settings': self.auto_restart_settings,
            'processes': {name: (task and not task.done()) for name, task in self.processes.items()},
            'uptime': self.system_status['uptime'],
            'last_restart': self.system_status['last_restart']
        }
    
    async def run_24_7(self):
        """7/24 ana dongu"""
        try:
            logger.info("🚀 7/24 Sistem calismaya basliyor...")
            
            while self.running:
                # Saglik kontrolu
                await self.health_check()
                
                # Otomatik yeniden baslatma kosullarini kontrol et
                await self.check_auto_restart_conditions()
                
                # Belirtilen aralikta bekle
                await asyncio.sleep(self.auto_restart_settings['health_check_interval'])
                
        except Exception as e:
            logger.error(f"❌ 7/24 dongu hatasi: {e}")
            self.system_status['errors'] += 1

# Ana baslatici
async def main():
    """Ana fonksiyon"""
    print("""
===============================================
    TRM NIRVANA v3.0 - 7/24 SISTEM
===============================================
  🚀 7 GUN 24 SAAT KESINTISIZ
  🔄 OTOMATIK YENIDEN BASLATMA
  📊 SAGLIK KONTROLU
  ⚠️ HATA TAKIBI
  🛑 ZARAFETLI KAPATMA
===============================================
    """)
    
    # Sistem yoneticisi olustur
    system_manager = SystemManager24_7()
    
    try:
        # Sistemi baslat
        if await system_manager.initialize_system():
            # Tum modulleri baslat
            await system_manager.start_all_modules()
            
            # 7/24 donguyu baslat
            await system_manager.run_24_7()
        else:
            logger.error("❌ Sistem baslatilamadi")
            
    except KeyboardInterrupt:
        logger.info("👋 Kullanici tarafindan durduruldu")
    except Exception as e:
        logger.error(f"❌ Ana sistem hatasi: {e}")
    finally:
        # Zarafetli kapatma
        await system_manager.shutdown_gracefully()

if __name__ == "__main__":
    asyncio.run(main())
