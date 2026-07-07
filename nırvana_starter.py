#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TRM NIRVANA STARTER v1.0
Maximum performans icin gelistirilmis baslatma sistemi
Otomatik saglik kontrolu, optimizasyon ve akilli baslatma
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
    """Nirvana baslatma sistemi"""
    
    def __init__(self):
        self.system_path = Path(__file__).parent
        self.processes = {}
        self.health_status = {}
        self.startup_time = datetime.now()
        
    async def pre_flight_checks(self) -> bool:
        """Ucus oncesi kontroller"""
        logger.info("🔍 Ucus oncesi kontroller yapiliyor...")
        
        # 1. Python versiyonu kontrolu
        if sys.version_info < (3, 8):
            logger.error("❌ Python 3.8+ gereklidir")
            return False
        
        # 2. Gerekli dosyalar kontrolu
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
        
        # 3. Secrets.env kontrolu
        if not self.check_secrets():
            logger.warning("⚠️ secrets.env yapilandirmasi eksik olabilir")
        
        # 4. Bagimlilik kontrolu
        if not await self.check_dependencies():
            logger.warning("⚠️ Bazi bagimliliklar eksik, yukleniyor...")
            await self.install_dependencies()
        
        logger.info("✅ Ucus oncesi kontroller tamamlandi")
        return True
    
    def check_secrets(self) -> bool:
        """Secrets dosyasini kontrol et"""
        try:
            secrets_file = self.system_path / 'secrets.env'
            if not secrets_file.exists():
                return False
            
            with open(secrets_file, 'r', encoding='utf-8') as f:
                content = f.read()
                # En az bir API anahtari olmali
                return any(key in content for key in ['API_KEY', 'TOKEN', 'SECRET'])
        except:
            return False
    
    async def check_dependencies(self) -> bool:
        """Bagimliliklari kontrol et"""
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
        """Bagimliliklari yukle"""
        try:
            logger.info("📦 Bagimliliklar yukleniyor...")
            process = await asyncio.create_subprocess_exec(
                sys.executable, '-m', 'pip', 'install', '-r',
                str(self.system_path / 'requirements.txt'),
                cwd=str(self.system_path),
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            stdout, stderr = await process.communicate()
            
            if process.returncode == 0:
                logger.info("✅ Bagimliliklar yuklendi")
            else:
                logger.error(f"❌ Bagimlilik yukleme hatasi: {stderr.decode()}")
        except Exception as e:
            logger.error(f"❌ Bagimlilik yukleme basarisiz: {e}")
    
    async def run_health_check(self):
        """Saglik kontrolu calistir"""
        try:
            logger.info("🏥 Saglik kontrolu yapiliyor...")
            
            # Health monitor modulunu calistir
            process = await asyncio.create_subprocess_exec(
                sys.executable, 'NIRVANA_HEALTH_MONITOR.py',
                cwd=str(self.system_path),
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            stdout, stderr = await process.communicate()
            
            if process.returncode == 0:
                logger.info("✅ Saglik kontrolu tamamlandi")
                return True
            else:
                logger.warning(f"⚠️ Saglik kontrolu uyarilari: {stderr.decode()}")
                return True
        except Exception as e:
            logger.error(f"❌ Saglik kontrolu basarisiz: {e}")
            return False
    
    async def start_core_systems(self):
        """Cekirdek sistemleri baslat"""
        logger.info("🚀 Cekirdek sistemler baslatiliyor...")
        
        # Ana orchestrator'i baslat
        try:
            process = await asyncio.create_subprocess_exec(
                sys.executable, 'run.py',
                cwd=str(self.system_path),
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            self.processes['main_orchestrator'] = process
            logger.info("✅ Ana orchestrator baslatildi")
            
        except Exception as e:
            logger.error(f"❌ Ana sistem baslatilamadi: {e}")
            return False
        
        return True
    
    async def start_monitoring(self):
        """Izleme sistemlerini baslat"""
        logger.info("📊 Izleme sistemleri baslatiliyor...")
        
        # Health monitor'u periyodik calistir
        asyncio.create_task(self.periodic_health_check())
        
        logger.info("✅ Izleme sistemleri baslatildi")
    
    async def periodic_health_check(self):
        """Periyodik saglik kontrolu"""
        while True:
            try:
                await asyncio.sleep(300)  # 5 dakikada bir
                await self.run_health_check()
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"❌ Periyodik saglik kontrolu hatasi: {e}")
    
    async def monitor_processes(self):
        """Surecleri izle"""
        while True:
            try:
                await asyncio.sleep(60)  # Her dakika
                
                for name, process in self.processes.items():
                    if process.returncode is not None:
                        logger.warning(f"⚠️ {name} sureci durdu, yeniden baslatiliyor...")
                        await self.restart_process(name)
                        
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"❌ Surec izleme hatasi: {e}")
    
    async def restart_process(self, name: str):
        """Sureci yeniden baslat"""
        try:
            if name == 'main_orchestrator':
                process = await asyncio.create_subprocess_exec(
                    sys.executable, 'run.py',
                    cwd=str(self.system_path),
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE
                )
                self.processes[name] = process
                logger.info(f"✅ {name} yeniden baslatildi")
        except Exception as e:
            logger.error(f"❌ {name} yeniden baslatilamadi: {e}")
    
    def print_startup_banner(self):
        """Baslangic banner'i yazdir"""
        banner = f"""
╔═══════════════════════════════════════════════════════════════╗
║                                                               ║
║   🚀 TRM NIRVANA STARTER v1.0                                 ║
║   Maximum Performans Otomasyon Sistemi                       ║
║                                                               ║
║   Baslatma Zamani: {self.startup_time.strftime('%d.%m.%Y %H:%M:%S')}                    ║
║   Python Versiyonu: {sys.version.split()[0]}                                ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝
        """
        print(banner)
    
    def print_status_summary(self):
        """Durum ozeti yazdir"""
        uptime = datetime.now() - self.startup_time
        summary = f"""
📊 SISTEM DURUMU
═══════════════════════════════════════════════════════════
⏱️  Calisma Suresi: {uptime}
🔄 Aktif Surecler: {len(self.processes)}
🏥 Saglik Durumu: {self.health_status.get('status', 'bilinmiyor')}
📁 Sistem Yolu: {self.system_path}
═══════════════════════════════════════════════════════════
        """
        print(summary)
    
    async def run(self):
        """Ana calisma dongusu"""
        self.print_startup_banner()
        
        # 1. Ucus oncesi kontroller
        if not await self.pre_flight_checks():
            logger.error("❌ Ucus oncesi kontroller basarisiz, baslatma iptal edildi")
            return False
        
        # 2. Saglik kontrolu
        await self.run_health_check()
        
        # 3. Cekirdek sistemleri baslat
        if not await self.start_core_systems():
            logger.error("❌ Cekirdek sistemler baslatilamadi")
            return False
        
        # 4. Izleme sistemlerini baslat
        await self.start_monitoring()
        
        # 5. Surec izleme
        await self.monitor_processes()
        
        return True
    
    async def shutdown(self):
        """Kapatma islemi"""
        logger.info("🛑 Sistem kapatiliyor...")
        
        for name, process in self.processes.items():
            try:
                process.terminate()
                await process.wait()
                logger.info(f"✅ {name} durduruldu")
            except Exception as e:
                logger.error(f"❌ {name} durdurulamadi: {e}")
        
        logger.info("✅ Sistem kapatildi")

async def main():
    """Ana fonksiyon"""
    starter = NirvanaStarter()
    
    try:
        success = await starter.run()
        if success:
            starter.print_status_summary()
            logger.info("🎉 TRM Nirvana sistemi basariyla baslatildi!")
        else:
            logger.error("❌ Sistem baslatilamadi")
            sys.exit(1)
    except KeyboardInterrupt:
        logger.info("⚠️ Kullanici tarafindan durduruldu")
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
