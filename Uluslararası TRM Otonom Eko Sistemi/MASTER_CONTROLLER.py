from ORCHESTRATOR_AGENT import OrchestratorAgent

class MasterController:
    def __init__(self):
        self.orchestrator = OrchestratorAgent()
        print("MASTER CONTROLLER: Ajanlar yüklendi.")

    def run(self):
        self.orchestrator.run_all()

if __name__ == "__main__":
    mc = MasterController()
    mc.run()