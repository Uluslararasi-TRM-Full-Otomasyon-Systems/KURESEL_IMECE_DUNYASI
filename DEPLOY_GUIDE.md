# 🚀 DEPLOY KILAVUZU — TRM v5.1
## Railway'e Tek Tıklamayla Bulut Deploy

---

## 1. NEDEN RAİLWAY?

| Platform | Ücretsiz Plan | Kolaylık | Öneri |
|----------|--------------|---------|-------|
| Railway | 500 saat/ay | ⭐⭐⭐⭐⭐ | ✅ ÖNERİLİR |
| Render | 750 saat/ay | ⭐⭐⭐⭐ | ✅ Alternatif |
| VPS (Hetzner) | Hayır | ⭐⭐⭐ | İleride |

---

## 2. RAİLWAY DEPLOY — ADIM ADIM

### Adım 1 — Railway Hesabı Aç
```
https://railway.app
```
→ "Login with GitHub" tıkla
→ GitHub hesabınla giriş yap

### Adım 2 — Yeni Proje Oluştur
→ "New Project" tıkla
→ "Deploy from GitHub repo" seç
→ `Uluslararasi-TRM-Full-Otomasyon-Sistemi` repo'sunu seç
→ "Deploy Now" tıkla

### Adım 3 — API Anahtarlarını Gir
→ Proje açıkken "Variables" sekmesine tıkla
→ Her anahtarı tek tek ekle:

```
TELEGRAM_API_ID          = 12345678
TELEGRAM_API_HASH        = abcdef123456...
TELEGRAM_BOT_TOKEN       = 123456:ABC-DEF...
TELEGRAM_CHAT_ID         = -100123456789
OPENAI_API_KEY           = sk-...
DEEPSEEK_API_KEY         = sk-...
BUFFER_ACCESS_TOKEN      = ...
DROPBOX_ACCESS_TOKEN     = ...
TRM_MODE                 = live
```

### Adım 4 — Deploy!
→ "Deploy" tıkla
→ 3-5 dakika bekle
→ Sistem 7/24 çalışmaya başlar ✅

---

## 3. RENDER ALTERNATİF DEPLOY

```
https://render.com
```
→ "New Web Service"
→ GitHub repo bağla
→ Build Command: `pip install -r requirements.txt`
→ Start Command: `python main_orchestrator.py`
→ Environment Variables ekle
→ "Create Web Service" tıkla

---

## 4. GÜVENLİK — DEPLOY ÖNCESİ KONTROL LİSTESİ

```
☐ secrets.env dosyası .gitignore'da mı?
☐ .gitignore dosyasında şunlar var mı:
    secrets.env
    *.env
    token.pickle
    credentials.json
    logs/
    data/
    __pycache__/
    *.pyc
☐ GitHub'da secrets.env dosyası görünüyor mu?
  → Varsa: git rm --cached secrets.env → commit → push
```

---

## 5. YENİ PROJE KOPYALAMA (DİĞER FİRMALAR İÇİN)

```bash
# 1. GitHub'dan klonla
git clone https://github.com/Uluslararasi-TRM-Full-Otomasyon-Systems/Uluslararasi-TRM-Full-Otomasyon-Sistemi.git YENI_FIRMA

# 2. Yeni klasöre gir
cd YENI_FIRMA

# 3. Yeni secrets.env oluştur
cp secrets.env.example secrets.env

# 4. secrets.env içinde değiştir:
SYSTEM_NAME=YENI_FIRMA_ADI
TELEGRAM_BOT_TOKEN=yeni_firma_bot_token
BUFFER_ACCESS_TOKEN=yeni_firma_buffer_token
TARGET_SUPPLIER_URLS=https://yeni-tedarikci.com
BANKA_IBAN=yeni_firma_iban

# 5. Yeni GitHub repo aç → push
# 6. Railway'de yeni proje → bu repoyu seç → deploy
```

---

## 6. KOD GİZLEME (OPSİYONEL)

```bash
# PyArmor kurulumu
pip install pyarmor

# Kodu gizle
pyarmor gen --output dist/ *.py

# dist/ klasörünü deploy et
# Kaynak kod artık okunamaz
```

---

## 7. SORUN GİDERME

| Sorun | Çözüm |
|-------|-------|
| "Module not found" | requirements.txt'e ekle |
| "secrets.env not found" | Railway Variables'a gir |
| Port hatası | PORT=9000 ekle |
| Bellek yetersiz | Starter plan → Basic plan yükselt |
| Deployment başarısız | Logs sekmesine bak |
