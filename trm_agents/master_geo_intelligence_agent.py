#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Master Geo Intelligence Agent
Tüm coğrafi istihbarat araçlarını tek bir çatı altında birleştiren master agent
"""

import os
import sys
import json
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime

# BaseAgent'ı import et
from .base_agent_template import BaseAgent

# Coğrafi entegrasyon modüllerini import et
from .hoodmaps_integration import HoodmapsIntegration
from .geospy_integration import GeoSpyIntegration
from .endeksa_integration import EndeksaIntegration
from .ultimate_web_scraper import UltimateWebScraper
from .withraven_integration import WithRavenIntegration

logger = logging.getLogger(__name__)

class MasterGeoIntelligenceAgent(BaseAgent):
    """
    Master Coğrafi İstihbarat Ajanı
    
    Bu ajan:
    - Hoodmaps, GeoSpy, Endeksa entegrasyonlarını yönetir
    - Ultimate Web Scraper ile veri toplar
    - WithRaven ile derin öğrenme analizi yapar
    - Tüm coğrafi verileri tek bir çatı altında birleştirir
    - Karar destek sistemi sağlar
    """
    
    def __init__(self, agent_id: Optional[int] = None):
        super().__init__(
            agent_name="Master Geo Intelligence Agent",
            agent_id=agent_id if agent_id else 168
        )
        
        # Coğrafi entegrasyon modülleri
        self.hoodmaps = HoodmapsIntegration()
        self.geospy = GeoSpyIntegration()
        self.endeksa = EndeksaIntegration()
        self.web_scraper = UltimateWebScraper()
        self.withraven = WithRavenIntegration()
        
        # Veri depolama
        self.geo_intelligence_cache = {}
        self.analysis_history = []
        
        self.log("🌍 Master Coğrafi İstihbarat Ajanı başlatıldı", "INFO")
    
    # ============================================
    # ANA METODLAR (BaseAgent Override)
    # ============================================
    
    def run(self, **kwargs) -> Dict[str, Any]:
        """
        Ana çalıştırma metodu
        
        Args:
            **kwargs: Çalıştırma parametreleri
                - target_location: Hedef konum
                - product_category: Ürün kategorisi
                - analysis_type: Analiz tipi (comprehensive, demographic, luxury, general)
        
        Returns:
            Kapsamlı coğrafi istihbarat analizi
        """
        self.status = "running"
        self.log("🚀 Coğrafi istihbarat analizi başlatılıyor...", "INFO")
        
        try:
            # Parametreleri al
            target_location = kwargs.get('target_location', 'Istanbul')
            product_category = kwargs.get('product_category', 'general')
            analysis_type = kwargs.get('analysis_type', 'comprehensive')
            
            # 1. Hoodmaps Mahalle Analizi
            hoodmaps_data = self.hoodmaps.analyze_target_audience(target_location, product_category)
            
            # 2. GeoSpy Konum İstihbaratı
            geospy_data = self.geospy.get_location_intelligence(target_location)
            
            # 3. Endeksa Lüks Bölge Analizi (Türkiye için)
            endeksa_data = {}
            if "Turkey" in target_location or "Türkiye" in target_location or "Istanbul" in target_location:
                endeksa_data = self.endeksa.get_premium_districts(target_location)
            
            # 4. Web Scraping (varsa hedef URL'ler)
            web_data = {}
            target_urls = kwargs.get('target_urls', [])
            if target_urls:
                web_data = self.web_scraper.batch_scrape(target_urls, "demographic")
            
            # 5. WithRaven Derin Öğrenme Analizi
            combined_geo_data = {
                "hoodmaps": hoodmaps_data,
                "geospy": geospy_data,
                "endeksa": endeksa_data,
                "web_data": web_data
            }
            
            withraven_analysis = self.withraven.process_geographic_data(combined_geo_data)
            
            # 6. Karar Destek Sistemi
            decision_support = self.withraven.generate_decision_support(combined_geo_data)
            
            # 7. Kapsamlı Analiz Sonucu
            comprehensive_result = {
                "analysis_timestamp": datetime.now().isoformat(),
                "target_location": target_location,
                "product_category": product_category,
                "analysis_type": analysis_type,
                "hoodmaps_analysis": hoodmaps_data,
                "geospy_analysis": geospy_data,
                "endeksa_analysis": endeksa_data,
                "web_scraping_data": web_data,
                "withraven_processing": withraven_analysis,
                "decision_support": decision_support,
                "overall_intelligence_score": self._calculate_intelligence_score(
                    hoodmaps_data, geospy_data, endeksa_data, withraven_analysis
                ),
                "strategic_recommendations": self._generate_strategic_recommendations(
                    combined_geo_data, decision_support
                )
            }
            
            # Sonucu kaydet
            self._save_analysis_result(comprehensive_result)
            
            self.status = "completed"
            self.log("✅ Coğrafi istihbarat analizi tamamlandı", "INFO")
            
            return comprehensive_result
            
        except Exception as e:
            self.status = "error"
            self.log(f"❌ Coğrafi istihbarat analizi hatası: {e}", "ERROR")
            raise
    
    def stop(self) -> None:
        """Ajanı durdurur"""
        self.status = "stopped"
        self.log("⏹️ Master Coğrafi İstihbarat Ajanı durduruldu", "INFO")
    
    def restart(self) -> None:
        """Ajanı yeniden başlatır"""
        self.log("🔄 Master Coğrafi İstihbarat Ajanı yeniden başlatılıyor...", "INFO")
        self.status = "restarting"
        # Cache temizle
        self.geo_intelligence_cache = {}
        self.analysis_history = []
        self.status = "ready"
        self.log("✅ Yeniden başlatma tamamlandı", "INFO")
    
    # ============================================
    # ÖZEL ANALİZ METODLARI
    # ============================================
    
    def analyze_luxury_targeting(self, city: str = "Istanbul", product: Dict = None) -> Dict[str, Any]:
        """
        Lüks hedefleme analizi
        """
        try:
            product = product or {"name": "Lüks Ürün", "price_range": "high", "category": "luxury"}
            
            # Endeksa premium bölgeler
            premium_districts = self.endeksa.get_premium_districts(city)
            
            # Lüks ürün uyumluluğu
            district_names = [d["district"] for d in premium_districts]
            luxury_analysis = self.endeksa.analyze_luxury_product_fit(product, district_names)
            
            # GeoSpy konum istihbaratı
            geo_intel = self.geospy.get_location_intelligence(city)
            
            # WithRaven derin öğrenme
            combined_data = {
                "endeksa": premium_districts,
                "geospy": geo_intel,
                "product": product
            }
            
            withraven_result = self.withraven.process_geographic_data(combined_data)
            
            result = {
                "analysis_type": "luxury_targeting",
                "city": city,
                "product": product,
                "premium_districts": premium_districts,
                "luxury_analysis": luxury_analysis,
                "geo_intelligence": geo_intel,
                "ai_processing": withraven_result,
                "timestamp": datetime.now().isoformat()
            }
            
            self.log(f"💎 Lüks hedefleme analizi tamamlandı: {city}")
            return result
            
        except Exception as e:
            self.log(f"❌ Lüks hedefleme analizi hatası: {e}", "ERROR")
            return {"error": str(e)}
    
    def analyze_demographic_targeting(self, location: str, target_audience: Dict = None) -> Dict[str, Any]:
        """
        Demografik hedefleme analizi
        """
        try:
            target_audience = target_audience or {"age_range": "25-45", "income": "middle"}
            
            # Hoodmaps demografik verisi
            demographics = self.hoodmaps.get_neighborhood_demographics(location)
            
            # Hoodmaps kültürel içgörüler
            cultural = self.hoodmaps.get_cultural_insights(location)
            
            # GeoSpy konum istihbaratı
            geo_intel = self.geospy.get_location_intelligence(location)
            
            # WithRaven davranışsal analiz
            behavioral_data = {
                "location": location,
                "demographics": demographics,
                "cultural": cultural
            }
            
            behavioral_analysis = self.withraven.analyze_behavioral_patterns(behavioral_data)
            
            result = {
                "analysis_type": "demographic_targeting",
                "location": location,
                "target_audience": target_audience,
                "demographics": demographics,
                "cultural_insights": cultural,
                "geo_intelligence": geo_intel,
                "behavioral_analysis": behavioral_analysis,
                "timestamp": datetime.now().isoformat()
            }
            
            self.log(f"👥 Demografik hedefleme analizi tamamlandı: {location}")
            return result
            
        except Exception as e:
            self.log(f"❌ Demografik hedefleme analizi hatası: {e}", "ERROR")
            return {"error": str(e)}
    
    def analyze_competitor_landscape(self, competitor_urls: List[str], location: str) -> Dict[str, Any]:
        """
        Rakip peyzaj analizi
        """
        try:
            # Web scraping ile rakip verileri
            competitor_data = self.web_scraper.batch_scrape(competitor_urls, "pricing")
            
            # GeoSpy konum istihbaratı
            geo_intel = self.geospy.get_location_intelligence(location)
            
            # WithRaven karar desteği
            combined_data = {
                "competitor_data": competitor_data,
                "geo_intel": geo_intel,
                "location": location
            }
            
            decision_support = self.withraven.generate_decision_support(combined_data)
            
            result = {
                "analysis_type": "competitor_landscape",
                "location": location,
                "competitor_count": len(competitor_urls),
                "competitor_data": competitor_data,
                "geo_intelligence": geo_intel,
                "decision_support": decision_support,
                "timestamp": datetime.now().isoformat()
            }
            
            self.log(f"🔍 Rakip peyzaj analizi tamamlandı: {location}")
            return result
            
        except Exception as e:
            self.log(f"❌ Rakip peyzaj analizi hatası: {e}", "ERROR")
            return {"error": str(e)}
    
    # ============================================
    # YARDIMCI METODLAR
    # ============================================
    
    def _calculate_intelligence_score(self, hoodmaps: Dict, geospy: Dict, endeksa: Dict, withraven: Dict) -> float:
        """Genel istihbarat skorunu hesaplar"""
        scores = []
        
        if hoodmaps and "target_score" in hoodmaps:
            scores.append(hoodmaps["target_score"] * 100)
        
        if geospy and "demographics" in geospy:
            scores.append(75)  # GeoSpy için varsayılan
        
        if endeksa and isinstance(endeksa, list) and len(endeksa) > 0:
            scores.append(80)  # Endeksa için varsayılan
        
        if withraven and "confidence_score" in withraven:
            scores.append(withraven["confidence_score"] * 100)
        
        return sum(scores) / len(scores) if scores else 0.0
    
    def _generate_strategic_recommendations(self, geo_data: Dict, decision_support: Dict) -> List[str]:
        """Stratejik öneriler üretir"""
        recommendations = []
        
        # Karar desteğinden öneriler
        if decision_support and "strategic_recommendations" in decision_support:
            strat_rec = decision_support["strategic_recommendations"]
            recommendations.append(f"Ana Strateji: {strat_rec.get('primary_strategy', 'genel')}")
            recommendations.append(f"İkincil Strateji: {strat_rec.get('secondary_strategy', 'genel')}")
        
        # Coğrafi veriye dayalı öneriler
        if geo_data.get("hoodmaps", {}).get("target_score", 0) > 0.7:
            recommendations.append("Hoodmaps analizi yüksek hedefleme potansiyeli gösteriyor")
        
        if geo_data.get("geospy", {}).get("infrastructure", {}).get("internet_penetration", 0) > 0.9:
            recommendations.append("Yüksek internet penetrasyonu - dijital strateji öneriliyor")
        
        if geo_data.get("endeksa") and len(geo_data["endeksa"]) > 0:
            recommendations.append("Lüks bölge tespit edildi - premium strateji uygulanabilir")
        
        return recommendations
    
    def _save_analysis_result(self, result: Dict[str, Any]) -> bool:
        """Analiz sonucunu kaydeder"""
        try:
            self.analysis_history.append(result)
            
            # Dosyaya da kaydet
            state_file = os.path.join(
                os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                "data",
                "geo_intelligence_analysis.json"
            )
            
            os.makedirs(os.path.dirname(state_file), exist_ok=True)
            
            with open(state_file, 'w', encoding='utf-8') as f:
                json.dump(result, f, indent=4, ensure_ascii=False)
            
            return True
        except Exception as e:
            self.log(f"❌ Analiz sonucu kaydetme hatası: {e}", "ERROR")
            return False
    
    def get_analysis_history(self) -> List[Dict[str, Any]]:
        """Analiz geçmişini döndürür"""
        return self.analysis_history

# Test çalıştırması
if __name__ == "__main__":
    agent = MasterGeoIntelligenceAgent(agent_id=168)
    
    # Kapsamlı analiz test
    result = agent.run(
        target_location="Istanbul",
        product_category="electronics",
        analysis_type="comprehensive"
    )
    
    print("🌍 MASTER COĞRAFİ İSTİHBARAT ANALİZ SONUCU:")
    print(json.dumps(result, indent=2, ensure_ascii=False))
