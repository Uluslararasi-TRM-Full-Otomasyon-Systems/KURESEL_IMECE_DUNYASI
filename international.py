# ============================================
# ULUSLARARASI COKLU DIL DESTEK SISTEMI
# TURKCE ACIKLAMALI
# ============================================

class InternationalSystem:
    """
    🌍 ULUSLARARASI COKLU DIL DESTEK SISTEMI
    Bu sistem, farkli dillerde icerik uretir, ceviri yapar
    ve her ulkeye ozel paylasimlar hazirlar.
    """
    
    def __init__(self):
        """Sistemi baslatir ve dil paketlerini yukler"""
        
        # Desteklenen diller ve kodlari
        self.diller = {
            'tr': 'Turkce',
            'en': 'English',
            'de': 'Deutsch',
            'fr': 'Francais',
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
        
        # Ulke bazli populer platformlar
        self.ulkeler = {
            'tr': {
                'adi': 'Turkiye',
                'para_birimi': 'TL',
                'platformlar': ['Instagram', 'Facebook', 'Telegram', 'TikTok'],
                'mesai_saatleri': '09:00-23:00',
                'hashtagler': ['#firsat', '#indirim', '#kampanya']
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
                'adi': 'Cin',
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
                'adi': 'Ingiltere',
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
        
        print(f"✅ Uluslararasi sistem baslatildi!")
        print(f"🌍 {len(self.diller)} dil destegi hazir")
        print(f"🏪 {len(self.ulkeler)} ulke profili yuklendi")
    
    # ============================================
    # 1. DIL CEVIRI
    # ============================================
    def ceviri_yap(self, metin, kaynak_dil='tr', hedef_dil='en'):
        """
        Bir metni istenilen dile cevirir
        Ornek: ceviri_yap("Merhaba", 'tr', 'en') -> "Hello"
        """
        
        # Basit ceviri sozlugu (ornek)
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
            'firsat': {
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
            'satis': {
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
                return f"{metin} ({hedef_dil} ceviri bekliyor)"
        else:
            return f"{metin} (ceviri icin AI gerekli)"
    
    # ============================================
    # 2. ULKEYE OZEL HASHTAG URET
    # ============================================
    def hashtag_uret(self, urun_adi, kategori, ulke_kodu):
        """
        Belirtilen ulke icin populer hashtag'ler uretir
        """
        
        if ulke_kodu not in self.ulkeler:
            return [f"#{urun_adi}"]
        
        ulke = self.ulkeler[ulke_kodu]
        hashtagler = ulke['hashtagler'].copy()
        
        # Urun adindan hashtag
        urun_hashtag = f"#{urun_adi.replace(' ', '')}"
        hashtagler.append(urun_hashtag)
        
        # Kategori hashtag'i
        if kategori == 'elektronik':
            hashtagler.append('#electronics' if ulke_kodu != 'tr' else '#elektronik')
        elif kategori == 'moda':
            hashtagler.append('#fashion' if ulke_kodu != 'tr' else '#moda')
        elif kategori == 'kozmetik':
            hashtagler.append('#beauty' if ulke_kodu != 'tr' else '#guzellik')
        
        return hashtagler
    
    # ============================================
    # 3. PARA BIRIMI CEVIR
    # ============================================
    def para_cevir(self, tutar, kaynak_birim, hedef_birim):
        """
        Para birimini cevirir (basit kur tablosu ile)
        """
        
        # Basit kur tablosu (ornek)
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
        
        # Once TL'ye cevir, sonra hedef birime
        tl_tutar = tutar * kurlar[kaynak_birim]
        hedef_tutar = tl_tutar / kurlar[hedef_birim]
        
        return f"{hedef_tutar:.2f} {hedef_birim}"
    
    # ============================================
    # 4. ULKEYE OZEL PAYLASIM METNI HAZIRLA
    # ============================================
    def paylasim_metni_hazirla(self, urun_adi, urun_fiyati, aciklama, ulke_kodu):
        """
        Belirtilen ulkeye ozel paylasim metni hazirlar
        """
        
        if ulke_kodu not in self.ulkeler:
            ulke_kodu = 'tr'
        
        ulke = self.ulkeler[ulke_kodu]
        
        # Ulkeye ozel selamlasma
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
        
        # Fiyati yerel para birimine cevir
        yerel_fiyat = self.para_cevir(urun_fiyati, 'TRY', ulke['para_birimi'])
        
        # Hashtag'leri hazirla
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
    # 5. ULKE LISTESINI GOSTER
    # ============================================
    def ulke_listesi_goster(self):
        """Tum desteklenen ulkeleri listeler"""
        
        print("\n" + "="*70)
        print("🌍 DESTEKLENEN ULKELER")
        print("="*70)
        
        for kod, bilgi in self.ulkeler.items():
            print(f"\n📍 {bilgi['adi']} ({kod.upper()})")
            print(f"   💰 Para Birimi: {bilgi['para_birimi']}")
            print(f"   📱 Platformlar: {', '.join(bilgi['platformlar'])}")
            print(f"   ⏰ Mesai: {bilgi['mesai_saatleri']}")
            print(f"   🏷️  Hashtag: {', '.join(bilgi['hashtagler'])}")
    
    # ============================================
    # 6. DIL LISTESINI GOSTER
    # ============================================
    def dil_listesi_goster(self):
        """Tum desteklenen dilleri listeler"""
        
        print("\n" + "="*70)
        print("🗣️ DESTEKLENEN DILLER")
        print("="*70)
        
        for kod, isim in self.diller.items():
            print(f"   {kod.upper()}: {isim}")

# ============================================
# ANA PROGRAM
# ============================================
if __name__ == "__main__":
    print("""
┌─────────────────────────────────────┐
│  🌍 TRM ULUSLARARASI SISTEM        │
│  COKLU DIL DESTEGI                  │
│  v1.0 - 2026                        │
└─────────────────────────────────────┘
    """)
    
    uluslararasi = InternationalSystem()
    
    while True:
        print("\n" + "="*50)
        print("📋 ULUSLARARASI MENU")
        print("="*50)
        print("1️⃣  Ulke listesini goster")
        print("2️⃣  Dil listesini goster")
        print("3️⃣  Ceviri test et")
        print("4️⃣  Para birimi cevir")
        print("5️⃣  Ulkeye ozel paylasim metni hazirla")
        print("6️⃣  Hashtag uret")
        print("7️⃣  Cikis")
        print("-"*50)
        
        secim = input("👉 Seciminiz: ")
        
        if secim == '1':
            uluslararasi.ulke_listesi_goster()
        
        elif secim == '2':
            uluslararasi.dil_listesi_goster()
        
        elif secim == '3':
            metin = input("📝 Cevrilecek metin: ")
            kaynak = input("🎯 Kaynak dil (tr): ") or 'tr'
            hedef = input("🎯 Hedef dil (en): ") or 'en'
            sonuc = uluslararasi.ceviri_yap(metin, kaynak, hedef)
            print(f"\n✅ Ceviri: {sonuc}")
        
        elif secim == '4':
            tutar = float(input("💰 Tutar: "))
            kaynak = input("🎯 Kaynak birim (TRY): ") or 'TRY'
            hedef = input("🎯 Hedef birim (USD): ") or 'USD'
            sonuc = uluslararasi.para_cevir(tutar, kaynak, hedef)
            print(f"\n✅ Sonuc: {sonuc}")
        
        elif secim == '5':
            urun = input("📦 Urun adi: ")
            fiyat = float(input("💰 Fiyat (TL): "))
            aciklama = input("📝 Aciklama: ")
            ulke = input("🎯 Ulke kodu (tr): ") or 'tr'
            metin = uluslararasi.paylasim_metni_hazirla(urun, fiyat, aciklama, ulke)
            print(f"\n📱 PAYLASIM METNI:\n{metin}")
        
        elif secim == '6':
            urun = input("📦 Urun adi: ")
            kategori = input("📂 Kategori: ")
            ulke = input("🎯 Ulke kodu (tr): ") or 'tr'
            hashtagler = uluslararasi.hashtag_uret(urun, kategori, ulke)
            print(f"\n🏷️  HASHTAGLER:\n{' '.join(hashtagler)}")
        
        elif secim == '7':
            print("\n👋 Dunyaya acilma vakti!")
            break
