# -*- coding: utf-8 -*-
"""
Merkezi yol cozumlemesi — pathlib tabanli, sabit kullanici yolu icermez.

Istege bagli ortam degiskenleri (bos birakilirsa proje koku kullanilir):
  TRM_PROJECT_ROOT — proje kok dizini
  TRM_HTML_DIR     — HTML panellerinin bulundugu dizin (varsayilan: proje koku)
  TRM_LOGS_DIR     — gunluk dizini (varsayilan: <proje koku>/logs)
  TRM_DATA_DIR     — veri dizini (varsayilan: <proje koku>/data)
  TRM_FLASH_ROOT   — flash / harici ayna senkron koku (yok veya gecersizse geriye donuk G: yolu)

flash_sync_root():
  TRM_FLASH_ROOT gecerliyse onu dondurur; aksi halde onceki DRIVE_FLASH_SYNC varsayilani (G:/...) kullanilir.
  Ilk kullanimda INFO veya WARNING ile acik log uretir (sessiz dusus yok).
"""

from __future__ import annotations

import logging
import os
from pathlib import Path

_log = logging.getLogger(__name__)

# DRIVE_FLASH_SYNC oncesi sabit varsayilan (davranis korunur).
_LEGACY_FLASH_SYNC_ROOT = Path("G:/Uluslararasi-TRM-Full-Otomasyon-Sistemi")
_LEGACY_PAZARLAMA_ROOT = Path("G:/PAZARLAMA")

_warned_invalid_trm_flash_root = False
_warned_invalid_trm_pazarlama_root = False
_logged_missing_trm_flash_root = False
_logged_pazarlama_discovery = False


def project_root() -> Path:
    """Proje koku: TRM_PROJECT_ROOT gecerliyse onu, degilse bu dosyanin bulundugu dizini dondurur."""
    override = os.environ.get("TRM_PROJECT_ROOT", "").strip()
    if override:
        candidate = Path(override).expanduser().resolve()
        if candidate.is_dir():
            return candidate
    return Path(__file__).resolve().parent


PROJECT_ROOT: Path = project_root()


def html_dir() -> Path:
    """HTML panelleri dizini; TRM_HTML_DIR gecerliyse onu, degilse proje kokunu dondurur."""
    override = os.environ.get("TRM_HTML_DIR", "").strip()
    if override:
        candidate = Path(override).expanduser().resolve()
        if candidate.is_dir():
            return candidate
    return project_root()


def logs_dir() -> Path:
    """Gunluk dizini; TRM_LOGS_DIR tanimliysa onu, degilse <proje koku>/logs dondurur."""
    override = os.environ.get("TRM_LOGS_DIR", "").strip()
    if override:
        return Path(override).expanduser().resolve()
    return project_root() / "logs"


def data_dir() -> Path:
    """Veri dizini; TRM_DATA_DIR tanimliysa onu, degilse <proje koku>/data dondurur."""
    override = os.environ.get("TRM_DATA_DIR", "").strip()
    if override:
        return Path(override).expanduser().resolve()
    return project_root() / "data"


def flash_sync_root() -> Path:
    """
    Flash / harici ayna senkron kok dizini.

    Oncelik: TRM_FLASH_ROOT mevcut bir dizin ise.
    Tanimli ama gecersiz: bir kez WARNING, ardindan geriye donuk varsayilan.
    Tanimsiz: bir kez INFO, ardindan geriye donuk varsayilan (onceki G: yolu).
    """
    global _warned_invalid_trm_flash_root, _logged_missing_trm_flash_root

    override = os.environ.get("TRM_FLASH_ROOT", "").strip()
    if override:
        candidate = Path(override).expanduser().resolve()
        if candidate.is_dir():
            return candidate
        if not _warned_invalid_trm_flash_root:
            _log.warning(
                "TRM_FLASH_ROOT gecersiz veya dizin yok (%r). "
                "Flash senkron koku geriye donuk varsayilan olarak kullaniliyor: %s",
                override,
                _LEGACY_FLASH_SYNC_ROOT,
            )
            _warned_invalid_trm_flash_root = True
        return _LEGACY_FLASH_SYNC_ROOT

    if not _logged_missing_trm_flash_root:
        _log.info(
            "TRM_FLASH_ROOT tanimli degil; flash senkron koku geriye donuk varsayilan: %s. "
            "Kalici yol icin TRM_FLASH_ROOT ortam degiskenini ayarlayin.",
            _LEGACY_FLASH_SYNC_ROOT,
        )
        _logged_missing_trm_flash_root = True
    return _LEGACY_FLASH_SYNC_ROOT


def pazarlama_root() -> Path:
    """
    PAZARLAMA sistemi kok dizini.

    Oncelik:
    1. TRM_PAZARLAMA_ROOT ortam degiskeni (gecerli bir dizin ise).
    2. Otomatik Kesif: Proje klasorunun kardesi (sibling) olan 'PAZARLAMA' klasoru.
    3. Geriye Donuk Varsayilan: G:/PAZARLAMA (legacy fallback).
    """
    global _warned_invalid_trm_pazarlama_root, _logged_pazarlama_discovery

    # 1. Ortam Degiskeni
    override = os.environ.get("TRM_PAZARLAMA_ROOT", "").strip()
    if override:
        candidate = Path(override).expanduser().resolve()
        if candidate.is_dir():
            return candidate
        if not _warned_invalid_trm_pazarlama_root:
            _log.warning(
                "TRM_PAZARLAMA_ROOT gecersiz veya dizin yok (%r). "
                "Diger yontemler deneniyor.",
                override,
            )
            _warned_invalid_trm_pazarlama_root = True

    # 2. Otomatik Kesif (Sibling Folder)
    sibling = PROJECT_ROOT.parent / "PAZARLAMA"
    if sibling.is_dir():
        if not _logged_pazarlama_discovery:
            _log.info("PAZARLAMA sistemi otomatik kesfedildi: %s", sibling)
            _logged_pazarlama_discovery = True
        return sibling

    # 3. Legacy Fallback
    if not _logged_pazarlama_discovery:
        _log.info(
            "PAZARLAMA sistemi icin geriye donuk varsayilan yol kullaniliyor: %s",
            _LEGACY_PAZARLAMA_ROOT,
        )
        _logged_pazarlama_discovery = True
    return _LEGACY_PAZARLAMA_ROOT
