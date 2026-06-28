import streamlit as st
from trm_agents.dinamik_regulasyon_ajani import DinamikRegulasyonAjani
from trm_agents.aksan_senkronize_ajani import AksanSenkronizeAjani
from trm_agents.kuresel_tedarik_ajani import KureselTedarikAjani

st.set_page_config(page_title="TRM 200 Ajanlık Komuta Merkezi", layout="wide")
st.title("🛰️ TRM MAREŞAL MASTER KOMUTA MERKEZİ (v4.5)")
st.write("**Siber Ordu:** 200 Ajan TAM MUTABAKAT[cite: 1]")

# Ajanları Başlat
reg = DinamikRegulasyonAjani()
aks = AksanSenkronizeAjani()
ted = KureselTedarikAjani()

if st.button("🚀 200 Ajanlık Küresel Hakimiyet Operasyonunu Başlat!"):
    st.success("Tüm ajanlar görev başında!")
    st.write("171. Ajan: " + reg.tarama_yap())
    st.write("172. Ajan: " + aks.module_et())
    st.write("174. Ajan: " + ted.stok_kontrol())
    st.info("Detaylar: TRM_Buyuk_Strateji_Belgesi.pdf dosyasında nizamlanmıştır[cite: 1].")