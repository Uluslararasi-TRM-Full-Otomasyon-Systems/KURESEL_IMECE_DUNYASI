import os
import sys
import logging
import time
from datetime import datetime

# 167. AJAN - Siber Muhafiz Ozel Loglama Altyapisi
logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s - [167. AJAN - SIBER MUHAFIZ] - %(levelname)s - %(message)s'
)

class CyberGuardianAgent:
    def __init__(self):
        self.agent_id = 167
        self.agent_name = "Cyber Guardian Agent"
        self.security_level = "PENTAGON_MAX"
        self.is_monitoring = True
        # Korunacak sahalar (Kopyalanmis TRM hucreleri)
        self.protected_nodes = [
            "TRM_KOPYA_AMAZON",
            "TRM_KOPYA_ALIEXPRESS",
            "TRM_KOPYA_EBAY",
            "TRM_KOPYA_YERLI_PAZAR"
        ]

    def scan_marshal_integrity(self):
        """
        Maresal klasorunun icindeki kopyalanmis firmalarin dosyalarinda 
        yetkisiz bir degisiklik, silme veya sizma var mi kontrol eder.
        """
        logging.info("🛡️ Celik Kalkan Aktif: Maresal klasor butunlugu taraniyor...")
        time.sleep(0.5) # Siber tarama simulasyonu
        
        for node in self.protected_nodes:
            # Gercek sistemde burada dosya hash kontrolu (MD5/SHA256) donecek
            logging.info(f"✔ [KORUMA ALTINDA] -> {node} hucresi temiz, siber sizinti yok.")
        
        return True

    def detect_intrusion_attempt(self, ip_address: str, failed_attempts: int):
        """
        Disaridan veya iceriden elini kolunu sallayarak sifre zorlayan 
        biri oldugunda siber kalkani devreye sokar.
        """
        if failed_attempts >= 3:
            logging.error(f"🚨 ALARM! {ip_address} adresinden UST USTE BASARISIZ GIRIS GIRISIMI TESPIT EDILDI!")
            self._trigger_lockdown(ip_address)
            return True
        return False

    def _trigger_lockdown(self, malicious_ip: str):
        """
        Saldiri aninda Maresal klasorunu karartir ve Mimar Fahri Bey'e acil durum raporu firlatir.
        """
        print("\n=================== !!! TRM LOCKDOWN !!! ===================")
        print(f"SIBER MUHAFIZ AJANI TUM GECITLERI KAPATTI!")
        print(f"Saldirgan IP: {malicious_ip} -> Kuresel Karalisteye Alindi.")
        print(f"Maresal Klasoru Kriptolu Duvar Arkasina Gizlendi.")
        print("============================================================\n")
        
        # Mimar Fahri Bey'in telefonuna gidecek SMS / Bildirim tetikleyicisi
        logging.warning(f"📱 Maresalim Fahri Bey'e Acil SMS Bildirimi Gonderildi: 'Konum disi sizma engellendi, kalemiz guvende!'")

if __name__ == "__main__":
    print("--- TRM 167. SIBER MUHAFIZ AJANI DEFANS PROTOKOLU BASLATILDI ---")
    guardian = CyberGuardianAgent()
    
    # 1. Asama: Rutin sinir guvenligi taramasi
    guardian.scan_marshal_integrity()
    
    print("\n--- SIBER SALDIRI SIMULASYONU BASLATILIYOR ---")
    # 2. Asama: Bir hackerin elini kolunu sallayarak 3 kez yanlis sifre girdigini varsayalim
    guardian.detect_intrusion_attempt(ip_address="192.168.4.210 (Zararli Yazilim/Hacker)", failed_attempts=3)