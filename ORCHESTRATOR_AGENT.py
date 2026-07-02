# ORCHESTRATOR_AGENT.py - TAM VE GUNCEL HALI

from SHIELD_AGENT import ShieldAgent
from SENTIMENT_TREND_AGENT import SentimentTrendAgent
from FINANCIAL_DISPATCH_AGENT import FinancialDispatchAgent
from TREASURY_KEEPER_AGENT import TreasuryKeeperAgent
from ACTIVITY_PROTECTOR_AGENT import ActivityProtectorAgent

class OrchestratorAgent:
    def __init__(self):
        print("ORCHESTRATOR_AGENT: Ajanlar yukleniyor...")
        self.agents = {
            "shield": ShieldAgent(),
            "sentiment": SentimentTrendAgent(),
            "financial": FinancialDispatchAgent(),
            "treasury": TreasuryKeeperAgent(),
            "protector": ActivityProtectorAgent()
        }
        print(f"ORCHESTRATOR_AGENT: {len(self.agents)} ajan basariyla baglandi.")

    def run_all(self):
        print("ORCHESTRATOR_AGENT: Tum ajanlar tetikleniyor...")
        for name, agent in self.agents.items():
            try:
                if hasattr(agent, 'run'):
                    agent.run()
                else:
                    print(f"UYARI: {name} ajani run() metoduna sahip degil!")
            except Exception as e:
                print(f"HATA: {name} ajani calisirken coktu: {e}")

if __name__ == "__main__":
    # Test amacli manuel baslatma
    orchestrator = OrchestratorAgent()
    orchestrator.run_all()