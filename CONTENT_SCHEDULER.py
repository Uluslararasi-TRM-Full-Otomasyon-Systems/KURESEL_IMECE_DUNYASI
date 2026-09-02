#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TRM Content Scheduler v5.0 - Madde 17: Saatlik yayin plani, platform bazli
zamanlama, icerik kuyruk planlayici.
"""

import asyncio
import json
import logging
from datetime import datetime, time, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Tuple

logger = logging.getLogger('TRMScheduler')

# ── Platform bazli optimum paylasim saatleri ───────────────────────────
# Turkiye TZ (UTC+3) hedeflenerek duzenlenmistir

PLATFORM_SCHEDULE: Dict[str, List[Tuple[int,int]]] = {
    'instagram':  [(9,0),(12,30),(18,0),(20,30),(22,0)],
    'facebook':   [(10,0),(13,0),(19,0),(21,0)],
    'twitter':    [(8,0),(12,0),(17,0),(21,0),(23,0)],
    'tiktok':     [(11,0),(15,0),(19,0),(21,30)],
    'linkedin':   [(9,0),(12,0),(17,30)],
    'youtube':    [(11,0),(15,0),(20,0)],
    'messaging':   [(9,30),(13,0),(18,30)],
    'telegram':   [(9,0),(12,0),(15,0),(18,0),(21,0)],
    'blog':       [(10,0),(14,0),(20,0)],
}

# Haftanin gunlerine gore ozel agirliklar (1.0 = normal, 1.5 = yogun)
DAY_WEIGHTS = {
    0: 1.0,  # Pazartesi
    1: 1.1,
    2: 1.1,
    3: 1.2,  # Carsamba — orta hafta
    4: 1.3,  # Persembe
    5: 1.5,  # Cuma — en yuksek
    6: 1.2,  # Cumartesi
}


class ContentScheduler:
    """Platform bazli icerik zamanlayici."""

    def __init__(self):
        self._scheduled: List[Dict] = []          # bekleyen gorevler
        self._running = False
        self._data_path = Path(__file__).parent / 'data' / 'schedule.json'
        self._data_path.parent.mkdir(exist_ok=True)
        self._load_state()

    def _load_state(self):
        try:
            if self._data_path.exists():
                self._scheduled = json.loads(self._data_path.read_text('utf-8'))
        except Exception:
            self._scheduled = []

    def _save_state(self):
        try:
            self._data_path.write_text(
                json.dumps(self._scheduled, ensure_ascii=False, indent=2), 'utf-8')
        except Exception as e:
            logger.error(f'Schedule kaydetme hatasi: {e}')

    def schedule_content(self, content: Dict, platform: str,
                         publish_at: Optional[datetime] = None) -> Dict:
        """Icerigi belirli bir zamana planla veya bir sonraki slota ekle."""
        if publish_at is None:
            publish_at = self.next_slot(platform)

        task = {
            'id': f"{platform}_{publish_at.strftime('%Y%m%d_%H%M')}",
            'platform': platform,
            'content': content,
            'publish_at': publish_at.isoformat(),
            'status': 'scheduled',
            'created_at': datetime.now().isoformat(),
        }
        self._scheduled.append(task)
        self._save_state()
        logger.info(f'Planlandi: {platform} → {publish_at.strftime("%d.%m %H:%M")}')
        return task

    def schedule_all_platforms(self, content: Dict) -> List[Dict]:
        """Ayni icerigi tum aktif platformlara zamanli sekilde dagit."""
        tasks = []
        for platform in PLATFORM_SCHEDULE:
            tasks.append(self.schedule_content(dict(content), platform))
        return tasks

    def next_slot(self, platform: str) -> datetime:
        """Platforma gore bir sonraki optimum yayin zamani."""
        now = datetime.now()
        slots = PLATFORM_SCHEDULE.get(platform, [(12, 0)])
        weight = DAY_WEIGHTS.get(now.weekday(), 1.0)

        # Bugunun kalan slotlarina bak
        for hour, minute in sorted(slots):
            candidate = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
            if candidate > now + timedelta(minutes=5):
                # Daha once bu saate zaten planlanmis mi?
                if not self._is_slot_taken(platform, candidate):
                    return candidate

        # Yarin ilk slota gec
        tomorrow = now + timedelta(days=1)
        h, m = sorted(slots)[0]
        return tomorrow.replace(hour=h, minute=m, second=0, microsecond=0)

    def _is_slot_taken(self, platform: str, dt: datetime) -> bool:
        target = dt.strftime('%Y-%m-%dT%H:%M')
        return any(
            t['platform'] == platform and t['publish_at'].startswith(target)
            and t['status'] == 'scheduled'
            for t in self._scheduled
        )

    def pending(self, platform: Optional[str] = None) -> List[Dict]:
        tasks = [t for t in self._scheduled if t['status'] == 'scheduled']
        if platform:
            tasks = [t for t in tasks if t['platform'] == platform]
        return sorted(tasks, key=lambda t: t['publish_at'])

    def due_now(self) -> List[Dict]:
        """Su an yayinlanmasi gereken icerikler."""
        now = datetime.now()
        due = []
        for t in self._scheduled:
            if t['status'] != 'scheduled':
                continue
            try:
                pt = datetime.fromisoformat(t['publish_at'])
                if pt <= now:
                    due.append(t)
            except (ValueError, KeyError):
                pass
        return due

    def mark_done(self, task_id: str, success: bool = True):
        for t in self._scheduled:
            if t['id'] == task_id:
                t['status'] = 'published' if success else 'failed'
                t['completed_at'] = datetime.now().isoformat()
                break
        self._save_state()

    def daily_plan(self) -> Dict[str, List[str]]:
        """Bugunku yayin planini platforma gore dondur."""
        today = datetime.now().date()
        plan: Dict[str, List[str]] = {p: [] for p in PLATFORM_SCHEDULE}
        for t in self._scheduled:
            if t['status'] != 'scheduled':
                continue
            try:
                pt = datetime.fromisoformat(t['publish_at'])
                if pt.date() == today:
                    platform = t['platform']
                    plan[platform].append(pt.strftime('%H:%M'))
            except Exception:
                pass
        return {k: sorted(v) for k, v in plan.items() if v}

    async def run_loop(self, publish_callback):
        """Scheduler dongusu — due olan icerikleri callback ile yayinla."""
        self._running = True
        logger.info('Content Scheduler baslatildi')
        while self._running:
            for task in self.due_now():
                try:
                    await publish_callback(task)
                    self.mark_done(task['id'], success=True)
                except Exception as e:
                    logger.error(f"Yayin hatasi [{task['id']}]: {e}")
                    self.mark_done(task['id'], success=False)
            await asyncio.sleep(60)  # Her dakika kontrol

    def stop(self):
        self._running = False

    def print_today_plan(self):
        plan = self.daily_plan()
        print(f"\n{'='*40}")
        print(f"  Bugunku Yayin Plani ({datetime.now().strftime('%d.%m.%Y')})")
        print(f"{'='*40}")
        if not plan:
            print("  Planlanmis icerik yok")
        for platform, times in plan.items():
            print(f"  {platform:12s}: {', '.join(times)}")
        print(f"{'='*40}\n")


# ── Singleton ─────────────────────────────────────────────────────────────
scheduler = ContentScheduler()


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    s = ContentScheduler()

    # Demo: tum platformlar icin bir sonraki slot hesapla
    print('\n=== Bir Sonraki Optimum Yayin Slotlari ===')
    for platform in PLATFORM_SCHEDULE:
        slot = s.next_slot(platform)
        print(f"  {platform:12s}: {slot.strftime('%d.%m %H:%M')}")

    # Demo planla
    demo_content = {'content': 'Test urun icerigi', 'title': 'Demo Urun', 'link': 'https://ty.gl/DEMO'}
    s.schedule_all_platforms(demo_content)
    s.print_today_plan()
