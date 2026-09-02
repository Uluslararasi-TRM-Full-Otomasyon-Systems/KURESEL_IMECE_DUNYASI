#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Siber Kalkan ve Tehdit Avcısı (Ajan 180) - Siber Güvenlik ve Tehdit Avcısı Modülü
Versiyon: 1.0.0

Hesap güvenliği ve trafik analizi, illegal içerik sızdırma kalkanı,
otomatik izolasyon (güvenli mod) sistemi.
"""

import os
import json
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
from pathlib import Path
import sys
import random

# Path handling for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from trm_agents.base_agent_template import BaseAgent
from trm_agents.system_protocols import CEO_TITLE


class SiberKalkanVeTehditAvcisi(BaseAgent):
    def __init__(self, agent_id: Optional[int] = None):
        super().__init__(
            agent_name="Siber Kalkan ve Tehdit Avcısı",
            agent_id=agent_id if agent_id else 180
        )
        
        # Dosya yolları
        self.guvenlik_loglari_dir = Path("data/siber_kalkan_guvenlik_loglari")
        self.guvenlik_loglari_dir.mkdir(parents=True, exist_ok=True)
        self.guvenlik_dosyasi = self.guvenlik_loglari_dir / "siber_kalkan_guvenlik_loglari.json"
        
        # Güvenlik veritabanı
        self.guvenlik_veritabani = self._guvenlik_veritabani_yukle()
        
        # Tehdit tespit eşikleri
        self.tehdit_esikleri = {
            "anormal_trafik": 100,  # Normalin 100 katı
            "sizma_denemesi": 5,  # 5 başarısız deneme
            "icerik_sizdirma": 3,  # 3 illegal içerik denemesi
            "yetkisiz_erisim": 10  # 10 yetkisiz erişim denemesi
        }
        
        # Illegal içerik anahtar kelimeleri
        self.illegal_icerik_kelimeleri = [
            "bahis", "kumar", "casino", "bet", "slot",
            "dolandırıcılık", "scam", "fraud", "fake",
            "kripto para", "bitcoin", "crypto", "yatırım",
            "kredi", "faiz", "borç", "para kazan"
        ]
        
        # Hesap sayısı
        self.isletme_hesap_sayisi = 6
        
        self.log(f"🛡️ Siber Kalkan ve Tehdit Avcısı (Ajan 180) devrede. Sayın {CEO_TITLE}", "INFO")
    
    def _guvenlik_veritabani_yukle(self) -> Dict[str, Any]:
        """Güvenlik veritabanını yükler"""
        if self.guvenlik_dosyasi.exists():
            with open(self.guvenlik_dosyasi, "r", encoding="utf-8") as f:
                return json.load(f)
        return {
            "hesaplar": {},
            "tehdit_loglari": [],
            "izolasyon_loglari": [],
            "guvenlik_istatistikleri": {
                "toplam_tarama": 0,
                "engellenen_tehdit": 0,
                "izolasyon_sayisi": 0
            }
        }
    
    def _guvenlik_veritabani_kaydet(self):
        """Güvenlik veritabanını kaydeder"""
        with open(self.guvenlik_dosyasi, "w", encoding="utf-8") as f:
            json.dump(self.guvenlik_veritabani, f, indent=4, ensure_ascii=False)
    
    def hesap_ekle(self, hesap_id: str, platform: str, hesap_adi: str, kullanici_id: str):
        """Hesap ekler ve güvenlik izlemeye başlar"""
        hesap_bilgisi = {
            "hesap_id": hesap_id,
            "platform": platform,
            "hesap_adi": hesap_adi,
            "kullanici_id": kullanici_id,
            "olusturma_tarihi": datetime.now().strftime("%Y-%m-%d"),
            "durum": "aktif",
            "trafik_istatistikleri": {
                "normal_trafik": 100,
                "anormal_trafik": 0,
                "sizma_denemesi": 0,
                "yetkisiz_erisim": 0
            },
            "icerik_sizdirma_denemesi": 0,
            "son_tarama": None
        }
        
        self.guvenlik_veritabani["hesaplar"][hesap_id] = hesap_bilgisi
        self._guvenlik_veritabani_kaydet()
        
        self.log(f"🔐 Hesap güvenlik izlemeye alındı: {hesap_adi} ({platform})", "INFO")
        
        return hesap_bilgisi
    
    def trafik_analizi_yap(self, hesap_id: str, trafik_miktari: int) -> Dict[str, Any]:
        """Trafik analizi yapar"""
        hesap = self.guvenlik_veritabani["hesaplar"].get(hesap_id)
        
        if not hesap:
            return {"hata": "Hesap bulunamadı"}
        
        normal_trafik = hesap["trafik_istatistikleri"]["normal_trafik"]
        trafik_orani = trafik_miktari / normal_trafik if normal_trafik > 0 else 0
        
        analiz_sonucu = {
            "hesap_id": hesap_id,
            "analiz_tarihi": datetime.now().isoformat(),
            "trafik_miktari": trafik_miktari,
            "normal_trafik": normal_trafik,
            "trafik_orani": round(trafik_orani, 2),
            "tehdit_durumu": "guvenli"
        }
        
        # Anormal trafik tespiti
        if trafik_orani > self.tehdit_esikleri["anormal_trafik"]:
            analiz_sonucu["tehdit_durumu"] = "tehlikeli"
            analiz_sonucu["tehdit_turu"] = "anormal_trafik"
            hesap["trafik_istatistikleri"]["anormal_trafik"] += 1
            
            self._tehdit_logla(hesap_id, "anormal_trafik", f"Trafik oranı: {trafik_orani}x")
            self.log(f"⚠️ Anormal trafik tespit edildi: {hesap['hesap_adi']}", "WARNING")
        
        hesap["son_tarama"] = datetime.now().isoformat()
        self.guvenlik_veritabani["guvenlik_istatistikleri"]["toplam_tarama"] += 1
        self._guvenlik_veritabani_kaydet()
        
        return analiz_sonucu
    
    def sizma_denemesi_tespit(self, hesap_id: str, ip_adresi: str, deneme_turu: str) -> Dict[str, Any]:
        """Sızma denemesi tespit eder"""
        hesap = self.guvenlik_veritabani["hesaplar"].get(hesap_id)
        
        if not hesap:
            return {"hata": "Hesap bulunamadı"}
        
        hesap["trafik_istatistikleri"]["sizma_denemesi"] += 1
        sizma_sayisi = hesap["trafik_istatistikleri"]["sizma_denemesi"]
        
        tespit_bilgisi = {
            "tespit_id": f"SIZ_{hesap_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "hesap_id": hesap_id,
            "ip_adresi": ip_adresi,
            "deneme_turu": deneme_turu,
            "tespit_tarihi": datetime.now().isoformat(),
            "sizma_sayisi": sizma_sayisi,
            "tehdit_durumu": "guvenli"
        }
        
        # Sızma denemesi eşiği aşıldı mı?
        if sizma_sayisi >= self.tehdit_esikleri["sizma_denemesi"]:
            tespit_bilgisi["tehdit_durumu"] = "tehlikeli"
            tespit_bilgisi["tehdit_turu"] = "sizma_denemesi"
            
            self._tehdit_logla(hesap_id, "sizma_denemesi", f"IP: {ip_adresi}, Deneme: {deneme_turu}")
            self.log(f"🚨 Sızma denemesi tespit edildi: {hesap['hesap_adi']} - IP: {ip_adresi}", "ERROR")
            
            # Otomatik izolasyon
            self._izolasyon_uygula(hesap_id, "sizma_denemesi")
        
        self._guvenlik_veritabani_kaydet()
        
        return tespit_bilgisi
    
    def illegal_icerik_tespit(self, hesap_id: str, icerik: str) -> Dict[str, Any]:
        """Illegal içerik sızdırma tespiti"""
        hesap = self.guvenlik_veritabani["hesaplar"].get(hesap_id)
        
        if not hesap:
            return {"hata": "Hesap bulunamadı"}
        
        icerik_lower = icerik.lower()
        tespit_edilen_kelimeler = []
        
        for kelime in self.illegal_icerik_kelimeleri:
            if kelime in icerik_lower:
                tespit_edilen_kelimeler.append(kelime)
        
        tespit_bilgisi = {
            "tespit_id": f"ICR_{hesap_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "hesap_id": hesap_id,
            "icerik": icerik[:100],  # İlk 100 karakter
            "tespit_edilen_kelimeler": tespit_edilen_kelimeler,
            "tespit_tarihi": datetime.now().isoformat(),
            "tehdit_durumu": "guvenli"
        }
        
        if tespit_edilen_kelimeler:
            hesap["icerik_sizdirma_denemesi"] += 1
            tespit_bilgisi["tehdit_durumu"] = "tehlikeli"
            tespit_bilgisi["tehdit_turu"] = "illegal_icerik"
            
            self._tehdit_logla(hesap_id, "illegal_icerik", f"Kelimeler: {', '.join(tespit_edilen_kelimeler)}")
            self.log(f"⚠️ Illegal içerik tespit edildi: {hesap['hesap_adi']} - {', '.join(tespit_edilen_kelimeler)}", "WARNING")
            
            # Eşik aşıldı mı?
            if hesap["icerik_sizdirma_denemesi"] >= self.tehdit_esikleri["icerik_sizdirma"]:
                self._izolasyon_uygula(hesap_id, "illegal_icerik")
        
        self._guvenlik_veritabani_kaydet()
        
        return tespit_bilgisi
    
    def yetkisiz_erisim_tespit(self, hesap_id: str, ip_adresi: str, kullanici_adi: str) -> Dict[str, Any]:
        """Yetkisiz erişim denemesi tespiti"""
        hesap = self.guvenlik_veritabani["hesaplar"].get(hesap_id)
        
        if not hesap:
            return {"hata": "Hesap bulunamadı"}
        
        hesap["trafik_istatistikleri"]["yetkisiz_erisim"] += 1
        yetkisiz_sayisi = hesap["trafik_istatistikleri"]["yetkisiz_erisim"]
        
        tespit_bilgisi = {
            "tespit_id": f"YTK_{hesap_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "hesap_id": hesap_id,
            "ip_adresi": ip_adresi,
            "kullanici_adi": kullanici_adi,
            "tespit_tarihi": datetime.now().isoformat(),
            "yetkisiz_sayisi": yetkisiz_sayisi,
            "tehdit_durumu": "guvenli"
        }
        
        if yetkisiz_sayisi >= self.tehdit_esikleri["yetkisiz_erisim"]:
            tespit_bilgisi["tehdit_durumu"] = "tehlikeli"
            tespit_bilgisi["tehdit_turu"] = "yetkisiz_erisim"
            
            self._tehdit_logla(hesap_id, "yetkisiz_erisim", f"IP: {ip_adresi}, Kullanıcı: {kullanici_adi}")
            self.log(f"🚨 Yetkisiz erişim tespit edildi: {hesap['hesap_adi']} - IP: {ip_adresi}", "ERROR")
            
            self._izolasyon_uygula(hesap_id, "yetkisiz_erisim")
        
        self._guvenlik_veritabani_kaydet()
        
        return tespit_bilgisi
    
    def _tehdit_logla(self, hesap_id: str, tehdit_turu: str, detay: str):
        """Tehdit loglar"""
        tehdit_logu = {
            "tehdit_id": f"THR_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "hesap_id": hesap_id,
            "tehdit_turu": tehdit_turu,
            "detay": detay,
            "tespit_tarihi": datetime.now().isoformat()
        }
        
        self.guvenlik_veritabani["tehdit_loglari"].append(tehdit_logu)
        self.guvenlik_veritabani["guvenlik_istatistikleri"]["engellenen_tehdit"] += 1
    
    def _izolasyon_uygula(self, hesap_id: str, neden: str):
        """Otomatik izolasyon (güvenli mod) uygular"""
        hesap = self.guvenlik_veritabani["hesaplar"].get(hesap_id)
        
        if not hesap:
            return
        
        izolasyon_bilgisi = {
            "izolasyon_id": f"IZL_{hesap_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "hesap_id": hesap_id,
            "hesap_adi": hesap["hesap_adi"],
            "platform": hesap["platform"],
            "izolasyon_nedeni": neden,
            "izolasyon_tarihi": datetime.now().isoformat(),
            "onceki_durum": hesap["durum"],
            "yeni_durum": "izole_edildi"
        }
        
        hesap["durum"] = "izole_edildi"
        hesap["izolasyon_bilgisi"] = izolasyon_bilgisi
        
        self.guvenlik_veritabani["izolasyon_loglari"].append(izolasyon_bilgisi)
        self.guvenlik_veritabani["guvenlik_istatistikleri"]["izolasyon_sayisi"] += 1
        
        self.log(f"🔒 HESAP İZOLE EDİLDİ: {hesap['hesap_adi']} - Neden: {neden}", "ERROR")
        self.log(f"🚨 ACİL GÜVENLİK ALARMI: İR-SA AŞ. yönetim paneli bilgilendirildi", "ERROR")
    
    def guvenlik_raporu_olustur(self) -> Dict[str, Any]:
        """Güvenlik raporu oluşturur"""
        rapor = {
            "rapor_id": f"GUV_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "rapor_tarihi": datetime.now().isoformat(),
            "raporlayan": f"{self.agent_name} (ID: {self.agent_id})",
            "toplam_hesap": len(self.guvenlik_veritabani["hesaplar"]),
            "aktif_hesap": 0,
            "izole_edilmis_hesap": 0,
            "toplam_tarama": self.guvenlik_veritabani["guvenlik_istatistikleri"]["toplam_tarama"],
            "engellenen_tehdit": self.guvenlik_veritabani["guvenlik_istatistikleri"]["engellenen_tehdit"],
            "izolasyon_sayisi": self.guvenlik_veritabani["guvenlik_istatistikleri"]["izolasyon_sayisi"],
            "tehdit_loglari": self.guvenlik_veritabani["tehdit_loglari"][-10:],  # Son 10 tehdit
            "izolasyon_loglari": self.guvenlik_veritabani["izolasyon_loglari"][-5:]  # Son 5 izolasyon
        }
        
        for hesap_id, hesap in self.guvenlik_veritabani["hesaplar"].items():
            if hesap["durum"] == "aktif":
                rapor["aktif_hesap"] += 1
            elif hesap["durum"] == "izole_edildi":
                rapor["izole_edilmis_hesap"] += 1
        
        self.log(f"📊 Güvenlik raporu oluşturuldu: {rapor['toplam_hesap']} hesap", "INFO")
        
        return rapor
    
    def stop(self) -> Dict[str, Any]:
        self.is_running = False
        self.status = "stopped"
        return {"status": "stopped", "agent_id": self.agent_id}
    
    def restart(self) -> Dict[str, Any]:
        self.status = "ready"
        self.is_running = True
        return {"status": "restarted", "agent_id": self.agent_id}
    
    def run(self, operation: str = "rapor", **kwargs) -> Dict[str, Any]:
        if operation == "hesap_ekle":
            return self.hesap_ekle(
                kwargs.get("hesap_id"),
                kwargs.get("platform"),
                kwargs.get("hesap_adi"),
                kwargs.get("kullanici_id")
            )
        elif operation == "trafik_analizi":
            return self.trafik_analizi_yap(
                kwargs.get("hesap_id"),
                kwargs.get("trafik_miktari")
            )
        elif operation == "sizma_tespit":
            return self.sizma_denemesi_tespit(
                kwargs.get("hesap_id"),
                kwargs.get("ip_adresi"),
                kwargs.get("deneme_turu")
            )
        elif operation == "illegal_icerik":
            return self.illegal_icerik_tespit(
                kwargs.get("hesap_id"),
                kwargs.get("icerik")
            )
        elif operation == "yetkisiz_erisim":
            return self.yetkisiz_erisim_tespit(
                kwargs.get("hesap_id"),
                kwargs.get("ip_adresi"),
                kwargs.get("kullanici_adi")
            )
        elif operation == "rapor":
            return self.guvenlik_raporu_olustur()
        return {"hata": "Bilinmeyen işlem"}


if __name__ == "__main__":
    print("Siber Kalkan ve Tehdit Avcisi Test Basliyor...")
    ajan = SiberKalkanVeTehditAvcisi(agent_id=180)
    
    # Test hesap ekle
    hesap = ajan.run(
        operation="hesap_ekle",
        hesap_id="HES001",
        platform="instagram",
        hesap_adi="test_hesap",
        kullanici_id="K001"
    )
    
    print(f"\nHesap Ekleme Sonucu:")
    print(f"Hesap ID: {hesap['hesap_id']}")
    print(f"Platform: {hesap['platform']}")
    print(f"Durum: {hesap['durum']}")
    
    # Test trafik analizi
    trafik = ajan.run(
        operation="trafik_analizi",
        hesap_id="HES001",
        trafik_miktari=15000  # Anormal trafik
    )
    
    print(f"\nTrafik Analizi Sonucu:")
    print(f"Trafik Oranı: {trafik['trafik_orani']}x")
    print(f"Tehdit Durumu: {trafik['tehdit_durumu']}")
    
    # Test illegal içerik
    icerik = ajan.run(
        operation="illegal_icerik",
        hesap_id="HES001",
        icerik="Bu hesapta kumar ve bahis içerikleri paylaşılmaktadır"
    )
    
    print(f"\nIllegal İçerik Sonucu:")
    print(f"Tespit Edilen Kelimeler: {icerik['tespit_edilen_kelimeler']}")
    print(f"Tehdit Durumu: {icerik['tehdit_durumu']}")
    
    # Güvenlik raporu
    rapor = ajan.run(operation="rapor")
    print(f"\nGüvenlik Raporu:")
    print(f"Toplam Hesap: {rapor['toplam_hesap']}")
    print(f"Aktif Hesap: {rapor['aktif_hesap']}")
    print(f"Engellenen Tehdit: {rapor['engellenen_tehdit']}")
