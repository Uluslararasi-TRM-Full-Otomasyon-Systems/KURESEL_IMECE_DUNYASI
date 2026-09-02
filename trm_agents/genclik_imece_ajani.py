#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gençlik Sosyal İmece Saha Yönetimi ve Otonom Denetim Ajanı
Farklı siyasi görüşlerden gençlerin saha faaliyetlerini yöneten otonom sistem
"""

import os
import sys
import json
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
import random

# BaseAgent'ı import et
from .base_agent_template import BaseAgent

# Kamera Psiko Analiz Ajanını import et
from .kamera_psiko_analiz_ajani import KameraPsikoAnalizAjani

# Sistem Protokollerini import et
from .system_protocols import (
    CEO_TITLE,
    get_ceo_title,
    format_ceo_message,
    MembershipStrategy,
    BypassAuthority,
    LogFormatter,
    InterfaceTexts,
    system_status
)

logger = logging.getLogger(__name__)

class GenclikImeceAjani(BaseAgent):
    """
    Gençlik Sosyal İmece Saha Yönetimi ve Otonom Denetim Ajanı
    
    Bu ajan:
    - AI Mülakat Asistanı ile işe alım yapar
    - Serbest zamanlı saha takibi sağlar
    - Görsel doğrulama ve puanlama yapar
    - İmece Payı dağıtım takibi yapar
    - 7/24 denetim ve öğretme sistemi sağlar
    """
    
    def __init__(self, agent_id: Optional[int] = None):
        super().__init__(
            agent_name="Gençlik Sosyal İmece Saha Yönetimi ve Otonom Denetim Ajanı",
            agent_id=agent_id if agent_id else 170
        )
        
        # Alt sistemler
        self.interview_assistant = InterviewAssistant()
        self.field_tracker = FieldTracker()
        self.visual_validator = VisualValidator()
        self.imece_share_calculator = ImeceShareCalculator()
        self.audit_teaching_system = AuditTeachingSystem()
        
        # Kamera Psiko Analiz Ajanı entegrasyonu
        self.kamera_psiko_analiz = KameraPsikoAnalizAjani(agent_id=171)
        
        # Veri depolama
        self.candidates = {}
        self.active_volunteers = {}
        self.field_reports = {}
        self.imece_shares = {}
        self.audit_logs = []
        
        self.log(f"🎓 Gençlik Sosyal İmece Saha Yönetimi ve Otonom Denetim Ajanı başlatıldı. {CEO_TITLE}", "INFO")
    
    # ============================================
    # ANA METODLAR (BaseAgent Override)
    # ============================================
    
    def run(self, **kwargs) -> Dict[str, Any]:
        """
        Ana çalıştırma metodu
        """
        self.status = "running"
        self.log("🚀 Gençlik İmece sistemi başlatılıyor...", "INFO")
        
        try:
            operation = kwargs.get('operation', 'dashboard')
            
            if operation == 'interview':
                return self._conduct_interview(kwargs)
            elif operation == 'field_report':
                return self._process_field_report(kwargs)
            elif operation == 'visual_validation':
                return self._validate_visual(kwargs)
            elif operation == 'imece_share':
                return self._calculate_imece_share(kwargs)
            elif operation == 'audit':
                return self._conduct_audit(kwargs)
            else:
                return self._get_dashboard(kwargs)
                
        except Exception as e:
            self.status = "error"
            self.log(f"❌ Gençlik İmece sistemi hatası: {e}", "ERROR")
            raise
    
    def stop(self) -> None:
        """Ajanı durdurur"""
        self.status = "stopped"
        self.log("⏹️ Gençlik İmece Ajanı durduruldu", "INFO")
    
    def restart(self) -> None:
        """Ajanı yeniden başlatır"""
        self.log("🔄 Gençlik İmece Ajanı yeniden başlatılıyor...", "INFO")
        self.status = "restarting"
        self.candidates = {}
        self.active_volunteers = {}
        self.field_reports = {}
        self.imece_shares = {}
        self.audit_logs = []
        self.status = "ready"
        self.log("✅ Yeniden başlatma tamamlandı", "INFO")
    
    # ============================================
    # İŞE ALIM MÜLAKAT SİSTEMİ
    # ============================================
    
    def _conduct_interview(self, kwargs: Dict[str, Any]) -> Dict[str, Any]:
        """AI Mülakat Asistanı ile mülakat yapar"""
        
        candidate_id = kwargs.get('candidate_id', f"candidate_{len(self.candidates) + 1}")
        candidate_name = kwargs.get('candidate_name', 'Bilinmeyen Aday')
        age = kwargs.get('age', 18)
        education = kwargs.get('education', 'lise')
        political_view = kwargs.get('political_view', 'belirtilmemiş')
        social_skills = kwargs.get('social_skills', {})
        enable_video_analysis = kwargs.get('enable_video_analysis', False)
        user_type = kwargs.get('user_type', 'regular')
        bypass_code = kwargs.get('bypass_code', None)
        
        # Bypass kontrolü
        if bypass_code and BypassAuthority.validate_bypass_code(bypass_code):
            bypass_record = BypassAuthority.create_bypass_record(candidate_id, "Amir onaylı manuel kabul")
            system_status.add_bypass_record(bypass_record)
            
            # Doğrudan kabul
            self.log(f"{candidate_name} bypass kodu ile sisteme dahil edildi. {CEO_TITLE}", "INFO")
            return self._direct_hire(candidate_id, candidate_name, age, education, political_view, social_skills, bypass_record)
        
        # UTEYKDER Yönetim Kurulu muafiyeti
        if MembershipStrategy.is_uteykder_board_member(candidate_id, system_status.uteykder_board_members):
            self.log(f"{candidate_name} UTEYKDER Yönetim Kurulu üyesi - testlerden muaf. {CEO_TITLE}", "INFO")
            return self._direct_hire(candidate_id, candidate_name, age, education, political_view, social_skills, {"exempt_reason": "UTEYKDER Board Member"})
        
        # Üye alım stratejisi kontrolü
        current_member_count = system_status.current_member_count
        system_validated = system_status.system_validated
        
        # Ön eleme gerekiyor mu?
        requires_pre_screening = MembershipStrategy.requires_pre_screening(user_type, current_member_count, system_validated)
        
        # Karakter testi gerekiyor mu?
        requires_character_test = MembershipStrategy.requires_character_test(current_member_count, system_validated)
        
        # Mülakat süreci
        interview_result = self.interview_assistant.conduct_interview(
            candidate_id=candidate_id,
            candidate_name=candidate_name,
            age=age,
            education=education,
            political_view=political_view,
            social_skills=social_skills,
            kamera_psiko_analiz=self.kamera_psiko_analiz if enable_video_analysis else None,
            requires_pre_screening=requires_pre_screening,
            requires_character_test=requires_character_test,
            user_type=user_type
        )
        
        # Başarılıysa gönüllü olarak ekle
        if interview_result['is_hired']:
            self.active_volunteers[candidate_id] = {
                "volunteer_id": candidate_id,
                "name": candidate_name,
                "age": age,
                "education": education,
                "political_view": political_view,
                "join_date": datetime.now().isoformat(),
                "status": "active",
                "total_score": 0,
                "total_tasks": 0,
                "imece_share": 0,
                "user_type": user_type
            }
            system_status.add_member()
        
        return {
            "operation": "interview",
            "candidate_id": candidate_id,
            "interview_result": interview_result,
            "is_hired": interview_result['is_hired'],
            "requires_pre_screening": requires_pre_screening,
            "requires_character_test": requires_character_test,
            "timestamp": datetime.now().isoformat()
        }
    
    def _direct_hire(self, candidate_id: str, candidate_name: str, age: int, 
                     education: str, political_view: str, social_skills: Dict, 
                     exemption_info: Dict) -> Dict[str, Any]:
        """Doğrudan kabul (bypass veya muafiyet durumları için)"""
        
        # Adayı kaydet
        self.candidates[candidate_id] = {
            "candidate_id": candidate_id,
            "candidate_name": candidate_name,
            "age": age,
            "education": education,
            "political_view": political_view,
            "social_skills": social_skills,
            "interview_result": {
                "is_hired": True,
                "exemption": exemption_info,
                "timestamp": datetime.now().isoformat()
            },
            "interview_date": datetime.now().isoformat()
        }
        
        # Gönüllü olarak ekle
        self.active_volunteers[candidate_id] = {
            "volunteer_id": candidate_id,
            "name": candidate_name,
            "age": age,
            "education": education,
            "political_view": political_view,
            "join_date": datetime.now().isoformat(),
            "status": "active",
            "total_score": 0,
            "total_tasks": 0,
            "imece_share": 0,
            "exemption": exemption_info
        }
        
        system_status.add_member()
        
        return {
            "operation": "direct_hire",
            "candidate_id": candidate_id,
            "candidate_name": candidate_name,
            "is_hired": True,
            "exemption": exemption_info,
            "timestamp": datetime.now().isoformat()
        }
    
    # ============================================
    # SAHA TAKİP SİSTEMİ
    # ============================================
    
    def _process_field_report(self, kwargs: Dict[str, Any]) -> Dict[str, Any]:
        """Saha raporunu işler"""
        
        volunteer_id = kwargs.get('volunteer_id')
        location = kwargs.get('location')
        activity_type = kwargs.get('activity_type', 'bilgilendirme')
        people_contacted = kwargs.get('people_contacted', 0)
        duration_minutes = kwargs.get('duration_minutes', 0)
        notes = kwargs.get('notes', '')
        
        # Saha raporu oluştur
        field_report = self.field_tracker.create_field_report(
            volunteer_id=volunteer_id,
            location=location,
            activity_type=activity_type,
            people_contacted=people_contacted,
            duration_minutes=duration_minutes,
            notes=notes
        )
        
        # Gönüllü istatistiklerini güncelle
        if volunteer_id in self.active_volunteers:
            self.active_volunteers[volunteer_id]['total_tasks'] += 1
            self.active_volunteers[volunteer_id]['total_score'] += field_report['performance_score']
        
        # Raporu kaydet
        report_id = f"report_{len(self.field_reports) + 1}"
        self.field_reports[report_id] = field_report
        
        return {
            "operation": "field_report",
            "report_id": report_id,
            "field_report": field_report,
            "timestamp": datetime.now().isoformat()
        }
    
    # ============================================
    # GÖRSEL DOĞRULAMA VE PUANLAMA
    # ============================================
    
    def _validate_visual(self, kwargs: Dict[str, Any]) -> Dict[str, Any]:
        """Görsel doğrulama ve puanlama yapar"""
        
        volunteer_id = kwargs.get('volunteer_id')
        report_id = kwargs.get('report_id')
        image_data = kwargs.get('image_data', None)
        interaction_context = kwargs.get('interaction_context', {})
        
        # Görsel doğrulama
        validation_result = self.visual_validator.validate_image(
            volunteer_id=volunteer_id,
            report_id=report_id,
            image_data=image_data,
            interaction_context=interaction_context
        )
        
        # Raporu güncelle
        if report_id in self.field_reports:
            self.field_reports[report_id]['visual_validation'] = validation_result
            self.field_reports[report_id]['final_score'] = (
                self.field_reports[report_id]['performance_score'] * 0.6 +
                validation_result['visual_score'] * 0.4
            )
        
        return {
            "operation": "visual_validation",
            "validation_result": validation_result,
            "timestamp": datetime.now().isoformat()
        }
    
    # ============================================
    # İMECE PAYI HESAPLAMA
    # ============================================
    
    def _calculate_imece_share(self, kwargs: Dict[str, Any]) -> Dict[str, Any]:
        """İmece Payı hesaplar"""
        
        volunteer_id = kwargs.get('volunteer_id')
        period = kwargs.get('period', 'monthly')
        
        # İmece Payı hesapla
        share_result = self.imece_share_calculator.calculate_share(
            volunteer_id=volunteer_id,
            volunteer_data=self.active_volunteers.get(volunteer_id, {}),
            field_reports=self.field_reports,
            period=period
        )
        
        # Gönüllünün İmece Payını güncelle
        if volunteer_id in self.active_volunteers:
            self.active_volunteers[volunteer_id]['imece_share'] = share_result['total_share']
        
        # İmece Payını kaydet
        share_id = f"share_{len(self.imece_shares) + 1}"
        self.imece_shares[share_id] = share_result
        
        return {
            "operation": "imece_share",
            "share_id": share_id,
            "share_result": share_result,
            "timestamp": datetime.now().isoformat()
        }
    
    # ============================================
    # 7/24 DENETİM VE ÖĞRETME
    # ============================================
    
    def _conduct_audit(self, kwargs: Dict[str, Any]) -> Dict[str, Any]:
        """Denetim ve öğretme yapar"""
        
        volunteer_id = kwargs.get('volunteer_id')
        audit_type = kwargs.get('audit_type', 'performance')
        
        # Denetim yap
        audit_result = self.audit_teaching_system.conduct_audit(
            volunteer_id=volunteer_id,
            volunteer_data=self.active_volunteers.get(volunteer_id, {}),
            field_reports=self.field_reports,
            audit_type=audit_type
        )
        
        # Denetim logunu kaydet
        audit_log = {
            "audit_id": f"audit_{len(self.audit_logs) + 1}",
            "volunteer_id": volunteer_id,
            "audit_result": audit_result,
            "audit_date": datetime.now().isoformat()
        }
        self.audit_logs.append(audit_log)
        
        return {
            "operation": "audit",
            "audit_result": audit_result,
            "timestamp": datetime.now().isoformat()
        }
    
    # ============================================
    # DASHBOARD
    # ============================================
    
    def _get_dashboard(self, kwargs: Dict[str, Any]) -> Dict[str, Any]:
        """Dashboard verilerini döndürür"""
        
        return {
            "operation": "dashboard",
            "total_candidates": len(self.candidates),
            "active_volunteers": len(self.active_volunteers),
            "total_field_reports": len(self.field_reports),
            "total_imece_shares": len(self.imece_shares),
            "total_audits": len(self.audit_logs),
            "candidates": self.candidates,
            "active_volunteers": self.active_volunteers,
            "field_reports": self.field_reports,
            "imece_shares": self.imece_shares,
            "audit_logs": self.audit_logs,
            "timestamp": datetime.now().isoformat()
        }


# ============================================
# ALT SİSTEM SINIFLARI
# ============================================

class InterviewAssistant:
    """AI Mülakat Asistanı"""
    
    def conduct_interview(self, candidate_id: str, candidate_name: str, age: int, 
                         education: str, political_view: str, social_skills: Dict, 
                         kamera_psiko_analiz: Optional[KameraPsikoAnalizAjani] = None,
                         requires_pre_screening: bool = False,
                         requires_character_test: bool = False,
                         user_type: str = 'regular') -> Dict[str, Any]:
        """Mülakat yapar"""
        
        # Sosyal beceri puanlaması
        social_score = self._evaluate_social_skills(social_skills)
        
        # Kamera Psiko Analiz entegrasyonu
        video_analysis_result = None
        if kamera_psiko_analiz:
            # Avatar oluştur
            avatar_result = kamera_psiko_analiz.run(
                operation='create_avatar',
                agent_id=candidate_id,
                agent_name=candidate_name,
                agent_type='genclik_imece',
                personality_traits=social_skills
            )
            
            # Video analizi seansı başlat
            session_result = kamera_psiko_analiz.run(
                operation='start_session',
                session_id=f"interview_{candidate_id}",
                agent_id=candidate_id,
                target_person_id=candidate_id,
                session_type='interview'
            )
            
            video_analysis_result = {
                "avatar_created": avatar_result.get('avatar'),
                "session_started": session_result.get('session_id'),
                "video_analysis_enabled": True
            }
        
        # Eğitim puanlaması
        education_score = self._evaluate_education(education)
        
        # Çeşitlilik puanlaması (siyasi görüş)
        diversity_score = self._evaluate_diversity(political_view)
        
        # Genel puan
        total_score = (social_score * 0.5) + (education_score * 0.3) + (diversity_score * 0.2)
        
        # İşe alım kararı
        is_hired = total_score >= 60
        
        # Mülakat soruları ve yanıtlar
        interview_questions = self._generate_interview_questions()
        
        return {
            "candidate_id": candidate_id,
            "candidate_name": candidate_name,
            "social_score": social_score,
            "education_score": education_score,
            "diversity_score": diversity_score,
            "total_score": total_score,
            "is_hired": is_hired,
            "interview_questions": interview_questions,
            "feedback": self._generate_feedback(total_score, is_hired),
            "video_analysis": video_analysis_result,
            "requires_pre_screening": requires_pre_screening,
            "requires_character_test": requires_character_test,
            "user_type": user_type,
            "timestamp": datetime.now().isoformat()
        }
    
    def _evaluate_social_skills(self, social_skills: Dict) -> float:
        """Sosyal becerileri değerlendirir"""
        
        communication = social_skills.get('communication', 5)
        persuasion = social_skills.get('persuasion', 5)
        community_management = social_skills.get('community_management', 5)
        leadership = social_skills.get('leadership', 5)
        
        return (communication + persuasion + community_management + leadership) / 4 * 20
    
    def _evaluate_education(self, education: str) -> float:
        """Eğitimi değerlendirir"""
        
        education_scores = {
            "ilkokul": 40,
            "ortaokul": 50,
            "lise": 70,
            "üniversite": 90,
            "yüksek_lisans": 95,
            "doktora": 100
        }
        
        return education_scores.get(education.lower(), 60)
    
    def _evaluate_diversity(self, political_view: str) -> float:
        """Çeşitliliği değerlendirir"""
        
        # Siyasi görüş çeşitliliği için yüksek puan
        if political_view.lower() in ['belirtilmemiş', 'diğer', 'bağımsız']:
            return 90
        elif political_view.lower() in ['sağ', 'sol', 'merkez']:
            return 70
        else:
            return 80
    
    def _generate_interview_questions(self) -> List[Dict[str, str]]:
        """Mülakat soruları üretir"""
        
        questions = [
            {
                "question": "Topluluk yönetimi deneyiminiz nedir?",
                "expected_answer": "Önceki deneyimler ve liderlik örnekleri"
            },
            {
                "question": "Farklı görüşlü insanlarla iletişim kurma beceriniz nedir?",
                "expected_answer": "İletişim ve ikna becerileri"
            },
            {
                "question": "Saha çalışmaları için motivasyonunuz nedir?",
                "expected_answer": "Sosyal sorumluluk ve toplum katkısı"
            },
            {
                "question": "Zaman yönetimi ve organizasyon becerileriniz nedir?",
                "expected_answer": "Planlama ve önceliklendirme"
            }
        ]
        
        return questions
    
    def _generate_feedback(self, total_score: float, is_hired: bool) -> str:
        """Geri bildirim üretir"""
        
        if is_hired:
            if total_score >= 85:
                return "Mükemmel profil. Saha çalışmalarında liderlik potansiyeli yüksek."
            elif total_score >= 70:
                return "İyi profil. Saha çalışmalarında başarılı olacaktır."
            else:
                return "Kabul edildi. Gelişim alanları var ancak potansiyel yüksek."
        else:
            return "Maalesef şu an için uygun değil. Gelişim önerileri: İletişim becerilerini güçlendirin, topluluk deneyimi kazanın."


class FieldTracker:
    """Saha Takip Sistemi"""
    
    def create_field_report(self, volunteer_id: str, location: str, activity_type: str,
                           people_contacted: int, duration_minutes: int, notes: str) -> Dict[str, Any]:
        """Saha raporu oluşturur"""
        
        # Performans puanı hesapla
        performance_score = self._calculate_performance_score(
            people_contacted, duration_minutes, activity_type
        )
        
        return {
            "volunteer_id": volunteer_id,
            "location": location,
            "activity_type": activity_type,
            "people_contacted": people_contacted,
            "duration_minutes": duration_minutes,
            "notes": notes,
            "performance_score": performance_score,
            "report_date": datetime.now().isoformat(),
            "visual_validation": None,
            "final_score": performance_score
        }
    
    def _calculate_performance_score(self, people_contacted: int, duration_minutes: int, activity_type: str) -> float:
        """Performans puanı hesaplar"""
        
        # Kişi başına dakika verimliliği
        if duration_minutes > 0:
            efficiency = people_contacted / duration_minutes
        else:
            efficiency = 0
        
        # Aktivite tipi katsayısı
        activity_coefficients = {
            "bilgilendirme": 1.0,
            "kayıt": 1.2,
            "etkinlik": 1.5,
            "eğitim": 1.3
        }
        
        coefficient = activity_coefficients.get(activity_type.lower(), 1.0)
        
        # Temel puan
        base_score = min(100, efficiency * 100 * coefficient)
        
        return min(100, max(0, base_score))


class VisualValidator:
    """Görsel Doğrulama ve Puanlama Motoru"""
    
    def validate_image(self, volunteer_id: str, report_id: str, image_data: Any,
                      interaction_context: Dict) -> Dict[str, Any]:
        """Görseli doğrular ve puanlar"""
        
        # Görsel kalite analizi (mock)
        visual_quality = self._analyze_visual_quality(image_data)
        
        # Etkileşim analizi
        interaction_score = self._analyze_interaction(interaction_context)
        
        # Görsel doğrulama skoru
        visual_score = (visual_quality * 0.6) + (interaction_score * 0.4)
        
        # Doğrulama sonucu
        is_valid = visual_score >= 50
        
        return {
            "volunteer_id": volunteer_id,
            "report_id": report_id,
            "visual_quality": visual_quality,
            "interaction_score": interaction_score,
            "visual_score": visual_score,
            "is_valid": is_valid,
            "feedback": self._generate_visual_feedback(visual_score),
            "timestamp": datetime.now().isoformat()
        }
    
    def _analyze_visual_quality(self, image_data: Any) -> float:
        """Görsel kaliteyi analiz eder"""
        
        # Mock analiz
        if image_data is None:
            return 50  # Görsel yoksa varsayılan puan
        
        # Gerçek uygulamada burada görsel işleme yapılır
        # Şimdilik random puan
        return random.uniform(40, 95)
    
    def _analyze_interaction(self, interaction_context: Dict) -> float:
        """Etkileşimi analiz eder"""
        
        # Etkileşim bağlamı
        engagement_level = interaction_context.get('engagement_level', 'medium')
        conversation_quality = interaction_context.get('conversation_quality', 'good')
        
        engagement_scores = {
            'low': 30,
            'medium': 60,
            'high': 90
        }
        
        conversation_scores = {
            'poor': 30,
            'fair': 50,
            'good': 70,
            'excellent': 90
        }
        
        engagement_score = engagement_scores.get(engagement_level.lower(), 60)
        conversation_score = conversation_scores.get(conversation_quality.lower(), 70)
        
        return (engagement_score + conversation_score) / 2
    
    def _generate_visual_feedback(self, visual_score: float) -> str:
        """Görsel geri bildirim üretir"""
        
        if visual_score >= 80:
            return "Mükemmel görsel ve etkileşim kalitesi."
        elif visual_score >= 60:
            return "İyi görsel kalite, etkileşim yeterli."
        elif visual_score >= 40:
            return "Orta seviye görsel kalite, geliştirme gerekli."
        else:
            return "Düşük görsel kalite, iyileştirme şart."


class ImeceShareCalculator:
    """İmece Payı Hesaplayıcı"""
    
    def calculate_share(self, volunteer_id: str, volunteer_data: Dict, 
                        field_reports: Dict, period: str) -> Dict[str, Any]:
        """İmece Payını hesaplar"""
        
        # Toplam görev sayısı
        total_tasks = volunteer_data.get('total_tasks', 0)
        
        # Toplam performans skoru
        total_score = volunteer_data.get('total_score', 0)
        
        # Ortalama performans
        avg_score = total_score / total_tasks if total_tasks > 0 else 0
        
        # İmece Payı hesaplama
        base_share = total_tasks * 10  # Her görev için 10 birim
        performance_bonus = avg_score * 0.5  # Performans bonusu
        
        total_share = base_share + performance_bonus
        
        # Periyot bazlı ayarlama
        period_multiplier = self._get_period_multiplier(period)
        final_share = total_share * period_multiplier
        
        return {
            "volunteer_id": volunteer_id,
            "period": period,
            "total_tasks": total_tasks,
            "total_score": total_score,
            "avg_score": avg_score,
            "base_share": base_share,
            "performance_bonus": performance_bonus,
            "period_multiplier": period_multiplier,
            "total_share": final_share,
            "share_details": self._generate_share_details(total_tasks, avg_score),
            "timestamp": datetime.now().isoformat()
        }
    
    def _get_period_multiplier(self, period: str) -> float:
        """Periyot çarpanını döndürür"""
        
        multipliers = {
            "weekly": 1.0,
            "monthly": 4.0,
            "quarterly": 12.0
        }
        
        return multipliers.get(period.lower(), 1.0)
    
    def _generate_share_details(self, total_tasks: int, avg_score: float) -> List[str]:
        """İmece Payı detaylarını üretir"""
        
        details = []
        
        if total_tasks >= 20:
            details.append("Yüksek aktivite bonusu: +20 birim")
        elif total_tasks >= 10:
            details.append("Orta aktivite bonusu: +10 birim")
        
        if avg_score >= 80:
            details.append("Üstün performans bonusu: +15 birim")
        elif avg_score >= 60:
            details.append("İyi performans bonusu: +5 birim")
        
        return details


class AuditTeachingSystem:
    """7/24 Denetim ve Öğretme Sistemi"""
    
    def conduct_audit(self, volunteer_id: str, volunteer_data: Dict, 
                     field_reports: Dict, audit_type: str) -> Dict[str, Any]:
        """Denetim yapar"""
        
        # Performans analizi
        performance_analysis = self._analyze_performance(volunteer_data, field_reports)
        
        # Eksik tespiti
        weaknesses = self._identify_weaknesses(performance_analysis)
        
        # Öğretme önerileri
        teaching_recommendations = self._generate_teaching_recommendations(weaknesses)
        
        # Denetim skoru
        audit_score = self._calculate_audit_score(performance_analysis)
        
        return {
            "volunteer_id": volunteer_id,
            "audit_type": audit_type,
            "performance_analysis": performance_analysis,
            "weaknesses": weaknesses,
            "teaching_recommendations": teaching_recommendations,
            "audit_score": audit_score,
            "overall_status": self._determine_status(audit_score),
            "timestamp": datetime.now().isoformat()
        }
    
    def _analyze_performance(self, volunteer_data: Dict, field_reports: Dict) -> Dict[str, Any]:
        """Performansı analiz eder"""
        
        total_tasks = volunteer_data.get('total_tasks', 0)
        total_score = volunteer_data.get('total_score', 0)
        avg_score = total_score / total_tasks if total_tasks > 0 else 0
        
        # Saha raporlarını analiz et
        recent_reports = [r for r in field_reports.values() if r.get('volunteer_id') == volunteer_data.get('volunteer_id')]
        
        recent_performance = [r.get('final_score', 0) for r in recent_reports[-5:]]  # Son 5 rapor
        recent_avg = sum(recent_performance) / len(recent_performance) if recent_performance else 0
        
        return {
            "total_tasks": total_tasks,
            "total_score": total_score,
            "avg_score": avg_score,
            "recent_avg_score": recent_avg,
            "activity_level": self._determine_activity_level(total_tasks),
            "performance_trend": self._determine_performance_trend(avg_score, recent_avg)
        }
    
    def _determine_activity_level(self, total_tasks: int) -> str:
        """Aktivite seviyesini belirler"""
        
        if total_tasks >= 20:
            return "very_high"
        elif total_tasks >= 10:
            return "high"
        elif total_tasks >= 5:
            return "medium"
        else:
            return "low"
    
    def _determine_performance_trend(self, overall_avg: float, recent_avg: float) -> str:
        """Performans trendini belirler"""
        
        if recent_avg > overall_avg + 10:
            return "improving"
        elif recent_avg < overall_avg - 10:
            return "declining"
        else:
            return "stable"
    
    def _identify_weaknesses(self, performance_analysis: Dict) -> List[str]:
        """Eksikleri tespit eder"""
        
        weaknesses = []
        
        activity_level = performance_analysis.get('activity_level', 'medium')
        avg_score = performance_analysis.get('avg_score', 0)
        performance_trend = performance_analysis.get('performance_trend', 'stable')
        
        if activity_level in ['low', 'medium']:
            weaknesses.append("Düşük aktivite seviyesi - Daha fazla saha çalışması gerekli")
        
        if avg_score < 60:
            weaknesses.append("Düşük performans skoru - İletişim becerileri güçlendirilmeli")
        
        if performance_trend == 'declining':
            weaknesses.append("Performans düşüşü - Motivasyon ve eğitim gerekli")
        
        return weaknesses
    
    def _generate_teaching_recommendations(self, weaknesses: List[str]) -> List[str]:
        """Öğretme önerileri üretir"""
        
        recommendations = []
        
        for weakness in weaknesses:
            if "aktivite" in weakness.lower():
                recommendations.append("Zaman planlama ve hedef belirleme eğitimi verin")
            elif "performans" in weakness.lower():
                recommendations.append("İletişim ve ikna teknikleri eğitimi verin")
            elif "düşüş" in weakness.lower():
                recommendations.append("Motivasyon ve liderlik eğitimi verin")
        
        if not weaknesses:
            recommendations.append("Mükemmel performans - Liderlik rolü önerin")
        
        return recommendations
    
    def _calculate_audit_score(self, performance_analysis: Dict) -> float:
        """Denetim skoru hesaplar"""
        
        activity_level = performance_analysis.get('activity_level', 'medium')
        avg_score = performance_analysis.get('avg_score', 0)
        performance_trend = performance_analysis.get('performance_trend', 'stable')
        
        activity_scores = {
            'very_high': 30,
            'high': 25,
            'medium': 20,
            'low': 10
        }
        
        trend_scores = {
            'improving': 20,
            'stable': 15,
            'declining': 5
        }
        
        activity_score = activity_scores.get(activity_level, 15)
        trend_score = trend_scores.get(performance_trend, 10)
        
        total_score = activity_score + (avg_score * 0.5) + trend_score
        
        return min(100, max(0, total_score))
    
    def _determine_status(self, audit_score: float) -> str:
        """Durum belirler"""
        
        if audit_score >= 80:
            return "excellent"
        elif audit_score >= 60:
            return "good"
        elif audit_score >= 40:
            return "needs_improvement"
        else:
            return "critical"


# Test çalıştırması
if __name__ == "__main__":
    agent = GenclikImeceAjani(agent_id=170)
    
    # Test mülakatı
    print("🎓 TEST MÜLAKATI:")
    interview_result = agent.run(
        operation='interview',
        candidate_id='test_001',
        candidate_name='Ahmet Yılmaz',
        age=20,
        education='üniversite',
        political_view='bağımsız',
        social_skills={
            'communication': 8,
            'persuasion': 7,
            'community_management': 9,
            'leadership': 8
        }
    )
    print(json.dumps(interview_result, indent=2, ensure_ascii=False))
    
    # Test saha raporu
    print("\n📍 TEST SAHA RAPORU:")
    field_result = agent.run(
        operation='field_report',
        volunteer_id='test_001',
        location='Kadıköy',
        activity_type='bilgilendirme',
        people_contacted=15,
        duration_minutes=60,
        notes='Başarılı bilgilendirme çalışması'
    )
    print(json.dumps(field_result, indent=2, ensure_ascii=False))
    
    # Test görsel doğrulama
    print("\n📸 TEST GÖRSEL DOĞRULAMA:")
    visual_result = agent.run(
        operation='visual_validation',
        volunteer_id='test_001',
        report_id='report_1',
        image_data=None,
        interaction_context={
            'engagement_level': 'high',
            'conversation_quality': 'excellent'
        }
    )
    print(json.dumps(visual_result, indent=2, ensure_ascii=False))
    
    # Test İmece Payı
    print("\n💰 TEST İMECE PAYI:")
    share_result = agent.run(
        operation='imece_share',
        volunteer_id='test_001',
        period='monthly'
    )
    print(json.dumps(share_result, indent=2, ensure_ascii=False))
    
    # Test denetim
    print("\n🔍 TEST DENETİM:")
    audit_result = agent.run(
        operation='audit',
        volunteer_id='test_001',
        audit_type='performance'
    )
    print(json.dumps(audit_result, indent=2, ensure_ascii=False))
    
    # Dashboard
    print("\n📊 DASHBOARD:")
    dashboard = agent.run(operation='dashboard')
    print(json.dumps(dashboard, indent=2, ensure_ascii=False))
