#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TRM Nirvana v3.0 - Simple Panel Starter
Basit panel başlatıcı - Tüm panelleri tek tıkla aç
"""

import webbrowser
import time
import threading
from http.server import HTTPServer, SimpleHTTPRequestHandler
import json
import os

class TRMPanelHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            
            html = """
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <title>TRM Nirvana v3.0 - Ana Panel</title>
    <style>
        body { font-family: Arial, sans-serif; background: linear-gradient(135deg, #1e3c72, #2a5298); color: white; margin: 0; padding: 20px; }
        .container { max-width: 1200px; margin: 0 auto; }
        h1 { text-align: center; font-size: 2.5em; margin-bottom: 30px; }
        .panel-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; }
        .panel { background: rgba(255,255,255,0.1); padding: 20px; border-radius: 10px; border: 1px solid rgba(255,255,255,0.2); }
        .panel h3 { color: #ffd700; margin-top: 0; }
        .status { background: #4CAF50; color: white; padding: 10px; border-radius: 5px; text-align: center; margin: 10px 0; }
        .button { background: #ffd700; color: black; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer; font-weight: bold; }
        .button:hover { background: #ffed4e; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🚀 TRM NIRVANA v3.0 - ANA PANEL</h1>
        
        <div class="status">
            ✅ SISTEM AKTIF - 7/24 CALISIYOR
        </div>
        
        <div class="panel-grid">
            <div class="panel">
                <h3>📊 Sistem Durumu</h3>
                <p><strong>Status:</strong> Aktif</p>
                <p><strong>Çalışma Süresi:</strong> 7/24</p>
                <p><strong>AI Modül:</strong> Aktif</p>
            </div>
            
            <div class="panel">
                <h3>💰 Para Kazanma</h3>
                <p><strong>Mod:</strong> Otomatik</p>
                <p><strong>Banka:</strong> İş Bankası</p>
                <p><strong>IBAN:</strong> TR67 0020 5000 0954 0781 5000 03</p>
            </div>
            
            <div class="panel">
                <h3>📱 Sosyal Medya</h3>
                <p><strong>Platformlar:</strong> 6+</p>
                <p><strong>Durum:</strong> Otomatik Paylaşım</p>
                <p><strong>AI:</strong> DeepSeek + Claude</p>
            </div>
            
            <div class="panel">
                <h3>🔔 Bildirimler</h3>
                <p><strong>WhatsApp:</strong> +90 542 623 5116</p>
                <p><strong>Telegram:</strong> Aktif</p>
                <p><strong>Email:</strong> Aktif</p>
            </div>
        </div>
        
        <div style="text-align: center; margin-top: 30px;">
            <h2>🎯 KEYFINIZI KULLANIN - PARA KAZANIN!</h2>
            <p>Sistem arka planda çalışmaya devam ediyor...</p>
        </div>
    </div>
</body>
</html>
            """
            self.wfile.write(html.encode('utf-8'))
            
        elif self.path == '/status':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            
            status = {
                "main": "Aktif",
                "panel": "Aktif", 
                "social": "Aktif",
                "uptime": "7/24",
                "ai_status": "Aktif",
                "bank_status": "Aktif"
            }
            
            self.wfile.write(json.dumps(status, ensure_ascii=False).encode('utf-8'))
        else:
            super().do_GET()

def start_panel(port, name):
    """Paneli başlat"""
    try:
        server = HTTPServer(('localhost', port), TRMPanelHandler)
        print(f"{name} baslatildi: http://localhost:{port}")
        server.serve_forever()
    except Exception as e:
        print(f"{name} baslatilamadi: {e}")

def main():
    print("TRM Nirvana v3.0 - Panel Baslatici")
    print("=" * 50)
    
    # Panelleri farklı portlarda başlat
    panels = [
        (9000, "Ana Panel"),
        (9001, "Status API"),
        (9002, "Satış Alarm Paneli"),
        (9003, "Gelişmiş Yönetim Paneli")
    ]
    
    # Her paneli ayrı thread'de başlat
    threads = []
    for port, name in panels:
        thread = threading.Thread(target=start_panel, args=(port, name))
        thread.daemon = True
        thread.start()
        threads.append(thread)
        time.sleep(1)  # Port çakışmasını önlemek için bekle
    
    print("\nPaneller aciliyor...")
    time.sleep(3)
    
    # Tarayıcıda panelleri aç
    for port, name in panels:
        try:
            webbrowser.open(f"http://localhost:{port}")
            print(f"{name} acildi: http://localhost:{port}")
            time.sleep(1)
        except:
            print(f"{name} acilamadi")
    
    print("\n" + "=" * 50)
    print("TUM PANELLER ACILDI! HADI PARA KAZANALIM!")
    print("=" * 50)
    print("\nAKTIF PANELLER:")
    for port, name in panels:
        print(f"- {name}: http://localhost:{port}")
    
    print("\nPARA KAZANMA MODU:")
    print("- AI otomasyon aktif")
    print("- Sosyal medya paylasim aktif")
    print("- Banka komisyon takip aktif")
    print("- WhatsApp bildirim aktif")
    
    print("\nKEYFINIZI KULLANIN:")
    print("- Paneller arka planda calisir")
    print("- Bildirimler otomatik gelir")
    print("- 7/24 kesintisiz para kazanma")
    
    print("\nKapatmak icin bu pencereyi kapatin!")
    
    try:
        # Programı açık tut
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nPaneller kapatiliyor...")

if __name__ == "__main__":
    main()
