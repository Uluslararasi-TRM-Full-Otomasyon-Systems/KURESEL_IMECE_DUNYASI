# 🏗️ SYSTEM ARCHITECTURE — TRM v5.1
## Merkezi Ayar, Modüler Yapı ve Finansal Havuz Mimarisi

---

## 1. GENEL MİMARİ AKIŞ

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
               TRM OTOMASYON EKOSİSTEMİ
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  VERİ KAYNAKLARI          İŞLEM MOTORU          ÇIKIŞ
  ─────────────────         ──────────────         ──────
  magazanolsun.com  ──►                    ──►  Instagram
  Telegram Grupları ──►   MASTER_CONTROLLER ──►  Facebook
  Tedarikçi Siteleri──►   + TRM AI KATMANI  ──►  TikTok
  Endeksa.com       ──►                    ──►  Telegram
  Hoodmaps          ──►                    ──►  YouTube
                                           ──►  LinkedIn
                                           ──►  Blog
  
  DEPOLAMA                 İZLEME                BİLDİRİM
  ─────────                ───────                ────────
  Dropbox          ◄──    Watchdog      ──►    Telegram
  Google Drive     ◄──    Health Monitor──►    Discord
  SQLite DB        ◄──    Self-Healing  ──►    Viber
```

---

## 2. MERKEZİ AYAR SİSTEMİ

Tüm ayarlar tek dosyada toplanır: `secrets.env`

```env
# ═══════════════════════════════════════
# TRM v5.1 — MERKEZI AYARLAR
# ═══════════════════════════════════════

# SİSTEM
SYSTEM_NAME=TRM-FULL-OTOMASYON
TRM_MODE=live                    # live | test | demo

# TELEGRAM
TELEGRAM_API_ID=xxxxxxxx
TELEGRAM_API_HASH=xxxxxxxxxxxxxxxx
TELEGRAM_BOT_TOKEN=xxxxxx:xxxxxxx
TELEGRAM_CHAT_ID=xxxxxxxxx
TELEGRAM_PHONE=+90xxxxxxxxxx

# AI
OPENAI_API_KEY=sk-xxxxxxxxxxxx
DEEPSEEK_API_KEY=sk-xxxxxxxxxxxx

# SOSYAL MEDYA
BUFFER_ACCESS_TOKEN=xxxxxxxxxx

# BULUT DEPOLAMA
DROPBOX_ACCESS_TOKEN=xxxxxxxxxx
GOOGLE_DRIVE_FOLDER_ID=xxxxxxxxx

# FİNANS
BANKA_IBAN=TR00 0000 0000 0000 0000 00
KOMISYON_ESIK_TRY=50

# BİLDİRİM
DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/xxx
VIBER_BOT_TOKEN=xxxxxxxxxx
```

---

## 3. BAĞIMSIZ MODÜLER YAPI (PLUG-AND-PLAY)

```python
# modules/ klasör yapısı:
modules/
├── __init__.py
├── base_module.py        # Tüm modüllerin kalıtım aldığı temel sınıf
├── scraper_module.py     # Veri çekme
├── ai_module.py          # İçerik üretimi
├── social_module.py      # Sosyal medya paylaşımı
├── notification_module.py # Bildirim
└── yeni_modul.py         # YENİ MODÜL EKLEMEK İÇİN ŞABLON
```

```python
# base_module.py — Yeni modül şablonu
class BaseModule:
    def __init__(self, name: str):
        self.name = name
        self.active = True
    
    async def start(self): pass
    async def stop(self): pass
    async def health_check(self) -> bool: return True
    async def get_status(self) -> dict: return {'active': self.active}

# Yeni modül eklemek:
# 1. BaseModule'den kalıt al
# 2. modules/ klasörüne koy
# 3. MASTER_CONTROLLER.py'ye import ekle
# 4. Deploy — HAZIR!
```

---

## 4. MULTI-TENANT YÖNETİMİ

```
ANA KULLANICI (Proje Sahibi)
        │
        ▼
  HAVUZ HESABI
  ┌─────────────────────────────────┐
  │  Toplam Komisyon Geliri         │
  │  Otomatik Hak Hesaplama         │
  │  Otomatik Transfer Bildirimi    │
  └─────────────────────────────────┘
        │           │           │
        ▼           ▼           ▼
   3. KİŞİ A    3. KİŞİ B    3. KİŞİ C
   (Engelli)    (Yaşlı)      (Ekonomik)
   %X komisyon  %X komisyon  %X komisyon
```

**multi_tenant_manager.py — Temel Yapı:**

```python
class MultiTenantManager:
    def __init__(self):
        self.tenants = {}  # {tenant_id: {buffer_token, komisyon_orani}}
    
    def tenant_ekle(self, ad, buffer_token, komisyon_orani):
        self.tenants[ad] = {
            'buffer_token': buffer_token,
            'komisyon_orani': komisyon_orani,
            'toplam_kazanc': 0.0
        }
    
    def komisyon_hesapla(self, toplam, tenant_id):
        oran = self.tenants[tenant_id]['komisyon_orani']
        return toplam * oran / 100
    
    async def herkese_paylas(self, icerik):
        # Tüm tenant'ların Buffer hesabına gönder
        for tenant in self.tenants.values():
            await self.buffer_gonder(tenant['buffer_token'], icerik)
```

---

## 5. FİNANSAL HAVUZ AKIŞ ŞEMASI

```
Satış Gerçekleşir
      │
      ▼
magazanolsun.com komisyon bildirimi
      │
      ▼
BANKA_KOMISYON_BILDIRIM.py
      │
      ├──► komisyon_log.jsonl'e kaydet
      │
      ├──► Hangi tenant'ın paylaşımından?
      │         │
      │         ▼
      │    Multi-Tenant Manager
      │    → Tenant payını hesapla
      │    → Ayrı dosyaya kaydet
      │
      └──► Telegram/Discord/Viber BİLDİR
               "Satış: 150 TRY
                Senin payın: 45 TRY
                Tenant payı: 15 TRY"
```

---

## 6. WATCHDOG MİMARİSİ

```
WATCHDOG.py (30 saniyede bir döngü)
      │
      ├── main_orchestrator çalışıyor mu? → Hayır → YENİDEN BAŞLAT
      ├── telegram_bot çalışıyor mu?      → Hayır → YENİDEN BAŞLAT
      ├── İnternet bağlantısı var mı?     → Hayır → 60sn bekle, tekrar dene
      ├── API rate limit aşıldı mı?       → Evet  → Bekleme süresini ayarla
      └── Bellek kullanımı %95 üstü mü?  → Evet  → ALARM + YENİDEN BAŞLAT
```
