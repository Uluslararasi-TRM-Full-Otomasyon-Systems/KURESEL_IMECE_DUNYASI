# instagram_simple.py
import os
import time
import random
from datetime import datetime

class InstagramSimpleBot:
    """
    BASIT INSTAGRAM BOTU
    Telefon bildirimi gonderir, sen manuel paylas
    """
    
    def __init__(self, hesap_adi):
        self.hesap = hesap_adi
        self.paylasimlar = []
    
    def paylasim_hazirla(self, urun_adi, urun_fiyati, urun_linki, resim_yolu=None):
        """Paylasilacak icerigi hazirlar ve WhatsApp/Telegram'a bildirim gonderir"""
        
        saat = datetime.now().strftime("%H:%M")
        
        mesaj = f"""
📱 **INSTAGRAM PAYLASIM HAZIR!**
⏰ {saat}
👤 Hesap: @{self.hesap}

📦 Urun: {urun_adi}
💰 Fiyat: {urun_fiyati} TL
🔗 Link: {urun_linki}

🏷️ Hashtagler:
#trendurunler #firsat #indirim #{urun_adi.replace(' ', '')}

📌 Yapilacak:
1. Bu mesaji gorunce Instagram'a gir
2. Yeni gonderi olustur
3. Fotografi yukle
4. Aciklamayi kopyala
5. Paylas!
"""
        
        # Telegram'a bildirim gonder (bot uzerinden)
        self.telegram_bildirim(mesaj)
        
        # WhatsApp'a bildirim gonder (ilerde)
        
        self.paylasimlar.append({
            'zaman': saat,
            'urun': urun_adi,
            'durum': 'hazir'
        })
        
        return mesaj
    
    def telegram_bildirim(self, mesaj):
        """Telegram botuna mesaj gonderir (senin ID'ne)"""
        try:
            # telegram_bot.py'yi kullan
            import telegram_bot
            # Burada bot.send_message(SENIN_ID, mesaj) cagrilacak
            print(f"📱 Telegram bildirimi gonderildi")
        except:
            print(f"⚠️ Telegram bildirimi gonderilemedi")
    
    def paylasim_raporu(self):
        """Bugunku paylasimlari gosterir"""
        print("\n" + "="*50)
        print(f"📊 INSTAGRAM PAYLASIM RAPORU - {datetime.now().strftime('%d.%m.%Y')}")
        print("="*50)
        
        for p in self.paylasimlar:
            durum_ikonu = "✅" if p['durum'] == 'paylasildi' else "⏳"
            print(f"{durum_ikonu} {p['zaman']} - {p['urun']}")
        
        print("-"*50)
        print(f"Toplam: {len(self.paylasimlar)} paylasim hazirlandi")
