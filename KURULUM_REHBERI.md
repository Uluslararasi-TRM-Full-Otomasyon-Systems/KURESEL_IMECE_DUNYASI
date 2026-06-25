# 🚀 TRM Tam Otomasyon Sistemi — Kurulum Rehberi
## Teknik bilgi gerektirmez | Adım adım | Türkçe

---

## 📦 ADIM 1 — Python Kur (1 kez yapılır)

1. https://www.python.org/downloads adresine gidin
2. Sarı "Download Python" butonuna tıklayın
3. İndirilen dosyayı çalıştırın
4. **"Add Python to PATH"** kutusunu mutlaka işaretleyin ✅
5. "Install Now" tıklayın
6. Kurulum bitince "Close" tıklayın

---

## 🔑 ADIM 2 — secrets.env Dosyasını Doldurun

`Uluslararasi-TRM-Full-Otomasyon-Sistemi` klasöründeki
`secrets.env` dosyasını **Notepad** ile açın ve doldurun.

### Öncelikli 3 anahtar (sistemi hemen başlatır):

**a) Telegram (30 dakika)**
- https://my.telegram.org adresine gidin (Türkçe)
- "API development tools" tıklayın
- Uygulama adı: TRM → "Create application"
- `api_id` ve `api_hash` değerlerini kopyalayın
- secrets.env'e yapıştırın:
  ```
  TELEGRAM_API_ID=12345678
  TELEGRAM_API_HASH=abc123def456...
  ```

**b) DeepSeek AI (ücretsiz, 15 dakika)**
- https://platform.deepseek.com adresine gidin
- Kaydolun → "API Keys" → "Create new key"
- secrets.env'e yapıştırın:
  ```
  DEEPSEEK_API_KEY=sk-...
  ```

**c) Gmail (15 dakika)**
- Gmail hesabınızda 2FA açın: https://myaccount.google.com/security
- "Uygulama Şifreleri" → 16 haneli şifre alın
- secrets.env'e yapıştırın:
  ```
  EMAIL_ADDRESS=trendurunlermarket@gmail.com
  EMAIL_PASSWORD=xxxx xxxx xxxx xxxx
  ```

---

## ▶️ ADIM 3 — Sistemi Başlatın

`BASLAT.bat` dosyasına **çift tıklayın**

- İlk açılışta bağımlılıklar otomatik kurulur (5 dakika)
- Menü açılır → `[1]` tuşuna basın → ENTER
- Sistem çalışmaya başlar!

---

## 📱 ADIM 4 — Platform API'lerini Ekleyin

Her platform için `PLATFORM_SETUP_WIZARD.py` çalıştırın:

Menüden `[Z]` seçin → ekranda adım adım talimatlar görürsünüz

| Platform | Süre | Zorluk |
|---|---|---|
| Gmail e-posta | 15 dk | ⭐ Çok kolay |
| YouTube | 30 dk | ⭐⭐ Kolay |
| Telegram/Discord/Viber Business | 1-2 gün | ⭐⭐ Kolay |
| Facebook | 1-2 gün | ⭐⭐⭐ Orta |
| Instagram | 1-3 gün | ⭐⭐⭐ Orta |
| LinkedIn | 2-5 gün | ⭐⭐⭐ Orta |
| TikTok | 3-7 gün | ⭐⭐⭐⭐ Zor |
| Twitter/X | Ücretli ($100/ay) | 💰 |

---

## 🌐 ADIM 5 — 7/24 Çalışma (Opsiyonel)

Bilgisayarınız kapanırsa sistem durur. 7/24 için:

**Railway (Ücretsiz plan — tavsiye edilir):**
1. https://railway.app adresine gidin
2. GitHub hesabıyla giriş yapın
3. "New Project" → "Deploy from GitHub repo"
4. secrets.env değişkenlerini Railway'e girin
5. Deploy tıklayın → sistem bulutta çalışır

**Veya Render.com (ücretsiz):**
- https://render.com → benzer adımlar

---

## 🆘 Sorun Giderme

| Sorun | Çözüm |
|---|---|
| "Python bulunamadı" | ADIM 1'i tekrarlayın, PATH işaretleyin |
| "Modül bulunamadı" | BASLAT.bat'ta `[1]` seçince kurulum otomatik olur |
| Telegram bağlanmıyor | TELEGRAM_PHONE numaranızı secrets.env'e ekleyin |
| Instagram çalışmıyor | PLATFORM_SETUP_WIZARD.py → instagram rehberine bakın |
| E-posta gitmiyor | Gmail Uygulama Şifresi kullanıldığından emin olun |

---

## 📞 Sistem Çalışınca Ne Olur?

✅ Telegram kanallarından otomatik ürün toplanır  
✅ AI ile her platform için farklı içerik üretilir  
✅ Facebook, Instagram, Telegram, YouTube'a otomatik paylaşılır  
✅ Gelen mesajlara otomatik yanıt verilir  
✅ E-posta kampanyaları otomatik gönderilir  
✅ Satış ve komisyon takibi yapılır  
✅ Sistem çöküp kendini yeniden başlatır (Watchdog)  

