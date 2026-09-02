# -*- coding: utf-8 -*-
"""
UTEYKDER Otonom Uye Kabul ve On Kayit Ajani (Entegre Streamlit & Backend Paneli)
"""
import os
import json
import pandas as pd
from datetime import datetime
import streamlit as st
from PIL import Image

# 1. Streamlit Sayfa Yapılandırması
st.set_page_config(page_title="UTEYKDER - Fahri Üyelik & DERBİS Ajanı", layout="wide")

class UteykderUyeAjani:
    def __init__(self):
        self.output_file = "uteykder_fahri_uyeler.json"
        self.excel_file = "DERBIS_hazir_liste.xlsx"
        
        # Dinamik sorular listesi güncellendi
        self.dinamik_sorular = [
            {"id": "tc_no", "soru_metni": "Lütfen 11 haneli T.C. Kimlik numaranızı giriniz:"},
            {"id": "ad_soyad", "soru_metni": "Adınız ve Soyadınız nedir?"},
            {"id": "telefon", "soru_metni": "Telefon numaranızı başında sıfır olmadan giriniz:"},
            {"id": "dogum_tarihi", "soru_metni": "Doğum tarihinizi gün-ay-yıl olarak belirtiniz:"},
            {"id": "meslek", "soru_metni": "Şu an yaptığınız işin adı nedir?"},
            {"id": "calisma_suresi", "soru_metni": "Ne kadar süredir bu işi yapıyorsunuz?"},
            {"id": "engelli_orani", "soru_metni": "Engelliyseniz Sağlık Raporu oranınız nedir veya Engelli Değilim?"},
            {"id": "vasi_durumu", "soru_metni": "Engelli birine bakıyorsanız vasiğlik veya refakat belgesi durumu nedir?"}
        ]

    def veri_dogrula(self, veri):
        """Toplanan verilerin DERBİS standartlarına uygunluğunu ve T.C. kontrolünü yapar."""
        tc_degeri = str(veri.get("tc_no", "")).strip()
        if len(tc_degeri) != 11 or not tc_degeri.isdigit():
            return False, "Hatalı veya Eksik 11 Haneli T.C. Kimlik Numarası!"
        return True, "Doğrulama Başarılı."

    def uye_kaydet(self, aday_bilgileri):
        """Aday bilgilerini doğrular, JSON tabanına yazar ve DERBİS Excel şablonunu günceller."""
        dogru_mu, mesaj = self.veri_dogrula(aday_bilgileri)
        if not dogru_mu:
            return {"durum": "Hata", "mesaj": mesaj}
            
        aday_bilgileri["kayit_tarihi"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # JSON Dosyasına Yazma (Kalıcı Yedekleme)
        mevcut_veriler = []
        if os.path.exists(self.output_file):
            with open(self.output_file, 'r', encoding='utf-8') as f:
                try:
                    mevcut_veriler = json.load(f)
                except json.JSONDecodeError:
                    mevcut_veriler = []
                    
        mevcut_veriler.append(aday_bilgileri)
        
        with open(self.output_file, 'w', encoding='utf-8') as f:
            json.dump(mevcut_veriler, f, ensure_ascii=False, indent=4)
            
        # DERBİS İçin Otomatik Excel Çıktısı Üretme
        df = pd.DataFrame(mevcut_veriler)
        df.to_excel(self.excel_file, index=False)
        
        return {"durum": "Başarılı", "mesaj": "Kayıt alındı, DERBİS Excel listesi güncellendi!"}


# Ajan nesnesini oturumda başlatıyoruz
if 'ajan_motoru' not in st.session_state:
    st.session_state.ajan_motoru = UteykderUyeAjani()

if 'uye_veritabani' not in st.session_state:
    st.session_state.uye_veritabani = []
    # Eğer önceden kaydedilmiş JSON varsa yükle
    if os.path.exists(st.session_state.ajan_motoru.output_file):
        try:
            with open(st.session_state.ajan_motoru.output_file, 'r', encoding='utf-8') as f:
                st.session_state.uye_veritabani = json.load(f)
        except:
            pass

# --- Streamlit Arayüz Tasarımı ---
st.title("🤖 UTEYKDER Otonom Fahri Üyelik & Kimlik Yönetim Ajansı")
st.markdown("WhatsApp üzerinden gelen fahri üye başvuru formlarını ve kimlik bilgilerini işleyip DERBİS formatına dönüştüren yapay zeka modülü.")

with st.sidebar:
    st.header("📥 Yeni Fahri Üye Verisi Ekle")
    
    # Form Alanları (Projeler alanı kaldırıldı)
    tc_no = st.text_input("11 Haneli T.C. Kimlik No", max_chars=11)
    ad_soyad = st.text_input("Adı Soyadı")
    telefon = st.text_input("Telefon Numarası (Başında 0 olmadan)")
    dogum_tarihi = st.text_input("Doğum Tarihi (GG-AA-YYYY)")
    
    su_anki_is = st.text_input("Şu An Yaptığınız İşin Adı")
    calisma_suresi = st.text_input("Ne Kadar Süredir Bu İşi Yapıyorsunuz?")
    
    # Engellilik Durumu Seçenekleri
    engelli_secenekleri = ["Engelli Değilim"] + [f"% {i}" for i in range(40, 96)]
    engelli_orani = st.selectbox("Engelliyseniz Sağlık Raporu Oranınızı Yazın", engelli_secenekleri)
    
    # Güncellenen Vasiğlik Durumu Alanı
    vasi_durumu = st.text_input("Engelli Birine Bakıyorsanız Vasiğlik veya Refakat Belgesi Durumu")
    
    adres = st.text_area("İkametgah Adresi")
    
    # Güncellenen Belge Yükleme Alanı
    belgeler = st.file_uploader("Kimlik Fotoğrafı, vesikalık fotoğrafınızı ve Diğer Belgeleri Yükle (JPG/PNG)", type=["jpg", "jpeg", "png"], accept_multiple_files=True)
    
    if st.button("Ajan ile Doğrula ve Kaydet"):
        if ad_soyad and tc_no and telefon:
            durum_metni = "Onaylandı (Belgeli)" if belgeler else "Onaylandı (Form Verisi)"
            
            yeni_aday = {
                "tc_no": tc_no,
                "ad_soyad": ad_soyad,
                "telefon": telefon,
                "dogum_tarihi": dogum_tarihi,
                "su_anki_is": su_anki_is,
                "calisma_suresi": calisma_suresi,
                "engelli_orani": engelli_orani,
                "vasi_durumu": vasi_durumu,
                "uyelik_turu": "Fahri Üye",
                "adres": adres,
                "durum": durum_metni
            }
            
            # Sınıf üzerinden doğrulama ve kayıt işlemi
            sonuc = st.session_state.ajan_motoru.uye_kaydet(yeni_aday)
            
            if sonuc["durum"] == "Başarılı":
                st.session_state.uye_veritabani.append(yeni_aday)
                st.success(f"✅ {ad_soyad} başarıyla kaydedildi ve DERBİS listesi güncellendi!")
            else:
                st.error(f"❌ Doğrulama Hatası: {sonuc['mesaj']}")
        else:
            st.warning("Lütfen zorunlu alanları (T.C., Ad Soyad, Telefon) eksiksiz doldurun.")

# --- Ana Ekran Görünümü ---
st.subheader("📋 Güncel Fahri Üyelik Havuzu ve DERBİS Hazır Listesi")

if len(st.session_state.uye_veritabani) > 0:
    df_uyeler = pd.DataFrame(st.session_state.uye_veritabani)
    st.dataframe(df_uyeler, use_container_width=True)
    
    col1, col2 = st.columns(2)
    with col1:
        # CSV İndirme Butonu
        csv_veri = df_uyeler.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Üye Listesini İndir (CSV)",
            data=csv_veri,
            file_name="uteykder_fahri_uye_listesi.csv",
            mime="text/csv"
        )
    with col2:
        if os.path.exists(st.session_state.ajan_motoru.excel_file):
            with open(st.session_state.ajan_motoru.excel_file, "rb") as file:
                st.download_button(
                    label="📊 DERBİS Hazır Excel Dosyasını İndir (.xlsx)",
                    data=file,
                    file_name="DERBIS_hazir_liste.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
else:
    st.info("Henüz kayıtlı fahri üye bulunmuyor. Sol menüden yeni üye bilgilerini girerek ajanı çalıştırabilirsin.")