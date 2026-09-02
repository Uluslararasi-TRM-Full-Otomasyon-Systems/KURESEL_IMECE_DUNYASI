# utils/theme.py
import streamlit as st
import os

def inject_theme():
    """
    assets/style.css dosyasını okuyarak Streamlit uygulamasına tema olarak uygular.
    """
    # Dosya yolunu proje köküne göre ayarla
    css_path = os.path.join(os.path.dirname(__file__), "..", "assets", "style.css")
    try:
        with open(css_path, "r", encoding="utf-8") as f:
            css = f.read()
        st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        st.warning("style.css dosyası bulunamadı. Tema uygulanamadı.")
    except Exception as e:
        st.error(f"Tema yüklenirken hata oluştu: {e}")