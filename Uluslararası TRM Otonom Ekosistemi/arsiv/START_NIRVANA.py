#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TRM Nirvana Starter - Tek tıkla tam otomasyon başlatıcı
"""

import os
import sys
import subprocess
import webbrowser
import time
import asyncio
from pathlib import Path

def check_python_version():
    """Python versiyonunu kontrol et"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ gerekiyor")
        print(f"   Mevcut: {sys.version}")
        return False
    print(f"✅ Python {sys.version.split()[0]} - Uygun")
    return True

def install_requirements():
    """Gerekli paketleri yükle"""
    print("📦 Gerekli paketler kontrol ediliyor...")
    
    required_packages = [
        "telethon>=1.34.0",
        "aiohttp>=3.8.0", 
        "beautifulsoup4>=4.12.0",
        "lxml>=4.9.0",
        "openai>=1.3.0",
        "anthropic>=0.7.0",
        "google-api-python-client>=2.100.0",
        "google-auth-httplib2>=0.1.0",
        "google-auth-oauthlib>=1.1.0",
        "pandas>=2.0.0",
        "numpy>=1.24.0",
        "requests>=2.31.0",
        "Pillow>=10.0.0",
        "python-dotenv>=1.0.0"
    ]
    
    missing_packages = []
    
    for package in required_packages:
        package_name = package.split('>=')[0].split('==')[0]
        try:
            __import__(package_name.replace('-', '_'))
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print(f"❌ Eksik paketler: {len(missing_packages)}")
        print("📦 Paketler yükleniyor...")
        
        for package in missing_packages:
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", package])
                print(f"✅ {package} yüklendi")
            except subprocess.CalledProcessError as e:
                print(f"❌ {package} yüklenemedi: {e}")
                return False
        
        print("✅ Tüm paketler yüklendi")
    else:
        print("✅ Tüm paketler mevcut")
    
    return True

def create_directories():
    """Gerekli dizinleri oluştur"""
    directories = [
        "logs",
        "data", 
        "temp_photos",
        "temp_docs",
        "config"
    ]
    
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
    
    print("✅ Dizinler oluşturuldu")

def create_env_file():
    """Ortam değişkenleri dosyası oluştur"""
    env_file = "secrets.env"
    
    if not os.path.exists(env_file):
        print(f"⚠️ {env_file} dosyası bulunamadı")
        
        env_content = """# TRM Full Otomasyon Sistemi - Ortam Değişkenleri
# Lütfen aşağıdaki anahtarları kendi değerlerinizle güncelleyin

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
        
        print(f"✅ {env_file} dosyası oluşturuldu")
        print(f"⚠️ Lütfen {env_file} dosyasını düzenleyerek API anahtarlarını girin!")
        return False
    else:
        print(f"✅ {env_file} dosyası mevcut")
        return True

def start_enhanced_panel():
    """Gelişmiş paneli başlat"""
    print("🚀 TRM Nirvana Panel v3.0 başlatılıyor...")
    
    try:
        # Paneli arka planda başlat
        subprocess.Popen([sys.executable, "ENHANCED_PANEL.py"])
        
        # Tarayıcıyı aç
        time.sleep(3)
        webbrowser.open('http://localhost:9000')
        print("✅ Panel tarayıcıda açıldı: http://localhost:9000")
        return True
    except Exception as e:
        print(f"❌ Panel başlatma hatası: {e}")
        return False

def start_full_system():
    """Tam sistemi başlat"""
    print("🤖 TRM Full Otomasyon Sistemi başlatılıyor...")
    
    try:
        # Ana orchestrator'ı başlat
        subprocess.Popen([sys.executable, "main_orchestrator.py"])
        print("✅ Full otomasyon sistemi başlatıldı")
        return True
    except Exception as e:
        print(f"❌ Full sistem başlatma hatası: {e}")
        return False

def show_system_info():
    """Sistem bilgisini göster"""
    print("""
===============================================
    TRM NİRVANA OTOMASYON v3.0
===============================================
  🚀 Nirvana Level Automation
  🤖 AI Powered | 7/24 Active
  📱 Multi Platform Integration
  📊 Real Analytics & Reporting
  ☁️ Cloud Ready
  🔒 Security First
===============================================
    """)

def main():
    """Ana başlatıcı fonksiyon"""
    show_system_info()
    
    # Kontroller
    print("🔍 Sistem kontrolleri yapılıyor...\n")
    
    if not check_python_version():
        input("Devam etmek için Enter'a basın...")
        return
    
    if not install_requirements():
        print("❌ Paket yükleme başarısız")
        input("Manuel olarak yükleyin: pip install -r requirements.txt")
        return
    
    create_directories()
    
    if not create_env_file():
        input("API anahtarlarını girdikten sonra devam edin...")
        return
    
    print("\n🎯 Başlatma seçenekleri:")
    print("1. 🚀 Sadece Panel (Web Arayüz)")
    print("2. 🤖 Full Otomasyon Sistemi") 
    print("3. 📊 Sadece Ana Orchestrator")
    print("4. ❌ Çıkış")
    
    while True:
        try:
            choice = input("\nSeçiminiz (1-4): ").strip()
            
            if choice == "1":
                if start_enhanced_panel():
                    print("\n✅ Panel başlatıldı!")
                    print("🌐 http://localhost:9000 adresini açın")
                    print("📊 Panel üzerinden sistem yönetimi yapabilirsiniz")
                break
                
            elif choice == "2":
                if start_enhanced_panel():
                    time.sleep(2)
                    if start_full_system():
                        print("\n✅ Full otomasyon sistemi başlatıldı!")
                        print("🚀 Panel: http://localhost:9000")
                        print("🤖 Arka plan botları çalışıyor")
                        print("📊 Her sabah 09:00 Telegram raporu")
                break
                
            elif choice == "3":
                if start_full_system():
                    print("\n✅ Ana orchestrator başlatıldı!")
                    print("🤖 Tüm modüller arka planda çalışıyor")
                break
                
            elif choice == "4":
                print("👋 Çıkış yapılıyor...")
                break
                
            else:
                print("❌ Geçersiz seçenek. Lütfen 1-4 arası bir sayı girin.")
                
        except KeyboardInterrupt:
            print("\n👋 İptal edildi")
            break
        except Exception as e:
            print(f"❌ Hata: {e}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n👋 TRM Nirvana Starter durduruldu")
    finally:
        input("\nÇıkmak için Enter'a basın...")
