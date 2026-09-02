# ============================================
# TIKTOK OTOMASYON BOTU
# Claude API ile yapay zeka destekli icerik
# Video paylasimi, otomatik metin uretimi
# ============================================

import os
import time
import random
import requests
from datetime import datetime
import anthropic  # Claude API icin

class TikTokBot:
    def __init__(self):
        self.username = os.getenv('TIKTOK_USERNAME', '')
        self.password = os.getenv('TIKTOK_PASSWORD', '')
        self.claude_api_key = os.getenv('CLAUDE_API_KEY', '')
        self.session = requests.Session()
        
        # Claude istemcisini baslat
        if self.claude_api_key:
            self.claude = anthropic.Anthropic(api_key=self.claude_api_key)
        else:
            self.claude = None
            print("⚠️ Claude API anahtari bulunamadi, temel modda calisilacak.")
        
        # Ornek video kaynaklari (gercekte video dosyalarin olacak)
        self.video_kaynaklari = [
            'videos/urun1.mp4',
            'videos/urun2.mp4',
            'videos/urun3.mp4'
        ]
    
    def giris_yap(self):
        """TikTok'a giris yapar (simulasyon)"""
        print(f"🎵 TikTok: @{self.username} giris yapiliyor...")
        time.sleep(2)
        print(f"✅ TikTok giris basarili")
        return True
    
    def claude_ile_metin_uret(self, urun_bilgisi, platform="tiktok"):
        """Claude API ile urun aciklamasi ve hashtag uretir"""
        if not self.claude:
            return self.temel_metin_uret(urun_bilgisi)
        
        prompt = f"""
        Bir urun tanitimi icin {platform} platformunda kullanilacak kisa ve etkili bir metin yaz.
        Urun adi: {urun_bilgisi['ad']}
        Fiyat: {urun_bilgisi['fiyat']} TL
        Aciklama: {urun_bilgisi.get('aciklama', '')}
        Kategori: {urun_bilgisi.get('kategori', 'genel')}
        
        Metin 150 karakteri gecmesin, dikkat cekici olsun, emoji kullan ve 5-10 arasi hashtag ekle.
        Sadece metni yaz, baska aciklama ekleme.
        """
        
        try:
            response = self.claude.messages.create(
                model="claude-3-sonnet-20241022",
                max_tokens=150,
                temperature=0.7,
                messages=[{"role": "user", "content": prompt}]
            )
            return response.content[0].text.strip()
        except Exception as e:
            print(f"❌ Claude API hatasi: {e}")
            return self.temel_metin_uret(urun_bilgisi)
    
    def temel_metin_uret(self, urun_bilgisi):
        """API yoksa kullanilacak temel metin"""
        return f"""
{urun_bilgisi['ad']} - {urun_bilgisi['fiyat']} TL 🔥

{urun_bilgisi.get('aciklama', 'Kacirma firsati!')}

#kesfet #fyp #{urun_bilgisi.get('kategori', 'urun')} #indirim #firsat
        """.strip()
    
    def video_hazirla(self, urun_adi):
        """Urun icin video hazirlar (simulasyon)"""
        print(f"🎬 {urun_adi} icin video hazirlaniyor...")
        time.sleep(3)
        # Gercek uygulamada video duzenleme veya secme yapilir
        return random.choice(self.video_kaynaklari) if self.video_kaynaklari else "videos/default.mp4"
    
    def video_paylas(self, video_yolu, metin):
        """TikTok'a video yukler (simulasyon)"""
        print(f"📤 TikTok: Video yukleniyor...")
        print(f"📝 Metin: {metin}")
        time.sleep(4)
        print(f"✅ TikTok video paylasildi!")
        return True
    
    def paylasim_hazirla(self, urun):
        """Urun bilgisiyle TikTok paylasimi hazirlar"""
        # Claude ile metin uret
        metin = self.claude_ile_metin_uret(urun)
        
        # Video hazirla (gercekte video dosyasi sec)
        video = self.video_hazirla(urun['ad'])
        
        # Paylas
        return self.video_paylas(video, metin)


if __name__ == "__main__":
    # Test icin
    bot = TikTokBot()
    bot.giris_yap()
    
    test_urun = {
        'ad': 'Xiaomi Akilli Bileklik',
        'fiyat': 449,
        'aciklama': 'Kalp atisi takibi, adim sayar, 14 gun pil omru',
        'kategori': 'elektronik'
    }
    
    bot.paylasim_hazirla(test_urun)
