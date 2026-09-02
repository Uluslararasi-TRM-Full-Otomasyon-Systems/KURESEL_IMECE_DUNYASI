# facebook_simple.py
import os
from datetime import datetime

class FacebookSimpleBot:
    """
    BASIT FACEBOOK BOTU
    Sayfana otomatik gonderi paylasir
    """
    
    def __init__(self, sayfa_adi, kullanici_adi):
        self.sayfa = sayfa_adi
        self.kullanici = kullanici_adi
        self.paylasimlar = []
    
    def paylasim_hazirla(self, urun_adi, urun_fiyati, urun_linki, aciklama):
        """Facebook icin paylasim hazirlar"""
        
        saat = datetime.now().strftime("%H:%M")
        
        # Facebook paylasim metni
        paylasim = f"""
📦 {urun_adi}
💰 {urun_fiyati} TL
🔗 {urun_linki}

{aciklama[:100]}...

#trendurunler #firsat #indirim
"""
        
        # NOT: Facebook otomatik paylasim icin API gerekli
        # Simdilik MANUEL yapacagiz, sonra otomatiklestiririz
        
        mesaj = f"""
📘 **FACEBOOK PAYLASIM HAZIR!**
⏰ {saat}
👤 Sayfa: {self.sayfa}

📦 Urun: {urun_adi}
💰 Fiyat: {urun_fiyati} TL
🔗 Link: {urun_linki}

📝 Paylasim metni:
{paylasim}

📌 Yapilacak:
1. Facebook Sayfana gir
2. Yeni gonderi olustur
3. Bu metni kopyala
4. Linki ekle
5. Paylas!
"""
        
        self.telegram_bildirim(mesaj)
        
        self.paylasimlar.append({
            'zaman': saat,
            'urun': urun_adi,
            'durum': 'hazir'
        })
        
        return mesaj
    
    def telegram_bildirim(self, mesaj):
        """Telegram bildirimi gonderir"""
        try:
            import telegram_bot
            print(f"📱 Telegram bildirimi gonderildi (Facebook)")
        except:
            print(f"⚠️ Telegram bildirimi gonderilemedi")
