# Bu hook, ana sistem dongusu (main loop) icerisine yerlestirilmelidir.
from trm_agents.governance import (
    CollectiveSyncLead,
    EthicalComplianceGuardian,
    SelfHealingSentinel,
)


class GovernanceBridge:
    def __init__(self):
        self.ethical = EthicalComplianceGuardian()
        self.sync = CollectiveSyncLead()
        self.sentinel = SelfHealingSentinel()

    def run_governance_cycle(self, current_log):
        self.ethical.audit_decision(current_log)
        self.sync.synchronize(current_log)
        self.sentinel.run_diagnosis(current_log)


# Entegrasyon notu: Bu yapiyi MASTER_CONTROLLER.py icerisinde
# ana dongunun sonuna ekle.
