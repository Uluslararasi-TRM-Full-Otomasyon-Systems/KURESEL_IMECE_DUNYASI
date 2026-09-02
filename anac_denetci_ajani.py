# -*- coding: utf-8 -*-
"""
ANAÇ RUHLU DANIŞMAN & NİYET DENETÇİ AJANI
Sisteme katılmak isteyen kişilerin gerçek niyetini (yalnız ve normal standartlarda huzurlu bir yaşam)
ve zihinsel berraklığını (sabit/takıntılı kırıntıların olmamasını) anaç bir şefkat ama net bir süzgeçle denetler.
"""
import os
import json
from datetime import datetime

class AnacRuhluDenetciAjani:
    def __init__(self):
        self.log_dosyasi = "anac_denetim_arsivi.json"

    def niyet_ve_zihin_sorgula(self, aday_bilgileri):
        """
        aday_bilgileri sözlüğü şu alanları içermelidir:
        - ad_soyad
        - yas
        - beyan_edilen_amac (Kişinin sistemi neden istediğine dair açıklaması)
        - zihinsel_durum_notu (Takıntılı, saplantılı veya komplo/sabit fikir belirtileri analizi)
        """
        ad = aday_bilgileri.get("ad_soyad", "Misafir")
        amac = aday_bilgileri.get("beyan_edilen_amac", "").lower()
        zihin_notu = aday_bilgileri.get("zihinsel_durum_notu", "").lower()

        # 1. Kriter: Gerçekten yalnız hayatını normal standartlarda sürdürme isteği
        normal_hayat_kriterleri = ["normal", "sakin", "huzurlu", "yalnız", "kendi halimde", "düzenli", "geçim"]
        amac_uygun_mu = any(kriter in amac for kriter in normal_hayat_kriterleri)

        # 2. Kriter: Sabit ve takıntılı bilgi kırıntılarının (saplantı, öfke, komplo, inat) olmaması
        takinti_belirtileri = ["intikam", "mutlaka", "tek doğru", "düşman", "komplo", "uğraşacağım", "takıntı", "hırs", "intikam"]
        takinti_var_mi = any(belirti in zihin_notu for belirti in takinti_belirtileri)

        # Anaç Sentez ve Karar
        if amac_uygun_mu and not takinti_var_mi:
            onay = True
            anac_mesaj = (
                f"Yavrum {ad}, seni dinledim, kalbini ve niyetini sezdim. "
                "Derdin gürültü patırtı değil, kendi köşende insan gibi, huzurla ve normal standartlarda yaşamak. "
                "Zihnin de berrak, ortada seni yiyip bitiren takıntılar, karanlık saplantılar yok. "
                "Kapımız sana açık, huzur bulmaya gelebilirsin, başımın üstünde yerin var."
            )
        else:
            onay = False
            if not amac_uygun_mu:
                anac_mesaj = (
                    f"Evladım {ad}, bak gözlerimin içine... Sen buraya sakin bir ömür sürmeye değil, "
                    "kafanda başka hesaplarla, karmaşayla geliyorsun. Burası dirlik düzen yeridir, "
                    "yalnızlığını normal ve huzurlu yaşamak istemiyorsan bu kapı sana ağır gelir, yorulursun."
                )
            else:
                anac_mesaj = (
                    f"Güzel çocuğum {ad}, içindeki o takıntılı, inatçı kırıntıları seziyorum. "
                    "O kafayla buraya gelip ne kendini ne bizi huzursuz et. "
                    "Önce o zihnini bir arındır, içindeki huzursuzlukları bırak, ondan sonra kapımızı çal."
                )

        sonuc = {
            "aday": ad,
            "zaman": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "onay_durumu": onay,
            "anac_yorum": anac_mesaj
        }

        self._arsivle(sonuc)
        return sonuc

    def _arsivle(self, veri):
        mevcut = []
        if os.path.exists(self.log_dosyasi):
            try:
                with open(self.log_dosyasi, 'r', encoding='utf-8') as f:
                    mevcut = json.load(f)
            except:
                mevcut = []
        mevcut.append(veri)
        with open(self.log_dosyasi, 'w', encoding='utf-8') as f:
            json.dump(mevcut, f, ensure_ascii=False, indent=4)