@echo off
chcp 65001 > nul
title TRM - Daemon Durdur
cd /d "%~dp0"
set PY_CMD=python
py --version >nul 2>&1
if %errorlevel% equ 0 set PY_CMD=py
echo TRM Daemon durduruluyor...
%PY_CMD% DAEMON_MANAGER.py stop
pause
