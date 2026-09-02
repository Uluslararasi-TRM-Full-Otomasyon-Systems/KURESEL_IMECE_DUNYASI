# TRM FULL OTOMASYON SİSTEMİ - MASAÜSTÜ KURULUM KILAVUZU

## 📋 İÇERİK TABLOSU

1. [Sistem Gereksinimleri](#sistem-gereksinimleri)
2. [Kurulum Adımları](#kurulum-adımları)
3. [İlk Çalıştırma](#ilk-çalıştırma)
4. [Panel Kullanımı](#panel-kullanımı)
5. [Sistem Yapılandırması](#sistem-yapılandırması)
6. [Sorun Giderme](#sorun-giderme)
7. [Güncelleme ve Bakım](#güncelleme-ve-bakım)

---

## 🔧 SİSTEM GEREKSİNİMLERİ

### Minimum Sistem Gereksinimleri
- **İşletim Sistemi:** Windows 10/11 (64-bit)
- **İşlemci:** Intel Core i3 veya AMD Ryzen 3
- **Bellek:** 4 GB RAM
- **Depolama:** 2 GB boş alan
- **Ağ:** İnternet bağlantısı

### Önerilen Sistem Gereksinimleri
- **İşletim Sistemi:** Windows 10/11 (64-bit)
- **İşlemci:** Intel Core i5 veya AMD Ryzen 5
- **Bellek:** 8 GB RAM
- **Depolama:** 5 GB boş alan
- **Ağ:** Hızlı internet bağlantısı

### Yazılım Gereksinimleri
- **Python 3.8+** (Python 3.10 önerilir)
- **Google Chrome** (Panel için)
- **Windows PowerShell** (Yüklü gelir)

---

## 📦 KURULUM ADIMLARI

### Adım 1: Python Kurulumu
1. [Python.org](https://www.python.org/downloads/) sitesine gidin
2. En son Python sürümünü indirin (3.10+ önerilir)
3. Kurulum dosyasını çalıştırın
4. **"Add Python to PATH"** kutucuğunu işaretleyin
5. **"Install Now"** butonuna tıklayın
6. Kurulumun tamamlanmasını bekleyin

### Adım 2: Gerekli Kütüphanelerin Kurulumu
1. **Windows + R** tuşlarına basın
2. `cmd` yazın ve Enter'a basın
3. Aşağıdaki komutu çalıştırın:
```cmd
pip install asyncio psutil requests matplotlib google-api-python-client google-auth-httplib2 google-auth-oauthlib flask beautifulsoup4 selenium
```

### Adım 3: TRM Sisteminin Kurulumu
1. TRM Full Otomasyon Sistemi klasörünü masaüstüne kopyalayın
2. Klasörün içindeki tüm dosyaların varlığını kontrol edin:
   - `MASTER_BASLATICI.bat`
   - `PANEL_ACICI.bat`
   - `PANEL_ACICI_HTML.html`
   - `ENHANCED_PANEL.py`
   - `management_panel.py`
   - Diğer Python dosyaları

### Adım 4: İlk Yapılandırma
1. `secrets.env` dosyasını açın
2. API anahtarlarınızı girin:
```env
TELEGRAM_API_ID=sizin_telegram_api_id
TELEGRAM_API_HASH=sizin_telegram_hash
TELEGRAM_PHONE=+90555xxxxxxx
DEEPSEEK_API_KEY=sizin_deepseek_anahtari
CLAUDE_API_KEY=sizin_claude_anahtari
FACEBOOK_ACCESS_TOKEN=sizin_facebook_token
INSTAGRAM_ACCESS_TOKEN=sizin_instagram_token
TIKTOK_ACCESS_TOKEN=sizin_tiktok_token
YOUTUBE_API_KEY=sizin_youtube_anahtari
GOOGLE_DRIVE_FOLDER_ID=sizin_drive_klasor_id
DISCORD_WEBHOOK_URL=sizin_discord_webhook_url
BANK_API_KEY=sizin_banka_anahtari
STORE_URL=https://trendurunlermarket.com
COMMISSION_THRESHOLD=20.0
CHECK_INTERVAL=300
MAX_PRODUCTS_PER_DAY=50
```

### Adım 5: Güvenlik Ayarları
1. Windows Defender'ı açın
2. "Virüs ve tehdit koruması" > "Yönetim ayarları"
3. "Gelen dışlamalar ekle" > "Klasör dışlaması ekle"
4. TRM sistem klasörünü seçin ve dışlama ekleyin
5. Antivirüs programınızda benzer ayarı yapın

---

## 🚀 İLK ÇALIŞTIRMA

### 1. Sistemi Başlatma
1. `MASTER_BASLATICI.bat` dosyasına çift tıklayın
2. Kurulum kontrolü yapılacak
3. Tüm sistemler otomatik olarak başlatılacak
4. Paneller erişime hazır hale gelecek

### 2. Panel Erişimi
Sistem başladıktan sonra şu adreslerden panellere erişebilirsiniz:
- **Ana Panel:** http://localhost:9000
- **Status API:** http://localhost:9001/status
- **Satış Alarmı:** http://localhost:9002
- **Gelişmiş Panel:** http://localhost:9003

### 3. Panel Açıcı Kullanımı
1. `PANEL_ACICI.bat` dosyasına çift tıklayın
2. Tüm paneller otomatik olarak açılır
3. Veya `PANEL_ACICI_HTML.html` dosyasını açın
4. Web arayüzünden panelleri tek tıkla açın

---

## 🌐 PANEL KULLANIMI

### Ana Panel (Port 9000)
**Özellikler:**
- Sistem durumu takibi
- Modül kontrolü
- Başlatma/durdurma butonları
- Gerçek zamanlı istatistikler

**Kullanım:**
1. Ana paneli açın
2. Sistem durumunu kontrol edin
3. İstediğiniz modülü başlatın/durun

### Status API (Port 9001)
**Özellikler:**
- JSON formatında sistem durumu
- Programatik erişim
- API entegrasyonu

**Kullanım:**
```json
{
  "system_status": "running",
  "uptime": 3600,
  "auto_restarts": 0,
  "health_score": 100,
  "errors": 0,
  "warnings": 0
}
```

### Satış Alarm Paneli (Port 9002)
**Özellikler:**
- Satış bildirimleri
- Komisyon takibi
- Alarm geçmişi
- Test bildirimi

**Kullanım:**
1. Paneli açın
2. Satış bildirimlerini izleyin
3. Test bildirimi gönderin

### Gelişmiş Panel (Port 9003)
**Özellikler:**
- 12 farklı panel sayfası
- Detaylı sistem analizi
- Grafiksel gösterim
- Mobil uyumluluk

**Panel Sayfaları:**
1. **Sistem Durumu** - 7/24 çalışma durumu
2. **Günlük İstatistikler** - Günlük performans
3. **Hata Logları** - Tüm hata kayıtları
4. **Sosyal Medya** - Paylaşılan içerikler
5. **AI Performansı** - AI işlem tablosu
6. **Web Veri Toplama** - Scraping durumu
7. **Satış Grafikleri** - En çok satışlar
8. **%20+ Komisyon** - Yüksek komisyonlu ürünler
9. **Satılan Ürünler** - trendurunlermarket satışları
10. **Komisyon Takibi** - 14 günlük takip
11. **Günlük Komisyon** - Günlük ödemeler
12. **24 Saat Sıfırlama** - Otomatik temizlik

---

## ⚙️ SİSTEM YAPILANDIRMASI

### secrets.env Dosyası Ayarları
```env
# Telegram Ayarları
TELEGRAM_API_ID=12345678
TELEGRAM_API_HASH=abcdef123456789
TELEGRAM_PHONE=+90555xxxxxxx

# AI Servisleri
DEEPSEEK_API_KEY=sk-deepseek-xxxxxxxxxx
CLAUDE_API_KEY=sk-ant-xxxxxxxxxx

# Sosyal Medya
FACEBOOK_ACCESS_TOKEN=EAACxxxxxxxxxx
INSTAGRAM_ACCESS_TOKEN=IGQWRxxxxxxxxxx
TIKTOK_ACCESS_TOKEN=xxxxxxxxxx
YOUTUBE_API_KEY=AIzaSyxxxxxxxxxx

# Google Drive
GOOGLE_DRIVE_FOLDER_ID=1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms

# Telegram/Discord/Viber ve Banka
DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/...
BANK_API_KEY=xxxxxxxxxx

# Sistem Ayarları
STORE_URL=https://trendurunlermarket.com
COMMISSION_THRESHOLD=20.0
CHECK_INTERVAL=300
MAX_PRODUCTS_PER_DAY=50
```

### Port Ayarları
Varsayılan portlar:
- **Ana Panel:** 9000
- **Status API:** 9001
- **Satış Alarmı:** 9002
- **Gelişmiş Panel:** 9003
- **Telegram/Discord/Viber Webhook:** 9004
- **Banka Webhook:** 9005

Port değiştirmek için Python dosyalarındaki PORT değişkenini güncelleyin.

### Log Ayarları
Log dosyaları `logs/` klasöründe saklanır:
- `system_manager.log` - Sistem yönetimi logları
- `auto_restart.log` - Otomatik yeniden başlatma logları
- `drive_social_manager.log` - Drive ve sosyal medya logları
- `messaging_notifications.log` - Telegram/Discord/Viber bildirim logları
- `bank_commission.log` - Banka komisyon logları

---

## 🔧 SORUN GİNDERME

### Panel Açılmıyor
**Sorun:** Paneller erişilemiyor

**Çözüm:**
1. Sistemi başlatın: `MASTER_BASLATICI.bat`
2. 30 saniye bekleyin
3. Portları kontrol edin: `netstat -an | findstr ":900"`
4. Firewall'ı kontrol edin
5. Antivirüsü geçici olarak devre dışı bırakın

### Python Hataları
**Sorun:** Python modülleri bulunamadı

**Çözüm:**
```cmd
pip install --upgrade pip
pip install asyncio psutil requests matplotlib google-api-python-client google-auth-httplib2 google-auth-oauthlib flask beautifulsoup4 selenium
```

### API Anahtar Hataları
**Sorun:** API anahtarları geçersiz

**Çözüm:**
1. `secrets.env` dosyasını kontrol edin
2. API anahtarlarının doğru olduğundan emin olun
3. Servis sağlayıcınızdan yeni anahtar alın

### Performans Sorunları
**Sorun:** Sistem yavaş çalışıyor

**Çözüm:**
1. Bilgisayarı yeniden başlatın
2. Gereksiz programları kapatın
3. Bellek kullanımını kontrol edin
4. Disk alanını temizleyin

### 7/24 Çalışma Sorunları
**Sorun:** Sistem duruyor

**Çözüm:**
1. `CHECK_SYSTEM.bat` çalıştırın
2. Hata loglarını kontrol edin
3. Sistemi yeniden başlatın
4. Otomatik yeniden başlatma ayarlarını kontrol edin

---

## 🔄 GÜNCELLEME VE BAKIM

### Günlük Bakım
**Her gün yapılması gerekenler:**
1. Sistem durumunu kontrol et
2. Hata loglarını kontrol et
3. Performans verilerini incele
4. Yedek al

**Haftalık bakım:**
1. Log dosyalarını temizle (30 günden eski)
2. Sistem performansını optimize et
3. API anahtarlarını kontrol et
4. Güncellemeleri kontrol et

### Yedekleme
**Yedeklenecek dosyalar:**
- `secrets.env` - API anahtarları
- `logs/` - Log dosyaları
- `data/` - Veri dosyaları
- `config.py` - Yapılandırma dosyası

**Yedekleme komutu:**
```cmd
xcopy "TRM Full Otomasyon Sistemi" "TRM_Yedek_%date%" /E /I /H /Y
```

### Sistem Güncellemesi
1. Mevcut sistemi durdurun
2. Yeni sürümü indirin
3. `secrets.env` dosyasını yedekleyin
4. Yeni dosyaları kopyalayın
5. `secrets.env` dosyasını geri kopyalayın
6. Sistemi yeniden başlatın

---

## 📞 DESTEK

### İletişim Bilgileri
- **E-posta:** support@trmnirvana.com
- **Telegram:** @trm_nirvana_support
- **Telegram/Discord/Viber:** +90 542 623 5116

### Destek Bilgileri
Destek talebi gönderirken şu bilgileri ekleyin:
- İşletim sistemi sürümü
- Python sürümü
- Hata mesajı
- Log dosyaları
- Ekran görüntüsü

### Sıkça Sorulan Sorular
**S: Sistem 7/24 çalışır mı?**
C: Evet, otomatik yeniden başlatma ile 7/24 çalışır.

**S: Kaç panel var?**
C: 4 ana panel ve 12 alt panel bulunur.

**S: Mobil erişim mümkün mü?**
C: Evet, aynı ağ içinde mobil cihazlardan erişilebilir.

**S: Verilerim güvende mi?**
C: Evet, tüm veriler yerel olarak saklanır.

---

## 📋 KONTROL LİSTESİ

### Kurulum Sonrası Kontrol
- [ ] Python kurulu ve PATH'e eklenmiş
- [ ] Gerekli kütüphaneler kurulmuş
- [ ] secrets.env dosyası yapılandırılmış
- [ ] Firewall ayarları yapılmış
- [ ] Sistem başlatılmış
- [ ] Paneller erişilebilir durumda

### İlk Çalıştırma Kontrolü
- [ ] MASTER_BASLATICI.bat çalışıyor
- [ ] Ana panel açılıyor (9000)
- [ ] Status API çalışıyor (9001)
- [ ] Satış alarmı çalışıyor (9002)
- [ ] Gelişmiş panel açılıyor (9003)
- [ ] Log dosyaları oluşturuluyor
- [ ] Hata yok

### Günlük Kontrol
- [ ] Sistem durumu normal
- [ ] Modüller çalışıyor
- [ ] Bildirimler geliyor
- [ ] Performans iyi
- [ ] Hata logları temiz

---

**TRM FULL OTOMASYON SİSTEMİ v3.0 - Masaüstü Kurulum Kılavuzu**

*Bu kılavuz ile sisteminizi kolayca kurabilir ve kullanmaya başlayabilirsiniz.*
