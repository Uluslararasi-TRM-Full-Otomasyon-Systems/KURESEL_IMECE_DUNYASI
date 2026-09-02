#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Sosyal İmece Bağımsız Üye Havuzu Sistemi
Bu sistem UTEYKDER derneğinden tamamen bağımsız, Sosyal İmece otonom ekosisteminin
kendi üye yönetim ve filtreleme sistemidir. Mali işlemler ve dağıtımlar bu havuz üzerinden yapılır.
"""
import os
import json
from datetime import datetime
from typing import Dict, List, Any, Optional


class SosyalImeceUyeHavuzu:
    def __init__(self):
        self.ana_klasor = "data/sosyal_imece_uye_havuzu"
        self.json_arsiv = os.path.join(self.ana_klasor, "sosyal_imece_uye_arsivi.json")
        
        if not os.path.exists(self.ana_klasor):
            os.makedirs(self.ana_klasor)
        
        self.arsiv_kontrol()

    def arsiv_kontrol(self):
        if not os.path.exists(self.json_arsiv):
            with open(self.json_arsiv, "w", encoding="utf-8") as f:
                json.dump([], f, ensure_ascii=False, indent=4)

    def uye_kaydet(self, uye_bilgileri: Dict[str, Any]) -> Dict[str, Any]:
        """
        Sosyal İmece otonom ekosistemine üye kaydeder.
        
        uye_bilgileri sözlüğü şu alanları içermelidir:
        Ad, Soyad, Dogum_Tarihi, Cinsiyet, Telefon, E_Posta, 
        Il, Ilce, Kayit_Tarihi, Uye_Turu, Durum
        """
        ad = uye_bilgileri.get("Ad", "Adsiz")
        soyad = uye_bilgileri.get("Soyad", "Soyadsiz")
        uye_id = f"{ad}_{soyad}_{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        uye_bilgileri["uye_id"] = uye_id
        uye_bilgileri["kayit_kaynagi"] = "Sosyal_Imece_Otonom_Ekosistem"
        uye_bilgileri["kayit_tarihi"] = datetime.now().isoformat()
        
        try:
            with open(self.json_arsiv, "r", encoding="utf-8") as f:
                uyeler = json.load(f)
        except:
            uyeler = []
        
        uyeler.append(uye_bilgileri)
        
        with open(self.json_arsiv, "w", encoding="utf-8") as f:
            json.dump(uyeler, f, ensure_ascii=False, indent=4)
        
        return {
            "durum": "basarili",
            "uye_id": uye_id,
            "mesaj": f"{ad} {soyad} Sosyal İmece otonom ekosistemine kaydedildi"
        }

    def yas_ve_emekli_filtrele(self, min_yas: int = 55, sadece_emekli: bool = True) -> Dict[str, Any]:
        """
        Sosyal İmece otonom üye havuzunda yaş ve emeklilik kriterlerine göre filtreleme yapar.
        
        Args:
            min_yas: Minimum yaş (varsayılan: 55)
            sadece_emekli: Sadece emeklileri filtrele (varsayılan: True)
        
        Returns:
            Filtrelenmiş üye listesi
        """
        try:
            with open(self.json_arsiv, "r", encoding="utf-8") as f:
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
            "liste": filtrelenen_uyeler,
            "kaynak": "Sosyal_Imece_Otonom_Ekosistem"
        }

    def istatistikleri_getir(self) -> Dict[str, Any]:
        try:
            with open(self.json_arsiv, "r", encoding="utf-8") as f:
                uyeler = json.load(f)
        except:
            uyeler = []
        
        toplam = len(uyeler)
        aktif = sum(1 for u in uyeler if u.get("Durum") == "Aktif")
        fahri = sum(1 for u in uyeler if u.get("Uye_Turu") == "Fahri")
        emekli = sum(1 for u in uyeler if "emekli" in u.get("Uye_Turu", "").lower())
        
        return {
            "toplam_uye": toplam,
            "aktif_uye": aktif,
            "fahri_uye": fahri,
            "emekli_uye": emekli,
            "liste": uyeler,
            "kaynak": "Sosyal_Imece_Otonom_Ekosistem"
        }

    def uye_ara(self, tc_kimlik_no: str = None, ad: str = None, soyad: str = None) -> List[Dict[str, Any]]:
        try:
            with open(self.json_arsiv, "r", encoding="utf-8") as f:
                uyeler = json.load(f)
        except:
            uyeler = []
        
        sonuc = []
        for uye in uyeler:
            eslesme = True
            if tc_kimlik_no and uye.get("TC_Kimlik_No") != tc_kimlik_no:
                eslesme = False
            if ad and uye.get("Ad") != ad:
                eslesme = False
            if soyad and uye.get("Soyad") != soyad:
                eslesme = False
            
            if eslesme:
                sonuc.append(uye)
        
        return sonuc


if __name__ == "__main__":
    print("Sosyal İmece Bağımsız Üye Havuzu Test Başlatılıyor...")
    print("=" * 60)
    
    havuz = SosyalImeceUyeHavuzu()
    
    # Test üyeleri
    test_uyeler = [
        {
            "Ad": "Ahmet",
            "Soyad": "Yılmaz",
            "Dogum_Tarihi": "1955-03-15",
            "Cinsiyet": "Erkek",
            "Telefon": "5551234567",
            "E_Posta": "ahmet@example.com",
            "Il": "İstanbul",
            "Ilce": "Kadıköy",
            "Uye_Turu": "Emekli",
            "Durum": "Aktif"
        },
        {
            "Ad": "Fatma",
            "Soyad": "Demir",
            "Dogum_Tarihi": "1960-07-22",
            "Cinsiyet": "Kadın",
            "Telefon": "5559876543",
            "E_Posta": "fatma@example.com",
            "Il": "Ankara",
            "Ilce": "Çankaya",
            "Uye_Turu": "Emekli",
            "Durum": "Aktif"
        },
        {
            "Ad": "Mehmet",
            "Soyad": "Kaya",
            "Dogum_Tarihi": "1980-01-01",
            "Cinsiyet": "Erkek",
            "Telefon": "5554567890",
            "E_Posta": "mehmet@example.com",
            "Il": "İzmir",
            "Ilce": "Konak",
            "Uye_Turu": "Standart",
            "Durum": "Aktif"
        }
    ]
    
    print("\n[TEST] Üye Kayıtları:")
    for uye in test_uyeler:
        sonuc = havuz.uye_kaydet(uye)
        print(f"  - {sonuc['mesaj']}")
    
    print(f"\n[ISTATISTIK] {havuz.istatistikleri_getir()}")
    
    print(f"\n[FILTRE] 55+ Emekli Filtreleme:")
    filtre_sonuc = havuz.yas_ve_emekli_filtrele(min_yas=55, sadece_emekli=True)
    print(f"  Toplam Üye: {filtre_sonuc['toplam_uye']}")
    print(f"  Filtrelenen Üye: {filtre_sonuc['filtrelenen_uye']}")
    print(f"  Kaynak: {filtre_sonuc['kaynak']}")
    
    print("\n" + "=" * 60)
    print("[TAMAMLANDI] Test Tamamlandı!")
