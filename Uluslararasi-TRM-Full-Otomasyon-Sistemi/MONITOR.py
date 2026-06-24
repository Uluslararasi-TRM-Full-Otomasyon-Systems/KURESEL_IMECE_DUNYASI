#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TRM Monitor v5.0 - Madde 16: Gerçek zamanlı log sistemi, hata paneli,
servis sağlık kontrolü, alarm sistemi.
"""

import asyncio
import json
import logging
import os
import sys
import time
from collections import deque
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional

try:
    import psutil
    PSUTIL_OK = True
except ImportError:
    PSUTIL_OK = False

logger = logging.getLogger('TRMMonitor')

BASE_DIR = Path(__file__).parent.resolve()
LOG_DIR  = BASE_DIR / 'logs'
LOG_DIR.mkdir(exist_ok=True)

# ── Log yöneticisi ────────────────────────────────────────────────────────

def setup_logging(level: str = 'INFO') -> logging.Logger:
    """Merkezi log sistemi kur — hem dosyaya hem terminale."""
    log_level = getattr(logging, level.upper(), logging.INFO)
    fmt = '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
    date_fmt = '%d.%m %H:%M:%S'

    root = logging.getLogger()
    root.setLevel(log_level)
    root.handlers.clear()

    # Terminal handler
    sh = logging.StreamHandler(sys.stdout)
    sh.setFormatter(logging.Formatter(fmt, datefmt=date_fmt))
    root.addHandler(sh)

    # Ana log dosyası (rotasyonlu)
    from logging.handlers import RotatingFileHandler
    fh = RotatingFileHandler(
        str(LOG_DIR / 'trm_main.log'),
        maxBytes=5*1024*1024,   # 5 MB
        backupCount=5,
        encoding='utf-8',
    )
    fh.setFormatter(logging.Formatter(fmt, datefmt=date_fmt))
    root.addHandler(fh)

    # Hata log dosyası
    eh = RotatingFileHandler(
        str(LOG_DIR / 'trm_errors.log'),
        maxBytes=2*1024*1024,
        backupCount=3,
        encoding='utf-8',
    )
    eh.setLevel(logging.ERROR)
    eh.setFormatter(logging.Formatter(fmt, datefmt=date_fmt))
    root.addHandler(eh)

    return root


# ── Sağlık Kontrolü ──────────────────────────────────────────────────────

class HealthMonitor:
    def __init__(self):
        self._alerts: deque = deque(maxlen=100)
        self._start_time = datetime.now()

    def check_system(self) -> Dict:
        result = {
            'timestamp': datetime.now().isoformat(),
            'uptime': str(datetime.now() - self._start_time).split('.')[0],
            'cpu': None,
            'memory': None,
            'disk': None,
            'logs': {},
        }

        if PSUTIL_OK:
            result['cpu'] = f'{psutil.cpu_percent(interval=1):.1f}%'
            mem = psutil.virtual_memory()
            result['memory'] = f'{mem.percent:.1f}% ({mem.used//1024//1024}MB/{mem.total//1024//1024}MB)'
            disk = psutil.disk_usage('.')
            result['disk'] = f'{disk.percent:.1f}% ({disk.free//1024//1024//1024}GB free)'

        # Log dosya boyutları
        for log_file in LOG_DIR.glob('*.log'):
            size_kb = log_file.stat().st_size // 1024
            result['logs'][log_file.name] = f'{size_kb}KB'

        return result

    def check_watchdog_port(self, port: int = 9099) -> bool:
        import socket
        try:
            s = socket.create_connection(('localhost', port), timeout=2)
            s.close()
            return True
        except OSError:
            return False

    def add_alert(self, level: str, message: str):
        self._alerts.append({
            'level': level,
            'message': message,
            'at': datetime.now().strftime('%H:%M:%S'),
        })
        logger.log(getattr(logging, level, logging.WARNING), f'ALARM: {message}')

    def recent_alerts(self, n: int = 10) -> List[Dict]:
        return list(self._alerts)[-n:]

    def print_status(self):
        h = self.check_system()
        watchdog = '🟢 Aktif' if self.check_watchdog_port() else '🔴 Kapalı'
        print(f"""
┌─────────────────────────────────────────────────┐
│  TRM Monitor — {h['timestamp'][:16]}
├─────────────────────────────────────────────────┤
│  Çalışma Süresi : {h['uptime']}
│  CPU            : {h.get('cpu','N/A')}
│  RAM            : {h.get('memory','N/A')}
│  Disk           : {h.get('disk','N/A')}
│  Watchdog       : {watchdog}
├─────────────────────────────────────────────────┤""")
        for name, size in h['logs'].items():
            print(f"│  {name:<30s} {size:>8s}")
        alerts = self.recent_alerts(5)
        if alerts:
            print('├─────────────────────────────────────────────────┤')
            for a in alerts:
                icon = '🔴' if a['level']=='ERROR' else '🟡'
                print(f"│  {icon} [{a['at']}] {a['message'][:42]}")
        print('└─────────────────────────────────────────────────┘')

    async def run_loop(self, interval: int = 300):
        """Periyodik sağlık kontrolü döngüsü."""
        while True:
            h = self.check_system()
            if PSUTIL_OK:
                cpu_val = float(h['cpu'].rstrip('%'))
                if cpu_val > 90:
                    self.add_alert('WARNING', f"CPU yüksek: {h['cpu']}")
            await asyncio.sleep(interval)


# ── Telegram alarm gönderici ─────────────────────────────────────────────

async def send_telegram_alert(message: str) -> bool:
    """Kritik alarm için Telegram mesajı gönder."""
    token = os.getenv('TELEGRAM_BOT_TOKEN_NOTIFICATION') or os.getenv('TELEGRAM_BOT_TOKEN','')
    chat_id = os.getenv('TELEGRAM_CHAT_ID','')
    if not token or not chat_id:
        return False
    try:
        import aiohttp
        url = f'https://api.telegram.org/bot{token}/sendMessage'
        payload = {'chat_id': chat_id, 'text': f'🚨 TRM ALARM\n{message}', 'parse_mode': 'HTML'}
        async with aiohttp.ClientSession() as sess:
            async with sess.post(url, json=payload, timeout=aiohttp.ClientTimeout(total=10)) as r:
                return r.status == 200
    except Exception as e:
        logger.error(f'Telegram alarm gönderilemedi: {e}')
        return False


# ── Singleton ─────────────────────────────────────────────────────────────
monitor = HealthMonitor()


if __name__ == '__main__':
    setup_logging()
    monitor.print_status()
    # Sürekli izleme modu
    if '--watch' in sys.argv:
        async def loop():
            while True:
                os.system('clear' if os.name != 'nt' else 'cls')
                monitor.print_status()
                await asyncio.sleep(10)
        asyncio.run(loop())
