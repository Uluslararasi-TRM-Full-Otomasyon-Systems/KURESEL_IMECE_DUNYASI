#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TRM Nirvana v3.0 - Otomatik Durma ve Yeniden Başlatma Mekanizması
Sistem hangi durumlarda otomatik olarak duracağını, hangi durumlarda 
kendini yeniden başlatacağını ve belirli bir süre sonra otomatik 
olarak tekrar çalışmaya devam edip etmeyeceğini yönetir
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
        
        # Otomatik durma koşulları
        self.shutdown_conditions = {
            'critical_errors': 10,           # Kritik hata sayısı
            'memory_threshold': 95,           # Bellek kullanım eşiği (%)
            'cpu_threshold': 98,               # CPU kullanım eşiği (%)
            'disk_space_threshold': 5,          # Disk alanı eşiği (GB)
            'network_timeout': 300,            # Ağ zaman aşımı (saniye)
            'consecutive_failures': 5,         # Art arda hata sayısı
            'max_uptime_hours': 168,          # Maksimum çalışma süresi (7 gün)
            'manual_shutdown': False            # Manuel kapatma
        }
        
        # Otomatik yeniden başlatma koşulları
        self.restart_conditions = {
            'error_threshold': 3,              # Hata eşiği
            'error_window': 300,               # Hata penceresi (saniye)
            'warning_threshold': 10,            # Uyarı eşiği
            'memory_restart_threshold': 90,      # Bellek yeniden başlatma eşiği
            'cpu_restart_threshold': 85,         # CPU yeniden başlatma eşiği
            'auto_restart_enabled': True,        # Otomatik yeniden başlatma aktif
            'restart_delay': 60,                # Yeniden başlatma gecikmesi (saniye)
            'max_restarts_per_hour': 3,         # Saatte maksimum yeniden başlatma
            'graceful_shutdown_timeout': 30     # Zarafetli kapatma zaman aşımı
        }
        
        # Çalışma durumu
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
        """Otomatik yeniden başlatma sistemini başlat"""
        try:
            logger.info("🔄 Otomatik Durma ve Yeniden Başlatma Sistemi Başlatılıyor...")
            
            # Log dizinini oluştur
            os.makedirs('logs', exist_ok=True)
            
            # Önceki durumu yükle
            await self.load_previous_state()
            
            self.running = True
            self.system_state['status'] = 'starting'
            self.system_state['last_check'] = datetime.now().isoformat()
            
            logger.info("✅ Otomatik yeniden başlatma sistemi başlatıldı")
            return True
            
        except Exception as e:
            logger.error(f"❌ Otomatik yeniden başlatma sistemi başlatma hatası: {e}")
            return False
    
    async def monitor_system(self):
        """Sistemi izle"""
        try:
            while self.running:
                current_time = datetime.now()
                
                # Sistem durumunu güncelle
                await self.update_system_status()
                
                # Otomatik durma koşullarını kontrol et
                shutdown_reason = await self.check_shutdown_conditions()
                
                if shutdown_reason:
                    logger.warning(f"⚠️ Otomatik durma koşulu: {shutdown_reason}")
                    await self.initiate_shutdown(shutdown_reason)
                    break
                
                # Otomatik yeniden başlatma koşullarını kontrol et
                restart_reason = await self.check_restart_conditions()
                
                if restart_reason:
                    logger.info(f"🔄 Otomatik yeniden başlatma koşulu: {restart_reason}")
                    await self.initiate_restart(restart_reason)
                
                # Belirli süre sonra devam etme kontrolü
                await self.check_continuation_conditions()
                
                # Sağlık skorunu güncelle
                await self.update_health_score()
                
                # Durumu kaydet
                await self.save_system_state()
                
                # İzleme aralığında bekle
                await asyncio.sleep(30)  # 30 saniye
                
        except Exception as e:
            logger.error(f"❌ Sistem izleme hatası: {e}")
            self.error_history.append({
                'timestamp': datetime.now().isoformat(),
                'error': str(e),
                'type': 'monitoring'
            })
    
    async def check_shutdown_conditions(self) -> Optional[str]:
        """Otomatik durma koşullarını kontrol et"""
        try:
            # Kritik hata sayısı kontrolü
            recent_errors = [e for e in self.error_history 
                           if datetime.fromisoformat(e['timestamp']) > datetime.now() - timedelta(hours=1)]
            
            if len(recent_errors) >= self.shutdown_conditions['critical_errors']:
                return f"Kritik hata sayısı aşıldı: {len(recent_errors)}"
            
            # Bellek kullanımı kontrolü
            memory = psutil.virtual_memory()
            if memory.percent >= self.shutdown_conditions['memory_threshold']:
                return f"Bellek kullanımı kritik seviyede: {memory.percent}%"
            
            # CPU kullanımı kontrolü
            cpu_usage = psutil.cpu_percent(interval=1)
            if cpu_usage >= self.shutdown_conditions['cpu_threshold']:
                return f"CPU kullanımı kritik seviyede: {cpu_usage}%"
            
            # Disk alanı kontrolü
            disk = psutil.disk_usage('/')
            free_gb = disk.free / (1024**3)
            if free_gb <= self.shutdown_conditions['disk_space_threshold']:
                return f"Disk alanı kritik seviyede: {free_gb:.1f}GB"
            
            # Art arda hata kontrolü
            consecutive_errors = await self.check_consecutive_failures()
            if consecutive_errors >= self.shutdown_conditions['consecutive_failures']:
                return f"Art arda hata sayısı: {consecutive_errors}"
            
            # Maksimum çalışma süresi kontrolü
            if self.system_state['uptime'] >= self.shutdown_conditions['max_uptime_hours'] * 3600:
                return f"Maksimum çalışma süresi aşıldı: {self.system_state['uptime']}saniye"
            
            return None
            
        except Exception as e:
            logger.error(f"❌ Durma koşulu kontrolü hatası: {e}")
            return None
    
    async def check_restart_conditions(self) -> Optional[str]:
        """Otomatik yeniden başlatma koşullarını kontrol et"""
        try:
            if not self.restart_conditions['auto_restart_enabled']:
                return None
            
            # Hata eşiği kontrolü
            recent_errors = [e for e in self.error_history 
                           if datetime.fromisoformat(e['timestamp']) > datetime.now() - timedelta(seconds=self.restart_conditions['error_window'])]
            
            if len(recent_errors) >= self.restart_conditions['error_threshold']:
                return f"Hata eşiği aşıldı: {len(recent_errors)}"
            
            # Bellek yeniden başlatma eşiği
            memory = psutil.virtual_memory()
            if memory.percent >= self.restart_conditions['memory_restart_threshold']:
                return f"Bellek kullanımı yeniden başlatma eşiğinde: {memory.percent}%"
            
            # CPU yeniden başlatma eşiği
            cpu_usage = psutil.cpu_percent(interval=1)
            if cpu_usage >= self.restart_conditions['cpu_restart_threshold']:
                return f"CPU kullanımı yeniden başlatma eşiğinde: {cpu_usage}%"
            
            # Saatte maksimum yeniden başlatma kontrolü
            recent_restarts = [r for r in self.error_history 
                              if datetime.fromisoformat(r['timestamp']) > datetime.now() - timedelta(hours=1)]
            
            if len(recent_restarts) >= self.restart_conditions['max_restarts_per_hour']:
                return f"Saatte maksimum yeniden başlatma aşıldı: {len(recent_restarts)}"
            
            return None
            
        except Exception as e:
            logger.error(f"❌ Yeniden başlatma koşulu kontrolü hatası: {e}")
            return None
    
    async def check_consecutive_failures(self) -> int:
        """Art arda hata sayısını kontrol et"""
        try:
            consecutive_count = 0
            current_time = datetime.now()
            
            # Son 1 saatlik hataları kontrol et
            recent_errors = sorted([e for e in self.error_history 
                                if datetime.fromisoformat(e['timestamp']) > current_time - timedelta(hours=1)],
                               key=lambda x: datetime.fromisoformat(x['timestamp']))
            
            for error in recent_errors:
                error_time = datetime.fromisoformat(error['timestamp'])
                time_diff = (current_time - error_time).total_seconds()
                
                if time_diff <= 300:  # 5 dakika içinde
                    consecutive_count += 1
                else:
                    break
            
            return consecutive_count
            
        except Exception as e:
            logger.error(f"❌ Art arda hata kontrolü hatası: {e}")
            return 0
    
    async def check_continuation_conditions(self):
        """Belirli süre sonra devam etme koşullarını kontrol et"""
        try:
            # Sistem durumuna göre devam etme kararı
            if self.system_state['status'] == 'restarting':
                # Yeniden başlatma durumunda 1 dakika bekle
                if datetime.now() > datetime.fromisoformat(self.system_state['next_restart_time']):
                    self.system_state['status'] = 'running'
                    logger.info("✅ Sistem yeniden başlatıldı, normale dönüldü")
            
            elif self.system_state['status'] == 'shutdown':
                # Kapatma durumunda devam etme
                logger.info("⏹️ Sistem kapatıldı, devam etmiyor")
                self.running = False
                
        except Exception as e:
            logger.error(f"❌ Devam etme koşulu kontrolü hatası: {e}")
    
    async def initiate_shutdown(self, reason: str):
        """Otomatik kapatmayı başlat"""
        try:
            logger.info(f"⏹️ Otomatik kapatma başlatılıyor: {reason}")
            
            self.system_state['status'] = 'shutdown'
            self.system_state['last_shutdown_reason'] = reason
            self.system_state['last_check'] = datetime.now().isoformat()
            
            # Kapatma bildirimi gönder
            await self.send_shutdown_notification(reason)
            
            # Zarafetli kapatma
            await self.graceful_shutdown()
            
        except Exception as e:
            logger.error(f"❌ Otomatik kapatma hatası: {e}")
    
    async def initiate_restart(self, reason: str):
        """Otomatik yeniden başlatmayı başlat"""
        try:
            logger.info(f"🔄 Otomatik yeniden başlatma başlatılıyor: {reason}")
            
            self.system_state['status'] = 'restarting'
            self.system_state['last_restart'] = datetime.now().isoformat()
            self.system_state['next_restart_time'] = (datetime.now() + timedelta(seconds=self.restart_conditions['restart_delay'])).isoformat()
            self.system_state['total_restarts'] += 1
            self.restart_count += 1
            
            # Yeniden başlatma bildirimi gönder
            await self.send_restart_notification(reason)
            
            # Zarafetli yeniden başlatma
            await self.graceful_restart()
            
        except Exception as e:
            logger.error(f"❌ Otomatik yeniden başlatma hatası: {e}")
    
    async def graceful_shutdown(self):
        """Zarafetli kapatma"""
        try:
            logger.info("🛑 Zarafetli kapatma başlatılıyor...")
            
            # Tüm process'leri durdur
            # Burada ana orchestrator ve diğer modüller durdurulacak
            
            # Kaydetme işlemleri
            await self.save_system_state()
            
            self.system_state['status'] = 'stopped'
            logger.info("✅ Zarafetli kapatma tamamlandı")
            
        except Exception as e:
            logger.error(f"❌ Zarafetli kapatma hatası: {e}")
    
    async def graceful_restart(self):
        """Zarafetli yeniden başlatma"""
        try:
            logger.info("🔄 Zarafetli yeniden başlatma başlatılıyor...")
            
            # Zarafetli kapatma
            await self.graceful_shutdown()
            
            # Bekle
            await asyncio.sleep(self.restart_conditions['restart_delay'])
            
            # Sistemi yeniden başlat
            # Burada ana orchestrator ve diğer modüller başlatılacak
            
            self.system_state['status'] = 'running'
            logger.info("✅ Zarafetli yeniden başlatma tamamlandı")
            
        except Exception as e:
            logger.error(f"❌ Zarafetli yeniden başlatma hatası: {e}")
    
    async def send_shutdown_notification(self, reason: str):
        """Kapatma bildirimi gönder"""
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
            
            logger.info(f"📢 Kapatma bildirimi gönderildi: {reason}")
            
        except Exception as e:
            logger.error(f"❌ Kapatma bildirimi gönderme hatası: {e}")
    
    async def send_restart_notification(self, reason: str):
        """Yeniden başlatma bildirimi gönder"""
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
            
            logger.info(f"📢 Yeniden başlatma bildirimi gönderildi: {reason}")
            
        except Exception as e:
            logger.error(f"❌ Yeniden başlatma bildirimi gönderme hatası: {e}")
    
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
            logger.error(f"❌ Bildirim kaydetme hatası: {e}")
    
    async def update_system_status(self):
        """Sistem durumunu güncelle"""
        try:
            current_time = datetime.now()
            
            # Uptime güncelle
            if self.system_state['status'] == 'running':
                self.system_state['uptime'] += 30  # 30 saniye ekle
            
            self.system_state['last_check'] = current_time.isoformat()
            
        except Exception as e:
            logger.error(f"❌ Sistem durumu güncelleme hatası: {e}")
    
    async def update_health_score(self):
        """Sağlık skorunu güncelle"""
        try:
            score = 100
            
            # Hatalara göre skor düşür
            recent_errors = [e for e in self.error_history 
                           if datetime.fromisoformat(e['timestamp']) > datetime.now() - timedelta(hours=1)]
            score -= len(recent_errors) * 5
            
            # Uyarılara göre skor düşür
            recent_warnings = [w for w in self.warning_history 
                            if datetime.fromisoformat(w['timestamp']) > datetime.now() - timedelta(hours=1)]
            score -= len(recent_warnings) * 2
            
            # Yeniden başlatmalara göre skor düşür
            score -= min(self.restart_count * 10, 50)
            
            # Skoru 0-100 arasına sınırla
            self.system_state['health_score'] = max(0, min(100, score))
            
        except Exception as e:
            logger.error(f"❌ Sağlık skoru güncelleme hatası: {e}")
    
    async def load_previous_state(self):
        """Önceki durumu yükle"""
        try:
            state_file = 'auto_restart_state.json'
            
            if os.path.exists(state_file):
                with open(state_file, 'r', encoding='utf-8') as f:
                    self.system_state = json.load(f)
                
                logger.info("✅ Önceki durum yüklendi")
                
        except Exception as e:
            logger.error(f"❌ Önceki durum yükleme hatası: {e}")
    
    async def save_system_state(self):
        """Sistem durumunu kaydet"""
        try:
            state_file = 'auto_restart_state.json'
            
            with open(state_file, 'w', encoding='utf-8') as f:
                json.dump(self.system_state, f, ensure_ascii=False, indent=2)
                
        except Exception as e:
            logger.error(f"❌ Sistem durumu kaydetme hatası: {e}")
    
    def get_system_status(self) -> Dict:
        """Sistem durumunu al"""
        return {
            'system_state': self.system_state,
            'shutdown_conditions': self.shutdown_conditions,
            'restart_conditions': self.restart_conditions,
            'restart_count': self.restart_count,
            'last_restart': self.last_restart,
            'error_history': self.error_history[-10:],  # Son 10 hata
            'warning_history': self.warning_history[-10:],  # Son 10 uyarı
            'health_score': self.system_state['health_score']
        }

# Ana başlatıcı
async def main():
    """Ana fonksiyon"""
    print("""
===============================================
    TRM NIRVANA v3.0 - OTOMATİK DURMA
    VE YENİDEN BAŞLATMA SİSTEMİ
===============================================
  🔄 OTOMATİK DURMA KOŞULLARI
  🚀 OTOMATİK YENİDEN BAŞLATMA
  📊 SİSTEM SAĞLIĞI İZLEME
  🛑 ZARAFETLİ KAPATMA
  ⏰ BELİRLİ SÜRE SONRA DEVAM ETME
===============================================
    """)
    
    # Otomatik yeniden başlatma yöneticisi oluştur
    restart_manager = AutoRestartManager()
    
    try:
        # Sistemi başlat
        if await restart_manager.initialize():
            # Sistemi izle
            await restart_manager.monitor_system()
        else:
            logger.error("❌ Otomatik yeniden başlatma sistemi başlatılamadı")
            
    except KeyboardInterrupt:
        logger.info("👋 Kullanıcı tarafından durduruldu")
    except Exception as e:
        logger.error(f"❌ Ana sistem hatası: {e}")
    finally:
        # Zarafetli kapatma
        await restart_manager.graceful_shutdown()

if __name__ == "__main__":
    asyncio.run(main())
