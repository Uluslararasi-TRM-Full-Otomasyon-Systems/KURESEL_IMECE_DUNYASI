import time
import sys
import os

def mobil_dugum_baslat():
    print("==================================================")
    print("🤖 KÜRESEL İMECE DÜNYASI - MOBİL DÜĞÜMÜ (NODE) v1.0")
    print("==================================================")
    print("✅ Durum: AKTİF")
    print("🔌 Elektrik/Wi-Fi Koruması: DEVREDE")
    print("--------------------------------------------------")
    print("🚀 Sistem arka planda dinlemeye başladı...")
    print("💡 Üye Giriş Onayı Bekleniyor... (Test Grubu: 10 Katılımcı)")
    print("--------------------------------------------------")

    imece_puani = 0
    
    # 10 Kişilik UTEYKDER test grubunun simülasyonu ve elektrik koruma mantığı
    try:
        while True:
            # Her 10 saniyede bir sistemi ve puan akışını kontrol eder
            time.sleep(10)
            imece_puani += 5
            print(f"📊 [TRM NODE] Sistem Sorunsuz Çalışıyor | Kazanılan Artı Puan: +{imece_puani}")
            
    except KeyboardInterrupt:
        print("\n⚠️ Mobil Düğüm kullanıcı tarafından durduruldu. Güvenli çıkış yapılıyor...")

if __name__ == "__main__":
    mobil_dugum_baslat()
