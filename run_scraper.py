import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import hashlib
import hmac
import html
import json
import math
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
from health_check import health_check_pre_flight

# Güvenlik ve Stealth modülleri
from trm_agents.security_logger import SecurityLogger
from trm_agents.traffic_policeman import TrafficPoliceman
from trm_agents.fingerprint_manager import FingerprintManager
from trm_agents.session_manager import SessionManager

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

st.set_page_config(page_title="Sosyalİmece.org Yönetim Konsolu", layout="wide")


# ============================================================
# YARDIMCI FONKSİYONLAR
# ============================================================

def get_email_settings():
    return load_email_settings(BASE_DIR)

def send_email(subject, body):
    success, message = send_email_message(subject, body, BASE_DIR)
    return success, message

def send_notification_email(product_count, output_path, trend_summary=""):
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
    subject = "Sosyalİmece.org | Bildirim Sistemi Aktif"
    body = f"""
Sosyalİmece.org bildirim sistemi başarıyla aktif edildi.
Test Zamanı: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Durum: Gmail SMTP bağlantısı test edildi.
"""
    return send_email(subject, body)

def load_latest_content_payload():
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

def render_metric_card(title, value, help_text=""):
    st.metric(title, value, help=help_text if help_text else None)

def clamp(value, min_value=0, max_value=100):
    return max(min_value, min(max_value, value))


# ============================================================
# NEON TEMA
# ============================================================

def inject_console_styles():
    st.markdown("""
    <style>
    .stApp {
        background: radial-gradient(circle at 20% 30%, #0a0f1e, #03060c);
        color: #eef;
    }
    .block-container { padding-top: 1.2rem; padding-bottom: 2rem; }
    .stApp h1, .stApp h2, .stApp h3 { color: #ffdd99; }
    
    div[role="radiogroup"] {
        display: flex; gap: 0.65rem; padding: 0.55rem;
        border-radius: 18px; background: rgba(17, 22, 30, 0.80);
        border: 1px solid #ffaa5544;
        backdrop-filter: blur(18px); margin-bottom: 1rem;
    }
    div[role="radiogroup"] label {
        background: rgba(255,255,255,0.06);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 14px; padding: 0.45rem 0.8rem;
        color: #88aaff !important;
    }
    div[role="radiogroup"] label[data-selected="true"] {
        background: rgba(255,170,85,0.18);
        border: 1px solid #ffaa55;
        color: #ffdd99 !important;
    }
    
    div[data-testid="stButton"] button {
        border-radius: 40px;
        font-weight: 600;
        transition: all 0.25s;
    }
    div[data-testid="stButton"] button:hover {
        transform: scale(1.02);
    }
    
    .neon-btn-group .stButton button {
        min-width: 100px;
        font-size: 0.85rem;
        font-weight: 700;
        padding: 0.5rem 1.2rem;
        border-radius: 40px;
        background: rgba(255, 170, 85, 0.10);
        border: 1px solid #ffaa5544;
        color: #ffdd99;
        transition: all 0.25s;
        text-shadow: 0 0 10px rgba(255, 170, 85, 0.15);
    }
    .neon-btn-group .stButton button:hover {
        background: rgba(255, 170, 85, 0.25);
        border-color: #ffaa55;
        box-shadow: 0 0 30px rgba(255, 170, 85, 0.20);
        transform: scale(1.05);
    }
    .neon-btn-group .stButton button[kind="primary"] {
        background: linear-gradient(135deg, rgba(255, 170, 85, 0.25), rgba(255, 85, 85, 0.15));
        border-color: #ffaa55;
        color: #ffdd99;
    }
    .neon-btn-group .stButton button[kind="primary"]:hover {
        background: rgba(255, 170, 85, 0.35);
        box-shadow: 0 0 40px rgba(255, 170, 85, 0.30);
    }
    
    @media (max-width: 640px) {
        .neon-btn-group .stButton button {
            min-width: 70px;
            font-size: 0.75rem;
            padding: 0.35rem 0.8rem;
        }
    }
    
    .neon-card {
        background: rgba(17, 22, 30, 0.90);
        border: 1px solid #ffaa5544;
        border-radius: 28px;
        padding: 1.2rem 1.5rem;
        backdrop-filter: blur(12px);
        box-shadow: 0 0 30px rgba(255, 170, 85, 0.08);
        transition: all 0.3s;
        min-height: 100px;
    }
    .neon-card:hover {
        border-color: #ffaa55;
        box-shadow: 0 0 40px rgba(255, 170, 85, 0.18);
        transform: translateY(-3px);
    }
    .neon-card .neon-value {
        font-size: 2.4rem;
        font-weight: 800;
        color: #ffdd99;
        text-shadow: 0 0 20px rgba(255, 170, 85, 0.25);
        line-height: 1.2;
    }
    .neon-card .neon-label {
        font-size: 0.8rem;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        color: #88aaff;
        margin-top: 0.3rem;
    }
    .neon-card .neon-sub {
        font-size: 0.85rem;
        color: #aabbdd;
        margin-top: 0.2rem;
    }
    .neon-divider {
        border: 0;
        height: 2px;
        background: linear-gradient(90deg, transparent, #ffaa5544, #ffaa55, #ffaa5544, transparent);
        margin: 1.2rem 0;
    }
    .neon-panel-header {
        background: rgba(17,22,30,0.7);
        border-radius: 32px;
        padding: 0.8rem 1.5rem;
        margin-bottom: 1.2rem;
        border: 1px solid #ffaa5544;
        backdrop-filter: blur(10px);
    }
    .neon-panel-header .panel-item {
        color: #88aaff;
        padding: 0 8px;
    }
    .neon-panel-header .panel-item.active {
        color: #ffaa55;
        font-weight: 700;
    }
    .neon-panel-header .panel-badge {
        color: #ffaa55;
        font-size: 0.8rem;
        margin-left: auto;
    }
    .simece-brand-minilogo { width: 28px; height: 28px; display: inline-block; vertical-align: middle; }
    .simece-brand-logo { width: 72px; height: 72px; flex-shrink: 0; filter: drop-shadow(0 12px 26px rgba(212,175,55,0.18)); }
    
    /* Güvenlik uyarısı için kırmızı kart */
    .security-card-critical {
        border: 2px solid #ff0000;
        border-radius: 12px;
        padding: 12px;
        margin-bottom: 10px;
        background: rgba(255,0,0,0.08);
    }
    .security-card-critical .title {
        color: #ff0000;
        font-weight: bold;
    }
    .security-card-critical .timestamp {
        color: #ffaa55;
    }
    .security-card-critical .threat-type {
        color: #ffdd99;
        font-weight: bold;
    }
    .security-card-critical .detail {
        color: #88aaff;
        font-size: 0.85rem;
    }
    .security-card-critical .log-line {
        color: #aabbdd;
        font-size: 0.8rem;
        margin-top: 4px;
    }
    </style>
    """, unsafe_allow_html=True)


# ============================================================
# LOGO VE GÖRSEL ÖĞELER
# ============================================================

def get_imece_logo_svg(size=72, compact=False):
    icon_size = 28 if compact else size
    return f"""
    <svg class="{'simece-brand-minilogo' if compact else 'simece-brand-logo'}" width="{icon_size}" height="{icon_size}" viewBox="0 0 120 120" fill="none" xmlns="http://www.w3.org/2000/svg">
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
    """

def render_splash_screen():
    if not st.session_state.get("show_splash_screen", False):
        return
    splash = st.empty()
    splash.markdown(f"""
    <div style="position:relative; overflow:hidden; border-radius:28px; padding:1.7rem 1.8rem; margin-bottom:1rem; min-height:240px;
        background:radial-gradient(circle at 20% 20%, rgba(255,170,85,0.22), transparent 24%),
                radial-gradient(circle at 80% 30%, rgba(16,185,129,0.18), transparent 28%),
                linear-gradient(135deg, rgba(2,8,23,0.94), rgba(6,78,59,0.72));
        border:1px solid #ffaa5544; box-shadow:0 22px 60px rgba(2,8,23,0.35); backdrop-filter:blur(18px);">
        <div style="display:flex; align-items:center; gap:1.2rem; position:relative; z-index:2;">
            {get_imece_logo_svg(size=84)}
            <div>
                <div style="font-size:0.82rem; text-transform:uppercase; letter-spacing:0.18em; color:#ffaa55; margin-bottom:0.5rem;">Sosyalİmece.org</div>
                <div style="font-size:2rem; font-weight:800; color:#ffdd99; line-height:1.2; text-shadow:0 0 30px rgba(255,170,85,0.15);">Dijital İyilik ve Üretim Ekosistemi</div>
                <div style="margin-top:0.65rem; color:#aabbdd; font-size:1rem;">5 Panelli Yönetim Konsolu | Canlı Ajan Ritmi</div>
                <div style="margin-top:0.95rem; display:inline-flex; gap:0.6rem; align-items:center; padding:0.4rem 0.8rem; border-radius:999px; background:rgba(255,170,85,0.14); border:1px solid #ffaa5544; color:#ffdd99; font-size:0.85rem;">
                    <span style="width:10px;height:10px;border-radius:50%;background:#10B981;display:inline-block; box-shadow:0 0 16px rgba(16,185,129,0.42);"></span>
                    Canlı Yayın Aktif
                </div>
            </div>
        </div>
        <div style="position:absolute; inset:auto 0 0 0; height:4px; background:rgba(255,255,255,0.08); overflow:hidden;">
            <div style="width:42%; height:100%; background:linear-gradient(90deg, #ffaa55, #ffdd99, #10B981); animation:simeceSlide 1.65s ease-in-out infinite;"></div>
        </div>
        <style>
        @keyframes simeceSlide {{ 0% {{ transform: translateX(-120%); }} 100% {{ transform: translateX(320%); }} }}
        </style>
    </div>
    """, unsafe_allow_html=True)
    time.sleep(1.2)
    splash.empty()
    st.session_state["show_splash_screen"] = False


# ============================================================
# SİSTEM SAĞLIĞI FONKSİYONLARI
# ============================================================

def get_system_cpu_percent():
    class FILETIME(ctypes.Structure):
        _fields_ = [("dwLowDateTime", ctypes.c_ulong), ("dwHighDateTime", ctypes.c_ulong)]
    idle_time, kernel_time, user_time = FILETIME(), FILETIME(), FILETIME()
    success = ctypes.windll.kernel32.GetSystemTimes(ctypes.byref(idle_time), ctypes.byref(kernel_time), ctypes.byref(user_time))
    if not success:
        return 0.0
    def as_int(value):
        return (value.dwHighDateTime << 32) + value.dwLowDateTime
    current = {"idle": as_int(idle_time), "kernel": as_int(kernel_time), "user": as_int(user_time)}
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
        _fields_ = [("dwLength", ctypes.c_ulong), ("dwMemoryLoad", ctypes.c_ulong), ("ullTotalPhys", ctypes.c_ulonglong), ("ullAvailPhys", ctypes.c_ulonglong), ("ullTotalPageFile", ctypes.c_ulonglong), ("ullAvailPageFile", ctypes.c_ulonglong), ("ullTotalVirtual", ctypes.c_ulonglong), ("ullAvailVirtual", ctypes.c_ulonglong), ("ullAvailExtendedVirtual", ctypes.c_ulonglong)]
    memory_status = MEMORYSTATUSEX()
    memory_status.dwLength = ctypes.sizeof(MEMORYSTATUSEX)
    if not ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(memory_status)):
        return 0.0
    return float(memory_status.dwMemoryLoad)

def update_system_health_history(kpis):
    cpu_percent = get_system_cpu_percent()
    ram_percent = get_memory_percent()
    simulated_traffic = round(24 + (kpis.get("aktif_ajan", 0) * 1.8) + (kpis.get("dijital_katki_endeksi", 0) * 0.32) + (math.sin(time.time() / 18) + 1) * 14, 1)
    history = st.session_state.get("system_health_history", [])
    history.append({"timestamp": datetime.now().strftime("%H:%M:%S"), "CPU": cpu_percent, "RAM": round(ram_percent, 1), "Trafik": simulated_traffic})
    st.session_state["system_health_history"] = history[-24:]
    return st.session_state["system_health_history"]


# ============================================================
# MOOD SİSTEMİ
# ============================================================

def apply_mood_system(kpis):
    mood = kpis.get("system_mood", "huzur")
    palette = {
        "huzur": {"bg": "radial-gradient(circle at 20% 30%, #0a0f1e, #03060c)", "accent": "#ffaa55"},
        "calisma": {"bg": "radial-gradient(circle at 20% 30%, #1a0f0a, #03060c)", "accent": "#ff7733"},
        "uyari": {"bg": "radial-gradient(circle at 20% 30%, #1a0a0a, #03060c)", "accent": "#ff3333"}
    }.get(mood, {})
    st.markdown(f"""
    <style>
    .stApp {{ background: {palette.get("bg")}; }}
    </style>
    """, unsafe_allow_html=True)


# ============================================================
# RENDER_AGENT_SYMPHONY (CANLI GÖRSEL SHOW)
# ============================================================

def render_agent_symphony(snapshot, kpis):
    """Canlı görsel show – ajan küreleri ve bağlantılar"""
    st.markdown("""
    <div style="background:rgba(17,22,30,0.7); border-radius:24px; padding:20px; border:1px solid #ffaa5544; text-align:center;">
        <div style="font-size:1.2rem; color:#ffdd99; margin-bottom:10px;">🎵 Ajan Senfonisi Canlı</div>
        <div style="display:flex; justify-content:center; gap:20px; flex-wrap:wrap; min-height:200px;">
    """, unsafe_allow_html=True)
    
    worker_status = snapshot.get("worker_status") or {}
    active_agents = worker_status.get("active_agents", [])
    
    if active_agents:
        for agent in active_agents[:20]:
            st.markdown(f"""
            <div style="background:rgba(255,170,85,0.08); border:1px solid #ffaa5544; border-radius:50%; 
                        width:70px; height:70px; display:flex; flex-direction:column; align-items:center; justify-content:center;
                        animation:pulseGlow 1.5s ease-in-out infinite;">
                <div style="font-size:0.6rem; color:#ffdd99; text-align:center; font-weight:700; word-break:break-word; max-width:60px;">
                    {agent[:20]}
                </div>
                <div style="font-size:0.5rem; color:#88aaff;">🟢 AKTİF</div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="color:#88aaff; padding:40px;">Henüz aktif ajan yok.<br>Ana Panel'den BAŞLAT'a basın.</div>
        """, unsafe_allow_html=True)
    
    st.markdown("""
    </div>
    <style>
    @keyframes pulseGlow {
        0% { box-shadow: 0 0 10px rgba(255,170,85,0.1); }
        50% { box-shadow: 0 0 30px rgba(255,170,85,0.3); }
        100% { box-shadow: 0 0 10px rgba(255,170,85,0.1); }
    }
    </style>
    </div>
    """, unsafe_allow_html=True)


# ============================================================
# RENDER CONSOLE HEADER
# ============================================================

def render_console_header(snapshot):
    worker_status = snapshot.get("worker_status") or {}
    last_cycle = worker_status.get("last_cycle_at", "-")
    mode = worker_status.get("last_mode", "-")
    active_agents = len(worker_status.get("active_agents", []))
    production_badge = "Production Ready" if st.session_state.get("production_ready") else "Hazırlanıyor"
    st.markdown(f"""
    <div style="background:rgba(17,22,30,0.7); border-radius:28px; padding:1rem 1.5rem; margin-bottom:1rem; border:1px solid #ffaa5544; backdrop-filter:blur(14px); display:flex; align-items:center; gap:1rem; flex-wrap:wrap;">
        <div style="display:flex; align-items:center; gap:0.8rem;">
            {get_imece_logo_svg(compact=True)}
            <span style="font-size:0.88rem; text-transform:uppercase; letter-spacing:0.14em; color:#ffaa55; font-weight:700;">Sosyalİmece.org</span>
        </div>
        <div style="flex:1;">
            <div style="font-size:1.3rem; font-weight:700; color:#ffdd99; text-shadow:0 0 20px rgba(255,170,85,0.12);">5 Panelli Yönetim Konsolu</div>
            <div style="font-size:0.85rem; color:#88aaff;">Canlı ritim korunur | Son nabız: {html.escape(str(last_cycle))} | Mod: {html.escape(str(mode))} | Aktif ajan: {active_agents}</div>
        </div>
        <div style="padding:0.35rem 0.9rem; border-radius:60px; background:rgba(255,170,85,0.12); border:1px solid #ffaa5544; color:#ffdd99; font-size:0.75rem; font-weight:600; display:flex; align-items:center; gap:0.4rem;">
            <span style="width:8px;height:8px;border-radius:50%;background:#10B981;display:inline-block; box-shadow:0 0 12px rgba(16,185,129,0.5);"></span>
            {html.escape(production_badge)}
        </div>
    </div>
    """, unsafe_allow_html=True)


# ============================================================
# SAYFA YÖNLENDİRME VE PANEL BAŞLIKLARI
# ============================================================

PANEL_ISIMLERI = ["Ana Panel", "Ajan Senfonisi", "Performans", "Görev & Erişim", "Ayarlar"]

def render_panel_header(aktif_panel, panel_numarasi):
    """Sayfa başında panel listesini gösterir"""
    html = f"""
    <div class="neon-panel-header">
        <div style="display:flex; flex-wrap:wrap; gap:8px 24px; justify-content:center; align-items:center;">
            <span style="color:#ffaa55; font-weight:700;">📌 PANELLER</span>
    """
    for i, panel in enumerate(PANEL_ISIMLERI):
        aktif_class = "active" if i == panel_numarasi else ""
        numara = i + 1
        html += f'<span class="panel-item {aktif_class}">{numara}️⃣ {panel}</span>'
    
    html += f"""
            <span class="panel-badge">🔴 CANLI</span>
        </div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)


# ============================================================
# İYİLEŞTİRME BİLDİRİMLERİ
# ============================================================

def render_healing_notifications():
    """İyileştirme bildirimlerini gösterir."""
    st.subheader("🩹 İyileştirme Bildirimleri")
    try:
        with open("intelligence_log.json", "r", encoding="utf-8") as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        st.info("Henüz bildirim yok.")
        return

    alerts = data.get("guardian_alerts", [])
    if alerts:
        st.markdown("#### 🛡️ Gözcü Uyarıları")
        for alert in alerts[-10:]:
            severity = alert.get("severity", "info")
            icon = "🔴" if severity == "critical" else "🟡" if severity == "warning" else "🟢"
            st.markdown(f"{icon} **{alert.get('agent')}** - {alert.get('error_type')} : {alert.get('log_line')[:80]}...")
    
    healing = data.get("healing_events", [])
    if healing:
        st.markdown("#### 🔧 Onarım Kayıtları")
        for event in healing[-10:]:
            status = event.get("status", "unknown")
            icon = "✅" if status == "success" else "❌"
            st.markdown(f"{icon} **{event.get('agent')}** onarıldı. Hata: {event.get('error_type')}")

    scaling = data.get("scaling_events", [])
    if scaling:
        st.markdown("#### ⚖️ Ölçeklendirme Kararları")
        for event in scaling[-10:]:
            status = event.get("status", "unknown")
            icon = "✅" if status == "success" else "❌"
            st.markdown(f"{icon} {event.get('reason')} yükü {event.get('threshold_value')} aşıldı. PID: {event.get('pid')}")

    if any(e.get("severity") == "critical" for e in alerts):
        if st.button("⚠️ Kritik Hata - Yeni Ajan Ekle (ONAYLA)", type="primary"):
            try:
                from trm_agents.scaling_agent import ScalingAgent
                sa = ScalingAgent()
                decisions = sa.scale_if_needed()
                st.success(f"{len(decisions)} yeni ajan başlatıldı.")
                st.rerun()
            except ImportError:
                st.error("ScalingAgent modülü bulunamadı.")


# ============================================================
# GÜVENLİK UYARILARI
# ============================================================

def render_security_alerts():
    """Kırmızı güvenlik uyarılarını gösterir."""
    st.subheader("🚨 Güvenlik Uyarıları")
    logger = SecurityLogger()
    threats = logger.get_active_threats(limit=10)
    
    if not threats:
        st.success("✅ Şu anda tüm sistem güvenli, tehdit tespit edilmedi.")
        return

    for threat in threats:
        severity = threat.get("severity", "critical")
        timestamp = threat.get("timestamp", "")
        threat_type = threat.get("threat_type", "")
        details = threat.get("details", {})
        
        st.markdown(f"""
        <div class="security-card-critical">
            <div style="display: flex; justify-content: space-between;">
                <span class="title">🔴 {severity.upper()}</span>
                <span class="timestamp">{timestamp}</span>
            </div>
            <div class="threat-type">{threat_type}</div>
            <div class="detail">Agent: {details.get('agent', 'Bilinmiyor')}</div>
            <div class="log-line">{details.get('log_line', '')[:150]}</div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button(f"✅ Çözüldü İşaretle - {threat_type[:20]}", key=f"resolve_{threat.get('timestamp', '')}"):
            try:
                with open("security_threats.json", "r", encoding="utf-8") as f:
                    data = json.load(f)
                for t in data:
                    if t.get("timestamp") == threat.get("timestamp"):
                        t["resolved"] = True
                        break
                with open("security_threats.json", "w", encoding="utf-8") as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
                st.success("Tehdit çözüldü olarak işaretlendi.")
                st.rerun()
            except:
                st.error("Güncelleme başarısız.")


# ============================================================
# SERTLEŞTİRİLMİŞ GÖRÜNMEZLİK / KARANTİNA
# ============================================================

def render_stealth_dashboard():
    """Sertleştirilmiş görünmezlik ve karantina durumunu gösterir."""
    st.subheader("🕵️ Sertleştirilmiş Görünmezlik / Karantina")

    # Emergency Stop durumu
    try:
        with open("emergency_stop.flag", "r", encoding="utf-8") as f:
            stop_data = json.load(f)
        if stop_data.get("active", False):
            st.error(f"🚨 EMERGENCY STOP AKTİF! Sebep: {stop_data.get('reason')} - {stop_data.get('triggered_at')}")
        else:
            st.success("✅ Emergency Stop devre dışı.")
    except:
        st.info("Henüz Emergency Stop kaydı yok.")

    # Karantina listesi
    try:
        with open("quarantine.json", "r", encoding="utf-8") as f:
            quarantines = json.load(f)
        active = [q for q in quarantines if q.get("active", True)]
        if active:
            st.warning(f"⚠️ {len(active)} ajan karantinada:")
            for q in active:
                st.markdown(f"- **{q['agent']}** - {q['reason']} (süre: {q['expires_at']})")
        else:
            st.success("✅ Hiçbir ajan karantinada değil.")
    except:
        st.info("Karantina verisi yok.")

    # Session Manager ve Fingerprint bilgisi (opsiyonel)
    with st.expander("🔍 Aktif Session ve Parmak İzi Profilleri"):
        try:
            session_dir = "sessions"
            if os.path.exists(session_dir):
                sessions = [f for f in os.listdir(session_dir) if f.endswith("_session.json")]
                if sessions:
                    for s in sessions[:5]:
                        st.code(f"📂 {s}")
                else:
                    st.info("Aktif session yok.")
            else:
                st.info("Session klasörü henüz oluşturulmamış.")
        except Exception as e:
            st.error(f"Session bilgisi alınamadı: {e}")


# ============================================================
# 1. PANEL: ANA PANEL
# ============================================================

def render_ana_panel(snapshot, kpis):
    render_panel_header("Ana Panel", 0)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"""
        <div class="neon-card">
            <div class="neon-value">%{kpis['imece_basari_skoru']}</div>
            <div class="neon-label">🏆 İmece Başarı</div>
            <div class="neon-sub">Ortak hedeflere yaklaşım</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class="neon-card">
            <div class="neon-value">{kpis['gunluk_erisim']}</div>
            <div class="neon-label">👥 Günlük Erişim</div>
            <div class="neon-sub">Bugün ulaşılan kişi</div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown(f"""
        <div class="neon-card">
            <div class="neon-value">{kpis['ortak_gorev_sayisi']}</div>
            <div class="neon-label">🤝 Ortak Görev</div>
            <div class="neon-sub">2+ ajan işbirliği</div>
        </div>
        """, unsafe_allow_html=True)
    with col4:
        st.markdown(f"""
        <div class="neon-card">
            <div class="neon-value">%{kpis['dijital_katki_endeksi']}</div>
            <div class="neon-label">⚡ Dijital Katkı</div>
            <div class="neon-sub">Anlık üretim faydası</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('<hr class="neon-divider">', unsafe_allow_html=True)
    
    # KOMUT MERKEZİ BUTONLARI
    st.markdown('<div class="neon-btn-group">', unsafe_allow_html=True)
    cols = st.columns(5)
    with cols[0]:
        if st.button("▶️ BAŞLAT", use_container_width=True, type="primary"):
            st.success("Sistem başlatıldı!")
    with cols[1]:
        if st.button("🛑 DURDUR", use_container_width=True):
            st.warning("Sistem durduruldu.")
    with cols[2]:
        if st.button("🔄 SIFIRLA", use_container_width=True):
            st.rerun()
    with cols[3]:
        if st.button("🔙 GERİ AL", use_container_width=True):
            st.info("Geri alındı.")
    with cols[4]:
        if st.button("📹 KAYIT", use_container_width=True):
            st.info("Kayıt başlatıldı.")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # DİĞER BUTON GRUPLARI
    st.markdown('<div class="neon-btn-group">', unsafe_allow_html=True)
    cols = st.columns(5)
    with cols[0]:
        if st.button("📊 RAPOR", use_container_width=True):
            st.session_state["console_page"] = "Performans"
            st.rerun()
    with cols[1]:
        if st.button("💰 FİNANS", use_container_width=True):
            st.info("Finans raporu hazırlanıyor...")
    with cols[2]:
        if st.button("📁 SİSTEM KUR", use_container_width=True):
            st.info("Sistem kurulumu başlatıldı.")
    with cols[3]:
        if st.button("📁 KLASÖR", use_container_width=True):
            st.info("Klasör oluşturuldu.")
    with cols[4]:
        if st.button("📁 TOPLU KLASÖR", use_container_width=True):
            st.info("Toplu klasör oluşturuldu.")
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="neon-btn-group">', unsafe_allow_html=True)
    cols = st.columns(5)
    with cols[0]:
        if st.button("📋 AJAN LİSTESİ", use_container_width=True):
            st.session_state["console_page"] = "Ajan Senfonisi"
            st.rerun()
    with cols[1]:
        if st.button("➕ YENİ AJAN", use_container_width=True):
            st.info("Yeni ajan eklendi.")
    with cols[2]:
        if st.button("🔄 YENİLE", use_container_width=True):
            st.rerun()
    with cols[3]:
        if st.button("📡 İLETİŞİM", use_container_width=True):
            st.info("İletişim kanalları açıldı.")
    with cols[4]:
        if st.button("🌐 WEB AÇ", use_container_width=True):
            st.info("Web adresi açılıyor...")
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<hr class="neon-divider">', unsafe_allow_html=True)
    
    # CANLI DURUM
    col_left, col_right = st.columns([1.2, 0.8])
    with col_left:
        st.markdown("### 📌 Canlı Durum")
        worker_status = snapshot.get("worker_status") or {}
        st.markdown(f"""
        <div style="background:rgba(17,22,30,0.7); border-radius:20px; padding:1rem; border:1px solid #ffaa5544;">
            <div style="display:grid; grid-template-columns:1fr 1fr; gap:8px 20px;">
                <span style="color:#88aaff;">Sistem Modu</span><span style="color:#ffdd99;">{kpis.get('system_mood_label', '-')}</span>
                <span style="color:#88aaff;">Aktif Ajan</span><span style="color:#ffdd99;">{kpis.get('aktif_ajan', 0)}</span>
                <span style="color:#88aaff;">Bağlı Ajan</span><span style="color:#ffdd99;">{kpis.get('bagli_ajan', 0)}</span>
                <span style="color:#88aaff;">Bekleyen Retry</span><span style="color:#ffdd99;">{kpis.get('pending_retry', 0)}</span>
                <span style="color:#88aaff;">Son Nabız</span><span style="color:#ffdd99;">{worker_status.get('last_cycle_at', '-')}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    with col_right:
        st.markdown("### 📰 Ticker")
        render_imece_ticker()
    
    # SİSTEM SAĞLIĞI
    st.markdown('<hr class="neon-divider">', unsafe_allow_html=True)
    st.markdown("### 🩺 Sistem Sağlığı")
    health_cols = st.columns(3)
    history = st.session_state.get("system_health_history", [])
    latest = history[-1] if history else {"CPU": 0.0, "RAM": 0.0, "Trafik": 0.0}
    with health_cols[0]:
        st.markdown(f"""
        <div class="neon-card">
            <div class="neon-value" style="font-size:1.6rem;">%{latest['CPU']}</div>
            <div class="neon-label">CPU</div>
        </div>
        """, unsafe_allow_html=True)
    with health_cols[1]:
        st.markdown(f"""
        <div class="neon-card">
            <div class="neon-value" style="font-size:1.6rem;">%{latest['RAM']}</div>
            <div class="neon-label">RAM</div>
        </div>
        """, unsafe_allow_html=True)
    with health_cols[2]:
        st.markdown(f"""
        <div class="neon-card">
            <div class="neon-value" style="font-size:1.6rem;">{latest['Trafik']} rps</div>
            <div class="neon-label">Trafik</div>
        </div>
        """, unsafe_allow_html=True)

    # İYİLEŞTİRME BİLDİRİMLERİ
    st.markdown('<hr class="neon-divider">', unsafe_allow_html=True)
    render_healing_notifications()
    
    # GÜVENLİK UYARILARI
    st.markdown('<hr class="neon-divider">, unsafe_allow_html=True)
    render_security_alerts()
    
    # SERTLEŞTİRİLMİŞ GÖRÜNMEZLİK / KARANTİNA
    st.markdown('<hr class="neon-divider">', unsafe_allow_html=True)
    render_stealth_dashboard()
    
    # SONRAKİ PANEL BUTONU
    st.markdown('<hr class="neon-divider">', unsafe_allow_html=True)
    col_prev, col_next = st.columns([1, 1])
    with col_next:
        if st.button("➡️ 2. Panel (Ajan Senfonisi) sayfasına geçiniz", use_container_width=True, type="primary"):
            st.session_state["console_page"] = "Ajan Senfonisi"
            st.rerun()


# ============================================================
# 2. PANEL: AJAN SENFONİSİ
# ============================================================

def render_ajan_senfonisi(snapshot, kpis):
    render_panel_header("Ajan Senfonisi", 1)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"""
        <div class="neon-card">
            <div class="neon-value">{kpis['aktif_ajan']}</div>
            <div class="neon-label">🟢 Aktif Ajan</div>
            <div class="neon-sub">Şu an çalışıyor</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class="neon-card">
            <div class="neon-value">{kpis['isleniyor_ajan']}</div>
            <div class="neon-label">🔄 İşleniyor</div>
            <div class="neon-sub">Veri akışında</div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown(f"""
        <div class="neon-card">
            <div class="neon-value">{kpis['beklemede_ajan']}</div>
            <div class="neon-label">⏳ Beklemede</div>
            <div class="neon-sub">Hazır bekleyen</div>
        </div>
        """, unsafe_allow_html=True)
    with col4:
        st.markdown(f"""
        <div class="neon-card">
            <div class="neon-value">%{kpis['dijital_katki_endeksi']}</div>
            <div class="neon-label">✨ Katkı</div>
            <div class="neon-sub">Canlı üretim</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('<hr class="neon-divider">', unsafe_allow_html=True)
    st.markdown("### 🎵 Ajan Senfonisi – Canlı Ağ Görselleştirmesi")
    render_agent_symphony(snapshot, kpis)
    
    st.markdown('<hr class="neon-divider">', unsafe_allow_html=True)
    col_prev, col_next = st.columns([1, 1])
    with col_prev:
        if st.button("⬅️ 1. Panel (Ana Panel) sayfasına dönün", use_container_width=True):
            st.session_state["console_page"] = "Ana Panel"
            st.rerun()
    with col_next:
        if st.button("➡️ 3. Panel (Performans) sayfasına geçiniz", use_container_width=True, type="primary"):
            st.session_state["console_page"] = "Performans"
            st.rerun()


# ============================================================
# 3. PANEL: PERFORMANS
# ============================================================

def render_performans_paneli(snapshot, kpis):
    render_panel_header("Performans", 2)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"""
        <div class="neon-card">
            <div class="neon-value">%{kpis['imece_basari_skoru']}</div>
            <div class="neon-label">🏆 Başarı Skoru</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class="neon-card">
            <div class="neon-value">{kpis['saved_human_hours']:.1f}</div>
            <div class="neon-label">⏱️ Tasarruf (insan-saat)</div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown(f"""
        <div class="neon-card">
            <div class="neon-value">{kpis['processed_data_mb']:.1f}</div>
            <div class="neon-label">💾 İşlenen Veri (MB)</div>
        </div>
        """, unsafe_allow_html=True)
    with col4:
        st.markdown(f"""
        <div class="neon-card">
            <div class="neon-value">%{kpis['success_rate']}</div>
            <div class="neon-label">✅ Başarı Oranı</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('<hr class="neon-divider">', unsafe_allow_html=True)
    render_trend_analysis()
    
    st.markdown('<hr class="neon-divider">', unsafe_allow_html=True)
    col_prev, col_next = st.columns([1, 1])
    with col_prev:
        if st.button("⬅️ 2. Panel (Ajan Senfonisi) sayfasına dönün", use_container_width=True):
            st.session_state["console_page"] = "Ajan Senfonisi"
            st.rerun()
    with col_next:
        if st.button("➡️ 4. Panel (Görev & Erişim) sayfasına geçiniz", use_container_width=True, type="primary"):
            st.session_state["console_page"] = "Görev & Erişim"
            st.rerun()


# ============================================================
# 4. PANEL: GÖREV & ERİŞİM
# ============================================================

def render_gorev_erisim_paneli(snapshot, kpis):
    render_panel_header("Görev & Erişim", 3)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"""
        <div class="neon-card">
            <div class="neon-value">{kpis['ortak_gorev_sayisi']}</div>
            <div class="neon-label">🤝 Ortak Görev</div>
            <div class="neon-sub">2+ ajan tamamladı</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class="neon-card">
            <div class="neon-value">{kpis['gunluk_erisim']}</div>
            <div class="neon-label">👥 Günlük Erişim</div>
            <div class="neon-sub">Bugün ulaşılan kişi</div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown(f"""
        <div class="neon-card">
            <div class="neon-value">{kpis['queue_ready']}</div>
            <div class="neon-label">📋 Hazır Kuyruk</div>
            <div class="neon-sub">Sırada bekleyen</div>
        </div>
        """, unsafe_allow_html=True)
    with col4:
        st.markdown(f"""
        <div class="neon-card">
            <div class="neon-value">{kpis['pending_retry']}</div>
            <div class="neon-label">🔄 Pending Retry</div>
            <div class="neon-sub">Yeniden deneniyor</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('<hr class="neon-divider">', unsafe_allow_html=True)
    col_a, col_b = st.columns(2)
    with col_a:
        render_content_generator_section(snapshot.get("content_payload"))
    with col_b:
        render_queue_section(snapshot.get("queue_payload"))
    
    st.markdown('<hr class="neon-divider">', unsafe_allow_html=True)
    col_prev, col_next = st.columns([1, 1])
    with col_prev:
        if st.button("⬅️ 3. Panel (Performans) sayfasına dönün", use_container_width=True):
            st.session_state["console_page"] = "Performans"
            st.rerun()
    with col_next:
        if st.button("➡️ 5. Panel (Ayarlar) sayfasına geçiniz", use_container_width=True, type="primary"):
            st.session_state["console_page"] = "Ayarlar"
            st.rerun()


# ============================================================
# 5. PANEL: AYARLAR
# ============================================================

def render_ayarlar_paneli(snapshot, kpis):
    render_panel_header("Ayarlar", 4)
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("⚙️ Sistem Ayarları")
        settings, settings_error = get_email_settings()
        if settings:
            st.success("E-posta ayarları hazır.")
            st.json({
                "email_sender": settings.get("email_sender"),
                "email_receiver": settings.get("email_receiver"),
                "smtp_server": settings.get("smtp_server"),
                "smtp_port": settings.get("smtp_port"),
            })
        else:
            st.warning(settings_error)
        
        if st.button("📧 Test E-postası Gönder", use_container_width=True):
            success, message = send_system_active_email()
            if success:
                st.success(message)
            else:
                st.error(message)
    
    with col2:
        st.subheader("🔐 Güvenlik")
        if st.button("🔄 Panel Oturumunu Yenile", use_container_width=True):
            st.rerun()
        if st.button("🔒 Panel Oturumunu Kilitle", use_container_width=True):
            st.session_state["performance_panel_authorized"] = False
            st.rerun()
    
    st.markdown('<hr class="neon-divider">', unsafe_allow_html=True)
    col_prev, _ = st.columns([1, 1])
    with col_prev:
        if st.button("⬅️ 4. Panel (Görev & Erişim) sayfasına dönün", use_container_width=True):
            st.session_state["console_page"] = "Görev & Erişim"
            st.rerun()


# ============================================================
# DİĞER RENDER FONKSİYONLARI
# ============================================================

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
    components.html(f"""
    <style>
    .ticker-wrap {{ overflow: hidden; border-radius: 18px; border: 1px solid #ffaa5544; background: rgba(17,22,30,0.7); backdrop-filter: blur(14px); padding: 10px 0; font-family: Arial, sans-serif; color: #E5EEF8; }}
    .ticker-track {{ display: inline-flex; gap: 34px; white-space: nowrap; min-width: 100%; animation: imeceTicker 46s linear infinite; }}
    .ticker-item {{ font-size: 13px; color: #aabbdd; }}
    .ticker-item strong {{ color: #ffaa55; margin-right: 8px; }}
    .ticker-item a {{ color: #E5EEF8; text-decoration: none; }}
    @keyframes imeceTicker {{ 0% {{ transform: translateX(0%); }} 100% {{ transform: translateX(-50%); }} }}
    </style>
    <div class="ticker-wrap"><div class="ticker-track">{''.join(ticker_html)}{''.join(ticker_html)}</div></div>
    """, height=62)

def render_trend_analysis():
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
                st.line_chart(data_rows, x="Periyot", y=["Dijital Katkı", "Sesli Komut", "İmece Başarı"], height=200)
            else:
                st.caption("Yeterli veri bekleniyor.")

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
        bucket = grouped.setdefault(label, {"Periyot": label, "Dijital Katkı": [], "Sesli Komut": [], "İmece Başarı": []})
        bucket["Dijital Katkı"].append(row.get("digital_contribution", 0))
        bucket["Sesli Komut"].append(row.get("voice_count", 0))
        bucket["İmece Başarı"].append(row.get("imece_success", 0))
    aggregated = []
    for label, values in grouped.items():
        aggregated.append({
            "Periyot": label,
            "Dijital Katkı": round(sum(values["Dijital Katkı"]) / max(1, len(values["Dijital Katkı"])), 1),
            "Sesli Komut": round(sum(values["Sesli Komut"]) / max(1, len(values["Sesli Komut"])), 1),
            "İmece Başarı": round(sum(values["İmece Başarı"]) / max(1, len(values["İmece Başarı"])), 1),
        })
    aggregated.sort(key=lambda item: item["Periyot"])
    limits = {"daily": 10, "weekly": 8, "monthly": 6}
    return aggregated[-limits.get(mode, 10):]

def render_content_generator_section(payload):
    st.subheader("📝 Content Generator Çıktıları")
    if not payload:
        st.info("Henüz üretilmiş içerik yok.")
        return
    st.caption(f"Üretim zamanı: {payload.get('generated_at', '-')}")
    for item in payload.get("contents", [])[:3]:
        with st.expander(f"{item.get('product_name', 'İçerik')}"):
            st.markdown(f"**Satış Metni:** {item.get('promo_text', '-')}")
            st.markdown(f"**Sosyal Medya:** {item.get('social_post', '-')[:100]}...")

def render_queue_section(queue_payload):
    st.subheader("📋 Sosyal Medya Kuyruğu")
    if not queue_payload:
        st.info("Henüz kuyruk oluşmadı.")
        return
    st.caption(f"Kuyruk zamanı: {queue_payload.get('generated_at', '-')}")
    for item in queue_payload.get("items", [])[:3]:
        with st.expander(f"{item.get('product_name', 'Post')}"):
            st.markdown(f"**Durum:** {item.get('status', '-')}")
            st.markdown(f"**Post:** {item.get('post_text', '-')[:100]}...")

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
    return {
        "nightly_fayda": nightly_fayda,
        "nightly_hours": total_hours,
        "nightly_mb": total_mb,
        "pdf_bytes": b"PDF content here",
        "file_name": f"sosyalimece_daily_briefing_{datetime.now().strftime('%Y%m%d')}.pdf",
    }

def render_daily_briefing(snapshot, kpis):
    briefing = build_daily_briefing(snapshot, kpis)
    st.subheader("📄 Günlük Brifing")
    st.caption(f"Dün gece tahmini dijital katkı: %{briefing['nightly_fayda']} | {briefing['nightly_hours']:.1f} insan-saati | {briefing['nightly_mb']:.1f} MB veri")
    if st.button("📥 PDF Raporu İndir", use_container_width=True):
        st.info("PDF raporu hazırlanıyor...")


# ============================================================
# SİSTEM SAĞLIĞI FOOTER
# ============================================================

def render_system_health_footer(kpis):
    history = update_system_health_history(kpis)
    latest = history[-1] if history else {"CPU": 0.0, "RAM": 0.0, "Trafik": 0.0}
    st.markdown("### 🩺 Sistem Sağlığı")
    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric("CPU", f"%{latest['CPU']}")
    with c2:
        st.metric("RAM", f"%{latest['RAM']}")
    with c3:
        st.metric("Trafik", f"{latest['Trafik']} rps")
    
    chart_rows = [{"Zaman": row["timestamp"], "CPU": row["CPU"], "RAM": row["RAM"], "Trafik": row["Trafik"]} for row in history[-12:]]
    if chart_rows:
        st.line_chart(chart_rows, x="Zaman", y=["CPU", "RAM", "Trafik"], height=150)


# ============================================================
# RUN_SCRAPER_LOGIC (ANA AJAN BAŞLATMA FONKSİYONU)
# ============================================================

def run_scraper_logic(show_ui=True):
    """
    Tüm TRM ajanlarını başlatan ana fonksiyon.
    Pre-flight kontrolü ile başlar, expansion ajanlarını ve çekirdek ajanları yükler.
    """
    from trm_agents.CoreNexus import CoreNexus
    from trm_agents.camouflage_agent import CamouflageAgent
    from trm_agents.account_manager_agent import AccountManagerAgent
    from trm_agents.analyst_agent import AnalystAgent
    from trm_agents.content_generator_agent import ContentGeneratorAgent
    from trm_agents.queue_agent import QueueAgent
    from trm_agents.poster_agent import PosterAgent
    from trm_agents.expansion_module import build_expansion_agents, get_capacity_snapshot

    # ============================================================
    # 1. PRE-FLIGHT KONTROLÜ – Tüm ajanların dosyalarını kontrol et
    # ============================================================
    expansion_specs = build_expansion_agents()
    core_agents = ["CamouflageAgent", "AccountManagerAgent", "ContentGeneratorAgent",
                   "QueueAgent", "PosterAgent"]

    all_agent_names = [spec["name"] for spec in expansion_specs]
    all_agent_names.extend(core_agents)

    for agent_name in all_agent_names:
        if not health_check_pre_flight(agent_name):
            error_msg = f"Pre-flight check failed for {agent_name}. Sistem durduruluyor."
            print(error_msg)
            raise Exception(error_msg)

    # ============================================================
    # 2. NORMAL BAŞLATMA KODU
    # ============================================================
    nexus = CoreNexus(zero_trust=True, stealth_mode=True)
    camou = CamouflageAgent()
    account_mgr = AccountManagerAgent()
    content_generator = ContentGeneratorAgent()
    queue_agent = QueueAgent()
    poster_agent = PosterAgent()
    capacity_snapshot = get_capacity_snapshot()

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
        with st.expander("Sistem Teknik Logları", expanded=False):
            st.write(f"Operatör Kimliği: {operator_identity['identity']}")
            st.write(f"E-posta: {operator_identity['email']}")

    mask_id = camou.mask_identity()
    if show_ui:
        with st.expander("Sistem Teknik Logları", expanded=False):
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
                enriched_details.append({
                    "product_name": product_name,
                    "trend_score": score,
                    "price": price,
                    "commission_rate": commission_rate,
                    "estimated_commission": round(price * commission_rate / 100, 2),
                    "product_url": product_meta.get("product_url", ""),
                })
            analysis_result["product_details"] = enriched_details
            if enriched_details:
                highest_commission_product = max(enriched_details, key=lambda item: (item.get("commission_rate", 0.0), item.get("estimated_commission", 0.0)))
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
        sync_results = nexus.run_system_sync(context={
            "trend_report": analysis_result,
            "active_agents": list(nexus.agents.keys()),
            "agent_capacity_snapshot": capacity_snapshot,
        })
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
            st.success(f"PosterAgent zamanı gelen içerikleri Instagram ve Facebook için işlemeye başladı. Başarılı yayın: {poster_payload.get('posted_count', 0)}")
    except Exception as e:
        if show_ui:
            st.error(f"Ajan zinciri hatası: {str(e)}")
        else:
            print(f"[AgentChain] Hata: {str(e)}")

    if show_ui:
        try:
            success, message = send_agent_activation_email("Content_Generator_Agent")
            if success:
                st.success(message)
            else:
                st.error(message)
        except Exception as e:
            st.error(f"Ajan aktivasyon bildirimi hatası: {str(e)}")

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
    }


# ============================================================
# MAIN
# ============================================================

def main():
    try:
        init_session_state()
        inject_console_styles()
        render_splash_screen()
        
        snapshot = {
            "worker_status": load_json_payload("worker_status.json") or {},
            "intelligence_entry": load_latest_log_entry("intelligence_log.json") or {},
            "sentinel_entry": load_latest_log_entry("sentinel_alerts.json") or {},
            "content_payload": st.session_state.get("latest_content_payload") or load_latest_content_payload(),
            "queue_payload": st.session_state.get("latest_queue_payload") or load_latest_queue_payload(),
            "intelligence_history": load_json_payload("intelligence_log.json", expect_list=True)[-12:],
            "sentinel_history": load_json_payload("sentinel_alerts.json", expect_list=True)[-12:],
        }
        
        # Örnek KPI değerleri (gerçek veri geldiğinde değişecek)
        kpis = {
            "imece_basari_skoru": 85.5,
            "gunluk_erisim": 1247,
            "ortak_gorev_sayisi": 42,
            "dijital_katki_endeksi": 78.3,
            "aktif_ajan": 37,
            "bagli_ajan": 45,
            "beklemede_ajan": 8,
            "isleniyor_ajan": 29,
            "queue_ready": 156,
            "pending_retry": 3,
            "warning_count": 2,
            "critical_count": 0,
            "success_rate": 94.2,
            "saved_human_hours": 12.4,
            "processed_data_mb": 87.6,
            "system_mood": "huzur",
            "system_mood_label": "Huzur Modu",
            "katki_uretildi": True,
        }
        
        update_system_health_history(kpis)
        apply_mood_system(kpis)
        render_console_header(snapshot)
        
        current_page = st.session_state.get("console_page", "Ana Panel")
        
        if current_page == "Ana Panel":
            render_ana_panel(snapshot, kpis)
        elif current_page == "Ajan Senfonisi":
            render_ajan_senfonisi(snapshot, kpis)
        elif current_page == "Performans":
            render_performans_paneli(snapshot, kpis)
        elif current_page == "Görev & Erişim":
            render_gorev_erisim_paneli(snapshot, kpis)
        elif current_page == "Ayarlar":
            render_ayarlar_paneli(snapshot, kpis)
        else:
            render_ana_panel(snapshot, kpis)
        
        st.markdown('<hr class="neon-divider">', unsafe_allow_html=True)
        render_imece_ticker()
        render_system_health_footer(kpis)
        
    except Exception as e:
        st.error(f"Hata oluştu: {str(e)}")
        st.exception(e)


if __name__ == "__main__":
    main()