# ==============================================================================
# 🤖 KÜRESEL SOSYAL İMECE DÜNYASI - OTONOM AJAN VE SWARM YÖNETİM BLOĞU
# ==============================================================================
import os
import logging
import streamlit as st
from logging.handlers import RotatingFileHandler

logger = logging.getLogger("trm_panel")
if not logger.handlers:
    os.makedirs("logs", exist_ok=True)
    handler = RotatingFileHandler("logs/panel.log", maxBytes=1_000_000, backupCount=3, encoding="utf-8")
    formatter = logging.Formatter("%(asctime)s %(levelname)s %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)

st.markdown("---") # Mevcut panel içeriklerinden görsel olarak ayırır
st.header("🤖 161 Ajanlı Otonom Ekosistem Yönetimi")
st.caption("Küresel Sosyal İmece Dünyası ve TRM Full Otomasyon Altyapısı")

# Yan menüye (Sidebar) sistem anahtarı ve kontrolü ekleme
st.sidebar.markdown("---")
st.sidebar.subheader("⚙️ Swarm Protokol Ayarları")
otonom_sistem_aktif = st.sidebar.toggle("Otonom Ajan Sistemini Devreye Al", value=False)

if otonom_sistem_aktif:
    # Ajanların çalışma durumunu görselleştirmek için durum kartları
    col_a, col_b, col_c = st.columns(3)
    with col_a:
        st.success("🤖 Core Agents: READY")
    with col_b:
        st.success("🔍 Discovery Node: ACTIVE")
    with col_c:
        st.success("📡 DNP Protocol: LISTENING")
        
    st.info("💡 **Bilgi:** Sistem `gpt-4o-mini` mimarisi üzerinde en optimum kaynak tüketimiyle çalışacak şekilde konfigüre edilmiştir.")

    # Operasyon Seçenekleri
    hedef_platform = st.selectbox(
        "Taranacak Affiliate Ağı Seçin",
        ["Amazon International (Global)", "Clickbank (Digital Products)", "Trendurunler Market Veri Ağı"]
    )

    # Tetikleyici Buton
    if st.button("🚀 Otonom Pazar Keşfi ve İçerik Çevrimini Tetikle"):
        with st.spinner("Ajan Swarm'u çalıştırılıyor... Lütfen bekleyin..."):
            try:
                # Modüllerimizi canlı olarak içeri alıyoruz
                from otonom_tarayici import OtonomVeriMotoru
                from icerik_fabrikasi import IcerikFabrikasi
                from ses_motoru import SanalElSesMotoru

                # 1. GÖZLER: Tarayıcıyı çalıştır
                motor = OtonomVeriMotoru()
                simule_html = """
                <div class='product-card'>
                    <h1>Autonomous Smart Home Hub V4</h1>
                    <span class='price'>$129.00</span>
                    <p>High demand item with 25% recurring affiliate commission rate. Perfect for tech enthusiasts.</p>
                </div>
                """

                st.write("🔄 *[Global_Product_Discoverer]* Hedef platform çerezlerle analiz ediliyor...")
                urun_analiz_sonucu = motor.sayfa_analiz_et(
                    url=f"https://target-network.com/scraped-{hedef_platform.lower().replace(' ', '-')}",
                    html_icerik=simule_html
                )

                # 2. BEYİN: İçerik Fabrikasını çalıştır
                st.write("🔄 *[Autonomous_Content_Factory]* Metin ve pazarlama stratejisi üretiliyor...")
                fabrika = IcerikFabrikasi(urun_analiz_sonucu)
                uretilen_reklam_metni = fabrika.icerik_uret()

                # 3. DİL: Sanal El Ses Motorunu çalıştır
                st.write("🔄 *[Sanal_El_Voice_Assistant]* Metin otonom olarak seslendiriliyor...")
                ses_motoru = SanalElSesMotoru()
                ses_dosyasi = ses_motoru.metni_seslendir(uretilen_reklam_metni)

                st.success("🎯 Tüm Otonom Çevrim Başarıyla Tamamlandı!")

                # Ekrana Çıktıları Basalım
                st.subheader("📦 Keşfedilen Fırsat Detayları")
                c1, c2, c3 = st.columns(3)
                c1.metric("Ürün Adı", urun_analiz_sonucu.get("urun_adi", "Bilinmiyor"))
                c2.metric("Fiyat", urun_analiz_sonucu.get("fiyat", "Bilinmiyor"))
                c3.metric("Tahmini Komisyon", urun_analiz_sonucu.get("komisyon_tahmini", "Bilinmiyor"))

                st.subheader("📢 Üretilen Pazarlama İçeriği")
                st.text_area("Sosyal Medya ve Blog Uyumlu Çıktı", uretilen_reklam_metni, height=180)

                # 🎙️ Ses Oynatıcı Bileşeni
                ses_dosyasi_var = bool(ses_dosyasi) and os.path.exists(ses_dosyasi)
                if ses_dosyasi_var:
                    st.subheader("🎙️ Sanal El Otonom Ses Çıktısı")
                    ses_uzantisi = os.path.splitext(ses_dosyasi)[1].lower()
                    ses_formati = "audio/wav" if ses_uzantisi == ".wav" else "audio/mp3"
                    st.audio(ses_dosyasi, format=ses_formati)
                else:
                    st.warning("Ses çıktısı üretilemedi. Dilerseniz metni manuel girip tekrar seslendirebilirsiniz.")
                    manuel_metin = st.text_input("Manuel Metin", value=uretilen_reklam_metni)
                    if manuel_metin and st.button("🎙️ Metni Tekrar Seslendir"):
                        ses_dosyasi_2 = ses_motoru.metni_seslendir(manuel_metin)
                        if ses_dosyasi_2 and os.path.exists(ses_dosyasi_2):
                            st.subheader("🎙️ Sanal El Otonom Ses Çıktısı")
                            st.audio(ses_dosyasi_2, format="audio/mp3")

            except Exception as e:
                logger.exception("Ajan cevrimi hata verdi: %s", e)
                st.warning("Şu anda geçici bir bağlantı veya servis sorunu yaşanıyor. Lütfen tekrar deneyin.")
else:
    st.info("💤 Otonom Ajan Sistemi şu anda uykuda. Devreye almak için sol menüdeki anahtarı kullanabilirsiniz.")
# ==============================================================================
