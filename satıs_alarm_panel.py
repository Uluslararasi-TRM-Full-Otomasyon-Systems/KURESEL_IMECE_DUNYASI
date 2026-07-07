#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TRM Nirvana v3.0 - SatÄ±Å Alarm Paneli
Panel Ã¼zerinden satÄ±Å alarm ve uyarÄ±larÄ±nÄ± gÃ¶sterir
"""

import asyncio
import json
import os
from datetime import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs
import threading

class SalesAlertHandler(BaseHTTPRequestHandler):
    def __init__(self, *args, alarm_system, **kwargs):
        self.alarm_system = alarm_system
        super().__init__(*args, **kwargs)
    
    def do_GET(self):
        """GET isteklerini yÃ¶net"""
        if self.path == '/':
            self.send_html_response()
        elif self.path == '/alerts':
            self.send_alerts_response()
        elif self.path == '/sales-summary':
            self.send_sales_summary_response()
        elif self.path == '/status':
            self.send_status_response()
        else:
            self.send_404()
    
    def do_POST(self):
        """POST isteklerini yÃ¶net"""
        if self.path == '/test-alert':
            self.send_test_alert_response()
        else:
            self.send_404()
    
    def send_html_response(self):
        """HTML paneli gÃ¶nder"""
        html_content = """
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <title>ULUSLARARASI TRM FULL OTOMASYON (Trend Ürünler Market) PANELÝ</title>
    <style>
        *{margin:0;padding:0;box-sizing:border-box;}
        body{background:radial-gradient(circle at 20%30%,#0a0f1e,#03060c);font-family:'Segoe UI',system-ui;color:#eef;padding:20px;}
        .container{max-width:1200px;margin:0 auto;background:rgba(15,22,36,0.85);backdrop-filter:blur(20px);border-radius:2rem;padding:2rem;border:1px solid rgba(255,170,51,0.4);}
        h1{font-size:2rem;font-weight:800;background:linear-gradient(135deg,#ffd966,#ffaa33,#ffdd99,#ffcc66);-webkit-background-clip:text;background-clip:text;color:transparent;text-align:center;margin-bottom:2rem;}
        .alert-grid{display:grid;grid-template-columns:1fr 1fr;gap:20px;margin-bottom:30px;}
        .alert-card{background:#0a0f18cc;border-radius:20px;padding:20px;border:1px solid #2a3344;transition:transform 0.3s;}
        .alert-card:hover{transform:scale(1.02);border-color:#ffaa55;}
        .alert-success{border-left:5px solid #22c55e;background:rgba(34,197,94,0.1);}
        .alert-warning{border-left:5px solid #f59e0b;background:rgba(245,158,11,0.1);}
        .alert-info{border-left:5px solid #3b82f6;background:rgba(59,130,246,0.1);}
        .alert-title{color:#ffdd99;font-size:1.2rem;font-weight:bold;margin-bottom:10px;}
        .alert-message{color:#eef;margin-bottom:10px;}
        .alert-time{color:#ffaa88;font-size:0.9rem;}
        .stats-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:15px;margin:30px 0;}
        .stat-card{background:#1e2a3a;border-radius:15px;padding:20px;text-align:center;border:1px solid #ffaa5544;}
        .stat-value{font-size:2rem;font-weight:bold;color:#ffd966;}
        .stat-label{color:#ffaa88;margin-top:5px;}
        .refresh-btn{background:#1e2a3a;border:2px solid #ffaa55;color:#fff;padding:10px 20px;border-radius:10px;cursor:pointer;margin:10px 0;}
        .refresh-btn:hover{background:#ffaa33;color:#000;}
        .pulse{animation:pulse 2s infinite;}
        @keyframes pulse{0%,100%{opacity:1;}50%{opacity:0.7;}
        .loading{display:none;text-align:center;padding:20px;}
        .loading.active{display:block;}
        .spinner{border:4px solid rgba(255,170,51,0.3);border-top:4px solid #ffaa33;border-radius:50%;width:40px;height:40px;animation:spin 1s linear infinite;margin:0 auto;}
        @keyframes spin{0%{transform:rotate(0deg);}100%{transform:rotate(360deg);}}
    </style>
</head>
<body>
<div class="container">
    <h1>ð¨ ULUSLARARASI TRM FULL OTOMASYON (Trend Ürünler Market) PANELÝ</h1>
    
    <div class="stats-grid" id="stats-grid">
        <div class="stat-card">
            <div class="stat-value" id="total-products">0</div>
            <div class="stat-label">ð¦ Toplam ÃrÃ¼n</div>
        </div>
        <div class="stat-card">
            <div class="stat-value" id="high-commission">0</div>
            <div class="stat-label">ð¥ %20+ ÃrÃ¼n</div>
        </div>
        <div class="stat-card">
            <div class="stat-value" id="social-published">0</div>
            <div class="stat-label">ð± Sosyal PaylaÅÄ±m</div>
        </div>
        <div class="stat-card">
            <div class="stat-value" id="estimated-commission">0 TL</div>
            <div class="stat-label">ð° Tahmini Komisyon</div>
        </div>
    </div>

    <div style="text-align:center;margin:20px 0;">
        <button class="refresh-btn" onclick="refreshData()">ð Veriyi Yenile</button>
        <button class="refresh-btn" onclick="testAlert()">ð§ª Test Alert</button>
    </div>

    <div class="loading" id="loading">
        <div class="spinner"></div>
        <p style="color:#ffdd99;margin-top:10px;">Veriler yÃ¼kleniyor...</p>
    </div>

    <div class="alert-grid" id="alerts-container">
        <!-- Alert'ler buraya yÃ¼klenecek -->
    </div>

    <div style="text-align:center;margin-top:30px;font-size:14px;color:#ffaa88;">
        ð¨ SatÄ±Å alarm sistemi aktif | ð Otomatik gÃ¼ncelleme | ð± AnlÄ±k bildirimler
    </div>
</div>

<script>
let refreshInterval;

function showLoading() {
    document.getElementById('loading').classList.add('active');
    document.getElementById('alerts-container').style.display = 'none';
}

function hideLoading() {
    document.getElementById('loading').classList.remove('active');
    document.getElementById('alerts-container').style.display = 'grid';
}

async function loadAlerts() {
    try {
        const response = await fetch('/alerts');
        const alerts = await response.json();
        
        const container = document.getElementById('alerts-container');
        container.innerHTML = '';
        
        if (alerts.length === 0) {
            container.innerHTML = '<div style="text-align:center;color:#ffaa88;padding:40px;">ð HenÃ¼z alert bulunmuyor</div>';
            return;
        }
        
        alerts.forEach(alert => {
            const alertCard = createAlertCard(alert);
            container.appendChild(alertCard);
        });
        
    } catch (error) {
        console.error('Alert yÃ¼klenemedi:', error);
    }
}

function createAlertCard(alert) {
    const card = document.createElement('div');
    card.className = `alert-card alert-${alert.level}`;
    
    const time = new Date(alert.timestamp).toLocaleString('tr-TR');
    
    card.innerHTML = `
        <div class="alert-title">${alert.title}</div>
        <div class="alert-message">${alert.message}</div>
        <div class="alert-time">ð ${time}</div>
    `;
    
    return card;
}

async function loadStats() {
    try {
        const response = await fetch('/sales-summary');
        const stats = await response.json();
        
        document.getElementById('total-products').textContent = stats.total_products || 0;
        document.getElementById('high-commission').textContent = stats.total_high_commission || 0;
        document.getElementById('social-published').textContent = stats.total_social_published || 0;
        document.getElementById('estimated-commission').textContent = `${stats.total_commission || 0} TL`;
        
    } catch (error) {
        console.error('Ä°statistikler yÃ¼klenemedi:', error);
    }
}

async function refreshData() {
    showLoading();
    
    try {
        await Promise.all([loadAlerts(), loadStats()]);
    } finally {
        hideLoading();
    }
}

async function testAlert() {
    try {
        const response = await fetch('/test-alert', { method: 'POST' });
        const result = await response.json();
        
        if (result.success) {
            alert('ð§ª Test alert gÃ¶nderildi! Paneli yenileyin.');
            setTimeout(refreshData, 2000);
        }
    } catch (error) {
        console.error('Test alert hatasÄ±:', error);
    }
}

// Sayfa yÃ¼klendiÄinde verileri yÃ¼kle
document.addEventListener('DOMContentLoaded', function() {
    refreshData();
    
    // Her 30 saniyede bir verileri yenile
    refreshInterval = setInterval(refreshData, 30000);
});

// Sayfa kapatÄ±ldÄ±ÄÄ±nda temizle
window.addEventListener('beforeunload', function() {
    if (refreshInterval) {
        clearInterval(refreshInterval);
    }
});
</script>
</body>
</html>
        """
        
        self.send_response(200, 'text/html', html_content)
    
    def send_alerts_response(self):
        """Alert'leri gÃ¶nder"""
        try:
            alerts = self.alarm_system.get_recent_alerts(20)
            self.send_response(200, 'application/json', json.dumps(alerts))
        except Exception as e:
            self.send_response(500, 'application/json', json.dumps({'error': str(e)}))
    
    def send_sales_summary_response(self):
        """SatÄ±Å Ã¶zetini gÃ¶nder"""
        try:
            summary = self.alarm_system.get_sales_summary()
            self.send_response(200, 'application/json', json.dumps(summary))
        except Exception as e:
            self.send_response(500, 'application/json', json.dumps({'error': str(e)}))
    
    def send_status_response(self):
        """Durum gÃ¶nder"""
        try:
            status = {
                'system': 'active',
                'alerts_count': len(self.alarm_system.alerts),
                'last_update': datetime.now().isoformat()
            }
            self.send_response(200, 'application/json', json.dumps(status))
        except Exception as e:
            self.send_response(500, 'application/json', json.dumps({'error': str(e)}))
    
    def send_test_alert_response(self):
        """Test alert gÃ¶nder"""
        try:
            # Test alert oluÅtur
            test_alert = {
                'type': 'test',
                'level': 'info',
                'title': 'ð§ª Test Alert!',
                'message': 'Bu bir test alarmÄ±dÄ±r. Sistem Ã§alÄ±ÅÄ±yor.',
                'timestamp': datetime.now().isoformat(),
                'data': {'test': True}
            }
            
            self.alarm_system.alerts.append(test_alert)
            
            self.send_response(200, 'application/json', json.dumps({'success': True}))
        except Exception as e:
            self.send_response(500, 'application/json', json.dumps({'error': str(e)}))
    
    def send_response(self, status_code, content_type, content):
        """HTTP yanÄ±tÄ± gÃ¶nder"""
        self.send_response(status_code, content_type, content)
    
    def log_message(self, format, *args):
        pass  # Log mesajlarÄ±nÄ± gÃ¶sterme

class SalesAlertServer:
    def __init__(self):
        self.alarm_system = None
        self.server = None
    
    async def start(self, port=9002):
        """Sunucuyu baÅlat"""
        try:
            # SatÄ±Å alarm sistemini baÅlat
            from SATIS_ALARM_SISTEMI import SalesAlarmSystem
            self.alarm_system = SalesAlarmSystem()
            
            # Sunucuyu oluÅtur
            handler = lambda *args, **kwargs: SalesAlertHandler(*args, alarm_system=self.alarm_system, **kwargs)
            self.server = HTTPServer(('localhost', port), handler)
            
            # Sunucuyu ayrÄ± thread'de baÅlat
            server_thread = threading.Thread(target=self.server.serve_forever)
            server_thread.daemon = True
            server_thread.start()
            
            print(f"ð¨ SatÄ±Å Alarm Paneli baÅlatÄ±ldÄ±: http://localhost:{port}")
            return True
            
        except Exception as e:
            print(f"â SatÄ±Å alarm paneli baÅlatÄ±lamadÄ±: {e}")
            return False
    
    def stop(self):
        """Sunucuyu durdur"""
        if self.server:
            self.server.shutdown()
            self.server.server_close()

# Ana baÅlatÄ±cÄ±
async def main():
    """Ana fonksiyon"""
    print("""
===============================================
    TRM NIRVANA v3.0 - SATIS ALARM PANELI
===============================================
  ð¨ SatÄ±Å hareketleri takibi
  ð± AnlÄ±k bildirimler
  ð GerÃ§ek zamanlÄ± istatistikler
  ð Otomatik gÃ¼ncelleme
===============================================
    """)
    
    server = SalesAlertServer()
    
    if await server.start():
        print("ð¨ SatÄ±Å alarm sistemi aktif!")
        print("ð Panel: http://localhost:9002")
        print("ð Ana panel: http://localhost:9000")
        
        try:
            # ProgramÄ± aÃ§Ä±k tut
            while True:
                await asyncio.sleep(1)
        except KeyboardInterrupt:
            print("\nð SatÄ±Å alarm paneli durduruluyor...")
            server.stop()

if __name__ == "__main__":
    asyncio.run(main())
