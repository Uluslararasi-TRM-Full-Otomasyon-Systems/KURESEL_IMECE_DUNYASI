class SentinelAgent:
    def __init__(self):
        # Hesapların sağlık durumunu anlık takip eden sistem hafızası
        self.karantina_listesi = set()

    def saglik_kontrolu(self, hesap_id, mevcut_etkilezim, esik_deger=5):
        """Hesabın algoritma tarafından kısıtlanıp kısıtlanmadığını denetler."""
        if hesap_id in self.karantina_listesi:
            print(f"[NÖBETÇİ] {hesap_id} zaten karantinada! İşlem engellendi.")
            return False

        if mevcut_etkilezim < esik_deger:
            print(f"[NÖBETÇİ UYARI] {hesap_id} numaralı hesapta KRİTİK etkileşim düşüşü!")
            print(f"[NÖBETÇİ] Algoritma takibi sezildi. {hesap_id} ÖNLEM OLARAK KARANTİNAYA ALINDI.")
            self.karantina_listesi.add(hesap_id)
            return False  # Bu hesap için otonom akışı durdur emri
        
        print(f"[NÖBETÇİ] {hesap_id} hesabı güvenli. Operasyon temiz.")
        return True