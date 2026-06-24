@echo off
echo Python kontrol ediliyor...
py --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Bu bilgisayarda Python yok!
    echo 📥 Lütfen https://python.org adresinden Python kurun.
    pause
    exit
)
py TRM_AUTOMATION_ENGINE.py