#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TRM Watchdog v5.0 - Madde 9: Servis cokmesi, internet kopma, Telegram reconnect, otomatik kurtarma
7/24 kesintisiz calisma icin tum servisleri izler ve kurtarir.
"""

import asyncio
import logging
import os
import sys
import time
import subprocess
import socket
import signal
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional

logger = logging.getLogger('TRMWatchdog')

BASE_DIR = Path(__file__).parent.resolve()
LOG_DIR  = BASE_DIR / 'logs'
LOG_DIR.mkdir(exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(str(LOG_DIR / 'watchdog.log'), encoding='utf-8'),
    ]
)

# ── Izlenecek servisler ──────────────────────────────────────────────────

SERVICES: Dict[str, dict] = {
    'orchestrator': {
        'cmd': [sys.executable, 'run.py'],
        'cwd': str(BASE_DIR),
        'health_url': 'http://localhost:9099',
        'restart_delay': 5,
        'max_restarts': 20,
    },
}

# ── Internet baglantisi kontrolu ───────────────────────────────────────

INTERNET_CHECK_HOSTS = [
    ('8.8.8.8', 53),
    ('1.1.1.1', 53),
    ('208.67.222.222', 53),
]

def check_internet(timeout: float = 3.0) -> bool:
    for host, port in INTERNET_CHECK_HOSTS:
        try:
            s = socket.create_connection((host, port), timeout=timeout)
            s.close()
            return True
        except OSError:
            continue
    return False

async def wait_for_internet(check_interval: int = 15) -> None:
    """Internet gelene kadar bekle."""
    if check_internet():
        return
    logger.warning('Internet baglantisi yok — bekleniyor...')
    while not check_internet():
        await asyncio.sleep(check_interval)
    logger.info('Internet baglantisi geri geldi')

# ── Telegram reconnect ──────────────────────────────────────────────────

class TelegramReconnectManager:
    def __init__(self):
        self._client = None
        self._reconnect_count = 0
        self._last_reconnect = None

    async def ensure_connected(self) -> bool:
        try:
            from telethon import TelegramClient
            from config import TRMConfig
            cfg = TRMConfig()
            if not cfg.telegram.get('api_id'):
                return False

            if self._client and self._client.is_connected():
                return True

            self._client = TelegramClient(
                str(BASE_DIR / 'data' / 'trm_session'),
                int(cfg.telegram['api_id']),
                cfg.telegram['api_hash'],
            )
            await self._client.connect()
            self._reconnect_count += 1
            self._last_reconnect = datetime.now()
            logger.info(f'Telegram baglandi (reconnect #{self._reconnect_count})')
            return True
        except Exception as e:
            logger.error(f'Telegram reconnect hatasi: {e}')
            return False

    async def disconnect(self):
        if self._client:
            await self._client.disconnect()

# ── Servis surec yoneticisi ─────────────────────────────────────────────

class ServiceProcess:
    def __init__(self, name: str, config: dict):
        self.name = name
        self.config = config
        self.process: Optional[subprocess.Popen] = None
        self.restart_count = 0
        self.last_crash: Optional[datetime] = None
        self.start_time: Optional[datetime] = None

    def is_running(self) -> bool:
        if self.process is None:
            return False
        return self.process.poll() is None

    def start(self) -> bool:
        if self.is_running():
            return True
        try:
            self.process = subprocess.Popen(
                self.config['cmd'],
                cwd=self.config.get('cwd', '.'),
                stdout=open(LOG_DIR / f'{self.name}.log', 'a', encoding='utf-8'),
                stderr=subprocess.STDOUT,
                env={**os.environ, 'PYTHONIOENCODING': 'utf-8', 'PYTHONUTF8': '1'},
            )
            self.start_time = datetime.now()
            self.restart_count += 1
            logger.info(f'[{self.name}] baslatildi PID={self.process.pid} (#{self.restart_count})')
            return True
        except Exception as e:
            logger.error(f'[{self.name}] baslatma hatasi: {e}')
            return False

    def stop(self):
        if self.process and self.is_running():
            try:
                self.process.terminate()
                self.process.wait(timeout=10)
            except Exception:
                self.process.kill()
            logger.info(f'[{self.name}] durduruldu')

    def restart(self, delay: float = 5.0) -> bool:
        self.stop()
        time.sleep(delay)
        self.last_crash = datetime.now()
        return self.start()

    def status(self) -> dict:
        uptime = None
        if self.start_time and self.is_running():
            uptime = str(datetime.now() - self.start_time).split('.')[0]
        return {
            'name': self.name,
            'running': self.is_running(),
            'pid': self.process.pid if self.process else None,
            'restart_count': self.restart_count,
            'uptime': uptime,
            'last_crash': self.last_crash.isoformat() if self.last_crash else None,
        }

# ── Ana Watchdog ────────────────────────────────────────────────────────

class TRMWatchdog:
    def __init__(self):
        self.services: Dict[str, ServiceProcess] = {
            name: ServiceProcess(name, cfg)
            for name, cfg in SERVICES.items()
        }
        self.telegram_mgr = TelegramReconnectManager()
        self._running = True
        self._last_internet_ok = True
        self._check_interval = 30  # saniye
        self._no_internet_since: Optional[datetime] = None

    def start_all(self):
        for svc in self.services.values():
            svc.start()
            time.sleep(2)

    def stop_all(self):
        for svc in self.services.values():
            svc.stop()

    async def _check_internet_loop(self):
        while self._running:
            ok = check_internet()
            if ok and not self._last_internet_ok:
                logger.info('Internet geri geldi — servisler kontrol ediliyor')
                self._no_internet_since = None
                for svc in self.services.values():
                    if not svc.is_running():
                        svc.start()
            elif not ok and self._last_internet_ok:
                self._no_internet_since = datetime.now()
                logger.warning('Internet baglantisi kesildi')
            self._last_internet_ok = ok
            await asyncio.sleep(15)

    async def _check_services_loop(self):
        while self._running:
            for svc in self.services.values():
                if not svc.is_running():
                    max_r = svc.config.get('max_restarts', 20)
                    if svc.restart_count < max_r:
                        logger.warning(f'[{svc.name}] cokmus — yeniden baslatiliyor')
                        ok = svc.restart(delay=svc.config.get('restart_delay', 5))
                        if not ok:
                            logger.error(f'[{svc.name}] baslatilamadi!')
                    else:
                        logger.critical(f'[{svc.name}] {max_r} kez yeniden baslatildi — manuel mudahale gerekiyor!')
            await asyncio.sleep(self._check_interval)

    async def _telegram_reconnect_loop(self):
        while self._running:
            if self._last_internet_ok:
                await self.telegram_mgr.ensure_connected()
            await asyncio.sleep(60)

    async def _print_status_loop(self):
        while self._running:
            now = datetime.now().strftime('%H:%M:%S')
            internet = '✅' if self._last_internet_ok else '❌'
            lines = [f'\n[{now}] TRM Watchdog Durumu | Internet: {internet}']
            for svc in self.services.values():
                st = svc.status()
                icon = '🟢' if st['running'] else '🔴'
                uptime = st['uptime'] or '-'
                lines.append(f"  {icon} {st['name']} | uptime: {uptime} | restart: {st['restart_count']}")
            print('\n'.join(lines))
            await asyncio.sleep(300)  # 5 dakikada bir durum yazdir

    async def run(self):
        logger.info('TRM Watchdog v5.0 baslatildi')
        self.start_all()
        await asyncio.gather(
            self._check_internet_loop(),
            self._check_services_loop(),
            self._telegram_reconnect_loop(),
            self._print_status_loop(),
        )

    def shutdown(self, *_):
        logger.info('Watchdog kapatiliyor...')
        self._running = False
        self.stop_all()


if __name__ == '__main__':
    watchdog = TRMWatchdog()
    signal.signal(signal.SIGINT, watchdog.shutdown)
    signal.signal(signal.SIGTERM, watchdog.shutdown)
    asyncio.run(watchdog.run())
