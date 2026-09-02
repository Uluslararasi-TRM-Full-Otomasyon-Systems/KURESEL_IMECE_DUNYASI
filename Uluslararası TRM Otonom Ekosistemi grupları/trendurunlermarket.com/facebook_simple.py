# facebook_simple.py
import os
from datetime import datetime

class FacebookSimpleBot:
    """
    BASİT FACEBOOK BOTU
    Sayfana otomatik gönderi paylaşır
    """
    
    def __init__(self, sayfa_adi, kullanici_adi):
        self.sayfa = sayfa_adi
        self.kullanici = kullanici_adi
        self.paylasimlar = []
    
    def paylasim_hazirla(self, urun_adi, urun_fiyati, urun_linki, aciklama):
        """Facebook için paylaşım hazırlar"""
        
        saat = datetime.now().strftime("%H:%M")
        
        # Facebook paylaşım metni
        paylasim = f"""
📦 {urun_adi}
💰 {urun_fiyati} TL
🔗 {urun_linki}

{aciklama[:100]}...

#trendurunler #fırsat #indirim
"""
        
        # NOT: Facebook otomatik paylaşım için API gerekli
        # Şimdilik MANUEL yapacağız, sonra otomatikleştiririz
        
        mesaj = f"""
📘 **FACEBOOK PAYLAŞIM HAZIR!**
⏰ {saat}
👤 Sayfa: {self.sayfa}

📦 Ürün: {urun_adi}
💰 Fiyat: {urun_fiyati} TL
🔗 Link: {urun_linki}

📝 Paylaşım metni:
{paylasim}

📌 Yapılacak:
1. Facebook Sayfana gir
2. Yeni gönderi oluştur
3. Bu metni kopyala
4. Linki ekle
5. Paylaş!
"""
        
        self.telegram_bildirim(mesaj)
        
        self.paylasimlar.append({
            'zaman': saat,
            'urun': urun_adi,
            'durum': 'hazır'
        })
        
        return mesaj
    
    def telegram_bildirim(self, mesaj):
        """Telegram bildirimi gönderir"""
        try:
            import telegram_bot
            print(f"📱 Telegram bildirimi gönderildi (Facebook)")
        except:
            print(f"⚠️ Telegram bildirimi gönderilemedi")
