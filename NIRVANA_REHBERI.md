# 🚀 TRM NIRVANA SİSTEMİ - KAPSAMLI REHBER

## 📋 İçindekiler

1. [Nirvana Sistemi Nedir?](#nirvana-sistemi-nedir)
2. [Kurulum ve Başlatma](#kurulum-ve-başlatma)
3. [Sağlık Kontrolü](#sağlık-kontrolü)
4. [Performans Optimizasyonu](#performans-optimizasyonu)
5. [Sorun Giderme](#sorun-giderme)
6. [İleri Düzey Ayarlar](#ileri-düzey-ayarlar)

---

## 🌟 Nirvana Sistemi Nedir?

TRM Nirvana Sistemi, mevcut TRM Full Otomasyon Sistemi'nin **maximum performans** seviyesine ulaşması için geliştirilmiş kapsamlı bir iyileştirme paketidir.

### Temel Özellikler

- ✅ **Otomatik Sağlık Kontrolü**: Sistem kaynaklarını, API bağlantılarını ve bağımlılıkları otomatik kontrol eder
- ✅ **Akıllı Başlatma**: Sistem durumuna göre en iyi başlatma stratejisini uygular
- ✅ **Performans Optimizasyonu**: Cache temizliği, log yönetimi ve kaynak optimizasyonu
- ✅ **Otomatik Kurtarma**: Çöken süreçleri otomatik olarak yeniden başlatır
- ✅ **Gerçek Zamanlı İzleme**: Sistem performansını sürekli izler ve raporlar

### Yeni Dosyalar

- `NIRVANA_HEALTH_MONITOR.py`: Kapsamlı sağlık kontrolü sistemi
- `NIRVANA_STARTER.py`: Akıllı başlatma sistemi
- `NIRVANA_BASLAT.bat`: Tek tıklama başlatma (Windows)
- `NIRVANA_REHBERI.md`: Bu rehber dosyası

---

## 🚀 Kurulum ve Başlatma

### 1. Gereksinimler

- Python 3.8 veya üzeri
- Windows 10/11 veya Linux/Mac
- İnternet bağlantısı
- 4GB+ RAM (önerilen: 8GB)
- 10GB+ boş disk alanı

### 2. Kurulum

```bash
# 1. Bağımlılıkları yükle
pip install -r requirements.txt

# 2. secrets.env dosyasını yapılandır
# (API anahtarlarınızı girin)

# 3. Health monitor'ü test et
python NIRVANA_HEALTH_MONITOR.py
```

### 3. Başlatma

#### Windows (Önerilen)
```bash
# Çift tıklayarak başlatın
NIRVANA_BASLAT.bat
```

#### Manuel Başlatma
```bash
# Health kontrolü
python NIRVANA_HEALTH_MONITOR.py

# Nirvana starter ile başlat
python NIRVANA_STARTER.py

# Veya klasik başlatma
python run.py
```

---

## 🏥 Sağlık Kontrolü

### Tam Sağlık Kontrolü

```bash
python NIRVANA_HEALTH_MONITOR.py
```

Bu komut şunları kontrol eder:

- **Sistem Kaynakları**: CPU, RAM, Disk kullanımı
- **Disk Alanı**: Kritik dizinlerdeki boş alan
- **Python Bağımlılıkları**: Gerekli paketlerin varlığı
- **API Bağlantıları**: Google, OpenAI, Telegram, Trendyol
- **Veritabanı Sağlığı**: DB dosyalarının boyutu ve durumu
- **Log Dosyaları**: Log boyutları ve temizlik ihtiyacı
- **Cache Temizliği**: Otomatik cache temizliği
- **Performans Optimizasyonu**: Sistem optimizasyonu

### Sağlık Raporu

Sonuçlar `nirvana_health_report.json` dosyasına kaydedilir ve konsola yazdırılır.

**Örnek Çıktı:**
```
📊 PERFORMANS METRİKLERİ:
  ✅ CPU: {'percent': 25, 'status': 'healthy'}
  ✅ MEMORY: {'percent': 45, 'status': 'healthy'}
  ✅ DISK: {'percent': 60, 'status': 'healthy'}
```

---

## ⚡ Performans Optimizasyonu

### Otomatik Optimizasyonlar

Nirvana sistemi şu optimizasyonları otomatik yapar:

1. **Cache Temizliği**: `__pycache__`, temp dosyalarını temizler
2. **Log Döndürme**: Büyük log dosyalarını otomatik döndürür
3. **Python Cache Temizliği**: `.pyc` dosyalarını temizler
4. **Küçük JSON Temizliği**: Boş veya çok küçük JSON dosyalarını siler

### Manuel Optimizasyon

```python
# Python ile
from NIRVANA_HEALTH_MONITOR import NirvanaHealthMonitor
import asyncio

monitor = NirvanaHealthMonitor()
asyncio.run(monitor.clean_cache())
asyncio.run(monitor.optimize_performance())
```

---

## 🔧 Sorun Giderme

### Yaygın Sorunlar

#### 1. Python Bulunamadı
**Çözüm:** Python 3.8+ yükleyin ve PATH'e ekleyin

#### 2. Bağımlılık Eksik
**Çözüm:** 
```bash
pip install -r requirements.txt
```

#### 3. secrets.env Eksik
**Çözüm:** `secrets.env` dosyasını oluşturun ve API anahtarlarınızı girin

#### 4. API Bağlantı Hatası
**Çözüm:** 
- İnternet bağlantınızı kontrol edin
- API anahtarlarınızın geçerli olduğunu doğrulayın
- Firewall ayarlarını kontrol edin

#### 5. CPU/RAM Yüksek Kullanım
**Çözüm:**
```bash
# Health kontrolü çalıştırın
python NIRVANA_HEALTH_MONITOR.py

# Önerileri uygulayın
```

### Log Dosyaları

- `nirvana_health.log`: Sağlık kontrolü logları
- `nirvana_starter.log`: Başlatma sistemi logları
- `nirvana_health_report.json`: Son sağlık raporu

---

## 🎯 İleri Düzey Ayarlar

### Sürekli İzleme

Nirvana starter sistemi sürekli izleme modunda çalışır:

- **5 dakikada bir**: Sağlık kontrolü
- **1 dakikada bir**: Süreç izleme
- **Otomatik**: Çöken süreçleri yeniden başlatma

### Özel Yapılandırma

`secrets.env` dosyasına ekleyebileceğiniz özel ayarlar:

```bash
# Sistem ayarları
DEBUG_MODE=false
LOG_LEVEL=INFO
MAX_RETRIES=3
API_RATE_LIMIT=100
REQUEST_TIMEOUT=30

# Performans ayarları
MAX_CONCURRENT_TASKS=10
CACHE_DURATION_MINUTES=30
AUTO_RESTART_ENABLED=true
HEALTH_CHECK_INTERVAL_MINUTES=15
```

### Manuel Süreç Yönetimi

```python
# Python ile süreç yönetimi
from NIRVANA_STARTER import NirvanaStarter
import asyncio

starter = NirvanaStarter()

# Sistemi başlat
await starter.run()

# Sistemi durdur
await starter.shutdown()
```

---

## 📊 Performans Kriterleri

### İdeal Değerler

| Metrik | İdeal | Uyarı | Kritik |
|--------|-------|-------|--------|
| CPU | < 50% | 50-70% | > 90% |
| RAM | < 60% | 60-80% | > 90% |
| Disk | < 70% | 70-85% | > 90% |

### Hedefler

- ✅ Sistem sürekli çalışma (24/7)
- ✅ Otomatik hata kurtarma
- ✅ Minimum manuel müdahale
- ✅ Maksimum performans

---

## 🔄 Güncellemeler

### Sistemi Güncelleme

```bash
# 1. Mevcut sistemi yedekle
python -c "import shutil; shutil.copytree('Uluslararasi-TRM-Full-Otomasyon-Sistemi', 'backup')"

# 2. Yeni dosyaları indirin ve değiştirin

# 3. Bağımlılıkları güncelleyin
pip install -r requirements.txt --upgrade

# 4. Health kontrolü çalıştırın
python NIRVANA_HEALTH_MONITOR.py

# 5. Sistemi yeniden başlatın
python NIRVANA_STARTER.py
```

---

## 📞 Destek

### Sorun Bildirimi

Sorun yaşarsanız:
1. `nirvana_health_report.json` dosyasını kontrol edin
2. Log dosyalarını inceleyin
3. Health kontrolü çıktısını kaydedin

### Faydalı Komutlar

```bash
# Sistem durumu
python NIRVANA_HEALTH_MONITOR.py

# Bağımlılık kontrolü
pip list

# Python versiyonu
python --version

# Disk kullanımı
dir (Windows)
df -h (Linux/Mac)
```

---

## 🎉 Başarıyla Kurulum!

Tebrikler! TRM Nirvana Sistemi'niz maximum performans seviyesine ulaştı.

**Sonraki Adımlar:**
1. ✅ Health kontrolünü düzenli çalıştırın
2. ✅ Log dosyalarını izleyin
3. ✅ Performans metriklerini takip edin
4. ✅ Gerekirse optimizasyon yapın

**İyi çalışmalar! 🚀**
