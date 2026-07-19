import datetime

class TRMRefahVeUretimMuhafizi:
    def __init__(self):
        self.ajan_adi = "TRM Refah ve Üretim Muhafızı"
        self.turkis_yoksulluk_siniri = 114576.0  # Mayıs 2026 Güncel Veri

    def uye_durum_denetle(self, uye_bilgisi):
        """
        Uyenin istifa edip etmedigini, tembellik durumunu ve hak edisini hesaplar.
        """
        isim = uye_bilgisi['isim']
        mevcut_maas = uye_bilgisi['mevcut_maas']
        aktif_calisiyor_mu = uye_bilgisi['aktif_calisiyor_mu']
        istifa_etti_mi = uye_bilgisi['istifa_etti_mi']
        trm_gunluk_mesai_saati = uye_bilgisi['trm_gunluk_mesai_saati']
        
        print(f"\n--- [{self.ajan_adi}] {isim} İçin Sorumluluk ve Refah Denetimi Başlatıldı ---")

        # 1. KURAL: Anti-İstifa Kontrolü
        if istifa_etti_mi and mevcut_maas > 0:
            print(f"🚨 TEHLİKE: {isim} sistem gelirine tamah ederek asıl işinden istifa etmiştir!")
            print("🚫 SİSTEM BLOKAJI: Hak ediş iptal edildi. Üretimden kaçan sisteme yük olamaz.")
            return {"durum": "REDDEDİLDİ", "hak_edis": 0, "neden": "Asıl işten keyfi istifa."}

        # 2. KURAL: Çalışmayan/Vasıfsız Kişiler İçin Tembellik Kontrolü
        if mevcut_maas == 0 or not aktif_calisiyor_mu:
            print(f"⚠️ BİLGİ: {isim} herhangi bir dış işte çalışmamaktadır (Vasıfsız/İşsiz Statüsü).")
            if trm_gunluk_mesai_saati < 4:
                print(f"🚫 BLOKAJ: {isim} günlük minimum 4 saatlik TRM dijital üretim mesaisini tamamlamadı (Mevcut: {trm_gunluk_mesai_saati} saat).")
                return {"durum": "ASKIDA", "hak_edis": 0, "neden": "Yetersiz sistem mesaisi / Tembellik riski."}
            else:
                print(f"✅ ONAY: {isim} TRM ekosisteminde aktif çalışıyor. Refah desteği tanımlanıyor.")

        # 3. KURAL: Dinamik Refah Açığı Hesaplama (Açık = Yoksulluk - Maaş)
        if mevcut_maas < self.turkis_yoksulluk_siniri:
            refah_acigi = self.turkis_yoksulluk_siniri - mevcut_maas
            print(f"📊 HESAPLAMA: Yoksulluk Sınırı: {self.turkis_yoksulluk_siniri} TL | Üye Maaşı: {mevcut_maas} TL")
            print(f"💰 AKTARILACAK REFAH PAYI: {refah_acigi} TL")
            return {"durum": "ONAYLANDI", "hak_edis": refah_acigi, "neden": "Refah sınırı tamamlama payı."}
        else:
            print(f"🎉 {isim} zaten yoksulluk sınırının üzerinde bir gelire sahip. Ek desteğe ihtiyacı yok.")
            return {"durum": "GEREK_YOK", "hak_edis": 0, "neden": "Gelir düzeyi yeterli."}

# --- TEST SENARYOSU ---
if __name__ == "__main__":
    muhafiz = TRMRefahVeUretimMuhafizi()

    # Senaryo A: Sizin verdiğiniz örnek (30.000 TL alıyor, işine devam ediyor)
    uye_A = {
        "isim": "Ahmet Yılmaz",
        "mevcut_maas": 30000.0,
        "aktif_calisiyor_mu": True,
        "istifa_etti_mi": False,
        "trm_gunluk_mesai_saati": 2
    }
    muhafiz.uye_durum_denetle(uye_A)

    # Senaryo B: Parayı bulup işten istifa eden tembellik eğilimli kişi
    uye_B = {
        "isim": "Cemil Kaya",
        "mevcut_maas": 30000.0,
        "aktif_calisiyor_mu": False,
        "istifa_etti_mi": True,
        "trm_gunluk_mesai_saati": 0
    }
    muhafiz.uye_durum_denetle(uye_B)