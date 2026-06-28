import streamlit as st
import pandas as pd
import time
from datetime import datetime

# Yeni yüklediğimiz otonom muhafızları panele entegre ediyoruz
from governance_agents.trm_refah_ve_uretim_muhafizi import TRMRefahVeUretimMuhafizi
from governance_agents.trm_muracaat_ve_antitembellik_filtresi import TRMHarikaGumrukMuhafizi

# Sayfa Yapılandırması
st.set_page_config(page_title="TRM Otonom Ekosistem Kontrol Paneli", page_icon="🛡️", layout="wide")

# Muhafız Ajan Nesnelerini Başlatma
refah_muhafizi = TRMRefahVeUretimMuhafizi()
gumruk_muhafizi = TRMHarikaGumrukMuhafizi()

st.title("🛡️ TRM (Trend Rota Market) Geliştirilmiş Yönetim Paneli")
st.subheader("Küresel İmece Dünyası - Otonom Yönetim ve Denetim Merkezi")
st.markdown("---")

# SOL PANEL - SİSTEM DURUMU VE KOTA KORUMASI
st.sidebar.header("📊 Sistem Metrikleri")
st.sidebar.success("⚡ Veri Koruma Modu: Aktif (Sıfır Kota İsrafı)")
st.sidebar.info(f"📅 Güncel Tarih: {datetime.now().strftime('%d.%m.%Y')}")

menu = st.sidebar.radio("Navigasyon", [
    "📌 Genel Durum", 
    "♿ Müracaat & Gümrük Denetimi", 
    "💰 Refah & Tembellik Süzgeci", 
    "🤖 CrewAI Keşif Ajanları (Ürün Swarm)"
])

# 1. TAB: GENEL DURUM
if menu == "📌 Genel Durum":
    st.header("📈 Pilot Test Genel Göstergeleri")
    col1, col2, col3 = st.columns(3)
    col1.metric("Hedeflenen Pilot Katılımcı", "10 Kişi", "Başlangıç Aşaması")
    col2.metric("Aktif Denetlenen Dosya Sayısı", "2 Muhafız Ajan", "Kilitli")
    col3.metric("Güncel Yoksulluk Sınırı (Türk-İş)", f"{refah_muhafizi.turkis_yoksulluk_siniri} TL", "Mayıs 2026")
    
    st.info("💡 Bu panel, TBMM Engelliler Komisyonu'na sunulan 'Sınırsız İstihdam Modeli' raporunun otonom doğrulama merkezidir.")

# 2. TAB: MÜRACAAT & GÜMRÜK DENETİMİ
elif menu == "♿ Müracaat & Gümrük Denetimi":
    st.header("📋 Akıllı Gümrük ve Anti-Tembellik Filtresi Sistemi")
    st.write("Sanal Mouse ve Ekran Okuma simülasyonu ile gelen verilerin anlık denetimi.")
    
    # Test için örnek müracaat form verisi alanları
    basvuru_tipi = st.selectbox("Başvuru Sahibi Tipi", ["REFAKATCI_UZERINDEN", "KENDISI"])
    aday_adi = st.text_input("Aday Adı Soyadı", "Ahmet Yılmaz (Ağır Engelli Evlat)")
    refakatci_adi = st.text_input("Refakatçi Adı (Varsa)", "Ayşe Yılmaz (Anne)")
    form_hizi = st.number_input("Form Doldurma Hızı (Saniye)", min_value=1, value=75)
    
    if st.button("🛡️ Gümrük Denetimini Otonom Çalıştır"):
        test_formu = {
            "basvuru_sahibi_tipi": basvuru_tipi,
            "aday_adi": aday_adi,
            "refakatci_adi": refakatci_adi,
            "form_hizi_sn": form_hizi,
            "sanal_mouse_ekran_okuma": {
                "raporda_agir_engelli_yaziyor_mu": True,
                "rapor_orani": 90
            }
        }
        with st.spinner("Sanal Göz ve RPA taraması yapılıyor..."):
            time.sleep(1)
            sonuc = gumruk_muhafizi.basvuru_sorgula(test_formu)
            
            if "ONAY" in sonuc["durum"]:
                st.success(f"🟢 DURUM: {sonuc['durum']}\n\n{sonuc['mesaj']}")
            else:
                st.error(f"🔴 DURUM: {sonuc['durum']}\n\n{sonuc['mesaj']}")

# 3. TAB: REFAH & TEMBELLİK SÜZGECİ
elif menu == "💰 Refah & Tembellik Süzgeci":
    st.header("⚖️ Dinamik Refah Payı ve Üretim Sorumluluğu Denetimi")
    
    uye_isim = st.text_input("Denetlenecek Üye Adı", "Ahmet Yılmaz")
    mevcut_maas = st.number_input("Mevcut Maaş (TL)", min_value=0.0, value=30000.0)
    istifa_durumu = st.checkbox("Sistem Gelirine Tamah Edip İşinden İstifa Etti mi?")
    mesai_saati = st.slider("Günlük TRM Dijital Üretim Mesai Saati", 0, 8, 4)
    
    if st.button("📊 Refah Desteği Hesapla"):
        uye_bilgisi = {
            "isim": uye_isim,
            "mevcut_maas": mevcut_maas,
            "aktif_calisiyor_mu": not istifa_durumu,
            "istifa_etti_mi": istifa_durumu,
            "trm_gunluk_mesai_saati": mesai_saati
        }
        
        with st.spinner("Sorumluluk ve Hak Ediş kuralları işletiliyor..."):
            time.sleep(1)
            sonuc = refah_muhafizi.uye_durum_denetle(uye_bilgisi)
            
            if sonuc["durum"] == "ONAYLANDI":
                st.success(f"✅ ONAY: {sonuc['neden']}")
                st.metric("Aktarılacak Refah Tamamlama Payı", f"{sonuc['hak_edis']:.2f} TL")
            elif sonuc["durum"] == "REDDEDİLDİ":
                st.error(f"🚫 RED: {sonuc['neden']} - Hak ediş iptal edildi.")
            else:
                st.warning(f"⚠️ DURUM: {sonuc['durum']} - {sonuc['neden']}")

# 4. TAB: CREWAI KEŞİF AJANLARI
elif menu == "🤖 CrewAI Keşif Ajanları (Ürün Swarm)":
    st.header("🔍 Aşama 1: Keşif Ajanları (Trend & Pazar Tarama Ordusu)")
    st.write("Scout_Agent ve Profit_Analyst_Agent tarafından otonom çekilen anlık global veri akışı.")
    
    if st.button("🛸 Küresel Pazar Yeri Taramasını Başlat (Simüle)"):
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        status_text.text("🤖 [Scout_Agent] Amazon Best Sellers listelerine sızıyor...")
        progress_bar.progress(30)
        time.sleep(1)
        
        status_text.text("🤖 [Scout_Agent] Trend e-ticaret parametreleri ve komisyon oranları çekildi.")
        progress_bar.progress(60)
        time.sleep(1)
        
        status_text.text("⚙️ [Profit_Analyst_Agent] Kargo maliyetleri ve net kâr marjları hesaplanıyor...")
        progress_bar.progress(90)
        time.sleep(1)
        
        progress_bar.progress(100)
        status_text.text("✅ İşlem Tamamlandı! En Kârlı Ürünler Havuza Aktarıldı.")
        
        # Simüle ürün veritabanı tablosu
        urun_data = {
            "Ürün Adı": ["Ortopedik Destekli Minder", "Akıllı Evcil Hayvan Besleyici", "Mini Taşınabilir Projeksiyon"],
            "Kaynak Platform": ["Amazon US", "Clickbank", "AliExpress"],
            "Brüt Fiyat": ["$29.99", "$45.00", "$89.99"],
            "Net Komisyon Oranı": ["%15", "%40", "%8"],
            "Yapay Zeka Kârlılık Skoru": ["9.4 / 10", "8.7 / 10", "8.1 / 10"]
        }
        df = pd.DataFrame(urun_data)
        st.table(df)
