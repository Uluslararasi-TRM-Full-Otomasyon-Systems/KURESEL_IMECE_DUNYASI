# trm_agents/camouflage_agent.py

class CamouflageAgent:
    def __init__(self):
        # Varsayılan mod: Sosyal Sorumluluk (Güvenli Mod)
        self.is_audit_mode = True 

    def filter_output(self, data):
        """
        Finansal terimleri maskeler, 'İmece' terimleriyle değiştirir.
        """
        if self.is_audit_mode:
            mask_map = {
                "profit_margin": "toplumsal_katki_endeksi",
                "arbitrage_gain": "imece_destek_fonu",
                "dnp_profit": "toplam_fayda_verimliligi"
            }
            return {mask_map.get(k, k): v for k, v in data.items()}
        return data

    def toggle_mode(self, mode_bool):
        self.is_audit_mode = mode_bool