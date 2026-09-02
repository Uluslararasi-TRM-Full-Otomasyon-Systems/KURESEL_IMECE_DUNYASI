#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sistem Protokolleri ve Kuralları
Tüm ajanlar ve arayüz bileşenleri için merkezi protokol tanımları
"""

from typing import Dict, List, Optional, Any
from datetime import datetime

# ============================================
# HITAP PROTOKOLÜ
# ============================================

CEO_TITLE = "Sayın CEO Fahri Bey"

def get_ceo_title() -> str:
    """CEO hitap başlığını döndürür"""
    return CEO_TITLE

def format_ceo_message(message: str) -> str:
    """CEO'ya yönelik mesajı formatlar"""
    return f"{CEO_TITLE}, {message}"

# ============================================
# ÜYE ALIM STRATEJİSİ
# ============================================

class MembershipStrategy:
    """Üye Alım Stratejisi Sınıfı"""
    
    # İlk 100-200 kişi için hızlı kabul
    FAST_TRACK_LIMIT = 200
    
    # Trendurunlermarket.com onay süresi (ay)
    SYSTEM_VALIDATION_PERIOD = 9
    
    # Karakter ve ruhsal test süresi (ay)
    CHARACTER_TEST_PERIOD = 6
    
    # UTEYKDER Yönetim Kurulu üye sayısı
    UTEYKDER_BOARD_SIZE = 20
    
    @staticmethod
    def is_fast_track_period(current_member_count: int) -> bool:
        """Hızlı kabul döneminde olup olmadığını kontrol eder"""
        return current_member_count < MembershipStrategy.FAST_TRACK_LIMIT
    
    @staticmethod
    def requires_character_test(member_count: int, system_validated: bool = False) -> bool:
        """Karakter testi gerekip gerekmediğini kontrol eder"""
        # İlk 200 kişi için test gerekmez
        if member_count < MembershipStrategy.FAST_TRACK_LIMIT:
            return False
        
        # Sistem onaylandıktan sonra test gerekir
        if system_validated:
            return True
        
        return False
    
    @staticmethod
    def is_uteykder_board_member(user_id: str, board_members: List[str]) -> bool:
        """UTEYKDER Yönetim Kurulu üyesi olup olmadığını kontrol eder"""
        return user_id in board_members
    
    @staticmethod
    def is_field_youth(user_type: str) -> bool:
        """81 İl Saha Gençliği olup olmadığını kontrol eder"""
        return user_type == "field_youth"
    
    @staticmethod
    def requires_pre_screening(user_type: str, member_count: int, system_validated: bool = False) -> bool:
        """Ön eleme gerekip gerekmediğini kontrol eder"""
        # 81 İl Saha Gençliği her zaman ön elemeden geçer
        if MembershipStrategy.is_field_youth(user_type):
            return True
        
        # Diğerleri için karakter testi kuralı geçerli
        return MembershipStrategy.requires_character_test(member_count, system_validated)


# ============================================
# BYPASS YETKİSİ
# ============================================

class BypassAuthority:
    """Amir Onaylı Manuel Bypass Yetkisi"""
    
    BYPASS_CODE = "CEO_FAHRI_BEY_BYPASS"
    
    @staticmethod
    def validate_bypass_code(code: str) -> bool:
        """Bypass kodunu doğrular"""
        return code == BypassAuthority.BYPASS_CODE
    
    @staticmethod
    def create_bypass_record(user_id: str, reason: str, authorized_by: str = CEO_TITLE) -> Dict[str, Any]:
        """Bypass kaydı oluşturur"""
        return {
            "user_id": user_id,
            "bypass_reason": reason,
            "authorized_by": authorized_by,
            "bypass_timestamp": datetime.now().isoformat(),
            "bypass_code": BypassAuthority.BYPASS_CODE
        }


# ============================================
# LOG MESAJ FORMATLARI
# ============================================

class LogFormatter:
    """Log mesaj formatlayıcı"""
    
    @staticmethod
    def format_info(message: str) -> str:
        """Bilgi mesajı formatlar"""
        return f"[INFO] {format_ceo_message(message)}"
    
    @staticmethod
    def format_warning(message: str) -> str:
        """Uyarı mesajı formatlar"""
        return f"[WARNING] {format_ceo_message(message)}"
    
    @staticmethod
    def format_error(message: str) -> str:
        """Hata mesajı formatlar"""
        return f"[ERROR] {format_ceo_message(message)}"
    
    @staticmethod
    def format_success(message: str) -> str:
        """Başarı mesajı formatlar"""
        return f"[SUCCESS] {format_ceo_message(message)}"


# ============================================
# ARAYÜZ METİNLERİ
# ============================================

class InterfaceTexts:
    """Arayüz metinleri"""
    
    @staticmethod
    def get_welcome_message() -> str:
        """Hoş geldin mesajı"""
        return f"Hoş geldiniz, {CEO_TITLE}. Sistem hazır."
    
    @staticmethod
    def get_operation_complete(operation: str) -> str:
        """Operasyon tamamlandı mesajı"""
        return f"{operation} operasyonu başarıyla tamamlandı, {CEO_TITLE}."
    
    @staticmethod
    def get_confirmation_message(action: str) -> str:
        """Onay mesajı"""
        return f"{action} işlemini onaylıyor musunuz, {CEO_TITLE}?"
    
    @staticmethod
    def get_bypass_button_text() -> str:
        """Bypass butonu metni"""
        return f"Amir Onaylı Manuel Kabul (Bypass Yetkisi - {CEO_TITLE})"
    
    @staticmethod
    def get_uteykder_exempt_text() -> str:
        """UTEYKDER muafiyet metni"""
        return f"UTEYKDER Yönetim Kurulu üyesi - {CEO_TITLE} onayıyla muaf"


# ============================================
# GLOBAL SİSTEM DURUMU
# ============================================

class SystemStatus:
    """Global Sistem Durumu"""
    
    def __init__(self):
        self.current_member_count = 0
        self.system_validated = False
        self.uteykder_board_members = []
        self.bypass_records = []
    
    def add_member(self) -> None:
        """Üye sayısını artırır"""
        self.current_member_count += 1
    
    def set_system_validated(self, validated: bool) -> None:
        """Sistem onay durumunu ayarlar"""
        self.system_validated = validated
    
    def add_uteykder_board_member(self, user_id: str) -> None:
        """UTEYKDER Yönetim Kurulu üyesi ekler"""
        if user_id not in self.uteykder_board_members:
            self.uteykder_board_members.append(user_id)
    
    def add_bypass_record(self, record: Dict[str, Any]) -> None:
        """Bypass kaydı ekler"""
        self.bypass_records.append(record)
    
    def get_status(self) -> Dict[str, Any]:
        """Sistem durumunu döndürür"""
        return {
            "current_member_count": self.current_member_count,
            "fast_track_active": MembershipStrategy.is_fast_track_period(self.current_member_count),
            "system_validated": self.system_validated,
            "uteykder_board_count": len(self.uteykder_board_members),
            "total_bypasses": len(self.bypass_records)
        }


# ============================================
# TEDARİK VE KALİTE GÜVENCE PROTOKOLLERİ
# ============================================

class SupplyQualityProtocols:
    """Tedarik ve Kalite Güvence Protokolleri"""
    
    # Stok eşikleri
    CRITICAL_STOCK_THRESHOLD = 10
    WARNING_STOCK_THRESHOLD = 20
    
    # Failover ayarları
    TRAFFIC_SHIFT_THRESHOLD = 0.05  # %5 stok altında
    MAX_SHIFT_ATTEMPTS = 3
    
    # Gelir koruma
    COMMISSION_SPLIT = {"personal": 0.70, "imece_pool": 0.30}
    VOLUNTEER_COUNT = 200
    
    @staticmethod
    def get_diplomatic_alert_template(alert_level: str) -> Dict[str, str]:
        """Diplomatik uyarı şablonunu döndürür"""
        templates = {
            "first_alert": {
                "subject": "Değerli İş Ortaklığımız - Stok Bilgilendirmesi",
                "message": """Değerli iş ortağımız,

Otonom talep motorumuz ürününüze yoğun ilgi saptadı. Mevcut stok seviyeniz kritik eşiğe yaklaşmaktadır.

Müşteri memnuniyeti ve iş birliğimizin sürdürülebilirliği adına, stok yenileme işleminizi en kısa sürede gerçekleştirmenizi rica ederiz.

İş birliğiniz için teşekkürler,
İR-SA AŞ. Otonom Sistem"""
            },
            "second_alert": {
                "subject": "Acil Stok Yenileme Gerekiyor - İş Birliği Çağrısı",
                "message": """Değerli iş ortağımız,

Ürününüzün stok seviyesi kritik düzeydedir. Müşteri taleplerini karşılamakta zorlanıyoruz.

Lütfen stokunuzu 24 saat içinde yenileyin. Aksi takdirde, sistemimiz müşteri memnuniyetini korumak adına alternatif çözümler devreye alabilir.

İş birliğinizin devamını dileriz,
İR-SA AŞ. Otonom Sistem"""
            },
            "final_alert": {
                "subject": "Son Uyarı - Stok Tükenme Riski",
                "message": """Değerli iş ortağımız,

Ürününüzün stok seviyesi tükenme noktasındadır. Bu durum müşteri memnuniyetini ve gelir akışını tehdit etmektedir.

Son bir kez stok yenileme işleminizi gerçekleştirmenizi rica ederiz. Aksi takdirde, sistemimiz otomatik olarak alternatif ürünlere trafik yönlendirecektir.

İş birliğiniz için teşekkürler,
İR-SA AŞ. Otonom Sistem"""
            }
        }
        return templates.get(alert_level, templates["first_alert"])
    
    @staticmethod
    def is_stock_critical(current_stock: int, threshold: int = None) -> bool:
        """Stokun kritik olup olmadığını kontrol eder"""
        if threshold is None:
            threshold = SupplyQualityProtocols.CRITICAL_STOCK_THRESHOLD
        return current_stock <= threshold
    
    @staticmethod
    def is_stock_warning(current_stock: int, threshold: int = None) -> bool:
        """Stokun uyarı seviyesinde olup olmadığını kontrol eder"""
        if threshold is None:
            threshold = SupplyQualityProtocols.WARNING_STOCK_THRESHOLD
        return current_stock <= threshold and current_stock > SupplyQualityProtocols.CRITICAL_STOCK_THRESHOLD
    
    @staticmethod
    def should_trigger_failover(current_stock: int, total_stock: int) -> bool:
        """Failover switch tetiklenip tetiklenmeyeceğini kontrol eder"""
        if total_stock == 0:
            return False
        stock_ratio = current_stock / total_stock
        return stock_ratio <= SupplyQualityProtocols.TRAFFIC_SHIFT_THRESHOLD


# Global sistem durumu örneği
system_status = SystemStatus()
