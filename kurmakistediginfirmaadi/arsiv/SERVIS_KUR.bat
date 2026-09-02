@echo off
chcp 65001 > nul
title TRM - Windows Servis Kurulum
cd /d "%~dp0"
set PY_CMD=python
py --version >nul 2>&1
if %errorlevel% equ 0 set PY_CMD=py
echo TRM Windows Servis Kurulumu...
echo (NSSM veya Task Scheduler dosyalari olusturulacak)
%PY_CMD% DAEMON_MANAGER.py install
pause
