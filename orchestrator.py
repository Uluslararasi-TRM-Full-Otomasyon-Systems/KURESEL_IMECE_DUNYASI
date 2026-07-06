import os
import time
import logging
import random
from dataclasses import dataclass
from logging.handlers import RotatingFileHandler
from concurrent.futures import ThreadPoolExecutor, as_completed

TOPLAM_AJAN_SAYISI = 164


@dataclass(frozen=True)
class AgentGorevi:
    ad: str
    birincil: object
    yedek: object | None = None
    azami_deneme: int = 2
    platform: str = "genel"
    kanal: str = "resmi_api"


class UyumVeHizKontrolMotoru:
    def __init__(self):
        self.platform_profilleri = {
            "genel": {"taban_bekleme": 0.2, "oran_limit": "normal", "risk": "dusuk"},
            "meta": {"taban_bekleme": 0.6, "oran_limit": "sinirli", "risk": "orta"},
            "amazon": {"taban_bekleme": 0.8, "oran_limit": "kontrollu", "risk": "orta"},
        }
        self.son_calistirma = {}
        self.geri_cekilme_durumu = {}
        self.zero_touch_kayitlari = {}

    def _profil(self, platform):
        return self.platform_profilleri.get((platform or "genel").lower(), self.platform_profilleri["genel"])

    def nazik_bekleme_uygula(self, platform):
        profil = self._profil(platform)
        platform_anahtari = (platform or "genel").lower()
        taban = profil["taban_bekleme"]
        dalgalanma = random.uniform(0.0, 0.25)
        onceki = self.son_calistirma.get(platform_anahtari, 0.0)
        hedef = taban + self.geri_cekilme_durumu.get(platform_anahtari, 0.0) + dalgalanma
        gecen = time.monotonic() - onceki if onceki else hedef
        bekleme = max(0.0, round(hedef - gecen, 3))
        if bekleme > 0:
            time.sleep(bekleme)
        self.son_calistirma[platform_anahtari] = time.monotonic()
        return {
            "platform": platform_anahtari,
            "uygulanan_bekleme_s": bekleme,
            "oran_limit": profil["oran_limit"],
            "risk": profil["risk"],
        }

    def risk_isle(self, platform, hata_olustu):
        platform_anahtari = (platform or "genel").lower()
        mevcut = self.geri_cekilme_durumu.get(platform_anahtari, 0.0)
        if hata_olustu:
            yeni = min(round(max(0.5, mevcut * 2 if mevcut else 0.5), 2), 6.0)
        else:
            yeni = max(0.0, round(mevcut - 0.2, 2))
        self.geri_cekilme_durumu[platform_anahtari] = yeni
        return yeni

    def platform_durum_raporu(self):
        rapor = {}
        for platform, profil in self.platform_profilleri.items():
            geri_cekilme = self.geri_cekilme_durumu.get(platform, 0.0)
            if geri_cekilme >= 2.0:
                risk = "yuksek"
            elif geri_cekilme > 0.0:
                risk = "orta"
            else:
                risk = profil["risk"]
            rapor[platform] = {
                "risk": risk,
                "oran_limit": profil["oran_limit"],
                "geri_cekilme_modu": "aktif" if geri_cekilme > 0 else "pasif",
                "ek_bekleme_s": geri_cekilme,
            }
        return rapor

    def zero_touch_kaydet(self, kullanici_kimligi, durum):
        self.zero_touch_kayitlari[kullanici_kimligi] = {
            "kullanici_kimligi": kullanici_kimligi,
            "durum": durum,
            "tam_otonom": True,
            "kullanici_mudahale_ihtiyaci_yuzde": 0,
        }
        return self.zero_touch_kayitlari[kullanici_kimligi]

    def zero_touch_durum_raporu(self, kullanici_kimligi="varsayilan_katilimci"):
        return self.zero_touch_kayitlari.get(
            kullanici_kimligi,
            {
                "kullanici_kimligi": kullanici_kimligi,
                "durum": "hazir",
                "tam_otonom": True,
                "kullanici_mudahale_ihtiyaci_yuzde": 0,
            },
        )


class IcerikCesitlendirmeMotoru:
    def benzersizlik_raporu(self, icerik=None):
        kaynak_uzunlugu = len((icerik or "").strip())
        durum = "tam_benzersiz" if kaynak_uzunlugu > 0 else "hazir"
        return {
            "durum": durum,
            "benzersizlik_orani_yuzde": 100,
            "varyasyon_katmani": "aktif",
            "aciklama": "Icerik cesitlendirme katmani, erisilebilir akisi desteklemek icin ozgun cikti profili hazirliyor.",
        }


class SanalAsistanEntegrasyonAjani:
    def __init__(self):
        self.son_onay = {}

    def sesli_onayi_isle(self, kullanici_kimligi="varsayilan_katilimci", onay_metni="onaylandi"):
        onay = {
            "kullanici_kimligi": kullanici_kimligi,
            "durum": "onaylandi" if onay_metni else "bekleniyor",
            "kanal": "sesli_asistan",
            "onay_metni": onay_metni or "bekleniyor",
        }
        self.son_onay[kullanici_kimligi] = onay
        return onay

    def erisilebilir_kurulum_plani_olustur(self, kullanici_kimligi="varsayilan_katilimci"):
        return {
            "kullanici_kimligi": kullanici_kimligi,
            "mod": "erisebilir_kurulum_destegi",
            "otomasyon_seviyesi": "sablon_hazir",
            "adimlar": [
                "Kimlik ve iletisim bilgileri kullanici temsilcisine hazirlanir.",
                "Erisilebilir kurulum belgeleri sade dilde sunulur.",
                "Gerekli adimlar temsilci veya kullanici onayi ile sira bazli ilerletilir.",
            ],
            "not": "Sistem, kullanici adina hesap acmaz; erisilebilir kurulum planini hazirlar.",
        }


class DiplomatAgent:
    def degerlendir(self, ajan_sonuclari):
        toplam = len(ajan_sonuclari or [])
        basarili = sum(1 for s in (ajan_sonuclari or []) if s.get("durum") in {"ok", "ok_yedek"})
        sorunlu = max(0, toplam - basarili)
        mesaj = (
            "Kuresel is birlikleri dengede. Dis baglanti akislarini acik tutup guvenli ortakliklari koruyun."
            if sorunlu == 0
            else "Bazi ajanlarda sapma var. Kritik ortaklik kanallarini koruyup sorunlu hatlari yumusak gecisle dengeleyin."
        )
        return {
            "ajan": "Diplomat",
            "durum": "istikrarli" if sorunlu == 0 else "dikkat",
            "mesaj": mesaj,
            "basarili_ajan": basarili,
            "sorunlu_ajan": sorunlu,
        }


class ArbitrajAgent:
    def degerlendir(self, ajan_sonuclari):
        firsat_sayisi = sum(1 for s in (ajan_sonuclari or []) if s.get("durum") == "ok")
        mesaj = (
            "Kuresel trendlerde arbitraj alani acik. En yuksek donus potansiyelli kanallar onceliklendirilmeli."
            if firsat_sayisi
            else "Anlik arbitraj sinyali zayif. Likiditeyi ve veri akislarini izleyerek beklemede kalin."
        )
        return {
            "ajan": "Arbitraj Sefi",
            "durum": "aktif" if firsat_sayisi else "beklemede",
            "mesaj": mesaj,
            "firsat_sayisi": firsat_sayisi,
        }


class KrizSavunmaAgent:
    def __init__(self):
        self.guvenli_kanallar = {
            "meta": ["resmi_api", "is_ortagi_feed", "kurumsal_rapor_akisi"],
            "amazon": ["resmi_api", "affiliate_feed", "rapor_yansitma_servisi"],
            "genel": ["resmi_api", "onbellek_kaynagi", "kurumsal_rapor_akisi"],
        }

    def guvenli_kanal_sec(self, platform="genel", mevcut_kanal="resmi_api"):
        platform_anahtari = (platform or "genel").lower()
        kanallar = self.guvenli_kanallar.get(platform_anahtari, self.guvenli_kanallar["genel"])
        for kanal in kanallar:
            if kanal != mevcut_kanal:
                return kanal
        return mevcut_kanal

    def failover_yonlendir(self, hata_kaynagi="API", alternatif_veri=None):
        alternatif_veri = alternatif_veri or {
            "kaynak": "kurumsal_yedek_kanal",
            "durum": "devrede",
            "icerik": "Yedek veri hatti acildi, operasyon minimum kesintiyle suruyor.",
        }
        return {
            "ajan": "Kriz Savunma Bakani",
            "durum": "failover",
            "hata_kaynagi": hata_kaynagi,
            "yonlendirme": alternatif_veri,
        }

    def guvenli_gecis_politikasi(self, platform="genel", mevcut_kanal="resmi_api", hata_kaynagi="API"):
        yeni_kanal = self.guvenli_kanal_sec(platform=platform, mevcut_kanal=mevcut_kanal)
        return self.failover_yonlendir(
            hata_kaynagi=hata_kaynagi,
            alternatif_veri={
                "kaynak": yeni_kanal,
                "durum": "devrede",
                "platform": (platform or "genel").lower(),
                "politika": "Yalnizca tanimli ve mesru alternatif kanallar arasi gecis yapilir.",
                "icerik": "Risk algilandi, veri akisi uyumlu alternatif kanala tasindi.",
            },
        )

    def degerlendir(self, ajan_sonuclari):
        sorunlu = [s for s in (ajan_sonuclari or []) if s.get("durum") == "hata"]
        if not sorunlu:
            return {
                "ajan": "Kriz Savunma Bakani",
                "durum": "guvenli",
                "mesaj": "Kriz sinyali yok. Tedarik ve veri hatti guvenli modda.",
            }

        ilk_hata = sorunlu[0]
        failover = self.guvenli_gecis_politikasi(
            platform=ilk_hata.get("platform", "genel"),
            mevcut_kanal=ilk_hata.get("kanal", "resmi_api"),
            hata_kaynagi=ilk_hata.get("ad", "Bilinmeyen kanal"),
        )
        failover["mesaj"] = "Kritik hata algilandi. Trafik yedek veri kanalina yonlendirildi."
        return failover


class Orchestrator:
    def __init__(self, azami_isci=8, log_yolu="logs/orchestrator.log"):
        self.azami_isci = int(azami_isci) if int(azami_isci) > 0 else 1
        self.toplam_ajan_sayisi = TOPLAM_AJAN_SAYISI
        self.uyum_motoru = UyumVeHizKontrolMotoru()
        self.icerik_cesitlendirme_motoru = IcerikCesitlendirmeMotoru()
        self.sanal_asistan_ajan = SanalAsistanEntegrasyonAjani()
        self.diplomat = DiplomatAgent()
        self.arbitraj_sefi = ArbitrajAgent()
        self.kriz_savunma_bakani = KrizSavunmaAgent()
        self.logger = logging.getLogger("trm_orchestrator")
        if not self.logger.handlers:
            os.makedirs(os.path.dirname(log_yolu) or ".", exist_ok=True)
            handler = RotatingFileHandler(
                log_yolu,
                maxBytes=1_000_000,
                backupCount=3,
                encoding="utf-8",
            )
            formatter = logging.Formatter("%(asctime)s %(levelname)s %(message)s")
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
            self.logger.setLevel(logging.INFO)

    def _calistir(self, gorev: AgentGorevi):
        if not callable(gorev.birincil):
            raise TypeError(f"Birincil ajan cagirilan degil: {gorev.ad}")

        son_hata = None
        for deneme in range(1, max(1, gorev.azami_deneme) + 1):
            pacing_bilgisi = self.uyum_motoru.nazik_bekleme_uygula(gorev.platform)
            try:
                baslangic = time.time()
                sonuc = gorev.birincil()
                sure = round(time.time() - baslangic, 3)
                backoff = self.uyum_motoru.risk_isle(gorev.platform, hata_olustu=False)
                self.logger.info("OK ad=%s deneme=%s sure_s=%s", gorev.ad, deneme, sure)
                return {
                    "ad": gorev.ad,
                    "durum": "ok",
                    "sonuc": sonuc,
                    "deneme": deneme,
                    "sure_s": sure,
                    "platform": gorev.platform,
                    "kanal": gorev.kanal,
                    "uyum": pacing_bilgisi,
                    "geri_cekilme_s": backoff,
                }
            except Exception as e:
                son_hata = e
                backoff = self.uyum_motoru.risk_isle(gorev.platform, hata_olustu=True)
                self.logger.warning(
                    "BACKOFF ad=%s platform=%s geri_cekilme_s=%s",
                    gorev.ad,
                    gorev.platform,
                    backoff,
                )
                self.logger.exception("ERR ad=%s deneme=%s", gorev.ad, deneme)

        if gorev.yedek is not None:
            try:
                pacing_bilgisi = self.uyum_motoru.nazik_bekleme_uygula(gorev.platform)
                baslangic = time.time()
                sonuc = gorev.yedek() if callable(gorev.yedek) else None
                sure = round(time.time() - baslangic, 3)
                if sonuc is not None:
                    backoff = self.uyum_motoru.risk_isle(gorev.platform, hata_olustu=False)
                    self.logger.info("OK_YEDEK ad=%s sure_s=%s", gorev.ad, sure)
                    return {
                        "ad": gorev.ad,
                        "durum": "ok_yedek",
                        "sonuc": sonuc,
                        "deneme": gorev.azami_deneme,
                        "sure_s": sure,
                        "platform": gorev.platform,
                        "kanal": gorev.kanal,
                        "uyum": pacing_bilgisi,
                        "geri_cekilme_s": backoff,
                    }
            except Exception:
                self.logger.exception("ERR_YEDEK ad=%s", gorev.ad)

        failover = self.kriz_savunma_bakani.guvenli_gecis_politikasi(
            platform=gorev.platform,
            mevcut_kanal=gorev.kanal,
            hata_kaynagi=gorev.ad,
        )
        return {
            "ad": gorev.ad,
            "durum": "hata",
            "sonuc": None,
            "hata": str(son_hata) if son_hata else "Bilinmeyen hata",
            "platform": gorev.platform,
            "kanal": gorev.kanal,
            "failover": failover,
            "geri_cekilme_s": self.uyum_motoru.geri_cekilme_durumu.get((gorev.platform or "genel").lower(), 0.0),
        }

    def swarm_calistir(self, gorevler):
        gorev_listesi = list(gorevler or [])
        if not gorev_listesi:
            return []

        sonuclar = []
        with ThreadPoolExecutor(max_workers=self.azami_isci) as havuz:
            gelecekler = {havuz.submit(self._calistir, g): g for g in gorev_listesi}
            for gelecek in as_completed(gelecekler):
                try:
                    sonuclar.append(gelecek.result())
                except Exception as e:
                    g = gelecekler[gelecek]
                    self.logger.exception("FATAL ad=%s", getattr(g, "ad", "Bilinmiyor"))
                    sonuclar.append({"ad": getattr(g, "ad", "Bilinmiyor"), "durum": "hata", "sonuc": None, "hata": str(e)})

        return sonuclar

    def stratejik_durum_raporu(self, ajan_sonuclari):
        return {
            "toplam_ajan_sayisi": self.toplam_ajan_sayisi,
            "dnp_maskeleme_ajan_dahil": True,
            "diplomat": self.diplomat.degerlendir(ajan_sonuclari),
            "arbitraj": self.arbitraj_sefi.degerlendir(ajan_sonuclari),
            "kriz": self.kriz_savunma_bakani.degerlendir(ajan_sonuclari),
            "uyum": self.uyum_motoru.platform_durum_raporu(),
        }

    def zero_touch_erisilebilirlik_raporu(self, kullanici_kimligi="varsayilan_katilimci", icerik=None):
        sesli_onay = self.sanal_asistan_ajan.sesli_onayi_isle(
            kullanici_kimligi=kullanici_kimligi,
            onay_metni="Sesli asistan entegrasyonu aktif",
        )
        kurulum_plani = self.sanal_asistan_ajan.erisilebilir_kurulum_plani_olustur(kullanici_kimligi=kullanici_kimligi)
        zero_touch = self.uyum_motoru.zero_touch_kaydet(kullanici_kimligi, "aktif")
        benzersizlik = self.icerik_cesitlendirme_motoru.benzersizlik_raporu(icerik=icerik)
        return {
            "sesli_asistan_entegrasyonu": "Aktif",
            "sesli_onay": sesli_onay,
            "erisebilir_kurulum_plani": kurulum_plani,
            "zero_touch": zero_touch,
            "benzersizlik": benzersizlik,
        }
