#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TRM FULL OTOMASYON - API ANAHTARLARI DURUM KONTROLÜ (ASCII)
Mevcut API anahtarlarını gösterir ve eksik olanları listeler
"""

import os
from pathlib import Path

def check_api_keys():
    """API anahtarlarını kontrol et"""
    
    secrets_file = Path("secrets.env")
    
    print(">> API ANAHTARLARI DURUM KONTROLU")
    print("=" * 50)
    
    if not secrets_file.exists():
        print("[!] secrets.env dosyasi bulunamadi!")
        return
    
    # API anahtarlarını oku
    api_keys = {}
    with open(secrets_file, 'r', encoding='utf-8') as f:
        for line in f:
            if '=' in line and not line.startswith('#'):
                key, value = line.strip().split('=', 1)
                api_keys[key.strip()] = value.strip()
    
    # Kategorilere göre göster
    print("TELEGRAM API ANAHTARLARI:")
    print("-" * 30)
    
    telegram_keys = [
        ("TELEGRAM_API_ID", "Telegram API ID"),
        ("TELEGRAM_API_HASH", "Telegram API Hash"),
        ("TELEGRAM_BOT_TOKEN", "Telegram Bot Token"),
        ("TELEGRAM_CHAT_ID", "Telegram Chat ID")
    ]
    
    for key, desc in telegram_keys:
        if key in api_keys and api_keys[key] and not api_keys[key].startswith('your_'):
            print(f"[OK] {desc:<25} [MEVCUT]")
        else:
            print(f"[!] {desc:<25} [EKSİK]")
    
    print("\nAI VE CLOUD API ANAHTARLARI:")
    print("-" * 30)
    
    ai_cloud_keys = [
        ("OPENAI_API_KEY", "OpenAI API Key"),
        ("GOOGLE_DRIVE_API_KEY", "Google Drive API Key"),
        ("GOOGLE_DRIVE_CLIENT_ID", "Google Drive Client ID"),
        ("GOOGLE_DRIVE_CLIENT_SECRET", "Google Drive Client Secret")
    ]
    
    for key, desc in ai_cloud_keys:
        if key in api_keys and api_keys[key] and not api_keys[key].startswith('your_'):
            print(f"[OK] {desc:<25} [MEVCUT]")
        else:
            print(f"[!] {desc:<25} [EKSİK]")
    
    print("\nSOSYAL MEDYA API ANAHTARLARI:")
    print("-" * 30)
    
    social_keys = [
        ("DISCORD_BOT_TOKEN", "Telegram/Discord/Viber API Token"),
        ("TELEGRAM_CHAT_ID", "Telegram/Discord/Viber Phone Number"),
        ("FACEBOOK_ACCESS_TOKEN", "Facebook Access Token"),
        ("INSTAGRAM_ACCESS_TOKEN", "Instagram Access Token"),
        ("TWITTER_API_KEY", "Twitter API Key"),
        ("TWITTER_API_SECRET", "Twitter API Secret")
    ]
    
    for key, desc in social_keys:
        if key in api_keys and api_keys[key] and not api_keys[key].startswith('your_'):
            print(f"[OK] {desc:<25} [MEVCUT]")
        else:
            print(f"[!] {desc:<25} [EKSİK]")
    
    print("\nE-TICARET PLATFORMLARI:")
    print("-" * 30)
    
    ecommerce_keys = [
        ("TRENDYOL_API_KEY", "Trendyol API Key"),
        ("HEPSIBURADA_API_KEY", "Hepsiburada API Key"),
        ("N11_API_KEY", "N11 API Key")
    ]
    
    for key, desc in ecommerce_keys:
        if key in api_keys and api_keys[key] and not api_keys[key].startswith('your_'):
            print(f"[OK] {desc:<25} [MEVCUT]")
        else:
            print(f"[!] {desc:<25} [EKSİK]")
    
    print("\nCLOUD DEPLOYMENT ANAHTARLARI:")
    print("-" * 30)
    
    cloud_keys = [
        ("RAILWAY_TOKEN", "Railway Token"),
        ("RENDER_API_KEY", "Render API Key"),
        ("HEROKU_API_KEY", "Heroku API Key")
    ]
    
    for key, desc in cloud_keys:
        if key in api_keys and api_keys[key] and not api_keys[key].startswith('your_'):
            print(f"[OK] {desc:<25} [MEVCUT]")
        else:
            print(f"[!] {desc:<25} [EKSİK]")
    
    # Özet
    print("\nOZET:")
    print("-" * 30)
    
    total_keys = len(api_keys)
    real_keys = sum(1 for key, value in api_keys.items() 
                   if value and not value.startswith('your_') and value)
    
    print(f"Toplam API Anahtari: {total_keys}")
    print(f"Yapılandırılmış: {real_keys}")
    print(f"Yapılandırma Oranı: {(real_keys/total_keys*100):.1f}%")
    
    # Mevcut olanları göster
    print(f"\nMEVCUT GERCEK API ANAHTARLARI:")
    print("-" * 30)
    
    real_api_keys = {}
    for key, value in api_keys.items():
        if value and not value.startswith('your_') and value and len(value) > 10:
            real_api_keys[key] = value
    
    if real_api_keys:
        for key, value in real_api_keys.items():
            masked_value = value[:8] + "..." + value[-4:] if len(value) > 12 else "***"
            print(f"{key:<25} : {masked_value}")
    else:
        print("Hicbir gercek API anahtari bulunamadi!")
    
    # Kullanım durumu
    print(f"\nKULLANIM DURUMU:")
    print("-" * 30)
    
    if "TELEGRAM_BOT_TOKEN" in real_api_keys:
        print("[AKTIF] Telegram bildirimleri")
    else:
        print("[PASIF] Telegram bildirimleri")
    
    if "OPENAI_API_KEY" in real_api_keys:
        print("[AKTIF] OpenAI entegrasyonu")
    else:
        print("[PASIF] OpenAI entegrasyonu")
    
    if any(key in real_api_keys for key in ["GOOGLE_DRIVE_API_KEY", "GOOGLE_DRIVE_CLIENT_ID"]):
        print("[AKTIF] Google Drive entegrasyonu")
    else:
        print("[PASIF] Google Drive entegrasyonu")
    
    if "DISCORD_BOT_TOKEN" in real_api_keys:
        print("[AKTIF] Telegram/Discord/Viber bildirimleri")
    else:
        print("[PASIF] Telegram/Discord/Viber bildirimleri")

if __name__ == "__main__":
    check_api_keys()
