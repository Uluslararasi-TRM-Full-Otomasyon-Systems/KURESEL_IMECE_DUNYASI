#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fiyatsızlaştırma Ajanı
Sosyal medya için fiyat odaklı olmayan, değer ve hikaye odaklı içerik üreticisi
"""

import os
import sys
import json
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime
import random

# BaseAgent'ı import et
from .base_agent_template import BaseAgent

logger = logging.getLogger(__name__)

class FiyatsizlastirAjani(BaseAgent):
    """
    Fiyatsızlaştırma Ajanı
    
    Bu ajan:
    - Ticari ürün verilerini analiz eder
    - Fiyat odaklı olmayan içerikler üretir
    - Değer, karizma ve hikaye odaklı senaryolar oluşturur
    - Sosyal medya platformları için optimize edilmiş çıktılar verir
    """
    
    def __init__(self, agent_id: Optional[int] = None):
        super().__init__(
            agent_name="Fiyatsızlaştırma Ajanı",
            agent_id=agent_id if agent_id else 169
        )
        
        # İçerik şablonları ve motorlar
        self.hook_generator = HookGenerator()
        self.story_engine = StoryEngine()
        self.charisma_tone = CharismaToneEngine()
        self.value_copywriter = ValueCopywriter()
        
        # Ürün veritabanı
        self.product_cache = {}
        self.content_history = []
        
        self.log("🎭 Fiyatsızlaştırma Ajanı başlatıldı", "INFO")
    
    # ============================================
    # ANA METODLAR (BaseAgent Override)
    # ============================================
    
    def run(self, **kwargs) -> Dict[str, Any]:
        """
        Ana çalıştırma metodu
        
        Args:
            **kwargs: Çalıştırma parametreleri
                - product_data: Ürün verisi
                - platform: Hedef platform (tiktok, reels, shorts)
                - tone: İçerik tonu (luxury, casual, professional)
        
        Returns:
            Video senaryosu ve değer odaklı metin
        """
        self.status = "running"
        self.log("🎬 Fiyatsızlaştırma analizi başlatılıyor...", "INFO")
        
        try:
            # Ürün verisini al
            product_data = kwargs.get('product_data', {})
            platform = kwargs.get('platform', 'tiktok')
            tone = kwargs.get('tone', 'luxury')
            
            # 1. Ürün analizi
            analyzed_product = self._analyze_product(product_data)
            
            # 2. Kanca cümlesi üret
            hook = self.hook_generator.generate_epic_hook(analyzed_product, platform)
            
            # 3. Hikayeleştirme
            story = self.story_engine.craft_product_story(analyzed_product, tone)
            
            # 4. Karizma tonu
            charisma_content = self.charisma_tone.apply_charisma_tone(hook, story, tone)
            
            # 5. Video senaryosu oluştur
            video_scenario = self._create_video_scenario(charisma_content, platform, analyzed_product)
            
            # 6. Değer odaklı paylaşım metni
            value_post = self.value_copywriter.create_value_post(analyzed_product, tone)
            
            # 7. Sonuçları birleştir
            result = {
                "analysis_timestamp": datetime.now().isoformat(),
                "product_data": analyzed_product,
                "platform": platform,
                "tone": tone,
                "video_scenario": video_scenario,
                "value_post": value_post,
                "content_quality_score": self._calculate_quality_score(video_scenario, value_post),
                "platform_optimization": self._get_platform_optimization(platform)
            }
            
            # Sonucu kaydet
            self._save_content_result(result)
            
            self.status = "completed"
            self.log("✅ Fiyatsızlaştırma analizi tamamlandı", "INFO")
            
            return result
            
        except Exception as e:
            self.status = "error"
            self.log(f"❌ Fiyatsızlaştırma analizi hatası: {e}", "ERROR")
            raise
    
    def stop(self) -> None:
        """Ajanı durdurur"""
        self.status = "stopped"
        self.log("⏹️ Fiyatsızlaştırma Ajanı durduruldu", "INFO")
    
    def restart(self) -> None:
        """Ajanı yeniden başlatır"""
        self.log("🔄 Fiyatsızlaştırma Ajanı yeniden başlatılıyor...", "INFO")
        self.status = "restarting"
        self.product_cache = {}
        self.content_history = []
        self.status = "ready"
        self.log("✅ Yeniden başlatma tamamlandı", "INFO")
    
    # ============================================
    # ÖZEL ANALİZ METODLARI
    # ============================================
    
    def _analyze_product(self, product_data: Dict[str, Any]) -> Dict[str, Any]:
        """Ürün verisini analiz eder"""
        
        analyzed = {
            "original_data": product_data,
            "name": product_data.get("name", "Bilinmeyen Ürün"),
            "category": product_data.get("category", "general"),
            "key_features": product_data.get("features", []),
            "materials": product_data.get("materials", []),
            "craftsmanship": product_data.get("craftsmanship", "standard"),
            "target_audience": product_data.get("target_audience", "general"),
            "unique_value": product_data.get("unique_value", "quality"),
            "price": product_data.get("price", 0),  # Sadece analiz için
            "analysis_timestamp": datetime.now().isoformat()
        }
        
        # Ürünün değer unsurlarını belirle
        analyzed["value_elements"] = self._extract_value_elements(analyzed)
        
        return analyzed
    
    def _extract_value_elements(self, product: Dict[str, Any]) -> List[str]:
        """Ürünün değer unsurlarını çıkarır"""
        
        value_elements = []
        
        # Malzemeler
        materials = product.get("materials", [])
        if materials:
            value_elements.append(f"Premium malzemeler: {', '.join(materials)}")
        
        # İşçilik
        craftsmanship = product.get("craftsmanship", "standard")
        if craftsmanship != "standard":
            value_elements.append(f"Özel işçilik: {craftsmanship}")
        
        # Özellikler
        features = product.get("key_features", [])
        if features:
            value_elements.append(f"Özellikler: {', '.join(features[:3])}")
        
        # Kategori bazlı değerler
        category = product.get("category", "general")
        category_values = {
            "electronics": ["Teknolojik mükemmellik", "Yenilikçi tasarım"],
            "fashion": ["Zarif detaylar", "Özgün stil"],
            "wellness": ["Doğal içerikler", "Holistik yaklaşım"],
            "luxury": ["Eksiksiz kalite", "Prestijli tasarım"]
        }
        
        if category in category_values:
            value_elements.extend(category_values[category])
        
        return value_elements
    
    def _create_video_scenario(self, charisma_content: Dict[str, str], platform: str, product: Dict[str, Any]) -> Dict[str, Any]:
        """Video senaryosu oluşturur"""
        
        scenario = {
            "platform": platform,
            "duration": self._get_platform_duration(platform),
            "hook": charisma_content["hook"],
            "voiceover": charisma_content["story"],
            "visual_direction": self._generate_visual_direction(product, platform),
            "audio_suggestion": self._suggest_audio(product, platform),
            "text_overlays": self._create_text_overlays(charisma_content, platform),
            "call_to_action": self._create_value_cta(product),
            "price_mention": self._create_subtle_price_mention(product),
            "platform_specific_tips": self._get_platform_tips(platform)
        }
        
        return scenario
    
    def _get_platform_duration(self, platform: str) -> str:
        """Platforma göre süre belirler"""
        durations = {
            "tiktok": "15-60 seconds",
            "reels": "30-90 seconds",
            "shorts": "30-60 seconds"
        }
        return durations.get(platform, "30-60 seconds")
    
    def _generate_visual_direction(self, product: Dict[str, Any], platform: str) -> List[str]:
        """Görsel yönlendirme üretir"""
        
        visuals = []
        
        # Ürün kategorisine göre görsel önerileri
        category = product.get("category", "general")
        
        if category == "electronics":
            visuals = [
                "Yavaş çekimde ürün detayları",
                "Teknolojik özelliklerin vurgulanması",
                "Kullanım senaryoları",
                "Şık, minimalist arka plan"
            ]
        elif category == "fashion":
            visuals = [
                "Model üzerinde ürün gösterimi",
                "Kumaş dokusunun yakın çekimi",
                "Stil kombinasyonları",
                "Lüks atmosfer"
            ]
        elif category == "wellness":
            visuals = [
                "Doğal ışıkta ürün",
                "Rahatlatıcı atmosfer",
                "Kullanım deneyimi",
                "Organik dokular"
            ]
        else:
            visuals = [
                "Ürünün en iyi açısı",
                "Detay odaklı çekimler",
                "Kalite vurgusu",
                "Profesyonel aydınlatma"
            ]
        
        # Platforma özel görsel önerileri
        if platform == "tiktok":
            visuals.append("Hızlı geçişler ve dinamik kurgu")
        elif platform == "reels":
            visuals.append("Estetik ve akıcı geçişler")
        elif platform == "shorts":
            visuals.append("Net ve odaklı çekimler")
        
        return visuals
    
    def _suggest_audio(self, product: Dict[str, Any], platform: str) -> Dict[str, str]:
        """Ses önerileri üretir"""
        
        category = product.get("category", "general")
        
        audio_suggestions = {
            "electronics": {
                "music_style": "Modern, teknolojik",
                "tempo": "Orta hız",
                "mood": "Yenilikçi ve güçlü"
            },
            "fashion": {
                "music_style": "Trend, sofistike",
                "tempo": "Orta hız",
                "mood": "Şık ve zarif"
            },
            "wellness": {
                "music_style": "Rahatlatıcı, doğal",
                "tempo": "Yavaş",
                "mood": "Huzurlu ve dengeli"
            },
            "luxury": {
                "music_style": "Klasik, prestijli",
                "tempo": "Yavaş",
                "mood": "Lüks ve etkileyici"
            }
        }
        
        return audio_suggestions.get(category, {
            "music_style": "Genel amaçlı",
            "tempo": "Orta hız",
            "mood": "Profesyonel"
        })
    
    def _create_text_overlays(self, charisma_content: Dict[str, str], platform: str) -> List[str]:
        """Metin katmanları oluşturur"""
        
        overlays = []
        
        # Kanca cümlesi
        hook = charisma_content.get("hook", "")
        if hook:
            overlays.append(hook[:50])  # İlk 50 karakter
        
        # Değer vurguları
        value_phrases = [
            "Mükemmel Kalite",
            "Özgün Tasarım",
            "Premium Deneyim",
            "Sanatsal İşçilik"
        ]
        
        overlays.extend(random.sample(value_phrases, 2))
        
        return overlays
    
    def _create_value_cta(self, product: Dict[str, Any]) -> str:
        """Değer odaklı CTA oluşturur"""
        
        ctas = [
            "Kaliteyi deneyimle",
            "Mükemmelliği keşfet",
            "Standartlarını yükselt",
            "Farkı hisset",
            "Premium deneyim yaşa"
        ]
        
        return random.choice(ctas)
    
    def _create_subtle_price_mention(self, product: Dict[str, Any]) -> str:
        """Önemsiz fiyat bahsi oluşturur"""
        
        price = product.get("price", 0)
        
        if price == 0:
            return ""
        
        return f"*Fiyat bilgisi için detaylar kısmını inceleyebilirsiniz"
    
    def _get_platform_tips(self, platform: str) -> List[str]:
        """Platform ipuçları verir"""
        
        tips = {
            "tiktok": [
                "İlk 3 saniye kritik",
                "Hızlı geçişler kullan",
                "Trend sesleri kullan",
                "Hashtag stratejisi önemli"
            ],
            "reels": [
                "Estetik görseller kullan",
                "Akışkan geçişler",
                "Instagram müzik kütüphanesi",
                "Hikaye anlatımı güçlü olmalı"
            ],
            "shorts": [
                "Net ve odaklı içerik",
                "YouTube algoritması uyumu",
                "Kısa ve etkili mesaj",
                "Thumbnail stratejisi"
            ]
        }
        
        return tips.get(platform, ["Kalite içerik üret", "İzleyici etkileşimi sağla"])
    
    def _calculate_quality_score(self, video_scenario: Dict[str, Any], value_post: Dict[str, Any]) -> float:
        """İçerik kalite skoru hesaplar"""
        
        score = 0.0
        
        # Video senaryo kalitesi
        if video_scenario.get("hook"):
            score += 25
        if video_scenario.get("voiceover"):
            score += 25
        if len(video_scenario.get("visual_direction", [])) > 0:
            score += 15
        
        # Değer post kalitesi
        if value_post.get("headline"):
            score += 20
        if value_post.get("body"):
            score += 15
        
        return min(100, score)
    
    def _get_platform_optimization(self, platform: str) -> Dict[str, Any]:
        """Platform optimizasyon bilgileri verir"""
        
        optimizations = {
            "tiktok": {
                "aspect_ratio": "9:16",
                "max_duration": "60s",
                "audio_source": "TikTok library",
                "hashtag_limit": 5
            },
            "reels": {
                "aspect_ratio": "9:16",
                "max_duration": "90s",
                "audio_source": "Instagram library",
                "hashtag_limit": 30
            },
            "shorts": {
                "aspect_ratio": "9:16",
                "max_duration": "60s",
                "audio_source": "YouTube library",
                "hashtag_limit": 15
            }
        }
        
        return optimizations.get(platform, {
            "aspect_ratio": "9:16",
            "max_duration": "60s",
            "audio_source": "Platform library",
            "hashtag_limit": 10
        })
    
    def _save_content_result(self, result: Dict[str, Any]) -> bool:
        """İçerik sonucunu kaydeder"""
        try:
            self.content_history.append(result)
            
            # Dosyaya da kaydet
            state_file = os.path.join(
                os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                "data",
                "fiyatsizlastirma_content.json"
            )
            
            os.makedirs(os.path.dirname(state_file), exist_ok=True)
            
            with open(state_file, 'w', encoding='utf-8') as f:
                json.dump(result, f, indent=4, ensure_ascii=False)
            
            return True
        except Exception as e:
            self.log(f"❌ İçerik kaydetme hatası: {e}", "ERROR")
            return False
    
    def get_content_history(self) -> List[Dict[str, Any]]:
        """İçerik geçmişini döndürür"""
        return self.content_history


# ============================================
# YARDIMCI MOTOR SINIFLARI
# ============================================

class HookGenerator:
    """Vurucu kanca cümleleri üretir"""
    
    def generate_epic_hook(self, product: Dict[str, Any], platform: str) -> str:
        """Epik kanca cümlesi üretir"""
        
        hooks = {
            "electronics": [
                "Teknolojinin zirvesine hoş geldiniz",
                "Sıradan cihazları unutun",
                "Mükemmellik standartları değişiyor",
                "Gelecek şimdi elinizde"
            ],
            "fashion": [
                "Stilin yeni dili burada",
                "Sıradan giyimi geride bırakın",
                "Zarafetin tanımını yeniden yazıyoruz",
                "Kendinizi ifade etmenin en şık yolu"
            ],
            "wellness": [
                "Huzurun ve dengeyin kaynağı",
                "Kendinize yatırımın en değerli hali",
                "Doğanın gücünü keşfedin",
                "Bütünsel iyilik yolculuğu"
            ],
            "luxury": [
                "Mükemmelliğin tanımı burada",
                "Prestijin yeni adresi",
                "Sıradanlığın ötesinde bir deneyim",
                "Lüksün en saf hali"
            ],
            "general": [
                "Kaliteyi yeniden tanımlıyoruz",
                "Standartlarınızı yükseltin",
                "Mükemmelliği deneyimleyin",
                "Farkı hissedin"
            ]
        }
        
        category = product.get("category", "general")
        category_hooks = hooks.get(category, hooks["general"])
        
        return random.choice(category_hooks)


class StoryEngine:
    """Hikaye oluşturma motoru"""
    
    def craft_product_story(self, product: Dict[str, Any], tone: str) -> str:
        """Ürün hikayesi oluşturur"""
        
        category = product.get("category", "general")
        materials = product.get("materials", [])
        craftsmanship = product.get("craftsmanship", "standard")
        
        story_templates = {
            "electronics": f"Her detayı mühendislik mükemmelliğiyle tasarlandı. {', '.join(materials[:2]) if materials else 'Premium malzemeler'} kullanılarak, {craftsmanship} işçilik ile üretildi. Bu sadece bir cihaz değil, teknoloji sanatı.",
            "fashion": f"Her dikişte zarafet, her kumaşta kalite var. {', '.join(materials[:2]) if materials else 'Özel seçilmiş kumaşlar'} ile {craftsmanship} işçilikle hayata geçirildi. Sıradan giyimin ötesinde, kişisel stil ifadesi.",
            "wellness": f"Doğanın en saf elementleri, bilimsel yaklaşımla birleşti. {', '.join(materials[:2]) if materials else 'Organik içerikler'} kullanılarak, {craftsmanship} standartlarda üretildi. Vücudunuzun hak ettiği iyilik.",
            "luxury": f"Zanaatkarların elinden çıkan her parça, bir sanat eseri. {', '.join(materials[:2]) if materials else 'Nadir malzemeler'} ile {craftsmanship} işçilikte üretildi. Sıradanlığın ötesinde, prestijli bir deneyim.",
            "general": f"Kalite ve özenin her aşamasında var. {', '.join(materials[:2]) if materials else 'Seçkin malzemeler'} ile {craftsmanship} işçilikte üretildi. Mükemmelliği deneyenler için."
        }
        
        base_story = story_templates.get(category, story_templates["general"])
        
        # Tona göre hikayeyi şekillendir
        if tone == "luxury":
            return f"✨ {base_story} Bu, sadece bir ürün değil, bir yaşam tarzı ifadesi."
        elif tone == "casual":
            return f"💫 {base_story} Kaliteyi hissedin, farkı yaşayın."
        else:  # professional
            return f"🎯 {base_story} Profesyonel standartlarda, güvenilir kalite."


class CharismaToneEngine:
    """Karizma tonu motoru"""
    
    def apply_charisma_tone(self, hook: str, story: str, tone: str) -> Dict[str, str]:
        """Karizma tonunu uygular"""
        
        tone_modifiers = {
            "luxury": {
                "prefix": "Değerli izleyicilerimiz, ",
                "suffix": " Mükemmellik sizin için.",
                "style": "sofistike"
            },
            "casual": {
                "prefix": "Arkadaşlar, ",
                "suffix": " Kaliteyi hissedin.",
                "style": "samimi"
            },
            "professional": {
                "prefix": "Sayın müşterilerimiz, ",
                "suffix": " Güvenilir kalite.",
                "style": "profesyonel"
            }
        }
        
        modifier = tone_modifiers.get(tone, tone_modifiers["professional"])
        
        return {
            "hook": f"{modifier['prefix']}{hook}",
            "story": f"{story}{modifier['suffix']}",
            "tone_style": modifier["style"]
        }


class ValueCopywriter:
    """Değer odaklı metin yazarı"""
    
    def create_value_post(self, product: Dict[str, Any], tone: str) -> Dict[str, str]:
        """Değer odaklı paylaşım metni oluşturur"""
        
        category = product.get("category", "general")
        value_elements = product.get("value_elements", [])
        
        # Başlık
        headlines = {
            "electronics": "Teknolojik Mükemmellik",
            "fashion": "Zarif Stil İfadesi",
            "wellness": "Bütünsel İyilik",
            "luxury": "Prestijli Deneyim",
            "general": "Kalite ve Özen"
        }
        
        headline = headlines.get(category, headlines["general"])
        
        # Gövde metni
        body_parts = []
        
        # Değer unsurlarını ekle
        for element in value_elements[:3]:
            body_parts.append(f"• {element}")
        
        # Kategoriye özel mesajlar
        category_messages = {
            "electronics": "Her detay mühendislik mükemmelliğiyle tasarlandı.",
            "fashion": "Her dikişte zarafet, her kumaşta kalite var.",
            "wellness": "Doğanın gücü, bilimsel yaklaşım.",
            "luxury": "Zanaatkarların elinden çıkan sanat eserleri.",
            "general": "Kalite ve özenin her aşamasında."
        }
        
        body_parts.append(f"\n{category_messages.get(category, category_messages['general'])}")
        
        # Tona göre mesaj
        tone_messages = {
            "luxury": "\n✨ Mükemmelliği sevenler için.",
            "casual": "\n💫 Kaliteyi hissedin.",
            "professional": "\n🎯 Güvenilir standartlarda."
        }
        
        body_parts.append(tone_messages.get(tone, tone_messages["professional"]))
        
        # Önemsiz fiyat bahsi
        price = product.get("price", 0)
        if price > 0:
            body_parts.append(f"\n\n*Fiyat bilgisi ve detaylar için profilimizi inceleyebilirsiniz.")
        
        return {
            "headline": headline,
            "body": "\n".join(body_parts),
            "hashtags": self._generate_value_hashtags(category),
            "tone": tone
        }
    
    def _generate_value_hashtags(self, category: str) -> List[str]:
        """Değer odaklı hashtag'ler üretir"""
        
        base_tags = ["#kalite", "#mükemmellik", "#değer", "#premium"]
        
        category_tags = {
            "electronics": ["#teknoloji", "#yenilik", "#mühendislik"],
            "fashion": ["#stil", "#zarafet", "#moda"],
            "wellness": ["#iyilik", "#denge", "#doğal"],
            "luxury": ["#lüks", "#prestij", "#sanat"],
            "general": ["#kalite", "#güvenilir", "#özen"]
        }
        
        tags = base_tags + category_tags.get(category, category_tags["general"])
        
        return tags[:8]  # Maksimum 8 hashtag


# Test çalıştırması
if __name__ == "__main__":
    agent = FiyatsizlastirAjani(agent_id=169)
    
    # Test ürün verisi
    test_product = {
        "name": "Premium Akıllı Saat",
        "category": "electronics",
        "features": ["Kalp atışı izleme", "GPS takibi", "Su geçirmez", "7 gün pil ömrü"],
        "materials": ["Titanyum kasa", "Safir kristal cam", "Deri kayış"],
        "craftsmanship": "el işçiliği",
        "target_audience": "premium",
        "unique_value": "teknolojik mükemmellik",
        "price": 15000
    }
    
    # Analizi çalıştır
    result = agent.run(
        product_data=test_product,
        platform="tiktok",
        tone="luxury"
    )
    
    print("🎭 FİYATSIZLAŞTIRMA ANALİZ SONUCU:")
    print(json.dumps(result, indent=2, ensure_ascii=False))
