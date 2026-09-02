# 🤖 AUTONOMOUS AI DESIGN — TRM v5.1
## Sınırlı TRM AI Katmanı ve "Önce Sor-Sonra Yap" Mekanizması

---

## 1. TRM AI'NIN GÜVENLİK SINIRLARI

```
TRM AI YAPAMAZ:               TRM AI YAPABİLİR:
──────────────────────         ──────────────────────
❌ Para harcayamaz             ✅ İçerik üretebilir
❌ Hesap açamaz                ✅ Görev planlayabilir
❌ Yetkisiz API çağrısı        ✅ Kampanya önerebilir
❌ Güvenlik kırma              ✅ Analiz yapabilir
❌ Finansal karar              ✅ Raporlayabilir
❌ Kullanıcı onaysız paylaşım  ✅ Hazırlayıp bekleyebilir
```

---

## 2. "ÖNCE SOR - SONRA YAP" ONAYI

Her önemli işlem öncesi kullanıcıya Telegram üzerinden onay gönderilir:

```
TRM AI sana şunu gönderir:
━━━━━━━━━━━━━━━━━━━━━━━━━━
🤖 TRM AI ONAY BEKLIYOR

📦 Görev: Ürün paylaşımı
📱 Platform: Instagram + Facebook + TikTok
🕒 Zaman: 20:30
📝 İçerik:
"🔥 Trend Ürün! Samsung Şarj Aleti
   ⚡ Hızlı şarj, 65W güç
   💰 199 TRY — Bugün sipariş ver!
   🔗 trendurunlermarket.com
   #teknoloji #şarj #trend"

✅ ONAYLA   ❌ REDDET   ✏️ DÜZENLE
━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**Telegram Bot Onay Kodu:**

```python
async def onay_iste(self, gorev: dict) -> bool:
    mesaj = f"""
🤖 TRM AI ONAY BEKLIYOR

📦 Görev: {gorev['tip']}
📱 Platform: {', '.join(gorev['platformlar'])}
📝 İçerik: {gorev['icerik'][:200]}

Onaylamak için /onayla_{gorev['id']}
Reddetmek için /reddet_{gorev['id']}
"""
    await telegram_bildir(mesaj)
    # 30 dakika bekle, cevap gelmezse iptal et
    return await self._bekle_onay(gorev['id'], timeout=1800)
```

---

## 3. GÖREV KUYRUĞU MİMARİSİ

```python
# task_queue.py
import asyncio
from dataclasses import dataclass
from datetime import datetime
from typing import List

@dataclass
class TRMGorev:
    id: str
    tip: str           # 'icerik_uret', 'paylas', 'analiz_et'
    oncelik: int       # 1=acil, 2=normal, 3=düşük
    veri: dict
    olusturma: datetime
    durum: str         # 'beklemede', 'onay_bekleniyor', 'tamamlandi'

class TRMGorevKuyruğu:
    def __init__(self):
        self.kuyruk: List[TRMGorev] = []
        self.tamamlanan: List[TRMGorev] = []
    
    def ekle(self, gorev: TRMGorev):
        self.kuyruk.append(gorev)
        self.kuyruk.sort(key=lambda x: x.oncelik)
    
    async def isle(self):
        while True:
            if self.kuyruk:
                gorev = self.kuyruk.pop(0)
                await self._calistir(gorev)
            await asyncio.sleep(5)
    
    async def _calistir(self, gorev: TRMGorev):
        # Önemli görevler için onay iste
        if gorev.tip in ['paylas', 'reklam_ver']:
            onaylandi = await self.ai.onay_iste(gorev.__dict__)
            if not onaylandi:
                gorev.durum = 'reddedildi'
                return
        # Onayland → çalıştır
        gorev.durum = 'tamamlandi'
        self.tamamlanan.append(gorev)
```

---

## 4. KAMPANYA PERFORMANS KARŞILAŞTIRMA

```python
class KampanyaAnalizoru:
    """Hangi kampanya daha iyi çalışıyor? Otomatik öğrenir."""
    
    def karsilastir(self, kampanya_a, kampanya_b) -> dict:
        return {
            'kazanan': 'A' if kampanya_a['etkilesim'] > kampanya_b['etkilesim'] else 'B',
            'a_etkilesim': kampanya_a['etkilesim'],
            'b_etkilesim': kampanya_b['etkilesim'],
            'oneri': f"'{kampanya_a['baslik']}' tarzı içerikler daha iyi performans gösteriyor"
        }
    
    def en_iyi_zaman(self, gecmis_veriler) -> str:
        """Geçmiş paylaşımlardan en iyi saati öğren"""
        saatler = {}
        for veri in gecmis_veriler:
            saat = veri['saat']
            saatler[saat] = saatler.get(saat, 0) + veri['etkilesim']
        return max(saatler, key=saatler.get)
```

---

## 5. KİTLE SEGMENTASYONU (18-60 YAŞ)

```python
SEGMENT_STRATEJILERI = {
    '18-25': {
        'ton': 'eğlenceli, emoji ağırlıklı, trend',
        'urun_tipleri': ['teknoloji', 'moda', 'oyun'],
        'platform': ['TikTok', 'Instagram'],
        'en_iyi_saat': '20:00-23:00'
    },
    '26-45': {
        'ton': 'bilgilendirici, güven odaklı, pratik',
        'urun_tipleri': ['ev', 'ofis', 'aile'],
        'platform': ['Facebook', 'Instagram'],
        'en_iyi_saat': '12:00-14:00, 19:00-21:00'
    },
    '46-60': {
        'ton': 'saygılı, net, güven veren',
        'urun_tipleri': ['ev yaşam', 'sağlık', 'bahçe'],
        'platform': ['Facebook'],
        'en_iyi_saat': '10:00-12:00, 15:00-17:00'
    }
}
```

---

## 6. ÖĞRENİLEN BİLGİLERİN KAYDEDILMESI

```python
# learning_memory.py
import sqlite3
from datetime import datetime

class LearningMemory:
    def __init__(self, db_path='data/learning_memory.db'):
        self.conn = sqlite3.connect(db_path)
        self._olustur()
    
    def _olustur(self):
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS ogrenilen_gorevler (
                id INTEGER PRIMARY KEY,
                gorev_tipi TEXT,
                parametre TEXT,
                sonuc TEXT,
                basari REAL,
                tarih TEXT
            )
        """)
    
    def kaydet(self, gorev_tipi, parametre, sonuc, basari):
        self.conn.execute(
            "INSERT INTO ogrenilen_gorevler VALUES (NULL,?,?,?,?,?)",
            (gorev_tipi, str(parametre), str(sonuc), basari, datetime.now().isoformat())
        )
        self.conn.commit()
    
    def en_basarili_strateji(self, gorev_tipi) -> dict:
        cur = self.conn.execute(
            "SELECT parametre, AVG(basari) as ort FROM ogrenilen_gorevler "
            "WHERE gorev_tipi=? GROUP BY parametre ORDER BY ort DESC LIMIT 1",
            (gorev_tipi,)
        )
        row = cur.fetchone()
        return {'parametre': row[0], 'ortalama_basari': row[1]} if row else {}
```
