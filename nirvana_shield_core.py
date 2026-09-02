import random
import time
import json
import os
from datetime import datetime

class NirvanaShieldCore:
    def __init__(self, config_path="nirvana_shield_config.json"):
        self.config_path = config_path
        self.load_config()
        
    def load_config(self):
        if os.path.exists(self.config_path):
            with open(self.config_path, "r", encoding="utf-8") as f:
                self.config = json.load(f)
        else:
            self.config = {
                "proxy_pool_active": True,
                "fingerprint_masking": True,
                "chaos_jitter_enabled": True,
                "circuit_breaker_status": "NORMAL"
            }
            self.save_config()

    def save_config(self):
        with open(self.config_path, "w", encoding="utf-8") as f:
            json.dump(self.config, f, indent=4, ensure_ascii=False)

    def apply_chaos_jitter(self, base_seconds=5):
        """
        3. Kaotik Zamanlama (Jitter): Robotik döngüleri kırmak için
        rastgele insan gecikmeleri ve 'düşünme payı' ekler.
        """
        if not self.config.get("chaos_jitter_enabled", True):
            return base_seconds
        
        # Gauss / Rastgele sapma ekle (Örn: 5 saniye baz alınırsa 3 ile 12 saniye arası rastgele bekler)
        jitter = random.uniform(0.5, 2.5)
        total_wait = base_seconds * jitter + random.randint(2, 7)
        time.sleep(total_wait)
        return total_wait

    def get_masked_fingerprint(self, user_id):
        """
        2. Tarayıcı Parmak İzi Maskelemesi: Her kullanıcı/oturum için 
        benzersiz donanım ve tarayıcı imzası üretir.
        """
        if not self.config.get("fingerprint_masking", True):
            return {"status": "standard"}
            
        platforms = ["Win32", "MacIntel", "Linux x86_64"]
        resolutions = ["1920x1080", "1440x900", "1366x768", "2560x1440"]
        languages = ["tr-TR,tr;q=0.9,en-US;q=0.8", "en-US,en;q=0.9", "tr,en;q=0.5"]
        
        # Kullanıcı kimliğine dayalı sabit ama farklılaştırılmış imza
        random.seed(str(user_id))
        fingerprint = {
            "platform": random.choice(platforms),
            "screen_resolution": random.choice(resolutions),
            "accept_language": random.choice(languages),
            "webgl_vendor": "Google Inc. (NVIDIA)",
            "canvas_hash": hex(random.randint(10000000, 99999999))
        }
        random.seed(None) # Tohumu sıfırla
        return fingerprint

    def check_circuit_breaker(self, platform_name):
        """
        4. Devre Kesici (Circuit Breaker): Bir platformda hata veya ban 
        sinyali alınırca sistemi korumaya alır.
        """
        status = self.config.get("circuit_breaker_status", "NORMAL")
        if status == "TRIPPED":
            print(f"[!] DİKKAT: Devre kesici devrede! {platform_name} için işlemler geçici olarak durduruldu.")
            return False
        return True

    def trip_circuit_breaker(self, reason):
        """Acil durumda tüm sistemi güvenli moda alır."""
        self.config["circuit_breaker_status"] = "TRIPPED"
        self.save_config()
        print(f"[ALARM] Devre kesici tetiklendi! Sebep: {reason}")

# Test Çalıştırması
if __name__ == "__main__":
    shield = NirvanaShieldCore()
    print("[*] Nirvana Güvenlik Çekirdeği Başlatıldı.")
    fp = shield.get_masked_fingerprint("user_12345")
    print(f"[*] Örnek Maskelenmiş Parmak İzi: {fp}")