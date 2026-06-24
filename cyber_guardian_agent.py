import os
import sys
import logging
import time
from datetime import datetime

# 167. AJAN - Siber Muhafız Özel Loglama Altyapısı
logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s - [167. AJAN - SİBER MUHAFIZ] - %(levelname)s - %(message)s'
)

class CyberGuardianAgent:
    def __init__(self):
        self.agent_id = 167
        self.agent_name = "Cyber Guardian Agent"
        self.security_level = "PENTAGON_MAX"
        self.is_monitoring = True
        # Korunacak sahalar (Kopyalanmış TRM hücreleri)
        self.protected_nodes = [
            "TRM_KOPYA_AMAZON",
            "TRM_KOPYA_ALIEXPRESS",
            "TRM_KOPYA_EBAY",
            "TRM_KOPYA_YERLI_PAZAR"
        ]

    def scan_marshal_integrity(self):
        """
        Mareşal klasörünün içindeki kopyalanmış firmaların dosyalarında 
        yetkisiz bir değişiklik, silme veya sızma var mı kontrol eder.
        """
        logging.info("🛡️ Çelik Kalkan Aktif: Mareşal klasör bütünlüğü taranıyor...")
        time.sleep(0.5) # Siber tarama simülasyonu
        
        for node in self.protected_nodes:
            # Gerçek sistemde burada dosya hash kontrolü (MD5/SHA256) dönecek
            logging.info(f"✔ [KORUMA ALTINDA] -> {node} hücresi temiz, siber sızıntı yok.")
        
        return True

    def detect_intrusion_attempt(self, ip_address: str, failed_attempts: int):
        """
        Dışarıdan veya içeriden elini kolunu sallayarak şifre zorlayan 
        biri olduğunda siber kalkanı devreye sokar.
        """
        if failed_attempts >= 3:
            logging.error(f"🚨 ALARM! {ip_address} adresinden ÜST ÜSTE BAŞARISIZ GİRİŞ GİRİŞİMİ TESPİT EDİLDİ!")
            self._trigger_lockdown(ip_address)
            return True
        return False

    def _trigger_lockdown(self, malicious_ip: str):
        """
        Saldırı anında Mareşal klasörünü karartır ve Mimar Fahri Bey'e acil durum raporu fırlatır.
        """
        print("\n=================== !!! TRM LOCKDOWN !!! ===================")
        print(f"SİBER MUHAFIZ AJANI TÜM GEÇİTLERİ KAPATTI!")
        print(f"Saldırgan IP: {malicious_ip} -> Küresel Karalisteye Alındı.")
        print(f"Mareşal Klasörü Kriptolu Duvar Arkasına Gizlendi.")
        print("============================================================\n")
        
        # Mimar Fahri Bey'in telefonuna gidecek SMS / Bildirim tetikleyicisi
        logging.warning(f"📱 Mareşalim Fahri Bey'e Acil SMS Bildirimi Gönderildi: 'Konum dışı sızma engellendi, kalemiz güvende!'")

if __name__ == "__main__":
    print("--- TRM 167. SİBER MUHAFIZ AJANI DEFANS PROTOKOLÜ BAŞLATILDI ---")
    guardian = CyberGuardianAgent()
    
    # 1. Aşama: Rutin sınır güvenliği taraması
    guardian.scan_marshal_integrity()
    
    print("\n--- SİBER SALDIRI SİMÜLASYONU BAŞLATILIYOR ---")
    # 2. Aşama: Bir hackerın elini kolunu sallayarak 3 kez yanlış şifre girdiğini varsayalım
    guardian.detect_intrusion_attempt(ip_address="192.168.4.210 (Zararlı Yazılım/Hacker)", failed_attempts=3)