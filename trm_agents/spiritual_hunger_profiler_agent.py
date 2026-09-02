#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Spiritual Hunger Profiler Agent - Ruhsal Açlık Profilleyici Ajan
Versiyon: 1.0.0

Bu ajan kullanıcıların ruhsal açlıklarını psikolojik olarak analiz eder,
bunu küresel Social Commerce trendleriyle birleştirir ve
doğal, non-intrusive satış tetikleyicileri üretir.

Dosya: trm_agents/spiritual_hunger_profiler_agent.py
"""

import os
import sys
import json
import random
from datetime import datetime, time as dt_time
from typing import Dict, Any, Optional, List
from enum import Enum

# BaseAgent'ı import et
from .base_agent_template import BaseAgent

# ============================================
# ENUM SINIFLARI
# ============================================

class PsychologicalSegment(Enum):
    """Psikolojik Segmentasyon Sınıfları"""
    MATERIAL_NEED = "maddi_ihtiyac"
    EMOTIONAL_VOID = "duygusal_eksiklik"
    STATUS_SEEKING = "statu_arayisi"
    BELONGING_NEED = "aidiyet_arayisi"
    SATISFACTION_SEEKING = "tatmin_arayisi"

class ContentFormat(Enum):
    """İçerik Formatları"""
    TIKTOK_SHORT_VIDEO = "tiktok_short_video"
    REELS_STORY = "reels_story"
    LIVE_STREAM = "live_stream"
    MICRO_INFLUENCER_POST = "micro_influencer_post"
    FRIEND_RECOMMENDATION = "friend_recommendation"

# ============================================
# USER PERSONA MAP VERİ YAPISI
# ============================================

class UserPersonaMap:
    """Kullanıcı Kişilik Profili Haritası"""
    
    def __init__(self):
        self.user_id = None
        self.psychological_segment = None
        self.digital_footprint = {}
        self.personality_traits = {}
        self.spiritual_hunger_score = 0
        self.readiness_timestamp = None
        self.preferred_content_format = None
        self.impulse_buying_threshold = 0
        self.trust_factors = {}
    
    def to_dict(self) -> Dict[str, Any]:
        """Dict formatına dönüştür"""
        return {
            "user_id": self.user_id,
            "psychological_segment": self.psychological_segment.value if self.psychological_segment else None,
            "digital_footprint": self.digital_footprint,
            "personality_traits": self.personality_traits,
            "spiritual_hunger_score": self.spiritual_hunger_score,
            "readiness_timestamp": self.readiness_timestamp,
            "preferred_content_format": self.preferred_content_format.value if self.preferred_content_format else None,
            "impulse_buying_threshold": self.impulse_buying_threshold,
            "trust_factors": self.trust_factors
        }

# ============================================
# SPIRITUAL HUNGER PROFILER AGENT
# ============================================

class SpiritualHungerProfilerAgent(BaseAgent):
    """
    Ruhsal Açlık Profilleyici Ajan
    
    Bu ajan:
    - Kullanıcıların ruhsal açlıklarını analiz eder
    - Psikolojik segmentasyon yapar
    - Dijital izlerden kişilik profili çıkarır
    - Social Commerce trendlerini entegre eder
    - Non-intrusive timing engine kullanır
    - Doğal satış tetikleyicileri üretir
    """
    
    def __init__(self, agent_id: Optional[int] = None):
        super().__init__(
            agent_name="Spiritual Hunger Profiler Agent",
            agent_id=agent_id if agent_id else 167
        )
        
        # Ajan özel yapılandırmaları
        self.user_profiles = {}
        self.trend_data = {}
        self.timing_engine = TimingEngine()
        self.content_generator = ContentGenerator()
        self.psychological_analyzer = PsychologicalAnalyzer()
        
        # Mutlak Kapanış ve Nirvana Protokolü modülleri
        self.micro_budget_shield = MicroBudgetShield()
        self.retargeing_loop = RetargetingLoop()
        self.emotional_scarcity_engine = EmotionalScarcityEngine()
        self.zero_risk_bait_engine = ZeroRiskBaitEngine()
        
        # Social Commerce trendleri
        self.social_commerce_trends = {
            "frictionless_checkout": True,
            "tiktok_made_me_buy_it": True,
            "micro_influencer_trust": True,
            "live_shopping": True,
            "impulse_buying": True
        }
        
        self.log("🧠 Ruhsal Açlık Profilleyici Ajan başlatıldı", "INFO")
    
    # ============================================
    # ANA METODLAR (BaseAgent Override)
    # ============================================
    
    def run(self, **kwargs) -> Dict[str, Any]:
        """
        Ana çalıştırma metodu
        
        Args:
            **kwargs: Çalıştırma parametreleri
                - user_data: Kullanıcı verisi
                - digital_footprint: Dijital iz verisi
                - context: Bağlam bilgileri
        
        Returns:
            Analiz sonuçları ve öneriler
        """
        self.status = "running"
        self.log("🚀 Ruhsal açlık analizi başlatılıyor...", "INFO")
        
        try:
            # Kullanıcı verisini al
            user_data = kwargs.get('user_data', {})
            digital_footprint = kwargs.get('digital_footprint', {})
            context = kwargs.get('context', {})
            
            # 1. Psikolojik Segmentasyon
            segment = self.psychological_analyzer.analyze_segment(user_data, digital_footprint)
            
            # 2. Kişilik Profili Çıkarma
            persona_map = self._create_persona_map(user_data, digital_footprint, segment)
            
            # 3. Ruhsal Açlık Skoru Hesaplama
            hunger_score = self._calculate_spiritual_hunger(persona_map)
            
            # 4. Timing Analizi
            timing_result = self.timing_engine.analyze_readiness(persona_map, context)
            
            # 5. İçerik Önerisi
            content_recommendation = self.content_generator.generate_content(
                persona_map, 
                timing_result, 
                self.social_commerce_trends
            )
            
            # 6. Mutlak Kapanış ve Nirvana Protokolü Analizleri
            # Mikro-Bütçe Analizi
            user_budget = context.get('user_budget', 50)
            product_price = context.get('product_price', 100)
            budget_analysis = self.micro_budget_shield.generate_budget_alternatives(product_price, user_budget)
            
            # Retargeting Analizi
            conversion_status = context.get('conversion_status', False)
            retargeting_analysis = self.retargeing_loop.analyze_retry_strategy(
                user_data.get('user_id', 'unknown'),
                segment,
                conversion_status
            )
            
            # Kıtlık Analizi
            user_location = context.get('user_location', 'Türkiye')
            product_stock = context.get('product_stock', 5)
            scarcity_analysis = self.emotional_scarcity_engine.generate_scarcity_message(
                user_location,
                product_stock,
                context.get('time_remaining', 0)
            )
            
            # Sıfır Risk Analizi
            user_resistance = persona_map.impulse_buying_threshold
            zero_risk_analysis = self.zero_risk_bait_engine.generate_zero_risk_offer(
                user_resistance,
                product_price
            )
            
            # 7. Sonuçları birleştir
            result = {
                "analysis_timestamp": datetime.now().isoformat(),
                "psychological_segment": segment.value if segment else None,
                "persona_map": persona_map.to_dict(),
                "spiritual_hunger_score": hunger_score,
                "timing_analysis": timing_result,
                "content_recommendation": content_recommendation,
                "impulse_buying_probability": self._calculate_impulse_probability(persona_map, timing_result),
                "trust_score": self._calculate_trust_score(persona_map),
                # Mutlak Kapanış ve Nirvana Protokolü sonuçları
                "budget_analysis": budget_analysis,
                "retargeting_analysis": retargeting_analysis,
                "scarcity_analysis": scarcity_analysis,
                "zero_risk_analysis": zero_risk_analysis
            }
            
            # Sonucu kaydet
            self._save_analysis_result(result)
            
            self.status = "completed"
            self.log("✅ Ruhsal açlık analizi tamamlandı", "INFO")
            
            return result
            
        except Exception as e:
            self.status = "error"
            self.log(f"❌ Analiz hatası: {e}", "ERROR")
            raise
    
    def stop(self) -> None:
        """Ajanı durdurur"""
        self.status = "stopped"
        self.log("⏹️ Ruhsal Açlık Profilleyici Ajan durduruldu", "INFO")
    
    def restart(self) -> None:
        """Ajanı yeniden başlatır"""
        self.log("🔄 Ruhsal Açlık Profilleyici Ajan yeniden başlatılıyor...", "INFO")
        self.status = "restarting"
        # Reset state
        self.user_profiles = {}
        self.trend_data = {}
        self.status = "ready"
        self.log("✅ Yeniden başlatma tamamlandı", "INFO")
    
    # ============================================
    # PSİKOLOJİK ANALİZ METODLARI
    # ============================================
    
    def _create_persona_map(self, user_data: Dict, digital_footprint: Dict, segment: PsychologicalSegment) -> UserPersonaMap:
        """Kullanıcı kişilik profili haritası oluşturur"""
        persona = UserPersonaMap()
        persona.user_id = user_data.get('user_id', 'unknown')
        persona.psychological_segment = segment
        persona.digital_footprint = digital_footprint
        
        # Kişilik özelliklerini çıkarma
        persona.personality_traits = self._extract_personality_traits(digital_footprint)
        
        # Ruhsal açlık skoru
        persona.spiritual_hunger_score = self._calculate_spiritual_hunger(persona)
        
        # İçerik formatı tercihi
        persona.preferred_content_format = self._determine_content_format(persona)
        
        # Dürtüsel satış eşiği
        persona.impulse_buying_threshold = self._calculate_impulse_threshold(persona)
        
        # Güven faktörleri
        persona.trust_factors = self._calculate_trust_factors(persona)
        
        return persona
    
    def _extract_personality_traits(self, digital_footprint: Dict) -> Dict[str, Any]:
        """Dijital izlerden kişilik özelliklerini çıkarır"""
        traits = {
            "openness": 0,
            "conscientiousness": 0,
            "extraversion": 0,
            "agreeableness": 0,
            "neuroticism": 0
        }
        
        # Arama geçmişinden analiz
        search_history = digital_footprint.get('search_history', [])
        if search_history:
            # Açıklık: Yeni şeyler arama
            new_topics = len([s for s in search_history if 'new' in s.lower() or 'discover' in s.lower()])
            traits['openness'] = min(100, new_topics * 10)
            
            # Dışadönüklülük: Sosyal içerik arama
            social_searches = len([s for s in search_history if 'social' in s.lower() or 'friend' in s.lower()])
            traits['extraversion'] = min(100, social_searches * 15)
        
        # İzleme süresinden analiz
        watch_time = digital_footprint.get('watch_time', {})
        if watch_time:
            total_hours = sum(watch_time.values())
            # Dikkat süresi = Sorumluluk
            traits['conscientiousness'] = min(100, total_hours * 5)
        
        # Beğeni analizinden uyumluluk
        likes = digital_footprint.get('likes', [])
        if likes:
            positive_content = len([l for l in likes if 'positive' in l.lower()])
            traits['agreeableness'] = min(100, positive_content * 8)
        
        # Stres göstergeleri = Nörotizm
        stress_indicators = digital_footprint.get('stress_indicators', 0)
        traits['neuroticism'] = min(100, stress_indicators * 10)
        
        return traits
    
    def _calculate_spiritual_hunger(self, persona: UserPersonaMap) -> int:
        """Ruhsal açlık skorunu hesaplar (0-100)"""
        base_score = 50
        
        # Psikolojik segmente göre ayarlama
        if persona.psychological_segment == PsychologicalSegment.EMOTIONAL_VOID:
            base_score += 30
        elif persona.psychological_segment == PsychologicalSegment.BELONGING_NEED:
            base_score += 25
        elif persona.psychological_segment == PsychologicalSegment.STATUS_SEEKING:
            base_score += 20
        elif persona.psychological_segment == PsychologicalSegment.SATISFACTION_SEEKING:
            base_score += 15
        
        # Kişilik özelliklerine göre ayarlama
        neuroticism = persona.personality_traits.get('neuroticism', 0)
        base_score += (neuroticism * 0.3)
        
        openness = persona.personality_traits.get('openness', 0)
        base_score += (openness * 0.2)
        
        # Dijital izlerden ek puanlar
        loneliness_indicators = persona.digital_footprint.get('loneliness_indicators', 0)
        base_score += (loneliness_indicators * 5)
        
        return min(100, max(0, int(base_score)))
    
    def _determine_content_format(self, persona: UserPersonaMap) -> ContentFormat:
        """Kullanıcı için en uygun içerik formatını belirler"""
        extraversion = persona.personality_traits.get('extraversion', 0)
        openness = persona.personality_traits.get('openness', 0)
        
        if extraversion > 70 and openness > 60:
            return ContentFormat.LIVE_STREAM
        elif extraversion > 50:
            return ContentFormat.TIKTOK_SHORT_VIDEO
        elif openness > 60:
            return ContentFormat.REELS_STORY
        else:
            return ContentFormat.FRIEND_RECOMMENDATION
    
    def _calculate_impulse_threshold(self, persona: UserPersonaMap) -> int:
        """Dürtüsel satış eşiğini hesaplar (0-100)"""
        base_threshold = 50
        
        # Ruhsal açlık yüksekse eşik düşer
        if persona.spiritual_hunger_score > 70:
            base_threshold -= 20
        elif persona.spiritual_hunger_score > 50:
            base_threshold -= 10
        
        # Nörotizm yüksekse eşik düşer
        neuroticism = persona.personality_traits.get('neuroticism', 0)
        base_threshold -= (neuroticism * 0.2)
        
        # Sorumluluk yüksekse eşik yükselir
        conscientiousness = persona.personality_traits.get('conscientiousness', 0)
        base_threshold += (conscientiousness * 0.15)
        
        return min(100, max(0, int(base_threshold)))
    
    def _calculate_trust_factors(self, persona: UserPersonaMap) -> Dict[str, int]:
        """Güven faktörlerini hesaplar"""
        return {
            "micro_influencer_trust": 70 + random.randint(-10, 10),
            "friend_recommendation_trust": 85 + random.randint(-5, 5),
            "brand_trust": 50 + random.randint(-15, 15),
            "social_proof_trust": 65 + random.randint(-10, 10)
        }
    
    def _calculate_impulse_probability(self, persona: UserPersonaMap, timing_result: Dict) -> int:
        """Dürtüsel satış olasılığını hesaplar (0-100)"""
        base_probability = 30
        
        # Ruhsal açlık skoru
        base_probability += (persona.spiritual_hunger_score * 0.3)
        
        # Timing uygunluğu
        if timing_result.get('is_optimal', False):
            base_probability += 25
        
        # Dürtüsel satış eşiği (ters orantılı)
        threshold = persona.impulse_buying_threshold
        base_probability += ((100 - threshold) * 0.2)
        
        return min(100, max(0, int(base_probability)))
    
    def _calculate_trust_score(self, persona: UserPersonaMap) -> int:
        """Genel güven faktörünü hesaplar"""
        trust_factors = persona.trust_factors
        return int(sum(trust_factors.values()) / len(trust_factors))
    
    # ============================================
    # VERİ ALIŞVERİŞİ METODLARI
    # ============================================
    
    def sync_with_trend_agent(self, trend_data: Dict[str, Any]) -> None:
        """Trend talep avcısı ajanıyla veri senkronizasyonu"""
        self.trend_data = trend_data
        self.log("📊 Trend verileri senkronize edildi", "INFO")
    
    def get_user_profile(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Kullanıcı profilini döndürür"""
        return self.user_profiles.get(user_id)
    
    def _save_analysis_result(self, result: Dict[str, Any]) -> bool:
        """Analiz sonucunu kaydeder"""
        try:
            user_id = result.get('persona_map', {}).get('user_id', 'unknown')
            self.user_profiles[user_id] = result
            
            # Dosyaya da kaydet
            state_file = os.path.join(
                os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                "data",
                "spiritual_hunger_profiles.json"
            )
            
            os.makedirs(os.path.dirname(state_file), exist_ok=True)
            
            if os.path.exists(state_file):
                with open(state_file, 'r', encoding='utf-8') as f:
                    all_profiles = json.load(f)
            else:
                all_profiles = {}
            
            all_profiles[user_id] = result
            
            with open(state_file, 'w', encoding='utf-8') as f:
                json.dump(all_profiles, f, indent=4, ensure_ascii=False)
            
            return True
        except Exception as e:
            self.log(f"❌ Analiz sonucu kaydetme hatası: {e}", "ERROR")
            return False

# ============================================
# PSYCHOLOGICAL ANALYZER SINIFI
# ============================================

class PsychologicalAnalyzer:
    """Psikolojik Analiz Motoru"""
    
    def analyze_segment(self, user_data: Dict, digital_footprint: Dict) -> PsychologicalSegment:
        """Kullanıcıyı psikolojik segmente ayırır"""
        
        # Dijital izlerden sinyaller
        search_keywords = digital_footprint.get('search_history', [])
        likes = digital_footprint.get('likes', [])
        stress_level = digital_footprint.get('stress_indicators', 0)
        
        # Anahtar kelime analizi
        material_keywords = ['price', 'cheap', 'discount', 'deal', 'buy']
        emotional_keywords = ['lonely', 'sad', 'depressed', 'anxious', 'stress']
        status_keywords = ['luxury', 'premium', 'exclusive', 'vip', 'famous']
        belonging_keywords = ['community', 'group', 'friend', 'social', 'connect']
        satisfaction_keywords = ['happy', 'joy', 'fulfill', 'meaning', 'purpose']
        
        scores = {
            PsychologicalSegment.MATERIAL_NEED: 0,
            PsychologicalSegment.EMOTIONAL_VOID: 0,
            PsychologicalSegment.STATUS_SEEKING: 0,
            PsychologicalSegment.BELONGING_NEED: 0,
            PsychologicalSegment.SATISFACTION_SEEKING: 0
        }
        
        # Arama geçmişinden puanlama
        for search in search_keywords:
            search_lower = search.lower()
            for keyword in material_keywords:
                if keyword in search_lower:
                    scores[PsychologicalSegment.MATERIAL_NEED] += 2
            for keyword in emotional_keywords:
                if keyword in search_lower:
                    scores[PsychologicalSegment.EMOTIONAL_VOID] += 3
            for keyword in status_keywords:
                if keyword in search_lower:
                    scores[PsychologicalSegment.STATUS_SEEKING] += 2
            for keyword in belonging_keywords:
                if keyword in search_lower:
                    scores[PsychologicalSegment.BELONGING_NEED] += 2
            for keyword in satisfaction_keywords:
                if keyword in search_lower:
                    scores[PsychologicalSegment.SATISFACTION_SEEKING] += 2
        
        # Beğeni analizinden puanlama
        for like in likes:
            like_lower = like.lower()
            for keyword in emotional_keywords:
                if keyword in like_lower:
                    scores[PsychologicalSegment.EMOTIONAL_VOID] += 1
            for keyword in belonging_keywords:
                if keyword in like_lower:
                    scores[PsychologicalSegment.BELONGING_NEED] += 1
        
        # Stres seviyesi etkisi
        if stress_level > 5:
            scores[PsychologicalSegment.EMOTIONAL_VOID] += stress_level
        
        # En yüksek puanlı segmenti seç
        return max(scores, key=scores.get)

# ============================================
# TIMING ENGINE SINIFI
# ============================================

class TimingEngine:
    """Timing Motoru - Non-Intrusive Sunum Motoru"""
    
    def analyze_readiness(self, persona: UserPersonaMap, context: Dict) -> Dict[str, Any]:
        """Kullanıcının ruhsal hazırlığını analiz eder"""
        
        current_time = datetime.now().time()
        current_hour = datetime.now().hour
        
        # Optimal zamanlar
        optimal_hours = {
            "evening": (18, 22),  # Akşam 18-22
            "late_night": (22, 24),  # Gece 22-24
            "morning": (6, 9),  # Sabah 6-9
            "weekend": (10, 20)  # Hafta sonu 10-20
        }
        
        is_optimal = False
        optimal_reason = ""
        
        # Akşam saatleri (yalnızlık anları)
        if optimal_hours["evening"][0] <= current_hour <= optimal_hours["evening"][1]:
            is_optimal = True
            optimal_reason = "Akşam saatleri - yalnızlık ve rahatlama anı"
        
        # Gece geç saatler
        elif optimal_hours["late_night"][0] <= current_hour <= optimal_hours["late_night"][1]:
            is_optimal = True
            optimal_reason = "Gece geç saatler - duygusal hassasiyet yüksek"
        
        # Stres sonrası
        stress_level = context.get('stress_level', 0)
        if stress_level > 7:
            is_optimal = True
            optimal_reason = "Yüksek stres sonrası - rahatlama ihtiyacı"
        
        # Hafta sonu
        is_weekend = datetime.now().weekday() >= 5
        if is_weekend and optimal_hours["weekend"][0] <= current_hour <= optimal_hours["weekend"][1]:
            is_optimal = True
            optimal_reason = "Hafta sonu - boş zaman ve keşif isteği"
        
        return {
            "is_optimal": is_optimal,
            "optimal_reason": optimal_reason,
            "current_time": current_time.strftime("%H:%M:%S"),
            "current_hour": current_hour,
            "is_weekend": is_weekend,
            "readiness_score": 85 if is_optimal else 40,
            "recommended_delay": 0 if is_optimal else random.randint(30, 120)  # dakika
        }

# ============================================
# CONTENT GENERATOR SINIFI
# ============================================

class ContentGenerator:
    """İçerik Üretici Motoru"""
    
    def generate_content(self, persona: UserPersonaMap, timing_result: Dict, trends: Dict) -> Dict[str, Any]:
        """Kişiselleştirilmiş içerik önerisi üretir"""
        
        content_format = persona.preferred_content_format
        segment = persona.psychological_segment
        
        # İçerik dili (copywriting)
        copywriting_style = self._determine_copywriting_style(segment, content_format)
        
        # Ürün önerisi mantığı
        product_recommendation = self._generate_product_recommendation(persona, trends)
        
        # CTA (Call to Action) mesajı
        cta_message = self._generate_cta_message(segment, timing_result)
        
        # Güven sinyalleri
        trust_signals = self._generate_trust_signals(persona)
        
        return {
            "content_format": content_format.value if content_format else "general",
            "copywriting_style": copywriting_style,
            "product_recommendation": product_recommendation,
            "cta_message": cta_message,
            "trust_signals": trust_signals,
            "tone": self._determine_tone(segment),
            "length": self._determine_content_length(content_format),
            "frictionless_checkout": trends.get("frictionless_checkout", False),
            "tiktok_style": trends.get("tiktok_made_me_buy_it", False)
        }
    
    def _determine_copywriting_style(self, segment: PsychologicalSegment, content_format: ContentFormat) -> str:
        """Kopya yazım stilini belirler"""
        
        if content_format == ContentFormat.FRIEND_RECOMMENDATION:
            return "casual_friend"
        elif content_format == ContentFormat.MICRO_INFLUENCER_POST:
            return "authentic_influencer"
        elif content_format == ContentFormat.LIVE_STREAM:
            return "live_conversational"
        elif content_format == ContentFormat.TIKTOK_SHORT_VIDEO:
            return "trendy_fast_paced"
        else:
            return "emotional_storytelling"
    
    def _generate_product_recommendation(self, persona: UserPersonaMap, trends: Dict) -> Dict[str, Any]:
        """Ürün önerisi üretir"""
        
        segment = persona.psychological_segment
        
        # Segment bazlı ürün kategorileri
        product_categories = {
            PsychologicalSegment.EMOTIONAL_VOID: ["wellness", "self_care", "meditation", "comfort"],
            PsychologicalSegment.BELONGING_NEED: ["community_products", "social_experiences", "group_activities"],
            PsychologicalSegment.STATUS_SEEKING: ["luxury", "premium", "exclusive", "limited_edition"],
            PsychologicalSegment.SATISFACTION_SEEKING: ["hobby", "creative", "learning", "experiences"],
            PsychologicalSegment.MATERIAL_NEED: ["practical", "value", "essential", "utility"]
        }
        
        category = product_categories.get(segment, ["general"])
        selected_category = random.choice(category)
        
        return {
            "category": selected_category,
            "price_range": self._determine_price_range(segment),
            "urgency": "high" if persona.spiritual_hunger_score > 70 else "medium",
            "social_proof_enabled": True,
            "micro_influencer_endorsed": trends.get("micro_influencer_trust", False)
        }
    
    def _determine_price_range(self, segment: PsychologicalSegment) -> str:
        """Fiyat aralığını belirler"""
        if segment == PsychologicalSegment.STATUS_SEEKING:
            return "$100-$500"
        elif segment == PsychologicalSegment.SATISFACTION_SEEKING:
            return "$50-$200"
        elif segment == PsychologicalSegment.EMOTIONAL_VOID:
            return "$30-$100"
        else:
            return "$20-$100"
    
    def _generate_cta_message(self, segment: PsychologicalSegment, timing_result: Dict) -> str:
        """CTA mesajı üretir"""
        
        if timing_result.get('is_optimal', False):
            urgency_phrases = [
                "Şimdi keşfet",
                "Hemen deneyimle",
                "Kaçırma",
                "Bugün özel"
            ]
        else:
            urgency_phrases = [
                "Daha sonra bak",
                "İlginizi çekebilir",
                "Keşfetmeye değer"
            ]
        
        base_cta = random.choice(urgency_phrases)
        
        # Segment bazlı CTA
        if segment == PsychologicalSegment.EMOTIONAL_VOID:
            return f"{base_cta} - Kendine iyi bak"
        elif segment == PsychologicalSegment.BELONGING_NEED:
            return f"{base_cta} - Topluluğa katıl"
        elif segment == PsychologicalSegment.STATUS_SEEKING:
            return f"{base_cta} - Öne çık"
        else:
            return base_cta
    
    def _generate_trust_signals(self, persona: UserPersonaMap) -> List[str]:
        """Güven sinyalleri üretir"""
        
        signals = [
            "10,000+ mutlu müşteri",
            "4.9/5 yıldız değerlendirme",
            "30 gün iade garantisi"
        ]
        
        if persona.trust_factors.get('micro_influencer_trust', 0) > 70:
            signals.append("Favori influencerların tercihi")
        
        if persona.trust_factors.get('social_proof_trust', 0) > 70:
            signals.append("Sosyal medyada viral")
        
        return signals
    
    def _determine_tone(self, segment: PsychologicalSegment) -> str:
        """İçerik tonunu belirler"""
        
        tone_map = {
            PsychologicalSegment.EMOTIONAL_VOID: "empathetic_warm",
            PsychologicalSegment.BELONGING_NEED: "inclusive_friendly",
            PsychologicalSegment.STATUS_SEEKING: "aspirational_exciting",
            PsychologicalSegment.SATISFACTION_SEEKING: "inspiring_motivational",
            PsychologicalSegment.MATERIAL_NEED: "practical_reassuring"
        }
        
        return tone_map.get(segment, "neutral_balanced")
    
    def _determine_content_length(self, content_format: ContentFormat) -> str:
        """İçerik uzunluğunu belirler"""
        
        length_map = {
            ContentFormat.TIKTOK_SHORT_VIDEO: "15-60 seconds",
            ContentFormat.REELS_STORY: "30-90 seconds",
            ContentFormat.LIVE_STREAM: "5-30 minutes",
            ContentFormat.MICRO_INFLUENCER_POST: "1-3 minutes",
            ContentFormat.FRIEND_RECOMMENDATION: "30-60 seconds"
        }
        
        return length_map.get(content_format, "1-2 minutes")

# ============================================
# MUTLAK KAPANIŞ VE NIRVANA PROTOKOLÜ
# ============================================

class MicroBudgetShield:
    """Mikro-Bütçe Esnekliği & Nano-Bütçe Kalkanı"""
    
    def __init__(self):
        self.budget_tiers = {
            "nano": {"max_price": 5, "installment_options": [3, 6]},
            "micro": {"max_price": 20, "installment_options": [3, 6, 9]},
            "standard": {"max_price": 50, "installment_options": [3, 6, 9, 12]},
            "premium": {"max_price": 100, "installment_options": [6, 12, 18]}
        }
    
    def generate_budget_alternatives(self, original_price: float, user_budget: float) -> Dict[str, Any]:
        """Kullanıcı bütçesine uygun alternatifler üretir"""
        
        if original_price <= user_budget:
            return {
                "needs_alternative": False,
                "message": "Ürün bütçeniz dahilinde"
            }
        
        # Bütçe aşımı varsa alternatifler üret
        discount_percentage = int(((original_price - user_budget) / original_price) * 100)
        
        # %80 daha ucuz alternatif
        nano_price = original_price * 0.20
        
        # Taksit seçenekleri
        installment_plan = self._calculate_installments(user_budget)
        
        return {
            "needs_alternative": True,
            "original_price": original_price,
            "user_budget": user_budget,
            "discount_percentage": discount_percentage,
            "nano_alternative": {
                "price": round(nano_price, 2),
                "savings": f"%{discount_percentage}",
                "description": "Mikro-ürün alternatifi"
            },
            "installment_plan": installment_plan,
            "urgency_message": f"Bütçenizi aşmıyoruz! %80 indirimli mikro-ürün veya 3 taksit seçeneği"
        }
    
    def _calculate_installments(self, amount: float) -> Dict[str, Any]:
        """Taksit planı hesaplar"""
        return {
            "3_taksit": {
                "monthly_payment": round(amount / 3, 2),
                "total_interest": 0,
                "delay_option": "İlk ödeme ertelenebilir"
            },
            "6_taksit": {
                "monthly_payment": round(amount / 6, 2),
                "total_interest": round(amount * 0.05, 2),
                "delay_option": "İlk ödeme ertelenebilir"
            },
            "9_taksit": {
                "monthly_payment": round(amount / 9, 2),
                "total_interest": round(amount * 0.08, 2),
                "delay_option": "İlk ödeme ertelenebilir"
            }
        }

class RetargetingLoop:
    """Retargeting Loop (Dürtüsel Tetikleyici Döngüsü)"""
    
    def __init__(self):
        self.attempt_history = {}
        self.max_attempts = 3
        self.retry_intervals = {
            "first_retry": 2,  # saat
            "second_retry": 24,  # saat
            "final_retry": 72  # saat
        }
    
    def analyze_retry_strategy(self, user_id: str, previous_segment: PsychologicalSegment, conversion_status: bool) -> Dict[str, Any]:
        """Yeniden deneme stratejisi analiz eder"""
        
        if conversion_status:
            return {"needs_retry": False, "message": "Dönüşüm başarılı"}
        
        # Kullanıcı geçmişini kontrol et
        if user_id not in self.attempt_history:
            self.attempt_history[user_id] = {
                "attempts": 1,
                "last_attempt": datetime.now(),
                "segments": [previous_segment]
            }
            return {
                "needs_retry": True,
                "attempt_number": 1,
                "next_retry_in": self.retry_intervals["first_retry"],
                "strategy": "İlk temas - standart yaklaşım"
            }
        
        history = self.attempt_history[user_id]
        
        if history["attempts"] >= self.max_attempts:
            return {
                "needs_retry": False,
                "message": "Maksimum deneme sayısına ulaşıldı",
                "attempts": history["attempts"]
            }
        
        # Segment güncelleme
        new_segment = self._update_segment_based_on_failure(previous_segment, history["attempts"])
        history["attempts"] += 1
        history["last_attempt"] = datetime.now()
        history["segments"].append(new_segment)
        
        # Zamanlama belirle
        if history["attempts"] == 2:
            retry_hours = self.retry_intervals["first_retry"]
            timing_window = "gece saatleri (22:00-02:00)"
        elif history["attempts"] == 3:
            retry_hours = self.retry_intervals["second_retry"]
            timing_window = "hafta sonu akşamı"
        else:
            retry_hours = self.retry_intervals["final_retry"]
            timing_window = "stres sonrası anlar"
        
        return {
            "needs_retry": True,
            "attempt_number": history["attempts"],
            "next_retry_in": retry_hours,
            "timing_window": timing_window,
            "new_segment": new_segment.value,
            "strategy": self._get_retry_strategy(history["attempts"], new_segment)
        }
    
    def _update_segment_based_on_failure(self, current_segment: PsychologicalSegment, attempt_count: int) -> PsychologicalSegment:
        """Başarısızlığa göre segment günceller"""
        
        # İkinci deneme: Duygusal eksikliğe odaklan
        if attempt_count == 1:
            if current_segment != PsychologicalSegment.EMOTIONAL_VOID:
                return PsychologicalSegment.EMOTIONAL_VOID
        
        # Üçüncü deneme: Aidiyet arayışına odaklan
        elif attempt_count == 2:
            if current_segment != PsychologicalSegment.BELONGING_NEED:
                return PsychologicalSegment.BELONGING_NEED
        
        # Son deneme: Statü arayışı
        else:
            return PsychologicalSegment.STATUS_SEEKING
        
        return current_segment
    
    def _get_retry_strategy(self, attempt_count: int, segment: PsychologicalSegment) -> str:
        """Yeniden deneme stratejisi metni"""
        
        strategies = {
            1: "İlk temas - standart yaklaşım",
            2: "Duygusal yaklaşım - gece saatlerinde samimi mesaj",
            3: "Topluluk yaklaşımı - aidiyet vurgusu",
            4: "Statü yaklaşımı - fırsat kaçırma kurgusu"
        }
        
        return strategies.get(attempt_count, "Genel yaklaşım")

class EmotionalScarcityEngine:
    """Duygusal Kıtlık ve Özgür İradeyi Kuşatma Motoru"""
    
    def __init__(self):
        self.scarcity_triggers = {
            "geo_based": True,
            "time_based": True,
            "inventory_based": True,
            "social_proof_based": True
        }
    
    def generate_scarcity_message(self, user_location: str, product_stock: int, time_remaining: int = 0) -> Dict[str, Any]:
        """Kıtlık mesajı üretir"""
        
        scarcity_elements = []
        urgency_score = 0
        
        # Coğrafi bazlı kıtlık
        if self.scarcity_triggers["geo_based"]:
            geo_message = f"Sadece {user_location} bölgesinde son {random.randint(3, 7)} adet kaldı!"
            scarcity_elements.append({
                "type": "geo_scarcity",
                "message": geo_message,
                "urgency_boost": 25
            })
            urgency_score += 25
        
        # Stok bazlı kıtlık
        if product_stock < 10:
            stock_message = f"Tükeniyor! Sadece {product_stock} adet kaldı"
            scarcity_elements.append({
                "type": "stock_scarcity",
                "message": stock_message,
                "urgency_boost": 30
            })
            urgency_score += 30
        
        # Zaman bazlı kıtlık
        if time_remaining > 0:
            time_message = f"Teklif {time_remaining} saat sonra sona eriyor!"
            scarcity_elements.append({
                "type": "time_scarcity",
                "message": time_message,
                "urgency_boost": 35
            })
            urgency_score += 35
        
        # Sosyal kanıt bazlı kıtlık
        if self.scarcity_triggers["social_proof_based"]:
            watching_count = random.randint(15, 50)
            social_message = f"Şu anda {watching_count} kişi bu ürünü inceliyor"
            scarcity_elements.append({
                "type": "social_proof",
                "message": social_message,
                "urgency_boost": 20
            })
            urgency_score += 20
        
        # Ana kıtlık mesajı
        primary_message = self._generate_primary_scarcity_message(scarcity_elements)
        
        return {
            "urgency_score": min(100, urgency_score),
            "primary_message": primary_message,
            "scarcity_elements": scarcity_elements,
            "call_to_action": "Hemen almadan önce tükenebilir!",
            "free_will_pressure": "Bu fırsatı kaçırma, pişman olma"
        }
    
    def _generate_primary_scarcity_message(self, elements: List[Dict]) -> str:
        """Birincil kıtlık mesajı üretir"""
        
        if not elements:
            return "Son fırsat!"
        
        # En yüksek aciliyetli elementi seç
        primary = max(elements, key=lambda x: x["urgency_boost"])
        
        return primary["message"]

class ZeroRiskBaitEngine:
    """Sıfır Risk Bait (Önce Yaşa, Sonra Öde) Motoru"""
    
    def __init__(self):
        self.bait_types = {
            "free_trial": True,
            "sample_kit": True,
            "pay_later": True,
            "money_back": True
        }
    
    def generate_zero_risk_offer(self, user_resistance_score: int, product_price: float) -> Dict[str, Any]:
        """Sıfır risk teklifi üretir"""
        
        # Direnç skoru yüksekse daha agresif teklif
        if user_resistance_score > 70:
            return self._generate_aggressive_bait(product_price)
        elif user_resistance_score > 40:
            return self._generate_moderate_bait(product_price)
        else:
            return self._generate_standard_bait(product_price)
    
    def _generate_aggressive_bait(self, price: float) -> Dict[str, Any]:
        """Agresif sıfır risk teklifi"""
        
        return {
            "bait_type": "aggressive",
            "offer_title": "Tamamen Ücretsiz Deneme",
            "offer_details": {
                "trial_duration": "30 gün",
                "trial_cost": 0,
                "shipping": "Sadece kargo ücreti",
                "shipping_cost": "₺19.90",
                "commitment": "30 gün içinde memnun kalmazsanız hiçbir ödeme yapma",
                "auto_charge": "Memnun kaldığınızda otomatik ödeme"
            },
            "urgency_message": "Risk yok, sadece deneyin!",
            "conversion_hook": "Kart bilgilerinizi girin, 30 gün boyunca hiçbir çekim yapılmayacak"
        }
    
    def _generate_moderate_bait(self, price: float) -> Dict[str, Any]:
        """Orta seviye sıfır risk teklifi"""
        
        sample_price = price * 0.10
        
        return {
            "bait_type": "moderate",
            "offer_title": "Deneme Kiti",
            "offer_details": {
                "kit_price": round(sample_price, 2),
                "kit_contents": "Mini versiyon ürün",
                "shipping": "Ücretsiz kargo",
                "upgrade_option": f"Beğenirseniz tam versiyonu {price} TL'ye satın al",
                "satisfaction": "Memnun kalmazsanız para iadesi"
            },
            "urgency_message": "Küçük bir yatırımla deneyin",
            "conversion_hook": "Sadece {sample_price} TL ile deneyin, beğenmezseniz kaybetmezsiniz"
        }
    
    def _generate_standard_bait(self, price: float) -> Dict[str, Any]:
        """Standart sıfır risk teklifi"""
        
        return {
            "bait_type": "standard",
            "offer_title": "İade Garantisi",
            "offer_details": {
                "money_back_period": "14 gün",
                "return_condition": "Kullanılmamış ürün",
                "refund_process": "Otomatik iade",
                "customer_support": "7/24 destek"
            },
            "urgency_message": "Risk yok, iade garantisi",
            "conversion_hook": "Beğenmezseniz 14 gün içinde koşulsuz iade"
        }

# ==========================================
# MAIN TEST
# ==========================================

if __name__ == "__main__":
    # Test için örnek veri
    agent = SpiritualHungerProfilerAgent(agent_id=167)
    
    # Örnek kullanıcı verisi
    user_data = {
        "user_id": "test_user_001",
        "age": 28,
        "gender": "female"
    }
    
    # Örnek dijital iz
    digital_footprint = {
        "search_history": [
            "how to feel less lonely",
            "best meditation apps",
            "self care products",
            "community activities near me"
        ],
        "watch_time": {
            "wellness_content": 5.5,
            "social_content": 3.2
        },
        "likes": [
            "positive affirmations",
            "community building",
            "self improvement"
        ],
        "stress_indicators": 8,
        "loneliness_indicators": 6
    }
    
    # Bağlam
    context = {
        "stress_level": 7,
        "time_of_day": "evening",
        "device_type": "mobile"
    }
    
    # Analizi çalıştır
    result = agent.run(
        user_data=user_data,
        digital_footprint=digital_footprint,
        context=context
    )
    
    print("🧠 RUHSAL AÇLIK PROFİLİZ SONUCU:")
    print(json.dumps(result, indent=2, ensure_ascii=False))
