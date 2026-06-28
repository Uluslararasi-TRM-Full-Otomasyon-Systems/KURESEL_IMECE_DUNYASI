import streamlit as st
from trm_agents.kultur_elcisi_ajani import KulturElcisiAjani
from trm_agents.stok_tahminci_ajani import StokTahminciAjani
from trm_agents.itibar_muhafizi_ajani import ItibarMuhafiziAjani

st.set_page_config(page_title="TRM 203 Ajanlık Komuta Merkezi", layout="wide")
st.title("🛰️ TRM MAREŞAL MASTER KOMUTA MERKEZİ (v4.6)")
st.write("**Siber Başkomutan:** Mareşal Fahri Güzel | **Sistem Kapasitesi:** 203 AJAN TAM KADRO")

# Ajan Başlatma
kultur = KulturElcisiAjani()
stok = StokTahminciAjani()
itibar = ItibarMuhafiziAjani()

st.subheader("🛠️ Süper Ajan Operasyonları")
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("🎭 181. Ajan: Kültür Elçisi"):
        st.write(kultur.yerel_kod_ekle("Japonya"))
with col2:
    if st.button("⚡ 182. Ajan: Stok Tahminci"):
        st.write(stok.tahminci_uret())
with col3:
    if st.button("🛡️ 183. Ajan: İtibar Muhafızı"):
        st.write(itibar.kriz_coz())

st.info("Sistem 203 ajana kadar genişletilmiştir, tüm birimler kışlada nizamdadır.")