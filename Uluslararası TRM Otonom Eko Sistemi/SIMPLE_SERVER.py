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
            
            # Her port için farklı içerik oluştur
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
        """Her port için özel HTML içerik oluştur"""
        port = self.server.server_port
        
        if port == 9000:
            return f"""
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <title>ULUSLARARASI TRM FULL OTOMASYON - ANA (Trend Ürünler Market) PANELİ</title>
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
        <h1>ULUSLARARASI TRM FULL OTOMASYON - ANA (Trend Ürünler Market) PANELİ</h1>
        
        <div class="status">
            <h3>✅ ANA PANEL AKTIF</h3>
            <p><strong>Port:</strong> {port}</p>
            <p><strong>Zaman:</strong> {datetime.now().strftime('%H:%M:%S')}</p>
            <p><strong>Durum:</strong> Tam Otomasyon Modu</p>
        </div>
        
        <div class="info">
            <h3>📊 ANA PANEL ÖZELLİKLERİ</h3>
            <p><strong>Panel Tipi:</strong> Ana Kontrol Merkezi</p>
            <p><strong>URL:</strong> http://localhost:{port}</p>
            <p><strong>Sistem:</strong> TRM FULL OTOMASYON v3.0</p>
            <p><strong>Özellik:</strong> Tüm sistem kontrolü</p>
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
    <title>ULUSLARARASI TRM FULL OTOMASYON (Trend Ürünler Market) - STATUS PANELİ</title>
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
        <h1>ULUSLARARASI TRM FULL OTOMASYON (Trend Ürünler Market) - STATUS PANELİ</h1>
        
        <div class="status">
            <h3>✅ STATUS API AKTIF</h3>
            <p><strong>Port:</strong> {port}</p>
            <p><strong>Zaman:</strong> {datetime.now().strftime('%H:%M:%S')}</p>
            <p><strong>Durum:</strong> API Hizmeti Aktif</p>
        </div>
        
        <div class="info">
            <h3>📊 STATUS API ÖZELLİKLERİ</h3>
            <p><strong>Panel Tipi:</strong> Status API</p>
            <p><strong>URL:</strong> http://localhost:{port}/status</p>
            <p><strong>Sistem:</strong> TRM FULL OTOMASYON v3.0</p>
            <p><strong>Özellik:</strong> Sistem durumu bildirimi</p>
        </div>
        
        <div style="text-align: center; margin-top: 30px;">
            <p>🔍 SİSTEM DURUMU TAKİP EDİLİYOR</p>
            <p>📊 JSON VERİ AKTİF</p>
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
    <title>ULUSLARARASI TRM FULL OTOMASYON (Trend Ürünler Market) - SATIŞ PANELİ</title>
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
        <h1>ULUSLARARASI TRM FULL OTOMASYON (Trend Ürünler Market) - SATIŞ PANELİ</h1>
        
        <div class="revenue">
            <h3>💰 GÜNLÜK GELİR</h3>
            <p>₺12,450</p>
            <p><small>Hedef: ₺18,000</small></p>
        </div>
        
        <div class="status">
            <h3>✅ SATIŞ PANELİ AKTIF</h3>
            <p><strong>Port:</strong> {port}</p>
            <p><strong>Zaman:</strong> {datetime.now().strftime('%H:%M:%S')}</p>
            <p><strong>Durum:</strong> Para Kazanma Modu Aktif</p>
        </div>
        
        <div class="info">
            <h3>📊 SATIŞ PANELİ ÖZELLİKLERİ</h3>
            <p><strong>Panel Tipi:</strong> Satış ve Komisyon Takibi</p>
            <p><strong>URL:</strong> http://localhost:{port}</p>
            <p><strong>Sistem:</strong> TRM FULL OTOMASYON v3.0</p>
            <p><strong>Özellik:</strong> Otomatik para kazanma</p>
        </div>
        
        <div style="text-align: center; margin-top: 30px;">
            <p>🎯 OTOMATİK PARA KAZANMA MODU AKTİF</p>
            <p>💰 SİSTEM SİZİN İÇİN ÇALIŞIYOR</p>
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
    <title>ULUSLARARASI TRM FULL OTOMASYON (Trend Ürünler Market) - GELİŞMİŞ YÖNETİM PANELİ</title>
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
        <h1>ULUSLARARASI TRM FULL OTOMASYON (Trend Ürünler Market) - GELİŞMİŞ YÖNETİM PANELİ</h1>
        
        <div class="ai">
            <h3>🤖 AI MODÜLLERİ</h3>
            <p><strong>DeepSeek:</strong> AKTİF</p>
            <p><strong>Claude:</strong> AKTİF</p>
            <p><strong>Analysis Engine:</strong> AKTİF</p>
            <p><strong>Decision Engine:</strong> AKTİF</p>
        </div>
        
        <div class="status">
            <h3>✅ GELİŞMİŞ PANEL AKTIF</h3>
            <p><strong>Port:</strong> {port}</p>
            <p><strong>Zaman:</strong> {datetime.now().strftime('%H:%M:%S')}</p>
            <p><strong>Durum:</strong> Gelişmiş Yönetim Modu</p>
        </div>
        
        <div class="info">
            <h3>📊 GELİŞMİŞ PANEL ÖZELLİKLERİ</h3>
            <p><strong>Panel Tipi:</strong> Gelişmiş Yönetim</p>
            <p><strong>URL:</strong> http://localhost:{port}</p>
            <p><strong>Sistem:</strong> TRM FULL OTOMASYON v3.0</p>
            <p><strong>Özellik:</strong> AI ve performans kontrolü</p>
        </div>
        
        <div style="text-align: center; margin-top: 30px;">
            <p>🚀 GELİŞMİŞ ÖZELLİKLER AKTİF</p>
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
        """Status verisi oluştur"""
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
        
        # Port'a özel veriler ekle
        if port == 9000:
            base_data["panel_type"] = "Ana Panel"
            base_data["features"] = ["Sistem kontrolü", "Panel navigasyonu", "Genel durum"]
        elif port == 9001:
            base_data["panel_type"] = "Status API"
            base_data["features"] = ["JSON veri", "Sistem durumu", "API hizmeti"]
        elif port == 9002:
            base_data["panel_type"] = "Satis Paneli"
            base_data["features"] = ["Para kazanma", "Komisyon takibi", "Gelir raporu"]
        elif port == 9003:
            base_data["panel_type"] = "Gelismis Panel"
            base_data["features"] = ["AI modülleri", "Performans", "Detaylı kontrol"]
        
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
        # Log mesajlarını basitleştir
        pass

def start_server(port):
    """Belirtilen portta sunucu başlat"""
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
    
    # Tüm sunucuları başlat
    for port in ports:
        thread = threading.Thread(target=start_server, args=(port,), daemon=True)
        thread.start()
        threads.append(thread)
        time.sleep(0.5)  # Portlar arasında bekleme
    
    print("\nTum Sunucular Baslatildi!")
    print("Paneller:")
    print("   • Ana Panel: http://localhost:9000")
    print("   • Status API: http://localhost:9001/status")
    print("   • Satis Paneli: http://localhost:9002")
    print("   • Gelismis Panel: http://localhost:9003")
    print("\nTam Otomasyon Aktif!")
    print("Para Kazanma Modu: CALISIYOR")
    print("\nDurdurmak için Ctrl+C")
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nSunucular durduruluyor...")
        print("Tum sunucular durduruldu")

if __name__ == "__main__":
    main()
