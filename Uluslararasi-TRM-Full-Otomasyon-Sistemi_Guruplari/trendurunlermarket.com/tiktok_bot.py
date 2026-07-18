# ============================================
# TİKTOK OTOMASYON BOTU
# Claude API ile yapay zeka destekli içerik
# Video paylaşımı, otomatik metin üretimi
# ============================================

import os
import time
import random
import requests
from datetime import datetime
import anthropic  # Claude API için

class TikTokBot:
    def __init__(self):
        self.username = os.getenv('TIKTOK_USERNAME', '')
        self.password = os.getenv('TIKTOK_PASSWORD', '')
        self.claude_api_key = os.getenv('CLAUDE_API_KEY', '')
        self.session = requests.Session()
        
        # Claude istemcisini başlat
        if self.claude_api_key:
            self.claude = anthropic.Anthropic(api_key=self.claude_api_key)
        else:
            self.claude = None
            print("⚠️ Claude API anahtarı bulunamadı, temel modda çalışılacak.")
        
        # Örnek video kaynakları (gerçekte video dosyaların olacak)
        self.video_kaynaklari = [
            'videos/urun1.mp4',
            'videos/urun2.mp4',
            'videos/urun3.mp4'
        ]
    
    def giris_yap(self):
        """TikTok'a giriş yapar (simülasyon)"""
        print(f"🎵 TikTok: @{self.username} giriş yapılıyor...")
        time.sleep(2)
        print(f"✅ TikTok giriş başarılı")
        return True
    
    def claude_ile_metin_uret(self, urun_bilgisi, platform="tiktok"):
        """Claude API ile ürün açıklaması ve hashtag üretir"""
        if not self.claude:
            return self.temel_metin_uret(urun_bilgisi)
        
        prompt = f"""
        Bir ürün tanıtımı için {platform} platformunda kullanılacak kısa ve etkili bir metin yaz.
        Ürün adı: {urun_bilgisi['ad']}
        Fiyat: {urun_bilgisi['fiyat']} TL
        Açıklama: {urun_bilgisi.get('aciklama', '')}
        Kategori: {urun_bilgisi.get('kategori', 'genel')}
        
        Metin 150 karakteri geçmesin, dikkat çekici olsun, emoji kullan ve 5-10 arası hashtag ekle.
        Sadece metni yaz, başka açıklama ekleme.
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
            print(f"❌ Claude API hatası: {e}")
            return self.temel_metin_uret(urun_bilgisi)
    
    def temel_metin_uret(self, urun_bilgisi):
        """API yoksa kullanılacak temel metin"""
        return f"""
{urun_bilgisi['ad']} - {urun_bilgisi['fiyat']} TL 🔥

{urun_bilgisi.get('aciklama', 'Kaçırma fırsatı!')}

#keşfet #fyp #{urun_bilgisi.get('kategori', 'ürün')} #indirim #fırsat
        """.strip()
    
    def video_hazirla(self, urun_adi):
        """Ürün için video hazırlar (simülasyon)"""
        print(f"🎬 {urun_adi} için video hazırlanıyor...")
        time.sleep(3)
        # Gerçek uygulamada video düzenleme veya seçme yapılır
        return random.choice(self.video_kaynaklari) if self.video_kaynaklari else "videos/default.mp4"
    
    def video_paylas(self, video_yolu, metin):
        """TikTok'a video yükler (simülasyon)"""
        print(f"📤 TikTok: Video yükleniyor...")
        print(f"📝 Metin: {metin}")
        time.sleep(4)
        print(f"✅ TikTok video paylaşıldı!")
        return True
    
    def paylasim_hazirla(self, urun):
        """Ürün bilgisiyle TikTok paylaşımı hazırlar"""
        # Claude ile metin üret
        metin = self.claude_ile_metin_uret(urun)
        
        # Video hazırla (gerçekte video dosyası seç)
        video = self.video_hazirla(urun['ad'])
        
        # Paylaş
        return self.video_paylas(video, metin)


if __name__ == "__main__":
    # Test için
    bot = TikTokBot()
    bot.giris_yap()
    
    test_urun = {
        'ad': 'Xiaomi Akıllı Bileklik',
        'fiyat': 449,
        'aciklama': 'Kalp atışı takibi, adım sayar, 14 gün pil ömrü',
        'kategori': 'elektronik'
    }
    
    bot.paylasim_hazirla(test_urun)
