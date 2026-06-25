#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TRM Queue Manager v5.0 - Madde 10: Gerçek zamanlı kuyruk, bozuk veri temizleme,
kilitlenme koruması, yedek veri sistemi.
"""

import asyncio
import json
import logging
import os
import shutil
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional
import filelock

logger = logging.getLogger('TRMQueue')

BASE_DIR  = Path(__file__).parent.resolve()
DATA_DIR  = BASE_DIR / 'data'
QUEUE_DIR = DATA_DIR / 'queues'
BACKUP_DIR = DATA_DIR / 'queue_backups'
DATA_DIR.mkdir(exist_ok=True)
QUEUE_DIR.mkdir(exist_ok=True)
BACKUP_DIR.mkdir(exist_ok=True)

LOCK_TIMEOUT = 10  # saniye

def _queue_path(name: str) -> Path:
    return QUEUE_DIR / f'{name}.json'

def _lock_path(name: str) -> Path:
    return QUEUE_DIR / f'{name}.lock'

def _load_safe(path: Path) -> List[Dict]:
    """JSON yükle; bozuksa boş liste döndür."""
    if not path.exists():
        return []
    try:
        data = json.loads(path.read_text(encoding='utf-8'))
        if isinstance(data, list):
            return data
        return []
    except (json.JSONDecodeError, UnicodeDecodeError):
        # Bozuk dosya → yedekle
        bak = BACKUP_DIR / f'{path.stem}_corrupt_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
        shutil.copy2(path, bak)
        logger.warning(f'Bozuk kuyruk yedeklendi: {bak.name}')
        path.write_text('[]', encoding='utf-8')
        return []

def _save_safe(path: Path, data: List) -> bool:
    tmp = path.with_suffix('.tmp')
    try:
        tmp.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')
        tmp.replace(path)
        return True
    except Exception as e:
        logger.error(f'Kuyruk kaydetme hatası: {e}')
        return False


class QueueManager:
    """Thread-safe, kilitleme korumalı kuyruk yöneticisi."""

    def __init__(self, name: str):
        self.name = name
        self._path = _queue_path(name)
        self._lock = filelock.FileLock(str(_lock_path(name)), timeout=LOCK_TIMEOUT)

    def push(self, item: Dict) -> bool:
        try:
            with self._lock:
                q = _load_safe(self._path)
                item['queued_at'] = datetime.now().isoformat()
                q.append(item)
                return _save_safe(self._path, q)
        except filelock.Timeout:
            logger.error(f'[{self.name}] Kilit zaman aşımı — push başarısız')
            return False

    def push_many(self, items: List[Dict]) -> int:
        try:
            with self._lock:
                q = _load_safe(self._path)
                now = datetime.now().isoformat()
                for item in items:
                    item['queued_at'] = now
                q.extend(items)
                _save_safe(self._path, q)
                return len(items)
        except filelock.Timeout:
            logger.error(f'[{self.name}] Kilit zaman aşımı — push_many başarısız')
            return 0

    def pop(self) -> Optional[Dict]:
        try:
            with self._lock:
                q = _load_safe(self._path)
                if not q:
                    return None
                item = q.pop(0)
                _save_safe(self._path, q)
                return item
        except filelock.Timeout:
            logger.error(f'[{self.name}] Kilit zaman aşımı — pop başarısız')
            return None

    def peek(self, n: int = 5) -> List[Dict]:
        return _load_safe(self._path)[:n]

    def size(self) -> int:
        return len(_load_safe(self._path))

    def clear_stale(self, max_age_hours: int = 48) -> int:
        """Eski ve bozuk kayıtları temizle."""
        try:
            with self._lock:
                q = _load_safe(self._path)
                cutoff = datetime.now() - timedelta(hours=max_age_hours)
                clean = []
                removed = 0
                for item in q:
                    if not isinstance(item, dict):
                        removed += 1
                        continue
                    ts = item.get('queued_at','')
                    try:
                        if datetime.fromisoformat(ts) < cutoff:
                            removed += 1
                            continue
                    except (ValueError, TypeError):
                        pass
                    clean.append(item)
                if removed:
                    _save_safe(self._path, clean)
                    logger.info(f'[{self.name}] {removed} eski kayıt temizlendi')
                return removed
        except filelock.Timeout:
            return 0

    def backup(self) -> Optional[Path]:
        """Anlık yedek al."""
        q = _load_safe(self._path)
        bak = BACKUP_DIR / f'{self.name}_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
        try:
            bak.write_text(json.dumps(q, ensure_ascii=False, indent=2), encoding='utf-8')
            return bak
        except Exception as e:
            logger.error(f'Yedek alınamadı: {e}')
            return None

    def status(self) -> Dict:
        q = _load_safe(self._path)
        oldest = None
        if q:
            try:
                oldest = q[0].get('queued_at')
            except Exception:
                pass
        return {'name': self.name, 'size': len(q), 'oldest_item': oldest}


# ── Global kuyruk örnekleri ─────────────────────────────────────────────

product_queue   = QueueManager('products')
content_queue   = QueueManager('contents')
publish_queue   = QueueManager('publish')
failed_queue    = QueueManager('failed')


async def queue_maintenance_loop(interval_minutes: int = 30):
    """Periyodik bakım: stale temizleme + yedekleme."""
    while True:
        await asyncio.sleep(interval_minutes * 60)
        for q in [product_queue, content_queue, publish_queue, failed_queue]:
            q.clear_stale(max_age_hours=48)
            q.backup()
        logger.info('Kuyruk bakımı tamamlandı')


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    print('=== Kuyruk Durumu ===')
    for q in [product_queue, content_queue, publish_queue, failed_queue]:
        print(q.status())
