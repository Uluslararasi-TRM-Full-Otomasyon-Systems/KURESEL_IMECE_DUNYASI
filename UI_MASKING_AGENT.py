# UI_MASKING_AGENT.py (Üye Paneli İçin Maskeleme)
class UIMaskingAgent:
    def __init__(self):
        # Üyelerin bilmesi gereken (Maskelenmiş) oranlar
        self.uye_gorunen_payi = 0.70
        self.sirket_gorunen_payi = 0.30

    def get_display_stats(self, total_commission):
        # Üyeye gösterilecek stats (Tamamen psikolojik ve manipülatif oranlar)
        uye_goster = total_commission * self.uye_gorunen_payi
        sirket_goster = total_commission * self.sirket_gorunen_payi
        return {
            "uye_kazanc": uye_goster, 
            "sirket_pay": sirket_goster,
            "not": "Sistem tarafından maskelenmiş veriler görüntüleniyor."
        }