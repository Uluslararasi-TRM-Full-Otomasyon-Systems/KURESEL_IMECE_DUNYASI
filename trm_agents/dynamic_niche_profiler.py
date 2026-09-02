#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Dynamic Niche Profiler (DNP) Agent
İçeriklerin doğru niş kitleyle eşleştirilmesini sağlayan filtreleme mekanizması
Yanlış kitlelere dağıtımı bloke eden güvenlik kuralı
"""

import json
import logging
from typing import Dict, List, Optional
from datetime import datetime
from utils.config_loader import load_config
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from nirvana_shield_core import NirvanaShieldCore
from ultra_nirvana_guardian import UltraNirvanaGuardian

logger = logging.getLogger(__name__)

class DynamicNicheProfiler:
    def __init__(self, agent_id=160):
        self.agent_id = agent_id
        self.name = f"DNP-{agent_id:03d}"
        self.config = load_config()
        self.niche_database = self.load_niche_database()
        self.blocked_distributions = []
        
        # Grup Tabanlı Dağıtım (Group-Based Distribution) İskeleti
        self.target_users = 100000  # Eşik tetikleyicisi
        self.group_based_distribution_enabled = False  # Şu an pasif
        self.group_size = 100  # Her grup 100 kullanıcı
        self.affiliate_groups = {}
        
        # Ban ve Risk Yönetim - Circuit Breaker
        self.ban_threshold = 0.15  # %15 ban/kısıtlama oranı eşiği
        self.group_ban_rates = {}  # Grup bazlı ban oranları
        self.circuit_breaker_status = {}  # Grup bazlı devre kesici durumu
        self.ban_signal_detectors = {}  # Ban sinyali algılayıcıları
        self.shadowban_indicators = {}  # Shadowban göstergeleri
        
        # Rehabilitasyon Modu (Rehab Mode)
        self.rehab_accounts = {}  # Rehabilitasyon modundaki hesaplar
        self.rehab_duration_days = 21  # 14-21 gün rehab süresi
        
        # Yedek Hesap Havuzu (Buffer Accounts)
        self.buffer_accounts = {}  # Yedek hesap havuzu
        self.warmup_buffer_status = {}  # Isıtma durumu takibi
        self.failover_enabled = True  # Failover protokolü aktif
        
        # Nirvana Güvenlik Entegrasyonu
        self.shield = NirvanaShieldCore()  # Cihaz parmak izi maskeleme
        self.guardian = UltraNirvanaGuardian()  # İnsani davranış simülasyonu
        
    def load_niche_database(self) -> Dict:
        """Niş veritabanını yükle"""
        try:
            with open("data/niche_profiles.json", "r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            # Varsayılan niş veritabanı
            default_niches = {
                "luxury_products": {
                    "target_audience": ["high_income", "urban_professionals", "age_35_55"],
                    "platforms": ["instagram", "linkedin", "facebook"],
                    "content_tone": "premium",
                    "keywords": ["lüks", "premium", "exclusive", "designer"]
                },
                "tech_products": {
                    "target_audience": ["tech_savvy", "early_adopters", "age_18_35"],
                    "platforms": ["twitter", "reddit", "youtube"],
                    "content_tone": "technical",
                    "keywords": ["tech", "innovation", "digital", "smart"]
                },
                "family_products": {
                    "target_audience": ["parents", "families", "age_25_45"],
                    "platforms": ["facebook", "instagram", "pinterest"],
                    "content_tone": "warm",
                    "keywords": ["family", "kids", "home", "comfort"]
                },
                "youth_products": {
                    "target_audience": ["gen_z", "students", "age_16_25"],
                    "platforms": ["tiktok", "instagram", "snapchat"],
                    "content_tone": "casual",
                    "keywords": ["trend", "viral", "cool", "style"]
                }
            }
            
            # Veritabanını kaydet
            import os
            os.makedirs("data", exist_ok=True)
            with open("data/niche_profiles.json", "w", encoding="utf-8") as f:
                json.dump(default_niches, f, indent=2, ensure_ascii=False)
            
            return default_niches
    
    def analyze_content_niche(self, content: Dict) -> str:
        """
        İçeriğin niş kategorisini analiz et
        """
        text = content.get("content", "").lower()
        title = content.get("title", "").lower()
        combined_text = f"{title} {text}"
        
        niche_scores = {}
        for niche_name, niche_data in self.niche_database.items():
            score = 0
            for keyword in niche_data.get("keywords", []):
                if keyword in combined_text:
                    score += 1
            niche_scores[niche_name] = score
        
        # En yüksek skorlu niş'i döndür
        if niche_scores:
            best_niche = max(niche_scores, key=niche_scores.get)
            if niche_scores[best_niche] > 0:
                return best_niche
        
        return "general"
    
    def validate_target_audience(self, content: Dict, target_platforms: List[str]) -> Dict:
        """
        Hedef kitle ve platform uyumluluğunu doğrula
        """
        niche = self.analyze_content_niche(content)
        niche_data = self.niche_database.get(niche, {})
        
        allowed_platforms = niche_data.get("platforms", ["facebook", "instagram", "twitter"])
        
        validation_result = {
            "niche": niche,
            "allowed_platforms": allowed_platforms,
            "requested_platforms": target_platforms,
            "blocked_platforms": [],
            "approved_platforms": [],
            "is_valid": True
        }
        
        for platform in target_platforms:
            if platform.lower() in [p.lower() for p in allowed_platforms]:
                validation_result["approved_platforms"].append(platform)
            else:
                validation_result["blocked_platforms"].append(platform)
                validation_result["is_valid"] = False
        
        if validation_result["blocked_platforms"]:
            logger.warning(f"🚫 {self.name}: {len(validation_result['blocked_platforms'])} platform bloke edildi (niş uyuşmazlığı)")
            self.blocked_distributions.append({
                "timestamp": datetime.now().isoformat(),
                "niche": niche,
                "blocked_platforms": validation_result["blocked_platforms"],
                "reason": "Niche audience mismatch"
            })
        
        return validation_result
    
    def get_content_tone_recommendation(self, content: Dict) -> str:
        """
        İçerik tonu önerisi
        """
        niche = self.analyze_content_niche(content)
        niche_data = self.niche_database.get(niche, {})
        return niche_data.get("content_tone", "casual")
    
    def filter_distribution_targets(self, content: Dict, all_platforms: List[str]) -> List[str]:
        """
        Dağıtım hedeflerini filtrele - sadece uygun platformları döndür
        """
        validation = self.validate_target_audience(content, all_platforms)
        
        if validation["is_valid"]:
            return validation["approved_platforms"]
        else:
            logger.warning(f"⚠️ {self.name}: Dağıtım filtrelendi - sadece {validation['approved_platforms']} platformlarına gönderilecek")
            return validation["approved_platforms"]
    
    def get_blocked_distributions_report(self) -> List[Dict]:
        """
        Bloke edilen dağıtımların raporunu döndür
        """
        return self.blocked_distributions
    
    def refresh_config(self):
        """Konfigürasyonu yenile"""
        self.config = load_config()
        self.niche_database = self.load_niche_database()
    
    def check_group_distribution_trigger(self, current_active_users: int) -> bool:
        """
        Grup tabanlı dağıtım tetikleyicisini kontrol et
        Aktif kullanıcı sayısı 100.000'e ulaştığında otomatik aktifleşir
        """
        if current_active_users >= self.target_users:
            if not self.group_based_distribution_enabled:
                self.group_based_distribution_enabled = True
                logger.info(f"🚀 {self.name}: Grup tabanlı dağıtım AKTIF! (Kullanıcı: {current_active_users})")
                self.initialize_affiliate_groups(current_active_users)
            return True
        return False
    
    def initialize_affiliate_groups(self, total_users: int):
        """
        Affiliate gruplarını başlat
        Kullanıcıları 100'er kişilik gruplara böl ve her gruba affiliate/niş ata
        """
        num_groups = total_users // self.group_size
        
        affiliate_templates = {
            "luxury_affiliate": {
                "name": "Lüks Ürünler Partneri",
                "niche": "luxury_products",
                "ip_tunnel": "simulated_luxury_network",
                "device_profile": "high_end_devices"
            },
            "tech_affiliate": {
                "name": "Teknoloji Partneri",
                "niche": "tech_products",
                "ip_tunnel": "simulated_tech_network",
                "device_profile": "tech_devices"
            },
            "family_affiliate": {
                "name": "Aile Ürünleri Partneri",
                "niche": "family_products",
                "ip_tunnel": "simulated_family_network",
                "device_profile": "family_devices"
            },
            "youth_affiliate": {
                "name": "Gençlik Partneri",
                "niche": "youth_products",
                "ip_tunnel": "simulated_youth_network",
                "device_profile": "youth_devices"
            }
        }
        
        for group_id in range(num_groups):
            template_key = list(affiliate_templates.keys())[group_id % len(affiliate_templates)]
            template = affiliate_templates[template_key]
            
            self.affiliate_groups[f"group_{group_id}"] = {
                "group_id": group_id,
                "users_count": self.group_size,
                "affiliate": template["name"],
                "niche": template["niche"],
                "ip_tunnel": template["ip_tunnel"],
                "device_profile": template["device_profile"],
                "status": "active",
                "created_at": datetime.now().isoformat()
            }
        
        logger.info(f"📊 {self.name}: {num_groups} affiliate grubu başlatıldı")
    
    def get_group_for_user(self, user_id: int) -> Optional[Dict]:
        """
        Kullanıcının ait olduğu grubu döndür
        """
        if not self.group_based_distribution_enabled:
            return None
        
        group_id = user_id // self.group_size
        return self.affiliate_groups.get(f"group_{group_id}")
    
    def distribute_to_group(self, content: Dict, group_id: int) -> Dict:
        """
        İçeriği belirtilen gruba dağıt - Nirvana güvenlik entegrasyonu ile
        """
        if not self.group_based_distribution_enabled:
            return {"error": "Grup tabanlı dağıtım henüz aktif değil"}
        
        group = self.affiliate_groups.get(f"group_{group_id}")
        if not group:
            return {"error": "Grup bulunamadı"}
        
        # Nirvana Guardian: İnsani davranış simülasyonu
        human_delay = self.guardian.human_behavior_simulation(f"Group_{group_id}")
        logger.info(f"[GUARDIAN] İnsan davranışı simülasyonu: {human_delay:.2f}s")
        
        # Nirvana Guardian: Risk analizi
        risk_score = content.get("risk_score", 0.1)
        quarantine_check = self.guardian.dynamic_agent_quarantine_check(group_id, risk_score)
        
        if not quarantine_check:
            logger.warning(f"[GUARDIAN] Grup {group_id} karantinaya alındı - yüksek risk")
            return {"error": "Grup karantinaya alındı - yüksek risk"}
        
        # Nirvana Shield: Cihaz parmak izi maskeleme
        user_id = content.get("user_id", f"group_{group_id}")
        fingerprint = self.shield.get_masked_fingerprint(user_id)
        logger.info(f"[SHIELD] Maskelenmiş parmak izi: {fingerprint}")
        
        # Nirvana Shield: Chaos jitter ile dağıtım aralığı
        jitter_wait = self.shield.apply_chaos_jitter(base_seconds=3)
        logger.info(f"[SHIELD] Chaos jitter bekleme süresi: {jitter_wait:.2f}s")
        
        # Grup nişine göre içerik filtrele
        niche = group.get("niche")
        niche_data = self.niche_database.get(niche, {})
        
        distribution_result = {
            "group_id": group_id,
            "group_size": group.get("users_count"),
            "affiliate": group.get("affiliate"),
            "niche": niche,
            "ip_tunnel": group.get("ip_tunnel"),
            "device_profile": group.get("device_profile"),
            "content_tone": niche_data.get("content_tone", "casual"),
            "recommended_platforms": niche_data.get("platforms", []),
            "status": "ready_for_distribution",
            "security_applied": {
                "fingerprint_masked": True,
                "human_simulation": True,
                "chaos_jitter": jitter_wait,
                "risk_check_passed": True
            }
        }
        
        logger.info(f"[DNP] Grup {group_id}'e dağıtım hazır - {group.get('affiliate')}")
        return distribution_result
    
    def get_group_distribution_status(self) -> Dict:
        """
        Grup dağıtım durumunu döndür
        """
        return {
            "enabled": self.group_based_distribution_enabled,
            "target_users": self.target_users,
            "group_size": self.group_size,
            "total_groups": len(self.affiliate_groups),
            "groups": self.affiliate_groups
        }
    
    # ============================================
    # CIRCUIT BREAKER MEKANİZMASI
    # ============================================
    
    def update_group_ban_rate(self, group_id: int, ban_count: int, total_actions: int):
        """
        Grup ban oranını güncelle
        """
        if total_actions == 0:
            return
        
        ban_rate = ban_count / total_actions
        self.group_ban_rates[f"group_{group_id}"] = {
            "ban_rate": ban_rate,
            "ban_count": ban_count,
            "total_actions": total_actions,
            "last_updated": datetime.now().isoformat()
        }
        
        # Circuit Breaker kontrolü
        if ban_rate >= self.ban_threshold:
            self.trigger_circuit_breaker(group_id, ban_rate)
    
    def detect_ban_signals(self, account_id: str, platform: str, metrics: Dict) -> Dict:
        """
        Ban/shadowban sinyallerini algıla (Facebook Reels, Instagram, TikTok vb.)
        """
        signals = {
            "account_id": account_id,
            "platform": platform,
            "detected_at": datetime.now().isoformat(),
            "signals": [],
            "risk_score": 0.0,
            "action_required": False
        }
        
        # Engagement drop kontrolü
        if "engagement_rate" in metrics:
            current_engagement = metrics["engagement_rate"]
            baseline_engagement = metrics.get("baseline_engagement", 0.05)
            
            if current_engagement < baseline_engagement * 0.5:
                signals["signals"].append({
                    "type": "engagement_drop",
                    "severity": "high",
                    "current": current_engagement,
                    "baseline": baseline_engagement,
                    "drop_percent": ((baseline_engagement - current_engagement) / baseline_engagement) * 100
                })
                signals["risk_score"] += 0.3
        
        # Reach/Impression drop kontrolü
        if "reach_rate" in metrics:
            current_reach = metrics["reach_rate"]
            baseline_reach = metrics.get("baseline_reach", 0.1)
            
            if current_reach < baseline_reach * 0.4:
                signals["signals"].append({
                    "type": "reach_drop",
                    "severity": "critical",
                    "current": current_reach,
                    "baseline": baseline_reach,
                    "drop_percent": ((baseline_reach - current_reach) / baseline_reach) * 100
                })
                signals["risk_score"] += 0.4
        
        # Hashtag visibility kontrolü
        if "hashtag_visibility" in metrics:
            if metrics["hashtag_visibility"] == "none":
                signals["signals"].append({
                    "type": "hashtag_shadowban",
                    "severity": "high"
                })
                signals["risk_score"] += 0.35
        
        # Account status kontrolü
        if "account_status" in metrics:
            if metrics["account_status"] in ["restricted", "shadowbanned", "action_blocked"]:
                signals["signals"].append({
                    "type": "account_restriction",
                    "severity": "critical",
                    "status": metrics["account_status"]
                })
                signals["risk_score"] += 0.5
        
        # Video/Reels özel kontroller
        if platform == "facebook" and "reels_metrics" in metrics:
            reels_data = metrics["reels_metrics"]
            if reels_data.get("views", 0) < 10 and reels_data.get("posted_hours_ago", 0) > 2:
                signals["signals"].append({
                    "type": "reels_visibility_issue",
                    "severity": "high",
                    "views": reels_data["views"],
                    "hours_since_post": reels_data["posted_hours_ago"]
                })
                signals["risk_score"] += 0.25
        
        # Risk skoru eşiği kontrolü
        if signals["risk_score"] >= 0.5:
            signals["action_required"] = True
            self.ban_signal_detectors[account_id] = signals
            logger.error(f"[BAN SIGNAL] {account_id} için ban sinyali algılandı! Risk: {signals['risk_score']:.2f}")
        
        return signals
    
    def trigger_circuit_breaker(self, group_id: int, ban_rate: float):
        """
        Devre kesiciyi tetikle - affiliate paylaşımlarını durdur
        """
        self.circuit_breaker_status[f"group_{group_id}"] = {
            "status": "TRIPPED",
            "ban_rate": ban_rate,
            "triggered_at": datetime.now().isoformat(),
            "reason": f"Ban oranı {ban_rate:.2%} eşiği aştı"
        }
        
        # Grup durumunu güncelle
        if f"group_{group_id}" in self.affiliate_groups:
            self.affiliate_groups[f"group_{group_id}"]["status"] = "circuit_breaker_tripped"
        
        logger.error(f"[CIRCUIT BREAKER] Grup {group_id} devre kesici tetiklendi! Ban oranı: {ban_rate:.2%}")
    
    def check_circuit_breaker(self, group_id: int) -> bool:
        """
        Devre kesici durumunu kontrol et
        True = paylaşıma izin ver, False = durdur
        """
        breaker_status = self.circuit_breaker_status.get(f"group_{group_id}", {})
        return breaker_status.get("status") != "TRIPPED"
    
    def reset_circuit_breaker(self, group_id: int):
        """
        Devre kesiciyi sıfırla
        """
        if f"group_{group_id}" in self.circuit_breaker_status:
            del self.circuit_breaker_status[f"group_{group_id}"]
        
        if f"group_{group_id}" in self.affiliate_groups:
            self.affiliate_groups[f"group_{group_id}"]["status"] = "active"
        
        logger.info(f"[CIRCUIT BREAKER] Grup {group_id} devre kesici sıfırlandı")
    
    # ============================================
    # REHABİLİTASYON MODU (REHAB MODE)
    # ============================================
    
    def enter_rehab_mode(self, account_id: str, reason: str):
        """
        Hesabı rehabilitasyon moduna al - sadece organik trend içerikler paylaşabilir
        """
        from datetime import timedelta
        
        rehab_end_date = datetime.now() + timedelta(days=self.rehab_duration_days)
        
        self.rehab_accounts[account_id] = {
            "status": "rehab",
            "reason": reason,
            "entered_at": datetime.now().isoformat(),
            "rehab_end_date": rehab_end_date.isoformat(),
            "allowed_content_types": ["organic", "trend", "engagement", "lifestyle", "entertainment"],
            "blocked_content_types": ["affiliate", "commercial", "promotional", "sales", "marketing"],
            "daily_post_limit": 2,
            "required_engagement_actions": ["like", "comment", "share"],
            "content_themes": ["trending_topics", "viral_content", "community_posts"]
        }
        
        logger.warning(f"[REHAB MODE] Hesap {account_id} rehabilitasyon moduna alındı. Süre: {self.rehab_duration_days} gün")
    
    def check_rehab_status(self, account_id: str) -> Dict:
        """
        Hesabın rehabilitasyon durumunu kontrol et
        """
        rehab_info = self.rehab_accounts.get(account_id)
        
        if not rehab_info:
            return {"in_rehab": False}
        
        rehab_end = datetime.fromisoformat(rehab_info["rehab_end_date"])
        
        if datetime.now() >= rehab_end:
            # Rehab süresi doldu
            del self.rehab_accounts[account_id]
            logger.info(f"[REHAB MODE] Hesap {account_id} rehabilitasyon süresi doldu, normal moda geçti")
            return {"in_rehab": False, "rehab_completed": True}
        
        return {
            "in_rehab": True,
            "rehab_end_date": rehab_info["rehab_end_date"],
            "allowed_content": rehab_info["allowed_content_types"],
            "blocked_content": rehab_info["blocked_content_types"]
        }
    
    def can_post_content(self, account_id: str, content_type: str, content_theme: str = None) -> bool:
        """
        Hesabın belirtilen içerik tipini paylaşabileceğini kontrol et
        Rehab modunda sadece organik trend içeriklere izin verilir
        """
        rehab_status = self.check_rehab_status(account_id)
        
        if rehab_status["in_rehab"]:
            if content_type in rehab_status.get("blocked_content", []):
                logger.warning(f"[REHAB MODE] Hesap {account_id} {content_type} içeriği paylaşamaz (rehab modunda)")
                return False
            
            if content_theme and content_theme not in rehab_status.get("content_themes", []):
                logger.warning(f"[REHAB MODE] Hesap {account_id} {content_theme} teması paylaşamaz (rehab modunda)")
                return False
            
            rehab_info = self.rehab_accounts.get(account_id, {})
            if rehab_info.get("daily_post_limit", 0) <= 0:
                logger.warning(f"[REHAB MODE] Hesap {account_id} günlük paylaşım limitine ulaştı")
                return False
        
        return True
    
    # ============================================
    # YEDEK HESAP HAVUZU (BUFFER ACCOUNTS)
    # ============================================
    
    def register_buffer_account(self, user_id: int, buffer_account_id: str, platform: str):
        """
        Kullanıcı için yedek hesap kaydet
        """
        if user_id not in self.buffer_accounts:
            self.buffer_accounts[user_id] = []
        
        self.buffer_accounts[user_id].append({
            "buffer_account_id": buffer_account_id,
            "platform": platform,
            "status": "warming_up",
            "warmup_start": datetime.now().isoformat(),
            "warmup_progress": 0
        })
        
        logger.info(f"[BUFFER] Yedek hesap kaydedildi: {buffer_account_id} için kullanıcı {user_id}")
    
    def update_warmup_progress(self, user_id: int, buffer_account_id: str, progress: int):
        """
        Isıtma ilerlemesini güncelle (0-100)
        """
        if user_id in self.buffer_accounts:
            for account in self.buffer_accounts[user_id]:
                if account["buffer_account_id"] == buffer_account_id:
                    account["warmup_progress"] = progress
                    if progress >= 100:
                        account["status"] = "ready"
                        account["warmup_complete"] = datetime.now().isoformat()
                    break
    
    def get_ready_buffer_account(self, user_id: int, platform: str) -> Optional[Dict]:
        """
        Hazır yedek hesabı döndür
        """
        if user_id not in self.buffer_accounts:
            return None
        
        for account in self.buffer_accounts[user_id]:
            if account["platform"] == platform and account["status"] == "ready":
                return account
        
        return None
    
    # ============================================
    # FAILOVER PROTOKOLÜ
    # ============================================
    
    def trigger_failover(self, user_id: int, platform: str, primary_account_id: str) -> Dict:
        """
        Ana hesap banlandığında yedek hesaba geçiş yap
        """
        if not self.failover_enabled:
            return {"error": "Failover protokolü devre dışı"}
        
        # Hazır yedek hesabı ara
        buffer_account = self.get_ready_buffer_account(user_id, platform)
        
        if not buffer_account:
            # Hazır yedek yok, rehabilitasyon moduna al
            self.enter_rehab_mode(primary_account_id, "Ana hesap banlandı - yedek hesap hazır değil")
            return {"error": "Hazır yedek hesap bulunamadı", "action": "rehab_mode_triggered"}
        
        # Failover başarılı
        failover_record = {
            "user_id": user_id,
            "platform": platform,
            "primary_account": primary_account_id,
            "buffer_account": buffer_account["buffer_account_id"],
            "failover_time": datetime.now().isoformat(),
            "status": "success"
        }
        
        logger.info(f"[FAILOVER] Başarılı: {primary_account_id} -> {buffer_account['buffer_account_id']}")
        
        return failover_record
    
    def get_buffer_status(self, user_id: int) -> Dict:
        """
        Kullanıcının yedek hesap durumunu döndür
        """
        return {
            "user_id": user_id,
            "buffer_accounts": self.buffer_accounts.get(user_id, []),
            "failover_enabled": self.failover_enabled
        }

# Test çalıştırması
if __name__ == "__main__":
    dnp = DynamicNicheProfiler()
    
    test_content = {
        "title": "Premium Lüks Saat Koleksiyonu",
        "content": "Exclusive designer watches for high-end customers"
    }
    
    platforms = ["facebook", "instagram", "linkedin", "tiktok", "twitter"]
    
    validation = dnp.validate_target_audience(test_content, platforms)
    print(json.dumps(validation, indent=2, ensure_ascii=False))
