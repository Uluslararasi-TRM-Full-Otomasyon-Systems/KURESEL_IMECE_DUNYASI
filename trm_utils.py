#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TRM Ortak Yardimci Modulu
- Log rotasyonu
- File-lock korumali JSON kuyruk islemleri
- Retry decorator
"""

import json
import logging
import os
from logging.handlers import RotatingFileHandler
from typing import List, Dict, Any

try:
    from filelock import FileLock
    FILELOCK_AVAILABLE = True
except ImportError:
    FILELOCK_AVAILABLE = False

try:
    from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
    TENACITY_AVAILABLE = True
except ImportError:
    TENACITY_AVAILABLE = False


def setup_logging(log_file: str = "logs/trm.log", level=logging.INFO):
    """Rotasyonlu log kurulumu (10 MB × 5 dosya)"""
    os.makedirs(os.path.dirname(log_file) or ".", exist_ok=True)

    handler = RotatingFileHandler(
        log_file,
        maxBytes=10 * 1024 * 1024,  # 10 MB
        backupCount=5,
        encoding='utf-8'
    )
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    handler.setFormatter(formatter)

    root = logging.getLogger()
    root.setLevel(level)
    # Var olan handler'lari temizle (duplicate onle)
    root.handlers = [h for h in root.handlers if not isinstance(h, logging.FileHandler)]
    root.addHandler(handler)

    # Konsola da yaz
    console = logging.StreamHandler()
    console.setFormatter(formatter)
    if not any(isinstance(h, logging.StreamHandler) and not isinstance(h, logging.FileHandler)
               for h in root.handlers):
        root.addHandler(console)


def safe_read_queue(queue_file: str) -> List[Dict[str, Any]]:
    """File-lock korumali JSON kuyruk okuma"""
    if not os.path.exists(queue_file):
        return []

    lock_path = f"{queue_file}.lock"

    def _read():
        try:
            with open(queue_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    if FILELOCK_AVAILABLE:
        with FileLock(lock_path, timeout=10):
            return _read()
    return _read()


def safe_write_queue(queue_file: str, data: List[Dict[str, Any]]) -> bool:
    """File-lock korumali JSON kuyruk yazma"""
    lock_path = f"{queue_file}.lock"

    def _write():
        # Atomic write: once tmp'ye, sonra rename
        tmp_path = f"{queue_file}.tmp"
        with open(tmp_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        os.replace(tmp_path, queue_file)
        return True

    try:
        if FILELOCK_AVAILABLE:
            with FileLock(lock_path, timeout=10):
                return _write()
        return _write()
    except Exception as e:
        logging.getLogger(__name__).error(f"Kuyruk yazma hatasi ({queue_file}): {e}")
        return False


def safe_append_to_queue(queue_file: str, item: Dict[str, Any]) -> bool:
    """File-lock korumali kuyruk append (read+append+write tek lock altinda)"""
    lock_path = f"{queue_file}.lock"

    def _append():
        try:
            with open(queue_file, 'r', encoding='utf-8') as f:
                queue = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            queue = []

        queue.append(item)

        tmp_path = f"{queue_file}.tmp"
        with open(tmp_path, 'w', encoding='utf-8') as f:
            json.dump(queue, f, ensure_ascii=False, indent=2)
        os.replace(tmp_path, queue_file)
        return True

    try:
        if FILELOCK_AVAILABLE:
            with FileLock(lock_path, timeout=10):
                return _append()
        return _append()
    except Exception as e:
        logging.getLogger(__name__).error(f"Kuyruk append hatasi ({queue_file}): {e}")
        return False


# Retry decorator - API cagrilarinda kullan
if TENACITY_AVAILABLE:
    def with_retry(max_attempts=3, min_wait=1, max_wait=10):
        """API cagrilari icin exponential backoff retry"""
        return retry(
            stop=stop_after_attempt(max_attempts),
            wait=wait_exponential(multiplier=min_wait, max=max_wait),
            retry=retry_if_exception_type((ConnectionError, TimeoutError, OSError)),
            reraise=True
        )
else:
    def with_retry(max_attempts=3, min_wait=1, max_wait=10):
        """Tenacity yok - no-op decorator"""
        def decorator(func):
            return func
        return decorator
