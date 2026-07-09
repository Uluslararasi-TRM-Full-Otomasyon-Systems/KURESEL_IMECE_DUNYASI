import streamlit as st
from ORCHESTRATOR_AGENT import main as run_orchestrator

st.set_page_config(page_title="TRM Full Otomasyon Paneli", layout="wide")

st.title("🚀 TRM Full Otomasyon Paneli")
st.markdown("Fahri, sistemin 7/24 otonom çalışıyor. Buradan operasyonu tetikleyebilirsin.")

if st.button("🔴 Operasyonu Başlat"):
    with st.spinner("Sistem denetleniyor ve küresel üretim başlıyor..."):
        try:
            run_orchestrator()
            st.success("Operasyon başarıyla tamamlandı!")
        except Exception as e:
            st.error(f"Hata: {e}")

st.sidebar.header("Sistem Durumu")
st.sidebar.info("Modül: Küresel Video Fabrikası")
st.sidebar.info("Modül: Sosyal Medya Uploader")
st.sidebar.info("Modül: Süper Denetçi")