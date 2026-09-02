# -*- coding: utf-8 -*-
"""
access_control.py
==================
CEO onaylı giriş/çıkış mekanizması.

DÜRÜST NOT — GÜVENLİK KAPSAMI:
Bu modül TAM bir kimlik doğrulama/yetkilendirme sistemi DEĞİLDİR. Tek bir
paylaşılan anahtarla (CEO_ACCESS_KEY ortam değişkeni) korunan basit bir
kapıdır: anahtarı bilen herkes CEO gibi davranabilir. Üretim ortamı için
gerçek bir oturum sistemi (Flask-Login, JWT + rol bazlı yetkilendirme,
şifre + 2FA vb.) ile değiştirilmesi ŞİDDETLE önerilir. Bu haliyle sadece
"yanlışlıkla / yetkisiz tıklamayı" engeller, kararlı bir saldırıya karşı
koruma sağlamaz.

CEO_ACCESS_KEY ayarlanmadan (boş) bırakılırsa, onay/çıkış işlemleri
GÜVENLİK GEREĞİ tamamen reddedilir (fail-closed) — böylece anahtar
unutulduğunda sistem "herkese açık onay" moduna sessizce düşmez.
"""

import os
import json
import secrets
from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).resolve().parent
ACCESS_FILE = ROOT / "ceo_access_control.json"

CEO_ACCESS_KEY = os.environ.get("CEO_ACCESS_KEY", "").strip()

_DEFAULT = {"pending_requests": [], "active_sessions": [], "history": []}


def _load():
    if not ACCESS_FILE.exists():
        _save(_DEFAULT)
        return dict(_DEFAULT)
    try:
        with open(ACCESS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            for k, v in _DEFAULT.items():
                data.setdefault(k, v)
            return data
    except Exception:
        return dict(_DEFAULT)


def _save(data):
    with open(ACCESS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def verify_ceo_key(provided_key):
    if not CEO_ACCESS_KEY:
        return False, ("CEO_ACCESS_KEY ortam değişkeni ayarlanmamış — güvenlik gereği "
                        "tüm CEO onayları reddediliyor. Sunucuda CEO_ACCESS_KEY tanımlayın.")
    if not provided_key or not secrets.compare_digest(str(provided_key), CEO_ACCESS_KEY):
        return False, "Geçersiz CEO anahtarı."
    return True, None


class AccessControl:

    @staticmethod
    def list_pending():
        return _load()["pending_requests"]

    @staticmethod
    def list_active_sessions():
        return _load()["active_sessions"]

    @staticmethod
    def request_access(user_id, name=None, reason=""):
        """Bir kullanıcı/ajan sisteme erişim talep ettiğinde çağrılır
        (ör. WhatsApp/panel tarafından), bekleyen listeye ekler."""
        if not user_id:
            return {"status": "error", "message": "user_id gerekli."}
        data = _load()
        data["pending_requests"] = [r for r in data["pending_requests"] if r["user_id"] != user_id]
        entry = {
            "user_id": user_id,
            "name": name or user_id,
            "reason": reason,
            "requested_at": datetime.now().isoformat(),
        }
        data["pending_requests"].append(entry)
        _save(data)
        return {"status": "success", "request": entry}

    @staticmethod
    def approve_login(user_id, ceo_key):
        ok, err = verify_ceo_key(ceo_key)
        if not ok:
            return {"status": "error", "message": err}
        if not user_id:
            return {"status": "error", "message": "user_id gerekli."}

        data = _load()
        pending = data["pending_requests"]
        match = next((r for r in pending if r["user_id"] == user_id), None)
        name = match["name"] if match else user_id

        data["pending_requests"] = [r for r in pending if r["user_id"] != user_id]
        data["active_sessions"] = [s for s in data["active_sessions"] if s["user_id"] != user_id]
        session_entry = {
            "user_id": user_id,
            "name": name,
            "token": secrets.token_hex(16),
            "approved_at": datetime.now().isoformat(),
        }
        data["active_sessions"].append(session_entry)
        data["history"].append({"action": "approve_login", "user_id": user_id,
                                 "ts": datetime.now().isoformat()})
        _save(data)
        return {"status": "success", "message": f"{name} için sisteme giriş onaylandı.",
                "session": session_entry}

    @staticmethod
    def force_logout(user_id, ceo_key):
        ok, err = verify_ceo_key(ceo_key)
        if not ok:
            return {"status": "error", "message": err}
        if not user_id:
            return {"status": "error", "message": "user_id gerekli."}

        data = _load()
        before = len(data["active_sessions"])
        removed = [s for s in data["active_sessions"] if s["user_id"] == user_id]
        data["active_sessions"] = [s for s in data["active_sessions"] if s["user_id"] != user_id]
        if len(data["active_sessions"]) == before:
            return {"status": "error", "message": f"'{user_id}' için aktif oturum bulunamadı."}

        data["history"].append({"action": "force_logout", "user_id": user_id,
                                 "ts": datetime.now().isoformat()})
        _save(data)
        name = removed[0]["name"] if removed else user_id
        return {"status": "success", "message": f"{name} oturumu CEO tarafından sonlandırıldı."}
