# 🔧 SELF-HEALING DESIGN — TRM v5.1
## Kendi Kendini İyileştirme, Rollback ve Siber Güvenlik

---

## 1. SELF-HEALING MİMARİSİ

```
SORUN OLUŞTU
     │
     ▼
self_healing_manager.py
     │
     ├── Algıla: Hangi modül çöktü?
     │
     ├── Sınıflandır:
     │   ├── Geçici hata → Yeniden başlat
     │   ├── API hatası → Rate limit bekle
     │   ├── Bellek hatası → Temizle + başlat
     │   └── Bilinmeyen → Kaydet + İnsan bildiri
     │
     ├── Çöz: Otomatik kurtarma dene
     │
     ├── Doğrula: Modül tekrar çalışıyor mu?
     │
     └── Raporla: Telegram/Discord/Viber
```

---

## 2. OLAY TİPLERİ VE TEPKİLER

| Olay | Otomatik Tepki | Bildirim |
|------|---------------|---------|
| Modül çöktü | Yeniden başlat | ✅ Gönder |
| İnternet koptu | 60sn bekle, tekrar | ❌ Gönderme |
| API rate limit | Bekleme süresi ayarla | ❌ Gönderme |
| Bellek %95+ | Temizle + yeniden başlat | ✅ Gönder |
| 5x aynı hata | Durdur + insan bildiri | ✅ Gönder |
| Güvenlik ihlali | KİLİTLE + bildir | ✅ ACİL GÖNDER |
| Veri kaybı riski | Yedekle + bildir | ✅ Gönder |

---

## 3. ROLLBACK SİSTEMİ

```python
# rollback_manager.py
import shutil
from pathlib import Path
from datetime import datetime

class RollbackManager:
    def __init__(self):
        self.backup_dir = Path('backups/')
        self.backup_dir.mkdir(exist_ok=True)
    
    def yedek_al(self, dosya_yolu: str) -> str:
        """Değişiklikten önce yedek al"""
        kaynak = Path(dosya_yolu)
        hedef = self.backup_dir / f"{kaynak.name}.{datetime.now().strftime('%Y%m%d_%H%M%S')}.bak"
        shutil.copy2(kaynak, hedef)
        return str(hedef)
    
    def geri_don(self, yedek_yolu: str, hedef_yolu: str):
        """Sorun çıkarsa eski versiyona dön"""
        shutil.copy2(yedek_yolu, hedef_yolu)
    
    def eski_yedekleri_temizle(self, gun: int = 7):
        """7 günden eski yedekleri sil"""
        import time
        esik = time.time() - (gun * 86400)
        for yedek in self.backup_dir.glob('*.bak'):
            if yedek.stat().st_mtime < esik:
                yedek.unlink()
```

---

## 4. SİBER GÜVENLİK KALKANI

### A) Yetkisiz Erişim Algılama

```python
# security_shield.py
import hashlib
import os
import json
from datetime import datetime

class SecurityShield:
    def __init__(self):
        self.izin_verilen_ip = os.getenv('ALLOWED_IP', '')
        self.parmak_izi_dosya = 'data/system_fingerprint.json'
        self.kilitli = False
    
    def sistem_parmak_izi_al(self) -> str:
        """Sunucu parmak izini hesapla"""
        import platform
        veri = f"{platform.node()}{platform.machine()}"
        return hashlib.sha256(veri.encode()).hexdigest()
    
    def parmak_izi_kaydet(self):
        with open(self.parmak_izi_dosya, 'w') as f:
            json.dump({
                'parmak_izi': self.sistem_parmak_izi_al(),
                'tarih': datetime.now().isoformat()
            }, f)
    
    def parmak_izi_kontrol(self) -> bool:
        """Sistem değişti mi?"""
        if not os.path.exists(self.parmak_izi_dosya):
            self.parmak_izi_kaydet()
            return True
        with open(self.parmak_izi_dosya) as f:
            kayitli = json.load(f)
        return kayitli['parmak_izi'] == self.sistem_parmak_izi_al()
    
    def freeze_mode(self):
        """Yetkisiz erişimde sistemi kilitle"""
        self.kilitli = True
        # API anahtarlarını geçici olarak devre dışı bırak
        os.environ['TRM_FROZEN'] = '1'
        # Acil bildirim gönder
        import asyncio
        asyncio.create_task(self._acil_bildir())
    
    async def _acil_bildir(self):
        from MESAJLASMA_BILDIRIM import herkese_bildir
        await herkese_bildir(
            "🚨 GÜVENLİK ALARMI!\n"
            "Yetkisiz sistem erişimi algılandı.\n"
            "Sistem FREEZE MODE'a geçti.\n"
            f"Zaman: {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}"
        )
```

### B) Kod Gizleme (Deploy Öncesi)

```bash
# deploy_oncesi_gizle.sh
# PyArmor ile kod gizleme

pip install pyarmor

# Tüm Python dosyalarını gizle
pyarmor gen --output dist/ src/

# dist/ klasörünü Railway/Render'a yükle
# Kaynak kod gizlenmiş olur
```

---

## 5. BİLDİRİM POLİTİKASI (SADECE KRİTİK)

```python
# Sistem HER OLAYI bildirmez. Sadece bunları bildirir:

BILDIRIM_GEREKTIREN_OLAYLAR = [
    "CRITICAL_ERROR",           # Kritik hata
    "SERVICE_CRASHED",          # Çöken servis
    "SERVICE_RESTARTED",        # Yeniden başlatılan servis
    "SECURITY_EVENT",           # Güvenlik olayı
    "UNAUTHORIZED_ACCESS",      # Yetkisiz erişim girişimi
    "DATA_LOSS_RISK",           # Veri kaybı riski
    "API_CONNECTION_FAILED",    # API bağlantı problemi
    "CLOUD_CONNECTION_FAILED",  # Cloud bağlantı problemi
    "UNRESOLVABLE_PROBLEM",     # Çözülemeyen problem
    "HUMAN_INTERVENTION_NEEDED",# İnsan müdahalesi gerekiyor
    "SYSTEM_STOP_RISK",         # Sistemi durdurabilecek risk
    "KOMISYON_ALINDI",          # Finansal hareket (her zaman bildir)
]

# Bildirim kanalları: Telegram + Discord + Viber
# Mesaj formatı: Kısa, net, teknik detay içerir
```

---

## 6. INCIDENT MANAGER

```python
# incident_manager.py
class IncidentManager:
    """Olayları kaydeder, analiz eder, raporlar."""
    
    SEVERITIES = {1: 'KRİTİK', 2: 'YÜKSEK', 3: 'ORTA', 4: 'DÜŞÜK'}
    
    def olay_kaydet(self, tip, modül, detay, severity=3):
        olay = {
            'id': self._yeni_id(),
            'tip': tip,
            'modül': modül,
            'detay': detay,
            'severity': severity,
            'tarih': datetime.now().isoformat(),
            'cozuldu': False
        }
        self._db_kaydet(olay)
        if severity <= 2:
            asyncio.create_task(self._bildir(olay))
        return olay
    
    def tekrarlayan_analiz(self) -> list:
        """Son 24 saatte 3+ kez tekrarlayan hataları bul"""
        # Kritik bulgu → insan müdahalesi öner
        pass
```
