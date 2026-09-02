# team_social_accounts.py
from team_manager import TeamManager

class TeamSocialAccounts:
    def __init__(self):
        self.team = TeamManager()
        self.ekip_hesaplari = []
    
    def ekip_hesabi_ekle(self, uye_id, platform, kullanici_adi, sifre):
        """Engelli ekip üyesinin sosyal medya hesabını ekler"""
        
        self.ekip_hesaplari.append({
            'uye_id': uye_id,
            'platform': platform,
            'kullanici_adi': kullanici_adi,
            'sifre': sifre  # Şifreler güvenli şekilde saklanmalı!
        })
        print(f"✅ {platform} hesabı ekip üyesine bağlandı")
    
    def ekip_hesabiyla_paylas(self, platform, urun):
        """Belirli bir ekip üyesinin hesabından paylaşım yapar"""
        
        for hesap in self.ekip_hesaplari:
            if hesap['platform'] == platform:
                print(f"👤 {hesap['kullanici_adi']} hesabından paylaşılıyor...")
                # Paylaşım kodu burada olacak
                # Komisyon otomatik hesaplanacak
                return True
        return False
