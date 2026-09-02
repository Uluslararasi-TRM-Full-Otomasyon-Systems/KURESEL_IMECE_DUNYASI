import random
import time
import json
import os
from datetime import datetime

class UltraNirvanaGuardian:
    def __init__(self, log_path="ultra_guardian_audit.json"):
        self.log_path = log_path
        self.load_audit_logs()

    def load_audit_logs(self):
        if os.path.exists(self.log_path):
            with open(self.log_path, "r", encoding="utf-8") as f:
                self.audit_data = json.load(f)
        else:
            self.audit_data = {"total_operations": 0, "quarantined_actions": []}
            self.save_audit_logs()

    def save_audit_logs(self):
        with open(self.log_path, "w", encoding="utf-8") as f:
            json.dump(self.audit_data, f, indent=4, ensure_ascii=False)

    def human_behavior_simulation(self, agent_name):
        """
        1. Biyolojik Simülasyon (Human Mimicry): Ajanların işlemler arasında 
        gerçek bir insanın yorulma, düşünme veya odaklanma sürelerini taklit eder.
        """
        # Gece saatlerinde işlem hızını yavaşlat (doğal insan akışı)
        current_hour = datetime.now().hour
        base_delay = random.uniform(2.0, 6.0)
        
        if 1 <= current_hour <= 6:
            base_delay *= random.uniform(1.8, 3.0) # Gece daha yavaş ve temkinli
            
        time.sleep(base_delay)
        return base_delay

    def dynamic_agent_quarantine_check(self, agent_id, risk_score):
        """
        2. Karantina ve Risk Analizi: Anormal aktivite gösteren veya 
        algoritma şüphesi taşıyan ajanı anında izole eder.
        """
        if risk_score > 0.85:
            quarantine_record = {
                "agent_id": agent_id,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "risk_score": risk_score,
                "status": "QUARANTINED"
            }
            self.audit_data["quarantined_actions"].append(quarantine_record)
            self.save_audit_logs()
            print(f"[ULTRA-GUARDIAN ALARMI] Ajan {agent_id} yüksek risk ({risk_score}) nedeniyle karantinaya alındı!")
            return False # İşlemi engelle
        return True

    def record_operation(self, agent_id, operation_type):
        self.audit_data["total_operations"] += 1
        self.save_audit_logs()

# Test Çalıştırması
if __name__ == "__main__":
    guardian = UltraNirvanaGuardian()
    print("[*] Ultra Nirvana Guardian Ajanı Devrede.")
    delay = guardian.human_behavior_simulation("Test_Agent_01")
    print(f"[*] Simüle edilen insan gecikme süresi: {delay:.2f} saniye")