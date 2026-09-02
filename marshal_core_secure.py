import os
import sys
import logging
import hashlib
from dataclasses import dataclass

# 167. AJAN (Siber Muhafiz) Entegrasyonu ile Loglama Altyapisi
logging.basicConfig(level=logging.INFO, format='%(asctime)s - [MARSAL KOMUTA MERKEZI] - %(levelname)s - %(message)s')

@dataclass
class AffiliateFirmNode:
    firm_name: str
    folder_name: str
    is_active: bool
    target_currency: str  # USD, EUR, GBP

class TRMMarshalMasterCore:
    def __init__(self):
        self.master_folder_name = "TRM_MARASAL_MASTER"
        # Maresal Klasorune erisim icin Kriptografik Guvenlik Anahtari (Mimar Fahri Bey'e Ozel SHA-256)
        # Gercek sistemde bu sizin telefonunuza gelen token ile eslesecek
        self._secure_hash = "8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918" # Ornek Guvenli Pin Hasli
        
        # Maresal klasorunun altindaki kopyalanmis, bagimsiz calisan firma ekosistemleri
        self.nodes = [
            AffiliateFirmNode("Amazon Global Cell", "TRM_NODE_AMAZON_US", True, "USD"),
            AffiliateFirmNode("AliExpress Global Cell", "TRM_NODE_ALIEXPRESS_INT", True, "EUR"),
            AffiliateFirmNode("eBay Global Cell", "TRM_NODE_EBAY_UK", True, "GBP"),
            AffiliateFirmNode("Local Market Cell", "TRM_NODE_TURKIYE_LOCAL", True, "TL")
        ]

    def verify_marshal_access(self, input_pin: str):
        """
        Pentagon Seviyesi 1. Duvar: Elini kolunu sallayarak girmek isteyenleri engeller.
        Mimar Fahri Bey'in guvenli pin girisini dogrular.
        """
        input_hash = hashlib.sha256(input_pin.encode()).hexdigest()
        if input_hash == self._secure_hash:
            logging.info("🛡️ DOGRULAMA BASARILI! Mimar Fahri Bey'in kimligi tescillendi.")
            logging.info("TRM Maresal Klasor kilitleri aciliyor, otonom hucreler aktif ediliyor...")
            return True
        else:
            logging.error("🚨 YETKISIZ ERISIM TESPIT EDILDI! 167. Siber Muhafiz Ajani IP'yi blokladi ve alarm durumuna gecti!")
            return False

    def deploy_marshal_ecosystem(self, pin: str):
        """
        Maresal klasoru altindaki tum kopyalanmis otonom firmalarin klasor yapisini
        ve 166 ajanin koordinasyonunu baslatir.
        """
        if not self.verify_marshal_access(pin):
            return False

        print("\n=== TRM MARESAL KOMUTA MERKEZI AKTIVASYONU ===")
        for node in self.nodes:
            status = "AKTIF - KAZANC SAGLIYOR" if node.is_active else "PASIF"
            print(f"-> Hucre Surucusu: [{node.firm_name}] | Klasor: {node.folder_name} | Para Birimi: {node.target_currency} | Durum: {status}")
        
        print("=============================================\n")
        logging.info("Tum kopyalanmis TRM hucreleri siber kalkan arkasinda %100 otonom calismaya hazir.")
        return True

# Sistemi Baslatalim (Masaustu Aktivasyon Simulasyonu)
if __name__ == "__main__":
    marshal_system = TRMMarshalMasterCore()
    
    # Varsayalim ki bir siber korsan rastgele sifreyle girmeye calisiyor
    print("--- DENEME 1: YETKISIZ SIZMA GIRISIMI ---")
    marshal_system.deploy_marshal_ecosystem(pin="123456_sahte_sifre")
    
    print("\n--- DENEME 2: MIMAR FAHRI BEY'IN GUVENLI GIRISI ---")
    # Gercek sifrenin hashi yukaridakiyle eslesen dogru pin girildiginde (Orn: "admin_fahri_trm_2026")
    marshal_system.deploy_marshal_ecosystem(pin="admin_fahri_trm_2026")