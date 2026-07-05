class IcerikFabrikasi:
    def __init__(self, urun_verisi):
        """
        Otonom tarayıcıdan gelen analiz sonuçlarını
        içerik fabrikasının merkezine yükler.
        """
        self.urun_verisi = urun_verisi

    def icerik_uret(self):
        """
        Gelen pazar verisini işleyerek hem sosyal medya hem de
        Sanal El (Sesli Asistan) için profesyonel içerik üretir.
        """
        urun_adi = self.urun_verisi.get("urun_adi", "Harika Fırsat Ürünü")
        fiyat = self.urun_verisi.get("fiyat", "Cazip Fiyat")
        neden_trend = self.urun_verisi.get("neden_trend", "Yüksek talep görüyor.")
        hedef_url = self.urun_verisi.get("hedef_url", "https://trendurunlermarket.com")

        # Otonom reklam stratejisi metni oluşturuluyor
        reklam_metni = (
            f"📢 DİKKAT, BU ÜRÜN ŞU AN İNTERNETTE ÇILGINLAR GİBİ SATIYOR!\n\n"
            f"📦 Ürün Adı: {urun_adi}\n"
            f"💰 Fiyat: {fiyat}\n\n"
            f"🎯 Neden Kaçırmamalısınız? Çünkü bu ürün {neden_trend.lower()}\n\n"
            f"⚡ Küresel Sosyal İmece Dünyası otonom sistemleri tarafından anlık olarak tespit edilmiştir. "
            f"Detaylar ve satın alma linki profilde! Güvenli alışverişin adresi trendurunlermarket!\n\n"
            f"🔗 İncelemek İçin: {hedef_url}"
        )

        return reklam_metni
