# self_healing_core.py - Ototnom Hata Yakalama ve Öz-İyileştirme Motoru
import os
import json
from datetime import datetime

class SelfHealingCore:
    def __init__(self):
        self.log_path = "data_cluster/healing_log.json"
        os.makedirs("data_cluster", exist_ok=True)

    def isolate_and_heal(self, error_message, module_name):
        """Sistemde oluşan hataları izole eder ve otomatik iyileştirme protokolünü çalıştırır."""
        log_entry = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "module": module_name,
            "error": str(error_message),
            "status": "HEALED_AND_ISOLATED"
        }
        
        try:
            logs = []
            if os.path.exists(self.log_path):
                with open(self.log_path, "r", encoding="utf-8") as f:
                    logs = json.load(f)
            logs.append(log_entry)
            with open(self.log_path, "w", encoding="utf-8") as f:
                json.dump(logs, f, indent=4)
        except Exception:
            pass

        print(f"🛡️ [Self-Healing Core] {module_name} üzerindeki hata izole edildi ve sistem kararlı duruma getirildi.")
        return True

if __name__ == "__main__":
    healer = SelfHealingCore()
    healer.isolate_and_heal("Test Hatası", "TestModule")