#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Küresel Konumlandırma Ajanı - TRM Otonom Ekosistemi
"""

import json
import logging
from datetime import datetime
from dataclasses import dataclass, asdict

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class KonumVerisi:
    """Konum verisi yapısı"""
    ulke: str
    sehir: str
    enlem: float
    boylam: float
    komisyon_orani: float
    link_aktif: bool
    kayit_tarihi: str

class KureselKonumlandirmaAjani:
    """Küresel konumlandırma ve komisyon yönetimi ajanı"""
    
    def __init__(self):
        self.konum_dosyasi = "konum_verileri.json"
        self.komisyon_dosyasi = "komisyon_raporlari.json"
    
    def konum_verisi_yukle(self):
        """Konum verilerini yükle"""
        try:
            with open(self.konum_dosyasi, 'r', encoding='utf-8') as f:
                veriler = json.load(f)
            return veriler
        except FileNotFoundError:
            return []
        except Exception as e:
            logger.error(f"Konum verisi yükleme hatası: {e}")
            return []
    
    def konum_kaydet(self, konum: KonumVerisi):
        """Yeni konum kaydet"""
        try:
            veriler = self.konum_verisi_yukle()
            veriler.append(asdict(konum))
            
            with open(self.konum_dosyasi, 'w', encoding='utf-8') as f:
                json.dump(veriler, f, ensure_ascii=False, indent=2)
            
            logger.info(f"Konum kaydedildi: {konum.ulke} - {konum.sehir}")
            return True
        except Exception as e:
            logger.error(f"Konum kaydetme hatası: {e}")
            return False
    
    def komisyon_hesapla(self, tutar: float, ulke: str) -> float:
        """Ülkeye göre komisyon hesapla"""
        komisyon_oranlari = {
            'TR': 0.05,  # Türkiye %5
            'US': 0.08,  # ABD %8
            'EU': 0.07,  # Avrupa %7
            'OTHER': 0.10  # Diğer %10
        }
        
        oran = komisyon_oranlari.get(ulke, komisyon_oranlari['OTHER'])
        return tutar * oran
    
    def tum_konumlari_listele(self):
        """Tüm konumları listele"""
        return self.konum_verisi_yukle()
    
    def pilot_grup_konumlari_olustur(self):
        """10 kişilik pilot grup için demo konum verileri oluştur"""
        pilot_konumlari = [
            KonumVerisi("TR", "İstanbul", 41.0082, 28.9784, 5.0, True, datetime.now().isoformat()),
            KonumVerisi("TR", "Ankara", 39.9334, 32.8597, 5.0, True, datetime.now().isoformat()),
            KonumVerisi("US", "New York", 40.7128, -74.0060, 8.0, True, datetime.now().isoformat()),
            KonumVerisi("EU", "Berlin", 52.5200, 13.4050, 7.0, True, datetime.now().isoformat()),
            KonumVerisi("TR", "İzmir", 38.4237, 27.1428, 5.0, True, datetime.now().isoformat()),
            KonumVerisi("US", "Los Angeles", 34.0522, -118.2437, 8.0, True, datetime.now().isoformat()),
            KonumVerisi("EU", "Paris", 48.8566, 2.3522, 7.0, True, datetime.now().isoformat()),
            KonumVerisi("TR", "Bursa", 40.1885, 29.0610, 5.0, True, datetime.now().isoformat()),
            KonumVerisi("US", "Chicago", 41.8781, -87.6298, 8.0, True, datetime.now().isoformat()),
            KonumVerisi("EU", "London", 51.5074, -0.1278, 7.0, True, datetime.now().isoformat())
        ]
        
        for konum in pilot_konumlari:
            self.konum_kaydet(konum)
        
        logger.info("10 kişilik pilot grup konum verileri oluşturuldu")
