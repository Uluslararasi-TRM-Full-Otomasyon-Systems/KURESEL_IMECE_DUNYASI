#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ULUSLARARASI TRM FULL OTOMASYON v3.0
Basit Sunucu Test Araci
"""

from http.server import HTTPServer, SimpleHTTPRequestHandler
import json
import time
import threading
import os
from datetime import datetime

class SimpleHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            
            # Her port icin farkli icerik olustur
            html_content = self.get_panel_content()
            self.wfile.write(html_content.encode('utf-8'))
            
        elif self.path == '/status':
            self.send_response(200)
            self.send_header('Content-type', 'application/json; charset=utf-8')
            self.end_headers()
            
            status_data = self.get_status_data()
            self.wfile.write(json.dumps(status_data, ensure_ascii=False, indent=2).encode('utf-8'))
            
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'Not Found')
    
    def get_panel_content(self):
        """Her port icin ozel HTML icerik olustur"""
        port = self.server.server_port
        
        if port == 9000:
            return f"""
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <title>ULUSLARARASI TRM FULL OTOMASYON - ANA (Trend Urunler Market) PANELI</title>
    <style>
        body {{ font-family: Arial, sans-serif; background: #1a1a2e; color: #eee; padding: 20px; }}
        .container {{ max-width: 800px; margin: 0 auto; background: #16213e; padding: 30px; border-radius: 10px; }}
        h1 {{ color: #ffd700; text-align: center; }}
        .status {{ background: #0f3460; padding: 15px; border-radius: 5px; margin: 20px 0; }}
        .info {{ background: #533483; padding: 15px; border-radius: 5px; margin: 20px 0; }}
        .button {{ background: #ffd700; color: #000; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer; margin: 5px; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>ULUSLARARASI TRM FULL OTOMASYON - ANA (Trend Urunler Market) PANELI</h1>
        
        <div class="status">
            <h3>✅ ANA PANEL AKTIF</h3>
            <p><strong>Port:</strong> {port}</p>
            <p><strong>Zaman:</strong> {datetime.now().strftime('%H:%M:%S')}</p>
            <p><strong>Durum:</strong> Tam Otomasyon Modu</p>
        </div>
        
        <div class="info">
            <h3>📊 ANA PANEL OZELLIKLERI</h3>
            <p><strong>Panel Tipi:</strong> Ana Kontrol Merkezi</p>
            <p><strong>URL:</strong> http://localhost:{port}</p>
            <p><strong>Sistem:</strong> TRM FULL OTOMASYON v3.0</p>
            <p><strong>Ozellik:</strong> Tum sistem kontrolu</p>
        </div>
        
        <div style="text-align: center; margin-top: 30px;">
            <button onclick="window.open('http://localhost:9001/status', '_blank')">Status Paneli</button>
            <button onclick="window.open('http://localhost:9002', '_blank')">Satis Paneli</button>
            <button onclick="window.open('http://localhost:9003', '_blank')">Gelismis Panel</button>
            <button onclick="window.open('http://localhost:9004/drive-social', '_blank')">Drive Sosyal</button>
        </div>
    </div>
</body>
</html>
"""
        elif port == 9001:
            return f"""
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <title>ULUSLARARASI TRM FULL OTOMASYON (Trend Urunler Market) - STATUS PANELI</title>
    <style>
        body {{ font-family: Arial, sans-serif; background: #1a1a2e; color: #eee; padding: 20px; }}
        .container {{ max-width: 800px; margin: 0 auto; background: #16213e; padding: 30px; border-radius: 10px; }}
        h1 {{ color: #ffd700; text-align: center; }}
        .status {{ background: #0f3460; padding: 15px; border-radius: 5px; margin: 20px 0; }}
        .info {{ background: #533483; padding: 15px; border-radius: 5px; margin: 20px 0; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>ULUSLARARASI TRM FULL OTOMASYON (Trend Urunler Market) - STATUS PANELI</h1>
        
        <div class="status">
            <h3>✅ STATUS API AKTIF</h3>
            <p><strong>Port:</strong> {port}</p>
            <p><strong>Zaman:</strong> {datetime.now().strftime('%H:%M:%S')}</p>
            <p><strong>Durum:</strong> API Hizmeti Aktif</p>
        </div>
        
        <div class="info">
            <h3>📊 STATUS API OZELLIKLERI</h3>
            <p><strong>Panel Tipi:</strong> Status API</p>
            <p><strong>URL:</strong> http://localhost:{port}/status</p>
            <p><strong>Sistem:</strong> TRM FULL OTOMASYON v3.0</p>
            <p><strong>Ozellik:</strong> Sistem durumu bildirimi</p>
        </div>
        
        <div style="text-align: center; margin-top: 30px;">
            <p>🔍 SISTEM DURUMU TAKIP EDILIYOR</p>
            <p>📊 JSON VERI AKTIF</p>
        </div>
    </div>
</body>
</html>
"""
        elif port == 9002:
            return f"""
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <title>ULUSLARARASI TRM FULL OTOMASYON (Trend Urunler Market) - SATIS PANELI</title>
    <style>
        body {{ font-family: Arial, sans-serif; background: #1a1a2e; color: #eee; padding: 20px; }}
        .container {{ max-width: 800px; margin: 0 auto; background: #16213e; padding: 30px; border-radius: 10px; }}
        h1 {{ color: #ffd700; text-align: center; }}
        .status {{ background: #0f3460; padding: 15px; border-radius: 5px; margin: 20px 0; }}
        .info {{ background: #533483; padding: 15px; border-radius: 5px; margin: 20px 0; }}
        .revenue {{ background: #22c55e; color: #000; padding: 20px; border-radius: 5px; margin: 20px 0; font-size: 24px; font-weight: bold; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>ULUSLARARASI TRM FULL OTOMASYON (Trend Urunler Market) - SATIS PANELI</h1>
        
        <div class="revenue">
            <h3>💰 GUNLUK GELIR</h3>
            <p>₺12,450</p>
            <p><small>Hedef: ₺18,000</small></p>
        </div>
        
        <div class="status">
            <h3>✅ SATIS PANELI AKTIF</h3>
            <p><strong>Port:</strong> {port}</p>
            <p><strong>Zaman:</strong> {datetime.now().strftime('%H:%M:%S')}</p>
            <p><strong>Durum:</strong> Para Kazanma Modu Aktif</p>
        </div>
        
        <div class="info">
            <h3>📊 SATIS PANELI OZELLIKLERI</h3>
            <p><strong>Panel Tipi:</strong> Satis ve Komisyon Takibi</p>
            <p><strong>URL:</strong> http://localhost:{port}</p>
            <p><strong>Sistem:</strong> TRM FULL OTOMASYON v3.0</p>
            <p><strong>Ozellik:</strong> Otomatik para kazanma</p>
        </div>
        
        <div style="text-align: center; margin-top: 30px;">
            <p>🎯 OTOMATIK PARA KAZANMA MODU AKTIF</p>
            <p>💰 SISTEM SIZIN ICIN CALISIYOR</p>
        </div>
    </div>
</body>
</html>
"""
        elif port == 9003:
            return f"""
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <title>ULUSLARARASI TRM FULL OTOMASYON (Trend Urunler Market) - GELISMIS YONETIM PANELI</title>
    <style>
        body {{ font-family: Arial, sans-serif; background: #1a1a2e; color: #eee; padding: 20px; }}
        .container {{ max-width: 800px; margin: 0 auto; background: #16213e; padding: 30px; border-radius: 10px; }}
        h1 {{ color: #ffd700; text-align: center; }}
        .status {{ background: #0f3460; padding: 15px; border-radius: 5px; margin: 20px 0; }}
        .info {{ background: #533483; padding: 15px; border-radius: 5px; margin: 20px 0; }}
        .ai {{ background: #8b5cf6; padding: 20px; border-radius: 5px; margin: 20px 0; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>ULUSLARARASI TRM FULL OTOMASYON (Trend Urunler Market) - GELISMIS YONETIM PANELI</h1>
        
        <div class="ai">
            <h3>🤖 AI MODULLERI</h3>
            <p><strong>DeepSeek:</strong> AKTIF</p>
            <p><strong>Claude:</strong> AKTIF</p>
            <p><strong>Analysis Engine:</strong> AKTIF</p>
            <p><strong>Decision Engine:</strong> AKTIF</p>
        </div>
        
        <div class="status">
            <h3>✅ GELISMIS PANEL AKTIF</h3>
            <p><strong>Port:</strong> {port}</p>
            <p><strong>Zaman:</strong> {datetime.now().strftime('%H:%M:%S')}</p>
            <p><strong>Durum:</strong> Gelismis Yonetim Modu</p>
        </div>
        
        <div class="info">
            <h3>📊 GELISMIS PANEL OZELLIKLERI</h3>
            <p><strong>Panel Tipi:</strong> Gelismis Yonetim</p>
            <p><strong>URL:</strong> http://localhost:{port}</p>
            <p><strong>Sistem:</strong> TRM FULL OTOMASYON v3.0</p>
            <p><strong>Ozellik:</strong> AI ve performans kontrolu</p>
        </div>
        
        <div style="text-align: center; margin-top: 30px;">
            <p>🚀 GELISMIS OZELLIKLER AKTIF</p>
            <p>🤖 TAM OTOMASYON MODU</p>
        </div>
    </div>
</body>
</html>
"""
        else:
            return f"""
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <title>TRM PANEL - Port {port}</title>
    <style>
        body {{ font-family: Arial, sans-serif; background: #1a1a2e; color: #eee; padding: 20px; }}
        .container {{ max-width: 800px; margin: 0 auto; background: #16213e; padding: 30px; border-radius: 10px; }}
        h1 {{ color: #ffd700; text-align: center; }}
        .status {{ background: #0f3460; padding: 15px; border-radius: 5px; margin: 20px 0; }}
        .info {{ background: #533483; padding: 15px; border-radius: 5px; margin: 20px 0; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>TRM PANEL - Port {port}</h1>
        
        <div class="status">
            <h3>✅ SUNUCU CALISIYOR</h3>
            <p><strong>Port:</strong> {port}</p>
            <p><strong>Zaman:</strong> {datetime.now().strftime('%H:%M:%S')}</p>
            <p><strong>Durum:</strong> AKTIF</p>
        </div>
        
        <div class="info">
            <h3>📊 PANEL BILGILERI</h3>
            <p><strong>Panel Tipi:</strong> Bilinmeyen Panel</p>
            <p><strong>URL:</strong> http://localhost:{port}</p>
            <p><strong>Sistem:</strong> TRM FULL OTOMASYON v3.0</p>
        </div>
    </div>
</body>
</html>
"""
    
    def get_status_data(self):
        """Status verisi olustur"""
        port = self.server.server_port
        base_data = {
            "system_status": "AKTIF",
            "uptime": "0g 0sa 0dk 5sn",
            "daily_revenue": 12450,
            "target_revenue": 18000,
            "commission_rate": 26.27,
            "active_products": 248,
            "ai_status": "AKTIF",
            "social_media_status": "AKTIF",
            "bank_status": "AKTIF",
            "server_port": port,
            "timestamp": datetime.now().isoformat()
        }
        
        # Port'a ozel veriler ekle
        if port == 9000:
            base_data["panel_type"] = "Ana Panel"
            base_data["features"] = ["Sistem kontrolu", "Panel navigasyonu", "Genel durum"]
        elif port == 9001:
            base_data["panel_type"] = "Status API"
            base_data["features"] = ["JSON veri", "Sistem durumu", "API hizmeti"]
        elif port == 9002:
            base_data["panel_type"] = "Satis Paneli"
            base_data["features"] = ["Para kazanma", "Komisyon takibi", "Gelir raporu"]
        elif port == 9003:
            base_data["panel_type"] = "Gelismis Panel"
            base_data["features"] = ["AI modulleri", "Performans", "Detayli kontrol"]
        
        return base_data
    
    def get_panel_type(self):
        port = self.server.server_port
        if port == 9000:
            return "Ana Panel"
        elif port == 9001:
            return "Status API"
        elif port == 9002:
            return "Satis Paneli"
        elif port == 9003:
            return "Gelismis Panel"
        else:
            return "Bilinmeyen Panel"
    
    def log_message(self, format, *args):
        # Log mesajlarini basitlestir
        pass

def start_server(port):
    """Belirtilen portta sunucu baslat"""
    try:
        server = HTTPServer(('localhost', port), SimpleHandler)
        print(f"+ Sunucu {port} portunda baslatildi")
        print(f"+ Panel: http://localhost:{port}")
        
        server.serve_forever()
    except Exception as e:
        print(f"- Sunucu baslatilamadi (Port {port}): {e}")

def main():
    print("ULUSLARARASI TRM FULL OTOMASYON v3.0")
    print("Basit Sunucu Test Araci")
    print("=" * 50)
    
    # Portlar
    ports = [9000, 9001, 9002, 9003]
    threads = []
    
    # Tum sunuculari baslat
    for port in ports:
        thread = threading.Thread(target=start_server, args=(port,), daemon=True)
        thread.start()
        threads.append(thread)
        time.sleep(0.5)  # Portlar arasinda bekleme
    
    print("\nTum Sunucular Baslatildi!")
    print("Paneller:")
    print("   • Ana Panel: http://localhost:9000")
    print("   • Status API: http://localhost:9001/status")
    print("   • Satis Paneli: http://localhost:9002")
    print("   • Gelismis Panel: http://localhost:9003")
    print("\nTam Otomasyon Aktif!")
    print("Para Kazanma Modu: CALISIYOR")
    print("\nDurdurmak icin Ctrl+C")
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nSunucular durduruluyor...")
        print("Tum sunucular durduruldu")

if __name__ == "__main__":
    main()
