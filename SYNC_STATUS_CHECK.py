#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TRM FULL OTOMASYON - SENKRONIZASYON DURUM KONTROLU
Google Drive ve Flash Bellek dosyalarini karsilastirir
"""

import os
import json
from datetime import datetime
from pathlib import Path

from trm_paths import flash_sync_root

def check_sync_status():
    """Senkronizasyon durumunu kontrol et"""
    
    flash_path = flash_sync_root()
    system_path = Path(__file__).parent
    
    print(">> GOOGLE DRIVE - FLASH BELLEK SENKRONIZASYON DURUMU")
    print("=" * 60)
    
    # Flash bellek dosyalarini say
    flash_files = []
    if flash_path.exists():
        for file_path in flash_path.rglob('*'):
            if file_path.is_file():
                flash_files.append(str(file_path.relative_to(flash_path)))
    
    # Sistem dosyalarini say
    system_files = []
    for file_path in system_path.rglob('*'):
        if file_path.is_file():
            system_files.append(str(file_path.relative_to(system_path)))
    
    # Istatistikler
    print(f"📁 Flash Bellek (G:): {len(flash_files)} dosya")
    print(f"📂 Sistem Klasoru: {len(system_files)} dosya")
    
    # Onemli dosyalari kontrol et
    important_files = [
        "secrets.env",
        "TRM_SYSTEM_STARTER.py",
        "API_INTEGRATION_MANAGER.py",
        "MESAJLASMA_BILDIRIM.py",
        "SOSYAL_MEDYA_KONTROL.py",
        "DRIVE_SOCIAL_WORKFLOW.py",
        "DRIVE_FLASH_SYNC.py",
        "AUTOMATED_BACKUP_SYSTEM.py",
        "SYSTEM_DOKUMANTASYONU.md"
    ]
    
    print("\n📋 ONEMLI DOSYALAR DURUMU:")
    print("-" * 40)
    
    for file_name in important_files:
        flash_has = file_name in flash_files
        system_has = file_name in system_files
        
        if flash_has and system_has:
            status = "✅ Iki konumda da var"
        elif flash_has:
            status = "⚠️ Sadece flash bellekte"
        elif system_has:
            status = "⚠️ Sadece sistem klasorunde"
        else:
            status = "❌ Hicbirinde yok"
        
        print(f"{file_name:<30} {status}")
    
    # Sadece flash bellekte olan dosyalar
    flash_only = set(flash_files) - set(system_files)
    if flash_only:
        print(f"\n📤 SADECE FLASH BELLEKTE OLAN DOSYALAR ({len(flash_only)}):")
        for file_name in sorted(list(flash_only))[:10]:  # Ilk 10
            print(f"  • {file_name}")
        if len(flash_only) > 10:
            print(f"  ... ve {len(flash_only) - 10} dosya daha")
    
    # Sadece sistem klasorunde olan dosyalar
    system_only = set(system_files) - set(flash_files)
    if system_only:
        print(f"\n📥 SADECE SISTEM KLASORUNDE OLAN DOSYALAR ({len(system_only)}):")
        for file_name in sorted(list(system_only))[:10]:  # Ilk 10
            print(f"  • {file_name}")
        if len(system_only) > 10:
            print(f"  ... ve {len(system_only) - 10} dosya daha")
    
    # Ortak dosyalar
    common_files = set(flash_files) & set(system_files)
    print(f"\n✅ IKI KONUMDA DA OLAN DOSYALAR: {len(common_files)}")
    
    # Senkronizasyon ozeti
    print(f"\n📊 SENKRONIZASYON OZETI:")
    print(f"  Toplam Flash Dosyasi: {len(flash_files)}")
    print(f"  Toplam Sistem Dosyasi: {len(system_files)}")
    print(f"  Ortak Dosyalar: {len(common_files)}")
    print(f"  Sadece Flash'ta: {len(flash_only)}")
    print(f"  Sadece Sistem'de: {len(system_only)}")
    
    # Senkronizasyon orani
    if len(flash_files) > 0:
        sync_rate = (len(common_files) / len(flash_files)) * 100
        print(f"  Senkronizasyon Orani: {sync_rate:.1f}%")
    
    # Google Drive durumu
    print(f"\n☁️ GOOGLE DRIVE DURUMU:")
    print("  API Anahtarlari: Eksik (simulasyon modu)")
    print("  Gercek Senkronizasyon: API anahtarlari gerekiyor")
    
    # Tavsiye
    print(f"\n💡 TAVSIYELER:")
    if len(flash_only) > 0:
        print("  • Flash bellekteki eksik dosyalari sistem klasorune kopyalayin")
    if len(system_only) > 0:
        print("  • Sistem klasorundeki yeni dosyalari flash bellege kopyalayin")
    print("  • Google Drive API anahtarlarini ekleyerek gercek senkronizasyon yapin")
    print("  • python DRIVE_FLASH_SYNC.py komutu ile tam senkronizasyon yapin")

if __name__ == "__main__":
    check_sync_status()
