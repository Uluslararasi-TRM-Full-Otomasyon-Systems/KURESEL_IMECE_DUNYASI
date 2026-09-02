#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Behavioral & Persona AI Agent
Kullanıcı/oturum etkileşimlerini analiz eden ve karakter profili çıkaran modül
"""

import uuid
import random
import threading
import time
import logging
from pathlib import Path
from datetime import datetime
from collections import defaultdict, deque

from database_manager import DatabaseManager

BASE_DIR = Path(__file__).resolve().parent
LOG_DIR = BASE_DIR / 'logs'
LOG_DIR.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s - [PersonaAI] %(message)s',
    handlers=[
        logging.FileHandler(LOG_DIR / 'persona_ai.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('PersonaAI')


PERSONA_TYPES = [
    "Fiyat Odaklı",
    "Hızlı Alıcı",
    "Trend Takipçisi",
    "Kalite Arayışçısı",
    "Karşılaştırmacı",
    "Sadık Müşteri",
    "Fırsat Avcısı",
    "Ağır Karar Verici",
    "Yenilikçi Erken Benimseyen",
    "Duygusal Alıcı"
]

CATEGORY_TYPES = [
    "Elektronik", "Moda", "Ev & Yaşam", "Kozmetik", "Spor",
    "Kitap", "Oyun", "Mobilya", "Gıda", "Aksesuar"
]


class PersonaInferenceEngine:
    """Kullanıcı davranışlarından persona çıkarım yapan motor"""

    def __init__(self):
        self.session_click_history = defaultdict(deque)
        self.session_dwell_history = defaultdict(deque)
        self.session_category_visits = defaultdict(lambda: defaultdict(int))
        self.persona_confidence_cache = {}

    def record_interaction(self, session_id, product_id, category, click_count, dwell_time_seconds, region):
        """Bir etkileşimi kaydet ve analiz için biriktir"""
        self.session_click_history[session_id].append({
            'product_id': product_id,
            'category': category,
            'click_count': click_count,
            'dwell_time': dwell_time_seconds,
            'region': region,
            'timestamp': datetime.now().isoformat()
        })
        if len(self.session_click_history[session_id]) > 50:
            self.session_click_history[session_id].popleft()

        self.session_dwell_history[session_id].append(dwell_time_seconds)
        if len(self.session_dwell_history[session_id]) > 50:
            self.session_dwell_history[session_id].popleft()

        if category:
            self.session_category_visits[session_id][category] += 1

    def infer_persona(self, session_id):
        """Kayıtlı davranışlardan persona çıkarımı yap"""
        clicks = list(self.session_click_history[session_id])
        dwells = list(self.session_dwell_history[session_id])
        categories = self.session_category_visits[session_id]

        if not clicks and not dwells:
            return "Analiz Ediliyor", 0.0

        total_clicks = sum(c['click_count'] for c in clicks) if clicks else 0
        avg_dwell = sum(dwells) / len(dwells) if dwells else 0
        unique_categories = len(categories)
        region = clicks[0]['region'] if clicks else 'yurtici'

        scores = defaultdict(float)

        # Hızlı Alıcı: Kısa dwell, çok sayıda hızlı tıklama
        if avg_dwell < 15 and total_clicks > 10:
            scores["Hızlı Alıcı"] += 0.65
        if avg_dwell < 8:
            scores["Hızlı Alıcı"] += 0.25

        # Fiyat Odaklı: Aynı kategoride çok gezinti, karşılaştırma yapısı
        if unique_categories == 1 and total_clicks > 12:
            scores["Fiyat Odaklı"] += 0.55
        if unique_categories <= 2 and total_clicks > 20:
            scores["Fiyat Odaklı"] += 0.30

        # Karşılaştırmacı: Birden fazla kategoride gezinti
        if unique_categories >= 3:
            scores["Karşılaştırmacı"] += 0.50
        if unique_categories >= 5:
            scores["Karşılaştırmacı"] += 0.30

        # Trend Takipçisi: Moda/Aksesuar gibi trend kategorileri
        trend_categories = {"Moda", "Aksesuar", "Kozmetik", "Oyun"}
        if any(cat in trend_categories for cat in categories.keys()):
            scores["Trend Takipçisi"] += 0.45
        if categories.get("Moda", 0) + categories.get("Aksesuar", 0) > 8:
            scores["Trend Takipçisi"] += 0.40

        # Kalite Arayışçısı: Uzun dwell süresi, detaylı inceleme
        if avg_dwell > 60:
            scores["Kalite Arayışçısı"] += 0.60
        if 30 < avg_dwell <= 60:
            scores["Kalite Arayışçısı"] += 0.25

        # Ağır Karar Verici: Çok sayıda tıklama + uzun dwell
        if total_clicks > 25 and avg_dwell > 40:
            scores["Ağır Karar Verici"] += 0.70
        if unique_categories >= 4 and avg_dwell > 45:
            scores["Ağır Karar Verici"] += 0.20

        # Fırsat Avcısı: Kısa ama yoğun tıklamalar
        if avg_dwell < 25 and 15 < total_clicks <= 30:
            scores["Fırsat Avcısı"] += 0.55

        # Yenilikçi Erken Benimseyen: Yurtdışı region + elektronik/oyun
        if region == 'yurtdisi' and ("Elektronik" in categories or "Oyun" in categories):
            scores["Yenilikçi Erken Benimseyen"] += 0.55
        if unique_categories >= 4 and region == 'yurtdisi':
            scores["Yenilikçi Erken Benimseyen"] += 0.25

        # Sadık Müşteri: Az kategori ama çok tıklama (dönüşlü ziyaret)
        if unique_categories <= 2 and total_clicks > 30:
            scores["Sadık Müşteri"] += 0.60

        # Duygusal Alıcı: Kozmetik/Moda ve orta derece dwell
        if "Kozmetik" in categories or "Moda" in categories:
            if 15 < avg_dwell < 50:
                scores["Duygusal Alıcı"] += 0.50

        if not scores:
            return "Analiz Ediliyor", 0.0

        best_persona = max(scores, key=scores.get)
        confidence = min(scores[best_persona], 0.99)
        return best_persona, confidence

    def get_session_profile(self, session_id):
        """Bir oturum için kapsamlı profil döndür"""
        persona, confidence = self.infer_persona(session_id)
        clicks = list(self.session_click_history[session_id])
        dwells = list(self.session_dwell_history[session_id])
        categories = dict(self.session_category_visits[session_id])

        return {
            'session_id': session_id,
            'inferred_persona': persona,
            'confidence': round(confidence, 4),
            'total_interactions': len(clicks),
            'total_clicks': sum(c['click_count'] for c in clicks) if clicks else 0,
            'avg_dwell_seconds': round(sum(dwells) / len(dwells), 2) if dwells else 0,
            'top_categories': sorted(categories.items(), key=lambda x: -x[1])[:5],
            'region': clicks[0]['region'] if clicks else 'yurtici',
            'last_activity': clicks[-1]['timestamp'] if clicks else None
        }


class BehavioralPersonaAgent:
    """Ana Behavioral & Persona AI Agent sınıfı"""

    def __init__(self, db=None):
        self.db = db or DatabaseManager()
        self.engine = PersonaInferenceEngine()
        self.is_running = False
        self._lock = threading.Lock()
        self._process_thread = None
        self._last_update_callbacks = []
        self._simulation_thread = None
        self._simulation_running = False
        logger.info("✅ Behavioral & Persona AI Agent başlatıldı")

    def register_update_callback(self, callback):
        """Yeni veri geldiğinde çağrılacak callback fonksiyonu kaydet"""
        self._last_update_callbacks.append(callback)

    def _notify_callbacks(self, data):
        """Tüm callback'leri tetikle"""
        for cb in self._last_update_callbacks:
            try:
                cb(data)
            except Exception as e:
                logger.error(f"Callback hatası: {e}")

    def process_interaction(self, session_id, product_id, category, click_count, dwell_time_seconds, region='yurtici'):
        """Bir kullanıcı etkileşimini işle, persona çıkar ve kaydet"""
        with self._lock:
            self.engine.record_interaction(
                session_id=session_id,
                product_id=product_id,
                category=category,
                click_count=click_count,
                dwell_time_seconds=dwell_time_seconds,
                region=region
            )
            persona, confidence = self.engine.infer_persona(session_id)

            record_id = self.db.insert_behavior_data({
                'session_id': session_id,
                'product_id': product_id,
                'category': category,
                'click_count': click_count,
                'dwell_time_seconds': dwell_time_seconds,
                'region': region,
                'inferred_persona': persona
            })

            profile = self.engine.get_session_profile(session_id)
            profile['record_id'] = record_id
            profile['confidence'] = confidence

            logger.info(
                f"📊 Etkileşim kaydedildi | Session: {session_id[:8]}... | "
                f"Ürün: {product_id} | Persona: {persona} | "
                f"Güven: {confidence:.2%}"
            )

            self._notify_callbacks(profile)
            return profile

    def track_click(self, session_id, product_id, category, region='yurtici'):
        """Tek bir ürün tıklamasını izle (kısa yol)"""
        return self.process_interaction(
            session_id=session_id,
            product_id=product_id,
            category=category,
            click_count=1,
            dwell_time_seconds=0,
            region=region
        )

    def track_dwell(self, session_id, product_id, category, dwell_time_seconds, region='yurtici'):
        """Sayfada kalma süresini izle"""
        return self.process_interaction(
            session_id=session_id,
            product_id=product_id,
            category=category,
            click_count=0,
            dwell_time_seconds=dwell_time_seconds,
            region=region
        )

    def get_dashboard_data(self, limit=50):
        """Panel için özet veri döndür"""
        return {
            'summary_stats': self.db.get_behavior_summary_stats(),
            'persona_distribution': self.db.get_behavior_persona_distribution(),
            'recent_activities': self.db.get_recent_behavior_with_personas(limit=limit)
        }

    def get_session_details(self, session_id):
        """Belirli bir oturumun detaylarını döndür"""
        records = self.db.get_behavior_by_session(session_id)
        profile = self.engine.get_session_profile(session_id)
        return {
            'session_profile': profile,
            'interaction_history': records
        }

    def start_background_simulation(self, interval_seconds=2, sessions_count=15):
        """Test/gerçek zamanlı demo için simüle edilmiş etkileşimler üret"""
        if self._simulation_running:
            return

        self._simulation_running = True
        sessions = [str(uuid.uuid4()) for _ in range(sessions_count)]

        def run_simulation():
            logger.info(f"🎯 Simülasyon başlatıldı: {sessions_count} oturum, {interval_seconds}s aralık")
            while self._simulation_running:
                try:
                    session_id = random.choice(sessions)
                    product_id = f"PRD-{random.randint(1000, 9999)}"
                    category = random.choice(CATEGORY_TYPES)
                    clicks = random.randint(1, 12)
                    dwell = random.randint(3, 180)
                    region = random.choice(['yurtici', 'yurtici', 'yurtici', 'yurtdisi'])

                    self.process_interaction(
                        session_id=session_id,
                        product_id=product_id,
                        category=category,
                        click_count=clicks,
                        dwell_time_seconds=dwell,
                        region=region
                    )
                    time.sleep(interval_seconds)
                except Exception as e:
                    logger.error(f"Simülasyon hatası: {e}")
                    time.sleep(interval_seconds)
            logger.info("⏹️ Simülasyon durduruldu")

        self._simulation_thread = threading.Thread(target=run_simulation, daemon=True)
        self._simulation_thread.start()

    def stop_background_simulation(self):
        """Simülasyonu durdur"""
        self._simulation_running = False
        if self._simulation_thread:
            self._simulation_thread.join(timeout=5)
        logger.info("⏹️ Simülasyon isteğiyle durduruldu")

    def start(self):
        """Ajanı başlat"""
        self.is_running = True
        logger.info("🚀 Behavioral & Persona AI Agent aktif")

    def stop(self):
        """Ajanı durdur"""
        self.stop_background_simulation()
        self.is_running = False
        logger.info("⏹️ Behavioral & Persona AI Agent durduruldu")


_global_persona_agent = None


def get_persona_agent():
    """Global singleton BehavioralPersonaAgent örneği döndür"""
    global _global_persona_agent
    if _global_persona_agent is None:
        _global_persona_agent = BehavioralPersonaAgent()
        _global_persona_agent.start()
    return _global_persona_agent


if __name__ == "__main__":
    print("=" * 60)
    print("Behavioral & Persona AI Agent - Test Modu")
    print("=" * 60)

    agent = get_persona_agent()

    print("\n[1/3] Manuel etkileşim testi...")
    session = str(uuid.uuid4())
    for i in range(5):
        result = agent.process_interaction(
            session_id=session,
            product_id=f"TEST-{i+1:03d}",
            category=random.choice(CATEGORY_TYPES),
            click_count=random.randint(1, 8),
            dwell_time_seconds=random.randint(5, 120),
            region='yurtici'
        )
        print(f"  -> {result['inferred_persona']} (Güven: {result['confidence']:.2%})")

    print("\n[2/3] Dashboard özeti...")
    dashboard = agent.get_dashboard_data(limit=10)
    summary = dashboard['summary_stats']
    print(f"  Toplam Kayıt: {summary['total_records']}")
    print(f"  Benzersiz Oturum: {summary['unique_sessions']}")
    print(f"  Toplam Tıklama: {summary['total_clicks']}")
    print(f"  Ort. Kalma: {summary['avg_dwell_time']}s")
    print(f"  Yurtiçi: {summary['yurtici_count']} | Yurtdışı: {summary['yurtdisi_count']}")
    print(f"  Persona Dağılımı:")
    for p in dashboard['persona_distribution']:
        print(f"    - {p['inferred_persona']}: {p['count']} kişi")

    print("\n[3/3] Oturum profili...")
    profile = agent.engine.get_session_profile(session)
    print(f"  Persona: {profile['inferred_persona']}")
    print(f"  Güven: {profile['confidence']:.2%}")
    print(f"  Toplam Etkileşim: {profile['total_interactions']}")
    print(f"  Ort. Kalma: {profile['avg_dwell_seconds']}s")

    print("\n" + "=" * 60)
    print("✅ Tüm testler başarılı")
    print("=" * 60)
