#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ULUSLARARASI TRM FULL OTOMASYON v3.0
Panel Test Araci - Port ve Sunucu Kontrolu
"""

import requests
import time
from datetime import datetime

def test_panel(port, path="", name="Panel"):
    """Paneli test et"""
    url = f"http://localhost:{port}{path}"
    
    try:
        response = requests.get(url, timeout=3)
        if response.status_code == 200:
            print(f"+ {name} (Port {port}): CALISIYOR")
            return True
        else:
            print(f"- {name} (Port {port}): HATA - Status {response.status_code}")
            return False
    except Exception as e:
        print(f"- {name} (Port {port}): BAGLANAMADI - {str(e)}")
        return False

def main():
    print("ULUSLARARASI TRM FULL OTOMASYON v3.0")
    print("Panel Test Araci")
    print("=" * 50)
    print()
    
    # Test edilecek paneller
    panels = [
        (9000, "", "Ana Panel"),
        (9001, "/status", "Status API"),
        (9002, "", "Satis Paneli"),
        (9003, "", "Gelismis Panel"),
        (9004, "/drive-social", "Drive Sosyal Panel"),
        (9004, "/drive-social/status", "Drive Sosyal Status")
    ]
    
    print("Panel Durumlari Test Ediliyor...")
    print()
    
    working_count = 0
    total_count = len(panels)
    
    for port, path, name in panels:
        if test_panel(port, path, name):
            working_count += 1
        time.sleep(0.5)  # Testler arasi bekleme
    
    print()
    print("=" * 50)
    print(f"Test Sonuclari: {working_count}/{total_count} Panel Calisiyor")
    print()
    
    if working_count == total_count:
        print("TUM PANELLER CALISIYOR!")
        print("Sistem tam olarak aktif")
    else:
        print("BAZI PANELLER CALISMIYOR!")
        print("Sistemleri baslatmaniz gerekebilir")
    
    print()
    print("Panel URL'leri:")
    print("• Ana Panel: http://localhost:9000")
    print("• Status API: http://localhost:9001/status")
    print("• Satis Paneli: http://localhost:9002")
    print("• Gelismis Panel: http://localhost:9003")
    print("• Drive Sosyal: http://localhost:9004/drive-social")
    print()
    print(f"Test Zamani: {datetime.now().strftime('%H:%M:%S')}")

if __name__ == "__main__":
    main()
