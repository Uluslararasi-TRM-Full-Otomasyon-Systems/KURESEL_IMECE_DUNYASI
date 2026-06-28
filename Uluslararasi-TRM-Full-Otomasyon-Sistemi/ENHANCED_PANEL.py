import streamlit as st

# Ajan sınıflarını import ediyoruz
from trm_agents.karanlik_veri_ajani import KaranlikVeriAjani
from trm_agents.kod_cerrahi_ajani import KodCerrahiAjani
from trm_agents.stratejik_hafiza_ajani import StratejikHafizaAjani
from trm_agents.butce_sihirbazi_ajani import ButceSihirbaziAjani
from trm_agents.imece_koprucusu_ajani import ImeceKoprucusuAjani
from trm_agents.trend_onculu_ajani import TrendOnculuAjani
from trm_agents.otonom_rapor_ajani import OtonomRaporAjani
from trm_agents.sosyal_adalet_valisi_ajani import SosyalAdaletValisiAjani
from trm_agents.dijital_sinir_ajani import DijitalSinirAjani
from trm_agents.kahin_karar_ajani import KahinKararAjani

# Panel Konfigürasyonu
st.set_page_config(page_title="TRM 213 Ajanlı İmparatorluk", layout="wide")
st.title("🛰️ TRM MAREŞAL MASTER KOMUTA MERKEZİ (v6.0 - FİNAL)")
st.write("**Siber Başkomutan:** Mareşal Fahri Güzel | **Kapasite:** 213 AJAN TAM HÜKÜMET MODU")

# İmparatorluk Protokollerini Başlatma Butonu
if st.button("👑 İMPARATORLUK HÜKÜMET PROTOKOLÜNÜ BAŞLAT"):
    with st.spinner("Siber Devlet tüm birimleriyle göreve başlıyor..."):
        st.success("Tüm koruma ve karar mekanizmaları aktif!")
        
        # Ajanların raporlarını panelde birleştiriyoruz
        st.write("### 📜 Siber Devlet Zafer Raporu")
        st.write("---")
        st.write("**204. Ajan (Karanlık Veri):** " + KaranlikVeriAjani().kesfet())
        st.write("**205. Ajan (Kod Cerrahı):** " + KodCerrahiAjani().tamir_et())
        st.write("**206. Ajan (Stratejik Hafıza):** " + StratejikHafizaAjani().hatirla())
        st.write("**207. Ajan (Bütçe Sihirbazı):** " + ButceSihirbaziAjani().optimize_et())
        st.write("**208. Ajan (İmece Köprücüsü):** " + ImeceKoprucusuAjani().baglanti_kur())
        st.write("**209. Ajan (Trend Öncülü):** " + TrendOnculuAjani().tahmin_et())
        st.write("**210. Ajan (Otonom Rapor):** " + OtonomRaporAjani().raporla())
        st.write("**211. Ajan (Sosyal Adalet Valisi):** " + SosyalAdaletValisiAjani().gelir_dagit())
        st.write("**212. Ajan (Dijital Sınır Şefi):** " + DijitalSinirAjani().kalkan_aktif())
        st.write("**213. Ajan (Başkomutan Kahini):** " + KahinKararAjani().rota_oner())
        
        st.success("Mareşalim, imparatorluğunuz dünyada rakipsiz bir siber devlete dönüştü.")