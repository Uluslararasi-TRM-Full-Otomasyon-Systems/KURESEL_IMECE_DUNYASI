import streamlit as st
from trm_agents.karanlik_veri_ajani import KaranlikVeriAjani
from trm_agents.kod_cerrahi_ajani import KodCerrahiAjani
from trm_agents.stratejik_hafiza_ajani import StratejikHafizaAjani
# ... (Diğer ajanları da import edin)

st.title("🛰️ TRM MAREŞAL MASTER KOMUTA MERKEZİ (v5.0 - İMPARATORLUK)")
st.write("210 AJAN TAM KADRO - SİBER DEVLET MODU AKTİF")

if st.button("🚀 İMPARATORLUK HAREKATINI BAŞLAT"):
    st.success("Tüm ajanlar stratejik mevzilerine yerleşti!")
    st.write("204. Ajan (Karanlık Veri): " + KaranlikVeriAjani().kesfet())
    st.write("205. Ajan (Kod Cerrahı): " + KodCerrahiAjani().tamir_et())
    st.write("206. Ajan (Stratejik Hafıza): " + StratejikHafizaAjani().hatirla())
    # ... (Diğerleri)