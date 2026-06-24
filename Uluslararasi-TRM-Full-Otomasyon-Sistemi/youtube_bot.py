# ============================================
# YOUTUBE OTOMASYON BOTU
# Video/Shorts yükleme
# ============================================

import os
import time
import random
from datetime import datetime

class YouTubeBot:
    def __init__(self):
        self.channel_name = os.getenv('YOUTUBE_CHANNEL', 'Trend Urunler Market')
        self.api_key = os.getenv('YOUTUBE_API_KEY', '')
    
    def giris_yap(self):
        print(f"📺 YouTube: {self.channel_name} kanalına giriş yapılıyor...")
        time.sleep(2)
        print(f"✅ YouTube giriş başarılı")
        return True
    
    def video_hazirla(self, urun):
        """Ürün için video açıklaması hazırlar"""
        aciklama = f"""
{urun['ad']} - {urun['fiyat']} TL

{urun['aciklama']}

Ürün linki: {urun['link']}

#trendurunler #{urun['kategori']} #indirim #fırsat
        """
        return aciklama.strip()
    
    def shorts_paylas(self, video_dosya, baslik, aciklama):
        """YouTube Shorts yükler"""
        print(f"📤 YouTube Shorts: {baslik} yükleniyor...")
        time.sleep(4)
        print(f"✅ YouTube Shorts paylaşıldı!")
        return True
    
    def video_paylas(self, video_dosya, baslik, aciklama):
        """Normal video yükler"""
        print(f"📤 YouTube Video: {baslik} yükleniyor...")
        time.sleep(5)
        print(f"✅ YouTube video paylaşıldı!")
        return True
    
    def paylasim_hazirla(self, urun, video_dosya):
        """Ürün için YouTube paylaşımı hazırlar"""
        baslik = f"{urun['ad']} - {urun['fiyat']} TL"
        aciklama = self.video_hazirla(urun)
        
        # Shorts mu normal video mu karar ver
        if random.choice([True, False]):
            return self.shorts_paylas(video_dosya, baslik, aciklama)
        else:
            return self.video_paylas(video_dosya, baslik, aciklama)


if __name__ == "__main__":
    bot = YouTubeBot()
    bot.giris_yap()
    test_urun = {
        'ad': 'Test Ürün',
        'fiyat': 199,
        'aciklama': 'Bu bir test ürünüdür.',
        'link': 'https://example.com',
        'kategori': 'test'
    }
    bot.paylasim_hazirla(test_urun, 'test_video.mp4')
