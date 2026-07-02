#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Otonom Etkileşim Swarm Ajanı - TRM Otonom Ekosistemi
İnsan Benzeri Etkileşim Swarm Sistemi
"""

import os
import json
import logging
import random
import time
from datetime import datetime
from dataclasses import dataclass, asdict
from typing import List

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class SwarmUyesi:
    """Swarm üyesi yapısı"""
    uye_id: str
    sosyal_medya_hesabi: str
    etkilesim_turu: str
    gecikme_araligi: tuple  # (min, max) saniye
    insani_davranis_skoru: float
    anti_bot_koruma: str
    son_aktivite: str

@dataclass
class EtkilesimKaydi:
    """Etkileşim kaydı yapısı"""
    kayit_id: str
    uye_id: str
    video_url: str
    etkilesim_turu: str
    zamanlama: str
    fare_rotasi: str
    video_izleme_suresi: float
    anti_bot_puani: float
    kayit_zamani: str

class OtonomEtkilesimSwarmAjani:
    """Otonom etkileşim swarm ajanı - insan benzeri davranış"""
    
    def __init__(self):
        self.swarm_dosyasi = "swarm_uyeleri.json"
        self.etkilesim_dosyasi = "etkilesim_kayitlari.json"
        self.pilot_grup_boyutu = 10
        self.etkilesim_turleri = ["BEGENI", "YORUM", "KAYDETME", "PAYLASIM"]
        self.anti_bot_korumalari = ["YUKSEK", "ORTA", "DUSUK"]
    
    def swarm_uyesi_olustur(self, uye_id, sosyal_medya_hesabi):
        """Swarm üyesi oluştur"""
        return SwarmUyesi(
            uye_id=uye_id,
            sosyal_medya_hesabi=sosyal_medya_hesabi,
            etkilesim_turu=random.choice(self.etkilesim_turleri),
            gecikme_araligi=(random.randint(3, 8), random.randint(10, 20)),
            insani_davranis_skoru=random.uniform(0.85, 0.99),
            anti_bot_koruma=random.choice(self.anti_bot_korumalari),
            son_aktivite=""
        )
    
    def pilot_grup_swarm_olustur(self):
        """10 kişilik pilot grup swarm oluştur"""
        sosyal_medya_hesaplari = [
            "@pilot1", "@pilot2", "@pilot3", "@pilot4", "@pilot5",
            "@pilot6", "@pilot7", "@pilot8", "@pilot9", "@pilot10"
        ]
        
        swarm_uyeleri = []
        for i, hesap in enumerate(sosyal_medya_hesaplari):
            uye = self.swarm_uyesi_olustur(f"SWM-{i+1:03d}", hesap)
            swarm_uyeleri.append(uye)
        
        self.swarm_kaydet(swarm_uyeleri)
        logger.info(f"Pilot grup swarm oluşturuldu: {len(swarm_uyeleri)} üye")
        return swarm_uyeleri
    
    def swarm_kaydet(self, uyeler):
        """Swam üyelerini kaydet"""
        try:
            uye_dict_listesi = [asdict(uye) for uye in uyeler]
            
            with open(self.swarm_dosyasi, 'w', encoding='utf-8') as f:
                json.dump(uye_dict_listesi, f, ensure_ascii=False, indent=2)
        except Exception as e:
            logger.error(f"Swarm kayıt hatası: {e}")
    
    def swarm_yukle(self):
        """Swam üyelerini yükle"""
        try:
            if not os.path.exists(self.swarm_dosyasi):
                return []
            
            with open(self.swarm_dosyasi, 'r', encoding='utf-8') as f:
                uye_dict_listesi = json.load(f)
            
            return [SwarmUyesi(**uye) for uye in uye_dict_listesi]
        except Exception as e:
            logger.error(f"Swarm yükleme hatası: {e}")
            return []
    
    def insani_fare_rotasi_olustur(self):
        """İnsan benzeri fare rotası oluştur"""
        rota_tipleri = [
            "BEZIER_CURVE", "RANDOM_WALK", "HUMAN_LIKE", "NATURAL_PATH"
        ]
        return random.choice(rota_tipleri)
    
    def rastgele_gecikme_uygula(self, uye):
        """Rastgele gecikme uygula"""
        min_gecikme, max_gecikme = uye.gecikme_araligi
        return random.uniform(min_gecikme, max_gecikme)
    
    def video_izleme_simulasyonu(self):
        """Video izleme simülasyonu"""
        # Videoyu baştan sona izleme simülasyonu
        izleme_suresi = random.uniform(15.0, 45.0)  # 15-45 saniye
        tamamlama_orani = random.uniform(0.7, 1.0)  # %70-%100 tamamlama
        
        return {
            "izleme_suresi": izleme_suresi,
            "tamamlama_orani": tamamlama_orani,
            "tam_izlendi": tamamlama_orani >= 0.9
        }
    
    def etkilesim_tetikle(self, uye, video_url):
        """Etkileşim tetikle"""
        try:
            gecikme = self.rastgele_gecikme_uygula(uye)
            time.sleep(gecikme)  # Gerçek gecikme simülasyonu
            
            fare_detayi = self.insani_fare_rotasi_olustur()
            video_detay = self.video_izleme_simulasyonu()
            
            kayit = EtkilesimKaydi(
                kayit_id=f"ETK-{datetime.now().strftime('%Y%m%d%H%M%S')}-{random.randint(1000, 9999)}",
                uye_id=uye.uye_id,
                video_url=video_url,
                etkilesim_turu=uye.etkilesim_turu,
                zamanlama=f"{gecikme:.2f}s",
                fare_rotasi=fare_detayi,
                video_izleme_suresi=video_detay["izleme_suresi"],
                anti_bot_puani=uye.insani_davranis_skoru,
                kayit_zamani=datetime.now().isoformat()
            )
            
            # Üyenin son aktivitesini güncelle
            uye.son_aktivite = datetime.now().isoformat()
            
            self.etkilesim_kaydet(kayit)
            logger.info(f"Etkileşim tetiklendi: {uye.uye_id} -> {uye.etkilesim_turu}")
            
            return kayit
        except Exception as e:
            logger.error(f"Etkileşim tetikleme hatası: {e}")
            return None
    
    def etkilesim_kaydet(self, kayit):
        """Etkileşim kaydı"""
        try:
            kayitlar = self.etkilesim_kayitlarini_oku()
            kayitlar.append(asdict(kayit))
            
            with open(self.etkilesim_dosyasi, 'w', encoding='utf-8') as f:
                json.dump(kayitlar, f, ensure_ascii=False, indent=2)
        except Exception as e:
            logger.error(f"Etkileşim kayıt hatası: {e}")
    
    def etkilesim_kayitlarini_oku(self):
        """Etkileşim kayıtlarını oku"""
        try:
            if not os.path.exists(self.etkilesim_dosyasi):
                return []
            
            with open(self.etkilesim_dosyasi, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Etkileşim kayıt okuma hatası: {e}")
            return []
    
    def video_paylasim_sinyali(self, video_url):
        """Video paylaşım sinyali - swarm tetikleme"""
        uyeler = self.swarm_yukle()
        
        if not uyeler:
            uyeler = self.pilot_grup_swarm_olustur()
        
        tetiklenenler = []
        for uye in uyeler:
            # Her üye farklı zamanlamada tetiklenir
            kayit = self.etkilesim_tetikle(uye, video_url)
            if kayit:
                tetiklenenler.append(kayit)
        
        # Güncellenmiş swarm'ı kaydet
        self.swarm_kaydet(uyeler)
        
        logger.info(f"Video paylaşım sinyali: {len(tetiklenenler)} etkileşim tetiklendi")
        return tetiklenenler
    
    def swarm_istatistikleri(self):
        """Swarm istatistikleri"""
        uyeler = self.swarm_yukle()
        kayitlar = self.etkilesim_kayitlarini_oku()
        
        toplam_uye = len(uyeler)
        toplam_etkilesim = len(kayitlar)
        
        etkilesim_turu_bazli = {}
        for kayit in kayitlar:
            tur = kayit.get("etkilesim_turu", "BILINMIYOR")
            if tur not in etkilesim_turu_bazli:
                etkilesim_turu_bazli[tur] = 0
            etkilesim_turu_bazli[tur] += 1
        
        ortalama_anti_bot_puani = 0.0
        if uyeler:
            ortalama_anti_bot_puani = sum(u.insani_davranis_skoru for u in uyeler) / len(uyeler)
        
        return {
            "toplam_uye": toplam_uye,
            "toplam_etkilesim": toplam_etkilesim,
            "etkilesim_turu_bazli": etkilesim_turu_bazli,
            "ortalama_anti_bot_puani": f"{ortalama_anti_bot_puani:.3f}",
            "aktif_uye_sayisi": sum(1 for u in uyeler if u.son_aktivite)
        }

if __name__ == "__main__":
    # Test
    ajan = OtonomEtkilesimSwarmAjani()
    uyeler = ajan.pilot_grup_swarm_olustur()
    tetiklenenler = ajan.video_paylasim_sinyali("https://example.com/video1")
    print(f"Tetiklenen etkileşimler: {len(tetiklenenler)}")
