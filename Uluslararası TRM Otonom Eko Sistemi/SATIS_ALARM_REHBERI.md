# 🚨 TRM Nirvana v3.0 - Satış Alarm ve Uyarı Sistemi

## 📋 İçindekiler
1. [Satış Alarm Sistemi Nedir?](#satış-alarm-sistemi-nedir)
2. [Alarm Paneli Nasıl Açılır?](#alarm-paneli-nasıl-açılır)
3. [Alarm Türleri ve Anlamları](#alarm-türleri-ve-anlamları)
4. [Satış Hareketlerini Takip Etme](#satış-hareketlerini-takip-etme)
5. [Bildirimleri Görme](#bildirimleri-görme)
6. [Alarm Ayarları](#alarm-ayarları)

---

## 🚨 Satış Alarm Sistemi Nedir?

TRM Nirvana v3.0'un **satış alarm sistemi**, panel üzerinden gerçekleşen tüm satış hareketlerini, ürün yakalamalarını ve sosyal medya paylaşımlarını gerçek zamanlı olarak takip eder ve önemli olaylarda size bildirim gönderir.

### 🎯 Amaç:
- Satış hareketlerini anlık takip etmek
- Başarılı operasyonları bildirmek
- Hedeflere ulaşıldığında uyarmak
- Performans metriklerini göstermek

---

## 🌐 Alarm Paneli Nasıl Açılır?

### Yöntem 1: Otomatik Başlatma
```
1. Sistemi başlat: SON_BASLAT.bat
2. "🚀 SİSTEMİ BAŞLAT" butonuna tıkla
3. Alarm paneli otomatik başlar
```

### Yöntem 2: Manuel Başlatma
```
1. SATIS_ALARM_PANEL.py çalıştır
2. Panel açılır: http://localhost:9002
3. Alarm sistemi aktif olur
```

### Panel Adresleri:
```
🚨 Satış Alarm Paneli: http://localhost:9002
📊 Ana Panel: http://localhost:9000
📊 Status API: http://localhost:9001/status
```

---

## 🔔 Alarm Türleri ve Anlamları

### 1. 🔥 Yüksek Komisyonlu Ürünler
**Ne Zaman Çalar:**
- Günde 3+ adet %20+ komisyonlu ürün yakalandığında

**Mesaj:**
```
🔥 Yüksek Komisyonlu Ürünler!
Bugün 5 adet %20+ komisyonlu ürün yakalandı!
```

**Anlamı:** Sistem yüksek değerli ürünler başarıyla yakalıyor.

---

### 2. 📱 Sosyal Medya Başarısı
**Ne Zaman Çalar:**
- Günde 5+ sosyal medya paylaşımı yapıldığında

**Mesaj:**
```
📱 Sosyal Medya Başarısı!
Bugün 8 adet sosyal medya paylaşımı yapıldı!
```

**Anlamı:** İçerik üretimi ve paylaşım başarılı.

---

### 3. 💰 Komisyon Hedefi
**Ne Zaman Çalar:**
- Tahmini günlük komisyon 50+ TL olduğunda

**Mesaj:**
```
💰 Komisyon Hedefi!
Tahmini günlük komisyon: 75.50 TL
```

**Anlamı:** Finansal hedeflere ulaşılıyor.

---

### 4. 📊 Yüksek Başarı Oranı
**Ne Zaman Çalar:**
- Sistem başarı oranı %80+ olduğunda

**Mesaj:**
```
📊 Yüksek Başarı Oranı!
Sistem başarı oranı: 85.5%
```

**Anlamı:** Sistem verimli çalışıyor.

---

## 📈 Satış Hareketlerini Takip Etme

### Panel Göstergeleri:
```
📦 Toplam Ürün: 15
🔥 %20+ Ürün: 5
📱 Sosyal Paylaşım: 8
💰 Tahmini Komisyon: 75.50 TL
```

### Gerçek Zamanlı Veriler:
- **Yakalanan Ürünler:** Telegram ve web scraper'dan gelen ürün sayısı
- **%20+ Ürünler:** Yüksek komisyonlu ürün sayısı
- **Sosyal Paylaşım:** Başarılı sosyal medya paylaşımı sayısı
- **Tahmini Komisyon:** Beklenen günlük kazanç

### Otomatik Güncelleme:
- Panel her 30 saniyede bir yenilenir
- Veriler gerçek zamanlı güncellenir
- Yeni alarm'lar anında görünür

---

## 🔔 Bildirimleri Görme

### Panel Üzerinde:
```
🚨 SATIS ALARM PANELI (http://localhost:9002)
├── 📊 İstatistikler (üst kısımda)
├── 🔔 Alert'ler (orta kısımda)
└── 🔄 Yenile butonu (alt kısımda)
```

### Alert Kartları:
```
🔥 Yüksek Komisyonlu Ürünler!
Bugün 5 adet %20+ komisyonlu ürün yakalandı!

📱 Sosyal Medya Başarısı!
Bugün 8 adet sosyal medya paylaşımı yapıldı!

💰 Komisyon Hedefi!
Tahmini günlük komisyon: 75.50 TL
```

### Renk Kodlaması:
- 🟢 **Yeşil:** Başarı alarmı
- 🟡 **Sarı:** Uyarı alarmı  
- 🔵 **Mavi:** Bilgilendirme alarmı

---

## 📱 Mobil Erişim

### Telefon/Tablet'tan:
```
🌐 http://localhost:9002 adresini açın
📱 Mobil uyumlu arayüz
🔄 Otomatik güncelleme
🔔 Anlık bildirimler
```

### Mobil Özellikler:
- Responsive tasarım
- Dokunmatik kontrol
- Gerçek zamanlı veriler
- Alert geçmişi

---

## ⚙️ Alarm Ayarları

### Varsayılan Ayarlar:
```python
alert_settings = {
    'min_commission': 20.0,      # Minimum komisyon oranı
    'min_price': 100.0,          # Minimum fiyat
    'success_threshold': 5,       # Başarılı paylaşım eşiği
    'check_interval': 300,       # Kontrol aralığı (saniye)
    'telegram_alerts': True,      # Telegram bildirimleri
    'panel_alerts': True          # Panel bildirimleri
}
```

### Ayarları Değiştirme:
```
1. SATIS_ALARM_SISTEMI.py dosyasını aç
2. alert_settings bölümünü bulun
3. Değerleri güncelleyin
4. Sistemi yeniden başlatın
```

---

## 🧪 Test Etme

### Test Alert'i:
```
1. Paneli aç: http://localhost:9002
2. "🧪 Test Alert" butonuna tıklayın
3. Test alarmı görünür
4. Paneli yenileyin
```

### Manuel Test:
```python
# Test alarm gönder
test_alert = {
    'type': 'test',
    'level': 'info',
    'title': '🧪 Test Alert!',
    'message': 'Bu bir test alarmıdır.',
    'timestamp': datetime.now().isoformat()
}
```

---

## 📊 Raporlama

### Günlük Rapor:
```
📅 Tarih: 10.05.2026
📦 Toplam Ürün: 15
🔥 %20+ Ürün: 5
📱 Sosyal Paylaşım: 8
💰 Tahmini Komisyon: 75.50 TL
📊 Başarı Oranı: 85.5%
```

### Alert Geçmişi:
- Son 50 alert kaydedilir
- Tarih ve zaman damgası
- Alert seviyesi ve mesajı
- İlgili veriler

---

## 🔧 Sorun Giderme

### Panel Açılmıyor:
```
❌ Çözüm: SATIS_ALARM_PANEL.py çalıştır
❌ Çözüm: Port 9002 kontrol et
❌ Çözüm: Ana sistemi başlat
```

### Alert'ler Görünmüyor:
```
❌ Çözüm: Paneli yenile
❌ Çözüm: Sistemi kontrol et
❌ Çözüm: Test alert gönder
```

### Veri Güncellenmiyor:
```
❌ Çözüm: Ana sistemi kontrol et
❌ Çözüm: İnternet bağlantısını kontrol et
❌ Çözüm: API anahtarlarını kontrol et
```

---

## 💡 İpuçları

### Etkili Kullanım:
```
✅ Paneli sık sık kontrol edin
✅ Alert'leri dikkate alın
✅ İstatistikleri takip edin
✅ Mobil erişimi kullanın
```

### Performans:
```
✅ Paneli sürekli açık tutun
✅ Otomatik güncellemeyi kullanın
✅ Test alarm'larla sistemi doğrulayın
✅ Logları kontrol edin
```

---

## 📞 Destek

### Hata Durumunda:
```
1. Ana sistemi kontrol et (CHECK_SYSTEM.bat)
2. Satış alarm panelini yeniden başlat
3. Log dosyalarını kontrol et
4. Test alert gönder
```

### İletişim:
```
📊 Satış Alarm Paneli: http://localhost:9002
📊 Ana Panel: http://localhost:9000
📊 Status API: http://localhost:9001/status
```

---

## 🎯 Başarı Metrikleri

### Hedefler:
```
📦 Günlük ürün: 50+
🔥 %20+ ürün: 20+
📱 Sosyal paylaşım: 100+
💰 Komisyon: 100+ TL
📊 Başarı oranı: 90%+
```

### Takip:
```
📈 Panelde görüntüle
📱 Mobil takip et
🔔 Alert'leri izle
📊 Raporları kontrol et
```

---

**TRM Nirvana v3.0 - Satış Alarm Sistemi**  
**🚨 Satış hareketlerinizi anlık takip edin!**

---

*Son güncelleme: 10 Mayıs 2026*  
*Versiyon: v3.0*  
*Durum: Production Ready*
