@echo off
chcp 65001 >nul
title TRM Full Otomasyon v5.0
cd /d "%~dp0"
set PYTHONIOENCODING=utf-8
set PYTHONUTF8=1

set PY=python
py --version >nul 2>&1 && set PY=py
%PY% --version >nul 2>&1
if errorlevel 1 (
    echo HATA: Python bulunamadi. python.org adresinden yukleyin.
    pause & exit /b
)

if not exist ".deps_v5" (
    echo Bagimliliklar yukleniyor...
    %PY% -m pip install -r requirements.txt --quiet
    if errorlevel 1 (echo HATA: pip install basarisiz & pause & exit /b)
    echo. >.deps_v5
    echo Kurulum tamamlandi!
)

:MENU
cls
echo.
echo  ====================================================
echo    TRM FULL OTOMASYON v5.0  ^|  trendurunlermarket.com
echo  ====================================================
echo.
echo   [1] SISTEMI BASLAT           (run.py - tam sistem)
echo   [2] WATCHDOG ile 7/24 Baslat (WATCHDOG.py)
echo   [3] Daemon Baslat            (DAEMON_MANAGER start)
echo   [4] Daemon Durdur            (DAEMON_MANAGER stop)
echo   [5] Daemon Durumu            (DAEMON_MANAGER status)
echo.
echo   [6] Sadece Telegram Dinle    (run.py telegram)
echo   [7] Sadece Web Scraper       (run.py scraper)
echo   [8] Sosyal Medya Testi       (run.py social)
echo   [9] AI Icerik Testi          (ai_integration.py)
echo.
echo   [S] Satis Dashboard          (SALES_DASHBOARD.py)
echo   [P] Yayin Plani              (CONTENT_SCHEDULER.py)
echo   [G] Guvenlik Denetimi        (SECURITY_MANAGER.py)
echo   [Q] Kuyruk Durumu            (QUEUE_MANAGER.py)
echo.
echo   [D] DM Otomatik Yanit         (DM_AUTO_REPLY.py)
  [M] E-posta Kampanyasi        (EMAIL_AUTOMATION.py)
  [Z] Platform Kurulum Rehberi  (PLATFORM_SETUP_WIZARD.py)
  [E] secrets.env Duzenle       (notepad)
echo   [T] Testleri Calistir        (pytest)
echo   [X] Cikis
echo  ====================================================
set /p secim=  Seciminiz: 

if /i "%secim%"=="1"  %PY% run.py & pause & goto MENU
if /i "%secim%"=="2"  %PY% WATCHDOG.py & pause & goto MENU
if /i "%secim%"=="3"  %PY% DAEMON_MANAGER.py start & pause & goto MENU
if /i "%secim%"=="4"  %PY% DAEMON_MANAGER.py stop & pause & goto MENU
if /i "%secim%"=="5"  %PY% DAEMON_MANAGER.py status & pause & goto MENU
if /i "%secim%"=="6"  %PY% run.py telegram & pause & goto MENU
if /i "%secim%"=="7"  %PY% run.py scraper & pause & goto MENU
if /i "%secim%"=="8"  %PY% run.py social & pause & goto MENU
if /i "%secim%"=="9"  %PY% ai_integration.py & pause & goto MENU
if /i "%secim%"=="S"  %PY% SALES_DASHBOARD.py & pause & goto MENU
if /i "%secim%"=="P"  %PY% CONTENT_SCHEDULER.py & pause & goto MENU
if /i "%secim%"=="G"  %PY% SECURITY_MANAGER.py & pause & goto MENU
if /i "%secim%"=="Q"  %PY% QUEUE_MANAGER.py & pause & goto MENU
if /i "%secim%"=="D"  %PY% DM_AUTO_REPLY.py & pause & goto MENU
if /i "%secim%"=="M"  %PY% EMAIL_AUTOMATION.py & pause & goto MENU
if /i "%secim%"=="Z"  %PY% PLATFORM_SETUP_WIZARD.py & pause & goto MENU
if /i "%secim%"=="E"  notepad secrets.env & goto MENU
if /i "%secim%"=="T"  %PY% -m pytest test_trm.py -v --tb=short & pause & goto MENU
if /i "%secim%"=="X"  exit /b
echo Gecersiz secim & timeout /t 1 >nul & goto MENU
