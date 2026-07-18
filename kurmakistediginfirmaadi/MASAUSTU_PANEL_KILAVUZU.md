# 🖥️ TRM Nirvana v3.0 - Masaüstü Panel Kılavuzu

## 📋 İçindekiler
1. [Paneli Açma](#paneli-açma)
2. [Sistemi Çalıştırma](#sistemi-çalıştırma)
3. [Sistem Durumu](#sistem-durumu)
4. [Takip Edilmesi Gerekenler](#takip-edilmesi-gerekenler)
5. [Sorun Giderme](#sorun-giderme)
6. [Önemli Notlar](#önemli-notlar)

---

## 🚀 Paneli Açma

### Yöntem 1: Otomatik Başlatıcı
```
1. Flash belleği takın
2. Çift tıklayın: SON_BASLAT.bat
3. Kontrol paneli otomatik açılır
```

### Yöntem 2: Manuel Başlatma
```
1. Flash bellekteki klasöre gidin
2. Çalıştırın: SON_BASLAT.bat
3. Açılan HTML'de butona tıklayın
```

### Yöntem 3: Doğrudan HTML
```
1. Dosyayı açın: TEK_TIK_SON.html
2. "🚀 SİSTEMİ BAŞLAT" butonuna tıklayın
```

---

## 🤖 Sistemi Çalıştırma

### Adım 1: Başlatıcıyı Çalıştır
```
✅ SON_BASLAT.bat çalıştır
✅ Bekleyin (2-3 saniye)
✅ Kontrol paneli açılır
```

### Adım 2: Sistemi Başlat
```
✅ "🚀 SİSTEMİ BAŞLAT" butonuna tıkla
✅ Bekleyin (10-15 saniye)
✅ Tüm modüller başlar
```

### Adım 3: Paneli Kullan
```
✅ Panel otomatik açılır: http://localhost:9000
✅ Sistem durumu görünür
✅ Kontroller yapılabilir
```

---

## 📊 Sistem Durumu

### Çalışan Modüller
```
🤖 Ana Orchestrator     → Sistem koordinasyonu
📱 Telegram Dinleyici   → Ürün yakalama
🌐 Web Scraper         → Site tarama
✨ AI Entegrasyonu      → İçerik üretimi
📢 Sosyal Medya        → Paylaşım
☁️ Google Drive        → Veri depolama
🌐 Web Panel           → Kontrol arayüzü
```

### Durum Göstergeleri
```
✅ Yeşil = Sistem çalışıyor
❌ Kırmızı = Sistem kapalı
⚠️ Sarı = Sistem başlıyor/duruyor
```

---

## 👁️ Takip Edilmesi Gerekenler

### 1. Sistem Durumu
```
📊 Status API: http://localhost:9001/status
🌐 Panel: http://localhost:9000
```

### 2. Günlük İstatistikler
```
📦 Yakalanan ürün sayısı
🔥 %20+ komisyonlu ürünler
📱 Sosyal medya paylaşım sayısı
💰 Tahmini komisyon kazancı
```

### 3. Modül Performansı
```
🤖 AI işlem süresi
📱 Sosyal medya başarısı
🌐 Web scraper hızı
📊 Veri akışı durumu
```

### 4. Hata Takibi
```
📋 Log dosyaları: logs/ klasörü
🔍 Hata mesajları
⚠️ Uyarılar
📝 Sistem logları
```

---

## 🎛️ Panel Kontrolleri

### Ana Panel (http://localhost:9000)
```
📊 Sistem durumu göstergeleri
📈 Gerçek zamanlı istatistikler
🔄 Modül başlat/durdur
📋 Canlı loglar
⚙️ Ayarlar
```

### Kontrol Paneli (TEK_TIK_SON.html)
```
🚀 SİSTEMİ BAŞLAT/DURDUR
📊 Modül durumları
⏰ Çalışma süresi
🌐 Erişim linkleri
```

---

## 📋 Günlük Kontrol Listesi

### Her Gün Yapılacaklar
```
☐ Sistem durumunu kontrol et
☐ Günlük raporu kontrol et
☐ Hata loglarını kontrol et
☐ Performans metriklerini kontrol et
☐ Sosyal medya paylaşımlarını kontrol et
```

### Her Hafta Yapılacaklar
```
☐ Veritabanını temizle
☐ Log dosyalarını arşivle
☐ API anahtarlarını kontrol et
☐ Sistem performansını analiz et
☐ Yedekleme yap
```

---

## ⚠️ Sorun Giderme

### Sistem Başlamıyor
```
❌ Çözüm: SON_BASLAT.bat çalıştır
❌ Çözüm: Python kontrol et
❌ Çözüm: Portları kontrol et (9000, 9001)
```

### Panel Açılmıyor
```
❌ Çözüm: Tarayıcıyı yenile
❌ Çözüm: http://localhost:9000 adresini kontrol et
❌ Çözüm: Firewall kontrol et
```

### Modüller Çalışmıyor
```
❌ Çözüm: API anahtarlarını kontrol et
❌ Çözüm: İnternet bağlantısını kontrol et
❌ Çözüm: Log dosyalarını kontrol et
```

---

## 🔧 Önemli Ayarlar

### API Anahtarları (secrets.env)
```
TELEGRAM_API_ID=xxx
TELEGRAM_API_HASH=xxx
DEEPSEEK_API_KEY=xxx
CLAUDE_API_KEY=xxx
FACEBOOK_ACCESS_TOKEN=xxx
```

### Sistem Ayarları
```
STORE_URL=https://trendurunlermarket.com
COMMISSION_THRESHOLD=20.0
CHECK_INTERVAL=300
MAX_PRODUCTS_PER_DAY=50
```

---

## 📱 Mobil Erişim

### Telefon/Tablet'tan Erişim
```
🌐 Panel: http://localhost:9000
📊 Status: http://localhost:9001/status
📱 Mobil uyumlu arayüz
🔄 Gerçek zamanlı güncelleme
```

---

## ☁️ Cloud Deployment

### Railway (Önerilen)
```
1. railway.app/new adresine gidin
2. GitHub reposu oluşturun
3. Dosyaları yükleyin
4. Deploy edin
5. URL'i alın
```

### Render
```
1. render.com adresine gidin
2. Web Service oluşturun
3. Repoyu bağlayın
4. Build edin
```

---

## 💡 İpuçları

### Performans İçin
```
✅ Sistemi her gün kontrol et
✅ Log dosyalarını temizle
✅ Veritabanını optimize et
✅ API limitlerini kontrol et
```

### Güvenlik İçin
```
✅ API anahtarlarını güncel tut
✅ Firewall ayarlarını kontrol et
✅ Yedekleme yap
✅ Erişim loglarını izle
```

---

## 📞 Destek

### Hata Durumunda
```
1. CHECK_SYSTEM.bat çalıştır
2. Log dosyalarını kontrol et
3. Portları kontrol et
4. İnternet bağlantısını kontrol et
```

### İletişim
```
📋 Log dosyaları: logs/
📊 Sistem durumu: CHECK_SYSTEM.bat
🌐 Panel: http://localhost:9000
```

---

## 🎯 Başarı Metrikleri

### Hedefler
```
📦 Günlük ürün: 50+
🔥 %20+ ürün: 20+
📱 Sosyal paylaşım: 100+
💰 Komisyon: Aktif
📊 Başarı oranı: 95%+
```

### Takip
```
📈 Grafikler panelde
📋 Raporlar günlük
🔍 Analytics Google Drive
📊 Metrikler gerçek zamanlı
```

---

**TRM Nirvana v3.0 - 7/24 Otomasyon Sistemi**  
**🚀 Tek tıkla başlat, 7/24 çalış, her yerden eriş!**

---

*Son güncelleme: 10 Mayıs 2026*  
*Versiyon: v3.0*  
*Durum: Production Ready*
