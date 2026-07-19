# -*- coding: utf-8 -*-
"""
config.py
MASTER_CONTROLLER.py ve diğer modüllerin ihtiyaç duyduğu sabitleri
config/global_config.json dosyasından okuyup dışa açan köprü modül.

ÖNEMLİ: Bu dosya bir Python MODÜLÜDÜR (import config), config/global_config.json
ise bir VERİ dosyasıdır. İkisi farklı şeylerdir; bu modül aradaki köprüdür.
"""

import os
import json

_BASE_DIR = os.path.dirname(os.path.abspath(__file__))
_CONFIG_PATH = os.path.join(_BASE_DIR, "config", "global_config.json")


def _load_global_config():
    """config/global_config.json dosyasını okur. Yoksa net bir hata fırlatır
    (sessizce varsayılana düşüp yanlış değerlerle çalışmak yerine)."""
    try:
        with open(_CONFIG_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        raise FileNotFoundError(
            f"config.py: '{_CONFIG_PATH}' bulunamadı. "
            "MASTER_CONTROLLER, global_config.json olmadan doğru şekilde çalışamaz."
        )
    except json.JSONDecodeError as e:
        raise ValueError(f"config.py: global_config.json geçersiz JSON içeriyor: {e}")


_cfg = _load_global_config()

# --- Dışa açılan sabitler -------------------------------------------------
_sistem = _cfg.get("sistem", {})

MAX_AJAN_SAYISI = _sistem.get("max_ajan_sayisi", 200)

LOG_DIR = _sistem.get("log_klasoru", "./logs")
REPORT_DIR = _sistem.get("rapor_klasoru", "./reports")

# Gerekli klasörlerin var olduğundan emin ol
os.makedirs(LOG_DIR, exist_ok=True)
os.makedirs(REPORT_DIR, exist_ok=True)
