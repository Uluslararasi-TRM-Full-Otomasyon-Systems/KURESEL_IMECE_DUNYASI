# -*- coding: utf-8 -*-
"""
Merkezi yol çözümlemesi — pathlib tabanlı, sabit kullanıcı yolu içermez.

İsteğe bağlı ortam değişkenleri (boş bırakılırsa proje kökü kullanılır):
  TRM_PROJECT_ROOT — proje kök dizini
  TRM_HTML_DIR     — HTML panellerinin bulunduğu dizin (varsayılan: proje kökü)
  TRM_LOGS_DIR     — günlük dizini (varsayılan: <proje kökü>/logs)
  TRM_DATA_DIR     — veri dizini (varsayılan: <proje kökü>/data)
  TRM_FLASH_ROOT   — flash / harici ayna senkron kökü (yok veya geçersizse geriye dönük G: yolu)

flash_sync_root():
  TRM_FLASH_ROOT geçerliyse onu döndürür; aksi halde önceki DRIVE_FLASH_SYNC varsayılanı (G:/...) kullanılır.
  İlk kullanımda INFO veya WARNING ile açık log üretir (sessiz düşüş yok).
"""

from __future__ import annotations

import logging
import os
from pathlib import Path

_log = logging.getLogger(__name__)

# DRIVE_FLASH_SYNC öncesi sabit varsayılan (davranış korunur).
_LEGACY_FLASH_SYNC_ROOT = Path("G:/Uluslararası TRM Otonom Ekosistemi")
_LEGACY_PAZARLAMA_ROOT = Path("G:/PAZARLAMA")

_warned_invalid_trm_flash_root = False
_warned_invalid_trm_pazarlama_root = False
_logged_missing_trm_flash_root = False
_logged_pazarlama_discovery = False


def project_root() -> Path:
    """Proje kökü: TRM_PROJECT_ROOT geçerliyse onu, değilse bu dosyanın bulunduğu dizini döndürür."""
    override = os.environ.get("TRM_PROJECT_ROOT", "").strip()
    if override:
        candidate = Path(override).expanduser().resolve()
        if candidate.is_dir():
            return candidate
    return Path(__file__).resolve().parent


PROJECT_ROOT: Path = project_root()


def html_dir() -> Path:
    """HTML panelleri dizini; TRM_HTML_DIR geçerliyse onu, değilse proje kökünü döndürür."""
    override = os.environ.get("TRM_HTML_DIR", "").strip()
    if override:
        candidate = Path(override).expanduser().resolve()
        if candidate.is_dir():
            return candidate
    return project_root()


def logs_dir() -> Path:
    """Günlük dizini; TRM_LOGS_DIR tanımlıysa onu, değilse <proje kökü>/logs döndürür."""
    override = os.environ.get("TRM_LOGS_DIR", "").strip()
    if override:
        return Path(override).expanduser().resolve()
    return project_root() / "logs"


def data_dir() -> Path:
    """Veri dizini; TRM_DATA_DIR tanımlıysa onu, değilse <proje kökü>/data döndürür."""
    override = os.environ.get("TRM_DATA_DIR", "").strip()
    if override:
        return Path(override).expanduser().resolve()
    return project_root() / "data"


def flash_sync_root() -> Path:
    """
    Flash / harici ayna senkron kök dizini.

    Öncelik: TRM_FLASH_ROOT mevcut bir dizin ise.
    Tanımlı ama geçersiz: bir kez WARNING, ardından geriye dönük varsayılan.
    Tanımsız: bir kez INFO, ardından geriye dönük varsayılan (önceki G: yolu).
    """
    global _warned_invalid_trm_flash_root, _logged_missing_trm_flash_root

    override = os.environ.get("TRM_FLASH_ROOT", "").strip()
    if override:
        candidate = Path(override).expanduser().resolve()
        if candidate.is_dir():
            return candidate
        if not _warned_invalid_trm_flash_root:
            _log.warning(
                "TRM_FLASH_ROOT geçersiz veya dizin yok (%r). "
                "Flash senkron kökü geriye dönük varsayılan olarak kullanılıyor: %s",
                override,
                _LEGACY_FLASH_SYNC_ROOT,
            )
            _warned_invalid_trm_flash_root = True
        return _LEGACY_FLASH_SYNC_ROOT

    if not _logged_missing_trm_flash_root:
        _log.info(
            "TRM_FLASH_ROOT tanımlı değil; flash senkron kökü geriye dönük varsayılan: %s. "
            "Kalıcı yol için TRM_FLASH_ROOT ortam değişkenini ayarlayın.",
            _LEGACY_FLASH_SYNC_ROOT,
        )
        _logged_missing_trm_flash_root = True
    return _LEGACY_FLASH_SYNC_ROOT


def pazarlama_root() -> Path:
    """
    PAZARLAMA sistemi kök dizini.

    Öncelik:
    1. TRM_PAZARLAMA_ROOT ortam değişkeni (geçerli bir dizin ise).
    2. Otomatik Keşif: Proje klasörünün kardeşi (sibling) olan 'PAZARLAMA' klasörü.
    3. Geriye Dönük Varsayılan: G:/PAZARLAMA (legacy fallback).
    """
    global _warned_invalid_trm_pazarlama_root, _logged_pazarlama_discovery

    # 1. Ortam Değişkeni
    override = os.environ.get("TRM_PAZARLAMA_ROOT", "").strip()
    if override:
        candidate = Path(override).expanduser().resolve()
        if candidate.is_dir():
            return candidate
        if not _warned_invalid_trm_pazarlama_root:
            _log.warning(
                "TRM_PAZARLAMA_ROOT geçersiz veya dizin yok (%r). "
                "Diğer yöntemler deneniyor.",
                override,
            )
            _warned_invalid_trm_pazarlama_root = True

    # 2. Otomatik Keşif (Sibling Folder)
    sibling = PROJECT_ROOT.parent / "PAZARLAMA"
    if sibling.is_dir():
        if not _logged_pazarlama_discovery:
            _log.info("PAZARLAMA sistemi otomatik keşfedildi: %s", sibling)
            _logged_pazarlama_discovery = True
        return sibling

    # 3. Legacy Fallback
    if not _logged_pazarlama_discovery:
        _log.info(
            "PAZARLAMA sistemi için geriye dönük varsayılan yol kullanılıyor: %s",
            _LEGACY_PAZARLAMA_ROOT,
        )
        _logged_pazarlama_discovery = True
    return _LEGACY_PAZARLAMA_ROOT
