#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Sosyal İmece İki Adımlı Dağıtım Algoritması
UTEYKDER'den tamamen bağımsız, Sosyal İmece otonom ekosistemi içinde çalışır
"""

import os
import json
from datetime import datetime
from typing import Dict, List, Any, Optional
from collections import defaultdict


class SosyalImeceDagitimAlgoritmasi:
    def __init__(self):
        # Yoksulluk sınırı (il bazlı - örnek değerler)
        self.yoksulluk_siniri_il_bazli = {
            "istanbul": 15000,
            "ankara": 14000,
            "izmir": 13500,
            "bursa": 12000,
            "antalya": 12500,
            "konya": 11000,
            "adana": 11500,
            "gaziantep": 11000,
            "diğer": 10000  # Varsayılan değer
        }
        
        # İmece Refah Payı oranı
        self.imece_refah_pay_orani = 0.20  # %20
        
        # Bağımsız üye havuzu
        from sosyal_imece_uye_havuzu import SosyalImeceUyeHavuzu
        self.uye_havuzu = SosyalImeceUyeHavuzu()
        
        # Şeffaflık arşivi
        self.seffaflik_dosyasi = "data/sosyal_imece_seffaflik_raporlari/iki_adimli_dagitim_loglari.json"
        os.makedirs(os.path.dirname(self.seffaflik_dosyasi), exist_ok=True)
    
    def il_bazli_yoksulluk_siniri_getir(self, il: str) -> float:
        """İl bazlı yoksulluk sınırını döndürür"""
        il_lower = il.lower() if il else ""
        return self.yoksulluk_siniri_il_bazli.get(il_lower, self.yoksulluk_siniri_il_bazli["diğer"])
    
    def birinci_adim_tum_katilimci_payi(self, toplam_havuz: float) -> Dict[str, Any]:
        """
        Birinci Adım: Tüm katılımcıların il bazlı payı
        Havuzdaki toplam para, tüm katılımcılar arasında il bazlı olarak
        'yoksulluk sınırı + %20 İmece Refah Payı' eklenerek paylaştırılır.
        """
        # Tüm katılımcıları al
        istatistik = self.uye_havuzu.istatistikleri_getir()
        tum_katilimcilar = istatistik["liste"]
        
        if not tum_katilimcilar:
            return {
                "durum": "hata",
                "mesaj": "Sistemde kayıtlı katılımcı bulunamadı",
                "adim": 1
            }
        
        # İl bazlı gruplama
        il_bazli_katilimcilar = defaultdict(list)
        for katilimci in tum_katilimcilar:
            il = katilimci.get("Il", "Diğer")
            il_bazli_katilimcilar[il].append(katilimci)
        
        # Her il için pay hesaplama
        dagitim_detaylari = []
        toplam_birinci_adim_odeme = 0
        
        for il, katilimcilar in il_bazli_katilimcilar.items():
            yoksulluk_siniri = self.il_bazli_yoksulluk_siniri_getir(il)
            imece_refah_payi = yoksulluk_siniri * self.imece_refah_pay_orani
            kisi_basi_pay = yoksulluk_siniri + imece_refah_payi
            
            il_toplam_odeme = kisi_basi_pay * len(katilimcilar)
            toplam_birinci_adim_odeme += il_toplam_odeme
            
            il_detay = {
                "il": il,
                "katilimci_sayisi": len(katilimcilar),
                "yoksulluk_siniri": yoksulluk_siniri,
                "imece_refah_pay_orani": f"%{self.imece_refah_pay_orani * 100}",
                "imece_refah_pay_tutar": imece_refah_payi,
                "kisi_basi_pay": kisi_basi_pay,
                "il_toplam_odeme": il_toplam_odeme,
                "katilimcilar": [
                    {
                        "uye_id": k.get("uye_id"),
                        "ad_soyad": f"{k.get('Ad')} {k.get('Soyad')}",
                        "odeme_tutari": kisi_basi_pay
                    }
                    for k in katilimcilar
                ]
            }
            
            dagitim_detaylari.append(il_detay)
        
        # Havuz kontrolü
        if toplam_birinci_adim_odeme > toplam_havuz:
            return {
                "durum": "uyari",
                "mesaj": "Havuz bakiyesi birinci adım ödemelerini karşılamaya yetmiyor",
                "toplam_havuz": toplam_havuz,
                "gereken_odeme": toplam_birinci_adim_odeme,
                "eksik": toplam_birinci_adim_odeme - toplam_havuz,
                "adim": 1
            }
        
        artik_bakiye = toplam_havuz - toplam_birinci_adim_odeme
        
        sonuc = {
            "durum": "basarili",
            "adim": 1,
            "adim_adi": "Tüm Katılımcıların İl Bazlı Payı",
            "toplam_havuz": toplam_havuz,
            "toplam_katilimci_sayisi": len(tum_katilimcilar),
            "toplam_birinci_adim_odeme": toplam_birinci_adim_odeme,
            "artik_bakiye": artik_bakiye,
            "il_bazli_dagitim": dagitim_detaylari,
            "sistem_kaynagi": "Sosyal_Imece_Otonom_Ekosistem",
            "mali_bagimsizlik": "UTEYKDER_dernek_butccesinden_bagimsiz"
        }
        
        return sonuc
    
    def ikinci_adim_emekli_payi(self, artik_bakiye: float) -> Dict[str, Any]:
        """
        İkinci Adım: 55+ Emekli Payı
        Birinci adımdan sonra kalan artık bakiye, 55 yaş ve üzeri tüm emeklilere
        eşit miktarda dağıtılır.
        """
        # 55+ emekli filtreleme
        filtre_sonuc = self.uye_havuzu.yas_ve_emekli_filtrele(min_yas=55, sadece_emekli=True)
        emekliler = filtre_sonuc["liste"]
        
        if not emekliler:
            return {
                "durum": "uyari",
                "mesaj": "55 yaş ve üzeri emekli bulunamadı",
                "artik_bakiye": artik_bakiye,
                "adim": 2
            }
        
        if artik_bakiye <= 0:
            return {
                "durum": "bilgi",
                "mesaj": "Dağıtılacak artık bakiye kalmadı",
                "artik_bakiye": artik_bakiye,
                "adim": 2
            }
        
        emekli_sayisi = len(emekliler)
        kisi_basi_pay = artik_bakiye / emekli_sayisi
        
        emekli_dagitim_detaylari = [
            {
                "uye_id": e.get("uye_id"),
                "ad_soyad": f"{e.get('Ad')} {e.get('Soyad')}",
                "yas": e.get("hesaplanan_yas"),
                "odeme_tutari": kisi_basi_pay
            }
            for e in emekliler
        ]
        
        sonuc = {
            "durum": "basarili",
            "adim": 2,
            "adim_adi": "55+ Emekli Artık Bakiye Dağıtımı",
            "artik_bakiye": artik_bakiye,
            "emekli_sayisi": emekli_sayisi,
            "kisi_basi_pay": round(kisi_basi_pay, 2),
            "emekli_dagitim": emekli_dagitim_detaylari,
            "sistem_kaynagi": "Sosyal_Imece_Otonom_Ekosistem",
            "mali_bagimsizlik": "UTEYKDER_dernek_butccesinden_bagimsiz"
        }
        
        return sonuc
    
    def iki_adimli_dagitim(self, toplam_havuz: float) -> Dict[str, Any]:
        """
        İki adımlı dağıtım algoritmasını tam olarak çalıştırır.
        """
        # Hukuki uyum denetimi
        from trm_agents.hukuki_uyum_ajani import HukukiUyumAjani
        hukuki_ajan = HukukiUyumAjani(agent_id=174)
        hukuki_sonuc = hukuki_ajan.hukuki_analiz_yap("İki Adımlı Sosyal İmece Dağıtım")
        
        # Birinci adım
        birinci_adim_sonuc = self.birinci_adim_tum_katilimci_payi(toplam_havuz)
        
        if birinci_adim_sonuc["durum"] != "basarili":
            return {
                "genel_durum": "hata",
                "hukuki_denetim": hukuki_sonuc,
                "birinci_adim": birinci_adim_sonuc,
                "ikinci_adim": None
            }
        
        artik_bakiye = birinci_adim_sonuc["artik_bakiye"]
        
        # İkinci adım
        ikinci_adim_sonuc = self.ikinci_adim_emekli_payi(artik_bakiye)
        
        tam_rapor = {
            "dağıtım_tarihi": datetime.now().isoformat(),
            "genel_durum": "tamamlandi",
            "hukuki_denetim": hukuki_sonuc,
            "toplam_havuz": toplam_havuz,
            "birinci_adim": birinci_adim_sonuc,
            "ikinci_adim": ikinci_adim_sonuc,
            "toplam_dagitilan": birinci_adim_sonuc["toplam_birinci_adim_odeme"] + (
                ikinci_adim_sonuc.get("artik_bakiye", 0) if ikinci_adim_sonuc["durum"] == "basarili" else 0
            ),
            "sistem_kaynagi": "Sosyal_Imece_Otonom_Ekosistem",
            "mali_bagimsizlik": "UTEYKDER_dernek_butccesinden_bagimsiz",
            "algoritma_turu": "Iki_Adimli_Dagitim",
            "aciklama": "1. Adım: Tüm katılımcıların il bazlı payı (yoksulluk sınırı + %20 İmece Refah Payı). 2. Adım: 55+ emekli artık bakiye dağıtımı."
        }
        
        # Şeffaflık kaydı
        with open(self.seffaflik_dosyasi, "a", encoding="utf-8") as f:
            json.dump(tam_rapor, f, ensure_ascii=False, indent=4)
            f.write("\n")
        
        return tam_rapor


if __name__ == "__main__":
    print("Sosyal İmece İki Adımlı Dağıtım Algoritması Test Başlatılıyor...")
    print("=" * 60)
    
    # Test için üye havuzuna örnek veriler ekle
    from sosyal_imece_uye_havuzu import SosyalImeceUyeHavuzu
    havuz = SosyalImeceUyeHavuzu()
    
    test_uyeler = [
        {"Ad": "Ahmet", "Soyad": "Yılmaz", "Dogum_Tarihi": "1955-03-15", "Cinsiyet": "Erkek", "Telefon": "5551234567", "E_Posta": "ahmet@example.com", "Il": "İstanbul", "Ilce": "Kadıköy", "Uye_Turu": "Emekli", "Durum": "Aktif"},
        {"Ad": "Fatma", "Soyad": "Demir", "Dogum_Tarihi": "1960-07-22", "Cinsiyet": "Kadın", "Telefon": "5559876543", "E_Posta": "fatma@example.com", "Il": "Ankara", "Ilce": "Çankaya", "Uye_Turu": "Emekli", "Durum": "Aktif"},
        {"Ad": "Mehmet", "Soyad": "Kaya", "Dogum_Tarihi": "1980-01-151", "Cinsiyet": "Erkek", "Telefon": "5554567890", "E_Posta": "mehmet@example.com", "Il": "İstanbul", "Ilce": "Beşiktaş", "Uye_Turu": "Standart", "Durum": "Aktif"},
        {"Ad": "Ayşe", "Soyad": "Şahin", "Dogum_Tarihi": "1990-05-10", "Cinsiyet": "Kadın", "Telefon": "5553210987", "E_Posta": "ayse@example.com", "Il": "İzmir", "Ilce": "Konak", "Uye_Turu": "Standart", "Durum": "Aktif"},
        {"Ad": "Ali", "Soyad": "Çelik", "Dogum_Tarihi": "1975-08-20", "Cinsiyet": "Erkek", "Telefon": "5556543210", "E_Posta": "ali@example.com", "Il": "Bursa", "Ilce": "Nilüfer", "Uye_Turu": "Standart", "Durum": "Aktif"}
    ]
    
    print("\n[TEST] Uye Kayıtları:")
    for uye in test_uyeler:
        sonuc = havuz.uye_kaydet(uye)
        print(f"  - {sonuc['mesaj']}")
    
    # İki adımlı dağıtım testi
    print(f"\n[TEST] İki Adımlı Dağıtım Testi:")
    print("-" * 60)
    
    algoritma = SosyalImeceDagitimAlgoritmasi()
    toplam_havuz = 200000  # 200.000 TL
    
    sonuc = algoritma.iki_adimli_dagitim(toplam_havuz)
    
    print(f"[DAGITIM] Genel Durum: {sonuc['genel_durum']}")
    print(f"[DAGITIM] Toplam Havuz: {sonuc['toplam_havuz']} TL")
    print(f"[DAGITIM] Toplam Dağıtılan: {sonuc['toplam_dagitilan']} TL")
    
    print(f"\n[BIRINCI ADIM] {sonuc['birinci_adim']['adim_adi']}:")
    print(f"  Toplam Katılımcı: {sonuc['birinci_adim']['toplam_katilimci_sayisi']}")
    print(f"  Toplam Ödeme: {sonuc['birinci_adim']['toplam_birinci_adim_odeme']} TL")
    print(f"  Artık Bakiye: {sonuc['birinci_adim']['artik_bakiye']} TL")
    
    for il_detay in sonuc['birinci_adim']['il_bazli_dagitim']:
        print(f"  - {il_detay['il']}: {il_detay['katilimci_sayisi']} kişi, Kişi Başı: {il_detay['kisi_basi_pay']} TL")
    
    print(f"\n[IKINCI ADIM] {sonuc['ikinci_adim']['adim_adi']}:")
    if sonuc['ikinci_adim']['durum'] == 'basarili':
        print(f"  Emekli Sayısı: {sonuc['ikinci_adim']['emekli_sayisi']}")
        print(f"  Dağıtılan Bakiye: {sonuc['ikinci_adim']['artik_bakiye']} TL")
        print(f"  Kişi Başı: {sonuc['ikinci_adim']['kisi_basi_pay']} TL")
    else:
        print(f"  Durum: {sonuc['ikinci_adim']['durum']}")
        print(f"  Mesaj: {sonuc['ikinci_adim']['mesaj']}")
    
    print(f"\n[BAGIMSIZLIK] Sistem Kaynağı: {sonuc['sistem_kaynagi']}")
    print(f"[BAGIMSIZLIK] Mali Bağımsızlık: {sonuc['mali_bagimsizlik']}")
    
    print("\n" + "=" * 60)
    print("[TAMAMLANDI] Test Tamamlandı!")
