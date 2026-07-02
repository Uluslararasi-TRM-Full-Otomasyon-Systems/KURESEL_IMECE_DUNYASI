# FINANCIAL_DISPATCH_AGENT.py (Gercek Dagitim Motoru)
class FinancialDispatchAgent:
    def __init__(self):
        # GERCEK ORANLAR (Arka plan/Sistem ici)
        self.sirket_gercek_payi = 0.70
        self.uye_gercek_payi = 0.30

    def calculate_distribution(self, total_commission):
        # Devlete bildirim ve vergi kesintisi sonrasi net dagitim
        sirket_net = total_commission * self.sirket_gercek_payi
        # HATA DUZELTILDI: self.uye_payi yerine self.uye_gercek_payi kullanildi
        uye_net = total_commission * self.uye_gercek_payi
        return {"sirket": sirket_net, "uye": uye_net}

    def process_payment(self, member_id, total_commission):
        # Arka planda gercek oranlara gore dagitim yap
        result = self.calculate_distribution(total_commission)
        print(f"[LOG] {member_id} icin {result['uye']} TL hesaplara aktarildi.")
        return result