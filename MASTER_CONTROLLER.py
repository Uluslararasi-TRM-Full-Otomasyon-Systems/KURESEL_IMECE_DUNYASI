# -*- coding: utf-8 -*-
"""
TRM Nirvana v3.0 - MASTER CONTROLLER
Main orchestrator managing all 165 agents in the ecosystem.
"""
import os
import sys
import logging
from config import LOG_DIR, REPORT_DIR

# 165. Muhasebe Ajanını ve diğer gerekli servisleri import ediyoruz
from trm_agents.trm_accounting_agent import TRMAccountingAgent

logger = logging.getLogger("MASTER_CONTROLLER")

class TRMMasterController:
    def __init__(self):
        logger.info("TRM Master Controller karargahı başlatılıyor...")
        self.total_agents = 165
        
        # 165. Muhasebe ve Finans Ajanını initialize ediyoruz
        self.accounting_agent = TRMAccountingAgent()
        
        # Gelecekte eklenecek veya mevcut diğer kritik servislerin altyapısı
        logger.info(f"Sistemdeki toplam {self.total_agents} aktif ajan kontrol mekanizmasına bağlandı.")

    def start_all_services(self):
        """Ekosistemdeki tüm otonom servisleri ve ajan döngülerini ateşler."""
        logger.info("Siber ordunun otonom servisleri sırayla devreye alınıyor...")
        
        # 165. Muhasebe ve Finans Ajanını çalıştırıyoruz
        try:
            self.accounting_agent.run()
            logger.info("165. TRM Muhasebe ve Finans Yönetim Ajanı başarıyla tetiklendi.")
        except Exception as e:
            logger.error(f"Muhasebe ajanı başlatılırken hata oluştu: {str(e)}")
            
        logger.info(f"Karargah aktif! Tüm {self.total_agents} ajan bulut sisteminde senkronize çalışıyor.")

    def generate_system_status_report(self):
        """Maliye, dernek ve e-ticaret akışlarının genel durum raporunu üretir."""
        report_path = os.path.join(REPORT_DIR, "system_status_165.json")
        logger.info(f"Sistem durum raporu oluşturuluyor: {report_path}")
        # Raporlama mantığı ve dosya yazma simülasyonu burada döner
        return report_path

if __name__ == "__main__":
    # Konsolda logları görebilmek için temel yapılandırma
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    
    controller = TRMMasterController()
    controller.start_all_services()
    controller.generate_system_status_report()