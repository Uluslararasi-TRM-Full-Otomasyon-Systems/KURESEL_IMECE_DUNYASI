#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TRM Nirvana v3.0 - Flash Bellekten Direkt Çalıştırıcı
Plug & Play - Hiçbir kurulum gerekmez
"""

import os
import sys
import subprocess
import webbrowser
import time
import platform
from pathlib import Path

def show_banner():
    """Başlık göster"""
    print("""
===============================================
    TRM NİRVANA v3.0 - FLASH BELLEK
===============================================
  🚀 Plug & Play Otomasyon
  🤖 Hiçbir kurulum gerekmez
  📁 Flash bellekten direkt çalışır
  ⚡ Tek tıkla başlat
===============================================
    """)

def check_system():
    """Sistem kontrolü"""
    print("🔍 Sistem kontrol ediliyor...")
    
    # Python kontrol
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ gerekiyor")
        return False
    
    print(f"✅ Python {sys.version.split()[0]}")
    
    # İşletim sistemi kontrol
    os_name = platform.system()
    print(f"✅ İşletim Sistemi: {os_name}")
    
    return True

def auto_install_packages():
    """Otomatik paket kurulumu"""
    print("📦 Paketler kontrol ediliyor...")
    
    required_packages = [
        'telethon', 'aiohttp', 'bs4', 'openai', 
        'anthropic', 'pandas', 'requests', 'Pillow'
    ]
    
    missing = []
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing.append(package)
    
    if missing:
        print(f"⚠️  {len(missing)} paket eksik, yükleniyor...")
        
        for package in missing:
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", package, "--quiet"])
                print(f"✅ {package} yüklendi")
            except:
                print(f"❌ {package} yüklenemedi")
                return False
    else:
        print("✅ Tüm paketler mevcut")
    
    return True

def create_env_if_needed():
    """Ortam değişkenleri dosyası oluştur"""
    env_file = "secrets.env"
    
    if not os.path.exists(env_file):
        print("⚠️  secrets.env bulunamadı, oluşturuluyor...")
        
        env_content = """# TRM Full Otomasyon Sistemi v3.0 - Flash Bellek
# Lütfen API anahtarlarınızı girin

# Telegram API
TELEGRAM_API_ID=your_telegram_api_id
TELEGRAM_API_HASH=your_telegram_api_hash
TELEGRAM_PHONE=+90555xxxxxxx

# AI Servisleri
DEEPSEEK_API_KEY=your_deepseek_api_key
CLAUDE_API_KEY=your_claude_api_key

# Sosyal Medya
FACEBOOK_ACCESS_TOKEN=your_facebook_access_token
INSTAGRAM_ACCESS_TOKEN=your_instagram_access_token
TIKTOK_ACCESS_TOKEN=your_tiktok_access_token
YOUTUBE_API_KEY=your_youtube_api_key

# Google Drive
GOOGLE_DRIVE_FOLDER_ID=your_google_drive_folder_id

# Sistem Konfigürasyonu
STORE_URL=https://trendurunlermarket.com
COMMISSION_THRESHOLD=20.0
CHECK_INTERVAL=300
MAX_PRODUCTS_PER_DAY=50
"""
        
        with open(env_file, 'w', encoding='utf-8') as f:
            f.write(env_content)
        
        print("✅ secrets.env oluşturuldu")
        print("⚠️  Lütfen API anahtarlarını girin!")
        return False
    
    print("✅ secrets.env mevcut")
    return True

def create_directories():
    """Gerekli dizinleri oluştur"""
    dirs = ['logs', 'data', 'temp_photos', 'temp_docs']
    
    for dir_name in dirs:
        Path(dir_name).mkdir(exist_ok=True)
    
    print("✅ Dizinler hazır")

def start_panel():
    """Paneli başlat"""
    print("🚀 Panel başlatılıyor...")
    
    try:
        subprocess.Popen([sys.executable, "ENHANCED_PANEL.py"])
        time.sleep(3)
        webbrowser.open('http://localhost:9000')
        print("✅ Panel açıldı: http://localhost:9000")
        return True
    except Exception as e:
        print(f"❌ Panel başlatılamadı: {e}")
        return False

def start_full_system():
    """Tam sistemi başlat"""
    print("🤖 Full otomasyon başlatılıyor...")
    
    try:
        # Paneli başlat
        subprocess.Popen([sys.executable, "ENHANCED_PANEL.py"])
        
        # Ana sistemi başlat
        subprocess.Popen([sys.executable, "main_orchestrator.py"])
        
        time.sleep(3)
        webbrowser.open('http://localhost:9000')
        
        print("✅ Full sistem başlatıldı!")
        print("🌐 Panel: http://localhost:9000")
        print("🤖 Arka plan botları çalışıyor")
        return True
    except Exception as e:
        print(f"❌ Sistem başlatılamadı: {e}")
        return False

def main_menu():
    """Ana menü"""
    while True:
        print("\n🎯 BAŞLATMA SEÇENEKLERİ:")
        print("=" * 40)
        print("1. 🚀 Sadece Panel (Web Arayüz)")
        print("2. 🤖 Full Otomasyon Sistemi")
        print("3. 📊 Sadece Ana Orchestrator")
        print("4. ⚙️  Ayarları Düzenle (secrets.env)")
        print("5. ❌ Çıkış")
        print("=" * 40)
        
        try:
            choice = input("\nSeçiminiz (1-5): ").strip()
            
            if choice == "1":
                if start_panel():
                    print("\n✅ Panel çalışıyor!")
                    print("🌐 http://localhost:9000 adresini kullanın")
                break
                
            elif choice == "2":
                if start_full_system():
                    print("\n✅ Full otomasyon çalışıyor!")
                    print("🌐 Panel: http://localhost:9000")
                    print("🤖 Tüm modüller arka planda")
                    print("📊 Her sabah 09:00 Telegram raporu")
                break
                
            elif choice == "3":
                print("📊 Ana orchestrator başlatılıyor...")
                subprocess.Popen([sys.executable, "main_orchestrator.py"])
                print("✅ Orchestrator çalışıyor")
                break
                
            elif choice == "4":
                print("⚙️  secrets.env açılıyor...")
                if platform.system() == "Windows":
                    os.startfile("secrets.env")
                else:
                    subprocess.run(["nano", "secrets.env"])
                continue
                
            elif choice == "5":
                print("👋 Çıkış yapılıyor...")
                break
                
            else:
                print("❌ Geçersiz seçenek!")
                
        except KeyboardInterrupt:
            print("\n👋 İptal edildi")
            break
        except Exception as e:
            print(f"❌ Hata: {e}")

def main():
    """Ana fonksiyon"""
    show_banner()
    
    # Flash bellek kontrolü
    current_dir = os.getcwd()
    if "ULUSLARASI-TRM-FULL-OTOMASYON-SISTEMI" not in current_dir:
        print("⚠️  Flash bellekteki dizinde değilsiniz!")
        print("📁 Lütfen flash bellekteki klasörde çalıştırın")
        input("Devam etmek için Enter'a basın...")
        return
    
    # Sistem kontrolleri
    if not check_system():
        input("Sistem gereksinimleri karşılanmıyor. Enter'a basın...")
        return
    
    # Otomatik kurulum
    if not auto_install_packages():
        print("❌ Paket kurulumu başarısız")
        input("Manuel kurulum gerekiyor. Enter'a basın...")
        return
    
    create_directories()
    
    # Ortam değişkenleri kontrolü
    if not create_env_if_needed():
        input("API anahtarlarını girdikten sonra devam edin...")
        return
    
    # Ana menü
    main_menu()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n👋 TRM Nirvana durduruldu")
    finally:
        input("\nÇıkmak için Enter'a basın...")
