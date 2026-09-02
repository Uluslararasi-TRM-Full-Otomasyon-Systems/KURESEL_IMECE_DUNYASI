#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TRM Self-Healing Manager v1.0
Coken modulleri algilar, yeniden baslatir, analiz eder ve raporlar.
"""

import asyncio
import logging
import json
import os
import subprocess
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional

logger = logging.getLogger('TRMSelfHealing')

class SelfHealingManager:
    """
    Sistem kendini izler ve sorunlari otomatik cozer.
    Cozemedigi sorunlari Telegram/Discord/Viber ile bildirir.
    """

    # Bildirim yapilacak kritik durumlar
    CRITICAL_EVENTS = [
        "CRITICAL_ERROR",
        "SERVICE_CRASHED",
        "SERVICE_RESTARTED",
        "SECURITY_EVENT",
        "DATA_LOSS_RISK",
        "API_CONNECTION_FAILED",
        "CLOUD_CONNECTION_FAILED",
        "UNRESOLVABLE_PROBLEM",
        "HUMAN_INTERVENTION_REQUIRED",
        "SYSTEM_STOP_RISK"
    ]

    def __init__(self):
        self.base_dir = Path(__file__).parent
        self.log_dir = self.base_dir / 'logs'
        self.log_dir.mkdir(exist_ok=True)

        self.incident_log = self.log_dir / 'incidents.json'
        self.incidents: List[Dict] = self._load_incidents()

        # Izlenen moduller ve baslatma komutlari
        self.monitored_modules = {
            'main_orchestrator': 'python main_orchestrator.py',
            'telegram_bot': 'python telegram_bot.py',
            'social_media_automation': 'python social_media_automation.py',
            'content_scheduler': 'python CONTENT_SCHEDULER.py',
            'watchdog': 'python WATCHDOG.py',
        }

        self.process_handles: Dict[str, subprocess.Popen] = {}
        self.restart_counts: Dict[str, int] = {}
        self.last_restart: Dict[str, datetime] = {}

        # Esik degerleri
        self.MAX_RESTARTS_PER_HOUR = 5
        self.RESTART_COOLDOWN_SECONDS = 30

    def _load_incidents(self) -> List[Dict]:
        if self.incident_log.exists():
            try:
                return json.loads(self.incident_log.read_text(encoding='utf-8'))
            except Exception:
                return []
        return []

    def _save_incidents(self):
        self.incident_log.write_text(
            json.dumps(self.incidents[-1000:], ensure_ascii=False, indent=2),
            encoding='utf-8'
        )

    def log_incident(self, event_type: str, module: str, detail: str, resolved: bool = False):
        incident = {
            'timestamp': datetime.now().isoformat(),
            'event_type': event_type,
            'module': module,
            'detail': detail,
            'resolved': resolved
        }
        self.incidents.append(incident)
        self._save_incidents()
        logger.info(f"[{event_type}] {module}: {detail}")

        # Kritik olaylari bildir
        if event_type in self.CRITICAL_EVENTS:
            asyncio.create_task(self._send_notification(incident))

    async def _send_notification(self, incident: Dict):
        """Telegram, Discord, Viber'a kritik bildirim gonder."""
        msg = (
            f"🚨 TRM ALARM\n"
            f"Olay: {incident['event_type']}\n"
            f"Modul: {incident['module']}\n"
            f"Detay: {incident['detail']}\n"
            f"Zaman: {incident['timestamp']}"
        )

        # Telegram
        bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
        chat_id = os.getenv('TELEGRAM_CHAT_ID')
        if bot_token and chat_id:
            try:
                import aiohttp
                async with aiohttp.ClientSession() as session:
                    await session.post(
                        f"https://api.telegram.org/bot{bot_token}/sendMessage",
                        json={'chat_id': chat_id, 'text': msg}
                    )
            except Exception as e:
                logger.error(f"Telegram bildirim hatasi: {e}")

    def is_process_running(self, module_name: str) -> bool:
        handle = self.process_handles.get(module_name)
        if handle is None:
            return False
        return handle.poll() is None

    def can_restart(self, module_name: str) -> bool:
        count = self.restart_counts.get(module_name, 0)
        last = self.last_restart.get(module_name)

        # Saatlik restart sayisini sifirla
        if last and (datetime.now() - last) > timedelta(hours=1):
            self.restart_counts[module_name] = 0
            return True

        if count >= self.MAX_RESTARTS_PER_HOUR:
            return False

        if last and (datetime.now() - last).seconds < self.RESTART_COOLDOWN_SECONDS:
            return False

        return True

    def restart_module(self, module_name: str) -> bool:
        cmd = self.monitored_modules.get(module_name)
        if not cmd:
            return False

        if not self.can_restart(module_name):
            self.log_incident(
                "HUMAN_INTERVENTION_REQUIRED",
                module_name,
                f"Saatlik restart limiti asildi ({self.MAX_RESTARTS_PER_HOUR}x). Manuel mudahale gerekiyor.",
                resolved=False
            )
            return False

        try:
            # Varsa eski process'i sonlandir
            old = self.process_handles.get(module_name)
            if old and old.poll() is None:
                old.terminate()
                time.sleep(2)

            proc = subprocess.Popen(
                cmd.split(),
                cwd=str(self.base_dir),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            self.process_handles[module_name] = proc
            self.restart_counts[module_name] = self.restart_counts.get(module_name, 0) + 1
            self.last_restart[module_name] = datetime.now()

            self.log_incident(
                "SERVICE_RESTARTED",
                module_name,
                f"Modul yeniden baslatildi. (#{self.restart_counts[module_name]})",
                resolved=True
            )
            return True

        except Exception as e:
            self.log_incident(
                "CRITICAL_ERROR",
                module_name,
                f"Yeniden baslatma basarisiz: {e}",
                resolved=False
            )
            return False

    async def monitor_loop(self, interval_seconds: int = 30):
        """Ana izleme dongusu - tum modulleri periyodik kontrol eder."""
        logger.info("🔄 Self-Healing Monitor baslatildi")
        while True:
            for module_name in self.monitored_modules:
                if not self.is_process_running(module_name):
                    self.log_incident(
                        "SERVICE_CRASHED",
                        module_name,
                        "Modul calismiyor. Yeniden baslatiliyor...",
                        resolved=False
                    )
                    self.restart_module(module_name)
            await asyncio.sleep(interval_seconds)

    def classify_recurring_errors(self) -> Dict:
        """Tekrarlayan hatalari analiz eder ve siniflandirir."""
        from collections import Counter
        error_types = [i['event_type'] for i in self.incidents if not i.get('resolved')]
        module_errors = [i['module'] for i in self.incidents if not i.get('resolved')]

        return {
            'most_common_errors': Counter(error_types).most_common(5),
            'most_problematic_modules': Counter(module_errors).most_common(5),
            'total_unresolved': len([i for i in self.incidents if not i.get('resolved')]),
            'total_incidents': len(self.incidents)
        }


if __name__ == '__main__':
    manager = SelfHealingManager()
    asyncio.run(manager.monitor_loop())
