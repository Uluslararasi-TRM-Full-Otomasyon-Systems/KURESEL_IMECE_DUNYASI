class SentinelAgent:
    def __init__(self):
        # Hesaplarin saglik durumunu anlik takip eden sistem hafizasi
        self.karantina_listesi = set()

    def saglik_kontrolu(self, hesap_id, mevcut_etkilezim, esik_deger=5):
        """Hesabin algoritma tarafindan kisitlanip kisitlanmadigini denetler."""
        if hesap_id in self.karantina_listesi:
            print(f"[NOBETCI] {hesap_id} zaten karantinada! Islem engellendi.")
            return False

        if mevcut_etkilezim < esik_deger:
            print(f"[NOBETCI UYARI] {hesap_id} numarali hesapta KRITIK etkilesim dususu!")
            print(f"[NOBETCI] Algoritma takibi sezildi. {hesap_id} ONLEM OLARAK KARANTINAYA ALINDI.")
            self.karantina_listesi.add(hesap_id)
            return False  # Bu hesap icin otonom akisi durdur emri
        
        print(f"[NOBETCI] {hesap_id} hesabi guvenli. Operasyon temiz.")
        return True