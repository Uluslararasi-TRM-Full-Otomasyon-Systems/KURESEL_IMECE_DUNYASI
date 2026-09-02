# -*- coding: utf-8 -*-
"""
UTEYKDER Veri Arşiv ve Fahri Üye Düzenleme Ajanı
Sistemdeki üyelerin kimlik, ikametgah, telefon ve vesikalık vesika/bilgilerini
DERBİS standartlarına uygun olarak Ad_Soyad_TC formatında arşivler ve listeler.
"""
import os
import json
import pandas as pd
from datetime import datetime

class UteyKderVeriArsivAjani:
    def __init__(self):
        self.ana_klasor = "UTEYKDER_UYE_BELGELER"
        self.json_arsiv = "uteykder_uye_arsivi.json"
        self.excel_arsiv = "UTYKDER_DERBIS_FAHRI_UYE_LISTESI.xlsx"
        
        if not os.path.exists(self.ana_klasor):
            os.makedirs(self.ana_klasor)

    def uye_kaydet_ve_arsivle(self, uye_bilgileri):
        """
        uye_bilgileri sözlüğü şu alanları içermelidir:
        Ad, Soyad, TC_Kimlik_No, Dogum_Tarihi, Cinsiyet, Telefon, 
        E_Posta, Ikamet_Adresi, Il, Ilce, Kayit_Tarihi, Uye_Turu, Durum
        """
        ad = uye_bilgileri.get("Ad", "Adsiz")
        soyad = uye_bilgileri.get("Soyad", "Soyadsiz")
        tc = uye_bilgileri.get("TC_Kimlik_No", "00000000000")
        
        # Kişiye özel alt klasör oluşturma: Ad_Soyad_TC
        uye_klasor_adi = f"{ad}_{soyad}_{tc}"
        uye_klasor_yolu = os.path.join(self.ana_klasor, uye_klasor_adi)
        
        if not os.path.exists(uye_klasor_yolu):
            os.makedirs(uye_klasor_yolu)
            
        # Üye detaylarını JSON olarak alt klasöre kaydetme
        uye_dosya_yolu = os.path.join(uye_klasor_yolu, "uye_bilgi.json")
        with open(uye_dosya_yolu, 'w', encoding='utf-8') as f:
            json.dump(uye_bilgileri, f, ensure_ascii=False, indent=4)
            
        # Genel JSON arşivine ekleme
        mevcut_uyeler = []
        if os.path.exists(self.json_arsiv):
            try:
                with open(self.json_arsiv, 'r', encoding='utf-8') as f:
                    mevcut_uyeler = json.load(f)
            except:
                mevcut_uyeler = []
                
        # Aynı TC ile kayıt varsa güncelle, yoksa ekle
        mevcut_uyeler = [u for u in mevcut_uyeler if u.get("TC_Kimlik_No") != tc]
        mevcut_uyeler.append(uye_bilgileri)
        
        with open(self.json_arsiv, 'w', encoding='utf-8') as f:
            json.dump(mevcut_uyeler, f, ensure_ascii=False, indent=4)
            
        # DERBİS Formatında Excel Raporu Güncelleme
        df = pd.DataFrame(mevcut_uyeler)
        df.to_excel(self.excel_arsiv, index=False)
        
        return uye_klasor_yolu, self.excel_arsiv

    def istatistikleri_getir(self):
        if not os.path.exists(self.json_arsiv):
            return {"toplam_uye": 0, "aktif_uye": 0, "fahri_uye": 0, "liste": []}
            
        try:
            with open(self.json_arsiv, 'r', encoding='utf-8') as f:
                uyeler = json.load(f)
        except:
            uyeler = []
            
        toplam = len(uyeler)
        aktif = sum(1 for u in uyeler if u.get("Durum") == "Aktif")
        fahri = sum(1 for u in uyeler if u.get("Uye_Turu") == "Fahri")
        
        return {
            "toplam_uye": toplam,
            "aktif_uye": aktif,
            "fahri_uye": fahri,
            "liste": uyeler
        }
    
    def yas_ve_emekli_filtrele(self, min_yas: int = 55, sadece_emekli: bool = True):
        """
        Belirtilen yaş ve emeklilik kriterlerine göre üyeleri filtreler.
        
        Args:
            min_yas: Minimum yaş (varsayılan: 55)
            sadece_emekli: Sadece emeklileri filtrele (varsayılan: True)
        
        Returns:
            Filtrelenmiş üye listesi
        """
        if not os.path.exists(self.json_arsiv):
            return {"toplam_uye": 0, "filtrelenen_uye": 0, "liste": []}
            
        try:
            with open(self.json_arsiv, 'r', encoding='utf-8') as f:
                uyeler = json.load(f)
        except:
            uyeler = []
        
        filtrelenen_uyeler = []
        simdiki_yil = datetime.now().year
        
        for uye in uyeler:
            # Yaş hesaplama
            dogum_tarihi = uye.get("Dogum_Tarihi", "")
            yas = 0
            
            if dogum_tarihi:
                try:
                    # Tarih formatı: YYYY-MM-DD veya DD/MM/YYYY
                    if "-" in dogum_tarihi:
                        dogum_yili = int(dogum_tarihi.split("-")[0])
                    elif "/" in dogum_tarihi:
                        dogum_yili = int(dogum_tarihi.split("/")[-1])
                    else:
                        dogum_yili = int(dogum_tarihi[:4])
                    
                    yas = simdiki_yil - dogum_yili
                except:
                    continue
            
            # Emeklilik statüsü kontrolü
            uye_turu = uye.get("Uye_Turu", "")
            emekli_mi = "emekli" in uye_turu.lower() or uye_turu == "Emekli"
            
            # Kriter kontrolü
            yas_kriteri = yas >= min_yas
            emekli_kriteri = not sadece_emekli or emekli_mi
            
            if yas_kriteri and emekli_kriteri:
                filtrelenen_uyeler.append({
                    **uye,
                    "hesaplanan_yas": yas,
                    "emekli_mi": emekli_mi
                })
        
        return {
            "toplam_uye": len(uyeler),
            "filtrelenen_uye": len(filtrelenen_uyeler),
            "min_yas": min_yas,
            "sadece_emekli": sadece_emekli,
            "liste": filtrelenen_uyeler
        }