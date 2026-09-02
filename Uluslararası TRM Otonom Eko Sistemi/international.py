# ============================================
# ULUSLARARASI ÇOKLU DİL DESTEK SİSTEMİ
# TÜRKÇE AÇIKLAMALI
# ============================================

class InternationalSystem:
    """
    🌍 ULUSLARARASI ÇOKLU DİL DESTEK SİSTEMİ
    Bu sistem, farklı dillerde içerik üretir, çeviri yapar
    ve her ülkeye özel paylaşımlar hazırlar.
    """
    
    def __init__(self):
        """Sistemi başlatır ve dil paketlerini yükler"""
        
        # Desteklenen diller ve kodları
        self.diller = {
            'tr': 'Türkçe',
            'en': 'English',
            'de': 'Deutsch',
            'fr': 'Français',
            'es': 'Español',
            'it': 'Italiano',
            'ar': 'العربية',
            'ru': 'Русский',
            'zh': '中文',
            'ja': '日本語',
            'ko': '한국어',
            'nl': 'Nederlands',
            'pl': 'Polski',
            'pt': 'Português',
            'sv': 'Svenska',
            'da': 'Dansk',
            'no': 'Norsk',
            'fi': 'Suomi',
            'el': 'Ελληνικά',
            'he': 'עברית'
        }
        
        # Ülke bazlı popüler platformlar
        self.ulkeler = {
            'tr': {
                'adi': 'Türkiye',
                'para_birimi': 'TL',
                'platformlar': ['Instagram', 'Facebook', 'Telegram', 'TikTok'],
                'mesai_saatleri': '09:00-23:00',
                'hashtagler': ['#fırsat', '#indirim', '#kampanya']
            },
            'de': {
                'adi': 'Almanya',
                'para_birimi': 'EUR',
                'platformlar': ['WhatsApp', 'Facebook', 'Instagram', 'Telegram'],
                'mesai_saatleri': '10:00-22:00',
                'hashtagler': ['#angebot', '#rabatt', '#sale']
            },
            'us': {
                'adi': 'Amerika',
                'para_birimi': 'USD',
                'platformlar': ['Instagram', 'Facebook', 'TikTok', 'Twitter'],
                'mesai_saatleri': '09:00-21:00',
                'hashtagler': ['#sale', '#discount', '#deal']
            },
            'sa': {
                'adi': 'Suudi Arabistan',
                'para_birimi': 'SAR',
                'platformlar': ['WhatsApp', 'Telegram', 'Twitter', 'Snapchat'],
                'mesai_saatleri': '20:00-02:00',
                'hashtagler': ['#تخفيضات', '#عروض', '#خصم']
            },
            'cn': {
                'adi': 'Çin',
                'para_birimi': 'CNY',
                'platformlar': ['WeChat', 'Weibo', 'Douyin', 'QQ'],
                'mesai_saatleri': '10:00-22:00',
                'hashtagler': ['#促销', '#折扣', '#特价']
            },
            'jp': {
                'adi': 'Japonya',
                'para_birimi': 'JPY',
                'platformlar': ['LINE', 'Twitter', 'Instagram', 'YouTube'],
                'mesai_saatleri': '10:00-20:00',
                'hashtagler': ['#セール', '#割引', '#特価']
            },
            'gb': {
                'adi': 'İngiltere',
                'para_birimi': 'GBP',
                'platformlar': ['Facebook', 'Instagram', 'Twitter', 'WhatsApp'],
                'mesai_saatleri': '09:00-21:00',
                'hashtagler': ['#sale', '#offer', '#discount']
            },
            'fr': {
                'adi': 'Fransa',
                'para_birimi': 'EUR',
                'platformlar': ['Facebook', 'Instagram', 'Snapchat', 'WhatsApp'],
                'mesai_saatleri': '10:00-22:00',
                'hashtagler': ['#soldes', '#promo', '#bonplan']
            }
        }
        
        print(f"✅ Uluslararası sistem başlatıldı!")
        print(f"🌍 {len(self.diller)} dil desteği hazır")
        print(f"🏪 {len(self.ulkeler)} ülke profili yüklendi")
    
    # ============================================
    # 1. DİL ÇEVİRİ
    # ============================================
    def ceviri_yap(self, metin, kaynak_dil='tr', hedef_dil='en'):
        """
        Bir metni istenilen dile çevirir
        Örnek: ceviri_yap("Merhaba", 'tr', 'en') -> "Hello"
        """
        
        # Basit çeviri sözlüğü (örnek)
        sozluk = {
            'merhaba': {
                'en': 'hello',
                'de': 'hallo',
                'fr': 'bonjour',
                'es': 'hola',
                'it': 'ciao',
                'ar': 'مرحبا',
                'ru': 'привет',
                'zh': '你好',
                'ja': 'こんにちは'
            },
            'fırsat': {
                'en': 'opportunity',
                'de': 'angebot',
                'fr': 'opportunité',
                'es': 'oportunidad',
                'ar': 'فرصة',
                'ru': 'возможность'
            },
            'indirim': {
                'en': 'discount',
                'de': 'rabatt',
                'fr': 'remise',
                'es': 'descuento',
                'ar': 'خصم',
                'ru': 'скидка',
                'zh': '折扣',
                'ja': '割引'
            },
            'satış': {
                'en': 'sale',
                'de': 'verkauf',
                'fr': 'vente',
                'es': 'venta',
                'ar': 'بيع',
                'ru': 'продажа'
            }
        }
        
        metin_kucuk = metin.lower().strip()
        
        if metin_kucuk in sozluk:
            if hedef_dil in sozluk[metin_kucuk]:
                return sozluk[metin_kucuk][hedef_dil]
            else:
                return f"{metin} ({hedef_dil} çeviri bekliyor)"
        else:
            return f"{metin} (çeviri için AI gerekli)"
    
    # ============================================
    # 2. ÜLKEYE ÖZEL HASHTAG ÜRET
    # ============================================
    def hashtag_uret(self, urun_adi, kategori, ulke_kodu):
        """
        Belirtilen ülke için popüler hashtag'ler üretir
        """
        
        if ulke_kodu not in self.ulkeler:
            return [f"#{urun_adi}"]
        
        ulke = self.ulkeler[ulke_kodu]
        hashtagler = ulke['hashtagler'].copy()
        
        # Ürün adından hashtag
        urun_hashtag = f"#{urun_adi.replace(' ', '')}"
        hashtagler.append(urun_hashtag)
        
        # Kategori hashtag'i
        if kategori == 'elektronik':
            hashtagler.append('#electronics' if ulke_kodu != 'tr' else '#elektronik')
        elif kategori == 'moda':
            hashtagler.append('#fashion' if ulke_kodu != 'tr' else '#moda')
        elif kategori == 'kozmetik':
            hashtagler.append('#beauty' if ulke_kodu != 'tr' else '#güzellik')
        
        return hashtagler
    
    # ============================================
    # 3. PARA BİRİMİ ÇEVİR
    # ============================================
    def para_cevir(self, tutar, kaynak_birim, hedef_birim):
        """
        Para birimini çevirir (basit kur tablosu ile)
        """
        
        # Basit kur tablosu (örnek)
        kurlar = {
            'TRY': 1,
            'USD': 36.5,   # 1 USD = 36.5 TL
            'EUR': 40.2,   # 1 EUR = 40.2 TL
            'GBP': 47.8,   # 1 GBP = 47.8 TL
            'CHF': 41.3,   # 1 CHF = 41.3 TL
            'CNY': 5.1,    # 1 CNY = 5.1 TL
            'JPY': 0.25,   # 1 JPY = 0.25 TL
            'SAR': 9.7,    # 1 SAR = 9.7 TL
            'RUB': 0.42,   # 1 RUB = 0.42 TL
        }
        
        if kaynak_birim not in kurlar or hedef_birim not in kurlar:
            return f"{tutar} {kaynak_birim}"
        
        # Önce TL'ye çevir, sonra hedef birime
        tl_tutar = tutar * kurlar[kaynak_birim]
        hedef_tutar = tl_tutar / kurlar[hedef_birim]
        
        return f"{hedef_tutar:.2f} {hedef_birim}"
    
    # ============================================
    # 4. ÜLKEYE ÖZEL PAYLAŞIM METNİ HAZIRLA
    # ============================================
    def paylasim_metni_hazirla(self, urun_adi, urun_fiyati, aciklama, ulke_kodu):
        """
        Belirtilen ülkeye özel paylaşım metni hazırlar
        """
        
        if ulke_kodu not in self.ulkeler:
            ulke_kodu = 'tr'
        
        ulke = self.ulkeler[ulke_kodu]
        
        # Ülkeye özel selamlaşma
        selamlar = {
            'tr': '🔥 FIRSAT!',
            'de': '🔥 ANGEBOT!',
            'us': '🔥 HOT DEAL!',
            'gb': '🔥 SPECIAL OFFER!',
            'fr': '🔥 BONNE AFFAIRE!',
            'es': '🔥 OFERTA!',
            'it': '🔥 OFFERTA!',
            'ar': '🔥 عرض خاص!',
            'ru': '🔥 ГОРЯЧЕЕ ПРЕДЛОЖЕНИЕ!',
            'zh': '🔥 特价优惠！',
            'jp': '🔥 スペシャルオファー！'
        }
        
        # Fiyatı yerel para birimine çevir
        yerel_fiyat = self.para_cevir(urün_fiyati, 'TRY', ulke['para_birimi'])
        
        # Hashtag'leri hazırla
        hashtagler = self.hashtag_uret(urun_adi, 'genel', ulke_kodu)
        hashtag_str = ' '.join(hashtagler[:5])
        
        # Metin
        metin = f"""
{selamlar.get(ulke_kodu, '🔥 FIRSAT!')}

📦 {urun_adi}
💰 {yerel_fiyat}
📝 {aciklama[:100]}...

{hashtag_str}
"""
        return metin.strip()
    
    # ============================================
    # 5. ÜLKE LİSTESİNİ GÖSTER
    # ============================================
    def ulke_listesi_goster(self):
        """Tüm desteklenen ülkeleri listeler"""
        
        print("\n" + "="*70)
        print("🌍 DESTEKLENEN ÜLKELER")
        print("="*70)
        
        for kod, bilgi in self.ulkeler.items():
            print(f"\n📍 {bilgi['adi']} ({kod.upper()})")
            print(f"   💰 Para Birimi: {bilgi['para_birimi']}")
            print(f"   📱 Platformlar: {', '.join(bilgi['platformlar'])}")
            print(f"   ⏰ Mesai: {bilgi['mesai_saatleri']}")
            print(f"   🏷️  Hashtag: {', '.join(bilgi['hashtagler'])}")
    
    # ============================================
    # 6. DİL LİSTESİNİ GÖSTER
    # ============================================
    def dil_listesi_goster(self):
        """Tüm desteklenen dilleri listeler"""
        
        print("\n" + "="*70)
        print("🗣️ DESTEKLENEN DİLLER")
        print("="*70)
        
        for kod, isim in self.diller.items():
            print(f"   {kod.upper()}: {isim}")

# ============================================
# ANA PROGRAM
# ============================================
if __name__ == "__main__":
    print("""
┌─────────────────────────────────────┐
│  🌍 TRM ULUSLARARASI SİSTEM        │
│  ÇOKLU DİL DESTEĞİ                  │
│  v1.0 - 2026                        │
└─────────────────────────────────────┘
    """)
    
    uluslararasi = InternationalSystem()
    
    while True:
        print("\n" + "="*50)
        print("📋 ULUSLARARASI MENÜ")
        print("="*50)
        print("1️⃣  Ülke listesini göster")
        print("2️⃣  Dil listesini göster")
        print("3️⃣  Çeviri test et")
        print("4️⃣  Para birimi çevir")
        print("5️⃣  Ülkeye özel paylaşım metni hazırla")
        print("6️⃣  Hashtag üret")
        print("7️⃣  Çıkış")
        print("-"*50)
        
        secim = input("👉 Seçiminiz: ")
        
        if secim == '1':
            uluslararasi.ulke_listesi_goster()
        
        elif secim == '2':
            uluslararasi.dil_listesi_goster()
        
        elif secim == '3':
            metin = input("📝 Çevrilecek metin: ")
            kaynak = input("🎯 Kaynak dil (tr): ") or 'tr'
            hedef = input("🎯 Hedef dil (en): ") or 'en'
            sonuc = uluslararasi.ceviri_yap(metin, kaynak, hedef)
            print(f"\n✅ Çeviri: {sonuc}")
        
        elif secim == '4':
            tutar = float(input("💰 Tutar: "))
            kaynak = input("🎯 Kaynak birim (TRY): ") or 'TRY'
            hedef = input("🎯 Hedef birim (USD): ") or 'USD'
            sonuc = uluslararasi.para_cevir(tutar, kaynak, hedef)
            print(f"\n✅ Sonuç: {sonuc}")
        
        elif secim == '5':
            urun = input("📦 Ürün adı: ")
            fiyat = float(input("💰 Fiyat (TL): "))
            aciklama = input("📝 Açıklama: ")
            ulke = input("🎯 Ülke kodu (tr): ") or 'tr'
            metin = uluslararasi.paylasim_metni_hazirla(urun, fiyat, aciklama, ulke)
            print(f"\n📱 PAYLAŞIM METNİ:\n{metin}")
        
        elif secim == '6':
            urun = input("📦 Ürün adı: ")
            kategori = input("📂 Kategori: ")
            ulke = input("🎯 Ülke kodu (tr): ") or 'tr'
            hashtagler = uluslararasi.hashtag_uret(urun, kategori, ulke)
            print(f"\n🏷️  HASHTAGLER:\n{' '.join(hashtagler)}")
        
        elif secim == '7':
            print("\n👋 Dünyaya açılma vakti!")
            break
