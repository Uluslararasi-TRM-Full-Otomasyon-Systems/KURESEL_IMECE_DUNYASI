# omni_dashboard_sync.py - Merkezi Akıllı Olay Paneli ve Bildirim Motoru
import os
import json
from datetime import datetime

class OmniDashboardSync:
    def __init__(self):
        self.status_file = "reports/system_status.json"
        os.makedirs("reports", exist_ok=True)

    def update_status(self, modul_adi, durum, detay=""):
        """Sistemdeki modüllerin anlık durumunu merkezi dosyaya kaydeder."""
        data = {}
        if os.path.exists(self.status_file):
            try:
                with open(self.status_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
            except json.JSONDecodeError:
                data = {}

        data[modul_adi] = {
            "durum": durum,
            "detay": detay,
            "son_guncelleme": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        with open(self.status_file, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        
        print(f"📊 [Dashboard] {modul_adi} durumu güncellendi: {durum}")

if __name__ == "__main__":
    ods = OmniDashboardSync()
    ods.update_status("SelfHealingCore", "Aktif", "Sistem hatasız çalışıyor.")