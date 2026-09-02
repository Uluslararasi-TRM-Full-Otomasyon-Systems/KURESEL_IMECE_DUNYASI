
import random
import time

def random_delay(min_sec=5, max_sec=60):
    time.sleep(random.uniform(min_sec, max_sec))

def get_user_agent():
    return random.choice([
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) Chrome/120.0.0.0"
    ])

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Coğrafi Arbitraj Ajanı - TRM Otonom Ekosistemi (164. Ajan)
Saat Dilimi ve Alım Gücü Gözetimi
"""

import os
import json
import logging
import random
from datetime import datetime, timezone, timedelta
from dataclasses import dataclass, asdict
import pytz

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class CoğrafiPazar:
    """Coğrafi pazar yapısı"""
    ulke: str
    saat_dilimi: str
    alim_gucu_index: float
    prime_time_baslangic: str
    prime_time_bitis: str
    aktif_durum: str
    son_tetikleme: str

class CoğrafiArbitrajAjani:
    """Coğrafi arbitraj ajanı - saat dilimi ve alım gücü gözetimi"""
    
    def __init__(self):
        self.pazar_dosyasi = "cografi_pazarlar.json"
        self.tetikleme_dosyasi = "tetikleme_kayitlari.json"
        self.pazarlar = self.pazarlari_tanimla()
    
    def pazarlari_tanimla(self):
        """Coğrafi pazarları tanımla"""
        return [
            CoğrafiPazar(
                ulke="ABD",
                saat_dilimi="America/New_York",
                alim_gucu_index=95.5,
                prime_time_baslangic="19:00",
                prime_time_bitis="23:00",
                aktif_durum="BEKLEMEDE",
                son_tetikleme=""
            ),
            CoğrafiPazar(
                ulke="Almanya",
                saat_dilimi="Europe/Berlin",
                alim_gucu_index=88.3,
                prime_time_baslangic="20:00",
                prime_time_bitis="23:00",
                aktif_durum="BEKLEMEDE",
                son_tetikleme=""
            ),
            CoğrafiPazar(
                ulke="Fransa",
                saat_dilimi="Europe/Paris",
                alim_gucu_index=85.7,
                prime_time_baslangic="20:00",
                prime_time_bitis="23:00",
                aktif_durum="BEKLEMEDE",
                son_tetikleme=""
            ),
            CoğrafiPazar(
                ulke="İngiltere",
                saat_dilimi="Europe/London",
                alim_gucu_index=82.1,
                prime_time_baslangic="19:00",
                prime_time_bitis="22:00",
                aktif_durum="BEKLEMEDE",
                son_tetikleme=""
            ),
            CoğrafiPazar(
                ulke="Kanada",
                saat_dilimi="America/Toronto",
                alim_gucu_index=79.8,
                prime_time_baslangic="19:00",
                prime_time_bitis="22:00",
                aktif_durum="BEKLEMEDE",
                son_tetikleme=""
            )
        ]
    
    def saat_dilimi_kontrol(self, pazar):
        """Pazarın saat dilimini kontrol et"""
        try:
            tz = pytz.timezone(pazar.saat_dilimi)
            simdiki_zaman = datetime.now(tz)
            saat = simdiki_zaman.strftime("%H:%M")
            
            baslangic = pazar.prime_time_baslangic
            bitis = pazar.prime_time_bitis
            
            if baslangic <= saat <= bitis:
                return True, saat
            return False, saat
        except Exception as e:
            logger.error(f"Saat dilimi kontrol hatası: {e}")
            return False, "00:00"
    
    def prime_time_tetikle(self, pazar):
        """Prime Time tetikleme"""
        try:
            tetikleme_zamani = datetime.now().isoformat()
            pazar.aktif_durum = "TETIKLENDI"
            pazar.son_tetikleme = tetikleme_zamani
            
            # Tetikleme kaydı oluştur
            tetikleme_kaydi = {
                "ulke": pazar.ulke,
                "tetikleme_zamani": tetikleme_zamani,
                "tetikleme_turu": "PRIME_TIME",
                "hedef_kitle": f"{pazar.ulke} Prime Time",
                "alinan_eylem": "Sosyal medya paylaşımı tetiklendi"
            }
            
            self.tetikleme_kaydet(tetikleme_kaydi)
            logger.info(f"Prime Time tetiklendi: {pazar.ulke}")
            
            return tetikleme_kaydi
        except Exception as e:
            logger.error(f"Prime Time tetikleme hatası: {e}")
            return None
    
    def tetikleme_kaydet(self, tetikleme):
        """Tetikleme kaydı"""
        try:
            kayitlar = self.tetikleme_kayitlarini_oku()
            kayitlar.append(tetikleme)
            
            with open(self.tetikleme_dosyasi, 'w', encoding='utf-8') as f:
                json.dump(kayitlar, f, ensure_ascii=False, indent=2)
        except Exception as e:
            logger.error(f"Tetikleme kayıt hatası: {e}")
    
    def tetikleme_kayitlarini_oku(self):
        """Tetikleme kayıtlarını oku"""
        try:
            if not os.path.exists(self.tetikleme_dosyasi):
                return []
            
            with open(self.tetikleme_dosyasi, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Tetikleme kayıt okuma hatası: {e}")
            return []
    
    def pazarlari_kaydet(self):
        """Pazarları kaydet"""
        try:
            pazar_dict_listesi = [asdict(pazar) for pazar in self.pazarlar]
            
            with open(self.pazar_dosyasi, 'w', encoding='utf-8') as f:
                json.dump(pazar_dict_listesi, f, ensure_ascii=False, indent=2)
        except Exception as e:
            logger.error(f"Pazar kayıt hatası: {e}")
    
    def tum_pazarlari_yukle(self):
        """Tüm pazarları yükle"""
        try:
            if not os.path.exists(self.pazar_dosyasi):
                return self.pazarlar
            
            with open(self.pazar_dosyasi, 'r', encoding='utf-8') as f:
                pazar_dict_listesi = json.load(f)
            
            return [CoğrafiPazar(**pazar) for pazar in pazar_dict_listesi]
        except Exception as e:
            logger.error(f"Pazar yükleme hatası: {e}")
            return self.pazarlar
    
    def gozetim_dongusu_7_24(self):
        """7/24 gözetim döngüsü"""
        self.pazarlar = self.tum_pazarlari_yukle()
        
        tetiklenenler = []
        for pazar in self.pazarlar:
            prime_time_aktif, saat = self.saat_dilimi_kontrol(pazar)
            
            if prime_time_aktif and pazar.aktif_durum == "BEKLEMEDE":
                tetikleme = self.prime_time_tetikle(pazar)
                if tetikleme:
                    tetiklenenler.append(tetikleme)
            elif not prime_time_aktif:
                pazar.aktif_durum = "BEKLEMEDE"
        
        self.pazarlari_kaydet()
        return tetiklenenler
    
    def pazar_istatistikleri(self):
        """Pazar istatistikleri"""
        tetiklemeler = self.tetikleme_kayitlarini_oku()
        
        ulke_bazli_tetikleme = {}
        for tetikleme in tetiklemeler:
            ulke = tetikleme["ulke"]
            if ulke not in ulke_bazli_tetikleme:
                ulke_bazli_tetikleme[ulke] = 0
            ulke_bazli_tetikleme[ulke] += 1
        
        return {
            "toplam_tetikleme": len(tetiklemeler),
            "ulke_bazli_tetikleme": ulke_bazli_tetikleme,
            "aktif_pazar_sayisi": sum(1 for p in self.pazarlar if p.aktif_durum == "TETIKLENDI"),
            "toplam_pazar": len(self.pazarlar)
        }

if __name__ == "__main__":
    # Test
    ajan = CoğrafiArbitrajAjani()
    tetiklenenler = ajan.gozetim_dongusu_7_24()
    print(f"Tetiklenen pazarlar: {len(tetiklenenler)}")
