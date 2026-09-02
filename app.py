# -*- coding: utf-8 -*-
import streamlit as st
import os
import json
from datetime import datetime

# Sayfa Yapılandırması
st.set_page_config(
    page_title="TRM Nirvana v3.0 - Komuta Merkezi",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("🚀 TRM Nirvana v3.0 - Otonom Komuta Merkezi")
st.markdown("Uluslararası TRM Full Otomasyon Sistemi ve Sosyal İmece Entegrasyon Paneli")

# Kenar Çubuğu (Sidebar) Kontrolleri
st.sidebar.header("🎛️ Operasyonel Kontroller")
st.sidebar.markdown(f"**Mağaza:** `www.trendurunlermarket.com`")
st.sidebar.markdown(f"**Lokasyon:** Kuşadası / Nazilli")

if st.sidebar.button("⚡ Tüm Sistemi ve 200 Ajanı Tetikle"):
    with st.spinner("Sistem ve dinamik ajan havuzu çalıştırılıyor..."):
        try:
            from MASTER_CONTROLLER import TRMMasterController
            controller = TRMMasterController()
            started = controller.start_all_services()
            controller.generate_system_status_report()
            st.sidebar.success(f"✅ Başarıyla tetiklendi! Aktif Ajan: {started}")
        except Exception as e:
            st.sidebar.error(f"⚠️ Hata oluştu: {e}")

if st.sidebar.button("🌍 Geo-Fusion Analizini Çalıştır"):
    with st.spinner("Coğrafi İstihbarat ve E-Ticaret Füzyonu çalışıyor..."):
        try:
            from trm_agents.geo_fusion_core import GeoEcommerceFusionEngine
            engine = GeoEcommerceFusionEngine()
            engine.run_fusion_analysis()
            st.sidebar.success("✅ Geo-Fusion Raporu güncellendi!")
        except Exception as e:
            st.sidebar.error(f"⚠️ Hata: {e}")

# Ana Ekran Sekmeleri
tab1, tab2, tab3 = st.tabs(["📊 Sistem Durumu & Metrikler", "🌍 Geo-Intelligence & Füzyon", "🤖 Dinamik Ajan Havuzu"])

with tab1:
    st.subheader("Sistem Sağlığı ve Durum Raporu")
    report_path = "reports/system_status.json"
    if os.path.exists(report_path):
        with open(report_path, "r", encoding="utf-8") as f:
            status_data = json.load(f)
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Hedef Ajan Kapasitesi", status_data.get("hedef_ajan_sayisi", 200))
        col2.metric("Kodda Bulunan Gerçek Ajan", status_data.get("kodda_bulunan_gercek_ajan_sayisi", 0))
        col3.metric("Toplam Aktif Ajan", status_data.get("toplam_aktif_ajan_sayisi", 0))
        
        st.json(status_data)
    else:
        info = "Henüz bir sistem durum raporu üretilmemiş. Kenar çubuğundan sistemi tetikleyebilirsiniz."
        st.info(info)

with tab2:
    st.subheader("Coğrafi Füzyon & E-Ticaret Analizi")
    fusion_path = "reports/geo_fusion_master_report.json"
    if os.path.exists(fusion_path):
        with open(fusion_path, "r", encoding="utf-8") as f:
            fusion_data = json.load(f)
        st.json(fusion_data)
    else:
        info_geo = "Geo-Fusion raporu bekleniyor. Kenar çubuğundan analizi çalıştırabilirsiniz."
        st.info(info_geo)

with tab3:
    st.subheader("Dinamik Ajan Çıktıları ve Özetleri")
    reports_dir = "reports"
    if os.path.exists(reports_dir):
        files = [f for f in os.listdir(reports_dir) if f.startswith("dynamic_agent_")]
        st.write(f"Toplam Depolanan Dinamik Ajan Raporu: {len(files)}")
        
        selected_file = st.selectbox("İncelemek için bir ajan raporu seçin:", files if files else ["Rapor yok"])
        if selected_file and selected_file != "Rapor yok":
            with open(os.path.join(reports_dir, selected_file), "r", encoding="utf-8") as f:
                agent_data = json.load(f)
            st.json(agent_data)
    else:
        info_reports = "Reports dizini henüz oluşmadı."
        st.info(info_reports)