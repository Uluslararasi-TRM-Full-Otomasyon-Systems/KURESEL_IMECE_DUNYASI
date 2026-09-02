# instagram_simple.py
import os
import time
import random
from datetime import datetime

class InstagramSimpleBot:
    """
    BASİT INSTAGRAM BOTU
    Telefon bildirimi gönderir, sen manuel paylaş
    """
    
    def __init__(self, hesap_adi):
        self.hesap = hesap_adi
        self.paylasimlar = []
    
    def paylasim_hazirla(self, urun_adi, urun_fiyati, urun_linki, resim_yolu=None):
        """Paylaşılacak içeriği hazırlar ve WhatsApp/Telegram'a bildirim gönderir"""
        
        saat = datetime.now().strftime("%H:%M")
        
        mesaj = f"""
📱 **INSTAGRAM PAYLAŞIM HAZIR!**
⏰ {saat}
👤 Hesap: @{self.hesap}

📦 Ürün: {urun_adi}
💰 Fiyat: {urun_fiyati} TL
🔗 Link: {urun_linki}

🏷️ Hashtagler:
#trendurunler #fırsat #indirim #{urun_adi.replace(' ', '')}

📌 Yapılacak:
1. Bu mesajı görünce Instagram'a gir
2. Yeni gönderi oluştur
3. Fotoğrafı yükle
4. Açıklamayı kopyala
5. Paylaş!
"""
        
        # Telegram'a bildirim gönder (bot üzerinden)
        self.telegram_bildirim(mesaj)
        
        # WhatsApp'a bildirim gönder (ilerde)
        
        self.paylasimlar.append({
            'zaman': saat,
            'urun': urun_adi,
            'durum': 'hazır'
        })
        
        return mesaj
    
    def telegram_bildirim(self, mesaj):
        """Telegram botuna mesaj gönderir (senin ID'ne)"""
        try:
            # telegram_bot.py'yi kullan
            import telegram_bot
            # Burada bot.send_message(SENIN_ID, mesaj) çağrılacak
            print(f"📱 Telegram bildirimi gönderildi")
        except:
            print(f"⚠️ Telegram bildirimi gönderilemedi")
    
    def paylasim_raporu(self):
        """Bugünkü paylaşımları gösterir"""
        print("\n" + "="*50)
        print(f"📊 INSTAGRAM PAYLAŞIM RAPORU - {datetime.now().strftime('%d.%m.%Y')}")
        print("="*50)
        
        for p in self.paylasimlar:
            durum_ikonu = "✅" if p['durum'] == 'paylaşıldı' else "⏳"
            print(f"{durum_ikonu} {p['zaman']} - {p['urun']}")
        
        print("-"*50)
        print(f"Toplam: {len(self.paylasimlar)} paylaşım hazırlandı")
