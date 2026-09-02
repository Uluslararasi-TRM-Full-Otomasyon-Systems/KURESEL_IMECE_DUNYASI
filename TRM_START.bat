@echo off
title TRM FULL OTOMASYON (FLASH BELLEK)
echo =======================================
echo TRM Sistem Flash Bellekten Baslatiliyor...
echo =======================================
cd /d "%~dp0"
echo Calisma Dizini: %cd%
echo.
echo Python baslatiliyor...
py TRM_AUTOMATION_ENGINE.py
pause