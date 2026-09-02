@echo off
echo 🚀 TRM FULL OTOMASYON KURULUM BAŞLIYOR...
echo ======================================
echo.

echo 📦 Python kutuphaneleri yukleniyor...
pip install pytelegrambotapi python-dotenv requests schedule pandas openpyxl

echo.
echo ✅ Kurulum tamamlandi!
echo.
echo 📌 Sonraki adimlar:
echo 1. secrets.env dosyasini duzenle
echo 2. START.bat ile sistemi baslat
echo.
pause
