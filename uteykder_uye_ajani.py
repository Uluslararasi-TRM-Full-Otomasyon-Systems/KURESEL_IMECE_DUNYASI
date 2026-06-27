# -*- coding: utf-8 -*-
"""
UTEYKDER Otonom Üye Kabul ve Ön Kayıt Ajanı (Fahri Üye Yapılanması)
"""
import os
import json
import pandas as pd
from datetime import datetime

class UteykderUyeAjani:
    def __init__(self):
        self.output_file = "uteykder_fahri_uyeler.json"
        self.excel_file = "DERBIS_hazir_liste.xlsx"
        
        # 🎯 İLERİDE AKLINIZA GELEN KIRINTI SORULARI DOĞRUDAN BU LİSTEYE EKLEYEBİLİRSİNİZ!
        self.dinamik_sorular = [
            {"id": "tc_no", "soru_metni": "Lütfen 11 haneli T.C. Kimlik numaranızı giriniz veya söyleyiniz:"},
            {"id": "ad_soyad", "soru_metni": "Adınız ve Soyadınız nedir?"},
            {"id": "telefon", "soru_metni": "Telefon numaranızı başında sıfır olmadan giriniz:"},
            {"id": "dogum_tarihi", "soru_metni": "Doğum tarihinizi gün-ay-yıl olarak belirtiniz:"},
            {"id": "meslek", "soru_metni": "Mesleğiniz veya uzmanlık alanınız nedir?"},
            # --- UTEYKDER Özel Soruları ---
            {"id": "proje_tercihi", "soru_metni": "UTEYKDER projelerinden (Sağlık, İşitme Engelliler, Kapıda Alışveriş) hangisinde görev almak istersiniz?"},
            {"id": "kan_grubu", "soru_metni": "Kan grubunuz nedir?"}
            # 📝 Yeni bir soru geldiğinde virgül koyup altına eklemeniz yeterli olacaktır.
        ]

    def veri_dogrula(self, veri):
        """Toplanan verilerin DERBİS standartlarına uygunluğunu ve T.C. kontrolünü yapar."""
        if "tc_no" in veri and len(str(veri["tc_no"])) != 11:
            return False, "Hatalı T.C. Kimlik Numarası!"
        return True, "Doğrulama Başarılı."

    def uye_kaydet(self, aday_bilgileri):
        """Aday bilgilerini doğrular, JSON tabanına yazar ve DERBİS Excel şablonunu günceller."""
        dogru_mu, mesaj = self.veri_dogrula(aday_bilgileri)
        if not dogru_mu:
            return {"durum": "Hata", "mesaj": mesaj}
            
        aday_bilgileri["kayit_tarihi"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        aday_bilgileri["uyelik_turu"] = "Fahri Üye"
        
        # JSON Dosyasına Yazma (Yedekleme)
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
            
        # DERBİS İçin Excel Çıktısı Üretme
        df = pd.DataFrame(mevcut_veriler)
        df.to_excel(self.excel_file, index=False)
        
        return {"durum": "Başarılı", "mesaj": "Kayıt alındı, DERBİS Excel listesi güncellendi!"}

    def sesli_asistan_dinle(self):
        """
        Mikrofonu açıp adayı dinleyen ve sesi metne çeviren metod taslağı.
        Gelişmiş sesli komut altyapınız buraya entegre edilecek.
        """
        # Gelecek aşamada ses tanıma kütüphaneleriyle doldurulacak
        pass

if __name__ == "__main__":
    ajan = UteykderUyeAjani()
    print("UTEYKDER Üye Kabul Ajanı Başlatıldı. Soru Sayısı:", len(ajan.dinamik_sorular))
