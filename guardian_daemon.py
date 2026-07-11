import threading
import time
from datetime import datetime
from trm_agents.guardian_agent import GuardianAgent
from trm_agents.self_healing import SelfHealingManager
from trm_agents.scaling_agent import ScalingAgent

def guardian_loop():
    guardian = GuardianAgent()
    healer = SelfHealingManager()
    scaler = ScalingAgent()
    
    print("[SİSTEM] 🛡️ Gözcü Ajanlar devrede, izleme başladı...")
    print("[SİSTEM] 🔄 Her 60 saniyede bir loglar taranacak.\n")
    
    while True:
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        # 1. Guardian tarama
        print(f"[{timestamp}] 📡 Guardian tarıyor...")
        alerts = guardian.run_once()
        
        # 2. Hataları onar
        if alerts:
            print(f"[{timestamp}] 🚨 {len(alerts)} hata bulundu! Onarılıyor...")
            healer.process_guardian_alerts(alerts)
        else:
            print(f"[{timestamp}] ✅ Hata tespit edilmedi.")
        
        # 3. Yük kontrolü
        scaling_decisions = scaler.scale_if_needed()
        if scaling_decisions:
            print(f"[{timestamp}] ⚖️ {len(scaling_decisions)} ölçeklendirme kararı alındı.")
        
        # 4. Kalp atışı
        print(f"[{timestamp}] 💓 Tarama tamamlandı, 60 saniye uyku...\n")
        time.sleep(60)

if __name__ == "__main__":
    # Daemon'u ayrı bir thread'de başlat
    t = threading.Thread(target=guardian_loop, daemon=True)
    t.start()
    
    # Ana thread'i canlı tut
    print("[SİSTEM] 🟢 Daemon arka planda çalışıyor. Çıkmak için Ctrl+C basın.\n")
    while True:
        time.sleep(10)