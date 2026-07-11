import hashlib
import hmac
import html
import json
import math
import os
import sys
import time
import traceback
import ctypes
from datetime import datetime, timedelta
from urllib.parse import quote
from urllib.request import Request, urlopen
from xml.etree import ElementTree as ET

import streamlit as st
import streamlit.components.v1 as components

from notification_utils import load_email_settings, send_email_message

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
TRM_AGENTS_DIR = os.path.join(BASE_DIR, "trm_agents")
COMMAND_HISTORY_FILE = os.path.join(BASE_DIR, "command_history.json")
ARCHIVED_COMMANDS_DIR = os.path.join(BASE_DIR, "data", "archived_commands")
DAILY_REPORTS_DIR = os.path.join(BASE_DIR, "exports", "daily_reports")
SHARED_REPORTS_DIR = os.path.join(BASE_DIR, "exports", "shared_reports")
HONORARY_MEMBERS_FILE = os.path.join(BASE_DIR, "honorary_members.json")
PERFORMANCE_TRENDS_FILE = os.path.join(BASE_DIR, "performance_trends.json")
IMECE_RSS_FEEDS = [
    ("Dijital İyilik", "https://news.google.com/rss/search?q=" + quote("digital social good OR digital wellbeing") + "&hl=tr&gl=TR&ceid=TR:tr"),
    ("Pazar Trendleri", "https://news.google.com/rss/search?q=" + quote("e-commerce trends OR retail technology") + "&hl=tr&gl=TR&ceid=TR:tr"),
]

if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)

if TRM_AGENTS_DIR not in sys.path:
    sys.path.append(TRM_AGENTS_DIR)

print(f"Python yolu: {sys.path}")

st.set_page_config(page_title="Sosyalİmece.org Yönetim Konsolu", layout="wide")


def get_email_settings():
    """E-posta ayarlarını Streamlit secrets içinden oku ve doğrula."""
    return load_email_settings(BASE_DIR)


def send_email(subject, body):
    """st.secrets içindeki Gmail SMTP ayarlarıyla e-posta gönder."""
    success, message = send_email_message(subject, body, BASE_DIR)
    print(f"[NotificationAgent] {message}")
    return success, message


def send_notification_email(product_count, output_path, trend_summary=""):
    """Otonom üretim tamamlandığında bildirim e-postası gönder."""
    subject = "Sosyalİmece.org | Otonom Üretim Başarıyla Tamamlandı"
    body = f"""
Sosyalİmece.org - Otonom Üretim Raporu

========================================
Üretim Zamanı: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Toplam Ürün Sayısı: {product_count}
Çıktı Dosyası: {output_path}
========================================

📊 {trend_summary}

Sistem otonom modda çalışmaya devam ediyor.
Her 6 saatte bir otomatik güncelleme yapılacak.

Sosyalİmece.org Yönetim Konsolu
"""
    return send_email(subject, body)


def send_system_active_email():
    """Test amaçlı 'Bildirim Sistemi Aktif' e-postası gönder."""
    subject = "Sosyalİmece.org | Bildirim Sistemi Aktif"
    body = f"""
Sosyalİmece.org bildirim sistemi başarıyla aktif edildi.

Test Zamanı: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Durum: Gmail SMTP bağlantısı test edildi.

Bu e-posta, NotificationAgent test bildirimi olarak gönderilmiştir.
"""
    return send_email(subject, body)


def send_agent_activation_email(agent_name="Content_Generator_Agent"):
    """Yeni ajan devreye alındığında onay e-postası gönder."""
    subject = f"Sosyalİmece.org | {agent_name} devreye alındı"
    body = f"""
Sosyalİmece.org fabrika sistemi güncellendi.

Durum: {agent_name} başarıyla sisteme eklendi ve CoreNexus entegrasyonu tamamlandı.
Zaman: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

NotificationAgent onayı: Aktif
"""
    return send_email(subject, body)


def load_latest_content_payload():
    """Content generator çıktılarının son kaydını oku."""
    output_path = os.path.join(BASE_DIR, "content_generator_outputs.json")
    if not os.path.exists(output_path):
        return None

    try:
        with open(output_path, "r", encoding="utf-8") as f:
            payloads = json.load(f)
        if isinstance(payloads, list) and payloads:
            return payloads[-1]
    except Exception:
        return None

    return None


def load_latest_queue_payload():
    """Sosyal medya kuyruğunun son kaydını oku."""
    queue_path = os.path.join(BASE_DIR, "sosyal_medya_kuyruk.json")
    if not os.path.exists(queue_path):
        return None

    try:
        with open(queue_path, "r", encoding="utf-8") as f:
            payloads = json.load(f)
        if isinstance(payloads, list) and payloads:
            return payloads[-1]
    except Exception:
        return None

    return None


def load_json_payload(file_name, expect_list=False):
    file_path = os.path.join(BASE_DIR, file_name)
    if not os.path.exists(file_path):
        return [] if expect_list else None

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        if expect_list:
            return data if isinstance(data, list) else []
        return data
    except Exception:
        return [] if expect_list else None


def load_latest_log_entry(file_name):
    payloads = load_json_payload(file_name, expect_list=True)
    if payloads:
        return payloads[-1]
    return None


def load_command_history():
    data = load_json_payload("command_history.json", expect_list=True)
    return data if isinstance(data, list) else []


def ensure_directory(path):
    os.makedirs(path, exist_ok=True)


def save_command_history(history):
    try:
        with open(COMMAND_HISTORY_FILE, "w", encoding="utf-8") as f:
            json.dump(history[-120:], f, ensure_ascii=False, indent=2)
    except Exception as exc:
        print(f"[CommandHistory] Kaydetme hatası: {exc}")


def archive_voice_command(entry):
    ensure_directory(ARCHIVED_COMMANDS_DIR)
    file_name = f"{datetime.now().strftime('%Y-%m-%d')}.json"
    archive_path = os.path.join(ARCHIVED_COMMANDS_DIR, file_name)
    archive_rows = []
    if os.path.exists(archive_path):
        try:
            with open(archive_path, "r", encoding="utf-8") as f:
                archive_rows = json.load(f)
            if not isinstance(archive_rows, list):
                archive_rows = []
        except Exception:
            archive_rows = []
    archive_rows.append(entry)
    with open(archive_path, "w", encoding="utf-8") as f:
        json.dump(archive_rows[-300:], f, ensure_ascii=False, indent=2)


def load_archived_command_history(days=14):
    ensure_directory(ARCHIVED_COMMANDS_DIR)
    rows = []
    file_names = sorted([name for name in os.listdir(ARCHIVED_COMMANDS_DIR) if name.endswith(".json")], reverse=True)
    for file_name in file_names[:days]:
        file_path = os.path.join(ARCHIVED_COMMANDS_DIR, file_name)
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                payload = json.load(f)
            if isinstance(payload, list):
                rows.extend(payload)
        except Exception:
            continue
    return rows


def load_honorary_members():
    if not os.path.exists(HONORARY_MEMBERS_FILE):
        return []
    try:
        with open(HONORARY_MEMBERS_FILE, "r", encoding="utf-8") as f:
            rows = json.load(f)
        return rows if isinstance(rows, list) else []
    except Exception:
        return []


def save_honorary_members(rows):
    with open(HONORARY_MEMBERS_FILE, "w", encoding="utf-8") as f:
        json.dump(rows, f, ensure_ascii=False, indent=2)


def load_performance_trends():
    if not os.path.exists(PERFORMANCE_TRENDS_FILE):
        return []
    try:
        with open(PERFORMANCE_TRENDS_FILE, "r", encoding="utf-8") as f:
            rows = json.load(f)
        return rows if isinstance(rows, list) else []
    except Exception:
        return []


def save_performance_trends(rows):
    with open(PERFORMANCE_TRENDS_FILE, "w", encoding="utf-8") as f:
        json.dump(rows[-180:], f, ensure_ascii=False, indent=2)


def generate_share_code(seed_text):
    digest = hashlib.sha256(seed_text.encode("utf-8")).hexdigest().upper()
    return f"SIM-{digest[:10]}"


def build_honorary_report_bundle(member_email, snapshot, kpis):
    briefing = build_daily_briefing(snapshot, kpis)
    ensure_directory(SHARED_REPORTS_DIR)
    share_code = generate_share_code(f"{member_email}|{datetime.now().strftime('%Y-%m-%d')}")
    file_name = f"fahri_rapor_{share_code}_{datetime.now().strftime('%Y%m%d')}.pdf"
    file_path = os.path.join(SHARED_REPORTS_DIR, file_name)
    with open(file_path, "wb") as f:
        f.write(briefing["pdf_bytes"])
    return {
        "share_code": share_code,
        "file_name": file_name,
        "file_path": file_path,
        "relative_link": f"http://localhost:8501/?fahri_uye_kodu={share_code}",
    }


@st.cache_data(ttl=900, show_spinner=False)
def fetch_imece_ticker_items():
    items = []
    for source_name, feed_url in IMECE_RSS_FEEDS:
        try:
            request = Request(feed_url, headers={"User-Agent": "SosyalImeceTicker/1.0"})
            with urlopen(request, timeout=6) as response:
                xml_data = response.read()
            root = ET.fromstring(xml_data)
            for item in root.findall(".//item")[:5]:
                title = (item.findtext("title") or "").strip()
                link = (item.findtext("link") or "").strip()
                if title:
                    items.append({"source": source_name, "title": title, "link": link})
        except Exception as exc:
            print(f"[Ticker] {source_name} verisi alınamadı: {exc}")

    if not items:
        return [
            {"source": "Sosyalİmece", "title": "Canlı haber akışı için ağ bağlantısı bekleniyor.", "link": ""},
            {"source": "Sosyalİmece", "title": "Yerel panel canlı kalmaya devam ediyor.", "link": ""},
        ]
    return items[:10]


def _is_sha256_digest(value):
    candidate = value.strip().lower()
    return len(candidate) == 64 and all(ch in "0123456789abcdef" for ch in candidate)


def get_panel_access_config():
    """
    Panel anahtari iki formatta okunabilir:
    - Duz metin: PERFORMANCE_PANEL_KEY = "guclu-anahtar"
    - SHA256: PERFORMANCE_PANEL_KEY = "sha256:<64_hex>"

    Geriye uyumluluk icin PERFORMANCE_PANEL_KEY yoksa EMAIL_PASSWORD kullanilir.
    """
    dedicated_key = str(st.secrets.get("PERFORMANCE_PANEL_KEY", "")).strip()
    if dedicated_key:
        if dedicated_key.lower().startswith("sha256:"):
            digest = dedicated_key.split(":", 1)[1].strip().lower()
            if _is_sha256_digest(digest):
                return {"mode": "sha256", "value": digest, "source": "PERFORMANCE_PANEL_KEY"}
            return {"mode": "invalid", "value": "", "source": "PERFORMANCE_PANEL_KEY"}
        return {"mode": "plain", "value": dedicated_key, "source": "PERFORMANCE_PANEL_KEY"}

    fallback = str(st.secrets.get("EMAIL_PASSWORD", "")).strip()
    if fallback:
        return {"mode": "plain", "value": fallback, "source": "EMAIL_PASSWORD"}

    return None


def verify_panel_access_key(entered_key, access_config):
    if not access_config or access_config.get("mode") == "invalid":
        return False

    normalized = entered_key.strip()
    expected_value = access_config["value"]
    if access_config.get("source") == "EMAIL_PASSWORD":
        normalized = "".join(normalized.split())
        expected_value = "".join(expected_value.split())

    if access_config["mode"] == "sha256":
        return hmac.compare_digest(hashlib.sha256(normalized.encode("utf-8")).hexdigest(), expected_value)
    return hmac.compare_digest(normalized, expected_value)


def render_panel_access_guard():
    st.subheader("Zero-Trust Erişimi")
    access_config = get_panel_access_config()
    if not access_config:
        st.error("Panel erişim anahtarı tanımlı değil. `.streamlit/secrets.toml` içine `PERFORMANCE_PANEL_KEY` ekleyin.")
        return False

    if access_config.get("mode") == "invalid":
        st.error("`PERFORMANCE_PANEL_KEY` SHA256 formatinda ise `sha256:<64_hex>` biciminde olmalidir.")
        return False

    if st.session_state.get("performance_panel_authorized"):
        st.success("İmece Performans erişimi doğrulandı.")
        return True

    entered_key = st.text_input("Yönetim konsolu erişim anahtarı", type="password", key="performance_panel_key_input")
    st.caption("Beklenen format: düz metin anahtar veya `sha256:<64_hex>` olarak saklanan anahtar.")
    if st.button("İmece Performans Kilidini Aç", key="unlock_performance_panel"):
        if verify_panel_access_key(entered_key, access_config):
            st.session_state["performance_panel_authorized"] = True
            st.success("Erişim doğrulandı. Performans merkezi açıldı.")
            return True
        st.error("Erişim anahtarı hatalı.")
    return False


def render_metric_card(title, value, help_text=""):
    st.metric(title, value, help=help_text if help_text else None)


def clamp(value, min_value=0, max_value=100):
    return max(min_value, min(max_value, value))


def init_session_state():
    st.session_state.setdefault("console_page", "Ana Panel")
    st.session_state.setdefault("latest_content_payload", None)
    st.session_state.setdefault("latest_queue_payload", None)
    st.session_state.setdefault("last_run_result", None)
    st.session_state.setdefault("command_palette_input", "")
    st.session_state.setdefault("command_palette_source", "keyboard")
    st.session_state.setdefault("command_feedback", "")
    st.session_state.setdefault("command_history", load_command_history())
    st.session_state.setdefault("honorary_members", load_honorary_members())
    st.session_state.setdefault("system_health_history", [])
    st.session_state.setdefault("cpu_prev_times", None)
    st.session_state.setdefault("last_daily_report_export", "")
    st.session_state.setdefault("self_healing_message", "")
    st.session_state.setdefault("show_splash_screen", True)
    st.session_state.setdefault("production_ready", True)


def inject_console_styles():
    st.markdown(
        """
        <style>
        .stApp {
            background:
                radial-gradient(circle at top left, rgba(212,175,55,0.18), transparent 28%),
                radial-gradient(circle at top right, rgba(6,78,59,0.22), transparent 26%),
                linear-gradient(135deg, #020817 0%, #031320 45%, #064E3B 100%);
            color: #E5EEF8;
        }
        .block-container {
            padding-top: 1.2rem;
            padding-bottom: 2rem;
        }
        div[role="radiogroup"] {
            display: flex;
            gap: 0.65rem;
            padding: 0.55rem;
            border-radius: 18px;
            background: rgba(15, 23, 42, 0.48);
            border: 1px solid rgba(212, 175, 55, 0.22);
            backdrop-filter: blur(18px);
            margin-bottom: 1rem;
        }
        div[role="radiogroup"] label {
            background: rgba(255,255,255,0.06);
            border: 1px solid rgba(255,255,255,0.08);
            border-radius: 14px;
            padding: 0.45rem 0.8rem;
        }
        div[role="radiogroup"] label[data-selected="true"] {
            background: rgba(212, 175, 55, 0.18);
            border: 1px solid rgba(212, 175, 55, 0.40);
        }
        .simece-card {
            background: rgba(255,255,255,0.08);
            border: 1px solid rgba(255,255,255,0.14);
            border-radius: 20px;
            padding: 1rem 1.1rem;
            backdrop-filter: blur(18px);
            box-shadow: 0 16px 40px rgba(2, 8, 23, 0.28);
            min-height: 132px;
        }
        .simece-card.gold {
            border-color: rgba(212, 175, 55, 0.42);
            box-shadow: 0 18px 40px rgba(212, 175, 55, 0.10);
        }
        .simece-card.green {
            border-color: rgba(16, 185, 129, 0.30);
        }
        .simece-card.blue {
            border-color: rgba(96, 165, 250, 0.28);
        }
        .simece-eyebrow {
            font-size: 0.78rem;
            letter-spacing: 0.08em;
            text-transform: uppercase;
            color: #D4AF37;
            margin-bottom: 0.4rem;
        }
        .simece-value {
            font-size: 2rem;
            font-weight: 700;
            color: #F8FAFC;
            line-height: 1.1;
        }
        .simece-subtitle {
            margin-top: 0.45rem;
            font-size: 0.92rem;
            color: #C8D4E3;
        }
        .simece-panel {
            background: rgba(255,255,255,0.06);
            border: 1px solid rgba(255,255,255,0.12);
            border-radius: 22px;
            padding: 1rem 1.1rem;
            backdrop-filter: blur(16px);
            margin-bottom: 1rem;
        }
        .simece-hero {
            background: linear-gradient(135deg, rgba(2,8,23,0.74), rgba(6,78,59,0.36));
            border: 1px solid rgba(212,175,55,0.24);
            border-radius: 24px;
            padding: 1.1rem 1.25rem;
            margin-bottom: 1rem;
            backdrop-filter: blur(18px);
        }
        .simece-hero-title {
            font-size: 2rem;
            font-weight: 800;
            color: #F8FAFC;
            margin-bottom: 0.3rem;
        }
        .simece-brand-row {
            display: flex;
            align-items: center;
            gap: 0.95rem;
        }
        .simece-brand-logo {
            width: 72px;
            height: 72px;
            flex-shrink: 0;
            filter: drop-shadow(0 12px 26px rgba(212,175,55,0.18));
        }
        .simece-brand-mark {
            display: inline-flex;
            align-items: center;
            gap: 0.65rem;
            margin-bottom: 0.55rem;
        }
        .simece-brand-minilogo {
            width: 28px;
            height: 28px;
            display: inline-block;
            vertical-align: middle;
        }
        .simece-badge {
            display: inline-flex;
            align-items: center;
            gap: 0.45rem;
            margin-top: 0.7rem;
            padding: 0.35rem 0.7rem;
            border-radius: 999px;
            background: rgba(212, 175, 55, 0.14);
            border: 1px solid rgba(212, 175, 55, 0.28);
            color: #F4E4A1;
            font-size: 0.82rem;
            font-weight: 600;
        }
        .simece-hero-caption {
            color: #C8D4E3;
            font-size: 0.98rem;
        }
        .simece-chip {
            display: inline-block;
            margin: 0.25rem 0.35rem 0 0;
            padding: 0.3rem 0.6rem;
            border-radius: 999px;
            background: rgba(212, 175, 55, 0.14);
            border: 1px solid rgba(212, 175, 55, 0.24);
            color: #F4E4A1;
            font-size: 0.84rem;
        }
        .simece-guide-title {
            font-size: 1.1rem;
            font-weight: 700;
            color: #F8FAFC;
            margin-bottom: 0.35rem;
        }
        .simece-guide-text {
            color: #CBD5E1;
            font-size: 0.95rem;
            line-height: 1.5;
        }
        div[data-testid="stButton"] button[kind="primary"] {
            background: linear-gradient(135deg, #7F1D1D, #DC2626);
            border: 1px solid rgba(248,113,113,0.45);
            color: #FEE2E2;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_glass_card(title, value, subtitle="", tone="gold"):
    st.markdown(
        f"""
        <div class="simece-card {tone}">
            <div class="simece-eyebrow">{html.escape(title)}</div>
            <div class="simece-value">{html.escape(str(value))}</div>
            <div class="simece-subtitle">{html.escape(subtitle)}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def get_imece_logo_svg(size=72, compact=False):
    icon_size = 28 if compact else size
    label = ""
    if compact:
        label = ""
    return f"""
    <svg class="{'simece-brand-minilogo' if compact else 'simece-brand-logo'}" width="{icon_size}" height="{icon_size}" viewBox="0 0 120 120" fill="none" xmlns="http://www.w3.org/2000/svg" aria-label="Sosyalİmece.org logosu">
      <defs>
        <linearGradient id="imeceGold" x1="20" y1="18" x2="95" y2="102" gradientUnits="userSpaceOnUse">
          <stop stop-color="#F7D97A"/>
          <stop offset="1" stop-color="#D4AF37"/>
        </linearGradient>
        <linearGradient id="imeceGreen" x1="18" y1="20" x2="100" y2="100" gradientUnits="userSpaceOnUse">
          <stop stop-color="#0F766E"/>
          <stop offset="1" stop-color="#064E3B"/>
        </linearGradient>
      </defs>
      <circle cx="60" cy="60" r="50" fill="rgba(2,8,23,0.38)" stroke="rgba(212,175,55,0.32)" stroke-width="2"/>
      <circle cx="60" cy="23" r="9" fill="url(#imeceGold)"/>
      <circle cx="93" cy="42" r="9" fill="url(#imeceGreen)"/>
      <circle cx="93" cy="79" r="9" fill="url(#imeceGold)"/>
      <circle cx="60" cy="97" r="9" fill="url(#imeceGreen)"/>
      <circle cx="27" cy="79" r="9" fill="url(#imeceGold)"/>
      <circle cx="27" cy="42" r="9" fill="url(#imeceGreen)"/>
      <circle cx="60" cy="60" r="12" fill="#020817" stroke="url(#imeceGold)" stroke-width="3"/>
      <path d="M60 23L93 42L93 79L60 97L27 79L27 42L60 23Z" stroke="url(#imeceGold)" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" opacity="0.95"/>
      <path d="M60 60L60 23M60 60L93 42M60 60L93 79M60 60L60 97M60 60L27 79M60 60L27 42" stroke="url(#imeceGreen)" stroke-width="2.6" stroke-linecap="round"/>
      <circle cx="60" cy="60" r="4" fill="#D4AF37"/>
    </svg>
    {label}
    """


def render_splash_screen():
    if not st.session_state.get("show_splash_screen", False):
        return

    splash = st.empty()
    splash.markdown(
        f"""
        <div style="
            position: relative;
            overflow: hidden;
            border-radius: 28px;
            padding: 1.7rem 1.8rem;
            margin-bottom: 1rem;
            min-height: 240px;
            background:
                radial-gradient(circle at 20% 20%, rgba(212,175,55,0.22), transparent 24%),
                radial-gradient(circle at 80% 30%, rgba(16,185,129,0.18), transparent 28%),
                linear-gradient(135deg, rgba(2,8,23,0.94), rgba(6,78,59,0.72));
            border: 1px solid rgba(212,175,55,0.28);
            box-shadow: 0 22px 60px rgba(2,8,23,0.35);
            backdrop-filter: blur(18px);
        ">
            <div style="display:flex; align-items:center; gap:1.2rem; position:relative; z-index:2;">
                {get_imece_logo_svg(size=84)}
                <div>
                    <div style="font-size:0.82rem; text-transform:uppercase; letter-spacing:0.18em; color:#D4AF37; margin-bottom:0.5rem;">
                        Sosyalİmece.org
                    </div>
                    <div style="font-size:2rem; font-weight:800; color:#F8FAFC; line-height:1.2;">
                        Dijital İyilik ve Üretim Ekosistemi
                    </div>
                    <div style="margin-top:0.65rem; color:#D9E4EF; font-size:1rem;">
                        Güvenli, şeffaf ve canlı üretim ritmiyle çalışan çok sayfalı yönetim konsolu hazırlanıyor.
                    </div>
                    <div style="margin-top:0.95rem; display:inline-flex; gap:0.6rem; align-items:center; padding:0.4rem 0.8rem; border-radius:999px; background:rgba(212,175,55,0.14); border:1px solid rgba(212,175,55,0.24); color:#F4E4A1; font-size:0.85rem;">
                        <span style="width:10px;height:10px;border-radius:50%;background:#10B981;display:inline-block; box-shadow:0 0 16px rgba(16,185,129,0.42);"></span>
                        Canlı Yayın Hazırlığı Tamamlanıyor
                    </div>
                </div>
            </div>
            <div style="position:absolute; inset:auto 0 0 0; height:4px; background:rgba(255,255,255,0.08); overflow:hidden;">
                <div style="width:42%; height:100%; background:linear-gradient(90deg, #D4AF37, #F7D97A, #10B981); animation:simeceSlide 1.65s ease-in-out infinite;"></div>
            </div>
            <style>
            @keyframes simeceSlide {{
                0% {{ transform: translateX(-120%); }}
                100% {{ transform: translateX(320%); }}
            }}
            </style>
        </div>
        """,
        unsafe_allow_html=True,
    )
    time.sleep(1.2)
    splash.empty()
    st.session_state["show_splash_screen"] = False


def render_console_header(snapshot):
    worker_status = snapshot.get("worker_status") or {}
    last_cycle = worker_status.get("last_cycle_at", "-")
    mode = worker_status.get("last_mode", "-")
    active_agents = len(worker_status.get("active_agents", []))
    production_badge = "Production Ready" if st.session_state.get("production_ready") else "Hazırlanıyor"
    st.markdown(
        f"""
        <div class="simece-hero">
            <div class="simece-brand-mark">
                {get_imece_logo_svg(compact=True)}
                <span style="font-size:0.88rem; text-transform:uppercase; letter-spacing:0.14em; color:#D4AF37;">Sosyalİmece.org</span>
            </div>
            <div class="simece-brand-row">
                {get_imece_logo_svg(size=72)}
                <div>
                    <div class="simece-hero-title">Sosyalİmece.org Çok Sayfalı Yönetim Konsolu</div>
                    <div class="simece-hero-caption">
                        Canlı ritim korunur, sayfalar bağımsız çalışır ve arka plandaki ajan akışı kesilmez.
                        Son nabız: {html.escape(str(last_cycle))} | Mod: {html.escape(str(mode))} | Aktif ajan: {active_agents}
                    </div>
                    <div class="simece-badge">İmece Ağı | {html.escape(production_badge)}</div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def apply_mood_system(kpis):
    mood = kpis.get("system_mood", "huzur")
    palette = {
        "huzur": {
            "bg": "radial-gradient(circle at top left, rgba(59,130,246,0.12), transparent 26%), radial-gradient(circle at top right, rgba(6,78,59,0.20), transparent 24%), linear-gradient(135deg, #020817 0%, #031320 45%, #064E3B 100%)",
            "accent": "#D4AF37",
        },
        "calisma": {
            "bg": "radial-gradient(circle at top left, rgba(251,146,60,0.18), transparent 28%), radial-gradient(circle at top right, rgba(212,175,55,0.18), transparent 22%), linear-gradient(135deg, #1f2937 0%, #3b2f18 45%, #7c2d12 100%)",
            "accent": "#FB923C",
        },
        "uyari": {
            "bg": "radial-gradient(circle at top left, rgba(248,113,113,0.22), transparent 28%), radial-gradient(circle at top right, rgba(212,175,55,0.18), transparent 20%), linear-gradient(135deg, #1f1b2e 0%, #3f1d1d 45%, #7f1d1d 100%)",
            "accent": "#F59E0B",
        },
    }.get(mood, {})
    st.markdown(
        f"""
        <style>
        .stApp {{
            background: {palette.get("bg")};
        }}
        .simece-hero {{
            border-color: {palette.get("accent", "#D4AF37")}55;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def get_system_cpu_percent():
    class FILETIME(ctypes.Structure):
        _fields_ = [("dwLowDateTime", ctypes.c_ulong), ("dwHighDateTime", ctypes.c_ulong)]

    idle_time, kernel_time, user_time = FILETIME(), FILETIME(), FILETIME()
    success = ctypes.windll.kernel32.GetSystemTimes(
        ctypes.byref(idle_time), ctypes.byref(kernel_time), ctypes.byref(user_time)
    )
    if not success:
        return 0.0

    def as_int(value):
        return (value.dwHighDateTime << 32) + value.dwLowDateTime

    current = {
        "idle": as_int(idle_time),
        "kernel": as_int(kernel_time),
        "user": as_int(user_time),
    }
    previous = st.session_state.get("cpu_prev_times")
    st.session_state["cpu_prev_times"] = current
    if not previous:
        return 0.0

    idle_delta = current["idle"] - previous["idle"]
    total_delta = (current["kernel"] - previous["kernel"]) + (current["user"] - previous["user"])
    if total_delta <= 0:
        return 0.0
    return round(max(0.0, min(100.0, (1 - (idle_delta / total_delta)) * 100)), 1)


def get_memory_percent():
    class MEMORYSTATUSEX(ctypes.Structure):
        _fields_ = [
            ("dwLength", ctypes.c_ulong),
            ("dwMemoryLoad", ctypes.c_ulong),
            ("ullTotalPhys", ctypes.c_ulonglong),
            ("ullAvailPhys", ctypes.c_ulonglong),
            ("ullTotalPageFile", ctypes.c_ulonglong),
            ("ullAvailPageFile", ctypes.c_ulonglong),
            ("ullTotalVirtual", ctypes.c_ulonglong),
            ("ullAvailVirtual", ctypes.c_ulonglong),
            ("ullAvailExtendedVirtual", ctypes.c_ulonglong),
        ]

    memory_status = MEMORYSTATUSEX()
    memory_status.dwLength = ctypes.sizeof(MEMORYSTATUSEX)
    if not ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(memory_status)):
        return 0.0
    return float(memory_status.dwMemoryLoad)


def update_system_health_history(kpis):
    cpu_percent = get_system_cpu_percent()
    ram_percent = get_memory_percent()
    simulated_traffic = round(
        24
        + (kpis.get("aktif_ajan", 0) * 1.8)
        + (kpis.get("dijital_katki_endeksi", 0) * 0.32)
        + (math.sin(time.time() / 18) + 1) * 14,
        1,
    )
    history = st.session_state.get("system_health_history", [])
    history.append(
        {
            "timestamp": datetime.now().strftime("%H:%M:%S"),
            "CPU": cpu_percent,
            "RAM": round(ram_percent, 1),
            "Trafik": simulated_traffic,
        }
    )
    st.session_state["system_health_history"] = history[-24:]
    return st.session_state["system_health_history"]


PAGE_GUIDES = {
    "Ana Panel": {
        "number": 1,
        "description": "Merkezi operasyon özeti, manuel kontrol, briefing ve içerik akışlarının başlangıç noktasıdır.",
        "next_page": "Ajanlar Ağı",
        "next_desc": "Aktif katmanları, ajan kümelerini ve canlı operasyon dağılımını görürsünüz.",
    },
    "Ajanlar Ağı": {
        "number": 2,
        "description": "Market, bridge ve sentinel ajanlarının canlı dağılımını ve ağ mimarisini gösterir.",
        "next_page": "İmece Performans",
        "next_desc": "KPI kartları, komut verimliliği ve trend analizleri burada yer alır.",
    },
    "İmece Performans": {
        "number": 3,
        "description": "Dijital katkı, komut etkinliği ve zaman içindeki üretim eğilimlerini izlersiniz.",
        "next_page": "Canlı Görsel Show",
        "next_desc": "Ajan kürelerinin senfonisini ve veri akışını görsel olarak takip edersiniz.",
    },
    "Canlı Görsel Show": {
        "number": 4,
        "description": "Ajanların birbiriyle olan canlı veri akışı, ödül parıltıları ve hareket ritmi burada sunulur.",
        "next_page": "Ayarlar",
        "next_desc": "Güvenlik, Fahri Üye erişimi ve sistem yapılandırmalarını yönetirsiniz.",
    },
    "Ayarlar": {
        "number": 5,
        "description": "Sistem yapılandırmaları, Zero-Trust erişimi ve Fahri Üye yönetimi bu sayfada toplanır.",
        "next_page": "Ana Panel",
        "next_desc": "Merkezi özet, self-healing kontrolü ve günlük briefing görünümüne dönersiniz.",
    },
}


def render_page_intro(page_name):
    guide = PAGE_GUIDES.get(page_name, {})
    st.markdown(
        f"""
        <div class="simece-panel">
            <div class="simece-eyebrow">Sayfa {guide.get('number', '-')} / 5</div>
            <div class="simece-guide-title">{html.escape(page_name)}</div>
            <div class="simece-guide-text">{html.escape(guide.get('description', ''))}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_next_page_hint(page_name):
    guide = PAGE_GUIDES.get(page_name, {})
    next_page = guide.get("next_page")
    next_desc = guide.get("next_desc", "")
    if not next_page:
        return
    st.markdown('<div class="simece-panel">', unsafe_allow_html=True)
    st.markdown(
        f"""
        <div class="simece-eyebrow">Sırada Ne Var?</div>
        <div class="simece-guide-title">Bir sonraki sayfada: {html.escape(next_page)}</div>
        <div class="simece-guide-text">{html.escape(next_desc)}</div>
        """,
        unsafe_allow_html=True,
    )
    if st.button(f"{next_page} sayfasına git", key=f"next_page_{page_name}", use_container_width=True):
        st.session_state["console_page"] = next_page
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)


def aggregate_trend_rows(rows, mode):
    grouped = {}
    for row in rows:
        date_str = row.get("date")
        if not date_str:
            continue
        try:
            dt = datetime.strptime(date_str, "%Y-%m-%d")
        except Exception:
            continue
        if mode == "daily":
            label = dt.strftime("%d.%m")
        elif mode == "weekly":
            iso = dt.isocalendar()
            label = f"{iso.year}-H{iso.week:02d}"
        else:
            label = dt.strftime("%Y-%m")

        bucket = grouped.setdefault(
            label,
            {"Periyot": label, "Dijital Katkı": [], "Sesli Komut": [], "İmece Başarı": []},
        )
        bucket["Dijital Katkı"].append(row.get("digital_contribution", 0))
        bucket["Sesli Komut"].append(row.get("voice_count", 0))
        bucket["İmece Başarı"].append(row.get("imece_success", 0))

    aggregated = []
    for label, values in grouped.items():
        aggregated.append(
            {
                "Periyot": label,
                "Dijital Katkı": round(sum(values["Dijital Katkı"]) / max(1, len(values["Dijital Katkı"])), 1),
                "Sesli Komut": round(sum(values["Sesli Komut"]) / max(1, len(values["Sesli Komut"])), 1),
                "İmece Başarı": round(sum(values["İmece Başarı"]) / max(1, len(values["İmece Başarı"])), 1),
            }
        )
    aggregated.sort(key=lambda item: item["Periyot"])
    limits = {"daily": 10, "weekly": 8, "monthly": 6}
    return aggregated[-limits.get(mode, 10):]


def update_performance_trends(kpis):
    today_key = datetime.now().strftime("%Y-%m-%d")
    rows = load_performance_trends()
    voice_today = 0
    for item in load_archived_command_history(days=2):
        timestamp = item.get("timestamp", "")
        if timestamp.startswith(today_key) and item.get("source") == "voice":
            voice_today += 1
    entry = {
        "date": today_key,
        "digital_contribution": kpis.get("dijital_katki_endeksi", 0),
        "voice_count": voice_today,
        "imece_success": kpis.get("imece_basari_skoru", 0),
    }
    existing = next((index for index, row in enumerate(rows) if row.get("date") == today_key), None)
    if existing is None:
        rows.append(entry)
    else:
        rows[existing] = entry
    save_performance_trends(rows)
    return rows


def render_trend_analysis():
    st.subheader("Günlük / Haftalık / Aylık Trend")
    rows = load_performance_trends()
    if not rows:
        st.info("Trend analizi için henüz yeterli tarihsel kayıt oluşmadı.")
        return
    c1, c2, c3 = st.columns(3)
    datasets = [
        ("Günlük Trend", aggregate_trend_rows(rows, "daily")),
        ("Haftalık Trend", aggregate_trend_rows(rows, "weekly")),
        ("Aylık Trend", aggregate_trend_rows(rows, "monthly")),
    ]
    for col, (title, data_rows) in zip([c1, c2, c3], datasets):
        with col:
            st.markdown(f"**{title}**")
            if data_rows:
                st.line_chart(data_rows, x="Periyot", y=["Dijital Katkı", "Sesli Komut", "İmece Başarı"], height=220)
            else:
                st.caption("Yeterli veri bekleniyor.")


def export_daily_briefing_file(snapshot, kpis, file_name, force=False):
    ensure_directory(DAILY_REPORTS_DIR)
    export_path = os.path.join(DAILY_REPORTS_DIR, file_name)
    if not force and os.path.exists(export_path):
        with open(export_path, "rb") as f:
            payload = f.read()
        return {"path": export_path, "bytes": payload}
    briefing = build_daily_briefing(snapshot, kpis)
    with open(export_path, "wb") as f:
        f.write(briefing["pdf_bytes"])
    return {"path": export_path, "bytes": briefing["pdf_bytes"]}


def run_daily_report_scheduler(snapshot, kpis):
    now = datetime.now()
    if now.hour < 3:
        return None
    file_name = f"sosyalimece_daily_briefing_{now.strftime('%Y%m%d')}_0300_auto.pdf"
    result = export_daily_briefing_file(snapshot, kpis, file_name, force=False)
    st.session_state["last_daily_report_export"] = now.strftime("%Y-%m-%d")
    return result


def run_self_healing():
    st.cache_data.clear()
    st.session_state["latest_content_payload"] = None
    st.session_state["latest_queue_payload"] = None
    st.session_state["command_feedback"] = ""
    st.session_state["show_splash_screen"] = False
    result = run_scraper_logic(show_ui=False)
    if result:
        st.session_state["last_run_result"] = result
        st.session_state["latest_content_payload"] = result.get("content_payload")
        st.session_state["latest_queue_payload"] = result.get("queue_payload")
    st.session_state["self_healing_message"] = "Sistem Kurtarıcı devrede: süreçler yenilendi ve operasyon saf akışa döndürüldü."


def normalize_ascii_pdf(text):
    table = str.maketrans(
        {
            "Ç": "C",
            "Ö": "O",
            "Ş": "S",
            "İ": "I",
            "I": "I",
            "Ü": "U",
            "Ğ": "G",
            "ç": "c",
            "ö": "o",
            "ş": "s",
            "ı": "i",
            "ü": "u",
            "ğ": "g",
        }
    )
    return text.translate(table)


def _pdf_escape(text):
    return text.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")


def build_simple_pdf(lines):
    safe_lines = [normalize_ascii_pdf(line)[:110] for line in lines]
    text_stream = ["BT", "/F1 12 Tf", "50 795 Td", "15 TL"]
    for index, line in enumerate(safe_lines):
        if index > 0:
            text_stream.append("T*")
        text_stream.append(f"({_pdf_escape(line)}) Tj")
    text_stream.append("ET")
    stream = "\n".join(text_stream)
    stream_bytes = stream.encode("latin-1", errors="replace")

    objects = [
        b"1 0 obj<< /Type /Catalog /Pages 2 0 R >>endobj\n",
        b"2 0 obj<< /Type /Pages /Kids [3 0 R] /Count 1 >>endobj\n",
        b"3 0 obj<< /Type /Page /Parent 2 0 R /MediaBox [0 0 595 842] /Resources << /Font << /F1 5 0 R >> >> /Contents 4 0 R >>endobj\n",
        f"4 0 obj<< /Length {len(stream_bytes)} >>stream\n".encode("latin-1") + stream_bytes + b"\nendstream\nendobj\n",
        b"5 0 obj<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>endobj\n",
    ]

    pdf = bytearray(b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n")
    offsets = [0]
    for obj in objects:
        offsets.append(len(pdf))
        pdf.extend(obj)
    xref_start = len(pdf)
    pdf.extend(f"xref\n0 {len(objects) + 1}\n".encode("latin-1"))
    pdf.extend(b"0000000000 65535 f \n")
    for offset in offsets[1:]:
        pdf.extend(f"{offset:010d} 00000 n \n".encode("latin-1"))
    pdf.extend(
        (
            "trailer\n"
            f"<< /Size {len(objects) + 1} /Root 1 0 R >>\n"
            f"startxref\n{xref_start}\n%%EOF"
        ).encode("latin-1")
    )
    return bytes(pdf)


def build_daily_briefing(snapshot, kpis):
    target_date = (datetime.now() - timedelta(days=1)).date()
    history = snapshot.get("intelligence_history", [])
    relevant_entries = []
    for entry in history:
        timestamp = entry.get("timestamp")
        if not timestamp:
            continue
        try:
            entry_dt = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
        except Exception:
            continue
        if entry_dt.date() == target_date:
            relevant_entries.append(entry)

    if not relevant_entries and history:
        relevant_entries = history[-4:]

    total_market = sum(len(item.get("market_intelligence", [])) for item in relevant_entries)
    total_bridge = sum(len(item.get("bridge_network", [])) for item in relevant_entries)
    total_hours = round(max(0.8, total_bridge * 0.55 + total_market * 0.25 + len(relevant_entries) * 0.9), 1)
    total_mb = round(max(8.0, total_market * 5.4 + total_bridge * 7.3 + len(relevant_entries) * 3.2), 1)
    nightly_fayda = round(clamp(total_hours * 5.2 + total_mb * 0.38), 1)
    command_history = st.session_state.get("command_history", [])
    voice_count = len([row for row in command_history if row.get("source") == "voice"])

    lines = [
        "SosyalImece.org Daily Briefing",
        f"Rapor Tarihi: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        f"Kapsanan Gun: {target_date.isoformat()}",
        "",
        f"Dijital Katki Endeksi: %{kpis.get('dijital_katki_endeksi', 0)}",
        f"Gece Boyunca Tahmini Fayda Skoru: %{nightly_fayda}",
        f"Tasarruf Edilen Insan-Saati: {total_hours}",
        f"Islenen Veri Miktari: {total_mb} MB",
        f"Bridge Sinyali: {total_bridge}",
        f"Market Sinyali: {total_market}",
        f"Sesli Komut Kayitlari: {voice_count}",
        "",
        "SosyalImece.org Nirvana Panel",
    ]
    return {
        "nightly_fayda": nightly_fayda,
        "nightly_hours": total_hours,
        "nightly_mb": total_mb,
        "pdf_bytes": build_simple_pdf(lines),
        "file_name": f"sosyalimece_daily_briefing_{datetime.now().strftime('%Y%m%d')}.pdf",
    }


def render_daily_briefing(snapshot, kpis):
    briefing = build_daily_briefing(snapshot, kpis)
    current_hour = datetime.now().hour
    greeting = "Günaydın Butonu" if current_hour < 12 else "Günlük Özet Butonu"
    export_day_key = datetime.now().strftime("%Y-%m-%d")
    if st.session_state.get("last_daily_report_export") != export_day_key:
        export_stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        export_daily_briefing_file(snapshot, kpis, f"sosyalimece_daily_briefing_{export_stamp}.pdf", force=True)
        st.session_state["last_daily_report_export"] = export_day_key

    st.subheader(greeting)
    st.caption(
        f"Dün gece tahmini dijital katkı: %{briefing['nightly_fayda']} | "
        f"{briefing['nightly_hours']:.1f} insan-saati | {briefing['nightly_mb']:.1f} MB veri"
    )
    st.caption(f"Otomatik export klasörü: {DAILY_REPORTS_DIR}")
    st.caption("03:00 scheduler aktif: gece briefing raporu uygun saatte otonom olarak üretilir.")
    st.download_button(
        "PDF raporunu indir",
        data=briefing["pdf_bytes"],
        file_name=briefing["file_name"],
        mime="application/pdf",
        use_container_width=True,
    )


def append_command_history(command_text, source, status, action):
    entry = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "command": command_text,
        "source": source,
        "status": status,
        "action": action,
    }
    history = st.session_state.get("command_history", [])
    history.append(entry)
    st.session_state["command_history"] = history[-120:]
    save_command_history(st.session_state["command_history"])
    if source == "voice":
        archive_voice_command(entry)


def execute_nirvana_command(command_text):
    normalized = command_text.strip().lower()
    source = st.session_state.get("command_palette_source", "keyboard").strip().lower() or "keyboard"
    if not normalized:
        return

    action = "izleme"
    status = "ok"
    feedback = "Komut işlendi."

    if "finans" in normalized or "performans" in normalized:
        st.session_state["console_page"] = "İmece Performans"
        action = "imece_performans"
        feedback = "İmece Performans sayfasına geçildi."
    elif "ajanlar" in normalized or "ajan ağı" in normalized:
        st.session_state["console_page"] = "Ajanlar Ağı"
        action = "ajanlar_agi"
        feedback = "Ajanlar Ağı sayfasına geçildi."
    elif "görsel" in normalized or "show" in normalized:
        st.session_state["console_page"] = "Canlı Görsel Show"
        action = "canli_gorsel_show"
        feedback = "Canlı Görsel Show sayfasına geçildi."
    elif "ayar" in normalized:
        st.session_state["console_page"] = "Ayarlar"
        action = "ayarlar"
        feedback = "Ayarlar sayfası açıldı."
    elif "ana panel" in normalized:
        st.session_state["console_page"] = "Ana Panel"
        action = "ana_panel"
        feedback = "Ana Panel açıldı."
    elif "sistemi başlat" in normalized or "havuzu çek" in normalized:
        result = run_scraper_logic(show_ui=False)
        st.session_state["last_run_result"] = result
        if result and result.get("content_payload"):
            st.session_state["latest_content_payload"] = result["content_payload"]
        if result and result.get("queue_payload"):
            st.session_state["latest_queue_payload"] = result["queue_payload"]
        action = "manuel_tetikleme"
        feedback = "Sistem tetiklendi ve güncel çıktılar yenilendi."
    elif "agent-" in normalized or "ajan-" in normalized or "agent " in normalized:
        st.session_state["console_page"] = "Ajanlar Ağı"
        action = "ajan_yonlendirme"
        feedback = f"{command_text.strip()} için Ajanlar Ağı izleme görünümü açıldı."
    else:
        status = "yorumlandi"
        feedback = f"Komut yorumlandı: {command_text.strip()} | En uygun aksiyon önerisi gösterildi."

    append_command_history(command_text.strip(), source, status, action)
    st.session_state["command_feedback"] = feedback
    st.session_state["command_palette_input"] = ""
    st.session_state["command_palette_source"] = "keyboard"


def render_command_palette():
    st.markdown(
        """
        <style>
        div[data-testid="stVerticalBlock"]:has(input[aria-label="Nirvana Komut Paleti"]) .nirvana-hidden-note {
            display: none;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
    hidden_col1, hidden_col2, hidden_col3 = st.columns([0.01, 0.01, 0.01])
    with hidden_col1:
        st.text_input("Nirvana Komut Paleti", key="command_palette_input", label_visibility="collapsed")
    with hidden_col2:
        st.text_input("Komut Kaynağı", key="command_palette_source", label_visibility="collapsed")
    with hidden_col3:
        run_cmd = st.button("Nirvana Komutunu İşlet")
        clear_cmd = st.button("Nirvana Komutunu Temizle")

    if run_cmd and st.session_state.get("command_palette_input", "").strip():
        execute_nirvana_command(st.session_state["command_palette_input"])
        st.rerun()
    if clear_cmd:
        st.session_state["command_palette_input"] = ""
        st.session_state["command_palette_source"] = "keyboard"
        st.rerun()

    if st.session_state.get("command_feedback"):
        st.info(st.session_state["command_feedback"])

    components.html(
        """
        <style>
        .nirvana-launcher {
            display:flex; align-items:center; justify-content:space-between; gap:14px;
            padding:10px 14px; border-radius:18px; border:1px solid rgba(212,175,55,0.24);
            background:rgba(255,255,255,0.06); color:#E5EEF8; font-family:Arial,sans-serif;
            backdrop-filter: blur(16px);
        }
        .nirvana-open-btn, .nirvana-mic-btn, .nirvana-action-btn {
            background:rgba(212,175,55,0.14); color:#F4E4A1; border:1px solid rgba(212,175,55,0.28);
            border-radius:12px; padding:10px 14px; cursor:pointer;
        }
        .nirvana-overlay {
            position:fixed; inset:0; display:none; z-index:999999;
            background:radial-gradient(circle at center, rgba(15,23,42,0.35), rgba(2,8,23,0.88));
            backdrop-filter: blur(18px);
            font-family:Arial,sans-serif;
        }
        .nirvana-overlay.open { display:flex; align-items:center; justify-content:center; }
        .nirvana-modal {
            width:min(880px, 92vw); padding:28px; border-radius:28px;
            border:1px solid rgba(212,175,55,0.28);
            background:linear-gradient(135deg, rgba(2,8,23,0.92), rgba(6,78,59,0.42));
            box-shadow:0 24px 80px rgba(2,8,23,0.45), 0 0 30px rgba(212,175,55,0.12);
            color:#E5EEF8; position:relative; overflow:hidden;
        }
        .nirvana-modal::before {
            content:""; position:absolute; inset:0;
            background:linear-gradient(90deg, transparent, rgba(212,175,55,0.06), transparent);
            transform:translateX(-100%); animation:nirvanaScan 4.4s linear infinite;
        }
        .nirvana-modal h2 { margin:0 0 8px; font-size:30px; color:#F8FAFC; position:relative; z-index:1; }
        .nirvana-modal p { margin:0 0 18px; color:#CBD5E1; position:relative; z-index:1; }
        .nirvana-modal input {
            width:100%; padding:16px 18px; border-radius:16px; border:1px solid rgba(212,175,55,0.25);
            background:rgba(255,255,255,0.06); color:#F8FAFC; font-size:18px; outline:none; position:relative; z-index:1;
        }
        .nirvana-actions { display:flex; gap:12px; margin-top:14px; position:relative; z-index:1; }
        .nirvana-shortcuts { margin-top:16px; color:#D4AF37; font-size:13px; position:relative; z-index:1; }
        @keyframes nirvanaScan {
            0% { transform:translateX(-100%); }
            100% { transform:translateX(100%); }
        }
        </style>
        <div class="nirvana-launcher">
            <div>
                <div style="font-weight:700; color:#F8FAFC;">Nirvana Command Palette</div>
                <div style="font-size:13px; color:#CBD5E1;">Ctrl + K ile tam ekran glassmorphism modal açılır.</div>
            </div>
            <button id="nirvanaOpen" class="nirvana-open-btn">Ctrl + K</button>
        </div>
        <div id="nirvanaOverlay" class="nirvana-overlay">
            <div class="nirvana-modal">
                <h2>Matrix Erişim Katmanı</h2>
                <p>Ajanlar arka planda çalışırken hızlı müdahale, sesli komut ve izleme akışını burada yönetin.</p>
                <input id="nirvanaModalInput" placeholder="Örn: Agent-105'i başlat | Finans Raporu | Ayarlar" />
                <div class="nirvana-actions">
                    <button id="nirvanaMic" class="nirvana-mic-btn">Mikrofonu Dinle</button>
                    <button id="nirvanaRun" class="nirvana-action-btn">Komutu İşlet</button>
                    <button id="nirvanaClear" class="nirvana-action-btn">Temizle</button>
                    <button id="nirvanaClose" class="nirvana-action-btn">Kapat</button>
                </div>
                <div class="nirvana-shortcuts">Kısayollar: Ctrl + K açar | Enter çalıştırır | Esc kapatır</div>
            </div>
        </div>
        <script>
        const parentDoc = window.parent.document;
        const overlay = document.getElementById("nirvanaOverlay");
        const modalInput = document.getElementById("nirvanaModalInput");
        const openBtn = document.getElementById("nirvanaOpen");
        const closeBtn = document.getElementById("nirvanaClose");
        const runBtn = document.getElementById("nirvanaRun");
        const clearBtn = document.getElementById("nirvanaClear");
        const micBtn = document.getElementById("nirvanaMic");
        function setStreamlitInput(label, value) {
            const input = parentDoc.querySelector(`input[aria-label="${label}"]`);
            if (!input) return false;
            const setter = Object.getOwnPropertyDescriptor(window.parent.HTMLInputElement.prototype, "value").set;
            setter.call(input, value);
            input.dispatchEvent(new Event("input", { bubbles: true }));
            input.dispatchEvent(new Event("change", { bubbles: true }));
            return true;
        }
        function clickStreamlitButton(labelText) {
            const buttons = Array.from(parentDoc.querySelectorAll("button"));
            const target = buttons.find((btn) => (btn.innerText || "").trim() === labelText);
            if (target) target.click();
        }
        function openOverlay() {
            overlay.classList.add("open");
            setTimeout(() => modalInput.focus(), 30);
            setStreamlitInput("Komut Kaynağı", "keyboard");
        }
        function closeOverlay() {
            overlay.classList.remove("open");
        }
        function runCommand(sourceValue) {
            const value = modalInput.value || "";
            if (!value.trim()) return;
            setStreamlitInput("Nirvana Komut Paleti", value);
            setStreamlitInput("Komut Kaynağı", sourceValue || "keyboard");
            clickStreamlitButton("Nirvana Komutunu İşlet");
            closeOverlay();
        }
        if (!window.parent.__simeceCtrlKBound) {
            window.parent.__simeceCtrlKBound = true;
            window.parent.addEventListener("keydown", (event) => {
                if ((event.ctrlKey || event.metaKey) && event.key.toLowerCase() === "k") {
                    event.preventDefault();
                    openOverlay();
                }
                if (event.key === "Escape") {
                    closeOverlay();
                }
            });
        }
        openBtn.addEventListener("click", openOverlay);
        closeBtn.addEventListener("click", closeOverlay);
        clearBtn.addEventListener("click", () => {
            modalInput.value = "";
            setStreamlitInput("Nirvana Komut Paleti", "");
            setStreamlitInput("Komut Kaynağı", "keyboard");
            clickStreamlitButton("Nirvana Komutunu Temizle");
        });
        runBtn.addEventListener("click", () => runCommand("keyboard"));
        modalInput.addEventListener("keydown", (event) => {
            if (event.key === "Enter") {
                event.preventDefault();
                runCommand("keyboard");
            }
        });
        micBtn.addEventListener("click", () => {
            const SpeechRecognition = window.parent.SpeechRecognition || window.parent.webkitSpeechRecognition || window.SpeechRecognition || window.webkitSpeechRecognition;
            if (!SpeechRecognition) {
                micBtn.innerText = "Tarayıcı mikrofon API desteklemiyor";
                return;
            }
            const recognition = new SpeechRecognition();
            recognition.lang = "tr-TR";
            recognition.interimResults = false;
            recognition.maxAlternatives = 1;
            recognition.onstart = () => {
                micBtn.innerText = "Dinleniyor...";
            };
            recognition.onresult = (event) => {
                const transcript = event.results[0][0].transcript || "";
                modalInput.value = transcript;
                micBtn.innerText = "Sesli komut alındı";
                runCommand("voice");
            };
            recognition.onerror = () => {
                micBtn.innerText = "Mikrofon hatası";
            };
            recognition.onend = () => {
                setTimeout(() => { micBtn.innerText = "Mikrofonu Dinle"; }, 1200);
            };
            recognition.start();
        });
        </script>
        """,
        height=110,
    )


def render_command_efficiency():
    live_history = st.session_state.get("command_history", [])
    archived_voice = load_archived_command_history(days=30)
    history = archived_voice + [row for row in live_history if row.get("source") != "voice"]
    st.subheader("Komut Verimliliği")
    if not history:
        st.info("Henüz komut geçmişi oluşmadı.")
        return

    voice_commands = [row for row in history if row.get("source") == "voice"]
    keyboard_commands = [row for row in history if row.get("source") == "keyboard"]
    successful_voice = len([row for row in voice_commands if row.get("status") == "ok"])
    voice_efficiency = round((successful_voice / max(1, len(voice_commands))) * 100, 1)

    c1, c2, c3 = st.columns(3)
    with c1:
        render_metric_card("Sesli Komut", len(voice_commands))
    with c2:
        render_metric_card("Klavye Komutu", len(keyboard_commands))
    with c3:
        render_metric_card("Komut Verimliliği", f"%{voice_efficiency}")

    chart_rows = [
        {"Kaynak": "Sesli", "Adet": len(voice_commands)},
        {"Kaynak": "Klavye", "Adet": len(keyboard_commands)},
    ]
    st.bar_chart(chart_rows, x="Kaynak", y="Adet")
    st.caption("Grafik, tarih bazlı arşivlenen sesli komut kayıtlarıyla her sabah otomatik beslenir.")
    st.dataframe(history[-10:][::-1], use_container_width=True, hide_index=True)


def render_imece_ticker():
    ticker_items = fetch_imece_ticker_items()
    ticker_html = []
    for item in ticker_items:
        title = html.escape(item.get("title", ""))
        source = html.escape(item.get("source", "Kaynak"))
        link = item.get("link", "")
        if link:
            ticker_html.append(f'<span class="ticker-item"><strong>{source}</strong> · <a href="{html.escape(link)}" target="_blank">{title}</a></span>')
        else:
            ticker_html.append(f'<span class="ticker-item"><strong>{source}</strong> · {title}</span>')

    components.html(
        f"""
        <style>
        .ticker-wrap {{
            overflow: hidden;
            border-radius: 18px;
            border: 1px solid rgba(212,175,55,0.24);
            background: rgba(2,8,23,0.78);
            backdrop-filter: blur(14px);
            padding: 10px 0;
            font-family: Arial, sans-serif;
            color: #E5EEF8;
        }}
        .ticker-track {{
            display: inline-flex;
            gap: 34px;
            white-space: nowrap;
            min-width: 100%;
            animation: imeceTicker 46s linear infinite;
        }}
        .ticker-item {{
            font-size: 13px;
            color: #DCE7F5;
        }}
        .ticker-item strong {{
            color: #D4AF37;
            margin-right: 8px;
        }}
        .ticker-item a {{
            color: #E5EEF8;
            text-decoration: none;
        }}
        @keyframes imeceTicker {{
            0% {{ transform: translateX(0%); }}
            100% {{ transform: translateX(-50%); }}
        }}
        </style>
        <div class="ticker-wrap">
            <div class="ticker-track">
                {''.join(ticker_html)}
                {''.join(ticker_html)}
            </div>
        </div>
        """,
        height=62,
    )


def render_system_health_footer(kpis):
    history = update_system_health_history(kpis)
    latest = history[-1] if history else {"CPU": 0.0, "RAM": 0.0, "Trafik": 0.0}
    st.markdown("### Sistem Sağlığı")
    c1, c2, c3 = st.columns(3)
    with c1:
        render_glass_card("CPU", f"%{latest['CPU']}", "Anlık işlemci kullanımı", "blue")
    with c2:
        render_glass_card("RAM", f"%{latest['RAM']}", "Anlık bellek kullanımı", "green")
    with c3:
        render_glass_card("Sunucu Trafiği", f"{latest['Trafik']} rps", "Simüle edilmiş Sosyalİmece.org trafiği", "gold")

    chart_rows = [{"Zaman": row["timestamp"], "CPU": row["CPU"], "RAM": row["RAM"], "Trafik": row["Trafik"]} for row in history]
    if chart_rows:
        st.line_chart(chart_rows, x="Zaman", y=["CPU", "RAM", "Trafik"], height=180)

def render_top_navigation():
    pages = ["Ana Panel", "Ajanlar Ağı", "İmece Performans", "Canlı Görsel Show", "Ayarlar"]
    current_page = st.radio(
        "Navigasyon",
        pages,
        index=pages.index(st.session_state.get("console_page", "Ana Panel")),
        horizontal=True,
        key="console_page",
        label_visibility="collapsed",
    )
    return current_page


def load_live_snapshot():
    return {
        "worker_status": load_json_payload("worker_status.json") or {},
        "intelligence_entry": load_latest_log_entry("intelligence_log.json") or {},
        "sentinel_entry": load_latest_log_entry("sentinel_alerts.json") or {},
        "content_payload": st.session_state.get("latest_content_payload") or load_latest_content_payload(),
        "queue_payload": st.session_state.get("latest_queue_payload") or load_latest_queue_payload(),
        "intelligence_history": load_json_payload("intelligence_log.json", expect_list=True)[-12:],
        "sentinel_history": load_json_payload("sentinel_alerts.json", expect_list=True)[-12:],
    }


def compute_console_kpis(snapshot):
    worker_status = snapshot.get("worker_status") or {}
    intelligence_entry = snapshot.get("intelligence_entry") or {}
    sentinel_entry = snapshot.get("sentinel_entry") or {}
    content_payload = snapshot.get("content_payload") or {}
    queue_payload = snapshot.get("queue_payload") or {}

    performance = worker_status.get("performance_metrics", {})
    queue_summary = worker_status.get("queue_summary", {})
    security = worker_status.get("security_status", {})
    market_reports = intelligence_entry.get("market_intelligence", [])
    bridge_reports = intelligence_entry.get("bridge_network", [])
    alerts = sentinel_entry.get("sentinel_alerts", [])
    active_agents = worker_status.get("active_agents", [])

    connected_agents = security.get("connected_agents") or len(active_agents)
    posted_count = queue_summary.get("posted", 0)
    pending_retry = queue_summary.get("pending_retry", 0)
    queued_items = len(queue_payload.get("items", [])) if isinstance(queue_payload, dict) else queue_summary.get("queued", 0)
    content_count = len(content_payload.get("contents", [])) if isinstance(content_payload, dict) else 0
    avg_bridge_health = 0
    if bridge_reports:
        avg_bridge_health = sum(item.get("freshness_score", 0) for item in bridge_reports) / len(bridge_reports)
    warning_count = len([item for item in alerts if item.get("severity") == "warning"])
    critical_count = len([item for item in alerts if item.get("severity") == "critical"])
    success_rate = float(performance.get("autonomous_success_rate", 0))
    heartbeat_speed = float(performance.get("heartbeat_speed_per_sec", 0))
    processed_record_count = (
        len(market_reports) * 11
        + len(bridge_reports) * 18
        + len(alerts) * 6
        + content_count * 14
        + queued_items * 9
        + posted_count * 12
    )
    processed_data_mb = round(max(12.0, processed_record_count * 0.72), 1)
    saved_human_hours = round(
        max(
            1.2,
            len(active_agents) * 0.18
            + len(bridge_reports) * 0.42
            + content_count * 0.55
            + posted_count * 0.75
            + queued_items * 0.12,
        ),
        1,
    )

    imece_basari_skoru = round(
        clamp(
            (success_rate * 0.40)
            + (min(100, connected_agents * 2.2) * 0.18)
            + (avg_bridge_health * 0.20)
            + (min(100, heartbeat_speed * 85) * 0.10)
            + (min(100, content_count * 6 + posted_count * 16) * 0.07)
            + (max(0, 100 - (warning_count * 3 + critical_count * 9 + pending_retry * 5)) * 0.05)
        ),
        1,
    )
    gunluk_erisim = int(sum(item.get("synced_offer_count", 0) for item in bridge_reports) * 7 + connected_agents * 9 + content_count * 16 + posted_count * 40)
    ortak_gorev_sayisi = len(market_reports) + len(bridge_reports) + len(alerts) + content_count + min(queued_items, 12)

    queue_ready = max(0, queued_items - pending_retry)
    beklemede = max(0, worker_status.get("agent_capacity_snapshot", {}).get("total_capacity", 0) - connected_agents)
    isleniyor = min(connected_agents, len(market_reports) + len(bridge_reports) + max(1, content_count))
    dijital_katki_endeksi = round(
        clamp(
            (saved_human_hours * 4.6)
            + (processed_data_mb * 0.34)
            + (posted_count * 6.5)
            + (queue_ready * 1.8)
            - (pending_retry * 5.5),
            0,
            100,
        ),
        1,
    )
    katkı_uretildi = bool(content_count or posted_count or queue_ready or len(bridge_reports))
    if critical_count or pending_retry >= 3:
        system_mood = "uyari"
        system_mood_label = "Çalışma Alarmı"
    elif isleniyor >= max(8, int(max(1, len(active_agents)) * 0.45)):
        system_mood = "calisma"
        system_mood_label = "Yoğun Üretim Modu"
    else:
        system_mood = "huzur"
        system_mood_label = "Huzur Modu"

    return {
        "imece_basari_skoru": imece_basari_skoru,
        "gunluk_erisim": gunluk_erisim,
        "ortak_gorev_sayisi": ortak_gorev_sayisi,
        "bagli_ajan": connected_agents,
        "aktif_ajan": len(active_agents),
        "beklemede_ajan": beklemede,
        "isleniyor_ajan": isleniyor,
        "queue_ready": queue_ready,
        "pending_retry": pending_retry,
        "warning_count": warning_count,
        "critical_count": critical_count,
        "avg_bridge_health": round(avg_bridge_health, 1),
        "success_rate": success_rate,
        "saved_human_hours": saved_human_hours,
        "processed_data_mb": processed_data_mb,
        "dijital_katki_endeksi": dijital_katki_endeksi,
        "katki_uretildi": katkı_uretildi,
        "system_mood": system_mood,
        "system_mood_label": system_mood_label,
    }


def render_intelligence_panel(intelligence_entry):
    st.subheader("İstihbarat Katmanı")
    if not intelligence_entry:
        st.info("Henüz intelligence log verisi oluşmadı.")
        return

    market_reports = intelligence_entry.get("market_intelligence", [])
    performance = intelligence_entry.get("performance_metrics", {})

    col1, col2, col3 = st.columns(3)
    with col1:
        render_metric_card("Fiyat Sinyali", len(market_reports))
    with col2:
        critical_count = len([item for item in market_reports if item.get("signal_priority") == "critical"])
        render_metric_card("Kritik Stok Baskısı", critical_count)
    with col3:
        render_metric_card("Kazanç Verimliliği", f"{performance.get('earnings_efficiency', 0):.2f} TL")

    chart_data = [
        {
            "Agent": item.get("agent_id"),
            "Rakip Fiyat": item.get("competitor_price", 0),
        }
        for item in market_reports
    ]
    if chart_data:
        st.bar_chart(chart_data, x="Agent", y="Rakip Fiyat")

    for item in market_reports:
        with st.expander(f"MarketIntelAgent_{int(item.get('agent_id', 0)):02d} | {item.get('product_name', '-')}"):
            st.markdown(f"**Bölge:** {item.get('region', '-')}")
            st.markdown(f"**Rakip Fiyat:** {item.get('competitor_price', 0):.2f} TL")
            st.markdown(f"**Stok Baskısı:** {item.get('stock_status', '-')}")
            st.markdown(f"**Öneri:** {item.get('smart_parameter', {}).get('recommended_angle', '-')}")
            st.markdown(f"**Öncelik:** {item.get('signal_priority', '-')}")


def render_bridge_network_panel(intelligence_entry):
    st.subheader("Ağ Köprüsü Katmanı")
    if not intelligence_entry:
        st.info("Henüz bridge network verisi oluşmadı.")
        return

    bridge_reports = intelligence_entry.get("bridge_network", [])
    if not bridge_reports:
        st.info("Bridge ajanlarından veri gelmedi.")
        return

    avg_health = sum(item.get("freshness_score", 0) for item in bridge_reports) / max(1, len(bridge_reports))
    col1, col2 = st.columns(2)
    with col1:
        render_metric_card("Aktif Bridge Senkronu", len(bridge_reports))
    with col2:
        render_metric_card("Ağ Sağlığı", f"{avg_health:.1f}/100")

    st.bar_chart(
        [
            {"Ağ": item.get("network_name"), "Sağlık": item.get("freshness_score", 0)}
            for item in bridge_reports
        ],
        x="Ağ",
        y="Sağlık",
    )

    for item in bridge_reports:
        with st.expander(f"{item.get('network_name', '-')} | BridgeAgent_{int(item.get('agent_id', 0)):02d}"):
            st.markdown(f"**Senkron Teklif Sayısı:** {item.get('synced_offer_count', 0)}")
            st.markdown(f"**Senkron Modu:** {item.get('recommended_sync_mode', '-')}")
            st.markdown(f"**Katalog Büyüklüğü:** {item.get('observed_catalog_size', 0)}")
            st.markdown(f"**Ağ Sağlığı:** {item.get('freshness_score', 0):.1f}")


def render_sentinel_panel(sentinel_entry):
    st.subheader("Sentinel Güvenlik Katmanı")
    if not sentinel_entry:
        st.info("Henüz sentinel güvenlik verisi oluşmadı.")
        return

    alerts = sentinel_entry.get("sentinel_alerts", [])
    security_status = sentinel_entry.get("security_status", {})

    risk_count = len([item for item in alerts if item.get("severity") in {"warning", "critical"}])
    security_score = max(0, 100 - (risk_count * 8))

    col1, col2, col3 = st.columns(3)
    with col1:
        render_metric_card("Sentinel Logu", len(alerts))
    with col2:
        render_metric_card("Riskli Anomali", risk_count)
    with col3:
        render_metric_card("Güvenlik Skoru", f"{security_score}/100")

    with st.expander("Sistem İçi Log"):
        st.write(
            {
                "zero_trust_enabled": security_status.get("zero_trust_enabled"),
                "stealth_mode_enabled": security_status.get("stealth_mode_enabled"),
                "encrypted_snapshots": security_status.get("encrypted_snapshots"),
                "connected_agents": security_status.get("connected_agents"),
            }
        )

    for item in alerts:
        severity = item.get("severity", "info")
        if severity == "critical":
            st.error(f"{item.get('watch_zone')}: {item.get('anomaly')}")
        elif severity == "warning":
            st.warning(f"{item.get('watch_zone')}: {item.get('anomaly')}")

    for item in alerts:
        with st.expander(f"SentinelAgent_{int(item.get('agent_id', 0)):02d} | {item.get('watch_zone', '-')}"):
            st.markdown(f"**Şiddet:** {item.get('severity', '-')}")
            st.markdown(f"**Anomali:** {item.get('anomaly', '-')}")
            st.markdown(f"**Retry Basıncı:** {item.get('pending_retry_count', 0)}")
            st.markdown(f"**Şifreli Snapshot:** {item.get('encrypted_snapshots', 0)}")


def render_entrepreneurship_dashboard(worker_status, intelligence_entry, sentinel_entry):
    st.subheader("İmece Performans Panoraması")
    metrics = (worker_status or {}).get("performance_metrics", {})
    capacity = (worker_status or {}).get("agent_capacity_snapshot", {})
    sentinel_alerts = (sentinel_entry or {}).get("sentinel_alerts", [])

    heartbeat_total = (worker_status or {}).get("heartbeat_capacity_total", 0)
    heartbeat_speed = metrics.get("heartbeat_speed_per_sec", 0)
    success_rate = metrics.get("autonomous_success_rate", 0)
    earnings_efficiency = metrics.get("earnings_efficiency", 0)

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        render_metric_card("200 Ajan Kapasitesi", heartbeat_total)
    with c2:
        render_metric_card("Heartbeat Hızı", f"{heartbeat_speed:.2f}/sn")
    with c3:
        render_metric_card("Kazanç Verimliliği", f"{earnings_efficiency:.2f} TL")
    with c4:
        render_metric_card("Otonom Başarı", f"%{success_rate:.2f}")

    snapshot_chart = [
        {"Kategori": "MarketIntel", "Adet": capacity.get("market_intel_agents", 0)},
        {"Kategori": "Bridge", "Adet": capacity.get("bridge_agents", 0)},
        {"Kategori": "Sentinel", "Adet": capacity.get("sentinel_agents", 0)},
    ]
    st.bar_chart(snapshot_chart, x="Kategori", y="Adet")

    if intelligence_entry:
        perf_history = load_json_payload("intelligence_log.json", expect_list=True)[-10:]
        history_rows = [
            {
                "Zaman": row.get("timestamp"),
                "Heartbeat": row.get("performance_metrics", {}).get("heartbeat_speed_per_sec", 0),
                "Verim": row.get("performance_metrics", {}).get("earnings_efficiency", 0),
                "Başarı": row.get("performance_metrics", {}).get("autonomous_success_rate", 0),
            }
            for row in perf_history
        ]
        if history_rows:
            st.line_chart(history_rows, x="Zaman", y=["Heartbeat", "Verim", "Başarı"])

    if sentinel_alerts:
            st.caption("Canlı güvenlik uyarı kartları")


def render_performance_center(snapshot, kpis):
    worker_status = snapshot.get("worker_status") or {}
    intelligence_entry = snapshot.get("intelligence_entry") or {}
    sentinel_entry = snapshot.get("sentinel_entry") or {}
    render_page_intro("İmece Performans")
    if not render_panel_access_guard():
        return

    security_status = (worker_status or {}).get("security_status", {})
    if not security_status.get("zero_trust_enabled"):
        st.error("Zero-Trust aktif değil. Panel erişimi durduruldu.")
        return

    card_cols = st.columns(5)
    with card_cols[0]:
        render_glass_card("İmece Başarı Skoru", f"%{kpis['imece_basari_skoru']}", "Ortak hedeflere yaklaşım seviyesi", "gold")
    with card_cols[1]:
        render_glass_card("Günlük Erişim", kpis["gunluk_erisim"], "Canlı loglardan türetilen tahmini erişim", "green")
    with card_cols[2]:
        render_glass_card("Ortak Görev Sayısı", kpis["ortak_gorev_sayisi"], "2+ ajan katkısıyla tamamlanan iş akışları", "blue")
    with card_cols[3]:
        render_glass_card(
            "Dijital Katkı Endeksi",
            f"%{kpis['dijital_katki_endeksi']}",
            f"{kpis['saved_human_hours']:.1f} insan-saati | {kpis['processed_data_mb']:.1f} MB veri",
            "gold",
        )
    with card_cols[4]:
        render_glass_card("Bekleyen Retry", kpis["pending_retry"], "Yeniden denenmek üzere sırada", "gold")

    st.success("İmece Performans merkezi canlı veriyle yüklendi.")
    if worker_status:
        st.caption(
            f"Son nabız: {worker_status.get('last_cycle_at', '-')} | "
            f"Mod: {worker_status.get('last_mode', '-')} | "
            f"Aktif ajan: {len(worker_status.get('active_agents', []))}"
        )
    st.caption(
        f"Dijital fayda skoru anlık hesaplanır: {kpis['saved_human_hours']:.1f} insan-saati tasarruf "
        f"| {kpis['processed_data_mb']:.1f} MB işlenen veri"
    )

    render_entrepreneurship_dashboard(worker_status, intelligence_entry, sentinel_entry)
    col1, col2 = st.columns([1.15, 0.85])
    with col1:
        render_intelligence_panel(intelligence_entry)
        render_bridge_network_panel(intelligence_entry)
    with col2:
        render_sentinel_panel(sentinel_entry)
        render_command_efficiency()
    render_trend_analysis()
    render_next_page_hint("İmece Performans")


def render_content_generator_section(payload):
    """Content_Generator_Agent çıktısını arayüzde göster."""
    st.subheader("Content_Generator_Agent Çıktıları")

    if not payload:
        st.info("Henüz üretilmiş içerik bulunmuyor. Önce sistemi çalıştırın.")
        return

    st.caption(
        f"Kaynak trend raporu: {payload.get('source_report_timestamp', '-')} | "
        f"Üretim zamanı: {payload.get('generated_at', '-')}"
    )
    
    with st.expander("Sistem İçi Log"):
        st.write(f"Öne çıkan trend ürün: **{payload.get('top_trend', '-')}**")

    for item in payload.get("contents", []):
        with st.expander(f"{item.get('position', '-')} - {item.get('product_name', 'İçerik')}"):
            st.markdown(f"**Kısa Başlık:** {item.get('short_caption', '-')}")
            st.markdown(
                f"**Fiyat / Komisyon:** {item.get('price', 0):.2f} TL | "
                f"%{item.get('commission_rate', 0):.2f} | "
                f"Tahmini Kazanç: {item.get('estimated_commission', 0):.2f} TL"
            )
            st.markdown(f"**Satış Metni:** {item.get('promo_text', '-')}")
            st.markdown(f"**Sosyal Medya Postu:**\n\n{item.get('social_post', '-')}")
            st.markdown(f"**CTA:** {item.get('call_to_action', '-')}")
            hashtags = " ".join(item.get("hashtags", []))
            st.markdown(f"**Hashtagler:** {hashtags}")


def render_queue_section(queue_payload):
    """QueueAgent tarafından oluşturulan sosyal medya kuyruğunu göster."""
    st.subheader("Sosyal Medya Kuyruğu")

    if not queue_payload:
        st.info("Henüz sosyal medya kuyruğu oluşmadı.")
        return

    st.caption(
        f"Kuyruk üretim zamanı: {queue_payload.get('generated_at', '-')} | "
        f"Kaynak rapor: {queue_payload.get('source_report_timestamp', '-')}"
    )

    for item in queue_payload.get("items", []):
        with st.expander(f"{item.get('scheduled_for', '-')} - {item.get('product_name', 'Post')}"):
            st.markdown(f"**Durum:** {item.get('status', '-')}")
            if item.get("posted_at"):
                st.markdown(f"**Yayın Zamanı:** {item.get('posted_at')}")
            st.markdown(
                f"**Komisyon Bilgisi:** %{item.get('commission_rate', 0):.2f} | "
                f"Tahmini Kazanç: {item.get('estimated_commission', 0):.2f} TL"
            )
            st.markdown(f"**Platformlar:** {', '.join(item.get('platforms', []))}")
            st.markdown(f"**Post Metni:**\n\n{item.get('post_text', '-')}")
            st.markdown(f"**Ürün Linki:** {item.get('product_url', '-')}")
            hashtags = " ".join(item.get("hashtags", []))
            st.markdown(f"**Hashtagler:** {hashtags}")
            if item.get("platform_results"):
                st.json(item.get("platform_results"))


def render_status_chips(snapshot, kpis):
    worker_status = snapshot.get("worker_status") or {}
    queue_summary = worker_status.get("queue_summary", {})
    st.markdown(
        "".join(
            [
                f'<span class="simece-chip">Canlı Ajan: {kpis["aktif_ajan"]}</span>',
                f'<span class="simece-chip">Bağlı Ajan: {kpis["bagli_ajan"]}</span>',
                f'<span class="simece-chip">Hazır Kuyruk: {kpis["queue_ready"]}</span>',
                f'<span class="simece-chip">Posted: {queue_summary.get("posted", 0)}</span>',
                f'<span class="simece-chip">Warning: {kpis["warning_count"]}</span>',
                f'<span class="simece-chip">Dijital Katkı: %{kpis["dijital_katki_endeksi"]}</span>',
            ]
        ),
        unsafe_allow_html=True,
    )


def render_snapshot_table(snapshot):
    with st.expander("Sistem İçi Log"):
        worker_status = snapshot.get("worker_status") or {}
        capacity = worker_status.get("agent_capacity_snapshot", {})
        queue_summary = worker_status.get("queue_summary", {})
        status_rows = [
            {"Alan": "Çalışma Modu", "Değer": worker_status.get("last_mode", "-")},
            {"Alan": "Son Nabız", "Değer": worker_status.get("last_cycle_at", "-")},
            {"Alan": "Toplam Kapasite", "Değer": capacity.get("total_capacity", 0)},
            {"Alan": "Bağlı Ajan", "Değer": worker_status.get("security_status", {}).get("connected_agents", 0)},
            {"Alan": "Kuyrukta Bekleyen", "Değer": queue_summary.get("queued", 0)},
            {"Alan": "Pending Retry", "Değer": queue_summary.get("pending_retry", 0)},
        ]
        st.dataframe(status_rows, use_container_width=True, hide_index=True)


def render_ana_panel(snapshot, kpis):
    render_page_intro("Ana Panel")
    card_cols = st.columns(4)
    with card_cols[0]:
        render_glass_card("İmece Başarı Skoru", f"%{kpis['imece_basari_skoru']}", "Sistemin ortak hedeflere ulaşma yüzdesi", "gold")
    with card_cols[1]:
        render_glass_card("Günlük Erişim", kpis["gunluk_erisim"], "Bugün ulaşılan kişi / nokta tahmini", "green")
    with card_cols[2]:
        render_glass_card("Ortak Görev Sayısı", kpis["ortak_gorev_sayisi"], "2+ ajan işbirliğiyle tamamlanan akışlar", "blue")
    with card_cols[3]:
        render_glass_card("Dijital Katkı", f"%{kpis['dijital_katki_endeksi']}", "Anlık fayda ve üretim skoru", "gold")

    render_status_chips(snapshot, kpis)

    left, right = st.columns([0.95, 1.05])
    with left:
        st.markdown('<div class="simece-panel">', unsafe_allow_html=True)
        st.subheader("Operasyon Kontrolü")
        st.info("Sosyalİmece.org canlı ritmi korunur; yalnızca istediğinizde manuel tetikleme yapılır.")
        settings, settings_error = get_email_settings()
        if settings:
            st.success("Bildirim altyapısı yüklendi.")
            st.caption(f"Gönderen: {settings['email_sender']} | Alıcı: {settings['email_receiver']}")
        else:
            st.warning(settings_error)

        button_col1, button_col2 = st.columns(2)
        with button_col1:
            if st.button("Bildirim test e-postası gönder", use_container_width=True):
                success, message = send_system_active_email()
                if success:
                    st.success(message)
                else:
                    st.error(message)
        with button_col2:
            if st.button("Sistemi Başlat ve Havuzu Çek", use_container_width=True):
                result = run_scraper_logic(show_ui=True)
                st.session_state["last_run_result"] = result
                if result and result.get("content_payload"):
                    st.session_state["latest_content_payload"] = result["content_payload"]
                if result and result.get("queue_payload"):
                    st.session_state["latest_queue_payload"] = result["queue_payload"]
                st.rerun()
        if st.button("Sistem Kurtarıcı | Self-Healing", type="primary", use_container_width=True):
            run_self_healing()
            st.rerun()
        if st.session_state.get("self_healing_message"):
            st.success(st.session_state["self_healing_message"])
        render_snapshot_table(snapshot)
        st.markdown("</div>", unsafe_allow_html=True)

    with right:
        st.markdown('<div class="simece-panel">', unsafe_allow_html=True)
        st.subheader("Canlı Özet")
        worker_status = snapshot.get("worker_status") or {}
        queue_summary = worker_status.get("queue_summary", {})
        security = worker_status.get("security_status", {})
        
        with st.expander("Sistem İçi Log"):
            st.write(
                {
                    "worker_state": worker_status.get("worker_state", "-"),
                    "last_mode": worker_status.get("last_mode", "-"),
                    "connected_agents": security.get("connected_agents", 0),
                    "zero_trust_enabled": security.get("zero_trust_enabled"),
                    "stealth_mode_enabled": security.get("stealth_mode_enabled"),
                    "pending_retry": queue_summary.get("pending_retry", 0),
                }
            )
        st.caption(f"Sistem Modu: {kpis['system_mood_label']}")
        st.markdown("</div>", unsafe_allow_html=True)
        st.markdown('<div class="simece-panel">', unsafe_allow_html=True)
        render_daily_briefing(snapshot, kpis)
        st.markdown("</div>", unsafe_allow_html=True)

    bottom_left, bottom_right = st.columns(2)
    with bottom_left:
        render_content_generator_section(snapshot.get("content_payload"))
    with bottom_right:
        render_queue_section(snapshot.get("queue_payload"))
    render_next_page_hint("Ana Panel")


def render_agents_agi(snapshot):
    render_page_intro("Ajanlar Ağı")
    worker_status = snapshot.get("worker_status") or {}
    intelligence_entry = snapshot.get("intelligence_entry") or {}
    sentinel_entry = snapshot.get("sentinel_entry") or {}
    capacity = worker_status.get("agent_capacity_snapshot", {})

    card_cols = st.columns(4)
    with card_cols[0]:
        render_glass_card("Toplam Kapasite", capacity.get("total_capacity", 0), "165 temel + 35 genişleme", "gold")
    with card_cols[1]:
        render_glass_card("MarketIntel", capacity.get("market_intel_agents", 0), "İstihbarat ajanları", "green")
    with card_cols[2]:
        render_glass_card("Bridge", capacity.get("bridge_agents", 0), "Ağ köprüsü ajanları", "blue")
    with card_cols[3]:
        render_glass_card("Sentinel", capacity.get("sentinel_agents", 0), "Güvenlik gözcüleri", "gold")

    col1, col2 = st.columns([1.1, 0.9])
    with col1:
        render_intelligence_panel(intelligence_entry)
        render_bridge_network_panel(intelligence_entry)
    with col2:
        render_sentinel_panel(sentinel_entry)
        active_agents = worker_status.get("active_agents", [])
        st.subheader("Canlı Ajan Listesi")
        if active_agents:
            st.dataframe([{"Ajan": item} for item in active_agents], use_container_width=True, hide_index=True)
        else:
            st.info("Canlı ajan listesi henüz oluşmadı.")
    render_next_page_hint("Ajanlar Ağı")


def build_agent_symphony_graph(snapshot):
    worker_status = snapshot.get("worker_status") or {}
    content_payload = snapshot.get("content_payload") or {}
    queue_payload = snapshot.get("queue_payload") or {}
    queue_summary = worker_status.get("queue_summary", {})
    active_agents = worker_status.get("active_agents", [])

    market_agents = sorted([name for name in active_agents if name.startswith("MarketIntelAgent_")])
    bridge_agents = sorted([name for name in active_agents if name.startswith("BridgeAgent_")])
    sentinel_agents = sorted([name for name in active_agents if name.startswith("SentinelAgent_")])
    other_agents = [name for name in active_agents if name not in market_agents + bridge_agents + sentinel_agents]

    nodes = []

    def status_for(name):
        if name == "Content_Generator_Agent":
            return "isleniyor" if content_payload.get("contents") else "beklemede"
        if name == "QueueAgent":
            return "isleniyor" if queue_payload.get("items") else "beklemede"
        if name == "PosterAgent":
            return "isleniyor" if queue_summary.get("pending_retry", 0) or queue_summary.get("posted", 0) else "aktif"
        if name == "HealthCheckAgent":
            return "aktif"
        if name in active_agents:
            if name.startswith("SentinelAgent_") or name.startswith("BridgeAgent_"):
                return "isleniyor"
            return "aktif"
        return "beklemede"

    core_ring = ["CoreNexus", "AnalystAgent", "Content_Generator_Agent", "QueueAgent", "PosterAgent", "HealthCheckAgent"]
    for name in core_ring:
        nodes.append({"name": name, "group": "Core", "status": status_for(name)})
    for name in other_agents:
        nodes.append({"name": name, "group": "Diğer", "status": status_for(name)})
    for name in market_agents:
        nodes.append({"name": name, "group": "Market", "status": status_for(name)})
    for name in bridge_agents:
        nodes.append({"name": name, "group": "Bridge", "status": status_for(name)})
    for name in sentinel_agents:
        nodes.append({"name": name, "group": "Sentinel", "status": status_for(name)})

    position_map = {}

    def place_ring(names, radius, start_deg, end_deg, center_x=540, center_y=310):
        if not names:
            return
        span = end_deg - start_deg
        for index, item in enumerate(names):
            ratio = 0.5 if len(names) == 1 else index / (len(names) - 1)
            angle = math.radians(start_deg + span * ratio)
            position_map[item] = {
                "x": center_x + math.cos(angle) * radius,
                "y": center_y + math.sin(angle) * radius,
            }

    place_ring(core_ring, 112, -130, 40)
    place_ring(other_agents, 180, 50, 140)
    place_ring(market_agents, 250, -160, -15)
    place_ring(bridge_agents, 250, 20, 155)
    place_ring(sentinel_agents, 305, 170, 345)

    for node in nodes:
        coords = position_map.get(node["name"], {"x": 540, "y": 310})
        node["x"] = round(coords["x"], 2)
        node["y"] = round(coords["y"], 2)

    edges = []
    for source, target in [
        ("CoreNexus", "AnalystAgent"),
        ("AnalystAgent", "Content_Generator_Agent"),
        ("Content_Generator_Agent", "QueueAgent"),
        ("QueueAgent", "PosterAgent"),
        ("PosterAgent", "HealthCheckAgent"),
    ]:
        edges.append((source, target, "core"))
    for name in market_agents:
        edges.append((name, "Content_Generator_Agent", "market"))
    for name in bridge_agents:
        edges.append((name, "QueueAgent", "bridge"))
    for name in sentinel_agents:
        edges.append((name, "HealthCheckAgent", "sentinel"))
    for name in other_agents:
        edges.append(("CoreNexus", name, "other"))

    return nodes, edges


def render_agent_symphony(snapshot, kpis):
    nodes, edges = build_agent_symphony_graph(snapshot)
    node_lookup = {node["name"]: node for node in nodes}
    color_map = {
        "aktif": ("#10B981", "#A7F3D0"),
        "beklemede": ("#64748B", "#CBD5E1"),
        "isleniyor": ("#D4AF37", "#FDE68A"),
    }
    edge_color = {
        "core": "#D4AF37",
        "market": "#38BDF8",
        "bridge": "#22C55E",
        "sentinel": "#F59E0B",
        "other": "#94A3B8",
    }
    reward_active = kpis.get("katki_uretildi", False)

    lines = []
    for source, target, edge_type in edges:
        if source not in node_lookup or target not in node_lookup:
            continue
        src = node_lookup[source]
        dst = node_lookup[target]
        reward_class = " reward-line" if reward_active and edge_type in {"core", "market", "bridge"} else ""
        lines.append(
            f'<line class="flow-line {edge_type}{reward_class}" x1="{src["x"]}" y1="{src["y"]}" '
            f'x2="{dst["x"]}" y2="{dst["y"]}" stroke="{edge_color[edge_type]}" />'
        )

    circles = []
    for node in nodes:
        fill, label_fill = color_map[node["status"]]
        safe_name = html.escape(node["name"])
        display_name = safe_name if len(safe_name) <= 20 else f"{safe_name[:17]}..."
        reward_glow = '<circle cx="{0}" cy="{1}" r="31" class="reward-glow" fill="#D4AF37" />'.format(node["x"], node["y"]) if reward_active and node["status"] != "beklemede" else ""
        circles.append(
            f"""
            <g class="agent-node {node['status']}">
                {reward_glow}
                <circle cx="{node['x']}" cy="{node['y']}" r="12" fill="{fill}" />
                <circle cx="{node['x']}" cy="{node['y']}" r="22" class="halo" fill="{fill}" />
                <text x="{node['x']}" y="{node['y'] + 33}" text-anchor="middle" fill="{label_fill}">{display_name}</text>
            </g>
            """
        )

    legend_html = (
        f"<div class='legend-item'><span class='legend-dot aktif'></span> Aktif: {kpis['aktif_ajan']}</div>"
        f"<div class='legend-item'><span class='legend-dot isleniyor'></span> İşleniyor: {kpis['isleniyor_ajan']}</div>"
        f"<div class='legend-item'><span class='legend-dot beklemede'></span> Beklemede: {kpis['beklemede_ajan']}</div>"
        f"<div class='legend-item'><span class='legend-dot isleniyor'></span> Dijital Katkı: %{kpis['dijital_katki_endeksi']}</div>"
    )

    components.html(
        f"""
        <style>
        .symphony-wrap {{
            background: radial-gradient(circle at top, rgba(212,175,55,0.12), transparent 28%), rgba(2,8,23,0.86);
            border: 1px solid rgba(212,175,55,0.24);
            border-radius: 24px;
            padding: 16px;
            backdrop-filter: blur(18px);
            color: #E5EEF8;
            font-family: Arial, sans-serif;
        }}
        .symphony-head {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            gap: 18px;
            margin-bottom: 12px;
        }}
        .symphony-title {{
            font-size: 24px;
            font-weight: 700;
            color: #F8FAFC;
        }}
        .symphony-sub {{
            font-size: 14px;
            color: #C8D4E3;
        }}
        .legend {{
            display: flex;
            gap: 16px;
            flex-wrap: wrap;
        }}
        .legend-item {{
            font-size: 13px;
            color: #D8E2F1;
        }}
        .legend-dot {{
            display: inline-block;
            width: 10px;
            height: 10px;
            border-radius: 50%;
            margin-right: 6px;
        }}
        .legend-dot.aktif {{ background: #10B981; }}
        .legend-dot.isleniyor {{ background: #D4AF37; }}
        .legend-dot.beklemede {{ background: #64748B; }}
        svg {{
            width: 100%;
            height: 620px;
        }}
        .flow-line {{
            stroke-width: 2.1;
            stroke-dasharray: 10 8;
            opacity: 0.58;
            animation: dash 4s linear infinite;
        }}
        .flow-line.reward-line {{
            stroke-width: 3.2;
            opacity: 0.92;
            filter: drop-shadow(0 0 10px rgba(212,175,55,0.85));
            animation: dash 3s linear infinite, rewardPulse 1.3s ease-in-out infinite;
        }}
        .agent-node circle.halo {{
            opacity: 0.12;
            animation: pulse 2.6s ease-in-out infinite;
        }}
        .agent-node .reward-glow {{
            opacity: 0.18;
            animation: rewardAura 1.6s ease-in-out infinite;
        }}
        .agent-node text {{
            font-size: 11px;
            font-weight: 600;
        }}
        @keyframes dash {{
            to {{ stroke-dashoffset: -72; }}
        }}
        @keyframes pulse {{
            0%, 100% {{ transform: scale(1); opacity: 0.08; }}
            50% {{ transform: scale(1.12); opacity: 0.20; }}
        }}
        @keyframes rewardPulse {{
            0%, 100% {{ opacity: 0.72; }}
            50% {{ opacity: 1; }}
        }}
        @keyframes rewardAura {{
            0%, 100% {{ opacity: 0.08; transform: scale(1); }}
            50% {{ opacity: 0.22; transform: scale(1.18); }}
        }}
        </style>
        <div class="symphony-wrap">
            <div class="symphony-head">
                <div>
                    <div class="symphony-title">Ajan Senfonisi</div>
                    <div class="symphony-sub">Canlı küre ağı, veri akışı çizgileri ve anlık durum tonları</div>
                </div>
                <div class="legend">{legend_html}</div>
            </div>
            <svg viewBox="0 0 1080 620">
                {''.join(lines)}
                {''.join(circles)}
            </svg>
        </div>
        """,
        height=700,
    )


def render_canli_gorsel_show(snapshot, kpis):
    render_page_intro("Canlı Görsel Show")
    card_cols = st.columns(4)
    with card_cols[0]:
        render_glass_card("Aktif Küre", kpis["aktif_ajan"], "Gerçek zamanlı devrede", "green")
    with card_cols[1]:
        render_glass_card("İşleniyor", kpis["isleniyor_ajan"], "Veri akışına temas eden ajanlar", "gold")
    with card_cols[2]:
        render_glass_card("Beklemede", kpis["beklemede_ajan"], "Kapasitede hazır bekleyen alan", "blue")
    with card_cols[3]:
        render_glass_card("Altın Katkı", f"%{kpis['dijital_katki_endeksi']}", "Görev tamamlandığında parlayan ödül ritmi", "gold")
    render_agent_symphony(snapshot, kpis)
    render_next_page_hint("Canlı Görsel Show")


def render_honorary_member_panel(snapshot, kpis):
    st.subheader("Fahri Üye Yönetim Paneli")
    with st.form("honorary_member_form", clear_on_submit=True):
        col1, col2 = st.columns([1.4, 1])
        with col1:
            member_email = st.text_input("Fahri üye e-posta adresi", placeholder="ornek@domain.org")
        with col2:
            member_name = st.text_input("Fahri üye adı", placeholder="Ad Soyad")
        submitted = st.form_submit_button("Fahri Üye Ekle / Güncelle", use_container_width=True)

    if submitted and member_email.strip():
        members = st.session_state.get("honorary_members", [])
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        member_record = {
            "name": member_name.strip() or member_email.split("@")[0],
            "email": member_email.strip(),
            "permission": "Sadece veri görüntüleme",
            "updated_at": now,
        }
        bundle = build_honorary_report_bundle(member_record["email"], snapshot, kpis)
        member_record.update(bundle)
        existing_index = next((index for index, row in enumerate(members) if row.get("email") == member_record["email"]), None)
        if existing_index is None:
            members.append(member_record)
        else:
            members[existing_index].update(member_record)
        st.session_state["honorary_members"] = members
        save_honorary_members(members)
        st.success(f"{member_record['email']} için Fahri Üye erişimi hazırlandı.")

    members = st.session_state.get("honorary_members", [])
    if not members:
        st.info("Henüz tanımlanmış Fahri Üye bulunmuyor.")
        return

    rows = []
    for member in members:
        rows.append(
            {
                "Ad": member.get("name"),
                "E-posta": member.get("email"),
                "Yetki": member.get("permission"),
                "Paylaşım Kodu": member.get("share_code"),
                "Dijital Erişim Linki": member.get("relative_link"),
                "PDF": member.get("file_path"),
            }
        )
    st.dataframe(rows, use_container_width=True, hide_index=True)
    for member in members:
        with st.expander(f"{member.get('name')} | Dijital Erişim Detayı"):
            with st.expander("Sistem İçi Log"):
                st.code(member.get("relative_link", ""))
            st.caption("Bu bağlantı panel içi dummy/local dijital erişim yapısı içindir.")
            st.link_button("Dijital Erişim Linkini Aç", member.get("relative_link", "http://localhost:8501/"))


def render_settings_page(snapshot):
    render_page_intro("Ayarlar")
    worker_status = snapshot.get("worker_status") or {}
    security = worker_status.get("security_status", {})
    settings, settings_error = get_email_settings()
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Bildirim ve Sistem Ayarları")
        if settings:
            st.success("E-posta ayarları hazır.")
            st.json(
                {
                    "email_sender": settings.get("email_sender"),
                    "email_receiver": settings.get("email_receiver"),
                    "smtp_server": settings.get("smtp_server"),
                    "smtp_port": settings.get("smtp_port"),
                }
            )
        else:
            st.warning(settings_error)

        if st.button("Bildirim test e-postası gönder", key="settings_test_email"):
            success, message = send_system_active_email()
            if success:
                st.success(message)
            else:
                st.error(message)

    with col2:
        st.subheader("Zero-Trust ve Oturum")
        access_config = get_panel_access_config()
        with st.expander("Sistem İçi Log"):
            st.write(
                {
                    "zero_trust_enabled": security.get("zero_trust_enabled"),
                    "stealth_mode_enabled": security.get("stealth_mode_enabled"),
                    "encrypted_snapshots": security.get("encrypted_snapshots"),
                    "registered_agents": len(security.get("registered_agents", [])),
                    "panel_key_source": (access_config or {}).get("source", "tanımlı değil"),
                }
            )
        lock_col1, lock_col2 = st.columns(2)
        with lock_col1:
            if st.button("Performans Verisini Yenile", use_container_width=True):
                st.rerun()
        with lock_col2:
            if st.button("Panel Oturumunu Kilitle", use_container_width=True):
                st.session_state["performance_panel_authorized"] = False
                st.rerun()
    st.markdown("---")
    render_honorary_member_panel(snapshot, compute_console_kpis(snapshot))
    render_next_page_hint("Ayarlar")


def run_scraper_logic(show_ui=True):
    from trm_agents.CoreNexus import CoreNexus
    from trm_agents.camouflage_agent import CamouflageAgent
    from trm_agents.account_manager_agent import AccountManagerAgent
    from trm_agents.analyst_agent import AnalystAgent
    from trm_agents.content_generator_agent import ContentGeneratorAgent
    from trm_agents.queue_agent import QueueAgent
    from trm_agents.poster_agent import PosterAgent
    from trm_agents.expansion_module import build_expansion_agents, get_capacity_snapshot

    nexus = CoreNexus(zero_trust=True, stealth_mode=True)
    camou = CamouflageAgent()
    account_mgr = AccountManagerAgent()
    content_generator = ContentGeneratorAgent()
    queue_agent = QueueAgent()
    poster_agent = PosterAgent()
    capacity_snapshot = get_capacity_snapshot()
    expansion_specs = build_expansion_agents()

    nexus.connect_agent("CamouflageAgent", camou)
    nexus.connect_agent("AccountManagerAgent", account_mgr)
    for spec in expansion_specs[:25]:
        nexus.connect_agent(
            spec["name"],
            spec["instance"],
            capabilities=spec["capabilities"],
            context_allowlist=spec["context_allowlist"],
        )
    nexus.connect_agent("Content_Generator_Agent", content_generator)
    nexus.connect_agent("QueueAgent", queue_agent)
    nexus.connect_agent("PosterAgent", poster_agent)
    for spec in expansion_specs[25:]:
        nexus.connect_agent(
            spec["name"],
            spec["instance"],
            capabilities=spec["capabilities"],
            context_allowlist=spec["context_allowlist"],
        )

    operator_identity = account_mgr.assign_operator_identity("TR")
    if show_ui:
        with st.expander("Sistem İçi Log"):
            st.write(f"Operatör Kimliği: {operator_identity['identity']}")
            st.write(f"E-posta: {operator_identity['email']}")

    mask_id = camou.mask_identity()
    if show_ui:
        with st.expander("Sistem İçi Log"):
            st.write(f"Maskeli Operasyon Aktif: {mask_id}")

    sample_products = [
        {"title": "Organik Zeytin Yagi 1L", "product_url": "https://www.trendyol.com/gida-saglik-ve-ozel-bakim/organik-urunler/organik-zeytin-yagi", "price": 349.90, "commission_rate": 28.0},
        {"title": "Kozmetik Cilt Bakim Seti", "product_url": "https://www.trendyol.com/kozmetik/cilt-bakim/cilt-bakim-seti", "price": 499.50, "commission_rate": 35.0},
        {"title": "Nemlendirici Krem", "product_url": "https://www.trendyol.com/kozmetik/cilt-bakim/nemlendirici-krem", "price": 189.90, "commission_rate": 22.0},
        {"title": "Şampuan 500ml", "product_url": "https://www.trendyol.com/kozmetik/sac-bakim/sampuan", "price": 159.90, "commission_rate": 18.0},
        {"title": "Bal 1kg", "product_url": "https://www.trendyol.com/gida-saglik-ve-ozel-bakim/tatli-urunler/bal", "price": 279.90, "commission_rate": 24.0},
    ]

    output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ACIL_SATIS_HAVUZU.txt")

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("=========================================\n")
        f.write("TRM ACIL NAKIT OTOMASYONU - ACIL SATIS HAVUZU\n")
        f.write("=========================================\n")
        f.write(f"Baslama Zamani: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Maske ID: {mask_id}\n")
        f.write(f"Operatör: {operator_identity['identity']}\n")
        f.write(f"E-posta: {operator_identity['email']}\n")
        f.write(f"Domain: {operator_identity['domain_authority']}\n")
        f.write(f"Toplam Urun: {len(sample_products)}\n")
        f.write("=========================================\n\n")

        affiliate_id = "trendurunlermarket"

        for p in sample_products:
            affiliate_link = p["product_url"]
            if "?" in affiliate_link:
                affiliate_link += f"&affiliate={affiliate_id}"
            else:
                affiliate_link += f"?affiliate={affiliate_id}"
            f.write(f"{p['title']} - {affiliate_link}\n")

    if show_ui:
        st.success(f"Havuz güncellendi! Dosya: {output_path}")
    else:
        print(f"[Otonom Mod] Havuz güncellendi: {output_path}")

    trend_summary = ""
    analysis_result = None
    try:
        analyst = AnalystAgent()
        analysis_result = analyst.analyze_pool(output_path)

        if analysis_result:
            trend_report_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "trend_raporlari.json")
            product_map = {item["title"]: item for item in sample_products}
            enriched_details = []
            for product_name, score in analysis_result.get("scores", {}).items():
                product_meta = product_map.get(product_name, {})
                price = float(product_meta.get("price", 0.0))
                commission_rate = float(product_meta.get("commission_rate", 0.0))
                enriched_details.append(
                    {
                        "product_name": product_name,
                        "trend_score": score,
                        "price": price,
                        "commission_rate": commission_rate,
                        "estimated_commission": round(price * commission_rate / 100, 2),
                        "product_url": product_meta.get("product_url", ""),
                    }
                )

            analysis_result["product_details"] = enriched_details
            if enriched_details:
                highest_commission_product = max(
                    enriched_details,
                    key=lambda item: (item.get("commission_rate", 0.0), item.get("estimated_commission", 0.0)),
                )
                analysis_result["top_commission_product"] = highest_commission_product["product_name"]
                analysis_result["top_commission_rate"] = highest_commission_product["commission_rate"]

            analyst.save_trend_report(analysis_result, trend_report_path)

            trend_summary = analyst.get_trend_summary(analysis_result)
            if show_ui:
                st.info(f"📊 {trend_summary}")
            else:
                print(f"[AnalystAgent] {trend_summary}")
    except Exception as e:
        if show_ui:
            st.error(f"Trend analizi hatası: {str(e)}")
        else:
            print(f"[AnalystAgent] Trend analizi hatası: {str(e)}")
        trend_summary = "Trend analizi yapılamadı."

    content_payload = None
    queue_payload = None
    poster_payload = None
    try:
        sync_results = nexus.run_system_sync(
            context={
                "trend_report": analysis_result,
                "active_agents": list(nexus.agents.keys()),
                "agent_capacity_snapshot": capacity_snapshot,
            }
        )
        content_payload = sync_results.get("Content_Generator_Agent") if sync_results else None
        queue_payload = sync_results.get("QueueAgent") if sync_results else None
        poster_payload = sync_results.get("PosterAgent") if sync_results else None
        if poster_payload:
            queue_payload = load_latest_queue_payload() or queue_payload
        if show_ui and content_payload:
            st.success("Content_Generator_Agent trend raporundan yeni satış içerikleri üretti.")
        if show_ui and queue_payload:
            st.success("QueueAgent içerikleri sosyal medya kuyruğuna aktardı.")
        if show_ui and poster_payload:
            st.success(
                "PosterAgent zamanı gelen içerikleri Instagram ve Facebook için işlemeye başladı. "
                f"Başarılı yayın: {poster_payload.get('posted_count', 0)}"
            )
    except Exception as e:
        if show_ui:
            st.error(f"Ajan zinciri hatası: {str(e)}")
        else:
            print(f"[AgentChain] Hata: {str(e)}")

    activation_message = None
    if show_ui:
        try:
            success, message = send_agent_activation_email("Content_Generator_Agent")
            activation_message = (success, message)
            if success:
                st.success(message)
            else:
                st.error(message)
        except Exception as e:
            st.error(f"Ajan aktivasyon bildirimi hatası: {str(e)}")

    if show_ui:
        try:
            success, message = send_notification_email(len(sample_products), output_path, trend_summary)
            if success:
                st.success(message)
            else:
                st.error(message)
        except Exception as e:
            st.error(f"E-posta gönderme hatası: {str(e)}")

    return {
        "output_path": output_path,
        "trend_summary": trend_summary,
        "content_payload": content_payload,
        "queue_payload": queue_payload,
        "poster_payload": poster_payload,
        "activation_message": activation_message,
    }


def main():
    try:
        init_session_state()
        inject_console_styles()
        render_splash_screen()
        snapshot = load_live_snapshot()
        kpis = compute_console_kpis(snapshot)
        update_performance_trends(kpis)
        run_daily_report_scheduler(snapshot, kpis)
        apply_mood_system(kpis)

        render_console_header(snapshot)
        render_command_palette()
        current_page = render_top_navigation()

        if current_page == "Ana Panel":
            render_ana_panel(snapshot, kpis)
        elif current_page == "Ajanlar Ağı":
            render_agents_agi(snapshot)
        elif current_page == "İmece Performans":
            render_performance_center(snapshot, kpis)
        elif current_page == "Canlı Görsel Show":
            render_canli_gorsel_show(snapshot, kpis)
        elif current_page == "Ayarlar":
            render_settings_page(snapshot)
        st.markdown("### İmece Ticker")
        render_imece_ticker()
        render_system_health_footer(kpis)

    except Exception as e:
        st.error(f"Hata oluştu: {str(e)}")
        st.exception(e)
        with st.expander("Sistem İçi Log"):
            st.code(traceback.format_exc())


if __name__ == "__main__":
    main()
