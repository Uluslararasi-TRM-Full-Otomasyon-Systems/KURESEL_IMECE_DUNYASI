@echo off
chcp 65001 >nul
title Sosyal İmece Sözleşme Onay Sistemi

echo.
echo ========================================
echo    SOSYAL İMECE SÖZLEŞME ONAY SİSTEMİ
echo ========================================
echo.
echo Streamlit uygulaması başlatılıyor...
echo.

streamlit run sozlesme_onay_sistemi.py --server.port 8501

pause
