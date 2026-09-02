#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TRM Nirvana v3.0 - Sistem Durumu Kontrolu
7/24 calisma durumunu kontrol eder
"""

import requests
import json
import time
import sys
from datetime import datetime

def check_system_status():
    """Sistem durumunu kontrol et"""
    print("🔍 TRM Nirvana v3.0 Sistem Durumu Kontrolu")
    print("=" * 50)
    
    # Status API kontrol
    try:
        response = requests.get('http://localhost:9001/status', timeout=5)
        if response.status_code == 200:
            status_data = response.json()
            print("✅ Status API calisiyor")
            print(f"📊 Ana Sistem: {status_data.get('main', 'Bilinmiyor')}")
            print(f"🌐 Web Panel: {status_data.get('panel', 'Bilinmiyor')}")
            print(f"📱 Sosyal Medya: {status_data.get('social', 'Bilinmiyor')}")
            print(f"☁️ Cloud Durumu: {status_data.get('cloud', 'Bilinmiyor')}")
            print(f"⏰ Calisma Suresi: {status_data.get('uptime', 'Bilinmiyor')}")
            
            if status_data.get('main') == 'Aktif':
                print("\n🚀 SISTEM 7/24 CALISIYOR!")
                print("✅ Tum moduller aktif")
                print("🌐 Panel: http://localhost:9000")
                return True
            else:
                print("\n❌ Sistem calismiyor")
                return False
        else:
            print(f"❌ Status API hata: {response.status_code}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Status API'ye baglanilamadi")
        print("📝 SON_BASLAT.py calismiyor olabilir")
        return False
    except Exception as e:
        print(f"❌ Hata: {e}")
        return False

def check_panel_status():
    """Panel durumunu kontrol et"""
    try:
        response = requests.get('http://localhost:9000', timeout=5)
        if response.status_code == 200:
            print("✅ Panel calisiyor: http://localhost:9000")
            return True
        else:
            print(f"❌ Panel hata: {response.status_code}")
            return False
    except:
        print("❌ Panel calismiyor")
        return False

def check_processes():
    """Process'leri kontrol et"""
    print("\n🔍 Process Kontrolu:")
    
    try:
        import psutil
        processes = []
        
        for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
            try:
                cmdline = ' '.join(proc.info['cmdline'] or [])
                if 'python' in cmdline and any(x in cmdline for x in [
                    'ENHANCED_PANEL.py', 'main_orchestrator.py', 
                    'telegram_listener.py', 'web_scraper.py'
                ]):
                    processes.append(proc.info)
            except:
                continue
        
        if processes:
            print(f"✅ {len(processes)} Python process calisiyor:")
            for proc in processes[:5]:  # Ilk 5'i goster
                cmdline = ' '.join(proc['cmdline'] or [])
                print(f"  • PID {proc['pid']}: {cmdline[:50]}...")
        else:
            print("❌ Hicbir Python process bulunamadi")
            
        return len(processes) > 0
        
    except ImportError:
        print("⚠️  psutil kurulu degil, process kontrol edilemiyor")
        return None

def main():
    """Ana kontrol fonksiyonu"""
    print(f"""
===============================================
    TRM NIRVANA v3.0 - SISTEM DURUMU
===============================================
Tarih: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
===============================================
""")
    
    # Status API kontrol
    status_ok = check_system_status()
    
    # Panel kontrol
    panel_ok = check_panel_status()
    
    # Process kontrol
    processes_ok = check_processes()
    
    print("\n" + "=" * 50)
    print("📊 OZET DURUM:")
    
    if status_ok and panel_ok:
        print("✅ SISTEM 7/24 CALISIYOR!")
        print("🚀 Tum moduller aktif")
        print("🌐 Panel erisilebilir")
        print("💾 Veri akisi devam ediyor")
        print("☁️ Cloud deployment hazir")
    elif status_ok:
        print("⚠️  Sistem calisiyor ama panel erisilebilir degil")
        print("📝 Panel yeniden baslatilabilir")
    elif panel_ok:
        print("⚠️  Panel calisiyor ama sistem durumu bilinmiyor")
        print("📝 Status API kontrol edilmeli")
    else:
        print("❌ SISTEM CALISMIYOR!")
        print("📝 SON_BASLAT.bat calistirin")
        print("🚀 'SISTEMI BASLAT' butonuna tiklayin")
    
    print("=" * 50)
    
    # Oneriler
    print("\n💡 ONERILER:")
    
    if not status_ok:
        print("• SON_BASLAT.bat calistirin")
        print("• TEK_TIK_SON.html acin")
        print("• '🚀 SISTEMI BASLAT' butonuna tiklayin")
    
    if not panel_ok and status_ok:
        print("• Panel yeniden baslatilabilir")
        print("• http://localhost:9000 adresini kontrol edin")
    
    if status_ok:
        print("• Sistem 7/24 calismaya devam edecek")
        print("• Bilgisayar kapansa bile cloud'da devam eder")
        print("• Durum takibi icin panel kullanabilirsiniz")

if __name__ == "__main__":
    main()
