# -*- coding: utf-8 -*-
"""
Küresel İmece Dünyası - Otonom Müracaat Analizi ve Otomatik Onay Psikolog Ajanı
"""
import os
import json
from datetime import datetime

class KureselPsikologAjani:
    def __init__(self):
        self.analiz_veritabani = "karakter_analizleri.json"
        self.onaylanan_uyeler_dosyasi = "otonom_onayli_uyeler.json"
        
        # 🎯 SİSTEME ZARAR VERECEK, ARKA PLANDA "SAPITMA" EĞİLİMİ OLAN KARAKTER PARAMETRELERİ
        self.tehlike_sinyalleri = [
            "kısa yoldan zengin", "vurgun", "emek harcamadan", "dolandırıcılık", 
            "illegal", "hack", "sistemi patlatma", "açık arama", "sahte hesap"
        ]
        
        # ✨ KÜRESEL İMECE RUHUNA VE UTEYKDER VİZYONUNA UYUM PARAMETRELERİ
        self.uyumlu_sinyaller = [
            "yardımlaşma", "dernek", "üretim", "kooperatif", "dürüst kazanç", 
            "sosyal sorumluluk", "engelli", "paylaşım", "imece"
        ]

    def muracaat_degerlendir_ve_onayla(self, aday_verisi):
        """
        Aday formu doldururken veya sesli asistanla konuşurken O AN tetiklenir.
        Karakter analizi yapar ve sisteme kaydı ANINDA OTOMATİK ONAYLAR veya REDDEDER.
        """
        motivasyon_metni = aday_verisi.get("motivasyon_cumlesi", "").lower()
        ad_soyad = aday_verisi.get("ad_soyad", "Bilinmeyen Aday")
        tc_no = aday_verisi.get("tc_no", "")
        
        sapitma_skoru = 0
        uyum_skoru = 0
        notlar = []

        # 1. Kelime ve Parametre Analizi (Ses transkripti veya form metni üzerinden)
        for kelime in self.tehlike_sinyalleri:
            if kelime in motivasyon_metni:
                sapitma_skoru += 25
                notlar.append(f"⚠️ Riskli Kelime Tespit Edildi: '{kelime}'")

        for kelime in self.uyumlu_sinyaller:
            if kelime in motivasyon_metni:
                uyum_skoru += 15
                notlar.append(f"✨ Olumlu Parametre: '{kelime}'")

        # 2. Nihai Psikolojik Karar Dengesi
        net_durum = "REDDEDİLDİ"
        otonom_onay = False
        
        # Karar Mekanizması: Sapıtma skoru kritik eşiği (50) aşarsa veya uyum skoru sıfırsa elenir
        if sapitma_skoru < 50 and (uyum_skoru >= 15 or sapitma_skoru == 0):
            net_durum = "OTONOM ONAYLANDI - SİSTEME GİRİŞ YETKİSİ VERİLDİ"
            otonom_onay = True
            notlar.append("✅ Karakter imece modeline uygun ve güvenli bulundu.")
        else:
            notlar.append("❌ Karakter yapısı ekosistemi sabote etme veya sapıtma eğilimi gösteriyor!")

        analiz_sonucu = {
            "tc_no": tc_no,
            "ad_soyad": ad_soyad,
            "sapitma_skoru": sapitma_skoru,
            "uyum_skoru": uyum_skoru,
            "karar": net_durum,
            "notlar": notlar,
            "analiz_tarihi": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        # Veritabanına Analizi Kaydet
        self._veritabanina_yaz(self.analiz_veritabani, analiz_sonucu)

        # 3. Eğer Otonom Onay Aldıysa, Parmağını Oynatmadan Kazanacağı Sisteme Kaydını Bas
        if otonom_onay:
            self._onayli_uye_kaydet(aday_verisi)

        return analiz_sonucu

    def _veritabanina_yaz(self, dosya_adi, veri):
        mevcut = []
        if os.path.exists(dosya_adi):
            with open(dosya_adi, 'r', encoding='utf-8') as f:
                try: mevcut = json.load(f)
                except: mevcut = []
        mevcut.append(veri)
        with open(dosya_adi, 'w', encoding='utf-8') as f:
            json.dump(mevcut, f, ensure_ascii=False, indent=4)

    def _onayli_uye_kaydet(self, aday_verisi):
        """Onaylanan kişiyi doğrudan pasif gelir havuzuna aktarır."""
        aday_verisi["aktivasyon_durumu"] = "Aktif (Parmağını Oynatmadan Kazanabilir)"
        aday_verisi["onay_tarihi"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self._veritabanina_yaz(self.onaylanan_uyeler_dosyasi, aday_verisi)

if __name__ == "__main__":
    psikolog = KureselPsikologAjani()
    print("🌍 Küresel İmece Dünyası - Otonom Onay Psikolog Ajanı Tetikte!")
