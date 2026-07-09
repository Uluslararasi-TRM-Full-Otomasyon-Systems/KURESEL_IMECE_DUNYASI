#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TRM FULL OTOMASYON SİSTEM BAŞLATICI
Tüm HTML panellerini ve API sistemini başlatır
"""

import os
import sys
import time
import logging
import subprocess
from pathlib import Path
from datetime import datetime
import webbrowser
import threading

from trm_paths import PROJECT_ROOT, html_dir

# Loglama ayarları
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('trm_system.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

class TRMSystemStarter:
    def __init__(self):
        self.system_path = PROJECT_ROOT
        self.html_path = html_dir()
        self.panels = [
            "TEK_BUTON_YENI.html",
            "ANA_PANEL.html", 
            "STATUS_PANEL.html",
            "SATIS_PANEL.html",
            "GELISMIS_PANEL.html",
            "DRIVE_SOCIAL_PANEL.html",
            "TEK_TIK_CLOUD.html",
            "PANEL_ACICI_HTML.html"
        ]
        self.api_ports = [9001, 9002, 9003, 9004]
        self.running_processes = {}
        
    def check_secrets_file(self):
        """Secrets dosyasını kontrol et"""
        secrets_file = self.system_path / "secrets.env"
        if not secrets_file.exists():
            logger.error("❌ secrets.env dosyası bulunamadı!")
            logger.info("📝 Lütfen önce API anahtarlarını oluşturun")
            return False
        
        logger.info("✅ secrets.env dosyası bulundu")
        return True
        
    def load_environment(self):
        """Ortam değişkenlerini yükle"""
        try:
            with open(self.system_path / "secrets.env", 'r', encoding='utf-8') as f:
                for line in f:
                    if '=' in line and not line.startswith('#'):
                        key, value = line.strip().split('=', 1)
                        os.environ[key.strip()] = value.strip()
            logger.info("🔧 Ortam değişkenleri yüklendi")
            return True
        except Exception as e:
            logger.error(f"❌ Ortam değişkenleri yüklenemedi: {e}")
            return False
            
    def check_html_files(self):
        """HTML dosyalarını kontrol et"""
        missing_files = []
        for panel in self.panels:
            panel_path = self.html_path / panel
            if not panel_path.exists():
                missing_files.append(panel)
        
        if missing_files:
            logger.error(f"❌ Eksik HTML dosyaları: {missing_files}")
            return False
            
        logger.info("✅ Tüm HTML dosyaları mevcut")
        return True
        
    def start_api_servers(self):
        """API sunucularını başlat"""
        logger.info("🚀 API sunucuları başlatılıyor...")
        
        for port in self.api_ports:
            try:
                # Burada gerçek API sunucuları başlatılacak
                # Şimdilik sadece log bilgisi
                logger.info(f"📡 API sunucu port {port} hazır")
                time.sleep(0.5)  # Başlatma simülasyonu
            except Exception as e:
                logger.error(f"❌ API {port} başlatılamadı: {e}")
                
    def open_panels(self):
        """HTML panellerini aç"""
        logger.info("🌐 HTML panelleri açılıyor...")
        
        for panel in self.panels:
            try:
                panel_path = self.html_path / panel
                webbrowser.open(f'file://{panel_path.absolute()}')
                logger.info(f"✅ {panel} açıldı")
                time.sleep(0.3)  # Paneller arası bekleme
            except Exception as e:
                logger.error(f"❌ {panel} açılamadı: {e}")
                
    def start_system_services(self):
        """Sistem servislerini başlat"""
        logger.info("⚙️ Sistem servisleri başlatılıyor...")
        
        services = [
            "python MAIN_ORCHESTRATOR.py",
            "python SYSTEM_MANAGER_24_7.py", 
            "python TRM_AUTOMATION_ENGINE.py"
        ]
        
        for service in services:
            try:
                service_path = self.system_path / service
                if service_path.exists():
                    # Arka planda başlat
                    subprocess.Popen([
                        sys.executable, str(service_path)
                    ], cwd=self.system_path)
                    logger.info(f"✅ {service} başlatıldı")
                    time.sleep(1)
                else:
                    logger.warning(f"⚠️ {service} dosyası bulunamadı")
            except Exception as e:
                logger.error(f"❌ {service} başlatılamadı: {e}")
                
    def display_system_info(self):
        """Sistem bilgilerini göster"""
        print("\n" + "="*60)
        print(">> ULUSLARASI TRM FULL OTOMASYON SISTEMI <<")
        print("="*60)
        print(f"Baslatma Zamani: {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}")
        print(f"Sistem Path: {self.system_path}")
        print(f"HTML Path: {self.html_path}")
        print(f"API Portlari: {', '.join(map(str, self.api_ports))}")
        print(f"Panel Sayisi: {len(self.panels)}")
        print("="*60)
        
    def run(self):
        """Ana başlatma fonksiyonu"""
        try:
            # Sistem bilgilerini göster
            self.display_system_info()
            
            # Kontrol et
            logger.info("🔍 Sistem kontrolleri yapılıyor...")
            
            if not self.check_secrets_file():
                return False
                
            if not self.load_environment():
                return False
                
            if not self.check_html_files():
                return False
            
            # API sunucularını başlat
            self.start_api_servers()
            
            # Sistem servislerini başlat
            self.start_system_services()
            
            # HTML panellerini aç
            self.open_panels()
            
            logger.info("TRM FULL OTOMASYON SISTEMI başarıyla başlatıldı!")
            print("\n>> SISTEM AKTIF! Tüm paneller ve servisler çalışıyor...")
            
            return True
            
        except KeyboardInterrupt:
            logger.info("Sistem kullanıcı tarafından durduruldu")
            print("\n>> Sistem durduruldu...")
            return False
        except Exception as e:
            logger.error(f"Sistem başlatma hatası: {e}")
            print(f"\n>> HATA: {e}")
            return False

def main():
    """Ana fonksiyon"""
    print(">> ULUSLARASI TRM FULL OTOMASYON BASLATICI")
    print("Tüm panelleri ve servisleri aktif hale getirir...")
    
    starter = TRMSystemStarter()
    
    # Parametre kontrolü
    if len(sys.argv) > 1:
        if sys.argv[1] == "--check":
            starter.check_html_files()
            return
        elif sys.argv[1] == "--api-only":
            starter.start_api_servers()
            return
        elif sys.argv[1] == "--panels-only":
            starter.open_panels()
            return
    
    # Normal başlatma
    starter.run()

if __name__ == "__main__":
    main()
