import time
import random
from datetime import datetime

class ActivityProtectorAgent:
    def __init__(self):
        pass

    def kaos_ve_sapma_kontrolu(self):
        """Sistemin kusursuz robotik ritmini bozarak algoritmayı şaşırtır."""
        zar = random.randint(1, 100)
        
        if zar <= 15:  # %15 ihtimalle yapay tembellik modu
            print("[KAOS PROTECTOR] Yapay tembellik tetiklendi. Sistem şu an sadece geziniyor...")
            time.sleep(random.uniform(30, 90))
            return True
        elif zar > 15 and zar <= 25:  # %10 ihtimalle paylaşımı erteleme kararı
            print("[KAOS PROTECTOR] İnsansı vazgeçme simülasyonu: İşlem bir sonraki tura ertelendi.")
            return False
        
        print("[KAOS PROTECTOR] Ritim insansı standartlarda, akış devam ediyor.")
        return True

    def gece_uyku_modu(self):
        """Gece saatlerinde sistemin tamamen uyumasını sağlar (Gerçek insan ritmi)."""
        su_an = datetime.now().hour
        if su_an >= 0 and su_an <= 6:  # 00:00 - 06:00 arası
            print("[KAOS PROTECTOR] Gece modu aktif. Robotlar uyuyor, işlem yapılmayacak.")
            return True
        return False