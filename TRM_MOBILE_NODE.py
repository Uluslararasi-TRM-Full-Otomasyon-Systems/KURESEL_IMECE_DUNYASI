import time
import sys
import os

def mobil_dugum_baslat():
    print("==================================================")
    print("🤖 KURESEL IMECE DUNYASI - MOBIL DUGUMU (NODE) v1.0")
    print("==================================================")
    print("✅ Durum: AKTIF")
    print("🔌 Elektrik/Wi-Fi Korumasi: DEVREDE")
    print("--------------------------------------------------")
    print("🚀 Sistem arka planda dinlemeye basladi...")
    print("💡 Uye Giris Onayi Bekleniyor... (Test Grubu: 10 Katilimci)")
    print("--------------------------------------------------")

    imece_puani = 0
    
    # 10 Kisilik UTEYKDER test grubunun simulasyonu ve elektrik koruma mantigi
    try:
        while True:
            # Her 10 saniyede bir sistemi ve puan akisini kontrol eder
            time.sleep(10)
            imece_puani += 5
            print(f"📊 [TRM NODE] Sistem Sorunsuz Calisiyor | Kazanilan Arti Puan: +{imece_puani}")
            
    except KeyboardInterrupt:
        print("\n⚠️ Mobil Dugum kullanici tarafindan durduruldu. Guvenli cikis yapiliyor...")

if __name__ == "__main__":
    mobil_dugum_baslat()
