# 🚀 Uluslararası TRM Full Otomasyon Sistemi v4.0 NIRVANA

Telegram, Web Scraping, AI, Sosyal Medya entegrasyonu ile %20+ komisyonlu trend ürün otomasyonu.
**Nirvana Edition** - Maximum performans ve otomatik optimizasyon sistemi.

## ⚡ Hızlı Başlangıç (Nirvana Modu)

```bash
# ÖNERİLEN: Nirvana sistemi ile başlatın (Windows)
NIRVANA_BASLAT.bat

# Veya manuel başlatma
python NIRVANA_STARTER.py
```

## 🌟 Nirvana Özellikleri

- ✅ **Otomatik Sağlık Kontrolü**: CPU, RAM, Disk, API bağlantıları
- ✅ **Akıllı Başlatma**: Sistem durumuna göre optimizasyon
- ✅ **Performans Optimizasyonu**: Cache temizliği, log yönetimi
- ✅ **Otomatik Kurtarma**: Çöken süreçleri yeniden başlatır
- ✅ **Gerçek Zamanlı İzleme**: Sürekli performans takibi

Detaylı bilgi için: `NIRVANA_REHBERI.md`

## ⚡ Klasik Başlangıç

```bash
# 1. Bağımlılıkları kur
pip install -r requirements.txt

# 2. API anahtarlarını düzenle (önemli!)
# secrets.env dosyasını aç ve kendi anahtarlarını koy
# Detaylı rehber: API_ANAHTARLARI_REHBERI.md

# 3. Konfigürasyonu kontrol et
python run.py status

# 4. Tüm modülleri test et
python run.py test

# 5. Tüm sistemi başlat
python run.py
```

## 📖 Dokümanlar

| Dosya | Açıklama |
|---|---|
| `NIRVANA_REHBERI.md` | **YENİ** Nirvana sistemi kapsamlı rehberi |
| `API_ANAHTARLARI_REHBERI.md` | Her API'yi nereden alıp nasıl bağlayacağınız |
| `TRM_FULL_KURULUM_ISLETIM_REHBERI.md` | Orijinal kapsamlı kılavuz |
| `SISTEM_BAKIM_KILAVUZU.md` | Bakım & sorun giderme |

## 🎯 Çalıştırma Modları

```bash
python run.py           # Tüm sistem (orchestrator)
python run.py status    # Config kontrol
python run.py test      # Tüm modülleri test et
python run.py telegram  # Sadece Telegram dinleyici
python run.py scraper   # Sadece web scraper
python run.py ai        # Sadece AI testi
python run.py social    # Sadece sosyal medya testi
```

**Windows:** `NIRVANA_BASLAT.bat` (önerilen) veya `SISTEM_BASLAT.bat`
**Linux/Mac:** `./sistem_baslat.sh`

## 🔒 Güvenlik

- `secrets.env` ve `credentials.json` dosyalarını **ASLA paylaşmayın**
- `.gitignore` zaten bunları koruyor
- API anahtarlarınızı yenilemek için `API_ANAHTARLARI_REHBERI.md`'ye bakın

## 🧪 Test

```bash
pip install pytest pytest-asyncio
pytest test_trm.py -v
```
