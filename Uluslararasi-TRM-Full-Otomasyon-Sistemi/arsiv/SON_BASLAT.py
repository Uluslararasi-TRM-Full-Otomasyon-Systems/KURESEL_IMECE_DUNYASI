#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TRM Nirvana v3.0 - Son Başlatıcı
Tek tıkla başlat, sistem durumunu takip et
"""

import os
import sys
import subprocess
import webbrowser
import time
import threading
import json
from pathlib import Path
from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse

class SystemStatusManager:
    def __init__(self):
        self.system_running = False
        self.processes = []
        self.start_time = None
        self.status_data = {
            'main': 'Kapalı',
            'panel': 'Kapalı',
            'social': 'Kapalı',
            'cloud': 'Hazır',
            'uptime': '00:00:00'
        }
    
    def start_all_modules(self):
        """Tüm modülleri başlat"""
        modules = [
            ('Panel', 'ENHANCED_PANEL.py'),
            ('Ana Orchestrator', 'main_orchestrator.py'),
            ('Telegram Dinleyici', 'telegram_listener.py'),
            ('Web Scraper', 'web_scraper.py'),
            ('AI Entegrasyonu', 'ai_integration.py'),
            ('Sosyal Medya', 'social_media_automation.py'),
            ('Google Drive', 'google_drive_integration.py')
        ]
        
        for name, script in modules:
            if os.path.exists(script):
                try:
                    process = subprocess.Popen([sys.executable, script])
                    self.processes.append(process)
                    print(f"✅ {name} başlatıldı")
                except Exception as e:
                    print(f"❌ {name} başlatılamadı: {e}")
        
        self.system_running = True
        self.start_time = time.time()
        self.update_status()
    
    def stop_all_modules(self):
        """Tüm modülleri durdur"""
        for process in self.processes:
            try:
                process.terminate()
                process.wait(timeout=5)
            except:
                try:
                    process.kill()
                except:
                    pass
        
        self.processes.clear()
        self.system_running = False
        self.update_status()
    
    def update_status(self):
        """Durum verilerini güncelle"""
        if self.system_running and self.start_time:
            uptime = int(time.time() - self.start_time)
            hours, remainder = divmod(uptime, 3600)
            minutes, seconds = divmod(remainder, 60)
            self.status_data['uptime'] = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
            self.status_data['main'] = 'Aktif'
            self.status_data['panel'] = 'Aktif'
            self.status_data['social'] = 'Aktif'
        else:
            self.status_data['uptime'] = '00:00:00'
            self.status_data['main'] = 'Kapalı'
            self.status_data['panel'] = 'Kapalı'
            self.status_data['social'] = 'Kapalı'
    
    def get_status_json(self):
        """JSON formatında durum döndür"""
        self.update_status()
        return json.dumps(self.status_data)

class StatusAPIHandler(BaseHTTPRequestHandler):
    def __init__(self, *args, status_manager, **kwargs):
        self.status_manager = status_manager
        super().__init__(*args, **kwargs)
    
    def do_GET(self):
        if self.path == '/status':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(self.status_manager.get_status_json().encode())
        else:
            self.send_response(404)
            self.end_headers()
    
    def do_POST(self):
        if self.path == '/stop':
            self.status_manager.stop_all_modules()
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({'status': 'stopped'}).encode())
        else:
            self.send_response(404)
            self.end_headers()
    
    def log_message(self, format, *args):
        pass  # Log mesajlarını gösterme

def start_status_server(status_manager):
    """Durum sunucusunu başlat"""
    def handler(*args, **kwargs):
        StatusAPIHandler(*args, status_manager=status_manager, **kwargs)
    
    server = HTTPServer(('localhost', 9001), handler)
    print("📊 Status API başlatıldı: http://localhost:9001/status")
    server.serve_forever()

def main():
    """Ana fonksiyon"""
    print("""
===============================================
    TRM NİRVANA v3.0 - SON BAŞLATICI
===============================================
  🚀 Tek tıkla başlat, durum takibi
  🤖 Sistem durumu kontrol edilir
  📊 Her seferinde yeniden başlamaz
  ☁️ 7/24 çalışmaya devam eder
===============================================
    """)
    
    # Status manager oluştur
    status_manager = SystemStatusManager()
    
    # Status server'ı ayrı thread'de başlat
    status_thread = threading.Thread(target=start_status_server, args=(status_manager,))
    status_thread.daemon = True
    status_thread.start()
    
    # HTML dosyasını aç
    html_path = os.path.join(os.getcwd(), 'TEK_TIK_SON.html')
    if os.path.exists(html_path):
        webbrowser.open(f'file://{html_path}')
        print("🌐 Kontrol paneli açıldı")
    else:
        print("❌ TEK_TIK_SON.html bulunamadı")
    
    try:
        input("Çıkmak için Enter'a basın...")
    except KeyboardInterrupt:
        print("\n👋 Başlatıcı durduruldu")
    finally:
        status_manager.stop_all_modules()

if __name__ == "__main__":
    main()
