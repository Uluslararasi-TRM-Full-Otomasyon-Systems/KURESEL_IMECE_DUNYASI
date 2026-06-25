#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TRM NIRVANA STARTER v1.0
Maximum performans için geliştirilmiş başlatma sistemi
Otomatik sağlık kontrolü, optimizasyon ve akıllı başlatma
"""

import os
import sys
import time
import logging
import asyncio
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

# Sistem yolu ekle
system_path = Path(__file__).parent
sys.path.insert(0, str(system_path))

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(system_path / 'nirvana_starter.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class NirvanaStarter:
    """Nirvana başlatma sistemi"""
    
    def __init__(self):
        self.system_path = Path(__file__).parent
        self.processes = {}
        self.health_status = {}
        self.startup_time = datetime.now()
        
    async def pre_flight_checks(self) -> bool:
        """Uçuş öncesi kontroller"""
        logger.info("🔍 Uçuş öncesi kontroller yapılıyor...")
        
        # 1. Python versiyonu kontrolü
        if sys.version_info < (3, 8):
            logger.error("❌ Python 3.8+ gereklidir")
            return False
        
        # 2. Gerekli dosyalar kontrolü
        required_files = [
            'config.py',
            'secrets.env',
            'requirements.txt',
            'run.py'
        ]
        
        for file in required_files:
            if not (self.system_path / file).exists():
                logger.error(f"❌ Gerekli dosya eksik: {file}")
                return False
        
        logger.info("✅ Gerekli dosyalar mevcut")
        
        # 3. Secrets.env kontrolü
        if not self.check_secrets():
            logger.warning("⚠️ secrets.env yapılandırması eksik olabilir")
        
        # 4. Bağımlılık kontrolü
        if not await self.check_dependencies():
            logger.warning("⚠️ Bazı bağımlılıklar eksik, yükleniyor...")
            await self.install_dependencies()
        
        logger.info("✅ Uçuş öncesi kontroller tamamlandı")
        return True
    
    def check_secrets(self) -> bool:
        """Secrets dosyasını kontrol et"""
        try:
            secrets_file = self.system_path / 'secrets.env'
            if not secrets_file.exists():
                return False
            
            with open(secrets_file, 'r', encoding='utf-8') as f:
                content = f.read()
                # En az bir API anahtarı olmalı
                return any(key in content for key in ['API_KEY', 'TOKEN', 'SECRET'])
        except:
            return False
    
    async def check_dependencies(self) -> bool:
        """Bağımlılıkları kontrol et"""
        try:
            import importlib
            required = ['requests', 'aiohttp', 'telethon']
            
            for package in required:
                try:
                    importlib.import_module(package)
                except ImportError:
                    return False
            
            return True
        except:
            return False
    
    async def install_dependencies(self):
        """Bağımlılıkları yükle"""
        try:
            logger.info("📦 Bağımlılıklar yükleniyor...")
            process = await asyncio.create_subprocess_exec(
                sys.executable, '-m', 'pip', 'install', '-r',
                str(self.system_path / 'requirements.txt'),
                cwd=str(self.system_path),
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            stdout, stderr = await process.communicate()
            
            if process.returncode == 0:
                logger.info("✅ Bağımlılıklar yüklendi")
            else:
                logger.error(f"❌ Bağımlılık yükleme hatası: {stderr.decode()}")
        except Exception as e:
            logger.error(f"❌ Bağımlılık yükleme başarısız: {e}")
    
    async def run_health_check(self):
        """Sağlık kontrolü çalıştır"""
        try:
            logger.info("🏥 Sağlık kontrolü yapılıyor...")
            
            # Health monitor modülünü çalıştır
            process = await asyncio.create_subprocess_exec(
                sys.executable, 'NIRVANA_HEALTH_MONITOR.py',
                cwd=str(self.system_path),
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            stdout, stderr = await process.communicate()
            
            if process.returncode == 0:
                logger.info("✅ Sağlık kontrolü tamamlandı")
                return True
            else:
                logger.warning(f"⚠️ Sağlık kontrolü uyarıları: {stderr.decode()}")
                return True
        except Exception as e:
            logger.error(f"❌ Sağlık kontrolü başarısız: {e}")
            return False
    
    async def start_core_systems(self):
        """Çekirdek sistemleri başlat"""
        logger.info("🚀 Çekirdek sistemler başlatılıyor...")
        
        # Ana orchestrator'ı başlat
        try:
            process = await asyncio.create_subprocess_exec(
                sys.executable, 'run.py',
                cwd=str(self.system_path),
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            self.processes['main_orchestrator'] = process
            logger.info("✅ Ana orchestrator başlatıldı")
            
        except Exception as e:
            logger.error(f"❌ Ana sistem başlatılamadı: {e}")
            return False
        
        return True
    
    async def start_monitoring(self):
        """İzleme sistemlerini başlat"""
        logger.info("📊 İzleme sistemleri başlatılıyor...")
        
        # Health monitor'ü periyodik çalıştır
        asyncio.create_task(self.periodic_health_check())
        
        logger.info("✅ İzleme sistemleri başlatıldı")
    
    async def periodic_health_check(self):
        """Periyodik sağlık kontrolü"""
        while True:
            try:
                await asyncio.sleep(300)  # 5 dakikada bir
                await self.run_health_check()
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"❌ Periyodik sağlık kontrolü hatası: {e}")
    
    async def monitor_processes(self):
        """Süreçleri izle"""
        while True:
            try:
                await asyncio.sleep(60)  # Her dakika
                
                for name, process in self.processes.items():
                    if process.returncode is not None:
                        logger.warning(f"⚠️ {name} süreci durdu, yeniden başlatılıyor...")
                        await self.restart_process(name)
                        
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"❌ Süreç izleme hatası: {e}")
    
    async def restart_process(self, name: str):
        """Süreci yeniden başlat"""
        try:
            if name == 'main_orchestrator':
                process = await asyncio.create_subprocess_exec(
                    sys.executable, 'run.py',
                    cwd=str(self.system_path),
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE
                )
                self.processes[name] = process
                logger.info(f"✅ {name} yeniden başlatıldı")
        except Exception as e:
            logger.error(f"❌ {name} yeniden başlatılamadı: {e}")
    
    def print_startup_banner(self):
        """Başlangıç banner'ı yazdır"""
        banner = f"""
╔═══════════════════════════════════════════════════════════════╗
║                                                               ║
║   🚀 TRM NIRVANA STARTER v1.0                                 ║
║   Maximum Performans Otomasyon Sistemi                       ║
║                                                               ║
║   Başlatma Zamanı: {self.startup_time.strftime('%d.%m.%Y %H:%M:%S')}                    ║
║   Python Versiyonu: {sys.version.split()[0]}                                ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝
        """
        print(banner)
    
    def print_status_summary(self):
        """Durum özeti yazdır"""
        uptime = datetime.now() - self.startup_time
        summary = f"""
📊 SİSTEM DURUMU
═══════════════════════════════════════════════════════════
⏱️  Çalışma Süresi: {uptime}
🔄 Aktif Süreçler: {len(self.processes)}
🏥 Sağlık Durumu: {self.health_status.get('status', 'bilinmiyor')}
📁 Sistem Yolu: {self.system_path}
═══════════════════════════════════════════════════════════
        """
        print(summary)
    
    async def run(self):
        """Ana çalışma döngüsü"""
        self.print_startup_banner()
        
        # 1. Uçuş öncesi kontroller
        if not await self.pre_flight_checks():
            logger.error("❌ Uçuş öncesi kontroller başarısız, başlatma iptal edildi")
            return False
        
        # 2. Sağlık kontrolü
        await self.run_health_check()
        
        # 3. Çekirdek sistemleri başlat
        if not await self.start_core_systems():
            logger.error("❌ Çekirdek sistemler başlatılamadı")
            return False
        
        # 4. İzleme sistemlerini başlat
        await self.start_monitoring()
        
        # 5. Süreç izleme
        await self.monitor_processes()
        
        return True
    
    async def shutdown(self):
        """Kapatma işlemi"""
        logger.info("🛑 Sistem kapatılıyor...")
        
        for name, process in self.processes.items():
            try:
                process.terminate()
                await process.wait()
                logger.info(f"✅ {name} durduruldu")
            except Exception as e:
                logger.error(f"❌ {name} durdurulamadı: {e}")
        
        logger.info("✅ Sistem kapatıldı")

async def main():
    """Ana fonksiyon"""
    starter = NirvanaStarter()
    
    try:
        success = await starter.run()
        if success:
            starter.print_status_summary()
            logger.info("🎉 TRM Nirvana sistemi başarıyla başlatıldı!")
        else:
            logger.error("❌ Sistem başlatılamadı")
            sys.exit(1)
    except KeyboardInterrupt:
        logger.info("⚠️ Kullanıcı tarafından durduruldu")
    except Exception as e:
        logger.error(f"❌ Kritik hata: {e}")
        sys.exit(1)
    finally:
        await starter.shutdown()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n⚠️ Program durduruldu")
        sys.exit(0)
