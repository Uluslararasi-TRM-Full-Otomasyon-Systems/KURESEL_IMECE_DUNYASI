from utils.config_loader import load_config

class FinansAgent:
    def __init__(self, name="FinansAjan-001"):
        self.name = name
        self.config = load_config()
        self.margin = self.config["finans"]["kar_marji"]
        self.commission = self.config["finans"]["affiliate_komisyon_orani"]
        self.cpu_yuk = 0
        self.api_gecikme = 0

    def refresh_config(self):
        """Her döngüde güncel konfigürasyonu al."""
        self.config = load_config()
        self.margin = self.config["finans"]["kar_marji"]
        self.commission = self.config["finans"]["affiliate_komisyon_orani"]

    def run(self):
        self.refresh_config()
        # İş mantığı (örnek simülasyon)
        print(f"[{self.name}] Çalışıyor. Kar Marjı: %{self.margin}, Komisyon: %{self.commission}")
        # Gerçek işlemler burada yapılır
        self.cpu_yuk = 20 + (self.margin % 10)  # Örnek CPU yükü
        self.api_gecikme = 100 + (self.commission % 20)  # Örnek API gecikmesi