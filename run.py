import streamlit as st
from trm_agents.CoreNexus import CoreNexus
from trm_agents.account_manager_agent import AccountManagerAgent
from trm_agents.camouflage_agent import CamouflageAgent

def start_factory():
    # 1. Beyni başlat
    nexus = CoreNexus(domain="trm-operations.net")
    
    # 2. Ajanları oluştur
    account_agent = AccountManagerAgent()
    camouflage_agent = CamouflageAgent()
    
    # 3. Ajanları merkeze bağla
    nexus.connect_agent("AccountManager", account_agent)
    nexus.connect_agent("CamouflageAgent", camouflage_agent)
    
    # 4. Operasyonu başlat ve Maskeyi tak
    st.write("--- Fabrika Çalıştırılıyor: İzler Gizleniyor ---")
    session_id = camouflage_agent.mask_identity()
    nexus.run_system_sync()
    
    # 5. Sonuç bildirimi
    st.success(f"Sistem Hazır. Aktif Maske ID: {session_id}")
    return True

# --- Streamlit Arayüzü ---
st.title("TRM-Operations Merkezi")
st.write("Sistem durumu: Operasyonel ve Güvenli")

if st.button("Fabrikayı Çalıştır"):
    start_factory()