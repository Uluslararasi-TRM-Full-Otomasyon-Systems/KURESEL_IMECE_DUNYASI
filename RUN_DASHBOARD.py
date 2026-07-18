#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TRM Nirvana v3.0 - Gelişmiş Yönetim Paneli
Streamlit headless modda port 8501'de çalışır
"""

import sys
import os
import subprocess
import time

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    
def start_streamlit_headless():
    """Streamlit'i headless modda baÅlat"""
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
"""
        config_path = os.path.join(BASE_DIR, ".streamlit", "config.toml")
        os.makedirs(os.path.dirname(config_path), exist_ok=True)
        with open(config_path, "w", encoding="utf-8") as f:
            f.write(config)
        
        # Streamlit app oluştur - basitlestirilmis versiyon
        app_code = '''
import streamlit as st
import datetime

st.set_page_config(
    page_title="TRM Nirvana v3.0",
    layout="wide"
)

# Test komutu - arayuzun yuklendigini dogrulamak icin
st.write("SISTEM BASARILI BIR SEKILDE CALISIYOR")

st.title("TRM NIRVANA v3.0 - Gelistirilmis Yonetim Paneli")
st.markdown("---")

st.info("Sistem aktif - Streamlit headless modda calisiyor")
st.success(f"Panel adresi: http://localhost:8501")
st.info(f"Baslangic zamani: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
'''
        
        app_path = os.path.join(BASE_DIR, "streamlit_app.py")
        with open(app_path, "w", encoding="utf-8") as f:
            f.write(app_code)
        
        # Streamlit'i baÅlat
        cmd = [sys.executable, "-m", "streamlit", "run", app_path, "--server.port", "8501", "--server.headless", "true"]
        
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        print("Streamlit baslatiliyor...")
        time.sleep(3)  # Streamlit'in baslamasi icin bekle
        
        if process.poll() is None:
            print("Streamlit basariyla baslatildi!")
            print("Panel adresi: http://localhost:8501")
            return process
        else:
            stdout, stderr = process.communicate()
            print(f"Streamlit baslatilamadi: {stderr}")
            return None
            
    except Exception as e:
        print(f"Streamlit baslatma hatasi: {e}")
        return None
    

def main():
    """Ana fonksiyon"""
    print("===============================================")
    print("  TRM NIRVANA v3.0 - STREAMLIT HEADLESS MOD")
    print("===============================================")
    print("  Port: 8501")
    print("  Headless (Arayuzsuz) Mod")
    print("===============================================\n")
    
    # Streamlit'i baslat
    streamlit_process = start_streamlit_headless()
    
    if streamlit_process:
        print("\nSistem aktif! Tarayicida http://localhost:8501 adresini acin.")
        print("Cikmak icin Ctrl+C basin...\n")
        
        try:
            while True:
                time.sleep(1)
                
                if streamlit_process.poll() is not None:
                    print("Streamlit process sonlandi, yeniden baslatiliyor...")
                    streamlit_process = start_streamlit_headless()
                    
        except KeyboardInterrupt:
            print("\nSistem durduruluyor...")
            if streamlit_process:
                streamlit_process.terminate()
    else:
        print("Sistem baslatilamadi!")

if __name__ == "__main__":
    main()
