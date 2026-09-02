@echo off
chcp 65001 > nul
title TRM Full Otomasyon v4.0 - Ana Baslatic
cd /d "%~dp0"
setlocal enabledelayedexpansion

:: ============================================================
::   TRM FULL OTOMASYON v4.0 - STABLE LAUNCHER
::   Tum duzeltmeler dahil (encoding, daemon, zincir)
:: ============================================================

:: Python tespiti (py launcher > python3 > python)
set PY_CMD=python
py --version >nul 2>&1
if %errorlevel% equ 0 (
    set PY_CMD=py
) else (
    python3 --version >nul 2>&1
    if %errorlevel% equ 0 set PY_CMD=python3
)

:: UTF-8 zorunlu
set PYTHONIOENCODING=utf-8
set PYTHONUTF8=1

:: Log klasoru
if not exist "logs" mkdir logs

:: Ilk kurulumda bagimlilik yukle
if not exist ".deps_v4_installed" (
    echo.
    echo ============================================================
    echo   ILK KURULUM - BAGIMLILIKLAR YUKLENIYOR...
    echo ============================================================
    %PY_CMD% -m pip install --upgrade pip --quiet
    %PY_CMD% -m pip install -r requirements.txt --quiet
    if %errorlevel% neq 0 (
        echo.
        echo HATA: Bagimliliklar yuklenemedi!
        echo   pip install -r requirements.txt komutunu manuel calistirin.
        pause
        exit /b 1
    )
    echo. > .deps_v4_installed
    echo    Bagimliliklar yuklendi.
    echo ============================================================
    echo.
)

:MENU
cls
echo.
echo  ============================================================
echo    TRM FULL OTOMASYON v4.0  -  Stable Launcher
echo  ============================================================
echo.
echo    SISTEM
echo    [1] Tum Sistemi Baslat           (main_orchestrator)
echo    [2] Daemon Baslat (arka plan)    (DAEMON_MANAGER start)
echo    [3] Daemon Durdur                (DAEMON_MANAGER stop)
echo    [4] Daemon Durumu / Health       (DAEMON_MANAGER status)
echo.
echo    MODULLER
echo    [5] Sadece Telegram Dinleyici    (run.py telegram)
echo    [6] Sadece Web Scraper           (run.py scraper)
echo    [7] Sadece AI Testi              (run.py ai)
echo    [8] Sadece Sosyal Medya Testi    (run.py social)
echo.
echo    SATIS ve RAPOR
echo    [9] Satis Donus Zinciri Raporu   (SATIS_DONUS_ZINCIRI.py)
echo    [A] Komisyon Takip Raporu        (trm_tracking.py)
echo    [B] API / Platform Durumu        (run.py status)
echo.
echo    YAPILANDIRMA
echo    [C] secrets.env Duzenle          (notepad)
echo    [D] API Anahtarlari Rehberi      (notepad)
echo    [E] Duzeltmeler Raporu           (notepad)
echo.
echo    TEST ve BAKIM
echo    [F] Birim Testleri               (pytest test_trm.py -v)
echo    [G] Parser Testi                 (telegram_parser.py)
echo    [H] Sistem Tamamen Test          (run.py test)
echo.
echo    [X] Cikis
echo.
echo  ============================================================
set /p secim="  Seciminiz: "

if /i "%secim%"=="1" goto :RUN_FULL
if /i "%secim%"=="2" goto :DAEMON_START
if /i "%secim%"=="3" goto :DAEMON_STOP
if /i "%secim%"=="4" goto :DAEMON_STATUS
if /i "%secim%"=="5" goto :RUN_TELEGRAM
if /i "%secim%"=="6" goto :RUN_SCRAPER
if /i "%secim%"=="7" goto :RUN_AI
if /i "%secim%"=="8" goto :RUN_SOCIAL
if /i "%secim%"=="9" goto :SATIS_RAPOR
if /i "%secim%"=="A" goto :KOMISYON_RAPOR
if /i "%secim%"=="B" goto :API_STATUS
if /i "%secim%"=="C" goto :EDIT_SECRETS
if /i "%secim%"=="D" goto :EDIT_REHBER
if /i "%secim%"=="E" goto :EDIT_DUZELTME
if /i "%secim%"=="F" goto :RUN_PYTEST
if /i "%secim%"=="G" goto :RUN_PARSER
if /i "%secim%"=="H" goto :RUN_TEST
if /i "%secim%"=="X" exit /b 0

echo   Gecersiz secim!
timeout /t 2 > nul
goto :MENU

:RUN_FULL
cls
echo  [1] Tum sistem baslatiliyor...
%PY_CMD% run.py
pause
goto :MENU

:DAEMON_START
cls
echo  [2] Daemon arka planda baslatiliyor...
%PY_CMD% DAEMON_MANAGER.py start
pause
goto :MENU

:DAEMON_STOP
cls
echo  [3] Daemon durduruluyor...
%PY_CMD% DAEMON_MANAGER.py stop
pause
goto :MENU

:DAEMON_STATUS
cls
echo  [4] Daemon durumu:
%PY_CMD% DAEMON_MANAGER.py status
echo.
%PY_CMD% DAEMON_MANAGER.py health
pause
goto :MENU

:RUN_TELEGRAM
cls
echo  [5] Telegram dinleyici:
%PY_CMD% run.py telegram
pause
goto :MENU

:RUN_SCRAPER
cls
echo  [6] Web Scraper:
%PY_CMD% run.py scraper
pause
goto :MENU

:RUN_AI
cls
echo  [7] AI testi:
%PY_CMD% run.py ai
pause
goto :MENU

:RUN_SOCIAL
cls
echo  [8] Sosyal medya testi:
%PY_CMD% run.py social
pause
goto :MENU

:SATIS_RAPOR
cls
echo  [9] Satis Donus Zinciri Raporu:
%PY_CMD% SATIS_DONUS_ZINCIRI.py
pause
goto :MENU

:KOMISYON_RAPOR
cls
echo  [A] Komisyon Takip Raporu:
%PY_CMD% trm_tracking.py
pause
goto :MENU

:API_STATUS
cls
echo  [B] API / Platform Durumu:
%PY_CMD% run.py status
pause
goto :MENU

:EDIT_SECRETS
start notepad secrets.env
goto :MENU

:EDIT_REHBER
start notepad API_ANAHTARLARI_REHBERI.md
goto :MENU

:EDIT_DUZELTME
start notepad DUZELTMELER.md
goto :MENU

:RUN_PYTEST
cls
echo  [F] Birim testler:
%PY_CMD% -m pytest test_trm.py -v --tb=short
pause
goto :MENU

:RUN_PARSER
cls
echo  [G] Parser testi:
%PY_CMD% telegram_parser.py
pause
goto :MENU

:RUN_TEST
cls
echo  [H] Tam sistem testi:
%PY_CMD% run.py test
pause
goto :MENU
