import os
import sys
import streamlit as st
from datetime import datetime

# Sörf alanı: Sistemin ana klasörünü otomatik tanı (otomatik path fix)
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from trm_agents.CoreNexus import CoreNexus
from trm_agents.camouflage_agent import CamouflageAgent
from trm_agents.account_manager_agent import AccountManagerAgent

def run_scraper_logic():
    # 1. CoreNexus'u başlat ve tüm ajanları bağla
    nexus = CoreNexus()
    camou = CamouflageAgent()
    account_mgr = AccountManagerAgent()
    
    # Ajanları sisteme bağla
    nexus.connect_agent("CamouflageAgent", camou)
    nexus.connect_agent("AccountManagerAgent", account_mgr)
    
    # 2. Operatör kimliği ataması
    operator_identity = account_mgr.assign_operator_identity("TR")
    st.write(f"Operatör Kimliği: {operator_identity['identity']}")
    st.write(f"E-posta: {operator_identity['email']}")
    
    # 3. Maskeyi tak (CoreNexus üzerinden maskelenmiş operasyon)
    mask_id = camou.mask_identity()
    st.write(f"Maskeli Operasyon Aktif: {mask_id}")
    
    # 4. Veri işleme havuzu (CoreNexus senkronizasyonu ile)
    nexus.run_system_sync()
    
    sample_products = [
        {"title": "Organik Zeytin Yagi 1L", "product_url": "https://www.trendyol.com/gida-saglik-ve-ozel-bakim/organik-urunler/organik-zeytin-yagi"},
        {"title": "Kozmetik Cilt Bakim Seti", "product_url": "https://www.trendyol.com/kozmetik/cilt-bakim/cilt-bakim-seti"},
        {"title": "Nemlendirici Krem", "product_url": "https://www.trendyol.com/kozmetik/cilt-bakim/nemlendirici-krem"},
        {"title": "Şampuan 500ml", "product_url": "https://www.trendyol.com/kozmetik/sac-bakim/sampuan"},
        {"title": "Bal 1kg", "product_url": "https://www.trendyol.com/gida-saglik-ve-ozel-bakim/tatli-urunler/bal"}
    ]
    
    output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ACIL_SATIS_HAVUZU.txt")
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("=========================================\n")
        f.write("TRM ACIL NAKIT OTOMASYONU - ACIL SATIS HAVUZU\n")
        f.write("=========================================\n")
        f.write(f"Baslama Zamani: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Maske ID: {mask_id}\n")
        f.write(f"Operatör: {operator_identity['identity']}\n")
        f.write(f"E-posta: {operator_identity['email']}\n")
        f.write(f"Domain: {operator_identity['domain_authority']}\n")
        f.write(f"Toplam Urun: {len(sample_products)}\n")
        f.write("=========================================\n\n")
        
        affiliate_id = "trendurunlermarket"
        
        for p in sample_products:
            affiliate_link = p['product_url']
            if "?" in affiliate_link:
                affiliate_link += f"&affiliate={affiliate_id}"
            else:
                affiliate_link += f"?affiliate={affiliate_id}"
            f.write(f"{p['title']} - {affiliate_link}\n")
            
    st.success(f"Havuz güncellendi! Dosya: {output_path}")

# --- Streamlit Arayüzü (Tek tuşla sörf) ---
st.title("TRM-Operations Otonom Scraper")
if st.button("Sistemi Başlat ve Havuzu Çek"):
    run_scraper_logic()