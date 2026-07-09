# TREASURY_KEEPER_AGENT.py
class TreasuryKeeperAgent:
    def __init__(self):
        # Hesap bakiyeleri (Sistemsel simulasyon)
        self.balances = {"TL": 50000, "EURO": 2000, "USD": 2500}

    def request_approval_hybrid(self, expense_type, amount, currency):
        """Hibrit onay mekanizmasi: Buton veya Sesli komut icin hazir."""
        print(f"[BILDIRIM] {expense_type} icin {amount} {currency} odeme onayi bekleniyor.")
        print("-> [BUTON] Panel uzerinden 'ONAYLA' tusuna basabilirsiniz.")
        print("-> [SESLI] Lutfen sesli olarak 'Onayliyorum' komutunu iletin.")
        return "WAITING_FOR_INPUT"

    def execute_payment(self, expense_type, amount, currency, confirmation):
        """Onay alindiktan sonra odemeyi gerceklestiren guvenli modul."""
        if confirmation.lower() in ["onayliyorum", "onayla", "evet"]:
            if self.balances.get(currency, 0) >= amount:
                self.balances[currency] -= amount
                print(f"[BASARILI] {expense_type} odemesi {currency} hesabindan yapildi. Kalan: {self.balances[currency]}")
                return True
            else:
                print(f"[HATA] {currency} hesabinda bakiye yetersiz.")
        else:
            print(f"[IPTAL] {expense_type} odemesi onaylanmadi.")
        return False

if __name__ == "__main__":
    # Test Modu: Ajan hazir
    keeper = TreasuryKeeperAgent()
    status = keeper.request_approval_hybrid("Sunucu_Kirasi", 1200, "TL")
    if status == "WAITING_FOR_INPUT":
        # Simulasyon: Sesli veya butonlu komut geldigini varsayalim
        keeper.execute_payment("Sunucu_Kirasi", 1200, "TL", "onayliyorum")