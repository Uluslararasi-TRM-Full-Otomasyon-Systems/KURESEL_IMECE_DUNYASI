# -*- coding: utf-8 -*-
"""
UTEYKDER Otonom Uye Kabul ve On Kayit Ajani (Fahri Uye Yapilanmasi)
"""
import os
import json
import pandas as pd
from datetime import datetime

class UteykderUyeAjani:
    def __init__(self):
        self.output_file = "uteykder_fahri_uyeler.json"
        self.excel_file = "DERBIS_hazir_liste.xlsx"
        
        # 🎯 ILERIDE AKLINIZA GELEN KIRINTI SORULARI DOGRUDAN BU LISTEYE EKLEYEBILIRSINIZ!
        self.dinamik_sorular = [
            {"id": "tc_no", "soru_metni": "Lutfen 11 haneli T.C. Kimlik numaranizi giriniz veya soyleyiniz:"},
            {"id": "ad_soyad", "soru_metni": "Adiniz ve Soyadiniz nedir?"},
            {"id": "telefon", "soru_metni": "Telefon numaranizi basinda sifir olmadan giriniz:"},
            {"id": "dogum_tarihi", "soru_metni": "Dogum tarihinizi gun-ay-yil olarak belirtiniz:"},
            {"id": "meslek", "soru_metni": "Mesleginiz veya uzmanlik alaniniz nedir?"},
            # --- UTEYKDER Ozel Sorulari ---
            {"id": "proje_tercihi", "soru_metni": "UTEYKDER projelerinden (Saglik, Isitme Engelliler, Kapida Alisveris) hangisinde gorev almak istersiniz?"},
            {"id": "kan_grubu", "soru_metni": "Kan grubunuz nedir?"}
            # 📝 Yeni bir soru geldiginde virgul koyup altina eklemeniz yeterli olacaktir.
        ]

    def veri_dogrula(self, veri):
        """Toplanan verilerin DERBIS standartlarina uygunlugunu ve T.C. kontrolunu yapar."""
        if "tc_no" in veri and len(str(veri["tc_no"])) != 11:
            return False, "Hatali T.C. Kimlik Numarasi!"
        return True, "Dogrulama Basarili."

    def uye_kaydet(self, aday_bilgileri):
        """Aday bilgilerini dogrular, JSON tabanina yazar ve DERBIS Excel sablonunu gunceller."""
        dogru_mu, mesaj = self.veri_dogrula(aday_bilgileri)
        if not dogru_mu:
            return {"durum": "Hata", "mesaj": mesaj}
            
        aday_bilgileri["kayit_tarihi"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        aday_bilgileri["uyelik_turu"] = "Fahri Uye"
        
        # JSON Dosyasina Yazma (Yedekleme)
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
            
        # DERBIS Icin Excel Ciktisi Uretme
        df = pd.DataFrame(mevcut_veriler)
        df.to_excel(self.excel_file, index=False)
        
        return {"durum": "Basarili", "mesaj": "Kayit alindi, DERBIS Excel listesi guncellendi!"}

    def sesli_asistan_dinle(self):
        """
        Mikrofonu acip adayi dinleyen ve sesi metne ceviren metod taslagi.
        Gelismis sesli komut altyapiniz buraya entegre edilecek.
        """
        # Gelecek asamada ses tanima kutuphaneleriyle doldurulacak
        pass

if __name__ == "__main__":
    ajan = UteykderUyeAjani()
    print("UTEYKDER Uye Kabul Ajani Baslatildi. Soru Sayisi:", len(ajan.dinamik_sorular))
