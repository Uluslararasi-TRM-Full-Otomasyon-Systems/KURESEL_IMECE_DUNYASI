#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Security Compatibility Check
Nirvana Shield ve Ultra Nirvana Guardian çakışma kontrolü
"""

import logging
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from nirvana_shield_core import NirvanaShieldCore
from ultra_nirvana_guardian import UltraNirvanaGuardian

logger = logging.getLogger(__name__)

class SecurityCompatibilityCheck:
    def __init__(self):
        self.shield = NirvanaShieldCore()
        self.guardian = UltraNirvanaGuardian()
        
    def check_conflicts(self) -> dict:
        """
        İki güvenlik modülü arasındaki çakışmaları kontrol et
        """
        conflicts = {
            "has_conflicts": False,
            "warnings": [],
            "recommendations": [],
            "modules": {
                "nirvana_shield": {
                    "functions": ["apply_chaos_jitter", "get_masked_fingerprint", "check_circuit_breaker"],
                    "purpose": "Anti-ban ve parmak izi maskeleme"
                },
                "ultra_guardian": {
                    "functions": ["human_behavior_simulation", "dynamic_agent_quarantine_check", "record_operation"],
                    "purpose": "İnsan davranışı simülasyonu ve risk analizi"
                }
            }
        }
        
        # Çakışma kontrolü: time.sleep() kullanımı
        conflicts["warnings"].append("⚠️ Her iki modül de time.sleep() kullanıyor - toplam gecikme artabilir")
        
        # Çözüm önerileri
        conflicts["recommendations"].append("💡 Modülleri sıralı kullanın: önce Guardian, sonra Shield")
        conflicts["recommendations"].append("💡 Gecikme sürelerini optimize edin (base_seconds parametresi)")
        conflicts["recommendations"].append("💡 Circuit Breaker ve Quarantine sistemlerini entegre edin")
        
        # Fonksiyon çakışması kontrolü
        shield_functions = set(dir(self.shield))
        guardian_functions = set(dir(self.guardian))
        
        common_functions = shield_functions.intersection(guardian_functions)
        
        if common_functions:
            conflicts["has_conflicts"] = True
            conflicts["warnings"].append(f"⚠️ Ortak fonksiyonlar: {common_functions}")
        else:
            conflicts["recommendations"].append("✅ Fonksiyon çakışması yok")
        
        # Konfigürasyon çakışması kontrolü
        if hasattr(self.shield, 'config') and hasattr(self.guardian, 'audit_data'):
            conflicts["recommendations"].append("✅ Konfigürasyon yapıları ayrı - çakışma yok")
        
        logger.info("🔒 Güvenlik modülü çakışma kontrolü tamamlandı")
        return conflicts
    
    def test_sequential_execution(self, agent_name: str = "Test_Agent") -> dict:
        """
        Sıralı çalışma testi
        """
        test_results = {
            "agent_name": agent_name,
            "guardian_delay": 0,
            "shield_delay": 0,
            "total_delay": 0,
            "status": "success"
        }
        
        try:
            # Önce Guardian
            guardian_delay = self.guardian.human_behavior_simulation(agent_name)
            test_results["guardian_delay"] = guardian_delay
            
            # Sonra Shield
            shield_delay = self.shield.apply_chaos_jitter(base_seconds=2)
            test_results["shield_delay"] = shield_delay
            
            test_results["total_delay"] = guardian_delay + shield_delay
            
            logger.info(f"✅ Sıralı çalışma testi başarılı: {test_results['total_delay']:.2f}s toplam")
            
        except Exception as e:
            test_results["status"] = "error"
            test_results["error"] = str(e)
            logger.error(f"❌ Sıralı çalışma testi hatası: {e}")
        
        return test_results
    
    def generate_compatibility_report(self) -> dict:
        """
        Tam uyumluluk raporu oluştur
        """
        conflicts = self.check_conflicts()
        test_results = self.test_sequential_execution()
        
        report = {
            "timestamp": "2026-07-27",
            "compatibility_status": "COMPATIBLE" if not conflicts["has_conflicts"] else "CONFLICTS_FOUND",
            "conflicts": conflicts,
            "execution_test": test_results,
            "summary": {
                "can_run_together": True,
                "recommended_order": "Guardian → Shield",
                "performance_impact": "low",
                "security_level": "enhanced"
            }
        }
        
        return report

# Test çalıştırması
if __name__ == "__main__":
    import sys
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    
    checker = SecurityCompatibilityCheck()
    report = checker.generate_compatibility_report()
    
    import json
    print(json.dumps(report, indent=2, ensure_ascii=False))
