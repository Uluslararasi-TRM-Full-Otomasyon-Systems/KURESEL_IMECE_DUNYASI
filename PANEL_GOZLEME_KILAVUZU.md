# TRM FULL OTOMASYON SİSTEMİ - PANEL GÖZLEMLEME VE KULLANIM KILAVUZU

## 📋 İÇERİK TABLOSU

1. [Panel Genel Bakışı](#panel-genel-bakışı)
2. [Ana Panel (Port 9000)](#ana-panel-port-9000)
3. [Status API (Port 9001)](#status-api-port-9001)
4. [Satış Alarm Paneli (Port 9002)](#satış-alarm-paneli-port-9002)
5. [Gelişmiş Panel (Port 9003)](#gelişmiş-panel-port-9003)
6. [Panel Arası Geçiş](#panel-arası-geçiş)
7. [Mobil Erişim](#mobil-erişim)
8. [Veri Analizi ve Raporlama](#veri-analizi-ve-raporlama)
9. [Performans Optimizasyonu](#performans-optimizasyonu)
10. [Sorun Giderme](#sorun-giderme)

---

## 🌐 PANEL GENEL BAKIŞI

### Panel Mimarisi
TRM Full Otomasyon Sistemi 4 ana panelden oluşur:
- **Ana Panel:** Sistem kontrol merkezi
- **Status API:** Programatik erişim
- **Satış Alarmı:** Satış bildirimleri
- **Gelişmiş Panel:** Detaylı analiz

### Panel Özellikleri
- ✅ Gerçek zamanlı veri güncelleme
- ✅ 7/24 kesintisiz çalışma
- ✅ Mobil uyumlu arayüz
- ✅ Otomatik yenileme
- ✅ Hata takibi ve bildirim
- ✅ Performans izleme

### Erişim Bilgileri
```
📊 Ana Panel: http://localhost:9000
📈 Status API: http://localhost:9001/status
🚨 Satış Alarmı: http://localhost:9002
🌐 Gelişmiş Panel: http://localhost:9003
```

---

## 🖥️ ANA PANEL (PORT 9000)

### Panel Açılışı
1. `PANEL_ACICI.bat` çalıştırın
2. "Ana Panel" butonuna tıklayın
3. Veya doğrudan: http://localhost:9000

### Ana Bileşenler

#### 🎯 Sistem Durumu Göstergeleri
- **Telegram:** 🟢 Aktif / 🔴 Kapalı
- **Web Scraper:** 🟢 Aktif / 🔴 Kapalı
- **AI Motoru:** 🟢 Aktif / 🔴 Kapalı
- **Sosyal Medya:** 🟢 Aktif / 🔴 Kapalı
- **Google Drive:** 🟢 Aktif / 🔴 Kapalı

#### 📊 İstatistik Kartları
- **Toplanan Ürün:** Kaç ürün toplandı
- **%20+ Ürün:** Yüksek komisyonlu ürün sayısı
- **Bugün Paylaşım:** Bugünkü sosyal medya paylaşımı
- **Kazanılan Komisyon:** Toplam kazanç

#### 🎛️ Kontrol Butonları
- **🔥 NIRVANA MODU BAŞLAT:** Tüm sistemleri başlatır
- **📊 SİSTEM SAĞLIK KONTROLÜ:** Sistem durumunu kontrol eder
- **💰 KOMİSYON BOTU:** %20+ ürünleri arar
- **✨ AI İÇERİK ÜRET:** AI ile içerik oluşturur
- **📢 SOSYAL MEDYADA ANINDA PAYLAŞ:** Sosyal medyada paylaşır
- **📈 GÜNLÜK ÖZET RAPOR AL:** Günlük rapor oluşturur

### Log Alanı
- Gerçek zamanlı log gösterimi
- Renk kodlu hata/uyarı/bilgi mesajları
- Otomatik kaydırma
- Temizleme butonu

### Kullanım İpuçları
- **Ctrl+R:** Paneli yenile
- **F5:** Tam yenileme
- **Otomatik yenileme:** 30 saniyede bir
- **Log arama:** Ctrl+F ile log içinde arama

---

## 📈 STATUS API (PORT 9001)

### API Erişimi
```
GET http://localhost:9001/status
```

### Yanıt Formatı
```json
{
  "system_status": "running",
  "uptime": 3600,
  "auto_restarts": 0,
  "health_score": 100,
  "errors": 0,
  "warnings": 0,
  "processes_running": 5,
  "memory_usage": "45.2%",
  "cpu_usage": "12.8%",
  "last_update": "2024-01-15T14:30:00"
}
```

### API Parametreleri
- **system_status:** Sistem durumu (running/stopped/error)
- **uptime:** Çalışma süresi (saniye)
- **auto_restarts:** Otomatik yeniden başlatma sayısı
- **health_score:** Sağlık skoru (0-100)
- **errors:** Hata sayısı
- **warnings:** Uyarı sayısı
- **processes_running:** Çalışan process sayısı
- **memory_usage:** Bellek kullanımı
- **cpu_usage:** CPU kullanımı
- **last_update:** Son güncelleme zamanı

### Kullanım Senaryoları

#### 1. Sistem Durumu Kontrolü
```javascript
fetch('http://localhost:9001/status')
  .then(response => response.json())
  .then(data => {
    console.log('Sistem durumu:', data.system_status);
    console.log('Sağlık skoru:', data.health_score);
  });
```

#### 2. Otomatik İzleme
```javascript
setInterval(async () => {
  const response = await fetch('http://localhost:9001/status');
  const data = await response.json();
  
  if (data.health_score < 50) {
    alert('Sistem sağlığı kritik seviyede!');
  }
}, 60000); // Her dakika
```

#### 3. Entegrasyon
```python
import requests

def get_system_status():
    response = requests.get('http://localhost:9001/status')
    return response.json()

status = get_system_status()
print(f"Sistem durumu: {status['system_status']}")
```

---

## 🚨 SATIŞ ALARM PANELİ (PORT 9002)

### Panel Açılışı
1. `PANEL_ACICI.bat` çalıştırın
2. "Satış Alarmı" butonuna tıklayın
3. Veya doğrudan: http://localhost:9002

### Ana Özellikler

#### 📊 İstatistik Göstergeleri
- **Toplam Ürün:** Kaç ürün takip ediliyor
- **%20+ Ürün:** Yüksek komisyonlu ürün sayısı
- **Bugünkü Satış:** Bugün yapılan satış sayısı
- **Toplam Kazanç:** Toplam komisyon kazancı

#### 🔔 Alarm Kartları
- **Satış Bildirimleri:** Yeni satış olduğunda
- **Komisyon Uyarıları:** Yüksek komisyonlu ürünler
- **Hata Bildirimleri:** Sistem hataları
- **Başarı Bildirimleri:** Başarılı işlemler

#### 🎛️ Kontrol Butonları
- **🔄 Yenile:** Verileri günceller
- **🧪 Test Bildirimi:** Test alarm gönderir
- **📊 Özet Rapor:** Özet rapor gösterir
- **🔕 Bildirimleri Temizle:** Bildirimleri temizler

### Alarm Türleri

#### 🟢 Başarı Bildirimleri
- Ürün başarıyla toplandı
- Sosyal medyada paylaşıldı
- AI içerik üretildi
- Komisyon hesaplandı

#### 🟡 Uyarı Bildirimleri
- Düşük komisyonlu ürün
- Sistem yavaşlığı
- Bellek kullanımı yüksek
- Ağ bağlantı sorunları

#### 🔴 Hata Bildirimleri
- API anahtar hatası
- Sistem çökmesi
- Veri tabanı hatası
- Servis bağlantı hatası

### Bildirim Yapılandırması
```javascript
// Bildirim ayarları
const notificationSettings = {
  sales: true,        // Satış bildirimleri
  commission: true,   // Komisyon bildirimleri
  errors: true,       // Hata bildirimleri
  warnings: true,     // Uyarı bildirimleri
  autoRefresh: 30000, // Otomatik yenileme (ms)
  soundAlert: true     // Sesli uyarı
};
```

---

## 🌐 GELİŞMİŞ PANEL (PORT 9003)

### Panel Açılışı
1. `PANEL_ACICI.bat` çalıştırın
2. "Gelişmiş Panel" butonuna tıklayın
3. Veya doğrudan: http://localhost:9003

### Panel Sayfaları

#### 📋 1. Sistem Durumu
- 7/24 çalışma durumu
- Otomatik yeniden başlatma sayısı
- Sağlık skoru
- Hata ve uyarı sayıları
- Bellek ve CPU kullanımı

#### 📊 2. Günlük İstatistikler
- Günlük ürün toplama
- Günlük paylaşım sayısı
- Günlük kazanç
- Başarı oranı
- Performans metrikleri

#### 🔍 3. Hata Logları
- Tüm hata kayıtları
- Zaman damgası
- Hata seviyesi
- Modül bilgisi
- Detaylı hata mesajları

#### 📱 4. Sosyal Medya
- Paylaşılan içerikler
- Platform bazında istatistikler
- Etkileşim verileri
- Paylaşım zamanları
- Başarı durumu

#### 🤖 5. AI Performansı
- AI işlem sayısı
- Başarılı/başarısız işlemler
- Ortalama yanıt süresi
- Token kullanımı
- Model bazında performans

#### 🌐 6. Web Veri Toplama
- Son scraping zamanı
- Toplanan ürün sayısı
- Başarılı scraping sayısı
- Hata oranları
- Site bazında istatistikler

#### 📈 7. Satış Grafikleri
- En çok satılan ürünler
- Satış trendleri
- Komisyon grafikleri
- Platform performansı
- Zaman bazında analiz

#### 🔥 8. %20+ Komisyon
- Yüksek komisyonlu ürünler
- Komisyon oranları
- Ürün detayları
- Potansiyel kazanç
- Sıralama ve filtreleme

#### 🛒 9. Satılan Ürünler
- trendurunlermarket satışları
- Satış tarihleri
- Komisyon tutarları
- Müşteri bilgileri
- Ödeme durumu

#### 💰 10. Komisyon Takibi
- 14 günlük takip
- Bekleyen komisyonlar
- Onaylanan komisyonlar
- Banka transfer durumu
- Ödeme takvimi

#### 💸 11. Günlük Komisyon
- Günlük yatan komisyonlar
- Banka hesap bilgileri
- IBAN doğrulaması
- Ödeme bildirimleri
- Tutar detayları

#### 🔄 12. 24 Saat Sıfırlama
- Veri temizleme zamanlayıcısı
- Otomatik sıfırlama ayarları
- Manuel sıfırlama butonu
- Yedekleme seçenekleri
- Veri koruma ayarları

### Gezinme ve Kullanım

#### 🖱️ Fare Kontrolleri
- **Sol Tık:** Seçim
- **Sağ Tık:** Menü
- **Tekerlek:** Kaydırma
- **Hover:** Detay göster

#### ⌨️ Klavye Kısayolları
- **Tab:** Sonraki panel
- **Shift+Tab:** Önceki panel
- **Ctrl+F:** Arama
- **Ctrl+R:** Yenile
- **Esc:** Menü kapat

#### 📱 Dokunmatik Kontroller
- **Dokun:** Seçim
- **Kaydır:** Panel değiştir
- **Çift Dokun:** Aç/Kapat
- **Yaklaştırma:** Parmak hareketi

### Veri Filtreleme ve Sıralama

#### 📅 Tarih Filtresi
```javascript
// Son 24 saat
const last24Hours = new Date(Date.now() - 24 * 60 * 60 * 1000);

// Son 7 gün
const last7Days = new Date(Date.now() - 7 * 24 * 60 * 60 * 1000);

// Son 30 gün
const last30Days = new Date(Date.now() - 30 * 24 * 60 * 60 * 1000);
```

#### 📊 Sıralama Seçenekleri
- **Tarih:** En yeni → En eski
- **Değer:** En yüksek → En düşük
- **İsim:** A → Z
- **Durum:** Aktif → Pasif

#### 🔍 Arama Özellikleri
- **Ürün adı:** İsim içeren
- **Platform:** Platform bazında
- **Durum:** Aktif/pasif
- **Tarih aralığı:** Başlangıç ve bitiş

---

## 🔄 PANEL ARASI GEÇİŞ

### Hızlı Geçiş Yöntemleri

#### 1. Panel Açıcı Kullanımı
```batch
# Tek tıkla tüm paneller
PANEL_ACICI.bat

# Menü tabanlı seçim
PANEL_KISA_YOL.bat

# Web arayüzü
PANEL_ACICI_HTML.html
```

#### 2. Manuel Geçiş
```html
<!-- Panel linkleri -->
<a href="http://localhost:9000">Ana Panel</a>
<a href="http://localhost:9001/status">Status API</a>
<a href="http://localhost:9002">Satış Alarmı</a>
<a href="http://localhost:9003">Gelişmiş Panel</a>
```

#### 3. Programatik Geçiş
```javascript
// Panel değiştirme fonksiyonu
function switchPanel(port) {
  window.open(`http://localhost:${port}`, '_blank');
}

// Kullanım
switchPanel(9000); // Ana Panel
switchPanel(9001); // Status API
switchPanel(9002); // Satış Alarmı
switchPanel(9003); // Gelişmiş Panel
```

### Panel Senkronizasyonu

#### 🔄 Otomatik Senkronizasyon
- 30 saniyede bir veri güncelleme
- Panel arası veri paylaşımı
- Gerçek zamanlı durum senkronizasyonu
- Hata durumunda otomatik yenileme

#### 📊 Veri Tutarlılığı
- Tüm paneller aynı veriyi gösterir
- Farklı zaman dilimlerinde tutarlılık
- Veri kaybı önleme
- Yedekleme ve geri yükleme

---

## 📱 MOBİL ERİŞİM

### Mobil Cihazlardan Erişim

#### 📲 Telefon Erişimi
```
📊 Ana Panel: http://192.168.1.100:9000
📈 Status API: http://192.168.1.100:9001/status
🚨 Satış Alarmı: http://192.168.1.100:9002
🌐 Gelişmiş Panel: http://192.168.1.100:9003
```

#### 📋 Tablet Erişimi
- Daha büyük ekran için optimize edilmiş
- Yatay ve dikey mod desteği
- Dokunmatik kontroller
- Sadeleştirilmiş arayüz

### Mobil Özellikler

#### 📱 Responsive Tasarım
- Ekran boyutuna göre otomatik ayarlama
- Dokunmatik butonlar
- Kaydırma ve zoom desteği
- Hızlı yükleme

#### 🔄 Mobil Optimizasyon
- Düşük veri kullanımı
- Hızlı yanıt süreleri
- Basitleştirilmiş arayüz
- Önemli bilgilere odaklanma

#### 📊 Mobil Veri Gösterimi
- Özet bilgiler
- Grafiksel gösterim
- Renk kodlu durumlar
- Hızlı erişim butonları

---

## 📈 VERİ ANALİZİ VE RAPORLAMA

### Gerçek Zamanlı Analiz

#### 📊 Performans Metrikleri
- **CPU Kullanımı:** Anlık CPU kullanımı
- **Bellek Kullanımı:** RAM kullanım oranı
- **Ağ Hızı:** Veri aktarım hızı
- **Disk I/O:** Okuma/yazma hızı
- **Response Time:** Yanıt süreleri

#### 📈 Trend Analizi
- **Saatlik:** Son 24 saat
- **Günlük:** Son 7 gün
- **Haftalık:** Son 4 hafta
- **Aylık:** Son 12 ay

#### 🎯 Hedef Takibi
- **Satış Hedefleri:** Günlük/haftalık/aylık
- **Komisyon Hedefleri:** Kazanç hedefleri
- **Performans Hedefleri:** Sistem performansı
- **Kullanım Hedefleri:** Panel kullanım oranı

### Raporlama Özellikleri

#### 📄 Rapor Türleri
- **Özet Rapor:** Ana metrikler
- **Detaylı Rapor:** Tüm veriler
- **Trend Raporu:** Zaman bazında analiz
- **Karşılaştırma Raporu:** Dönem karşılaştırması

#### 📊 Rapor Formatları
- **PDF:** Yazdırma ve paylaşım
- **Excel:** Veri analizi
- **JSON:** Programatik kullanım
- **CSV:** Veri içe/dışa aktarma

#### 📧 Rapor Dağıtımı
- **E-posta:** Otomatik gönderim
- **Telegram/Discord/Viber:** Bildirim gönderimi
- **Telegram:** Grup paylaşımı
- **Web:** İndirme linki

---

## ⚡ PERFORMANS OPTİMİZASYONU

### Panel Performansı

#### 🚀 Yükleme Optimizasyonu
- **Önbellekleme:** Veri önbellekleme
- **Lazy Loading:** Gerektiğinde yükleme
- **Minifikasyon:** CSS/JS optimizasyonu
- **CDN:** Hızlı içerik dağıtımı

#### 📊 Veri Optimizasyonu
- **Sayfalama:** Büyük veri setleri
- **Filtreleme:** Gerekli veri gösterimi
- **İndeksleme:** Hızlı arama
- **Sıkıştırma:** Veri boyutu düşürme

#### 🔄 Güncelleme Stratejisi
- **WebSocket:** Gerçek zamanlı güncelleme
- **Polling:** Düzenli kontrol
- **Event-Driven:** Olay tabanlı güncelleme
- **Batch Processing:** Toplu işlemler

### Sistem Performansı

#### 💾 Bellek Yönetimi
- **Garbage Collection:** Otomatik temizleme
- **Memory Pool:** Bellek havuzu
- **Cache Management:** Önbellek yönetimi
- **Leak Detection:** Bellek sızıntısı kontrolü

#### ⚡ İşlem Optimizasyonu
- **Async Processing:** Asenkron işlemler
- **Thread Pool:** İş parçacığı havuzu
- **Queue Management:** Kuyruk yönetimi
- **Load Balancing:** Yük dengeleme

---

## 🔧 SORUN GİNDERME

### Yaygın Sorunlar

#### 🚫 Panel Erişimi Sorunu
**Sorun:** Paneller açılmıyor

**Çözüm:**
1. Sistemi başlatın: `MASTER_BASLATICI.bat`
2. Portları kontrol edin: `netstat -an | findstr ":900"`
3. Firewall'ı kontrol edin
4. Antivirüsü geçici devre dışı bırakın
5. Sistemi yeniden başlatın

#### 🐌 Yavaş Yükleme
**Sorun:** Paneller yavaş açılıyor

**Çözüm:**
1. Tarayıcı önbelleğini temizleyin
2. Gereksiz sekmeleri kapatın
3. İnternet bağlantısını kontrol edin
4. Sistem kaynaklarını kontrol edin
5. Tarayıcıyı güncelleyin

#### 📊 Veri Gösterimi Sorunu
**Sorun:** Veriler güncellenmiyor

**Çözüm:**
1. Manuel yenileme yapın (F5)
2. API durumunu kontrol edin
3. Log dosyalarını kontrol edin
4. Sistemi yeniden başlatın
5. Veri tabanını kontrol edin

#### 🔄 Otomatik Yenileme Sorunu
**Sorun:** Otomatik yenileme çalışmıyor

**Çözüm:**
1. JavaScript'i kontrol edin
2. Tarayıcı konsolunu kontrol edin
3. Ağ bağlantısını test edin
4. CORS ayarlarını kontrol edin
5. Tarayıcıyı yeniden başlatın

### Hata Ayıklama

#### 🔍 Log Analizi
```bash
# Sistem loglarını kontrol et
tail -f logs/system_manager.log

# Hata loglarını filtrele
grep "ERROR" logs/*.log

# Son 100 satırı göster
tail -n 100 logs/system_manager.log
```

#### 🌐 Ağ Testleri
```bash
# Port kontrolü
telnet localhost 9000

# Bağlantı testi
curl -I http://localhost:9000

# Yanıt süresi ölçümü
time curl http://localhost:9000
```

#### 📊 Performans Testleri
```javascript
// Panel yükleme süresi
console.time('panelLoad');
window.addEventListener('load', () => {
  console.timeEnd('panelLoad');
});

// API yanıt süresi
const startTime = performance.now();
fetch('/status')
  .then(() => {
    const endTime = performance.now();
    console.log(`API yanıt süresi: ${endTime - startTime}ms`);
  });
```

### Destek ve Yardım

#### 📞 Hata Bildirimi
Hata bildirimi için şu bilgileri ekleyin:
- İşletim sistemi ve sürümü
- Tarayıcı ve sürümü
- Hata mesajı
- Zaman damgası
- Ekran görüntüsü

#### 📧 Destek Kanalları
- **E-posta:** support@trmnirvana.com
- **Telegram:** @trm_nirvana_support
- **Telegram/Discord/Viber:** +90 542 623 5116
- **Web:** https://trmnirvana.com/support

---

## 📋 HIZLI BAŞLANGIÇ KONTROL LİSTESİ

### Kurulum Sonrası Kontrol
- [ ] Paneller erişilebilir durumda
- [ ] Tüm portlar açık
- [ ] Veriler güncelleniyor
- [ ] Otomatik yenileme çalışıyor
- [ ] Mobil erişim mümkün
- [ ] API yanıtları doğru
- [ ] Log dosyaları oluşturuluyor
- [ ] Bildirimler geliyor

### Günlük Kontrol
- [ ] Ana panel çalışıyor
- [ ] Status API yanıt veriyor
- [ ] Satış alarmı aktif
- [ ] Gelişmiş panel açılıyor
- [ ] Veriler senkronize
- [ ] Hata yok
- [ ] Performans iyi
- [ ] Mobil uyumlu

### Performans Kontrolü
- [ ] Panel yükleme < 3 saniye
- [ ] API yanıt süresi < 1 saniye
- [ ] Veri güncelleme < 30 saniye
- [ ] Bellek kullanımı < 70%
- [ ] CPU kullanımı < 50%
- [ ] Ağ bağlantısı stabil

---

**TRM FULL OTOMASYON SİSTEMİ v3.0 - Panel Gözlemleme ve Kullanım Kılavuzu**

*Bu kılavuz ile tüm panelleri etkili bir şekilde kullanabilir ve sistem performansını optimize edebilirsiniz.*
