#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Artık Bakiye Dağıtım Sistemi Test Scripti
"""

import os
import json
from datetime import datetime

# Test için örnek üye verileri oluştur
test_uyeler = [
    {
        "Ad": "Ahmet",
        "Soyad": "Yılmaz",
        "TC_Kimlik_No": "12345678901",
        "Dogum_Tarihi": "1955-03-15",  # 71 yaş - hak sahibi
        "Cinsiyet": "Erkek",
        "Telefon": "5551234567",
        "E_Posta": "ahmet@example.com",
        "Ikamet_Adresi": "İstanbul",
        "Il": "İstanbul",
        "Ilce": "Kadıköy",
        "Kayit_Tarihi": "2024-01-01",
        "Uye_Turu": "Emekli",
        "Durum": "Aktif"
    },
    {
        "Ad": "Fatma",
        "Soyad": "Demir",
        "TC_Kimlik_No": "98765432109",
        "Dogum_Tarihi": "1960-07-22",  # 66 yaş - hak sahibi
        "Cinsiyet": "Kadın",
        "Telefon": "5559876543",
        "E_Posta": "fatma@example.com",
        "Ikamet_Adresi": "Ankara",
        "Il": "Ankara",
        "Ilce": "Çankaya",
        "Kayit_Tarihi": "2024-02-01",
        "Uye_Turu": "Emekli",
        "Durum": "Aktif"
    },
    {
        "Ad": "Mehmet",
        "Soyad": "Kaya",
        "TC_Kimlik_No": "45678901234",
        "Dogum_Tarihi": "1980-01-01",  # 46 yaş - hak sahibi değil
        "Cinsiyet": "Erkek",
        "Telefon": "5554567890",
        "E_Posta": "mehmet@example.com",
        "Ikamet_Adresi": "İzmir",
        "Il": "İzmir",
        "Ilce": "Konak",
        "Kayit_Tarihi": "2024-03-01",
        "Uye_Turu": "Standart",
        "Durum": "Aktif"
    },
    {
        "Ad": "Ayşe",
        "Soyad": "Şahin",
        "TC_Kimlik_No": "32109876543",
        "Dogum_Tarihi": "1968-11-30",  # 58 yaş - hak sahibi
        "Cinsiyet": "Kadın",
        "Telefon": "5553210987",
        "E_Posta": "ayse@example.com",
        "Ikamet_Adresi": "Bursa",
        "Il": "Bursa",
        "Ilce": "Nilüfer",
        "Kayit_Tarihi": "2024-04-01",
        "Uye_Turu": "Emekli",
        "Durum": "Aktif"
    }
]

print("Artik Bakiye Dagitim Sistemi Test Baslatiliyor...")
print("=" * 60)

# 1. UTEYKDER veri arşivini test et
print("\n1. UTEYKDER Veri Arsiv Ajan Testi")
print("-" * 60)

from uteykder_veri_arsiv_ajani import UteyKderVeriArsivAjani
uteykder = UteyKderVeriArsivAjani()

# Test üyelerini kaydet
for uye in test_uyeler:
    uye_klasor, excel_dosya = uteykder.uye_kaydet_ve_arsivle(uye)
    print(f"[OK] Uye kaydedildi: {uye['Ad']} {uye['Soyad']}")

# İstatistikleri al
istatistik = uteykder.istatistikleri_getir()
print(f"\n[ISTATISTIK] Toplam Uye: {istatistik['toplam_uye']}")
print(f"[ISTATISTIK] Aktif Uye: {istatistik['aktif_uye']}")
print(f"[ISTATISTIK] Fahri Uye: {istatistik['fahri_uye']}")

# Yaş ve emekli filtreleme testi
print(f"\n[FILTRE] Yas ve Emekli Filtreleme Testi (55+ Emekli):")
filtre_sonuc = uteykder.yas_ve_emekli_filtrele(min_yas=55, sadece_emekli=True)
print(f"[FILTRE] Toplam Uye: {filtre_sonuc['toplam_uye']}")
print(f"[FILTRE] Filtrelenen Uye: {filtre_sonuc['filtrelenen_uye']}")

print(f"\n[HAK SAHIBLERI]:")
for hak_sahibi in filtre_sonuc['liste']:
    print(f"  - {hak_sahibi['Ad']} {hak_sahibi['Soyad']} ({hak_sahibi['hesaplanan_yas']} yas, Emekli: {hak_sahibi['emekli_mi']})")

# 2. Hukuki uyum denetimi testi
print(f"\n2. Hukuki Uyum Denetimi Testi")
print("-" * 60)

from trm_agents.hukuki_uyum_ajani import HukukiUyumAjani
hukuki_ajan = HukukiUyumAjani(agent_id=174)
hukuki_sonuc = hukuki_ajan.hukuki_analiz_yap("Artık Bakiye Dağıtım - 55+ Emekli Paylaşımı")

print(f"[HUKUKI] Denetim Durumu: {hukuki_sonuc['durum']}")
print(f"[HUKUKI] Analiz: {hukuki_sonuc['analiz'][:100]}...")

# 3. Artık bakiye dağıtım simülasyonu
print(f"\n3. Artık Bakiye Dağıtım Simülasyonu")
print("-" * 60)

havuz_bakiyesi = 100000
hak_sahibi_sayisi = filtre_sonuc['filtrelenen_uye']

if hak_sahibi_sayisi > 0:
    kisi_basi_pay = havuz_bakiyesi / hak_sahibi_sayisi
    
    print(f"[DAĞITIM] Havuz Bakiyesi: {havuz_bakiyesi} TL")
    print(f"[DAĞITIM] Hak Sahibi Sayısı: {hak_sahibi_sayisi}")
    print(f"[DAĞITIM] Kisi Basi Pay: {kisi_basi_pay:.2f} TL")
    
    # Dağıtım raporu oluştur
    dagitim_raporu = {
        "dağıtım_tarihi": datetime.now().isoformat(),
        "havuz_bakiyesi": havuz_bakiyesi,
        "hak_sahibi_sayisi": hak_sahibi_sayisi,
        "kisi_basi_pay": round(kisi_basi_pay, 2),
        "kriterler": {
            "min_yas": 55,
            "sadece_emekli": True
        },
        "hak_sahipleri": filtre_sonuc['liste'],
        "hukuki_denetim": hukuki_sonuc
    }
    
    # Şeffaflık kaydı
    seffaflik_dosyasi = "data/kamu_denetim_seffaflik_raporlari/artik_bakiye_dagitim_loglari.json"
    os.makedirs(os.path.dirname(seffaflik_dosyasi), exist_ok=True)
    
    with open(seffaflik_dosyasi, "a", encoding="utf-8") as f:
        json.dump(dagitim_raporu, f, ensure_ascii=False, indent=4)
        f.write("\n")
    
    print(f"[SEFFAFLIK] Dagitim raporu seffaflik arsivine kaydedildi: {seffaflik_dosyasi}")
else:
    print("[UYARI] Hak sahibi bulunamadi. Dagitim yapilamadi.")

print("\n" + "=" * 60)
print("[TAMAMLANDI] Test Tamamlandi!")
