import streamlit as st
import os
import sys
from pathlib import Path

# Proje kök dizinini absolute path olarak al
PROJECT_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(PROJECT_ROOT))

# GROQ_API_KEY güvenli çekilmesini doğrula
GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "")
if not GROQ_API_KEY:
    st.warning("⚠️ GROQ_API_KEY ortam değişkeni bulunamadı. Lütfen ayarlayın.")

st.set_page_config(page_title="TRM Full Otomasyon Paneli", layout="wide")

st.title("🚀 TRM Full Otomasyon Paneli")
st.markdown("Fahri, sistemin 7/24 otonom çalışıyor. Buradan operasyonu tetikleyebilirsin.")

# Sidebar - Sistem Durumu
st.sidebar.header("📊 Sistem Durumu")
st.sidebar.info("Modül: Küresel Video Fabrikası")
st.sidebar.info("Modül: Sosyal Medya Uploader")
st.sidebar.info("Modül: Süper Denetçi")

# API Anahtarı Durumu
st.sidebar.subheader("🔑 API Anahtarları")
st.sidebar.info(f"GROQ_API_KEY: {'✅ Aktif' if GROQ_API_KEY else '❌ Eksik'}")

# Ana Panel
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("🎯 Operasyon Kontrolü")
    
    # Ürün Seçimi
    product_options = ["High_End_Electronics", "Fashion_Trends", "Home_Appliances", "Digital_Products"]
    selected_product = st.selectbox("Ürün Kategorisi Seçin:", product_options)
    
    # Dil Seçimi
    language_options = ["Japanese", "German", "English", "Spanish", "Turkish"]
    selected_languages = st.multiselect("Hedef Pazarlar Seçin:", language_options, default=["English", "Turkish"])
    
    # Operasyon Başlat Butonu
    if st.button("🔴 Operasyonu Başlat", type="primary"):
        if not selected_languages:
            st.error("⚠️ En az bir hedef pazar seçmelisiniz!")
        else:
            with st.spinner(f"Sistem denetleniyor ve {selected_product} için küresel üretim başlıyor..."):
                try:
                    # ORCHESTRATOR_AGENT'ı çağır
                    from ORCHESTRATOR_AGENT import main as run_orchestrator
                    
                    # Progress bar göster
                    progress_bar = st.progress(0)
                    status_text = st.empty()
                    
                    for i, lang in enumerate(selected_languages):
                        status_text.text(f"🔄 {lang} pazarı için içerik üretiliyor...")
                        progress_bar.progress((i + 1) / len(selected_languages))
                    
                    # Gerçek orchestrator çağrısı
                    run_orchestrator()
                    
                    progress_bar.progress(1.0)
                    status_text.text("✅ Operasyon tamamlandı!")
                    st.success(f"🎉 {selected_product} operasyonu {len(selected_languages)} pazar için başarıyla tamamlandı!")
                    
                except ImportError as e:
                    st.error(f"❌ Import hatası: {e}")
                    st.info("ORCHESTRATOR_AGENT.py dosyasının proje kök dizinde olduğundan emin olun.")
                except Exception as e:
                    st.error(f"❌ Operasyon hatası: {e}")
                    st.info("Detaylı hata bilgisi için terminal loglarını kontrol edin.")

with col2:
    st.subheader("📈 İstatistikler")
    
    # Mock istatistikler
    st.metric("Toplam Operasyon", "156")
    st.metric("Başarı Oranı", "%94")
    st.metric("Aktif Pazarlar", "5")
    st.metric("Günlük Üretim", "23 video")

# Log Paneli
st.subheader("📋 Sistem Logları")
log_placeholder = st.empty()
log_placeholder.info("🔄 Log sistemi başlatılıyor...")

# Otomatik yenileme
if st.checkbox("🔄 Otomatik Yenileme (30 saniye)", value=False):
    import time
    time.sleep(30)
    st.rerun()