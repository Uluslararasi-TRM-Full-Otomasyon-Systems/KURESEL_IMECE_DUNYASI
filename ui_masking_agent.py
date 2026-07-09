class UIMaskingAgent:
    def __init__(self):
        self.gercek_oran = 0.70
        self.gosterilen_oran = 0.30

    def komisyon_getir(self, sorgu_tipi="kullanici"):
        if sorgu_tipi == "admin":
            return self.gercek_oran
        else:
            return self.gosterilen_oran