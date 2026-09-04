# -*- coding: utf-8 -*-
import streamlit as st
import os
import json
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import pandas as pd
import random

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
tab1, tab2, tab3, tab4 = st.tabs(["📊 Sistem Durumu & Metrikler", "🌍 Geo-Intelligence & Füzyon", "🤖 Dinamik Ajan Havuzu", "🧠 Davranışsal Pazarlama Ajanı"])

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

with tab4:
    st.subheader("🧠 TRM Nirvana v3.0 - Davranışsal Pazarlama Ajanı")
    st.markdown("""**Otonom Özellikler:**
    - 📍 **Lokasyon Bazlı Analiz**: Kullanıcının bölgesine göre dinamik içerik önerisi
    - 🔄 **Davranışsal Takip & Feedback Loop**: Etkileşim detaylarını kaydetme ve analiz etme
    - 😊 **Ruh Hali / Niyet Tespiti**: Anlık niyet analizi ve uygun mesaj gösterimi""")
    
    # Ajan başlatma
    col1, col2 = st.columns([2, 1])
    
    with col1:
        if st.button("🚀 Davranışsal Ajanı Başlat", use_container_width=True):
            try:
                from behavioral_marketing_agent import BehavioralMarketingAgent
                if 'behavioral_agent' not in st.session_state:
                    st.session_state.behavioral_agent = BehavioralMarketingAgent()
                st.success("✅ Davranışsal Pazarlama Ajanı başlatıldı!")
            except Exception as e:
                st.error(f"⚠️ Hata: {e}")
    
    with col2:
        if st.button("📊 Rapor Oluştur", use_container_width=True):
            try:
                if 'behavioral_agent' in st.session_state:
                    report_path = st.session_state.behavioral_agent.export_behavioral_report()
                    st.success(f"✅ Rapor oluşturuldu: {report_path}")
                else:
                    st.warning("⚠️ Önce ajanı başlatın")
            except Exception as e:
                st.error(f"⚠️ Hata: {e}")
    
    # Simülasyon Paneli
    st.divider()
    st.subheader("🎮 Simülasyon Paneli")
    
    sim_col1, sim_col2, sim_col3 = st.columns(3)
    
    with sim_col1:
        test_location = st.selectbox("📍 Test Lokasyonu", ["Kuşadası", "Nazilli", "İstanbul", "Ankara", "İzmir", "default"])
    
    with sim_col2:
        test_product = st.text_input("📦 Test Ürünü", "Premium Yazlık Elbise")
    
    with sim_col3:
        test_engagement = st.slider("⏱️ Etkileşim Süresi (saniye)", 0, 60, 25)
    
    if st.button("🔄 Simülasyon Çalıştır", use_container_width=True):
        try:
            if 'behavioral_agent' not in st.session_state:
                st.warning("⚠️ Önce ajanı başlatın")
            else:
                agent = st.session_state.behavioral_agent
                
                # Simüle edilmiş session data
                session_data = {
                    "user_id": f"test_user_{random.randint(1000, 9999)}",
                    "location": test_location,
                    "viewed_product": test_product,
                    "engagement_time": test_engagement,
                    "click_count": random.randint(0, 10),
                    "interaction_type": "view"
                }
                
                # Analiz çalıştır
                user_intent = agent.analyze_user_behavior(session_data)
                personalized_message = agent.generate_personalized_message(user_intent)
                
                # Sonuçları göster
                st.success("✅ Simülasyon tamamlandı!")
                
                # Sonuç kartları
                result_col1, result_col2, result_col3 = st.columns(3)
                
                with result_col1:
                    st.metric("📍 Lokasyon", user_intent["location"])
                    st.metric("😊 Ruh Hali", user_intent["mood"])
                
                with result_col2:
                    st.metric("🎯 Niyet Tipi", user_intent["intent_type"])
                    st.metric("📊 Güven Skoru", f"{user_intent['confidence_score']:.2f}")
                
                with result_col3:
                    st.metric("⚡ Önerilen Eylem", user_intent["recommended_action"])
                
                st.divider()
                st.subheader("📝 Kişiselleştirilmiş Mesaj")
                st.info(personalized_message)
                
                st.divider()
                st.subheader("📦 Lokasyon Bazlı Ürün Önerileri")
                st.write(user_intent["location_products"])
                
        except Exception as e:
            st.error(f"⚠️ Simülasyon hatası: {e}")
    
    # Canlı Metrikler
    st.divider()
    st.subheader("📊 Canlı Davranışsal Metrikler")
    
    if 'behavioral_agent' in st.session_state:
        agent = st.session_state.behavioral_agent
        metrics = agent.get_aggregated_metrics()
        
        metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)
        
        metric_col1.metric("👥 Toplam Kullanıcı", metrics["total_users"])
        metric_col2.metric("🔄 Toplam Etkileşim", metrics["total_interactions"])
        metric_col3.metric("⏱️ Ort. Etkileşim Süresi", f"{metrics['avg_engagement_time']:.1f}s")
        metric_col4.metric("🖱️ Ort. Tıklama Oranı", f"{metrics['avg_click_rate']:.2f}")
        
        # Grafikler
        st.divider()
        graph_col1, graph_col2 = st.columns(2)
        
        with graph_col1:
            st.subheader("📍 Lokasyon Dağılımı")
            location_data = agent.get_behavioral_metrics()
            if location_data:
                loc_counts = {}
                for user_data in location_data.values():
                    loc = user_data.get("location", "unknown")
                    loc_counts[loc] = loc_counts.get(loc, 0) + 1
                
                if loc_counts:
                    fig_loc = px.pie(
                        values=list(loc_counts.values()),
                        names=list(loc_counts.keys()),
                        title="Kullanıcı Lokasyon Dağılımı",
                        color_discrete_sequence=px.colors.sequential.Viridis
                    )
                    st.plotly_chart(fig_loc, use_container_width=True)
                else:
                    st.info("Henüz lokasyon verisi yok")
        
        with graph_col2:
            st.subheader("😊 Ruh Hali Dağılımı")
            behavior_data = agent.get_behavioral_metrics()
            if behavior_data:
                mood_counts = {"focused": 0, "interested": 0, "browsing": 0, "neutral": 0}
                for user_data in behavior_data.values():
                    # Son etkileşime göre mood tahmini
                    view_times = user_data.get("view_times", [])
                    if view_times:
                        avg_time = sum(view_times) / len(view_times)
                        if avg_time > 30:
                            mood_counts["focused"] += 1
                        elif avg_time > 15:
                            mood_counts["interested"] += 1
                        else:
                            mood_counts["browsing"] += 1
                    else:
                        mood_counts["neutral"] += 1
                
                fig_mood = px.bar(
                    x=list(mood_counts.keys()),
                    y=list(mood_counts.values()),
                    title="Kullanıcı Ruh Hali Dağılımı",
                    color=list(mood_counts.values()),
                    color_continuous_scale=px.colors.sequential.Blues
                )
                st.plotly_chart(fig_mood, use_container_width=True)
            else:
                st.info("Henüz ruh hali verisi yok")
        
        # Zaman serisi grafiği
        st.divider()
        st.subheader("📈 Etkileşim Süresi Trendi")
        behavior_data = agent.get_behavioral_metrics()
        if behavior_data:
            all_times = []
            for user_data in behavior_data.values():
                all_times.extend(user_data.get("view_times", []))
            
            if all_times:
                df_times = pd.DataFrame({
                    "Etkileşim Sırası": range(1, len(all_times) + 1),
                    "Süre (saniye)": all_times
                })
                
                fig_trend = px.line(
                    df_times,
                    x="Etkileşim Sırası",
                    y="Süre (saniye)",
                    title="Etkileşim Süresi Trendi",
                    markers=True
                )
                fig_trend.add_hline(y=30, line_dash="dash", line_color="red", annotation_text="Yüksek Eşik")
                fig_trend.add_hline(y=15, line_dash="dash", line_color="orange", annotation_text="Orta Eşik")
                st.plotly_chart(fig_trend, use_container_width=True)
            else:
                st.info("Henüz etkileşim verisi yok")
    else:
        st.info("👆 Önce ajanı başlatın ve simülasyon çalıştırın")
    
    # Rapor görüntüleme
    st.divider()
    st.subheader("📋 Davranışsal Pazarlama Raporu")
    report_path = "reports/behavioral_marketing_report.json"
    if os.path.exists(report_path):
        with open(report_path, "r", encoding="utf-8") as f:
            report_data = json.load(f)
        
        st.json(report_data)
    else:
        st.info("Henüz bir rapor oluşturulmadı. 'Rapor Oluştur' butonuna tıklayın.")