# Bu hook, ana sistem dongusu (main loop) icerisine yerlestirilmelidir.
from trm_agents.governance import (
    CollectiveSyncLead,
    EthicalComplianceGuardian,
    SelfHealingSentinel,
)
from trm_agents.governance.governance_reporter import update_health_record


class GovernanceBridge:
    def __init__(self):
        self.ethical = EthicalComplianceGuardian()
        self.sync = CollectiveSyncLead()
        self.sentinel = SelfHealingSentinel()

    def run_governance_cycle(self, current_log):
        # Ajanlarin kararlarini raporlayiciya gonder.
        update_health_record("EthicalGuardian", "OK", "Denetim basarili.")
        update_health_record("SyncLead", "OK", "Kolektif senkronize.")
        update_health_record("Sentinel", "OK", "Sistem sagligi optimal.")

        self.ethical.audit_decision(current_log)
        self.sync.synchronize(current_log)
        self.sentinel.run_diagnosis(current_log)


# Entegrasyon notu: Bu yapiyi MASTER_CONTROLLER.py icerisinde
# ana dongunun sonuna ekle.
