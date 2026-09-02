@echo off
chcp 65001 > nul
title TRM - Hizli Baslat
cd /d "%~dp0"
set PYTHONIOENCODING=utf-8
set PYTHONUTF8=1
set PY_CMD=python
py --version >nul 2>&1
if %errorlevel% equ 0 set PY_CMD=py
echo TRM Full Otomasyon - Hizli Baslat
echo =====================================
%PY_CMD% run.py
pause
