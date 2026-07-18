from agents.icerik_agent import IcerikAgent
from agents.seo_agent import SeoAgent
from agents.finans_agent import FinansAgent
from agents.dnp_agent import DNPAgent
import time

def main():
    # Tüm ajanları başlat
    icerik_ajanlari = [IcerikAgent(i) for i in range(1, 51)]      # 50 içerik ajanı
    seo_ajanlari = [SeoAgent(i) for i in range(51, 101)]          # 50 SEO ajanı
    finans_ajanlari = [FinansAgent(i) for i in range(101, 160)]   # 59 finans ajanı
    dnp = DNPAgent(160)                                           # 161. ajan DNP

    tum_ajanlar = icerik_ajanlari + seo_ajanlari + finans_ajanlari + [dnp]

    print("🌟 TRM NIRVANA v3.0 Başlatılıyor – 161 ajan aktif.")
    cycle = 0
    while True:
        cycle += 1
        print(f"\n🔄 Çalışma Döngüsü #{cycle}")

        # Her ajanı çalıştır
        for ajan in tum_ajanlar:
            try:
                sonuc = ajan.run()
                # İsteğe bağlı log
                # print(f"{ajan.name} -> {sonuc}")
            except Exception as e:
                print(f"❌ {ajan.name} hatası: {e}")

        # DNP denetimi – tüm ajanları kontrol et
        dnp.denetle(tum_ajanlar)

        # 30 saniye bekle (konfigürasyon değişikliklerinin okunması için yeterli)
        time.sleep(30)

if __name__ == "__main__":
    main()