# KAR_DAGITIM_LOGIC.py - Gelir Yönetimi ve Dağıtım Modülü

class KarDagitimLogic:
    def __init__(self, havuz_bakiyesi_usd):
        self.havuz_bakiyesi_usd = havuz_bakiyesi_usd
        self.kur = 34.00 # Güncel kur referansı
        
    def usd_to_tl_convert(self):
        # Global kazancın yerel para birimine çevrilmesi
        return self.havuz_bakiyesi_usd * self.kur
    
    def calculate_imece_maas(self, aktif_katilimci_sayisi):
        # Toplam kârın katılımcı sayısına göre adaletli dağıtımı
        toplam_tl = self.usd_to_tl_convert()
        maas_payi = toplam_tl / aktif_katilimci_sayisi
        print(f"[HAVUZ] Aktif {aktif_katilimci_sayisi} katılımcıya kişi başı {maas_payi} TL dağıtılmak üzere hazırlandı.")
        return maas_payi

# Örnek Çalışma:
# Havuzda 10.000 USD birikti, 1000 aktif katılımcı var
dagitim = KarDagitimLogic(10000)
dagitim.calculate_imece_maas(1000)