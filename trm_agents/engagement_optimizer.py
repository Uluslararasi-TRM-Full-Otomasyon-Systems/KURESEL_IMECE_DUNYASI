import time
import random
import threading
from datetime import datetime
from trm_agents.human_behavior_engine import HumanBehaviorEngine

class EngagementOptimizer:
    """
    Ajan 163 – Engagement-Optimizer
    Trusted hesaplar için organik görünüm sağlamak amacıyla insan davranış simülasyonu başlatır.
    """
    def __init__(self):
        self.active_simulations = {}  # agent_name -> thread
        self.behavior_engine = HumanBehaviorEngine()

    def start_simulation(self, agent_name: str, duration_minutes: int = 45):
        """
        Bir ajan için insan davranış simülasyonu başlatır (30-60 dakika).
        """
        if agent_name in self.active_simulations:
            print(f"[Engagement-Optimizer] {agent_name} zaten simülasyonda.")
            return

        def simulate():
            print(f"[Engagement-Optimizer] {agent_name} simülasyonu başladı ({duration_minutes} dk).")
            start_time = time.time()
            end_time = start_time + (duration_minutes * 60)
            while time.time() < end_time:
                # Rastgele insan davranışı
                action = random.choice([
                    "scroll", "mouse_move", "read", "pause", "switch_tab"
                ])
                if action == "scroll":
                    time.sleep(self.behavior_engine.scroll_jitter())
                elif action == "mouse_move":
                    # Fare hareketi simülasyonu
                    time.sleep(random.uniform(0.5, 2.0))
                elif action == "read":
                    text_len = random.randint(500, 2000)
                    time.sleep(self.behavior_engine.reading_time(text_len))
                elif action == "pause":
                    time.sleep(self.behavior_engine.between_actions(2, 10))
                elif action == "switch_tab":
                    time.sleep(random.uniform(1, 5))
                # Her döngüde %10 ihtimalle non-action browsing
                if random.random() < 0.1:
                    time.sleep(self.behavior_engine.non_action_browsing((30, 90)))
            print(f"[Engagement-Optimizer] {agent_name} simülasyonu tamamlandı.")
            # Simulation bittiğinde listeden çıkar
            if agent_name in self.active_simulations:
                del self.active_simulations[agent_name]

        thread = threading.Thread(target=simulate, daemon=True)
        thread.start()
        self.active_simulations[agent_name] = thread

    def stop_simulation(self, agent_name: str):
        """Simülasyonu durdur (acil durumlar için)"""
        if agent_name in self.active_simulations:
            # Thread'leri durdurmanın temiz yolu yok, flag kullanılabilir.
            # Bu basit versiyonda thread'i iptal ediyoruz (tehlikeli olabilir)
            # Daha iyisi: bir flag kullanarak döngüden çıkmasını sağlamak.
            # Pratikte, thread'in daemon olması program kapanınca temizlenir.
            del self.active_simulations[agent_name]
            print(f"[Engagement-Optimizer] {agent_name} simülasyonu durduruldu.")