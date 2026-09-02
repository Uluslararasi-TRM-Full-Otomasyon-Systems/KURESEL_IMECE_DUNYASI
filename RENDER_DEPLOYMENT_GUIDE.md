# Render Free Tier Deployment Guide
## TRM Nirvana v3.0 - Tamamen Ücretsiz Deploy

Bu rehber, TRM Nirvana projesini Render'ın ücretsiz katmanına (free tier) deploy etmek için gereken tüm adımları içerir.

---

## 📋 Ön Hazırlık

### Gerekli Dosyalar
Projede şu yapılandırma dosyaları hazırlandı:
- ✅ `render.yaml` - Render konfigürasyonu
- ✅ `requirements.txt` - Optimize edilmiş Python bağımlılıkları
- ✅ `.streamlit/config.toml` - Streamlit ayarları
- ✅ `start.sh` - Başlatma scripti
- ✅ `app.py` - Ana Streamlit uygulaması

---

## 🚀 Adım 1: GitHub'a Push

Projenizi GitHub'a yükleyin:

```bash
git init
git add .
git commit -m "TRM Nirvana v3.0 - Render Free Tier Ready"
git branch -M main
git remote add origin https://github.com/KULLANICI_ADINIZ/proje-adiniz.git
git push -u origin main
```

---

## 🔧 Adım 2: Render Hesabı Oluşturma

1. [render.com](https://render.com) adresine gidin
2. "Sign Up" ile ücretsiz hesap oluşturun
3. GitHub hesabınızla bağlayın (GitHub OAuth)

---

## 📦 Adım 3: Render'da Web Service Oluşturma

### Manuel Yöntem (Önerilen)

1. Render Dashboard'da **"New +"** butonuna tıklayın
2. **"Web Service"** seçin
3. **GitHub repository'nizi seçin**
4. Aşağıdaki ayarları yapın:

#### Build & Deploy Ayarları:
- **Name**: `trm-nirvana` (veya istediğiniz isim)
- **Region**: Frankfurt (veya en yakın bölge)
- **Branch**: `main`
- **Runtime**: `Python`
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `streamlit run app.py --server.port=$PORT --server.address=0.0.0.0`

#### Environment Variables:
Aşağıdaki değişkenleri ekleyin:

| Key | Value |
|-----|-------|
| `PORT` | `8501` |
| `PYTHONUNBUFFERED` | `1` |
| `PYTHONDONTWRITEBYTECODE` | `1` |

5. **"Create Web Service"** butonuna tıklayın

---

## ⚙️ Alternatif: render.yaml ile Otomatik Deploy

Eğer `render.yaml` dosyası repo'da varsa:

1. Render Dashboard'da **"New +"** tıklayın
2. **"Blueprints"** seçin
3. GitHub repository'nizi seçin
4. Render, `render.yaml` dosyasını otomatik okuyacak
5. **"Apply Blueprint"** tıklayın

---

## 🎛️ Adım 4: Environment Variables (API Anahtarları)

Gerekirse API anahtarlarınızı ekleyin:

1. Web Service sayfasına gidin
2. **"Environment"** sekmesine tıklayın
3. API anahtarlarınızı ekleyin (örneğin):
   - `OPENAI_API_KEY`
   - `GROQ_API_KEY`
   - `GOOGLE_API_KEY`

⚠️ **Önemli**: Asla API anahtarlarını kod içine yazmayın!

---

## 📊 Adım 5: Deploy İzleme

1. **"Events"** sekmesinden build sürecini izleyin
2. İlk deploy 5-10 dakika sürebilir
3. Yeşil ✅ işareti görünürse deploy başarılı

---

## 🌐 Adım 6: Uygulamaya Erişim

Deploy tamamlandıktan sonra:
- Render size bir URL verecek: `https://trm-nirvana.onrender.com`
- Bu URL ile uygulamanıza erişebilirsiniz

---

## 🔍 Adım 7: Health Check

Uygulamanın çalıştığını doğrulayın:

1. Render Dashboard'da **"Logs"** sekmesine tıklayın
2. Hata mesajı olmadığını kontrol edin
3. URL'yi tarayıcınızda açın
4. Streamlit arayüzünün yüklendiğini görün

---

## 💰 Free Tier Limitleri

Render'ın ücretsiz katmanı şunları sağlar:

- **512 MB RAM**
- **0.1 CPU**
- **Sınırsız bant genişliği**
- **15 dakika inaktivite sonrası sleep**
- **Her istekte cold start (yaklaşık 30-60 saniye)**

---

## ⚠️ Önemli Notlar

### Sleep Modu
- Uygulama 15 dakika kullanılmadığında sleep moduna geçer
- İlk istek 30-60 saniye sürebilir (cold start)
- Bu normaldir, ücretsiz katmanın bir özelliğidir

### Memory Limit
- 512 MB RAM limiti var
- Ağır işlemler (örneğin 200 ajan çalıştırmak) free tier'de çalışmayabilir
- Streamlit UI için optimize edildi, arka plan işlemleri için ücretli katman gerekebilir

### Build Time
- İlk deploy 5-10 dakika sürebilir
- Sonraki deploys daha hızlı olacaktır

---

## 🛠️ Sorun Giderme

### Build Hataları
```bash
# Logs sekmesinden hatalı satırı bulun
# requirements.txt'de versiyon çakışmalarını kontrol edin
```

### Runtime Hataları
```bash
# Environment variables doğru ayarlanmış mı kontrol edin 
# API anahtarları eksik olabilir
```

### Uygulama Yüklenmiyor
```bash
# start.sh script'in çalıştığından emin olun
# PORT değişkeni 8501 olarak ayarlanmış mı kontrol edin
```

---

## 🔄 Güncelleme Yapma

Kod değişiklikleri sonrası:

```bash
git add .
git commit -m "Yeni özellik eklendi"
git push
```

Render otomatik olarak yeni deploy başlatacak.

---

## 📝 Alternatif: Streamlit Cloud

Eğer Render yerine Streamlit Cloud kullanmak isterseniz:

1. [share.streamlit.io](https://share.streamlit.io) adresine gidin
2. GitHub hesabınızla giriş yapın
3. **"New app"** tıklayın
4. Repository'nizi seçin
5. Main file: `app.py`
6. **"Deploy"** tıklayın

Streamlit Cloud da tamamen ücretsizdir ve Streamlit uygulamaları için optimize edilmiştir.

---

## ✅ Kontrol Listesi

Deploy öncesi kontrol edin:

- [ ] `render.yaml` dosyası repo'da mı?
- [ ] `requirements.txt` optimize edildi mi?
- [ ] `.streamlit/config.toml` ayarları doğru mu?
- [ ] `app.py` dosyası çalışıyor mu?
- [ ] GitHub repo public veya private?
- [ ] API anahtarları environment variables'da mı?

---

## 🎉 Başarılı Deploy!

Deploy tamamlandıktan sonra:
- Uygulamanız `https://trm-nirvana.onrender.com` adresinde çalışacak
- Her kod push'unda otomatik deploy olacak
- Tamamen ücretsiz!

---

## 📞 Destek

Sorun yaşarsanız:
- Render Logs sekmesini kontrol edin
- GitHub Issues açabilirsiniz
- Render documentation: [docs.render.com](https://docs.render.com)

---

**Son Güncelleme**: 2026-09-02
**Versiyon**: TRM Nirvana v3.0 - Render Free Tier
