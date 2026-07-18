from utils.config_loader import load_config

class DNPAgent:
    def __init__(self, name="DNP-161"):
        self.name = name
        self.config = load_config()

    def refresh_config(self):
        self.config = load_config()

    def denetle(self, agent_list):
        self.refresh_config()
        esikler = self.config["dnp"]["parametre_esik_degerleri"]
        uyarilar = []
        for agent in agent_list:
            if hasattr(agent, 'cpu_yuk') and agent.cpu_yuk > esikler["cpu_esik_yuzde"]:
                uyarilar.append(f"⚠️ {agent.name} CPU yükü (%{agent.cpu_yuk}) eşiği aştı.")
            if hasattr(agent, 'api_gecikme') and agent.api_gecikme > esikler["api_gectikme_ms"]:
                uyarilar.append(f"⚠️ {agent.name} API gecikmesi ({agent.api_gecikme} ms) eşiği aştı.")
        if uyarilar:
            print(f"[{self.name}] Denetim raporu:")
            for uyari in uyarilar:
                print(uyari)
        else:
            print(f"[{self.name}] Tüm ajanlar normal.")
        return uyarilar