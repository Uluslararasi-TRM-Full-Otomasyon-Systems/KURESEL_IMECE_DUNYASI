# ============================================
# ULUSLARARASI GENİŞLEME MODÜLÜ
# Çoklu dil, para birimi, ülke adaptasyonu
# ============================================

import os
from datetime import datetime

class Uluslararasi:
    def __init__(self):
        self.diller = {
            'tr': 'Türkçe',
            'en': 'English',
            'de': 'Deutsch',
            'fr': 'Français',
            'ar': 'العربية',
            'ru': 'Русский'
        }
        
        self.para_birimleri = {
            'TRY': '₺',
            'USD': '$',
            'EUR': '€',
            'GBP': '£',
            'RUB': '₽',
            'SAR': '﷼'
        }
        
        self.kurlar = {
            'TRY': 1,
            'USD': 36.5,
            'EUR': 40.2,
            'GBP': 47.8,
            'RUB': 0.42,
            'SAR': 9.7
        }
        
        self.ulkeler = {
            'TR': {'dil': 'tr', 'para': 'TRY', 'hashtag': ['#fırsat', '#indirim']},
            'US': {'dil': 'en', 'para': 'USD', 'hashtag': ['#sale', '#discount']},
            'DE': {'dil': 'de', 'para': 'EUR', 'hashtag': ['#angebot', '#rabatt']},
            'SA': {'dil': 'ar', 'para': 'SAR', 'hashtag': ['#تخفيضات', '#عروض']}
        }
    
    def ceviri_yap(self, metin, kaynak='tr', hedef='en'):
        """Basit çeviri simülasyonu (gerçek çeviri için API gerekir)"""
        sozluk = {
            'merhaba': {'en': 'hello', 'de': 'hallo'},
            'fırsat': {'en': 'opportunity', 'de': 'angebot'},
            'indirim': {'en': 'discount', 'de': 'rabatt'}
        }
        metin_lower = metin.lower().strip()
        if metin_lower in sozluk and hedef in sozluk[metin_lower]:
            return sozluk[metin_lower][hedef]
        return f"{metin} ({hedef})"
    
    def para_cevir(self, tutar, kaynak='TRY', hedef='USD'):
        if kaynak not in self.kurlar or hedef not in self.kurlar:
            return tutar
        tl_tutar = tutar * self.kurlar[kaynak]
        hedef_tutar = tl_tutar / self.kurlar[hedef]
        return round(hedef_tutar, 2)
    
    def ulke_hashtag(self, ulke_kodu):
        if ulke_kodu in self.ulkeler:
            return self.ulkeler[ulke_kodu]['hashtag']
        return ['#sale']
    
    def paylasim_hazirla(self, urun, ulke_kodu='TR'):
        """Ülkeye özel paylaşım metni hazırlar"""
        ulke = self.ulkeler.get(ulke_kodu, self.ulkeler['TR'])
        hedef_para = ulke['para']
        hedef_dil = ulke['dil']
        
        fiyat_cevrilmis = self.para_cevir(urun['fiyat'], 'TRY', hedef_para)
        sembol = self.para_birimleri[hedef_para]
        
        # Basit çeviri (gerçekte API ile yapılmalı)
        urun_adi_ceviri = self.ceviri_yap(urun['ad'], 'tr', hedef_dil)
        
        hashtagler = self.ulke_hashtag(ulke_kodu)
        hashtag_str = ' '.join(hashtagler)
        
        metin = f"""
🔥 {urun_adi_ceviri} - {fiyat_cevrilmis} {sembol}

{urun['aciklama']}

{hashtag_str}
        """.strip()
        return metin

if __name__ == "__main__":
    ulu = Uluslararasi()
    test_urun = {'ad': 'Akıllı Bileklik', 'fiyat': 449, 'aciklama': 'Harika bir ürün'}
    print("🇹🇷 Türkiye:", ulu.paylasim_hazirla(test_urun, 'TR'))
    print("🇺🇸 ABD:", ulu.paylasim_hazirla(test_urun, 'US'))
    print("🇩🇪 Almanya:", ulu.paylasim_hazirla(test_urun, 'DE'))
