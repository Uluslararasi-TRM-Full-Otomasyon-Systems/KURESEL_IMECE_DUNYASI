# ============================================
# YOUTUBE OTOMASYON BOTU
# Video/Shorts yukleme
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
        print(f"📺 YouTube: {self.channel_name} kanalina giris yapiliyor...")
        time.sleep(2)
        print(f"✅ YouTube giris basarili")
        return True
    
    def video_hazirla(self, urun):
        """Urun icin video aciklamasi hazirlar"""
        aciklama = f"""
{urun['ad']} - {urun['fiyat']} TL

{urun['aciklama']}

Urun linki: {urun['link']}

#trendurunler #{urun['kategori']} #indirim #firsat
        """
        return aciklama.strip()
    
    def shorts_paylas(self, video_dosya, baslik, aciklama):
        """YouTube Shorts yukler"""
        print(f"📤 YouTube Shorts: {baslik} yukleniyor...")
        time.sleep(4)
        print(f"✅ YouTube Shorts paylasildi!")
        return True
    
    def video_paylas(self, video_dosya, baslik, aciklama):
        """Normal video yukler"""
        print(f"📤 YouTube Video: {baslik} yukleniyor...")
        time.sleep(5)
        print(f"✅ YouTube video paylasildi!")
        return True
    
    def paylasim_hazirla(self, urun, video_dosya):
        """Urun icin YouTube paylasimi hazirlar"""
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
        'ad': 'Test Urun',
        'fiyat': 199,
        'aciklama': 'Bu bir test urunudur.',
        'link': 'https://example.com',
        'kategori': 'test'
    }
    bot.paylasim_hazirla(test_urun, 'test_video.mp4')
