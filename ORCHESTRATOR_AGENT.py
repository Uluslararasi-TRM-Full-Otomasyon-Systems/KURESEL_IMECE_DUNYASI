# trm_agents/orchestrator_agent.py

from trm_agents.camouflage_agent import CamouflageAgent
# Diğer ajanlarını buraya import etmeye devam et
# from trm_agents.dnp_agent import DNPAgent
# from trm_agents.arbitrage_agent import ArbitrageAgent

class OrchestratorAgent:
    def __init__(self):
        self.camouflage = CamouflageAgent()
        # Denetim durumunu buradan manuel veya otomatik (network header ile) set edebilirsin
        # self.camouflage.is_audit_mode = True 
        
    def execute_agent_task(self, agent_instance, task_data):
        """
        Ara Katman (Middleware): Ajan çıktısını denetim kalkanından geçirir.
        """
        # 1. Görevi çalıştır
        raw_output = agent_instance.perform(task_data)
        
        # 2. ARA KATMAN: Kamuflaj kalkanını devreye sok
        # Denetim modundaysa veriyi maskeler, değilse olduğu gibi bırakır
        safe_output = self.camouflage.filter_output(raw_output)
        
        return safe_output

    def run_system(self):
        # Örnek: Sistem döngüsü
        print("Sistem operasyonel: Otonom fabrika çalışıyor...")
        # ... ajanların döngüleri buraya ...

# Orkestratörün başlatılması
orchestrator = OrchestratorAgent()