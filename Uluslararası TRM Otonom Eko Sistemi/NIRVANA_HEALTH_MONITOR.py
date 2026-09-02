#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TRM NIRVANA HEALTH MONITOR v1.0
Maximum performans için kapsamlı sağlık kontrolü ve otomatik iyileştirme sistemi
"""

import os
import sys
import json
import logging
import psutil
import asyncio
import platform
import subprocess
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import aiohttp
import shutil

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('nirvana_health.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class NirvanaHealthMonitor:
    """Nirvana performans seviyesi için kapsamlı sağlık monitörü"""
    
    def __init__(self):
        self.system_path = Path(__file__).parent
        self.health_report = {}
        self.performance_metrics = {}
        self.recommendations = []
        self.critical_issues = []
        
    async def full_health_check(self) -> Dict:
        """Tam sağlık kontrolü yap"""
        logger.info("🚀 Nirvana sağlık kontrolü başlatılıyor...")
        
        # Sistem kaynakları
        self.check_system_resources()
        
        # Disk alanı
        self.check_disk_space()
        
        # Python bağımlılıkları
        await self.check_dependencies()
        
        # API bağlantıları
        await self.check_api_connections()
        
        # Veritabanı sağlığı
        self.check_database_health()
        
        # Log dosyası boyutları
        self.check_log_files()
        
        # Cache temizliği
        await self.clean_cache()
        
        # Performans optimizasyonu
        await self.optimize_performance()
        
        # Rapor oluştur
        return self.generate_health_report()
    
    def check_system_resources(self):
        """Sistem kaynaklarını kontrol et"""
        try:
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            
            self.performance_metrics['cpu'] = {
                'percent': cpu_percent,
                'status': 'critical' if cpu_percent > 90 else 'warning' if cpu_percent > 70 else 'healthy'
            }
            
            self.performance_metrics['memory'] = {
                'percent': memory.percent,
                'available_gb': memory.available / (1024**3),
                'status': 'critical' if memory.percent > 90 else 'warning' if memory.percent > 70 else 'healthy'
            }
            
            self.performance_metrics['disk'] = {
                'percent': disk.percent,
                'free_gb': disk.free / (1024**3),
                'status': 'critical' if disk.percent > 90 else 'warning' if disk.percent > 80 else 'healthy'
            }
            
            if cpu_percent > 90:
                self.critical_issues.append(f"🔴 CPU kullanımı çok yüksek: %{cpu_percent}")
            elif cpu_percent > 70:
                self.recommendations.append(f"⚠️ CPU kullanımı yüksek: %{cpu_percent}")
                
            if memory.percent > 90:
                self.critical_issues.append(f"🔴 RAM kullanımı çok yüksek: %{memory.percent}")
            elif memory.percent > 70:
                self.recommendations.append(f"⚠️ RAM kullanımı yüksek: %{memory.percent}")
                
            logger.info(f"💻 CPU: %{cpu_percent}, RAM: %{memory.percent}, Disk: %{disk.percent}")
            
        except Exception as e:
            logger.error(f"❌ Sistem kaynakları kontrol edilemedi: {e}")
            self.critical_issues.append(f"❌ Sistem kaynakları kontrol hatası: {e}")
    
    def check_disk_space(self):
        """Disk alanını detaylı kontrol et"""
        try:
            critical_paths = [
                self.system_path,
                self.system_path / 'logs',
                self.system_path / 'data',
                self.system_path / 'temp_docs',
                self.system_path / 'temp_photos'
            ]
            
            for path in critical_paths:
                if path.exists():
                    usage = shutil.disk_usage(path)
                    free_gb = usage.free / (1024**3)
                    
                    if free_gb < 1:
                        self.critical_issues.append(f"🔴 {path} dizininde kalan alan kritik: {free_gb:.2f} GB")
                    elif free_gb < 5:
                        self.recommendations.append(f"⚠️ {path} dizininde az alan: {free_gb:.2f} GB")
                        
        except Exception as e:
            logger.error(f"❌ Disk alanı kontrol edilemedi: {e}")
    
    async def check_dependencies(self):
        """Python bağımlılıklarını kontrol et"""
        try:
            required_packages = [
                'requests', 'aiohttp', 'telethon', 'openai', 'google-api-python-client',
                'google-auth-oauthlib', 'psutil', 'pillow', 'tweepy', 'beautifulsoup4'
            ]
            
            missing_packages = []
            for package in required_packages:
                try:
                    __import__(package.replace('-', '_'))
                except ImportError:
                    missing_packages.append(package)
            
            if missing_packages:
                self.critical_issues.append(f"🔴 Eksik paketler: {', '.join(missing_packages)}")
                self.recommendations.append(f"💡 Çözüm: pip install {' '.join(missing_packages)}")
            else:
                logger.info("✅ Tüm paketler yüklü")
                
        except Exception as e:
            logger.error(f"❌ Bağımlılık kontrolü başarısız: {e}")
    
    async def check_api_connections(self):
        """API bağlantılarını test et"""
        try:
            test_urls = {
                'Google': 'https://www.googleapis.com',
                'OpenAI': 'https://api.openai.com',
                'Telegram': 'https://api.telegram.org',
                'Trendyol': 'https://www.trendyol.com'
            }
            
            async with aiohttp.ClientSession() as session:
                for name, url in test_urls.items():
                    try:
                        async with session.get(url, timeout=aiohttp.ClientTimeout(total=10)) as response:
                            if response.status == 200:
                                logger.info(f"✅ {name} API erişilebilir")
                            else:
                                self.recommendations.append(f"⚠️ {name} API durumu: {response.status}")
                    except Exception as e:
                        self.recommendations.append(f"⚠️ {name} API erişim hatası: {e}")
                        
        except Exception as e:
            logger.error(f"❌ API bağlantı kontrolü başarısız: {e}")
    
    def check_database_health(self):
        """Veritabanı sağlığını kontrol et"""
        try:
            db_files = list(self.system_path.glob('*.db')) + list(self.system_path.glob('data/*.db'))
            
            for db_file in db_files:
                if db_file.exists():
                    size_mb = db_file.stat().st_size / (1024**2)
                    if size_mb > 100:
                        self.recommendations.append(f"⚠️ {db_file.name} boyutu büyük: {size_mb:.2f} MB")
                    logger.info(f"📊 {db_file.name}: {size_mb:.2f} MB")
                    
        except Exception as e:
            logger.error(f"❌ Veritabanı kontrolü başarısız: {e}")
    
    def check_log_files(self):
        """Log dosyalarını kontrol et"""
        try:
            log_files = list(self.system_path.glob('*.log')) + list(self.system_path.glob('logs/*.log'))
            
            for log_file in log_files:
                if log_file.exists():
                    size_mb = log_file.stat().st_size / (1024**2)
                    if size_mb > 10:
                        self.recommendations.append(f"⚠️ {log_file.name} boyutu büyük: {size_mb:.2f} MB - temizleme önerilir")
                        # Otomatik temizlik
                        self.rotate_log_file(log_file)
                        
        except Exception as e:
            logger.error(f"❌ Log dosyası kontrolü başarısız: {e}")
    
    def rotate_log_file(self, log_file: Path):
        """Log dosyasını döndür"""
        try:
            backup_file = log_file.with_suffix('.log.1')
            if backup_file.exists():
                backup_file.unlink()
            shutil.move(str(log_file), str(backup_file))
            logger.info(f"🔄 Log dosyası döndürüldü: {log_file.name}")
        except Exception as e:
            logger.error(f"❌ Log döndürme başarısız: {e}")
    
    async def clean_cache(self):
        """Cache dosyalarını temizle"""
        try:
            cache_dirs = [
                self.system_path / '__pycache__',
                self.system_path / 'temp_docs',
                self.system_path / 'temp_photos'
            ]
            
            cleaned_size = 0
            for cache_dir in cache_dirs:
                if cache_dir.exists():
                    size_before = sum(f.stat().st_size for f in cache_dir.rglob('*') if f.is_file())
                    shutil.rmtree(cache_dir, ignore_errors=True)
                    cache_dir.mkdir(exist_ok=True)
                    cleaned_size += size_before
                    logger.info(f"🧹 {cache_dir.name} temizlendi: {size_before / (1024**2):.2f} MB")
            
            if cleaned_size > 0:
                self.recommendations.append(f"✅ Cache temizlendi: {cleaned_size / (1024**2):.2f} MB")
                
        except Exception as e:
            logger.error(f"❌ Cache temizliği başarısız: {e}")
    
    async def optimize_performance(self):
        """Performans optimizasyonu"""
        try:
            # Python cache temizliği
            pycache_dirs = list(self.system_path.rglob('__pycache__'))
            for pycache in pycache_dirs:
                if pycache.is_dir():
                    shutil.rmtree(pycache, ignore_errors=True)
            
            # Eski JSON dosyalarını temizle
            json_files = list(self.system_path.glob('*.json'))
            for json_file in json_files:
                if json_file.name in ['scraped_products_queue.json', 'product_queue.json']:
                    if json_file.stat().st_size < 100:  # Boş veya çok küçük dosyalar
                        json_file.unlink()
                        logger.info(f"🗑️ Küçük JSON dosyası silindi: {json_file.name}")
            
            self.recommendations.append("✅ Performans optimizasyonu tamamlandı")
            
        except Exception as e:
            logger.error(f"❌ Performans optimizasyonu başarısız: {e}")
    
    def generate_health_report(self) -> Dict:
        """Sağlık raporu oluştur"""
        report = {
            'timestamp': datetime.now().isoformat(),
            'status': 'critical' if self.critical_issues else 'warning' if self.recommendations else 'healthy',
            'performance_metrics': self.performance_metrics,
            'critical_issues': self.critical_issues,
            'recommendations': self.recommendations,
            'system_info': {
                'platform': platform.system(),
                'python_version': sys.version,
                'cpu_count': psutil.cpu_count()
            }
        }
        
        # Raporu kaydet
        report_file = self.system_path / 'nirvana_health_report.json'
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        logger.info(f"📋 Sağlık raporu kaydedildi: {report_file}")
        return report
    
    def print_summary(self):
        """Özet rapor yazdır"""
        print("\n" + "="*60)
        print("🚀 TRM NIRVANA HEALTH MONITOR - ÖZET RAPOR")
        print("="*60)
        
        if self.critical_issues:
            print("\n🔴 KRİTİK SORUNLAR:")
            for issue in self.critical_issues:
                print(f"  {issue}")
        
        if self.recommendations:
            print("\n⚠️ ÖNERİLER:")
            for rec in self.recommendations:
                print(f"  {rec}")
        
        if not self.critical_issues and not self.recommendations:
            print("\n✅ Sistem mükemmel durumda!")
        
        print("\n📊 PERFORMANS METRİKLERİ:")
        for metric, data in self.performance_metrics.items():
            status_emoji = "🔴" if data['status'] == 'critical' else "⚠️" if data['status'] == 'warning' else "✅"
            print(f"  {status_emoji} {metric.upper()}: {data}")
        
        print("\n" + "="*60)

async def main():
    """Ana fonksiyon"""
    monitor = NirvanaHealthMonitor()
    await monitor.full_health_check()
    monitor.print_summary()

if __name__ == "__main__":
    asyncio.run(main())
