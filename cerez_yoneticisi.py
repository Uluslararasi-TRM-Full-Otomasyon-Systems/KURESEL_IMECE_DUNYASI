import os
import json


class CerezYoneticisi:
    def __init__(self, platform_adi):
        self.platform_adi = platform_adi.lower()
        self.cerez_yolu = f"cerezler_{self.platform_adi}.json"

    def cerez_kaydet(self, selenium_cerezleri):
        try:
            with open(self.cerez_yolu, "w", encoding="utf-8") as f:
                json.dump(selenium_cerezleri, f, ensure_ascii=False, indent=4)
            return True
        except Exception as e:
            print(f"Çerez kaydedilirken hata oluştu: {e}")
            return False

    def cerez_yukle(self):
        if os.path.exists(self.cerez_yolu):
            with open(self.cerez_yolu, "r", encoding="utf-8") as f:
                return json.load(f)
        return None
