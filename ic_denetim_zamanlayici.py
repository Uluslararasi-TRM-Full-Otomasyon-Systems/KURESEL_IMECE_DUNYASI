#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
İç Denetim Zamanlayıcı
Her ayın 1'inde otomatik olarak İç Denetim Ajanını tetikler
"""

import time
import schedule
import logging
from datetime import datetime
from trm_agents.ic_denetim_ajani import IcDenetimAjani

# Log yapılandırması
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] [%(name)s] %(levelname)s: %(message)s'
)
logger = logging.getLogger(__name__)

class IcDenetimZamanlayici:
    def __init__(self):
        self.ajan = IcDenetimAjani(agent_id=175)
        self.calisiyor = False
        
    def aylik_denetim_tetikle(self):
        """Aylık denetimi tetikler"""
        logger.info("🔔 Aylık denetim tetikleniyor...")
        sonuc = self.ajan.denetim_yap()
        logger.info(f"📊 Denetim tamamlandı: {sonuc['genel_degerlendirme']}")
        return sonuc
    
    def baslat(self):
        """Zamanlayıcıyı başlatır"""
        logger.info("⏰ İç Denetim Zamanlayıcı başlatılıyor...")
        
        # Her ayın 1'inde saat 00:00'da tetikle
        schedule.every().month.do(self.aylik_denetim_tetikle).at("00:00")
        
        self.calisiyor = True
        logger.info("✅ Zamanlayıcı aktif - Her ayın 1'inde denetim yapılacak")
        
        # Ana döngü
        while self.calisiyor:
            schedule.run_pending()
            time.sleep(60)  # Her dakika kontrol et
    
    def durdur(self):
        """Zamanlayıcıyı durdurur"""
        self.calisiyor = False
        schedule.clear()
        logger.info("⏹️ Zamanlayıcı durduruldu")
    
    def manuel_denetim(self):
        """Manuel denetim tetikler"""
        logger.info("🔨 Manuel denetim tetikleniyor...")
        return self.aylik_denetim_tetikle()

if __name__ == "__main__":
    import sys
    
    zamanlayici = IcDenetimZamanlayici()
    
    if len(sys.argv) > 1 and sys.argv[1] == "--manuel":
        # Manuel denetim
        sonuc = zamanlayici.manuel_denetim()
        print(f"\n📊 Denetim Sonucu: {sonuc['genel_degerlendirme']}")
        print(f"📋 Durum: {sonuc['durum']}")
        print(f"📁 Rapor Dosyası: {sonuc.get('rapor_dosyasi', 'Oluşturulmadı')}")
    else:
        # Otomatik zamanlayıcı
        try:
            zamanlayici.baslat()
        except KeyboardInterrupt:
            zamanlayici.durdur()
            print("\n⏹️ Zamanlayıcı kullanıcı tarafından durduruldu")
