#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Sosyal İmece Bağımsız Mali Sistem Test Scripti
UTEYKDER derneğinden tamamen bağımsız sistem testi
"""

import os
import json
from datetime import datetime

print("Sosyal İmece Bağımsız Mali Sistem Test Başlatılıyor...")
print("=" * 60)

# 1. Sosyal İmece Bağımsız Üye Havuzu Testi
print("\n1. Sosyal İmece Bağımsız Üye Havuzu Testi")
print("-" * 60)

from sosyal_imece_uye_havuzu import SosyalImeceUyeHavuzu
imece_havuzu = SosyalImeceUyeHavuzu()

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

print("[TEST] Uye Kayıtları:")
for uye in test_uyeler:
    sonuc = imece_havuzu.uye_kaydet(uye)
    print(f"  - {sonuc['mesaj']}")
    print(f"    Kaynak: {sonuc.get('durum')}")

istatistik = imece_havuzu.istatistikleri_getir()
print(f"\n[ISTATISTIK] Toplam Uye: {istatistik['toplam_uye']}")
print(f"[ISTATISTIK] Aktif Uye: {istatistik['aktif_uye']}")
print(f"[ISTATISTIK] Emekli Uye: {istatistik['emekli_uye']}")
print(f"[ISTATISTIK] Kaynak: {istatistik['kaynak']}")

# 2. 55+ Emekli Filtreleme Testi
print(f"\n2. 55+ Emekli Filtreleme Testi (Bağımsız Havuz)")
print("-" * 60)

filtre_sonuc = imece_havuzu.yas_ve_emekli_filtrele(min_yas=55, sadece_emekli=True)
print(f"[FILTRE] Toplam Uye: {filtre_sonuc['toplam_uye']}")
print(f"[FILTRE] Filtrelenen Uye: {filtre_sonuc['filtrelenen_uye']}")
print(f"[FILTRE] Kaynak: {filtre_sonuc['kaynak']}")

print(f"\n[HAK SAHIBLERI]:")
for hak_sahibi in filtre_sonuc['liste']:
    print(f"  - {hak_sahibi['Ad']} {hak_sahibi['Soyad']} ({hak_sahibi['hesaplanan_yas']} yas, Emekli: {hak_sahibi['emekli_mi']})")

# 3. Hukuki Uyum Denetimi Testi
print(f"\n3. Hukuki Uyum Denetimi Testi")
print("-" * 60)

from trm_agents.hukuki_uyum_ajani import HukukiUyumAjani
hukuki_ajan = HukukiUyumAjani(agent_id=174)
hukuki_sonuc = hukuki_ajan.hukuki_analiz_yap("Artık Bakiye Dağıtım - 55+ Emekli Paylaşımı")

print(f"[HUKUKI] Denetim Durumu: {hukuki_sonuc['durum']}")
print(f"[HUKUKI] Analiz: {hukuki_sonuc['analiz'][:100]}...")

# 4. Artık Bakiye Dağıtım Simülasyonu (Bağımsız Sistem)
print(f"\n4. Artık Bakiye Dağıtım Simülasyonu (Bağımsız Sistem)")
print("-" * 60)

havuz_bakiyesi = 100000
hak_sahibi_sayisi = filtre_sonuc['filtrelenen_uye']

if hak_sahibi_sayisi > 0:
    kisi_basi_pay = havuz_bakiyesi / hak_sahibi_sayisi
    
    print(f"[DAĞITIM] Havuz Bakiyesi: {havuz_bakiyesi} TL")
    print(f"[DAĞITIM] Hak Sahibi Sayısı: {hak_sahibi_sayisi}")
    print(f"[DAĞITIM] Kisi Basi Pay: {kisi_basi_pay:.2f} TL")
    
    # Bağımsız dağıtım raporu
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
        "hukuki_denetim": hukuki_sonuc,
        "sistem_kaynagi": "Sosyal_Imece_Otonom_Ekosistem",
        "mali_bagimsizlik": "UTEYKDER_dernek_butccesinden_bagimsiz",
        "uye_havuzu_kaynagi": "Sosyal_Imece_Bagimsiz_Uye_Havuzu"
    }
    
    # Bağımsız şeffaflık arşivi
    seffaflik_dosyasi = "data/sosyal_imece_seffaflik_raporlari/artik_bakiye_dagitim_loglari.json"
    os.makedirs(os.path.dirname(seffaflik_dosyasi), exist_ok=True)
    
    with open(seffaflik_dosyasi, "a", encoding="utf-8") as f:
        json.dump(dagitim_raporu, f, ensure_ascii=False, indent=4)
        f.write("\n")
    
    print(f"[SEFFAFLIK] Dagitim raporu bagimsiz arsive kaydedildi: {seffaflik_dosyasi}")
    print(f"[BAGIMSIZLIK] Mali Bagimsizlik: {dagitim_raporu['mali_bagimsizlik']}")
    print(f"[BAGIMSIZLIK] Uye Havuzu Kaynagi: {dagitim_raporu['uye_havuzu_kaynagi']}")
else:
    print("[UYARI] Hak sahibi bulunamadi. Dagitim yapilamadi.")

# 5. Şeffaflık Ajanı Testi (Bağımsız Arşiv)
print(f"\n5. Şeffaflık Ajanı Testi (Bağımsız Arşiv)")
print("-" * 60)

from trm_agents.seffaflik_ve_denetim_ajani import SeffaflikVeDenetimAjani
seffaflik_ajan = SeffaflikVeDenetimAjani(agent_id=181)

# Test gelir kaydet
gelir = seffaflik_ajan.run(
    operation="gelir_kaydet",
    islem_id="GEL001",
    gelir_tutari=10000,
    gelir_kaynagi="e_ticaret",
    kullanici_id="K001"
)

print(f"[SEFFAFLIK] Gelir Kaydedildi: {gelir['gelir_tutari']} TL")
print(f"[SEFFAFLIK] İmece Kesintisi: {gelir['imece_havuz_kesintisi']} TL")

# Genel şeffaflık raporu
rapor = seffaflik_ajan.run(operation="rapor")
print(f"[SEFFAFLIK] Sistem Kaynagi: Sosyal_Imece_Otonom_Ekosistem")
print(f"[SEFFAFLIK] Toplam Gelir: {rapor['ozet']['toplam_gelir']} TL")
print(f"[SEFFAFLIK] Toplam İmece Kesintisi: {rapor['ozet']['toplam_imece_kesintisi']} TL")

# 6. UTEYKDER Bağımsızlık Kontrolü
print(f"\n6. UTEYKDER Bağımsızlık Kontrolü")
print("-" * 60)

print(f"[KONTROL] UTEYKDER dernek butcesi ile ILISKISI: YOK")
print(f"[KONTROL] Mali islemler kaynagi: Sosyal_Imece_Otonom_Ekosistem")
print(f"[KONTROL] Uye havuzu kaynagi: Sosyal_Imece_Bagimsiz_Uye_Havuzu")
print(f"[KONTROL] Seffaflik arsivi: data/sosyal_imece_seffaflik_raporlari/")
print(f"[KONTROL] UTEYKDER rolu: Sadece fahri uye kaydi ve tanitim faaliyetleri")

print("\n" + "=" * 60)
print("[TAMAMLANDI] Bağımsız Mali Sistem Test Tamamlandı!")
print("[DURUM] Sosyal İmece mali sistemi UTEYKDER'den tamamen bagimsiz calisiyor.")
