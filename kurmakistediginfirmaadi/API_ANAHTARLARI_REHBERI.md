# 🔐 API Anahtarlarını Değiştirme ve Bağlama Rehberi

Bu rehber, tüm API anahtarlarınızı nereden alacağınızı ve `secrets.env` dosyasına nasıl ekleyeceğinizi adım adım anlatır.

> **⚠️ ÇOK ÖNEMLİ:** Şu anki `secrets.env` dosyasındaki **eski anahtarlar internette paylaşıldı**. Sistemi gerçek kullanıma açmadan önce **HEPSİNİ İPTAL EDİP YENİDEN OLUŞTURUN!**

---

## 📋 Anahtarların Tek Noktası: `secrets.env`

Tüm anahtarlar **`secrets.env`** dosyasında tutulur. Notepad/VS Code ile açıp düzenleyin:

```env
ANAHTAR_ADI=DEĞER_BURAYA
```

**Kural:** `=` işaretinin etrafında **boşluk olmamalı**, değer **tırnak içinde değil**.

---

## 1️⃣ Telegram API (Tedarikçi grup dinleme)

### Nereden alınır?
1. https://my.telegram.org adresine git, telefon numaranla giriş yap
2. **"API development tools"** → yeni uygulama oluştur
3. Sana 2 değer verecek: **API ID** (sayı) ve **API Hash** (uzun string)

### secrets.env'de:
```env
TELEGRAM_API_ID=21406034
TELEGRAM_API_HASH=c0c5a326621acf53d21a4a6e9c83a50f
TELEGRAM_PHONE=+905426235116
```

### Bot için (BotFather):
1. Telegram'da @BotFather'a yaz: `/newbot`
2. Bot adı seç, kullanıcı adı seç → token alacaksın
3. **Chat ID öğrenmek için:** kendi botuna `/start` mesajı at, sonra şu linki aç:
   `https://api.telegram.org/bot<TOKEN>/getUpdates` → `chat.id`

```env
TELEGRAM_BOT_TOKEN=8686224874:AAEpaGBx_xxxxxxxxxxxx
TELEGRAM_BOT_TOKEN_NOTIFICATION=8686224874:AAEpaGBx_xxxxxxxxxxxx
TELEGRAM_CHAT_ID=123456789
```

---

## 2️⃣ OpenAI (AI içerik üretimi için)

### Nereden alınır?
1. https://platform.openai.com/api-keys
2. "Create new secret key" → kopyala (bir daha gösterilmez!)

### secrets.env'de:
```env
OPENAI_API_KEY=sk-proj-XXXXXXXXXXXXXXXXXXXX
```

> 💡 **Not:** Sistem aynı anahtarı **DeepSeek API**'si için de kullanır (uyumlu format). DeepSeek için ayrı istersen:
> ```env
> DEEPSEEK_API_KEY=sk-xxxxx
> ```

---

## 3️⃣ Anthropic Claude (opsiyonel, gelişmiş içerik için)

### Nereden alınır?
1. https://console.anthropic.com/ → API Keys
2. Yeni anahtar oluştur

```env
CLAUDE_API_KEY=sk-ant-xxxxxxxxxxxxx
```

---

## 4️⃣ YouTube API (YouTube paylaşımı için)

### Nereden alınır?
1. https://console.cloud.google.com/apis/credentials
2. Proje seç/oluştur → **"YouTube Data API v3"** etkinleştir
3. **"API key"** oluştur

```env
YOUTUBE_API_KEY=AIzaSyXXXXXXXXXXXXXXXXXXXX
```

---

## 5️⃣ Google Drive / Sheets (Raporlama için)

Bu **iki dosya** gerekir:

### A) `credentials.json` (OAuth 2.0 client)
1. https://console.cloud.google.com/apis/credentials
2. **"Create Credentials"** → **"OAuth client ID"** → **"Desktop app"**
3. İndir → **`credentials.json`** olarak proje köküne kaydet
4. **"Google Drive API"** ve **"Google Sheets API"** etkinleştir

### B) İlk kullanımda otomatik authorize
Sistem ilk açıldığında tarayıcı açar, Google hesabınla giriş yap → onay ver.
Sonra `token.pickle` otomatik oluşur, bir daha sormaz.

### Google Drive klasör ID'si (opsiyonel):
Drive'da yedeklerin yükleneceği klasörün URL'sinden ID'yi al:
```
https://drive.google.com/drive/folders/1A2B3C4D5E6F7G   ← bu kısım
```

```env
GOOGLE_DRIVE_FOLDER_ID=1A2B3C4D5E6F7G
```

---

## 6️⃣ Facebook (Sayfa paylaşımı için)

### Nereden alınır?
1. https://developers.facebook.com/apps/ → yeni uygulama oluştur (Business tipi)
2. **"Facebook Login"** ürünü ekle
3. **Graph API Explorer** → token oluştur → sayfa için `pages_manage_posts` izni
4. **Long-lived token**'a dönüştür: https://developers.facebook.com/tools/debug/accesstoken/

```env
FACEBOOK_ACCESS_TOKEN=EAAxxxxxxxxxxxxxxxxxx
```

---

## 7️⃣ Instagram (Business hesabı gerekli!)

### Önkoşul:
- Instagram **Business** veya **Creator** hesabı
- Facebook sayfasına bağlı

### Nereden alınır?
1. Facebook geliştirici konsoluna gir (yukarıdaki Facebook ile aynı)
2. **"Instagram Graph API"** ürünü ekle
3. Hesabını bağla → token oluştur

```env
INSTAGRAM_ACCESS_TOKEN=IGQVxxxxxxxxxxx
```

---

## 8️⃣ Twitter / X API

### Nereden alınır?
1. https://developer.twitter.com/en/portal/dashboard
2. Proje oluştur → "Keys and tokens"
3. **API Key** ve **API Secret** kopyala

```env
TWITTER_API_KEY=xxxxxxxxxxxxxxx
TWITTER_API_SECRET=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

---

## 9️⃣ Telegram/Discord/Viber Business API (Twilio veya Meta)

### Twilio kolay yol:
1. https://www.twilio.com/console
2. "Messaging" → "Try Telegram/Discord/Viber" → sandbox token
```env
DISCORD_BOT_TOKEN=ACxxxxxxxxxxxxx
TELEGRAM_CHAT_ID=+14155238886
```

### Meta resmi yol:
1. https://developers.facebook.com/ → "Telegram/Discord/Viber" ürünü
2. Business Manager hesabı gerekir, doğrulama uzun sürer

---

## 🔟 E-Ticaret Pazaryeri API'leri (Türkiye)

| Platform | API Başvuru |
|---|---|
| **Trendyol** | https://partner.trendyol.com → Entegrasyon → API |
| **Hepsiburada** | https://developers.hepsiburada.com/ |
| **N11** | https://www.n11.com/satici/api-bilgilendirme |

```env
TRENDYOL_API_KEY=xxxxxxxxxxxxxxx
HEPSIBURADA_API_KEY=xxxxxxxxxxxxxxx
N11_API_KEY=xxxxxxxxxxxxxxx
```

> ⚠️ Bu platformların API'leri **satıcı/iş ortağı hesabı** gerektirir. Onay süreci 1-2 hafta sürebilir.

---

## 🔧 Güvenlik Ayarları

Bunları rastgele uzun değerlerle değiştir:

```env
SECRET_KEY=trm_super_secret_key_2024_secure_change_immediately
JWT_SECRET=trm_jwt_secret_2024_secure_change_immediately
```

**Rastgele 64 karakter üretmek için:**
```bash
python -c "import secrets; print(secrets.token_urlsafe(48))"
```

---

## ✅ Değişiklikten Sonra Kontrol

`secrets.env` dosyasını kaydettikten sonra anahtarların düzgün okunup okunmadığını test et:

```bash
cd /app/trm
python config.py
```

Çıktıda şunu görmelisin:
```
📱 TELEGRAM: ✅ Yapılandırıldı
🤖 OPENAI: ✅ Yapılandırıldı
📺 YOUTUBE: ✅ Yapılandırıldı
☁️ GOOGLE SERVİSLERİ: ✅ Yapılandırıldı
```

❌ işareti varsa → ilgili anahtar boş veya yanlış formatta.

---

## 🚀 Sistemi Çalıştırma

```bash
cd /app/trm
python main_orchestrator.py
```

**Tek modülü test için:**
```bash
python ai_integration.py          # AI testi
python telegram_listener.py       # Telegram testi
python web_scraper.py             # Scraper testi
python social_media_automation.py # Sosyal medya testi
```

---

## 🛡️ Güvenlik Hatırlatmaları

1. **`secrets.env` ve `credentials.json`** dosyalarını **ASLA** GitHub'a, Drive'a veya başkalarına göndermeyin
2. `.gitignore` zaten bunları koruyor — silmeyin
3. Bir anahtar sızdıysa → **derhal iptal edip yenisini oluşturun**
4. OpenAI'da **kullanım limiti** ayarlayın (Settings → Limits → "Hard limit": 20$)
5. Telegram bot token'i sızdıysa → BotFather'da `/revoke` ile iptal

---

## 📞 Yardım

Bir anahtar düzgün bağlanmıyorsa:
1. `secrets.env`'de **boşluk veya tırnak işareti** olmadığından emin ol
2. Anahtarın **başında/sonunda boşluk** olmasın
3. `python config.py` çalıştırıp hata mesajına bak
4. İlgili platformun konsolundan anahtarın **aktif** olduğunu doğrula

🌟 İyi kullanımlar!
