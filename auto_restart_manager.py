#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TRM Nirvana v3.0 - Otomatik Durma ve Yeniden Baslatma Mekanizmasi
Sistem hangi durumlarda otomatik olarak duracagini, hangi durumlarda 
kendini yeniden baslatacagini ve belirli bir sure sonra otomatik 
olarak tekrar calismaya devam edip etmeyecegini yonetir
"""

import asyncio
import logging
import json
import time
import os
import psutil
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/auto_restart.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class AutoRestartManager:
    def __init__(self):
        self.running = False
        self.restart_count = 0
        self.last_restart = None
        self.error_history = []
        self.warning_history = []
        
        # Otomatik durma kosullari
        self.shutdown_conditions = {
            'critical_errors': 10,           # Kritik hata sayisi
            'memory_threshold': 95,           # Bellek kullanim esigi (%)
            'cpu_threshold': 98,               # CPU kullanim esigi (%)
            'disk_space_threshold': 5,          # Disk alani esigi (GB)
            'network_timeout': 300,            # Ag zaman asimi (saniye)
            'consecutive_failures': 5,         # Art arda hata sayisi
            'max_uptime_hours': 168,          # Maksimum calisma suresi (7 gun)
            'manual_shutdown': False            # Manuel kapatma
        }
        
        # Otomatik yeniden baslatma kosullari
        self.restart_conditions = {
            'error_threshold': 3,              # Hata esigi
            'error_window': 300,               # Hata penceresi (saniye)
            'warning_threshold': 10,            # Uyari esigi
            'memory_restart_threshold': 90,      # Bellek yeniden baslatma esigi
            'cpu_restart_threshold': 85,         # CPU yeniden baslatma esigi
            'auto_restart_enabled': True,        # Otomatik yeniden baslatma aktif
            'restart_delay': 60,                # Yeniden baslatma gecikmesi (saniye)
            'max_restarts_per_hour': 3,         # Saatte maksimum yeniden baslatma
            'graceful_shutdown_timeout': 30     # Zarafetli kapatma zaman asimi
        }
        
        # Calisma durumu
        self.system_state = {
            'status': 'stopped',                # stopped, starting, running, restarting, shutdown
            'last_check': None,
            'uptime': 0,
            'total_restarts': 0,
            'last_shutdown_reason': None,
            'next_restart_time': None,
            'health_score': 100
        }
    
    async def initialize(self):
        """Otomatik yeniden baslatma sistemini baslat"""
        try:
            logger.info("🔄 Otomatik Durma ve Yeniden Baslatma Sistemi Baslatiliyor...")
            
            # Log dizinini olustur
            os.makedirs('logs', exist_ok=True)
            
            # Onceki durumu yukle
            await self.load_previous_state()
            
            self.running = True
            self.system_state['status'] = 'starting'
            self.system_state['last_check'] = datetime.now().isoformat()
            
            logger.info("✅ Otomatik yeniden baslatma sistemi baslatildi")
            return True
            
        except Exception as e:
            logger.error(f"❌ Otomatik yeniden baslatma sistemi baslatma hatasi: {e}")
            return False
    
    async def monitor_system(self):
        """Sistemi izle"""
        try:
            while self.running:
                current_time = datetime.now()
                
                # Sistem durumunu guncelle
                await self.update_system_status()
                
                # Otomatik durma kosullarini kontrol et
                shutdown_reason = await self.check_shutdown_conditions()
                
                if shutdown_reason:
                    logger.warning(f"⚠️ Otomatik durma kosulu: {shutdown_reason}")
                    await self.initiate_shutdown(shutdown_reason)
                    break
                
                # Otomatik yeniden baslatma kosullarini kontrol et
                restart_reason = await self.check_restart_conditions()
                
                if restart_reason:
                    logger.info(f"🔄 Otomatik yeniden baslatma kosulu: {restart_reason}")
                    await self.initiate_restart(restart_reason)
                
                # Belirli sure sonra devam etme kontrolu
                await self.check_continuation_conditions()
                
                # Saglik skorunu guncelle
                await self.update_health_score()
                
                # Durumu kaydet
                await self.save_system_state()
                
                # Izleme araliginda bekle
                await asyncio.sleep(30)  # 30 saniye
                
        except Exception as e:
            logger.error(f"❌ Sistem izleme hatasi: {e}")
            self.error_history.append({
                'timestamp': datetime.now().isoformat(),
                'error': str(e),
                'type': 'monitoring'
            })
    
    async def check_shutdown_conditions(self) -> Optional[str]:
        """Otomatik durma kosullarini kontrol et"""
        try:
            # Kritik hata sayisi kontrolu
            recent_errors = [e for e in self.error_history 
                           if datetime.fromisoformat(e['timestamp']) > datetime.now() - timedelta(hours=1)]
            
            if len(recent_errors) >= self.shutdown_conditions['critical_errors']:
                return f"Kritik hata sayisi asildi: {len(recent_errors)}"
            
            # Bellek kullanimi kontrolu
            memory = psutil.virtual_memory()
            if memory.percent >= self.shutdown_conditions['memory_threshold']:
                return f"Bellek kullanimi kritik seviyede: {memory.percent}%"
            
            # CPU kullanimi kontrolu
            cpu_usage = psutil.cpu_percent(interval=1)
            if cpu_usage >= self.shutdown_conditions['cpu_threshold']:
                return f"CPU kullanimi kritik seviyede: {cpu_usage}%"
            
            # Disk alani kontrolu
            disk = psutil.disk_usage('/')
            free_gb = disk.free / (1024**3)
            if free_gb <= self.shutdown_conditions['disk_space_threshold']:
                return f"Disk alani kritik seviyede: {free_gb:.1f}GB"
            
            # Art arda hata kontrolu
            consecutive_errors = await self.check_consecutive_failures()
            if consecutive_errors >= self.shutdown_conditions['consecutive_failures']:
                return f"Art arda hata sayisi: {consecutive_errors}"
            
            # Maksimum calisma suresi kontrolu
            if self.system_state['uptime'] >= self.shutdown_conditions['max_uptime_hours'] * 3600:
                return f"Maksimum calisma suresi asildi: {self.system_state['uptime']}saniye"
            
            return None
            
        except Exception as e:
            logger.error(f"❌ Durma kosulu kontrolu hatasi: {e}")
            return None
    
    async def check_restart_conditions(self) -> Optional[str]:
        """Otomatik yeniden baslatma kosullarini kontrol et"""
        try:
            if not self.restart_conditions['auto_restart_enabled']:
                return None
            
            # Hata esigi kontrolu
            recent_errors = [e for e in self.error_history 
                           if datetime.fromisoformat(e['timestamp']) > datetime.now() - timedelta(seconds=self.restart_conditions['error_window'])]
            
            if len(recent_errors) >= self.restart_conditions['error_threshold']:
                return f"Hata esigi asildi: {len(recent_errors)}"
            
            # Bellek yeniden baslatma esigi
            memory = psutil.virtual_memory()
            if memory.percent >= self.restart_conditions['memory_restart_threshold']:
                return f"Bellek kullanimi yeniden baslatma esiginde: {memory.percent}%"
            
            # CPU yeniden baslatma esigi
            cpu_usage = psutil.cpu_percent(interval=1)
            if cpu_usage >= self.restart_conditions['cpu_restart_threshold']:
                return f"CPU kullanimi yeniden baslatma esiginde: {cpu_usage}%"
            
            # Saatte maksimum yeniden baslatma kontrolu
            recent_restarts = [r for r in self.error_history 
                              if datetime.fromisoformat(r['timestamp']) > datetime.now() - timedelta(hours=1)]
            
            if len(recent_restarts) >= self.restart_conditions['max_restarts_per_hour']:
                return f"Saatte maksimum yeniden baslatma asildi: {len(recent_restarts)}"
            
            return None
            
        except Exception as e:
            logger.error(f"❌ Yeniden baslatma kosulu kontrolu hatasi: {e}")
            return None
    
    async def check_consecutive_failures(self) -> int:
        """Art arda hata sayisini kontrol et"""
        try:
            consecutive_count = 0
            current_time = datetime.now()
            
            # Son 1 saatlik hatalari kontrol et
            recent_errors = sorted([e for e in self.error_history 
                                if datetime.fromisoformat(e['timestamp']) > current_time - timedelta(hours=1)],
                               key=lambda x: datetime.fromisoformat(x['timestamp']))
            
            for error in recent_errors:
                error_time = datetime.fromisoformat(error['timestamp'])
                time_diff = (current_time - error_time).total_seconds()
                
                if time_diff <= 300:  # 5 dakika icinde
                    consecutive_count += 1
                else:
                    break
            
            return consecutive_count
            
        except Exception as e:
            logger.error(f"❌ Art arda hata kontrolu hatasi: {e}")
            return 0
    
    async def check_continuation_conditions(self):
        """Belirli sure sonra devam etme kosullarini kontrol et"""
        try:
            # Sistem durumuna gore devam etme karari
            if self.system_state['status'] == 'restarting':
                # Yeniden baslatma durumunda 1 dakika bekle
                if datetime.now() > datetime.fromisoformat(self.system_state['next_restart_time']):
                    self.system_state['status'] = 'running'
                    logger.info("✅ Sistem yeniden baslatildi, normale donuldu")
            
            elif self.system_state['status'] == 'shutdown':
                # Kapatma durumunda devam etme
                logger.info("⏹️ Sistem kapatildi, devam etmiyor")
                self.running = False
                
        except Exception as e:
            logger.error(f"❌ Devam etme kosulu kontrolu hatasi: {e}")
    
    async def initiate_shutdown(self, reason: str):
        """Otomatik kapatmayi baslat"""
        try:
            logger.info(f"⏹️ Otomatik kapatma baslatiliyor: {reason}")
            
            self.system_state['status'] = 'shutdown'
            self.system_state['last_shutdown_reason'] = reason
            self.system_state['last_check'] = datetime.now().isoformat()
            
            # Kapatma bildirimi gonder
            await self.send_shutdown_notification(reason)
            
            # Zarafetli kapatma
            await self.graceful_shutdown()
            
        except Exception as e:
            logger.error(f"❌ Otomatik kapatma hatasi: {e}")
    
    async def initiate_restart(self, reason: str):
        """Otomatik yeniden baslatmayi baslat"""
        try:
            logger.info(f"🔄 Otomatik yeniden baslatma baslatiliyor: {reason}")
            
            self.system_state['status'] = 'restarting'
            self.system_state['last_restart'] = datetime.now().isoformat()
            self.system_state['next_restart_time'] = (datetime.now() + timedelta(seconds=self.restart_conditions['restart_delay'])).isoformat()
            self.system_state['total_restarts'] += 1
            self.restart_count += 1
            
            # Yeniden baslatma bildirimi gonder
            await self.send_restart_notification(reason)
            
            # Zarafetli yeniden baslatma
            await self.graceful_restart()
            
        except Exception as e:
            logger.error(f"❌ Otomatik yeniden baslatma hatasi: {e}")
    
    async def graceful_shutdown(self):
        """Zarafetli kapatma"""
        try:
            logger.info("🛑 Zarafetli kapatma baslatiliyor...")
            
            # Tum process'leri durdur
            # Burada ana orchestrator ve diger moduller durdurulacak
            
            # Kaydetme islemleri
            await self.save_system_state()
            
            self.system_state['status'] = 'stopped'
            logger.info("✅ Zarafetli kapatma tamamlandi")
            
        except Exception as e:
            logger.error(f"❌ Zarafetli kapatma hatasi: {e}")
    
    async def graceful_restart(self):
        """Zarafetli yeniden baslatma"""
        try:
            logger.info("🔄 Zarafetli yeniden baslatma baslatiliyor...")
            
            # Zarafetli kapatma
            await self.graceful_shutdown()
            
            # Bekle
            await asyncio.sleep(self.restart_conditions['restart_delay'])
            
            # Sistemi yeniden baslat
            # Burada ana orchestrator ve diger moduller baslatilacak
            
            self.system_state['status'] = 'running'
            logger.info("✅ Zarafetli yeniden baslatma tamamlandi")
            
        except Exception as e:
            logger.error(f"❌ Zarafetli yeniden baslatma hatasi: {e}")
    
    async def send_shutdown_notification(self, reason: str):
        """Kapatma bildirimi gonder"""
        try:
            notification = {
                'type': 'shutdown',
                'reason': reason,
                'timestamp': datetime.now().isoformat(),
                'uptime': self.system_state['uptime'],
                'total_restarts': self.system_state['total_restarts']
            }
            
            # Bildirimi kaydet
            await self.save_notification(notification)
            
            logger.info(f"📢 Kapatma bildirimi gonderildi: {reason}")
            
        except Exception as e:
            logger.error(f"❌ Kapatma bildirimi gonderme hatasi: {e}")
    
    async def send_restart_notification(self, reason: str):
        """Yeniden baslatma bildirimi gonder"""
        try:
            notification = {
                'type': 'restart',
                'reason': reason,
                'timestamp': datetime.now().isoformat(),
                'uptime': self.system_state['uptime'],
                'restart_count': self.restart_count
            }
            
            # Bildirimi kaydet
            await self.save_notification(notification)
            
            logger.info(f"📢 Yeniden baslatma bildirimi gonderildi: {reason}")
            
        except Exception as e:
            logger.error(f"❌ Yeniden baslatma bildirimi gonderme hatasi: {e}")
    
    async def save_notification(self, notification: Dict):
        """Bildirimi kaydet"""
        try:
            notifications_file = 'notifications.json'
            
            # Mevcut bildirimleri oku
            notifications = []
            if os.path.exists(notifications_file):
                with open(notifications_file, 'r', encoding='utf-8') as f:
                    notifications = json.load(f)
            
            # Yeni bildirimi ekle
            notifications.append(notification)
            
            # Son 50 bildirimi tut
            if len(notifications) > 50:
                notifications = notifications[-50:]
            
            # Kaydet
            with open(notifications_file, 'w', encoding='utf-8') as f:
                json.dump(notifications, f, ensure_ascii=False, indent=2)
                
        except Exception as e:
            logger.error(f"❌ Bildirim kaydetme hatasi: {e}")
    
    async def update_system_status(self):
        """Sistem durumunu guncelle"""
        try:
            current_time = datetime.now()
            
            # Uptime guncelle
            if self.system_state['status'] == 'running':
                self.system_state['uptime'] += 30  # 30 saniye ekle
            
            self.system_state['last_check'] = current_time.isoformat()
            
        except Exception as e:
            logger.error(f"❌ Sistem durumu guncelleme hatasi: {e}")
    
    async def update_health_score(self):
        """Saglik skorunu guncelle"""
        try:
            score = 100
            
            # Hatalara gore skor dusur
            recent_errors = [e for e in self.error_history 
                           if datetime.fromisoformat(e['timestamp']) > datetime.now() - timedelta(hours=1)]
            score -= len(recent_errors) * 5
            
            # Uyarilara gore skor dusur
            recent_warnings = [w for w in self.warning_history 
                            if datetime.fromisoformat(w['timestamp']) > datetime.now() - timedelta(hours=1)]
            score -= len(recent_warnings) * 2
            
            # Yeniden baslatmalara gore skor dusur
            score -= min(self.restart_count * 10, 50)
            
            # Skoru 0-100 arasina sinirla
            self.system_state['health_score'] = max(0, min(100, score))
            
        except Exception as e:
            logger.error(f"❌ Saglik skoru guncelleme hatasi: {e}")
    
    async def load_previous_state(self):
        """Onceki durumu yukle"""
        try:
            state_file = 'auto_restart_state.json'
            
            if os.path.exists(state_file):
                with open(state_file, 'r', encoding='utf-8') as f:
                    self.system_state = json.load(f)
                
                logger.info("✅ Onceki durum yuklendi")
                
        except Exception as e:
            logger.error(f"❌ Onceki durum yukleme hatasi: {e}")
    
    async def save_system_state(self):
        """Sistem durumunu kaydet"""
        try:
            state_file = 'auto_restart_state.json'
            
            with open(state_file, 'w', encoding='utf-8') as f:
                json.dump(self.system_state, f, ensure_ascii=False, indent=2)
                
        except Exception as e:
            logger.error(f"❌ Sistem durumu kaydetme hatasi: {e}")
    
    def get_system_status(self) -> Dict:
        """Sistem durumunu al"""
        return {
            'system_state': self.system_state,
            'shutdown_conditions': self.shutdown_conditions,
            'restart_conditions': self.restart_conditions,
            'restart_count': self.restart_count,
            'last_restart': self.last_restart,
            'error_history': self.error_history[-10:],  # Son 10 hata
            'warning_history': self.warning_history[-10:],  # Son 10 uyari
            'health_score': self.system_state['health_score']
        }

# Ana baslatici
async def main():
    """Ana fonksiyon"""
    print("""
===============================================
    TRM NIRVANA v3.0 - OTOMATIK DURMA
    VE YENIDEN BASLATMA SISTEMI
===============================================
  🔄 OTOMATIK DURMA KOSULLARI
  🚀 OTOMATIK YENIDEN BASLATMA
  📊 SISTEM SAGLIGI IZLEME
  🛑 ZARAFETLI KAPATMA
  ⏰ BELIRLI SURE SONRA DEVAM ETME
===============================================
    """)
    
    # Otomatik yeniden baslatma yoneticisi olustur
    restart_manager = AutoRestartManager()
    
    try:
        # Sistemi baslat
        if await restart_manager.initialize():
            # Sistemi izle
            await restart_manager.monitor_system()
        else:
            logger.error("❌ Otomatik yeniden baslatma sistemi baslatilamadi")
            
    except KeyboardInterrupt:
        logger.info("👋 Kullanici tarafindan durduruldu")
    except Exception as e:
        logger.error(f"❌ Ana sistem hatasi: {e}")
    finally:
        # Zarafetli kapatma
        await restart_manager.graceful_shutdown()

if __name__ == "__main__":
    asyncio.run(main())
