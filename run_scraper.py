import streamlit as st
# Diğer mevcut importların burada kalsın...
from imece_utils.theme import inject_theme  # Yeni eklediğimiz tema modülü

# Sayfa ayarlarını yapılandır
st.set_page_config(page_title="İmparatorluk Paneli", layout="wide")

# Yeni İmparatorluk temasını enjekte et (Glassmorphism ve Altın Vurgular)
inject_theme()

# Buradan itibaren mevcut kodların (run_scraper_logic vb.) devam edebilir...