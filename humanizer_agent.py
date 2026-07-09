import time
import random
import sys

class HumanizerAgent:
    def __init__(self):
        # Islemler arasi rastgele bekleme araligi (saniye cinsinden)
        self.min_wait = 10
        self.max_wait = 45

    def insansi_bekle(self):
        """Algoritmanin sabit zamanli bot takibini bozmak icin rastgele surelerde bekler."""
        bekleme_suresi = random.uniform(self.min_wait, self.max_wait)
        print(f"[HUMANIZER] Bir insan gibi {bekleme_suresi:.2f} saniye duraklaniyor...")
        time.sleep(bekleme_suresi)

    def insansi_yaz(self, metin):
        """Metni tek seferde yapistirmaz, klavyede yaziliyor gibi harf harf basar."""
        print("[HUMANIZER] Metin insansi klavye simulasyonu ile isleniyor...")
        for harf in metin:
            sys.stdout.write(harf)
            sys.stdout.flush()
            # Harfler arasi milisaniyelik degisken gecikmeler
            time.sleep(random.uniform(0.03, 0.18))
        print("\n[HUMANIZER] Metin girisi basarili.")