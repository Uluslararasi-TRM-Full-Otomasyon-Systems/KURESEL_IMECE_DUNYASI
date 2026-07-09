# team_social_accounts.py
from team_manager import TeamManager

class TeamSocialAccounts:
    def __init__(self):
        self.team = TeamManager()
        self.ekip_hesaplari = []
    
    def ekip_hesabi_ekle(self, uye_id, platform, kullanici_adi, sifre):
        """Engelli ekip uyesinin sosyal medya hesabini ekler"""
        
        self.ekip_hesaplari.append({
            'uye_id': uye_id,
            'platform': platform,
            'kullanici_adi': kullanici_adi,
            'sifre': sifre  # Sifreler guvenli sekilde saklanmali!
        })
        print(f"✅ {platform} hesabi ekip uyesine baglandi")
    
    def ekip_hesabiyla_paylas(self, platform, urun):
        """Belirli bir ekip uyesinin hesabindan paylasim yapar"""
        
        for hesap in self.ekip_hesaplari:
            if hesap['platform'] == platform:
                print(f"👤 {hesap['kullanici_adi']} hesabindan paylasiliyor...")
                # Paylasim kodu burada olacak
                # Komisyon otomatik hesaplanacak
                return True
        return False
