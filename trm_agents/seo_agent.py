from utils.config_loader import load_config
import random
import time

class SeoAgent:
    """
    SEO ve pazarlama ajanı.
    Konfigürasyondan hedef pazar, anahtar kelime stratejisi, backlink kalitesi ve denetim ayarlarını alır.
    """
    def __init__(self, agent_id=101):
        self.agent_id = agent_id
        self.name = f"SeoAgent-{agent_id:03d}"
        self.config = load_config()
        self.pazar = self.config["seo"]["hedef_pazar"]
        self.strateji = self.config["seo"]["anahtar_kelime_stratejisi"]
        self.backlink_kalitesi = self.config["seo"]["backlink_kalitesi"]
        self.denetim_aktif = self.config["seo"]["günlük_denetim"]
        self.cpu_yuk = 0.0
        self.api_gecikme = 0.0

    def refresh_config(self):
        self.config = load_config()
        self.pazar = self.config["seo"]["hedef_pazar"]
        self.strateji = self.config["seo"]["anahtar_kelime_stratejisi"]
        self.backlink_kalitesi = self.config["seo"]["backlink_kalitesi"]
        self.denetim_aktif = self.config["seo"]["günlük_denetim"]

    def anahtar_kelime_analizi(self):
        """Simüle edilmiş anahtar kelime analizi."""
        gecikme = random.uniform(0.2, 1.0)
        time.sleep(gecikme * 0.1)
        self.api_gecikme = gecikme * 1000
        self.cpu_yuk = random.uniform(15, 85)

        if self.strateji == "uzun_kuyruk":
            kelimeler = ["en iyi yapay zeka araçları", "dijital pazarlama trendleri 2025"]
        elif self.strateji == "kisa_kuyruk":
            kelimeler = ["AI", "SEO", "pazarlama"]
        else:  # reklam
            kelimeler = ["reklam kampanyası", "hedefleme", "dönüşüm"]

        return {
            "durum": "basarili",
            "pazar": self.pazar,
            "strateji": self.strateji,
            "anahtar_kelimeler": kelimeler,
            "backlink_kalitesi": self.backlink_kalitesi
        }

    def denetim_yap(self):
        """Denetim aktifse günlük kontrol simülasyonu."""
        if self.denetim_aktif:
            return {"denetim": "tamam", "rapor": "SEO uyumluluğu kontrol edildi, sorun yok."}
        return {"denetim": "pasif", "mesaj": "Denetim kapalı."}

    def run(self):
        self.refresh_config()
        analiz_sonuc = self.anahtar_kelime_analizi()
        denetim_sonuc = self.denetim_yap()
        return {**analiz_sonuc, **denetim_sonuc}