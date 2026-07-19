@echo off
chcp 65001 >nul
title TRM Nirvana Starter v1.0
color 0B

echo.
echo ╔═══════════════════════════════════════════════════════════════╗
echo ║                                                               ║
echo ║   🚀 TRM NIRVANA STARTER v1.0                                 ║
echo ║   Maximum Performans Otomasyon Sistemi                       ║
echo ║                                                               ║
echo ╚═══════════════════════════════════════════════════════════════╝
echo.

REM Python kontrolü
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python bulunamadı! Lütfen Python 3.8+ yükleyin.
    pause
    exit /b 1
)

echo ✅ Python tespit edildi
echo.

REM Bağımlılık kontrolü ve yükleme
echo 📦 Bağımlılıklar kontrol ediliyor...
pip show aiohttp >nul 2>&1
if errorlevel 1 (
    echo ⚠️  Bazı bağımlılıklar eksik, yükleniyor...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo ❌ Bağımlılık yükleme hatası!
        pause
        exit /b 1
    )
    echo ✅ Bağımlılıklar yüklendi
) else (
    echo ✅ Bağımlılıklar mevcut
)

echo.
echo 🏥 Sağlık kontrolü yapılıyor...
python NIRVANA_HEALTH_MONITOR.py
if errorlevel 1 (
    echo ⚠️  Sağlık kontrolünde uyarılar var
) else (
    echo ✅ Sağlık kontrolü tamamlandı
)

echo.
echo 🚀 TRM Nirvana sistemi başlatılıyor...
echo.

REM Nirvana starter'ı başlat
python NIRVANA_STARTER.py

if errorlevel 1 (
    echo.
    echo ❌ Sistem başlatılamadı!
    echo.
    echo Lütfen aşağıdakileri kontrol edin:
    echo 1. secrets.env dosyasının mevcut ve doğru yapılandırılmış olduğundan emin olun
    echo 2. Tüm API anahtarlarının geçerli olduğundan emin olun
    echo 3. İnternet bağlantınızın olduğundan emin olun
    echo.
    pause
    exit /b 1
)

echo.
echo ✅ Sistem başarıyla başlatıldı!
echo.
pause
