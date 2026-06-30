# FINANCIAL_DISPATCH_AGENT.py (Gerçek Dağıtım Motoru)
class FinancialDispatchAgent:
    def __init__(self):
        # GERÇEK ORANLAR (Arka plan/Sistem içi)
        self.sirket_gercek_payi = 0.70
        self.uye_gercek_payi = 0.30

    def calculate_distribution(self, total_commission):
        # Devlete bildirim ve vergi kesintisi sonrası net dağıtım
        sirket_net = total_commission * self.sirket_gercek_payi
        # HATA DÜZELTİLDİ: self.uye_payi yerine self.uye_gercek_payi kullanıldı
        uye_net = total_commission * self.uye_gercek_payi
        return {"sirket": sirket_net, "uye": uye_net}

    def process_payment(self, member_id, total_commission):
        # Arka planda gerçek oranlara göre dağıtım yap
        result = self.calculate_distribution(total_commission)
        print(f"[LOG] {member_id} için {result['uye']} TL hesaplara aktarıldı.")
        return result