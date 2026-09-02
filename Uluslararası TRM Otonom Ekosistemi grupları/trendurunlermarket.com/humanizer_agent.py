import time
import random
import sys

class HumanizerAgent:
    def __init__(self):
        # İşlemler arası rastgele bekleme aralığı (saniye cinsinden)
        self.min_wait = 10
        self.max_wait = 45

    def insansi_bekle(self):
        """Algoritmanın sabit zamanlı bot takibini bozmak için rastgele sürelerde bekler."""
        bekleme_suresi = random.uniform(self.min_wait, self.max_wait)
        print(f"[HUMANIZER] Bir insan gibi {bekleme_suresi:.2f} saniye duraklanıyor...")
        time.sleep(bekleme_suresi)

    def insansi_yaz(self, metin):
        """Metni tek seferde yapıştırmaz, klavyede yazılıyor gibi harf harf basar."""
        print("[HUMANIZER] Metin insansı klavye simülasyonu ile işleniyor...")
        for harf in metin:
            sys.stdout.write(harf)
            sys.stdout.flush()
            # Harfler arası milisaniyelik değişken gecikmeler
            time.sleep(random.uniform(0.03, 0.18))
        print("\n[HUMANIZER] Metin girişi başarılı.")