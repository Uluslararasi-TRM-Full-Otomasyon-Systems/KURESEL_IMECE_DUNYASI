class CoreNexus:
    def __init__(self, domain="trm-operations.net"):
        self.domain = domain
        self.agents = {} # Ajanları burada tutacağız

    def connect_agent(self, agent_name, agent_instance):
        """Ajanı sisteme bağlar ve yetkilendirir."""
        self.agents[agent_name] = agent_instance
        print(f"[CoreNexus] {agent_name} başarıyla sisteme bağlandı ve denetim altına alındı.")

    def run_system_sync(self):
        """Tüm bağlı ajanların altyapısını eş zamanlı çalıştırır."""
        for name, agent in self.agents.items():
            print(f"[CoreNexus] {name} senkronize ediliyor...")