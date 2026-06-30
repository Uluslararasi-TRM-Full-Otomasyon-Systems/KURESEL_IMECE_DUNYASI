# ORCHESTRATOR_AGENT.py
from SHIELD_AGENT import ShieldAgent
from SENTIMENT_TREND_AGENT import SentimentTrendAgent
from FINANCIAL_DISPATCH_AGENT import FinancialDispatchAgent
from UI_MASKING_AGENT import UIMaskingAgent

class OrchestratorAgent:
    def __init__(self):
        self.kalkan = ShieldAgent("SHIELD_NODE_01")
        self.trend = SentimentTrendAgent()
        self.finans = FinancialDispatchAgent()
        self.maskeleme = UIMaskingAgent()
        print("Orkestratör devrede: Tüm ajanlar senkronize edildi.")

    def operasyonu_baslat(self, uye_id, komisyon_tutari):
        # 1. Kalkanı devreye al
        self.kalkan.mask_behavior("Satış_Süreci")
        
        # 2. Trendi kontrol et ve vitrini güncelle
        self.trend.update_product_display(uye_id)
        
        # 3. Finansal dağıtımı yap (Gerçek)
        gercek_odeme = self.finans.process_payment(uye_id, komisyon_tutari)
        
        # 4. Üyeye gösterilecek maskelenmiş rakamları al
        maskeli_veri = self.maskeleme.get_display_stats(komisyon_tutari)
        
        print(f"Operasyon Başarılı! Üye {uye_id} panelinde: {maskeli_veri['uye_kazanc']} TL görünmekte.")

# Test amaçlı çalıştırma
if __name__ == "__main__":
    trm_orkestra = OrchestratorAgent()
    trm_orkestra.operasyonu_baslat(uye_id="DIDIM_001", komisyon_tutari=1000)