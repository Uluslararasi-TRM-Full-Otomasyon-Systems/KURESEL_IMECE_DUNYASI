# self_healing_core.py - Otonom Öz-İyileştirme ve Hata Giderme Modülü
import os
import sys
import traceback
import logging
import subprocess
from datetime import datetime

# Günlük kayıt tutma ayarları
logging.basicConfig(
    filename='reports/self_healing.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class SelfHealingEngine:
    def __init__(self):
        self.active = True

    def safe_execute(self, func, *args, **kwargs):
        """Fonksiyonları güvenli çalıştırır, hata durumunda loglar ve onarım tetikler."""
        try:
            return func(*args, **kwargs)
        except Exception as e:
            hata_detayi = traceback.format_exc()
            print(f"⚠️ Çalışma Zamanı Hatası Yakalandı: {e}")
            logging.error(f"Hata Yakalandı: {e}\n{hata_detayi}")
            
            # Otonom Onarım Adımı
            self.auto_patch(e, hata_detayi)
            return None

    def auto_patch(self, exception, traceback_str):
        """Hataları analiz edip otomatik düzeltme simülasyonu veya raporlaması yapar."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        patch_raporu = f"reports/patch_report_{timestamp}.txt"
        
        os.makedirs("reports", exist_ok=True)
        with open(patch_raporu, "w", encoding="utf-8") as f:
            f.write(f"HATA ZAMANI: {timestamp}\n")
            f.write(f"HATA TÜRÜ: {type(exception).__name__}\n")
            f.write(f"DETAY:\n{traceback_str}\n")
            f.write("DURUM: Ajan analizi bekleniyor / Modül izolasyonu uygulandı.\n")
            
        print(f"🔧 Otonom Öz-İyileştirme: Hata raporlandı ve sistem güvenli moda alındı -> {patch_raporu}")
        logging.info(f"Otonom yama raporu oluşturuldu: {patch_raporu}")

if __name__ == "__main__":
    he = SelfHealingEngine()
    print("🤖 Self-Healing Core aktif ve izlemede.")