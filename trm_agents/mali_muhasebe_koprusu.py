#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Mali Muhasebe Köprüsü Ajanı (Financial Bridge Agent)
Uluslararası e-ticaret/affiliate gelirlerini, e-fatura/e-arşiv altyapısını ve 
dijital banka entegrasyonlarını izleyen, SMMM için aylık mali raporlar derleyen otonom ajan
"""

import json
import logging
from typing import Dict, List, Optional
from datetime import datetime, timedelta
from pathlib import Path
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from nirvana_shield_core import NirvanaShieldCore
from ultra_nirvana_guardian import UltraNirvanaGuardian

logger = logging.getLogger(__name__)

class MaliMuhasebeKoprusuAgent:
    def __init__(self, agent_id=161):
        self.agent_id = agent_id
        self.name = f"MaliMuhasebeKoprusu-{agent_id:03d}"
        
        # Veri depolama
        self.income_data = {}  # Affiliate gelirleri
        self.invoice_data = {}  # E-fatura/e-arşiv verileri
        self.bank_integration_data = {}  # Dijital banka entegrasyonları
        self.monthly_reports = {}  # Aylık raporlar
        
        # Güvenlik entegrasyonu
        self.shield = NirvanaShieldCore()
        self.guardian = UltraNirvanaGuardian()
        
        # Circuit Breaker
        self.circuit_breaker_active = False
        self.financial_discrepancy_threshold = 0.05  # %5 uyumsuzluk eşiği
        
        # SMMM ayarları
        self.smmm_contact_info = {
            "email": "",
            "phone": "",
            "report_format": "PDF",
            "report_language": "TR"
        }
        
        # Veri dizinleri
        self.data_dir = Path("data/financial")
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
        logger.info(f"[{self.name}] Mali Muhasebe Köprüsü Ajanı başlatıldı")
    
    # ============================================
    # ULUSLARARASI E-TİCARET/AFFILIATE GELİR İZLEME
    # ============================================
    
    def record_affiliate_income(self, platform: str, amount: float, currency: str, 
                                transaction_id: str, date: str = None) -> Dict:
        """
        Affiliate gelirini kaydet
        """
        if date is None:
            date = datetime.now().isoformat()
        
        # Nirvana Guardian: Risk analizi
        risk_score = self._calculate_transaction_risk(amount, currency)
        quarantine_check = self.guardian.dynamic_agent_quarantine_check(
            f"income_{transaction_id}", risk_score
        )
        
        if not quarantine_check:
            logger.warning(f"[{self.name}] İşlem {transaction_id} karantinaya alındı - yüksek risk")
            return {"status": "quarantined", "reason": "high_risk"}
        
        # Gelir kaydı
        income_record = {
            "platform": platform,
            "amount": amount,
            "currency": currency,
            "transaction_id": transaction_id,
            "date": date,
            "risk_score": risk_score,
            "status": "recorded"
        }
        
        # Döviz dönüşümü (basit implementasyon)
        try_amount = self._convert_to_try(amount, currency)
        income_record["amount_try"] = try_amount
        
        # Aylık kümülatif güncelleme
        month_key = date[:7]  # YYYY-MM
        if month_key not in self.income_data:
            self.income_data[month_key] = []
        
        self.income_data[month_key].append(income_record)
        
        logger.info(f"[{self.name}] Affiliate gelir kaydedildi: {platform} - {amount} {currency} ({try_amount:.2f} TRY)")
        
        return income_record
    
    def _calculate_transaction_risk(self, amount: float, currency: str) -> float:
        """
        İşlem risk skorunu hesapla
        """
        risk = 0.0
        
        # Tutar bazlı risk
        if amount > 10000:
            risk += 0.2
        elif amount > 50000:
            risk += 0.4
        
        # Döviz bazlı risk
        if currency not in ["TRY", "USD", "EUR"]:
            risk += 0.1
        
        return min(risk, 0.9)
    
    def _convert_to_try(self, amount: float, currency: str) -> float:
        """
        Döviz dönüşümü (basit implementasyon - gerçek API entegrasyonu gerekir)
        """
        exchange_rates = {
            "USD": 32.5,
            "EUR": 35.2,
            "GBP": 41.5,
            "TRY": 1.0
        }
        
        rate = exchange_rates.get(currency, 32.5)
        return amount * rate
    
    def get_monthly_income_summary(self, month: str) -> Dict:
        """
        Aylık gelir özetini döndür
        """
        if month not in self.income_data:
            return {"error": "Veri bulunamadı"}
        
        records = self.income_data[month]
        
        summary = {
            "month": month,
            "total_transactions": len(records),
            "total_amount_try": sum(r.get("amount_try", 0) for r in records),
            "by_platform": {},
            "by_currency": {},
            "average_transaction": 0
        }
        
        for record in records:
            platform = record["platform"]
            currency = record["currency"]
            amount_try = record.get("amount_try", 0)
            
            if platform not in summary["by_platform"]:
                summary["by_platform"][platform] = {"count": 0, "total_try": 0}
            summary["by_platform"][platform]["count"] += 1
            summary["by_platform"][platform]["total_try"] += amount_try
            
            if currency not in summary["by_currency"]:
                summary["by_currency"][currency] = {"count": 0, "total_amount": 0}
            summary["by_currency"][currency]["count"] += 1
            summary["by_currency"][currency]["total_amount"] += record["amount"]
        
        if records:
            summary["average_transaction"] = summary["total_amount_try"] / len(records)
        
        return summary
    
    # ============================================
    # E-FATURA/E-ARŞİV İZLEME
    # ============================================
    
    def record_invoice(self, invoice_type: str, invoice_number: str, 
                      amount: float, vat_amount: float, customer_info: Dict) -> Dict:
        """
        E-fatura/e-arşiv kaydı
        """
        invoice_record = {
            "invoice_type": invoice_type,  # "e-fatura" veya "e-arşiv"
            "invoice_number": invoice_number,
            "amount": amount,
            "vat_amount": vat_amount,
            "total_amount": amount + vat_amount,
            "customer_info": customer_info,
            "created_at": datetime.now().isoformat(),
            "status": "recorded"
        }
        
        month_key = datetime.now().strftime("%Y-%m")
        if month_key not in self.invoice_data:
            self.invoice_data[month_key] = []
        
        self.invoice_data[month_key].append(invoice_record)
        
        logger.info(f"[{self.name}] {invoice_type} kaydedildi: {invoice_number} - {invoice_record['total_amount']:.2f} TRY")
        
        return invoice_record
    
    def get_monthly_invoice_summary(self, month: str) -> Dict:
        """
        Aylık fatura özetini döndür
        """
        if month not in self.invoice_data:
            return {"error": "Veri bulunamadı"}
        
        invoices = self.invoice_data[month]
        
        summary = {
            "month": month,
            "total_invoices": len(invoices),
            "total_amount": sum(i["amount"] for i in invoices),
            "total_vat": sum(i["vat_amount"] for i in invoices),
            "total_with_vat": sum(i["total_amount"] for i in invoices),
            "by_type": {"e-fatura": 0, "e-arşiv": 0}
        }
        
        for invoice in invoices:
            summary["by_type"][invoice["invoice_type"]] += 1
        
        return summary
    
    # ============================================
    # DİJİTAL BANKA ENTEGRASYONU İZLEME
    # ============================================
    
    def record_bank_transaction(self, bank: str, transaction_type: str, 
                                amount: float, description: str, reference: str) -> Dict:
        """
        Banka işlemi kaydı
        """
        transaction_record = {
            "bank": bank,
            "transaction_type": transaction_type,  # "credit", "debit", "transfer"
            "amount": amount,
            "description": description,
            "reference": reference,
            "recorded_at": datetime.now().isoformat(),
            "status": "recorded"
        }
        
        month_key = datetime.now().strftime("%Y-%m")
        if month_key not in self.bank_integration_data:
            self.bank_integration_data[month_key] = []
        
        self.bank_integration_data[month_key].append(transaction_record)
        
        logger.info(f"[{self.name}] Banka işlemi kaydedildi: {bank} - {transaction_type} - {amount:.2f} TRY")
        
        return transaction_record
    
    def get_monthly_bank_summary(self, month: str) -> Dict:
        """
        Aylık banka özetini döndür
        """
        if month not in self.bank_integration_data:
            return {"error": "Veri bulunamadı"}
        
        transactions = self.bank_integration_data[month]
        
        summary = {
            "month": month,
            "total_transactions": len(transactions),
            "total_credits": sum(t["amount"] for t in transactions if t["transaction_type"] == "credit"),
            "total_debits": sum(t["amount"] for t in transactions if t["transaction_type"] == "debit"),
            "by_bank": {},
            "net_balance": 0
        }
        
        for transaction in transactions:
            bank = transaction["bank"]
            if bank not in summary["by_bank"]:
                summary["by_bank"][bank] = {"credits": 0, "debits": 0, "count": 0}
            
            if transaction["transaction_type"] == "credit":
                summary["by_bank"][bank]["credits"] += transaction["amount"]
            else:
                summary["by_bank"][bank]["debits"] += transaction["amount"]
            
            summary["by_bank"][bank]["count"] += 1
        
        summary["net_balance"] = summary["total_credits"] - summary["total_debits"]
        
        return summary
    
    # ============================================
    # CIRCUIT BREAKER VE GÜVENLİK MİMARİSİ
    # ============================================
    
    def check_financial_discrepancy(self, month: str) -> Dict:
        """
        Finansal uyumsuzluk kontrolü
        """
        income_summary = self.get_monthly_income_summary(month)
        invoice_summary = self.get_monthly_invoice_summary(month)
        bank_summary = self.get_monthly_bank_summary(month)
        
        discrepancy_report = {
            "month": month,
            "has_discrepancy": False,
            "discrepancies": [],
            "circuit_breaker_triggered": False
        }
        
        # Gelir vs Banka girişi karşılaştırma
        if "total_amount_try" in income_summary and "total_credits" in bank_summary:
            income_total = income_summary["total_amount_try"]
            bank_credits = bank_summary["total_credits"]
            
            if income_total > 0:
                difference = abs(income_total - bank_credits) / income_total
                if difference > self.financial_discrepancy_threshold:
                    discrepancy_report["has_discrepancy"] = True
                    discrepancy_report["discrepancies"].append({
                        "type": "income_bank_mismatch",
                        "income_total": income_total,
                        "bank_credits": bank_credits,
                        "difference_percent": difference * 100
                    })
        
        # Fatura vs Banka çıkışı karşılaştırma
        if "total_with_vat" in invoice_summary and "total_debits" in bank_summary:
            invoice_total = invoice_summary["total_with_vat"]
            bank_debits = bank_summary["total_debits"]
            
            if invoice_total > 0:
                difference = abs(invoice_total - bank_debits) / invoice_total
                if difference > self.financial_discrepancy_threshold:
                    discrepancy_report["has_discrepancy"] = True
                    discrepancy_report["discrepancies"].append({
                        "type": "invoice_bank_mismatch",
                        "invoice_total": invoice_total,
                        "bank_debits": bank_debits,
                        "difference_percent": difference * 100
                    })
        
        # Circuit Breaker tetikleme
        if discrepancy_report["has_discrepancy"]:
            self.trigger_circuit_breaker(discrepancy_report)
            discrepancy_report["circuit_breaker_triggered"] = True
        
        return discrepancy_report
    
    def trigger_circuit_breaker(self, discrepancy_report: Dict):
        """
        Finansal uyumsuzlukta circuit breaker tetikle
        """
        self.circuit_breaker_active = True
        
        logger.error(f"[{self.name}] CIRCUIT BREAKER TETİKLENDİ! Finansal uyumsuzluk tespit edildi")
        for discrepancy in discrepancy_report["discrepancies"]:
            logger.error(f"  - {discrepancy['type']}: {discrepancy['difference_percent']:.2f}% fark")
    
    def reset_circuit_breaker(self):
        """
        Circuit breaker'ı sıfırla
        """
        self.circuit_breaker_active = False
        logger.info(f"[{self.name}] Circuit breaker sıfırlandı")
    
    # ============================================
    # SMMM İÇİN AYLIK DİJİTAL MALİ RAPOR DERLEME
    # ============================================
    
    def generate_monthly_report(self, month: str) -> Dict:
        """
        SMMM için aylık mali rapor oluştur
        """
        # Nirvana Shield: Güvenli rapor oluşturma
        fingerprint = self.shield.get_masked_fingerprint(f"report_{month}")
        
        report = {
            "report_id": f"RPT_{month}_{datetime.now().strftime('%Y%m%d%H%M%S')}",
            "month": month,
            "generated_at": datetime.now().isoformat(),
            "generated_by": self.name,
            "security_fingerprint": fingerprint,
            
            # Gelir özeti
            "income_summary": self.get_monthly_income_summary(month),
            
            # Fatura özeti
            "invoice_summary": self.get_monthly_invoice_summary(month),
            
            # Banka özeti
            "bank_summary": self.get_monthly_bank_summary(month),
            
            # Uyumsuzluk kontrolü
            "discrepancy_check": self.check_financial_discrepancy(month),
            
            # SMMM notları
            "smmm_notes": {
                "report_type": "monthly_financial",
                "compliance_status": "pending_review",
                "recommended_actions": []
            }
        }
        
        # Önerilen eylemler
        if report["discrepancy_check"]["has_discrepancy"]:
            report["smmm_notes"]["recommended_actions"].append("Finansal uyumsuzluk incelemesi gerekiyor")
            report["smmm_notes"]["compliance_status"] = "attention_required"
        else:
            report["smmm_notes"]["recommended_actions"].append("Standart inceleme yeterli")
            report["smmm_notes"]["compliance_status"] = "compliant"
        
        # Raporu kaydet
        self.monthly_reports[month] = report
        
        # Raporu dosyaya yaz
        report_file = self.data_dir / f"monthly_report_{month}.json"
        with open(report_file, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        logger.info(f"[{self.name}] Aylık rapor oluşturuldu: {month}")
        
        return report
    
    def export_report_for_smmm(self, month: str, format: str = "JSON") -> str:
        """
        SMMM için raporu dışa aktar
        """
        if month not in self.monthly_reports:
            report = self.generate_monthly_report(month)
        else:
            report = self.monthly_reports[month]
        
        if format == "JSON":
            report_file = self.data_dir / f"smmm_report_{month}.json"
            with open(report_file, "w", encoding="utf-8") as f:
                json.dump(report, f, indent=2, ensure_ascii=False)
            return str(report_file)
        
        elif format == "CSV":
            # Basit CSV dışa aktarım
            import csv
            csv_file = self.data_dir / f"smmm_report_{month}.csv"
            
            with open(csv_file, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(["Kategori", "Anahtar", "Değer"])
                
                for key, value in report.items():
                    if isinstance(value, dict):
                        for sub_key, sub_value in value.items():
                            writer.writerow([key, sub_key, sub_value])
                    else:
                        writer.writerow([key, "", value])
            
            return str(csv_file)
        
        return str(self.data_dir / f"smmm_report_{month}.json")
    
    def set_smmm_contact_info(self, email: str, phone: str = "", report_format: str = "PDF"):
        """
        SMMM iletişim bilgilerini ayarla
        """
        self.smmm_contact_info = {
            "email": email,
            "phone": phone,
            "report_format": report_format,
            "updated_at": datetime.now().isoformat()
        }
        logger.info(f"[{self.name}] SMMM iletişim bilgileri güncellendi: {email}")
    
    def schedule_monthly_report(self, day_of_month: int = 1) -> Dict:
        """
        Aylık rapor zamanlaması oluştur
        """
        schedule = {
            "scheduled_day": day_of_month,
            "next_report_date": self._get_next_report_date(day_of_month),
            "auto_send_to_smmm": bool(self.smmm_contact_info["email"]),
            "smmm_contact": self.smmm_contact_info
        }
        
        logger.info(f"[{self.name}] Aylık rapor zamanlandı: Her ayın {day_of_month}. günü")
        
        return schedule
    
    def _get_next_report_date(self, day_of_month: int) -> str:
        """
        Bir sonraki rapor tarihini hesapla
        """
        today = datetime.now()
        next_month = today.replace(day=1) + timedelta(days=32)
        next_month = next_month.replace(day=day_of_month)
        return next_month.isoformat()
    
    def save_data(self):
        """
        Tüm verileri kaydet
        """
        data = {
            "income_data": self.income_data,
            "invoice_data": self.invoice_data,
            "bank_integration_data": self.bank_integration_data,
            "monthly_reports": self.monthly_reports,
            "smmm_contact_info": self.smmm_contact_info,
            "saved_at": datetime.now().isoformat()
        }
        
        data_file = self.data_dir / "mali_muhasebe_data.json"
        with open(data_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        logger.info(f"[{self.name}] Veriler kaydedildi")
    
    def load_data(self):
        """
        Kaydedilmiş verileri yükle
        """
        data_file = self.data_dir / "mali_muhasebe_data.json"
        
        if data_file.exists():
            with open(data_file, "r", encoding="utf-8") as f:
                data = json.load(f)
            
            self.income_data = data.get("income_data", {})
            self.invoice_data = data.get("invoice_data", {})
            self.bank_integration_data = data.get("bank_integration_data", {})
            self.monthly_reports = data.get("monthly_reports", {})
            self.smmm_contact_info = data.get("smmm_contact_info", self.smmm_contact_info)
            
            logger.info(f"[{self.name}] Veriler yüklendi")

# Test çalıştırması
if __name__ == "__main__":
    agent = MaliMuhasebeKoprusuAgent()
    
    # Test gelir kaydı
    agent.record_affiliate_income("Amazon", 1500.50, "USD", "TXN001")
    agent.record_affiliate_income("ClickBank", 850.00, "EUR", "TXN002")
    
    # Test fatura kaydı
    agent.record_invoice("e-fatura", "FTR2024001", 5000.00, 950.00, {"name": "Test Müşteri", "tax_no": "1234567890"})
    
    # Test banka işlemi
    agent.record_bank_transaction("Garanti", "credit", 50000.00, "Affiliate ödemesi", "REF001")
    
    # Aylık rapor oluştur
    month = datetime.now().strftime("%Y-%m")
    report = agent.generate_monthly_report(month)
    
    print(json.dumps(report, indent=2, ensure_ascii=False))
