#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TRM Nirvana v3.0 - Gelişmiş Yönetim Paneli (Streamlit Versiyonu)
Headless modda port 8501'de çalışır
"""

import asyncio
import json
import sys
import threading
import os
import subprocess
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import sqlite3
import matplotlib.pyplot as plt
import base64
from io import BytesIO

# Sistem modülleri (opsiyonel import)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(BASE_DIR, "Uluslararasi-TRM-Full-Otomasyon-Sistemi"))

try:
    from SYSTEM_MANAGER_24_7 import SystemManager24_7
    from DRIVE_SOCIAL_MANAGER import DriveSocialManager
    from SATIS_ALARM_SISTEMI import SalesAlarmSystem
    MODULES_AVAILABLE = True
except ImportError as e:
    print(f"⚠️ Sistem modülleri yüklenemedi: {e}")
    print("📊 Dashboard temel modda çalışacak...")
    SystemManager24_7 = None
    DriveSocialManager = None
    SalesAlarmSystem = None
    MODULES_AVAILABLE = False

class AdvancedDashboardManager:
    def __init__(self):
        self.system_manager = SystemManager24_7() if SystemManager24_7 else None
        self.drive_social = DriveSocialManager() if DriveSocialManager else None
        self.sales_alarm = SalesAlarmSystem() if SalesAlarmSystem else None
        self.db_path = os.path.join(BASE_DIR, "trm_dashboard.db")
        self.init_database()
    
    def init_database(self):
        """Veritabanını başlat"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS system_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    level TEXT,
                    module TEXT,
                    message TEXT
                )
            ''')
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS social_posts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    platform TEXT,
                    status TEXT,
                    likes INTEGER,
                    shares INTEGER,
                    comments INTEGER
                )
            ''')
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS ai_performance (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    agent_name TEXT,
                    task_type TEXT,
                    success_rate REAL,
                    execution_time REAL
                )
            ''')
            
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"Veritabanı başlatma hatası: {e}")
    
    def get_system_status(self):
        """Sistem durumunu al"""
        try:
            status = {
                'system_manager': self.system_manager.get_status() if hasattr(self.system_manager, 'get_status') else {'status': 'active'},
                'drive_social': self.drive_social.get_status() if hasattr(self.drive_social, 'get_status') else {'status': 'active'},
                'sales_alarm': self.sales_alarm.get_status() if hasattr(self.sales_alarm, 'get_status') else {'status': 'active'},
                'timestamp': datetime.now().isoformat()
            }
            return status
        except Exception as e:
            return {'error': str(e), 'timestamp': datetime.now().isoformat()}
    
    def get_daily_stats(self):
        """Günlük istatistikleri al"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            today = datetime.now().strftime('%Y-%m-%d')
            
            cursor.execute('SELECT COUNT(*) FROM system_logs WHERE DATE(timestamp) = ?', (today,))
            log_count = cursor.fetchone()[0]
            
            cursor.execute('SELECT COUNT(*) FROM social_posts WHERE DATE(timestamp) = ?', (today,))
            post_count = cursor.fetchone()[0]
            
            cursor.execute('SELECT AVG(success_rate) FROM ai_performance WHERE DATE(timestamp) = ?', (today,))
            avg_success = cursor.fetchone()[0] or 0
            
            conn.close()
            
            return {
                'date': today,
                'log_count': log_count,
                'post_count': post_count,
                'avg_success_rate': round(avg_success, 2),
                'timestamp': datetime.now().isoformat()
            }
        except Exception as e:
            return {'error': str(e), 'timestamp': datetime.now().isoformat()}
    
    def get_error_logs(self):
        """Hata loglarını al"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT timestamp, level, module, message 
                FROM system_logs 
                WHERE level = 'ERROR' 
                ORDER BY timestamp DESC 
                LIMIT 50
            ''')
            
            logs = []
            for row in cursor.fetchall():
                logs.append({
                    'timestamp': row[0],
                    'level': row[1],
                    'module': row[2],
                    'message': row[3]
                })
            
            conn.close()
            return logs
        except Exception as e:
            return [{'error': str(e)}]
    
    def get_social_posts(self):
        """Sosyal medya gönderilerini al"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT timestamp, platform, status, likes, shares, comments 
                FROM social_posts 
                ORDER BY timestamp DESC 
                LIMIT 20
            ''')
            
            posts = []
            for row in cursor.fetchall():
                posts.append({
                    'timestamp': row[0],
                    'platform': row[1],
                    'status': row[2],
                    'likes': row[3],
                    'shares': row[4],
                    'comments': row[5]
                })
            
            conn.close()
            return posts
        except Exception as e:
            return [{'error': str(e)}]
    
    def get_ai_performance(self):
        """AI performansını al"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT timestamp, agent_name, task_type, success_rate, execution_time 
                FROM ai_performance 
                ORDER BY timestamp DESC 
                LIMIT 30
            ''')
            
            performance = []
            for row in cursor.fetchall():
                performance.append({
                    'timestamp': row[0],
                    'agent_name': row[1],
                    'task_type': row[2],
                    'success_rate': row[3],
                    'execution_time': row[4]
                })
            
            conn.close()
            return performance
        except Exception as e:
            return [{'error': str(e)}]

def start_orchestrator_background():
    """ORCHESTRATOR_AGENT'ı arka planda başlat"""
    try:
        import importlib.util
        spec = importlib.util.spec_from_file_location("orchestrator", os.path.join(BASE_DIR, "ORCHESTRATOR_AGENT.py"))
        orchestrator_module = importlib.util.module_from_spec(spec)
        
        def run_orchestrator():
            try:
                spec.loader.exec_module(orchestrator_module)
                if hasattr(orchestrator_module, 'orchestrator'):
                    orchestrator = orchestrator_module.orchestrator
                    if hasattr(orchestrator, 'run_system'):
                        orchestrator.run_system()
            except Exception as e:
                print(f"Orchestrator arka plan hatası: {e}")
        
        orchestrator_thread = threading.Thread(target=run_orchestrator, daemon=True)
        orchestrator_thread.start()
        print("✅ ORCHESTRATOR_AGENT arka planda başlatıldı")
        return True
    except Exception as e:
        print(f"❌ ORCHESTRATOR_AGENT başlatılamadı: {e}")
        return False

def start_streamlit_headless():
    """Streamlit'i headless modda başlat"""
    try:
        # Streamlit config oluştur
        config = """
[server]
port = 8501
headless = true
enableCORS = false
enableXsrfProtection = true

[client]
showErrorDetails = true

[logger]
level = info
"""
        config_path = os.path.join(BASE_DIR, ".streamlit", "config.toml")
        os.makedirs(os.path.dirname(config_path), exist_ok=True)
        with open(config_path, "w", encoding="utf-8") as f:
            f.write(config)
        
        # Streamlit app oluştur
        app_code = '''
import streamlit as st
import sys
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(BASE_DIR, "Uluslararasi-TRM-Full-Otomasyon-Sistemi"))

from ADVANCED_DASHBOARD_STREAMLIT import AdvancedDashboardManager

st.set_page_config(
    page_title="TRM Nirvana v3.0",
    page_icon="🌐",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("🌐 TRM NIRVANA v3.0 - Gelişmiş Yönetim Paneli")
st.markdown("---")

manager = AdvancedDashboardManager()

# Sidebar
st.sidebar.title("📊 Paneller")
page = st.sidebar.radio(
    "Sayfa Seçin",
    ["Sistem Durumu", "Günlük İstatistikler", "Hata Logları", "Sosyal Medya", "AI Performans"]
)

if page == "Sistem Durumu":
    st.header("🔧 Sistem Durumu")
    status = manager.get_system_status()
    st.json(status)
    
elif page == "Günlük İstatistikler":
    st.header("📈 Günlük İstatistikler")
    stats = manager.get_daily_stats()
    st.json(stats)
    
elif page == "Hata Logları":
    st.header("❌ Hata Logları")
    logs = manager.get_error_logs()
    for log in logs:
        st.json(log)
        st.markdown("---")
        
elif page == "Sosyal Medya":
    st.header("📱 Sosyal Medya Gönderileri")
    posts = manager.get_social_posts()
    for post in posts:
        st.json(post)
        st.markdown("---")
        
elif page == "AI Performans":
    st.header("🤖 AI Performans")
    performance = manager.get_ai_performance()
    for perf in performance:
        st.json(perf)
        st.markdown("---")

st.sidebar.markdown("---")
st.sidebar.info(f"🕐 Son güncelleme: {datetime.now().strftime('%H:%M:%S')}")
'''
        
        app_path = os.path.join(BASE_DIR, "streamlit_app.py")
        with open(app_path, "w", encoding="utf-8") as f:
            f.write(app_code)
        
        # Streamlit'i başlat
        cmd = [sys.executable, "-m", "streamlit", "run", app_path, "--server.port", "8501", "--server.headless", "true"]
        
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        print("🚀 Streamlit başlatılıyor...")
        time.sleep(3)  # Streamlit'in başlaması için bekle
        
        if process.poll() is None:
            print("✅ Streamlit başarıyla başlatıldı!")
            print("📊 Panel adresi: http://localhost:8501")
            return process
        else:
            stdout, stderr = process.communicate()
            print(f"❌ Streamlit başlatılamadı: {stderr}")
            return None
            
    except Exception as e:
        print(f"❌ Streamlit başlatma hatası: {e}")
        return None

def main():
    """Ana fonksiyon"""
    print("""
===============================================
    TRM NIRVANA v3.0 - STREAMLIT HEADLESS MOD
===============================================
  🌐 Port: 8501
  📊 Headless (Arayüzsüz) Mod
  🔧 Arka Plan Ajan Desteği
  🚀 Otomatik Başlatma
===============================================
    """)
    
    # Orchestrator'ı arka planda başlat
    start_orchestrator_background()
    
    # Streamlit'i başlat
    streamlit_process = start_streamlit_headless()
    
    if streamlit_process:
        try:
            print("\n✅ Sistem aktif! Tarayıcıda http://localhost:8501 adresini açın.")
            print("⌨️ Çıkmak için Ctrl+C basın...")
            
            # Ana döngü
            while True:
                time.sleep(1)
                
                # Process kontrolü
                if streamlit_process.poll() is not None:
                    print("⚠️ Streamlit process sonlandı, yeniden başlatılıyor...")
                    streamlit_process = start_streamlit_headless()
                    
        except KeyboardInterrupt:
            print("\n👋 Sistem durduruluyor...")
            if streamlit_process:
                streamlit_process.terminate()
    else:
        print("❌ Sistem başlatılamadı!")

if __name__ == "__main__":
    main()
