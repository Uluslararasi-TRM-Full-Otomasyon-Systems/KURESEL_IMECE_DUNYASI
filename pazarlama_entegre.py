#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TRM Nirvana v3.0 + PAZARLAMA Entegrasyonu
Iki sistemin birlesik baslaticisi
"""

import os
import sys
import subprocess
import webbrowser
import time
from pathlib import Path
from trm_paths import project_root, pazarlama_root

def show_integrated_banner():
    """Entegre sistem basligi"""
    print("""
===============================================
    TRM NIRVANA v3.0 + PAZARLAMA
===============================================
  🚀 Full Otomasyon + Pazarlama Stratejisi
  🤖 AI Powered + DMP Sistemi
  📊 7/24 Veri Toplama + Analiz
  📱 Multi Platform + Konum Bazli
===============================================
    """)

def check_pazarlama_system():
    """PAZARLAMA sistemini kontrol et"""
    pazarlama_path = pazarlama_root()
    
    if not pazarlama_path.exists():
        print("⚠️  PAZARLAMA klasoru bulunamadi")
        return False
    
    # PAZARLAMA sistem dosyalarini kontrol et
    required_files = [
        pazarlama_path / "03_Kilavuzlar_ve_Dokumanlar" / "TRM_Sistem_Kullanim_Kilavuzu.md"
    ]
    
    for file_path in required_files:
        if not file_path.exists():
            print(f"⚠️  {file_path} bulunamadi")
            return False
    
    print("✅ PAZARLAMA sistemi mevcut")
    return True

def create_integrated_launcher():
    """Entegre baslatici olustur"""
    trm_path = project_root()
    pazarlama_path = pazarlama_root()
    trm_bat_path = str(trm_path).replace("/", "\\")
    pazarlama_bat_path = str(pazarlama_path).replace("/", "\\")
    kilavuz_bat_path = str(pazarlama_path / "03_Kilavuzlar_ve_Dokumanlar" / "TRM_Sistem_Kullanim_Kilavuzu.md").replace("/", "\\")
    pazarlama_docs_path = str(pazarlama_path / "03_Kilavuzlar_ve_Dokumanlar").replace("/", "\\")

    launcher_content = f'''@echo off
chcp 65001 >nul
title TRM Nirvana v3.0 + PAZARLAMA - Entegre Sistem

REM Python komutunu tespit et (py veya python)
set PY_CMD=python
py --version >nul 2>&1
if %errorlevel% equ 0 set PY_CMD=py

echo.
echo ===============================================
echo    TRM NIRVANA v3.0 + PAZARLAMA
echo ===============================================
echo.
echo  🚀 Entegre sistem baslatiliyor...
echo  🤖 TRM Otomasyon + PAZARLAMA DMP
echo  📊 7/24 Veri toplama + Analiz
echo.

REM TRM sistemini baslat
cd /d "{trm_bat_path}"

echo ✅ TRM Nirvana baslatiliyor...
start /b %PY_CMD% START_NIRVANA.py

REM PAZARLAMA sistemini kontrol et
if exist "{kilavuz_bat_path}" (
    echo ✅ PAZARLAMA sistemi hazir
    echo 📊 Pazarlama dokumanlari: {pazarlama_docs_path}\\
)

echo.
echo 🎯 ENTEGRE SISTEM OZELLIKLERI:
echo ===============================================
echo 1. 🚀 TRM Full Otomasyon (7/24)
echo 2. 📊 PAZARLAMA DMP Sistemi
echo 3. 🤖 AI Destekli Analiz
echo 4. 📱 Multi Platform Paylasim
echo 5. 📍 Konum Bazli Veri Toplama
echo 6. 📈 Gercek Zamanli Raporlama
echo 7. 🌐 Web Dashboard
echo 8. ❌ Cikis
echo ===============================================

:menu
set /p choice="Seciminiz (1-8): "

if "%choice%"=="1" (
    echo.
    echo 🚀 TRM Full Otomasyon baslatiliyor...
    call CALISTIR_FLASH.bat
    goto end
)
if "%choice%"=="2" (
    echo.
    echo 📊 PAZARLAMA DMP sistemi baslatiliyor...
    start notepad "{kilavuz_bat_path}"
    echo 📋 Kullanim kilavuzu acildi
    goto menu
)
if "%choice%"=="3" (
    echo.
    echo 🤖 AI Destekli analiz baslatiliyor...
    %PY_CMD% ai_integration.py
    goto menu
)
if "%choice%"=="4" (
    echo.
    echo 📱 Multi Platform paylasim baslatiliyor...
    %PY_CMD% social_media_automation.py
    goto menu
)
if "%choice%"=="5" (
    echo.
    echo 📍 Konum bazli veri toplama baslatiliyor...
    echo 📊 PAZARLAMA DMP sistemi aktif
    echo 🌐 Dashboard: http://localhost:9000
    goto menu
)
if "%choice%"=="6" (
    echo.
    echo 📈 Gercek zamanli raporlama baslatiliyor...
    %PY_CMD% google_drive_integration.py
    goto menu
)
if "%choice%"=="7" (
    echo.
    echo 🌐 Web dashboard aciliyor...
    start http://localhost:9000
    goto menu
)
if "%choice%"=="8" (
    echo.
    echo 👋 Entegre sistem kapatiliyor...
    goto end
)

echo ❌ Gecersiz secenek! Lutfen 1-8 arasi bir sayi girin.
goto menu

:end
echo.
echo ✅ TRM Nirvana + PAZARLAMA entegre sistemi calisiyor...
echo 🌐 Panel: http://localhost:9000
echo 📊 Pazarlama dokumanlari: {pazarlama_docs_path}\\
pause
'''
    
    with open(trm_path / "ENTEGR_CALISTIR.bat", "w", encoding="utf-8") as f:
        f.write(launcher_content)
    
    print("✅ Entegre baslatici olusturuldu: ENTEGRE_CALISTIR.bat")

def create_integrated_dashboard():
    """Entegre dashboard olustur"""
    dashboard_path = project_root() / "ENTEGR_DASHBOARD.html"
    pazarlama_docs_js = str(pazarlama_root() / "03_Kilavuzlar_ve_Dokumanlar").replace("/", "\\\\").replace("\\", "\\\\")
    dashboard_html = '''<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <title>TRM Nirvana + PAZARLAMA Entegre Dashboard</title>
    <style>
        *{margin:0;padding:0;box-sizing:border-box;}
        body{background:radial-gradient(circle at 20%30%,#0a0f1e,#03060c);font-family:'Segoe UI',system-ui;color:#eef;padding:20px;}
        .container{max-width:1600px;margin:0 auto;background:rgba(15,22,36,0.75);backdrop-filter:blur(15px);border-radius:2rem;padding:1.8rem 2rem 2.2rem;border:1px solid rgba(255,170,51,0.3);}
        h1{font-size:2.2rem;font-weight:800;background:linear-gradient(135deg,#ffd966,#ffaa33,#ffdd99,#ffcc66);-webkit-background-clip:text;background-clip:text;color:transparent;text-align:center;}
        .system-grid{display:grid;grid-template-columns:1fr 1fr;gap:20px;margin-bottom:30px;}
        .system-card{background:#11161fe6;border-radius:28px;padding:20px;border:1px solid #ffaa5544;}
        .system-card h3{color:#ffdd99;margin-bottom:15px;}
        .status-badge{background:#1e2a3a;border:1px solid #ffaa55;color:#ffd966;padding:8px 20px;border-radius:40px;display:inline-block;margin:10px 0;}
        .btn-integrated{background:#1e2a3a;border:2px solid #ffaa55;color:#fff;padding:12px 20px;border-radius:60px;cursor:pointer;font-weight:bold;margin:8px 0;width:100%;transition:0.2s;}
        .btn-integrated:hover{background:#ffaa33;color:#000;transform:scale(1.02);}
        .features{display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:15px;margin:20px 0;}
        .feature{background:#0a0f18cc;border-radius:20px;padding:15px;border:1px solid #2a3344;}
        .feature h4{color:#ffdd99;margin-bottom:10px;}
    </style>
</head>
<body>
<div class="container">
    <h1>🚀 TRM Nirvana v3.0 + PAZARLAMA Entegre</h1>
    <div style="text-align:center"><span class="status-badge">🤖 7/24 AKTIF | 📊 DMP SISTEMI | 📱 MULTI PLATFORM</span></div>

    <div class="system-grid">
        <div class="system-card">
            <h3>🚀 TRM Nirvana v3.0</h3>
            <p>AI destekli tam otomasyon sistemi</p>
            <div class="status-badge">✅ Aktif</div>
            <ul style="color:#eef; margin:15px 0;">
                <li>🤖 AI icerik uretimi (DeepSeek + Claude)</li>
                <li>📱 Multi platform paylasim (6+ platform)</li>
                <li>📊 Google Drive entegrasyonu</li>
                <li>⚡ 7/24 tam otomasyon</li>
                <li>🔥 %20+ komisyon filtresi</li>
            </ul>
            <button class="btn-integrated" onclick="window.open('http://localhost:9000')">🌐 TRM Panel Ac</button>
        </div>

        <div class="system-card">
            <h3>📊 PAZARLAMA DMP Sistemi</h3>
            <p>Veri toplama ve segmentasyon platformu</p>
            <div class="status-badge">✅ Hazir</div>
            <ul style="color:#eef; margin:15px 0;">
                <li>📍 Konum bazli veri toplama</li>
                <li>🧠 AI destekli segmentasyon</li>
                <li>📈 Gercek zamanli analiz</li>
                <li>👥 Anonim kullanici takibi</li>
                <li>🎯 Hedefli reklam stratejisi</li>
            </ul>
            <button class="btn-integrated" onclick="openPazarlama()">📋 Pazarlama Dokumanlari</button>
        </div>
    </div>

    <div class="features">
        <div class="feature">
            <h4>🤖 AI Destekli Otomasyon</h4>
            <p>DeepSeek ile urun analizi, Claude ile icerik uretimi. %20+ komisyonlu urunleri otomatik tespit eder ve sosyal medyada paylasir.</p>
        </div>
        <div class="feature">
            <h4>📊 DMP Veri Toplama</h4>
            <p>WiFi, uygulama ve pixel uzerinden konum bazli veri toplama. AI ile segmentasyon ve kisisellestirilmis reklam stratejisi.</p>
        </div>
        <div class="feature">
            <h4>📱 Multi Platform</h4>
            <p>Facebook, Instagram, TikTok, YouTube, Blog sitelerinde otomatik paylasim. Google Drive'da veri yedekleme ve analitik.</p>
        </div>
        <div class="feature">
            <h4>🎯 Hedefli Pazarlama</h4>
            <p>Konum bazli segmentasyon, kullanici davranis analizi, kisisellestirilmis icerik ve reklam stratejileri.</p>
        </div>
    </div>

    <div style="text-align:center;margin-top:30px;">
        <h3 style="color:#ffdd99;margin-bottom:20px;">🎯 Entegre Sistem Kontrolu</h3>
        <button class="btn-integrated" onclick="startTRM()">🚀 TRM Sistemi Baslat</button>
        <button class="btn-integrated" onclick="openPazarlama()">📊 Pazarlama Sistemi</button>
        <button class="btn-integrated" onclick="showStatus()">📈 Sistem Durumu</button>
    </div>

    <div style="text-align:center;margin-top:30px;font-size:12px;color:#ffaa88;">
        ⚡ TRM Nirvana v3.0 + PAZARLAMA | Full Entegre Otomasyon | AI Powered | 7/24 Active
    </div>
</div>

<script>
function openPazarlama() {
    alert('📊 Pazarlama dokumanlari: PAZARLAMA/03_Kilavuzlar_ve_Dokumanlar/\\n📋 TRM_Sistem_Kullanim_Kilavuzu.md');
}

function startTRM() {
    window.open('http://localhost:9000');
}

function showStatus() {
    alert('🤖 TRM Nirvana: Aktif\\n📊 PAZARLAMA DMP: Hazir\\n🚀 Entegre Sistem: Calisiyor');
}
</script>
</body>
</html>'''
    
    dashboard_html = dashboard_html.replace(
        "G:\\\\PAZARLAMA\\\\03_Kilavuzlar_ve_Dokumanlar", 
        pazarlama_docs_js
    )
    
    with open(dashboard_path, "w", encoding="utf-8") as f:
        f.write(dashboard_html)
    
    print("✅ Entegre dashboard olusturuldu: ENTEGR_DASHBOARD.html")

def main():
    """Ana fonksiyon"""
    show_integrated_banner()
    
    print("🔍 Entegre sistem kontrol ediliyor...")
    
    # PAZARLAMA sistemini kontrol et
    if not check_pazarlama_system():
        print("⚠️  PAZARLAMA sistemi bulunamadi, sadece TRM sistemi calisacak")
    else:
        print("✅ PAZARLAMA sistemi mevcut")
    
    # Entegre baslatici olustur
    create_integrated_launcher()
    
    # Entegre dashboard olustur
    create_integrated_dashboard()
    
    print("\n🎯 ENTEGRE SISTEM OZELLIKLERI:")
    print("=" * 50)
    print("🚀 TRM Nirvana v3.0:")
    print("   • AI destekli otomasyon")
    print("   • Multi platform paylasim")
    print("   • 7/24 tam otomasyon")
    print("")
    print("📊 PAZARLAMA DMP:")
    print("   • Konum bazli veri toplama")
    print("   • AI segmentasyon")
    print("   • Gercek zamanli analiz")
    print("")
    print("🌐 Entegre Dashboard:")
    print("   • Iki sistemi bir arada yonet")
    print("   • Tek arayuzden kontrol")
    print("   • Gercek zamanli durum")
    print("=" * 50)
    
    print("\n📋 Baslatma Secenekleri:")
    print("1. 🚀 ENTEGRE_CALISTIR.bat - Iki sistem birlikte")
    print("2. 🌐 ENTEGR_DASHBOARD.html - Web arayuzu")
    print("3. 🚀 CALISTIR_FLASH.bat - Sadece TRM")
    
    # Dashboard'u ac
    dashboard_path = project_root() / "ENTEGR_DASHBOARD.html"
    webbrowser.open(dashboard_path.as_uri())
    
    print("\n✅ Entegre sistem hazir!")
    print("🌐 Dashboard acildi")

if __name__ == "__main__":
    main()
