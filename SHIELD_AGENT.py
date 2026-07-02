# SHIELD_AGENT.py
import time
import random

class ShieldAgent:
    def __init__(self, agent_id="SHIELD_NODE_DEFAULT"):
        self.agent_id = agent_id
        self.status = "Aktif - Koruma Modunda"

    def organic_delay(self):
        # Algoritmalari sasirtmak icin insani gecikmeler ekler
        delay = random.uniform(2.5, 7.0)
        time.sleep(delay)

    def mask_behavior(self, action_type):
        print(f"[{self.agent_id}] {action_type} islemi icin organik imza olusturuluyor...")
        self.organic_delay()
        return True

# Ajan baslatildiginda calisacak mantik
if __name__ == "__main__":
    shield = ShieldAgent("SHIELD_NODE_01")
    print(f"{shield.agent_id} devreye alindi. Didim operasyonu guvende.")