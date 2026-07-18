from utils.config_loader import load_config
import random
import time

class IcerikAgent:
    """
    İçerik üretiminden sorumlu ajan.
    Konfigürasyondan API anahtarı, hedef dil, günlük limit ve ton bilgilerini alır.
    """
    def __init__(self, agent_id=1):
        self.agent_id = agent_id
        self.name = f"IcerikAgent-{agent_id:03d}"
        self.config = load_config()
        self.api_key = self.config["icerik"]["api_key"]
        self.dil = self.config["icerik"]["hedef_dil"]
        self.gunluk_limit = self.config["icerik"]["günlük_limit"]
        self.ton = self.config["icerik"]["ton"]
        self.uretilen_miktar = 0
        self.cpu_yuk = 0.0      # DNP denetimi için
        self.api_gecikme = 0.0  # DNP denetimi için

    def refresh_config(self):
        """Güncel konfigürasyonu yükle ve parametreleri güncelle."""
        self.config = load_config()
        self.api_key = self.config["icerik"]["api_key"]
        self.dil = self.config["icerik"]["hedef_dil"]
        self.gunluk_limit = self.config["icerik"]["günlük_limit"]
        self.ton = self.config["icerik"]["ton"]

    def icerik_uret(self, konu=""):
        """
        Simüle edilmiş içerik üretimi.
        Gerçekte burada OpenAI veya başka bir API çağrılır.
        """
        if self.uretilen_miktar >= self.gunluk_limit:
            return {"durum": "limit_asildi", "mesaj": f"Günlük limit ({self.gunluk_limit}) aşıldı."}

        # API çağrısı simülasyonu – gecikme ve CPU yükü oluştur
        gecikme = random.uniform(0.1, 0.8)
        time.sleep(gecikme * 0.1)  # sadece simülasyon
        self.api_gecikme = gecikme * 1000  # ms cinsinden
        self.cpu_yuk = random.uniform(10, 90)

        # İçerik üret
        self.uretilen_miktar += 1
        icerik = f"{self.ton} tonunda, {self.dil} dilinde yazılmış makale. Konu: {konu or 'Genel'}"
        return {
            "durum": "basarili",
            "icerik": icerik,
            "kalan_limit": self.gunluk_limit - self.uretilen_miktar
        }

    def run(self):
        """Her çalıştırmada güncel konfigürasyonu al ve içerik üret."""
        self.refresh_config()
        # Örnek: rastgele bir konu ile içerik üret
        konular = ["Yapay Zeka", "Sosyal Medya", "SEO Stratejileri", "Finansal Okuryazarlık"]
        konu = random.choice(konular)
        sonuc = self.icerik_uret(konu)
        return sonuc