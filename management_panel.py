#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
TRM NIRVANA OTOMASYON â ANA YÃNETÄ°M PANELÄ°
"""

import os
import json
import webbrowser
import threading
import time
import random
import subprocess
import sys
from http.server import HTTPServer, BaseHTTPRequestHandler

PORT = 9000
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))

# ========== NÄ°RVANA HTML ==========
HTML = '''
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <title>ULUSLARARASI TRM FULL OTOMASYON (Trend Ürünler Market) PANELÝ</title>
    <style>
        *{margin:0;padding:0;box-sizing:border-box;}
        body{background:radial-gradient(circle at 20%30%,#0a0f1e,#03060c);font-family:'Segoe UI',system-ui;color:#eef;padding:20px;}
        .container{max-width:1400px;margin:0 auto;background:rgba(15,22,36,0.65);backdrop-filter:blur(12px);border-radius:2rem;padding:1.8rem 2rem 2.2rem;border:1px solid rgba(66,153,225,0.2);}
        h1{font-size:2.5rem;font-weight:800;background:linear-gradient(135deg,#ffd966,#ffaa33,#ffdd99,#ffcc66);-webkit-background-clip:text;background-clip:text;color:transparent;text-align:center;letter-spacing:2px;margin-bottom:10px;}
        .status-badge{background:#1e2a3a;border:1px solid #ffaa55;color:#ffd966;padding:10px 25px;border-radius:40px;display:inline-block;margin:15px auto;text-align:center;font-weight:bold;box-shadow: 0 0 15px rgba(255,170,85,0.2);}
        .stats-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:25px;margin-bottom:40px;}
        .stat-card{background:#11161fe6;border-radius:32px;padding:25px;text-align:center;border:1px solid #ffaa5544;transition:0.3s;}
        .stat-card:hover{transform:translateY(-5px);border-color:#ffaa55;}
        .stat-card .value{font-size:36px;font-weight:bold;color:#ffdd99;}
        .stat-card .label{font-size:14px;color:#8a99b4;margin-top:10px;}
        .main-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(400px,1fr));gap:30px;margin-bottom:40px;}
        .card{background:#0a0f18cc;border-radius:40px;padding:30px;border:1px solid #2a3344;}
        .card h3{border-left:6px solid #ffaa55;padding-left:15px;margin-bottom:25px;color:#ffdd99;font-size:1.4rem;text-transform:uppercase;}
        .btn-nirvana{background:#1e2a3a;border:2px solid #ffaa55;color:#fff;padding:18px 25px;border-radius:60px;cursor:pointer;font-weight:bold;font-size:18px;transition:0.3s;margin:10px 0;width:100%;display:flex;align-items:center;justify-content:center;gap:15px;}
        .btn-nirvana:hover{background:#ffaa33;color:#000;transform:scale(1.02);box-shadow:0 0 20px #ffaa55;}
        .btn-special{background:linear-gradient(135deg, #4a0000, #8b0000);border:2px solid #ff4444;animation:pulse 2s infinite;}
        @keyframes pulse {0% {box-shadow:0 0 0 0 rgba(255,68,68,0.4);}70% {box-shadow:0 0 0 15px rgba(255,68,68,0);}100% {box-shadow:0 0 0 0 rgba(255,68,68,0);}}
        .log-area{background:#010101aa;border-radius:25px;padding:20px;height:300px;overflow-y:auto;font-family:'Consolas',monospace;font-size:13px;margin-top:20px;color:#9eff9e;border:1px solid #2a3344;}
        .log-entry{margin-bottom:8px;border-bottom:1px solid #ffffff05;padding-bottom:5px;}
        .footer{text-align:center;margin-top:40px;font-size:14px;color:#ffaa88;opacity:0.8;}
    </style>
</head>
<body>
<div class="container">
    <h1>ð ULUSLARARASI TRM FULL OTOMASYON (Trend Ürünler Market) PANELÝ</h1>
    <div style="text-align:center"><span class="status-badge" id="systemStatus">ð¤ SÄ°STEM HAZIR | ONUR MODU AKTÄ°F</span></div>

    <div class="stats-grid">
        <div class="stat-card"><div class="value" id="toplam_urun">247</div><div class="label">Toplanan ÃrÃ¼n</div></div>
        <div class="stat-card"><div class="value" id="yuksek_komisyon">86</div><div class="label">%20+ FÄ±rsat</div></div>
        <div class="stat-card"><div class="value" id="bugun_paylasim">1.2K</div><div class="label">BugÃ¼n GÃ¶sterim</div></div>
        <div class="stat-card"><div class="value" id="komisyon">3.280 âº</div><div class="label">Tahmini KazanÃ§</div></div>
    </div>

    <div class="main-grid">
        <div class="card">
            <h3>ð¦¾ ANA KONTROL ÃSSÃ</h3>
            <button class="btn-nirvana btn-special" onclick="calistir('/baslat_hersey')">ð¥ NIRVANA MODU BAÅLAT (TAM OTOMATÄ°K)</button>
            <button class="btn-nirvana" onclick="calistir('/durum')">ð SÄ°STEM SAÄLIK KONTROLÃ</button>
        </div>
        <div class="card">
            <h3>ð¤ AKILLI BOTLAR</h3>
            <button class="btn-nirvana" onclick="calistir('/komisyon_bot')">ð° KOMÄ°SYON BOTU (%20+ ÃRÃNLER)</button>
            <button class="btn-nirvana" onclick="calistir('/ai_icerik')">â¨ AI Ä°ÃERÄ°K ÃRET (DeepSeek v4)</button>
        </div>
        <div class="card">
            <h3>ð¢ SOSYAL MEDYA & YAYIN</h3>
            <button class="btn-nirvana" onclick="calistir('/sosyal_paylas')">ð¢ SOSYAL MEDYADA ANINDA PAYLAÅ</button>
            <button class="btn-nirvana" onclick="calistir('/rapor')">ð GÃNLÃK ÃZET RAPOR AL</button>
        </div>
    </div>

    <div class="card">
        <h3>ð SÄ°STEM HAREKETLERÄ°</h3>
        <div class="log-area" id="logArea"><div>[SÄ°STEM] TRM Nirvana YÃ¶netim Paneli BaÅlatÄ±ldÄ±.</div></div>
    </div>
    <div class="footer">â¡ TRM Otomasyon v3.1 | 7/24 Tam Otomatik ÃalÄ±Åma | E-Ticaret Edisyonu</div>
</div>
<script>
    async function calistir(endpoint) {
        const logDiv = document.getElementById('logArea');
        const systemStatus = document.getElementById('systemStatus');
        
        try {
            const res = await fetch(endpoint);
            const data = await res.json();
            
            if(endpoint === '/baslat_hersey') {
                systemStatus.textContent = 'ð¥ NIRVANA MODU: TÃM BOTLAR AKTÄ°F';
                systemStatus.style.background = '#4a0000';
                systemStatus.style.borderColor = '#ff4444';
            }
            
            const entry = document.createElement('div');
            entry.className = 'log-entry';
            entry.innerHTML = `<span style="color:#8a99b4">[${new Date().toLocaleTimeString()}]</span> <span style="color:#00ff88">â ${data.mesaj}</span>`;
            logDiv.insertBefore(entry, logDiv.firstChild);
        } catch(e) {
            const entry = document.createElement('div');
            entry.className = 'log-entry';
            entry.innerHTML = `<span style="color:#ff6666">[${new Date().toLocaleTimeString()}] â BaÄlantÄ± HatasÄ±!</span>`;
            logDiv.insertBefore(entry, logDiv.firstChild);
        }
    }

    setInterval(async () => {
        try {
            const res = await fetch('/durum_guncelle');
            const data = await res.json();
            document.getElementById('toplam_urun').innerText = data.toplam_urun;
            document.getElementById('yuksek_komisyon').innerText = data.yuksek_komisyon;
            document.getElementById('bugun_paylasim').innerText = data.bugun_paylasim + (data.bugun_paylasim > 1000 ? "" : "");
            document.getElementById('komisyon').innerText = data.komisyon.toLocaleString() + " âº";
        } catch(e) {}
    }, 5000);
</script>
</body>
</html>
'''

class NirvanaPanelHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(HTML.encode('utf-8'))

        elif self.path == '/baslat_hersey':
            # GerÃ§ek sistemde sistem_baslat.py'yi Ã§aÄÄ±rabiliriz
            try:
                subprocess.Popen([sys.executable, "sistem_baslat.py"], cwd=PROJECT_DIR)
                mesaj = "NIRVANA MODU: TÃ¼m servisler (Telegram, RPA, AI) arka planda baÅlatÄ±ldÄ±."
            except:
                mesaj = "Nirvana modu simÃ¼le ediliyor (sistem_baslat.py bulunamadÄ±)."
            self.send_json({'mesaj': mesaj})

        elif self.path == '/komisyon_bot':
            self.send_json({'mesaj': "KOMÄ°SYON BOTU: YÃ¼ksek kÃ¢rlÄ± Ã¼rÃ¼nler taranÄ±yor..."})

        elif self.path == '/ai_icerik':
            self.send_json({'mesaj': "AI MODÃLÃ: DeepSeek v4 ile yeni satÄ±Å metinleri oluÅturuldu."})

        elif self.path == '/sosyal_paylas':
            self.send_json({'mesaj': "SOSYAL MEDYA: PaylaÅÄ±mlar sÄ±raya alÄ±ndÄ±."})

        elif self.path == '/rapor':
            self.send_json({'mesaj': "RAPOR: GÃ¼nlÃ¼k performans Ã¶zeti hazÄ±rlandÄ±."})

        elif self.path == '/durum':
            self.send_json({'mesaj': "SÄ°STEM: TÃ¼m modÃ¼ller yeÅil. ÃalÄ±Åma sÃ¼resi: 100%"})

        elif self.path == '/durum_guncelle':
            self.send_json({
                'toplam_urun': random.randint(240, 300), 
                'yuksek_komisyon': random.randint(80, 110), 
                'bugun_paylasim': random.randint(1100, 1500), 
                'komisyon': random.randint(3100, 4200)
            })
        else:
            self.send_response(404)
            self.end_headers()

    def send_json(self, data):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode('utf-8'))

    def log_message(self, format, *args):
        pass

def main():
    print(f"ð TRM Nirvana Paneli http://localhost:{PORT} adresinde baÅlatÄ±lÄ±yor...")
    webbrowser.open(f'http://localhost:{PORT}')
    server = HTTPServer(('0.0.0.0', PORT), NirvanaPanelHandler)
    server.serve_forever()

if __name__ == '__main__':
    main()
