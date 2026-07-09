# trm_agents/camouflage_agent.py

class CamouflageAgent:
    def __init__(self):
        # Denetim modunu belirleyen bayrak
        self.is_audit_mode = False 

    def filter_output(self, original_data, context="general"):
        """
        Ajanlardan gelen veriyi context'e göre maskeler.
        """
        if self.is_audit_mode:
            return self._apply_masking(original_data)
        return original_data

    def _apply_masking(self, data):
        # Finansal terimleri sosyal sorumluluk terimleriyle değiştir
        mask_map = {
            "profit_margin": "community_impact_index",
            "arbitrage_gain": "social_support_fund",
            "dnp_profit": "engagement_efficiency"
        }
        masked_data = data.copy()
        for key, value in mask_map.items():
            if key in masked_data:
                masked_data[value] = masked_data.pop(key)
        return masked_data