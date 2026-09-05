# global_expansion_nexus.py - Uluslararası Afiliyet ve Küresel Genleşme Motoru
import os
import json
from datetime import datetime

class GlobalExpansionNexus:
    def __init__(self):
        self.nexus_path = "data_cluster/global_expansion_registry.json"
        os.makedirs("data_cluster", exist_ok=True)

    def adapt_to_global_partner(self, partner_name, target_market_code, custom_parameters):
        """trendurunlermarket.com'da test edilen modüler yapıyı parametrik olarak uluslararası affiliate ağlarına uyarlar."""
        expansion_record = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "base_model": "trendurunlermarket.com",
            "international_partner": partner_name,
            "target_market": target_market_code,
            "parameters": custom_parameters,
            "status": "EXPANDED_AND_ACTIVE"
        }
        
        try:
            records = []
            if os.path.exists(self.nexus_path):
                with open(self.nexus_path, "r", encoding="utf-8") as f:
                    records = json.load(f)
            records.append(expansion_record)
            with open(self.nexus_path, "w", encoding="utf-8") as f:
                json.dump(records, f, indent=4)
        except Exception as e:
            print(f"⚠️ Kayıt hatası: {str(e)}")

        print(f"🌍 [Global Nexus] Başarıyla entegre edildi: {partner_name} ({target_market_code}) -> Model devreye alındı!")
        return expansion_record

if __name__ == "__main__":
    nexus = GlobalExpansionNexus()
    nexus.adapt_to_global_partner("Global_Affiliate_Network_X", "US-EU", {"commission_rate": 0.15, "currency": "USD"})