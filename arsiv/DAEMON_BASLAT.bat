@echo off
chcp 65001 > nul
title TRM - Daemon Baslat
cd /d "%~dp0"
set PYTHONIOENCODING=utf-8
set PYTHONUTF8=1
set PY_CMD=python
py --version >nul 2>&1
if %errorlevel% equ 0 set PY_CMD=py
echo TRM Daemon baslatiliyor (arka plan)...
%PY_CMD% DAEMON_MANAGER.py start
echo.
timeout /t 3 > nul
%PY_CMD% DAEMON_MANAGER.py status
pause
