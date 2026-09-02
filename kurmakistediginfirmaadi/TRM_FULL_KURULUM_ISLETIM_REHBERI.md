# TRM FULL OTOMASYON SİSTEMİ - KURULUM VE İŞLETİM REHBERİ

## 📋 İÇERİK TABLOSU

**BÖLÜM 1: TRM FULL OTOMASYON SİSTEMİ KURULUM YOL HARİTASI**
1. [Kurulum Modülleri](#kurulum-modülleri)
2. [Kurulum Adımları](#kurulum-adımları)
3. [Teknik Gereksinimler](#teknik-gereksinimler)

**BÖLÜM 2: TRM FULL OTOMASYON SİSTEMİNİN ÇALIŞMASI**
1. [Sistemin Çalışma Döngüsü](#sistemin-çalışma-döngüsü)
2. [Aktif Görevler](#aktif-görevler)
3. [İşletim Prosedürleri](#işletim-prosedürleri)

**BÖLÜM 3: DİĞER FİRMALARA ADAPTE ETME**
1. [Modüler Ekleme Yöntemi](#modüler-ekleme-yöntemi)
2. [Sistem Kopyalama Yöntemi](#sistem-kopyalama-yöntemi)
3. [Firma Ekleme Kontrol Listesi](#firma-ekleme-kontrol-listesi)

**BÖLÜM 4: TEKNİK ÖZELLİKLER VE GEREKSİNİMLER**
1. [Minimum Sistem Gereksinimleri](#minimum-sistem-gereksinimleri)
2. [Güvenlik Önlemleri](#güvenlik-önlemleri)
3. [Performans Optimizasyonu](#performans-optimizasyonu)

---

## BÖLÜM 1: TRM FULL OTOMASYON SİSTEMİ KURULUM YOL HARİTASI

### KURULUM MODÜLLERİ

#### Modül 1: Bulut Sunucu Modülü (Railway/Render)
**Dosyalar:** `Dockerfile`, `main.py`
**Fonksiyon:** Sistemin 7/24 kesintisiz çalışmasını sağlayan motor katmanı
**Özellik:** Bilgisayar kapalı olsa bile işlemler devam eder
**Kurulum:** Railway veya Render platformuna Docker container olarak deploy edilir

**Dockerfile Örneği:**
```dockerfile
FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["python", "main.py"]
```

**main.py Örneği:**
```python
from flask import Flask, jsonify
import threading
import time

app = Flask(__name__)

@app.route('/health')
def health_check():
    return jsonify({'status': 'running', 'uptime': time.time()})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
```

#### Modül 2: Veri Yakalama / Dinleyici Modülü
**Dosyalar:** `telegram_listener.py`, `web_scraper.py`
**Fonksiyon:** 
- Telegram kanallarını anlık tarar
- magazanolsun.com sitesini izler
- Rakip sosyal medya hesaplarını takip eder
**Özellik:** TOP 20 listesindeki başarılı mağazaların son 3 yıllık verilerini analiz eden "ajan bot" teknolojisi

**telegram_listener.py Örneği:**
```python
import telethon
from telethon.sync import TelegramClient

class TelegramListener:
    def __init__(self, api_id, api_hash, phone):
        self.client = TelegramClient('session_name', api_id, api_hash)
        self.phone = phone
    
    async def listen_channels(self):
        await self.client.start(self.phone)
        
        # Kanalları dinle
        async for message in self.client.iter_messages('target_channel'):
            await self.process_message(message)
    
    async def process_message(self, message):
        # Ürün bilgisini çıkar ve işle
        if self.is_product_post(message):
            product_data = self.extract_product_info(message)
            await self.send_to_ai(product_data)

    def is_product_post(self, message):
        # Ürün paylaşımı olup olmadığını kontrol et
        keywords = ['yeni ürün', 'indirim', 'kampanya', 'fırsat']
        return any(keyword in message.text.lower() for keyword in keywords)
```

#### Modül 3: Veri Deposu Modülü (Google Drive)
**Klasörler:**
- `TRM_Arsiv` (tüm ürün görselleri ve videoları)
- `TRM_Raporlar` (satış raporları)
- `TRM_Medya` (AI çıktıları)
**Fonksiyon:** Tüm verilerin toplandığı hafıza merkezi

**Google Drive Entegrasyonu:**
```python
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials

class GoogleDriveManager:
    def __init__(self, credentials_file):
        self.creds = Credentials.from_authorized_user_file(credentials_file)
        self.service = build('drive', 'v3', credentials=self.creds)
    
    def create_folder_structure(self):
        folders = {
            'TRM_Arsiv': 'Tüm ürün görselleri ve videoları',
            'TRM_Raporlar': 'Satış raporları',
            'TRM_Medya': 'AI çıktıları'
        }
        
        for folder_name, description in folders.items():
            folder_metadata = {
                'name': folder_name,
                'mimeType': 'application/vnd.google-apps.folder',
                'description': description
            }
            self.service.files().create(body=folder_metadata, fields='id').execute()
    
    def upload_file(self, file_path, folder_id):
        file_metadata = {
            'name': os.path.basename(file_path),
            'parents': [folder_id]
        }
        
        media = MediaFileUpload(file_path, resumable=True)
        self.service.files().create(
            body=file_metadata,
            media_body=media,
            fields='id'
        ).execute()
```

#### Modül 4: n8n Otomasyon Zinciri (Orkestra Şefi)
**Dosya:** `workflow.json`
**Fonksiyon:** 
- Modüller arası köprü görevi
- Telegram'dan gelen veriyi AI'ya gönderir
- Onay mekanizmasını işletir
- Dağıtımı yönetir

**workflow.json Örneği:**
```json
{
  "name": "TRM Otomasyon Akışı",
  "nodes": [
    {
      "name": "Telegram Listener",
      "type": "webhook",
      "webhook": "telegram_webhook"
    },
    {
      "name": "AI Processing",
      "type": "function",
      "function": "process_with_ai",
      "parameters": {
        "deepseek_key": "{{DEEPSEEK_API_KEY}}",
        "claude_key": "{{CLAUDE_API_KEY}}"
      }
    },
    {
      "name": "Content Generation",
      "type": "function",
      "function": "generate_content"
    },
    {
      "name": "Social Media Publisher",
      "type": "function",
      "function": "publish_to_social"
    }
  ],
  "connections": [
    {
      "source": "Telegram Listener",
      "target": "AI Processing"
    },
    {
      "source": "AI Processing",
      "target": "Content Generation"
    },
    {
      "source": "Content Generation",
      "target": "Social Media Publisher"
    }
  ]
}
```

#### Modül 5: AI Analiz Modülü (DeepSeek & Claude)
**Entegrasyon:** API entegrasyonu
- **DeepSeek:** Görsel/video analizi ve hedef kitle belirleme
- **Claude:** Satış odaklı, SEO uyumlu başlık/açıklama metinleri üretme

**AI Entegrasyon Örneği:**
```python
import openai
from deepseek import DeepSeekClient

class AIProcessor:
    def __init__(self, deepseek_key, claude_key):
        self.deepseek_client = DeepSeekClient(api_key=deepseek_key)
        self.claude_client = openai.OpenAI(api_key=claude_key)
    
    async def analyze_with_deepseek(self, image_url):
        """Görsel/video analizi ve hedef kitle belirleme"""
        response = await self.deepseek_client.analyze_image(image_url)
        return {
            'target_audience': response.audience,
            'product_features': response.features,
            'recommended_tags': response.tags
        }
    
    async def generate_with_claude(self, product_info, analysis):
        """Satış odaklı, SEO uyumlu metin üretme"""
        prompt = f"""
        Ürün: {product_info['name']}
        Analiz: {analysis}
        
        SEO uyumlu, satış odaklı başlık ve açıklama metni üret.
        Hedef kitle: {analysis['target_audience']}
        Özellikler: {analysis['product_features']}
        """
        
        response = await self.claude_client.messages.create(
            model="claude-3-sonnet-20240229",
            max_tokens=1000,
            messages=[{"role": "user", "content": prompt}]
        )
        
        return {
            'title': response.content[0].text.split('\n')[0],
            'description': response.content[0].text.split('\n')[1],
            'tags': analysis['recommended_tags']
        }
```

#### Modül 6: Paylaşım ve Dağıtım Modülü
**Dosya:** `social_publisher.py`
**Platformlar:** Facebook, Instagram, TikTok, YouTube ve 4 farklı blog sitesi (Blogger, WordPress vb.)
**Özellik:** Otomatik içerik gönderir, görsellere mağaza linki ve logo ekler

**Social Publisher Örneği:**
```python
import facebook
import instagrapi
from tiktok_uploader import TikTokUploader

class SocialPublisher:
    def __init__(self):
        self.facebook_client = facebook.GraphAPI(access_token=FACEBOOK_TOKEN)
        self.instagram_client = instagrapi.InstagramAPI()
        self.tiktok_uploader = TikTokUploader()
    
    async def publish_to_all_platforms(self, content, image_path, store_link):
        """Tüm platformlara otomatik paylaşım"""
        
        # Görseli işle (logo ve mağaza linki ekle)
        processed_image = self.add_store_logo_and_link(image_path, store_link)
        
        # Platformlara gönder
        tasks = [
            self.publish_to_facebook(content, processed_image),
            self.publish_to_instagram(content, processed_image),
            self.publish_to_tiktok(content, processed_image),
            self.publish_to_youtube(content, processed_image),
            self.publish_to_blogs(content, processed_image)
        ]
        
        results = await asyncio.gather(*tasks)
        return results
    
    def add_store_logo_and_link(self, image_path, store_link):
        """Görsel üzerine mağaza linki ve logo ekle"""
        from PIL import Image, ImageDraw, ImageFont
        
        image = Image.open(image_path)
        draw = ImageDraw.Draw(image)
        
        # Logo ekle
        logo = Image.open('store_logo.png')
        image.paste(logo, (10, 10), logo)
        
        # Mağaza linki ekle
        font = ImageFont.truetype("arial.ttf", 20)
        draw.text((10, image.height - 30), store_link, fill="white", font=font)
        
        return image
```

#### Modül 7: Raporlama ve Kontrol Modülü
**Dosya:** `report_manager.py`
**Fonksiyon:** 
- Satışları takip eder
- Hata durumunda bildirim gönderir
- Her sabah saat 09:00'da Telegram üzerinden günlük performans raporu sunar

**Report Manager Örneği:**
```python
import asyncio
import schedule
from datetime import datetime

class ReportManager:
    def __init__(self, telegram_client):
        self.telegram_client = telegram_client
        self.sales_data = []
        self.error_count = 0
    
    async def track_sales(self, sale_data):
        """Satışları takip et"""
        self.sales_data.append({
            'timestamp': datetime.now(),
            'product_id': sale_data['product_id'],
            'amount': sale_data['amount'],
            'commission': sale_data['commission']
        })
    
    async def send_daily_report(self):
        """Günlük performans raporu gönder"""
        today_sales = [s for s in self.sales_data 
                        if s['timestamp'].date() == datetime.now().date()]
        
        total_sales = len(today_sales)
        total_commission = sum(s['commission'] for s in today_sales)
        
        report = f"""
📊 GÜNLÜK PERFORMANS RAPORU
📅 Tarih: {datetime.now().strftime('%d.%m.%Y')}
💰 Toplam Satış: {total_sales}
💸 Toplam Komisyon: {total_commission:.2f} TL
🔧 Hata Sayısı: {self.error_count}
📈 Başarı Oranı: {self.calculate_success_rate():.1f}%
        """
        
        await self.telegram_client.send_message('admin_channel', report)
    
    def setup_scheduled_reports(self):
        """Planlı raporları ayarla"""
        schedule.every().day.at("09:00").do(self.send_daily_report)
        
        while True:
            schedule.run_pending()
            asyncio.sleep(60)
```

### KURULUM ADIMLARI

#### Adım 1: Bulut Sunucu Hesabı Oluşturma (Railway/Render)
**Railway Kurulumu:**
1. [Railway](https://railway.app) sitesine gidin
2. Hesap oluşturun veya giriş yapın
3. "New Project" butonuna tıklayın
4. "Deploy from GitHub" seçin
5. Repository'nizi bağlayın veya yeni oluşturun
6. Dockerfile ve main.py dosyalarınızın olduğundan emin olun
7. "Deploy" butonuna tıklayın
8. Deployment tamamlandığında URL'i kopyalayın

**Render Kurulumu:**
1. [Render](https://render.com) sitesine gidin
2. "New" -> "Web Service" seçin
3. GitHub repository'nizi bağlayın
4. Build komutunu belirleyin: `pip install -r requirements.txt && python main.py`
5. Port'u belirleyin: 8000
6. "Create Web Service" butonuna tıklayın
7. Deployment URL'ini kopyalayın

#### Adım 2: Docker Container'ı Deploy Etme
**Dockerfile Oluşturma:**
```dockerfile
# Python 3.10 tabanlı image
FROM python:3.10-slim

# Çalışma dizini ayarla
WORKDIR /app

# Gerekli paketleri kopyala ve yükle
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Uygulama kodunu kopyala
COPY . .

# Port'u belirle
EXPOSE 8000

# Başlangıç komutunu belirle
CMD ["python", "main.py"]
```

**requirements.txt:**
```txt
flask==2.3.3
telethon==1.28.5
requests==2.31.0
google-api-python-client==2.100.0
google-auth-httplib2==0.1.1
google-auth-oauthlib==1.0.0
openai==1.3.5
deepseek-api==1.0.0
schedule==1.2.0
Pillow==10.0.1
beautifulsoup4==4.12.2
selenium==4.15.2
```

#### Adım 3: Google Drive API Entegrasyonu ve Klasör Yapısı Oluşturma
**Google Cloud Console Ayarları:**
1. [Google Cloud Console](https://console.cloud.google.com) gidin
2. Yeni proje oluşturun
3. "APIs & Services" -> "Library" gidin
4. "Google Drive API" arayın ve etkinleştirin
5. "OAuth consent screen" ayarlarını yapın
6. "Credentials" -> "Create Credentials" -> "OAuth 2.0 Client ID" oluşturun
7. JSON dosyasını indirin ve `credentials.json` olarak kaydedin

**Klasör Yapısı Oluşturma:**
```python
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials

def setup_drive_structure():
    """Google Drive klasör yapısını oluştur"""
    
    folders = {
        'TRM_Arsiv': {
            'description': 'Tüm ürün görselleri ve videoları',
            'subfolders': ['Gorseller', 'Videolar', 'Logolar']
        },
        'TRM_Raporlar': {
            'description': 'Satış raporları',
            'subfolders': ['Gunluk', 'Haftalik', 'Aylik']
        },
        'TRM_Medya': {
            'description': 'AI çıktıları',
            'subfolders': ['AI_Gorseller', 'AI_Videolar', 'AI_Metinler']
        }
    }
    
    service = build('drive', 'v3', credentials=creds)
    
    for folder_name, details in folders.items():
        # Ana klasörü oluştur
        folder_metadata = {
            'name': folder_name,
            'mimeType': 'application/vnd.google-apps.folder',
            'description': details['description']
        }
        
        folder = service.files().create(body=folder_metadata, fields='id').execute()
        folder_id = folder.get('id')
        
        # Alt klasörleri oluştur
        for subfolder in details['subfolders']:
            subfolder_metadata = {
                'name': subfolder,
                'mimeType': 'application/vnd.google-apps.folder',
                'parents': [folder_id]
            }
            
            service.files().create(body=subfolder_metadata).execute()
        
        print(f"✅ {folder_name} klasörü oluşturuldu")
```

#### Adım 4: n8n Workflow Kurulumu ve Yapılandırma
**n8n Kurulumu:**
1. [n8n.io](https://n8n.io) sitesine gidin
2. Hesap oluşturun
3. "Workflows" -> "Create new workflow" seçin
4. Aşağıdaki workflow'u import edin:

**Workflow JSON:**
```json
{
  "name": "TRM Otomasyon Akışı",
  "nodes": [
    {
      "parameters": {},
      "id": "telegram-webhook",
      "name": "Telegram Webhook",
      "type": "n8n-nodes-base.webhook",
      "typeVersion": 1,
      "position": [240, 300],
      "webhookId": "telegram-webhook"
    },
    {
      "parameters": {
        "deepseek_key": "={{DEEPSEEK_API_KEY}}",
        "claude_key": "={{CLAUDE_API_KEY}}"
      },
      "id": "ai-processing",
      "name": "AI Processing",
      "type": "n8n-nodes-base.function",
      "typeVersion": 1,
      "position": [460, 300]
    },
    {
      "parameters": {},
      "id": "content-generation",
      "name": "Content Generation",
      "type": "n8n-nodes-base.function",
      "typeVersion": 1,
      "position": [680, 300]
    },
    {
      "parameters": {},
      "id": "social-publisher",
      "name": "Social Publisher",
      "type": "n8n-nodes-base.function",
      "typeVersion": 1,
      "position": [900, 300]
    }
  ],
  "connections": {
    "Telegram Webhook": {
      "main": [["AI Processing"]]
    },
    "AI Processing": {
      "main": [["Content Generation"]]
    },
    "Content Generation": {
      "main": [["Social Publisher"]]
    }
  }
}
```

#### Adım 5: AI API Anahtarları (DeepSeek & Claude) Entegrasyonu
**DeepSeek API Anahtarı:**
1. [DeepSeek Platform](https://platform.deepseek.com) gidin
2. Hesap oluşturun
3. API Keys bölümünden yeni anahtar oluşturun
4. Anahtarı kopyalayın ve güvenli bir yere kaydedin

**Claude API Anahtarı:**
1. [Anthropic Console](https://console.anthropic.com) gidin
2. Hesap oluşturun
3. API Keys bölümünden yeni anahtar oluşturun
4. Anahtarı kopyalayın ve güvenli bir yere kaydedin

**Entegrasyon Kodu:**
```python
# .env dosyası
DEEPSEEK_API_KEY=sk-deepseek-xxxxxxxxxxxxxxxxx
CLAUDE_API_KEY=sk-ant-xxxxxxxxxxxxxxxxx

# Python kodu
import os
from deepseek import DeepSeekClient
import openai

# DeepSeek client
deepseek_client = DeepSeekClient(api_key=os.getenv('DEEPSEEK_API_KEY'))

# Claude client
claude_client = openai.OpenAI(api_key=os.getenv('CLAUDE_API_KEY'))
```

#### Adım 6: Telegram Bot API Anahtarı Alma ve Listener Kurulumu
**Telegram Bot Oluşturma:**
1. [@BotFather](https://t.me/BotFather) ile konuşun
2. `/newbot` komutunu gönderin
3. Bot adını ve kullanıcı adını belirleyin
4. Bot token'ını kopyalayın

**Listener Kurulumu:**
```python
import asyncio
from telethon.sync import TelegramClient

class TRMTelegramListener:
    def __init__(self):
        self.api_id = int(os.getenv('TELEGRAM_API_ID'))
        self.api_hash = os.getenv('TELEGRAM_API_HASH')
        self.phone = os.getenv('TELEGRAM_PHONE')
        self.client = TelegramClient('trm_session', self.api_id, self.api_hash)
    
    async def start(self):
        await self.client.start(self.phone)
        print("✅ Telegram listener başlatıldı")
        
        # Kanalları dinle
        async for message in self.client.iter_messages(['channel1', 'channel2']):
            await self.process_message(message)
    
    async def process_message(self, message):
        # Mesajı işle ve AI'ya gönder
        if self.is_product_message(message):
            await self.send_to_ai_workflow(message)
    
    async def send_to_ai_workflow(self, message):
        # n8n workflow'unu tetikle
        webhook_url = "https://your-n8n-instance.com/webhook/telegram-webhook"
        
        payload = {
            'message_text': message.text,
            'message_id': message.id,
            'sender': message.sender_id,
            'timestamp': message.date.isoformat()
        }
        
        import requests
        response = requests.post(webhook_url, json=payload)
        
        if response.status_code == 200:
            print("✅ Mesaj AI workflow'una gönderildi")
        else:
            print(f"❌ Gönderim başarısız: {response.status_code}")

# Kullanım
listener = TRMTelegramListener()
asyncio.run(listener.start())
```

#### Adım 7: Sosyal Medya API Entegrasyonları
**Facebook API:**
1. [Facebook Developers](https://developers.facebook.com) gidin
2. Yeni uygulama oluşturun
3. Marketing API ve Pages API izinlerini alın
4. Access token'ı alın

**Instagram API:**
1. [Instagram Basic Display API](https://developers.facebook.com/docs/instagram-basic-display-api) gidin
2. Uygulamanıza bağlayın
3. Content publishing izinlerini alın

**TikTok API:**
1. [TikTok for Developers](https://developers.tiktok.com) gidin
2. Geliştirici hesabı oluşturun
3. Video upload API izinlerini alın

**Entegrasyon Kodu:**
```python
import facebook
import instagrapi

class SocialMediaIntegrator:
    def __init__(self):
        self.facebook_token = os.getenv('FACEBOOK_ACCESS_TOKEN')
        self.instagram_token = os.getenv('INSTAGRAM_ACCESS_TOKEN')
        self.tiktok_token = os.getenv('TIKTOK_ACCESS_TOKEN')
        
        # Client'ları başlat
        self.facebook_client = facebook.GraphAPI(access_token=self.facebook_token)
        self.instagram_client = instagrapi.InstagramAPI()
    
    async def publish_to_facebook(self, content, image_path):
        """Facebook'a paylaşım"""
        page_id = os.getenv('FACEBOOK_PAGE_ID')
        
        # Fotoğraf yükle
        photo = self.facebook_client.put_photo(
            image_path,
            message=content,
            album_path=f'/{page_id}/photos'
        )
        
        return photo
    
    async def publish_to_instagram(self, content, image_path):
        """Instagram'a paylaşım"""
        media = self.instagram_client.media_upload(image_path, caption=content)
        self.instagram_client.media_configure(media)
        
        return media
    
    async def publish_to_tiktok(self, content, video_path):
        """TikTok'a paylaşım"""
        # TikTok API kullanarak video yükle
        # (TikTok API spesifik implementasyon gerektirir)
        
        return {"status": "success", "video_id": "tiktok_video_id"}
```

#### Adım 8: Test ve Devreye Alma
**Test Senaryoları:**
1. **Telegram Dinleyici Testi:**
   - Test kanalına ürün gönderin
   - n8n workflow'unun tetiklendiğini kontrol edin
   
2. **AI İşleme Testi:**
   - Test görseli gönderin
   - DeepSeek ve Claude yanıtlarını kontrol edin
   
3. **Sosyal Medya Testi:**
   - Test içeriği paylaşın
   - Tüm platformlarda yayınlandığını doğrulayın
   
4. **Raporlama Testi:**
   - Test satışı oluşturun
   - Telegram raporunun geldiğini kontrol edin

---

## BÖLÜM 2: TRM FULL OTOMASYON SİSTEMİNİN ÇALIŞMASI

### SİSTEMİN ÇALIŞMA DÖNGÜSÜ

#### Adım 1: Veri Yakalama
**Aktif ve şu an Çalışıyor:**
- Telegram kanalları ve web siteleri anlık izlenir
- Yeni ürün paylaşıldığında botlar saniyeler içinde yakalar
- Trendurunlermarket tarafından tüm ürünler sistem tarafından otomatik olarak içeri alınır

**İş Akışı:**
```
Telegram/Web Sitesi → Bot Yakalar → n8n Workflow → AI İşleme → Google Drive Kayıt
```

**Aktif Görev Detayı:**
- **Görev Adı:** Ürünleri Otomatik Çekme
- **Durum:** Aktif ve şu an çalışıyor
- **Adres:** https://trm-cloudpackage-final-safe.onrender.com/internal/ingest/products
- **Açıklama:** Trendurunlermarket tarafından tüm ürünler sistem tarafından otomatik olarak içeri alınıyor

#### Adım 2: AI İşleme
**Aktif ve şu An Çalışıyor:**
- Görsel/video DeepSeek'e gönderilir
- Ürünün hedef kitlesi belirlenir
- Claude profesyonel satış metinleri hazırlar

**İş Akışı:**
```
Google Drive → DeepSeek Analiz → Claude Metin Üretimi → İçerik Hazırlama
```

#### Adım 3: İçerik Üretimi
**Aktif ve şu An Çalışıyor:**
- Orijinal materyaller bozulmadan üzerine trendurunlermarket.com linki ve logo eklenerek Google Drive'a kaydedilir

**İş Akışı:**
```
AI İşleme Sonucu → Görsel İşleme → Mağaza Linki Ekleme → Google Drive Kayıt
```

#### Adım 4: Çoklu Paylaşım
**Aktif ve şu An Çalışıyor:**
- n8n zinciri, içeriği eş zamanlı olarak tüm sosyal medya ve bloglarda yayınlar

**İş Akışı:**
```
Hazır İçerik → n8n Zinciri → Tüm Platformlara Dağıtım → Yayın Takibi
```

#### Adım 5: Performans Takibi
**Aktif ve şu An Çalışıyor:**
- Satışlar ve komisyonlar anında Drive'daki Excel tablosuna işlenir
- Komisyon hesaplama motoru otomatik çalışır

**İş Akışı:**
```
Satış Verisi → Komisyon Hesaplama → Excel Güncelleme → Performans Raporu
```

#### Adım 6: Onay Mekanizması (İsteğe Bağlı)
**Aktif ve şu An Çalışıyor:**
- Panel üzerinden hangi ürünlerin paylaşılacağı seçilebilir
- Tam "Otomatik Pilot" moduna geçilebilir

**İş Akışı:**
```
Panel Onayı → Yayın Kararı → Sosyal Medya Gönderimi → Sonuç Takibi
```

#### Adım 7: Nihai Rapor
**Aktif ve şu An Çalışıyor:**
- Her sabah kazanç ve operasyon özeti Telegram'a gönderilir

**İş Akışı:**
```
Günlük Veri Topla → Özet Hesapla → Telegram Raporu Gönder
```

### AKTİF GÖREVLER

#### 1) Ürünleri Otomatik Çekme
**Görev Aktif ve şu An Çalışıyor:**
- Telegram kanallarını ve web sitelerini anlık izler
- Yeni ürün paylaşıldığında botlar saniyeler içinde yakalar
- Trendurunlermarket tarafından tüm ürünler sistem tarafından otomatik olarak içeri alınır

**Teknik Detaylar:**
- **Webhook URL:** https://trm-cloudpackage-final-safe.onrender.com/internal/ingest/products
- **İzleme Frekansı:** Saniyede bir kontrol
- **Veri Kaynağı:** Telegram kanalları, magazanolsun.com, rakip siteler
- **Desteklenen Formatlar:** Metin, görsel, video, link

#### 2) Ürün ID - Kategori - Komisyon Eşleştirme
**Görev Aktif ve şu An Çalışıyor:**
- Ürünlerin kategorisi alınıyor
- Kategori komisyon oranı ile eşleştiriliyor
- Gelir odaklı tabloyla uyumlu şekilde öncelik puanı veriliyor

**Komisyon Tablosu:**
```python
COMMISSION_RATES = {
    'Elektronik': {'min': 15, 'max': 25, 'avg': 20},
    'Giyim': {'min': 20, 'max': 35, 'avg': 27.5},
    'Ev': {'min': 10, 'max': 20, 'avg': 15},
    'Spor': {'min': 12, 'max': 22, 'avg': 17},
    'Kozmetik': {'min': 18, 'max': 30, 'avg': 24},
    'Kitap': {'min': 8, 'max': 15, 'avg': 11.5},
    'Oyuncak': {'min': 10, 'max': 18, 'avg': 14}
}

def calculate_priority_score(product):
    category = product['category']
    commission_rate = product['commission_rate']
    
    category_rate = COMMISSION_RATES.get(category, {'avg': 15})
    category_score = (commission_rate / category_rate['avg']) * 100
    
    return min(category_score, 100)  # Maksimum 100 puan
```

#### 3) Komisyon Hesaplama Motoru
**Görev Aktif ve Çalışmaya Hazır:**
- Sipariş gelince otomatik hesaplar
- Satış fiyatını okur
- Tedarik maliyetini çeker
- Komisyon oranını kategoriye göre koyar
- Ödeme ücreti hesaplar
- Kargo maliyeti ekler
- Toplam net komisyonu hesaplar

**Hesaplama Formülü:**
```python
def calculate_commission(order_data):
    # Temel veriler
    sale_price = order_data['sale_price']
    category = order_data['category']
    shipping_cost = order_data.get('shipping_cost', 0)
    payment_fee = order_data.get('payment_fee', 0)
    
    # Komisyon oranını al
    commission_rate = get_category_commission_rate(category)
    
    # Brüt komisyon
    gross_commission = sale_price * (commission_rate / 100)
    
    # Net komisyon (maliyetler düşüldükten sonra)
    net_commission = gross_commission - shipping_cost - payment_fee
    
    return {
        'sale_price': sale_price,
        'commission_rate': commission_rate,
        'gross_commission': gross_commission,
        'net_commission': net_commission,
        'costs': {
            'shipping': shipping_cost,
            'payment': payment_fee
        }
    }
```

#### 4) 15 Günlük Vade Hesaplama
**Görev Aktif ve Çalışmaya Hazır:**
- Vade tarihi = Sipariş tarihi + 15 gün
- Günlük olarak vade kontrolü yapılır
- Vade dolan komisyonları ödeme listesine ekler

**Vade Hesaplama Kodu:**
```python
from datetime import datetime, timedelta

def calculate_commission_due(order_date):
    """15 günlük vade hesapla"""
    due_date = order_date + timedelta(days=15)
    today = datetime.now()
    
    days_until_due = (due_date - today).days
    
    if days_until_due <= 0:
        return {
            'status': 'due',
            'days_overdue': abs(days_until_due),
            'due_date': due_date
        }
    else:
        return {
            'status': 'pending',
            'days_until_due': days_until_due,
            'due_date': due_date
        }

# Günlük kontrol
def check_daily_commissions():
    pending_orders = get_pending_orders()
    
    for order in pending_orders:
        due_info = calculate_commission_due(order['order_date'])
        
        if due_info['status'] == 'due':
            # Ödeme listesine ekle
            add_to_payment_list({
                'order_id': order['id'],
                'amount': order['net_commission'],
                'due_date': due_info['due_date'],
                'days_overdue': due_info['days_overdue']
            })
```

#### 5) Excel Komisyon Raporu Üretme
**Görev Aktif ve Çalışıyor:**
- Otomatik raporlama sistemi aktif
- Günlük olarak Excel raporu oluşturur
- Google Drive'a kaydeder
- Panel üzerinden erişim sağlar

**Excel Raporu Kodu:**
```python
import pandas as pd
from datetime import datetime

def generate_commission_report():
    """Excel komisyon raporu üret"""
    
    # Verileri topla
    commissions = get_daily_commissions()
    
    # DataFrame oluştur
    df = pd.DataFrame(commissions)
    
    # Excel dosyası oluştur
    report_filename = f"komisyon_raporu_{datetime.now().strftime('%Y%m%d')}.xlsx"
    
    with pd.ExcelWriter(report_filename, engine='openpyxl') as writer:
        # Ana rapor sayfası
        df.to_excel(writer, sheet_name='Komisyonlar', index=False)
        
        # Özet sayfası
        summary_data = {
            'Toplam Komisyon': [df['net_commission'].sum()],
            'Ortalama Komisyon': [df['net_commission'].mean()],
            'İşlem Sayısı': [len(df)],
            'Tarih': [datetime.now().strftime('%d.%m.%Y')]
        }
        
        summary_df = pd.DataFrame(summary_data)
        summary_df.to_excel(writer, sheet_name='Özet', index=False)
    
    # Google Drive'a yükle
    upload_to_drive(report_filename, 'TRM_Raporlar/Gunluk')
    
    return report_filename
```

### İŞLETİM PROSEDÜRLERİ

#### Sabah Rutini (09:00)
1. **Sistem Durumu Kontrolü:**
   - Tüm modüllerin çalıştığını doğrula
   - Panellere erişimi test et
   - API anahtarlarının geçerliliğini kontrol et

2. **Önceki Günün Değerlendirmesi:**
   - Satış performansını analiz et
   - Hata raporlarını incele
   - Sistem kaynak kullanımını değerlendir

3. **Günün Planlaması:**
   - Öncelikli ürünleri belirle
   - Kampanya takvimini kontrol et
   - AI kaynaklarını optimize et

#### Öğleden Sonra Rutini (14:00)
1. **Performans Analizi:**
   - CPU, bellek, disk kullanımını kontrol et
   - Yanıt sürelerini ölç
   - Optimizasyon ihtiyaçlarını belirle

2. **Veri Senkronizasyonu:**
   - Google Drive senkronizasyonunu kontrol et
   - Veri tutarlılığını doğrula
   - Yedekleme durumunu kontrol et

#### Akşam Rutini (18:00)
1. **Günlük Raporlama:**
   - Satış özetini hazırla
   - Komisyon durumunu analiz et
   - Performans metriklerini topla

2. **Sistem Bakımı:**
   - Log dosyalarını temizle
   - Geçici dosyaları sil
   - Sistem kaynaklarını serbest bırak

#### Gece Rutini (23:00)
1. **Otomatik Yedekleme:**
   - Tüm kritik verileri yedekle
   - Google Drive'a senkronize et
   - Yedek başarısını doğrula

2. **Sistem Optimizasyonu:**
   - Veri tabanını optimize et
   - Önbelleği temizle
   - Sistemi yeniden başlatma hazırlığı yap

---

## BÖLÜM 3: DİĞER FİRMALARA ADAPTE ETME

### MODÜLER EKLEME YÖNTEMİ

#### YÖNTEM A: MODÜLER EKLEME (AYNI SİSTEM İÇİNDE - TAVSİYE EDİLEN)

**Avantajları:**
- Tek sistem üzerinden yönetim
- Daha düşük maliyet
- Merkezi kontrol
- Kolay bakım

**Uygulama Adımları:**
1. **n8n üzerinde yeni bir "Akış" (Workflow) oluşturulur**
2. **Yeni firmanın Telegram kanalları sisteme ikinci bir kaynak olarak tanımlanır**
3. **API anahtarları ve mağaza satış linkleri eklenir**
4. **Aynı AI motoru üzerinden içerik üretimi devam eder**
5. **Raporlama sisteminde firma bazında ayrıştırma yapılır**

**Yeni Workflow Oluşturma:**
```json
{
  "name": "Yeni Firma Otomasyon Akışı",
  "nodes": [
    {
      "name": "Yeni Firma Telegram Webhook",
      "type": "webhook",
      "webhook": "new_firma_webhook"
    },
    {
      "name": "Firma AI Processing",
      "type": "function",
      "function": "process_firma_with_ai",
      "parameters": {
        "deepseek_key": "{{FIRMA_DEEPSEEK_API_KEY}}",
        "claude_key": "{{FIRMA_CLAUDE_API_KEY}}"
      }
    },
    {
      "name": "Firma Content Generation",
      "type": "function",
      "function": "generate_firma_content"
    },
    {
      "name": "Firma Social Publisher",
      "type": "function",
      "function": "publish_firma_to_social"
    }
  ]
}
```

#### YÖNTEM B: SİSTEM KOPYALAMA (HER FİRMA İÇİN AYRI KURULUM)

**Avantajları:**
- Tam bağımsız çalışma
- Özelleştirme imkanı
- Güvenlik ayrımı
- Ölçeklenebilirlik

**Uygulama Adımları:**
1. **Mevcut sistem klasörü tamamen kopyalanır**
2. **Yeni firma için özel yapılandırma yapılır**
3. **Ayrı bulut sunucu ve API anahtarları kullanılır**
4. **Bağımsız Google Drive klasörü oluşturulur**
5. **Ayrı Telegram bot ve sosyal medya hesapları entegre edilir**

**Sistem Kopyalama Script'i:**
```batch
@echo off
echo 🔄 Yeni Firma Sistemi Kopyalanıyor...

# Ana sistem klasörünü kopyala
xcopy "TRM_Full_Otomasyon_Sistemi" "TRM_Firma_Yeni" /E /I /H /Y

# Yeni firma için özel yapılandırma
cd "TRM_Firma_Yeni"

# .env dosyasını oluştur
(
echo # YENI FIRMA AYARLARI
echo TELEGRAM_API_ID=yeni_firma_api_id
echo TELEGRAM_API_HASH=yeni_firma_api_hash
echo TELEGRAM_PHONE=+90555xxxxxxx
echo DEEPSEEK_API_KEY=yeni_firma_deepseek_key
echo CLAUDE_API_KEY=yeni_firma_claude_key
echo FACEBOOK_ACCESS_TOKEN=yeni_firma_facebook_token
echo INSTAGRAM_ACCESS_TOKEN=yeni_firma_instagram_token
echo STORE_URL=https://yenifirmamagazasi.com
echo COMMISSION_THRESHOLD=20.0
) > .env

echo ✅ Yeni firma sistemi kopyalandı ve yapılandırıldı
echo 📝 Lütfen API anahtarlarını güncelleyin
pause
```

### TAVSİYE EDİLEN YÖNTEM

Yöntem A (Modüler Ekleme) daha ekonomik ve yönetimi kolay olduğu için tavsiye edilir. Ancak firmalar arasında rekabet veya güvenlik endişesi varsa Yöntem B tercih edilebilir.

### FİRMA EKLEME KONTROL LİSTESİ

#### Modüler Ekleme İçin:
- [ ] n8n yeni workflow oluşturma
- [ ] Firma API anahtarlarını ekleme
- [ ] Telegram kanal entegrasyonu
- [ ] Mağaza linkleri tanımlama
- [ ] Raporlama ayarlarını güncelleme
- [ ] Test ve devreye alma

#### Sistem Kopyalama İçin:
- [ ] Sistem klasörünü kopyalama
- [ ] Yeni bulut sunucu kurulumu
- [ ] Ayrı API anahtarları oluşturma
- [ ] Bağımsız Google Drive kurulumu
- [ ] Yeni Telegram bot oluşturma
- [ ] Sosyal medya hesaplarını entegrasyonu
- [ ] Test ve devreye alma

---

## BÖLÜM 4: TEKNİK ÖZELLİKLER VE GEREKSİNİMLER

### MİNİMUM SİSTEM GEREKSİNİMLERİ

**Bulut Sunucu:**
- **RAM:** 2GB minimum, 4GB önerilir
- **CPU:** 1 vCPU minimum, 2 vCPU önerilir
- **Depolama:** 20GB minimum, 50GB önerilir
- **Ağ:** İnternet bağlantısı

**Yerel Sistem:**
- **İşletim Sistemi:** Windows 10/11 (64-bit)
- **İşlemci:** Intel Core i3 veya AMD Ryzen 3
- **Bellek:** 4GB minimum, 8GB önerilir
- **Depolama:** 2GB boş alan
- **Python:** 3.8+ (3.10+ önerilir)

**Yazılım Gereksinimleri:**
- **Python 3.8+**
- **Google Chrome** (Panel için)
- **Windows PowerShell** (Yüklü gelir)
- **Git** (Version control için)

### GÜVENLİK ÖNLEMLERİ

**API Anahtarları Güvenliği:**
- API anahtarlarını güvenli bir yerde saklayın
- Asla kod içinde doğrudan API anahtarı yazmayın
- Ortam değişkenlerini kullanın
- Düzenli olarak anahtarları güncelleyin

**Sistem Güvenliği:**
- Firewall ayarlarını yapılandırın
- Antivirüs istisnaları ekleyin
- Port güvenliğini sağlayın
- Düzenli yedekleme yapın

**Veri Güvenliği:**
- Hassas verileri şifreleyin
- GDPR uyumluluğu sağlayın
- Veri saklama politikası oluşturun
- Erişim loglarını tutun

### PERFORMANS OPTİMİZASYONU

**Otomatik Temizleme Görevleri:**
- Log dosyalarını düzenli temizleme (30 günden eski)
- Geçici dosyaları otomatik silme
- Önbelleği temizleme
- Veri tabanını optimize etme

**Kaynak Yönetimi:**
- CPU kullanımını izleme (%80 altında tut)
- Bellek kullanımını kontrol etme (%85 altında tut)
- Disk alanını düzenli kontrol etme (%10 boş alan bırak)
- Ağ trafiğini optimize etme

**Load Balancing (Çoklu Firma Durumunda):**
- İş yükünü firmalar arasında dağıt
- Otomatik failover mekanizması
- Performans izleme ve raporlama
- Dinamik kaynak ayırma

---

## 📋 SON KONTROL LİSTESİ

### KURULUM SONRASI KONTROL
- [ ] Bulut sunucu çalışıyor
- [ ] Tüm modüller aktif
- [ ] API anahtarları geçerli
- [ ] Telegram listener çalışıyor
- [ ] AI servisleri bağlandı
- [ ] Sosyal medya hesapları hazır
- [ ] Google Drive entegrasyonu tamam
- [ ] n8n workflow'ları aktif
- [ ] Paneller erişilebilir durumda

### İŞLETİM KONTROLÜ
- [ ] Veri yakalama aktif
- [ ] AI işleme çalışıyor
- [ ] İçerik üretimi devam ediyor
- [ ] Çoklu paylaşım aktif
- [ ] Performans takibi çalışıyor
- [ ] Komisyon hesaplama hazır
- [ ] Vade takibi aktif
- [ ] Raporlama sistemi çalışıyor

### FİRMA EKLEME KONTROLÜ
- [ ] Yeni workflow oluşturuldu
- [ ] API anahtarları eklendi
- [ ] Telegram entegrasyonu tamam
- [ ] Sosyal medya hazır
- [ ] Testler başarılı
- [ ] Performans kabul edilebilir
- [ ] Güvenlik önlemleri alındı

---

**TRM FULL OTOMASYON SİSTEMİ v3.0 - Kurulum ve İşletim Rehberi**

*Bu rehber ile sistemi kurabilir, işletebilir ve yeni firmalar için ölçeklendirebilirsiniz.*
