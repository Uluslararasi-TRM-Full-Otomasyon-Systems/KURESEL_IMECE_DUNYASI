# TREASURY_KEEPER_AGENT.py
class TreasuryKeeperAgent:
    def __init__(self):
        # Hesap bakiyeleri (Sistemsel simülasyon)
        self.balances = {"TL": 50000, "EURO": 2000, "USD": 2500}

    def request_approval_hybrid(self, expense_type, amount, currency):
        """Hibrit onay mekanizması: Buton veya Sesli komut için hazır."""
        print(f"[BİLDİRİM] {expense_type} için {amount} {currency} ödeme onayı bekleniyor.")
        print("-> [BUTON] Panel üzerinden 'ONAYLA' tuşuna basabilirsiniz.")
        print("-> [SESLİ] Lütfen sesli olarak 'Onaylıyorum' komutunu iletin.")
        return "WAITING_FOR_INPUT"

    def execute_payment(self, expense_type, amount, currency, confirmation):
        """Onay alındıktan sonra ödemeyi gerçekleştiren güvenli modül."""
        if confirmation.lower() in ["onaylıyorum", "onayla", "evet"]:
            if self.balances.get(currency, 0) >= amount:
                self.balances[currency] -= amount
                print(f"[BAŞARILI] {expense_type} ödemesi {currency} hesabından yapıldı. Kalan: {self.balances[currency]}")
                return True
            else:
                print(f"[HATA] {currency} hesabında bakiye yetersiz.")
        else:
            print(f"[İPTAL] {expense_type} ödemesi onaylanmadı.")
        return False

if __name__ == "__main__":
    # Test Modu: Ajan hazır
    keeper = TreasuryKeeperAgent()
    status = keeper.request_approval_hybrid("Sunucu_Kirasi", 1200, "TL")
    if status == "WAITING_FOR_INPUT":
        # Simülasyon: Sesli veya butonlu komut geldiğini varsayalım
        keeper.execute_payment("Sunucu_Kirasi", 1200, "TL", "onaylıyorum")