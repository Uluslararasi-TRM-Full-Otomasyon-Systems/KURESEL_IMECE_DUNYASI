import os
import logging
import random
from dataclasses import dataclass

# Loglama Sistemi (Ajanin attigi her adimi izlemek icin)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - [166. AJAN - MOBILE GATEWAY] - %(levelname)s - %(message)s')

@dataclass
class MobileDeviceProfile:
    device_name: str
    user_agent: str
    screen_width: int
    screen_height: int

class MobileGatewayAgent:
    def __init__(self):
        self.agent_id = 166
        self.agent_name = "Mobile Autonomous Gateway & Configuration Agent"
        # Telefon tiplerini simule etmek icin profil havuzu
        self.mobile_profiles = [
            MobileDeviceProfile(
                device_name="iPhone 15 Pro", 
                user_agent="Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
                screen_width=393, screen_height=852
            ),
            MobileDeviceProfile(
                device_name="Samsung Galaxy S24", 
                user_agent="Mozilla/5.0 (Linux; Android 14; SM-S921B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.6261.64 Mobile Safari/537.36",
                screen_width=360, screen_height=800
            )
        ]

    def listen_mobile_trigger(self, user_id: str, platform_approved: bool):
        """
        Kullanicinin cep telefonundan TRM paneline gelip 'Onay veriyorum' dedigi ani yakalar.
        """
        logging.info(f"Kullanici ({user_id}) cep telefonundan sisteme giris yapti ve onay butonuna basti.")
        
        if not platform_approved:
            logging.warning(f"Kullanici {user_id} onayi dogrulanmadi. Islem iptal edildi.")
            return False
            
        logging.info("Kullanici onayi alindi! %100 Otonom Kurulum sureci baslatiliyor...")
        return self.initialize_cloud_emulation(user_id)

    def initialize_cloud_emulation(self, user_id: str):
        """
        Kullanicinin kendi telefonuna dokunmadan, sunucuda sanal bir mobil ortam simule eder.
        """
        # Rastgele bir mobil parmak izi secerek platform algoritmalarini sasirtiyoruz
        selected_profile = random.choice(self.mobile_profiles)
        logging.info(f"Sunucuda {selected_profile.device_name} icin sanal tarayici ortami simule ediliyor.")
        logging.info(f"Kullanilacak User-Agent: {selected_profile.user_agent}")
        
        # Diger ajanlari (Proxy ve Spoofer) goreve cagirma simulasyonu
        logging.info("Siber kalkan ajanlari (Proxy, Spoofer, Humanizer) goreve cagriliyor...")
        
        # Hesap kurulum adimlari
        success_domestic = self._create_account_on_cloud(user_id, region="TR", profile=selected_profile)
        success_global = self._create_account_on_cloud(user_id, region="US", profile=selected_profile)
        
        if success_domestic and success_global:
            logging.info(f"Tebrikler! Kullanici {user_id} icin IKIZ HESAPLAR (TR ve US) sunucuda otonom olarak kuruldu.")
            logging.info("Kullanicinin cep telefonuna 'Kurulum Tamamlandi, Kazanc Basladi' bildirimi gonderiliyor.")
            return True
        return False

    def _create_account_on_cloud(self, user_id: str, region: str, profile: MobileDeviceProfile):
        """
        Arka planda (Bulutta) hesabi tescil eden ic fonksiyon
        """
        logging.info(f"[{region}] Bolgesi icin hesap acma motoru tetiklendi. Ekran Cozunurlugu: {profile.screen_width}x{profile.screen_height}")
        # Burada diger otonom kayit fonksiyonlari devreye girecek
        return True

# Ajani Test Edelim ve Ordunun En Son Uyesini Uyandiralim
if __name__ == "__main__":
    print("--- TRM OTONOM EKOSISTEMI ORDUYA YENI AJAN KATILIM PROTOKOLU ---")
    trm_agent_166 = MobileGatewayAgent()
    
    # Simule edilmis bir kullanici tetiklemesi (Orn: Engelli bir vatandasimizin ebeveyni telefondan butona basti)
    trm_agent_166.listen_mobile_trigger(user_id="TRM_USER_786", platform_approved=True)