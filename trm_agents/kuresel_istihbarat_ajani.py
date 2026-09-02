#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Küresel İstihbarat Ajanı (Ajan 176) - Nirvana Modülü & Küresel Gümrük/Hukuk Matrisi
Versiyon: 2.0.0

Dünyadaki tüm büyük afiliye e-ticaret ağlarından ürün tarar, tüm hedef ülkeler için
gümrük ve mevzuat denetimi yapar, hukuki uyum köprüsü kurar ve her pazar için
ayrı yasal risk skoru üretir.
"""

import os
import json
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime
from pathlib import Path
import sys

# Path handling for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from trm_agents.base_agent_template import BaseAgent
from trm_agents.hukuki_uyum_ajani import HukukiUyumAjani
from trm_agents.system_protocols import CEO_TITLE


class KureselIstihbaratAjani(BaseAgent):
    def __init__(self, agent_id: Optional[int] = None):
        super().__init__(
            agent_name="Küresel İstihbarat Ajanı",
            agent_id=agent_id if agent_id else 176
        )
        
        # Dosya yolları
        self.istihbarat_raporlari_dir = Path("data/kuresel_istihbarat_raporlari")
        self.istihbarat_raporlari_dir.mkdir(parents=True, exist_ok=True)
        self.rapor_dosyasi = self.istihbarat_raporlari_dir / "kuresel_istihbarat_raporlari.json"
        
        # Hukuki uyum ajanı entegrasyonu
        self.hukuki_ajan = HukukiUyumAjani(agent_id=174)
        
        # Küresel gümrük ve mevzuat veritabanı (tüm ülkeler için)
        self.kuresel_gumruk_mevzuat_db = self._kuresel_gumruk_mevzuat_veritabani_olustur()
        
        # Küresel pazar veritabanı
        self.kuresel_pazarlar = self._kuresel_pazar_veritabani_olustur()
        
        # Risk esikleri
        self.risk_esikleri = {
            "yasakli_urun": 100,  # Yasaklı ürün
            "izne_tabi": 80,  # İzne tabi ürün
            "limit_ustu": 70,  # Limit üstü
            "vergi_yuksek": 50,  # Yüksek vergi
            "sertifika_eksik": 60  # Sertifika eksik
        }
        
        self.log(f"🌍 Küresel İstihbarat Ajanı (Ajan 176) devrede. Sayın {CEO_TITLE}", "INFO")
    
    def _kuresel_gumruk_mevzuat_veritabani_olustur(self) -> Dict[str, Any]:
        """Küresel gümrük ve mevzuat veritabanı (tüm ülkeler için)"""
        return {
            "turkiye": {
                "ulke_adi": "Türkiye",
                "bireysel_ithalat_limitleri": {
                    "de_minimis_limit_eu": 150,  # Euro (AB'den)
                    "de_minimis_limit_abd": 100,  # USD (ABD'den)
                    "de_minimis_limit_diger": 75,  # USD (diğer ülkelerden)
                    "yillik_limit": 5000  # USD (yıllık toplam)
                },
                "yasakli_urunler": ["alkol", "tütün", "silah", "ilaç", "narkotik", "patlayıcı", "radyoaktif"],
                "izne_tabi_urunler": {
                    "kozmetik": ["GMP sertifikası", "Kozmetik Uygunluk Belgesi"],
                    "takviye_gida": ["GMP sertifikası", "Gıda İzin Belgesi"],
                    "elektronik": ["CE sertifikası", "TSE onayı"],
                    "medikal": ["CE sertifikası", "TİB onayı"],
                    "oyuncak": ["CE sertifikası", "EN71 test raporu"]
                },
                "vergi_oranlari": {
                    "elektronik": {"gumruk_vergisi": 20, "kdv": 20},
                    "giyim": {"gumruk_vergisi": 12, "kdv": 20},
                    "kozmetik": {"gumruk_vergisi": 18, "kdv": 20},
                    "takviye_gida": {"gumruk_vergisi": 15, "kdv": 10},
                    "ev_esyalari": {"gumruk_vergisi": 10, "kdv": 18}
                },
                "ticaret_mevzuati": {
                    "ticari_reklam": True,
                    "haksiz_ticari_uygulamalar": True,
                    "tuketicinin_korunmasi": True,
                    "fiyat_etiketleme": True
                }
            },
            "abd": {
                "ulke_adi": "Amerika Birleşik Devletleri",
                "bireysel_ithalat_limitleri": {
                    "de_minimis_limit": 800,  # USD
                    "yillik_limit": 2500  # USD
                },
                "yasakli_urunler": ["alkol", "tütün", "silah", "ilaç", "narkotik", "patlayıcı"],
                "izne_tabi_urunler": {
                    "kozmetik": ["FDA onayı"],
                    "takviye_gida": ["FDA onayı"],
                    "elektronik": ["FCC sertifikası"],
                    "medikal": ["FDA onayı"],
                    "oyuncak": ["CPSC onayı"]
                },
                "vergi_oranlari": {
                    "elektronik": {"gumruk_vergisi": 0, "kdv": 0},
                    "giyim": {"gumruk_vergisi": 0, "kdv": 0},
                    "kozmetik": {"gumruk_vergisi": 0, "kdv": 0},
                    "takviye_gida": {"gumruk_vergisi": 0, "kdv": 0},
                    "ev_esyalari": {"gumruk_vergisi": 0, "kdv": 0}
                },
                "ticaret_mevzuati": {
                    "federal_trade_commission": True,
                    "consumer_protection": True,
                    "truth_in_advertising": True
                }
            },
            "almanya": {
                "ulke_adi": "Almanya",
                "bireysel_ithalat_limitleri": {
                    "de_minimis_limit_eu": 150,  # Euro (AB içi)
                    "de_minimis_limit_diger": 22,  # Euro (AB dışı)
                    "yillik_limit": 1000  # Euro
                },
                "yasakli_urunler": ["alkol", "tütün", "silah", "ilaç", "narkotik", "patlayıcı"],
                "izne_tabi_urunler": {
                    "kozmetik": ["CE sertifikası", "GMP"],
                    "takviye_gida": ["CE sertifikası", "Gıda İzin"],
                    "elektronik": ["CE sertifikası"],
                    "medikal": ["CE sertifikası"],
                    "oyuncak": ["CE sertifikası", "EN71"]
                },
                "vergi_oranlari": {
                    "elektronik": {"gumruk_vergisi": 0, "kdv": 19},
                    "giyim": {"gumruk_vergisi": 12, "kdv": 19},
                    "kozmetik": {"gumruk_vergisi": 0, "kdv": 19},
                    "takviye_gida": {"gumruk_vergisi": 0, "kdv": 7},
                    "ev_esyalari": {"gumruk_vergisi": 0, "kdv": 19}
                },
                "ticaret_mevzuati": {
                    "bnetza": True,
                    "consumer_protection": True,
                    "price_indication": True
                }
            },
            "cin": {
                "ulke_adi": "Çin",
                "bireysel_ithalat_limitleri": {
                    "de_minimis_limit": 50,  # USD
                    "yillik_limit": 2000  # USD
                },
                "yasakli_urunler": ["alkol", "tütün", "silah", "ilaç", "narkotik", "patlayıcı"],
                "izne_tabi_urunler": {
                    "kozmetik": ["NMPA onayı"],
                    "takviye_gida": ["NMPA onayı"],
                    "elektronik": ["CCC sertifikası"],
                    "medikal": ["NMPA onayı"],
                    "oyuncak": ["CCC sertifikası"]
                },
                "vergi_oranlari": {
                    "elektronik": {"gumruk_vergisi": 13, "kdv": 13},
                    "giyim": {"gumruk_vergisi": 10, "kdv": 13},
                    "kozmetik": {"gumruk_vergisi": 5, "kdv": 13},
                    "takviye_gida": {"gumruk_vergisi": 10, "kdv": 13},
                    "ev_esyalari": {"gumruk_vergisi": 10, "kdv": 13}
                },
                "ticaret_mevzuati": {
                    "samr": True,
                    "consumer_protection": True,
                    "advertising_law": True
                }
            },
            "guney_kore": {
                "ulke_adi": "Güney Kore",
                "bireysel_ithalat_limitleri": {
                    "de_minimis_limit": 150,  # USD
                    "yillik_limit": 2000  # USD
                },
                "yasakli_urunler": ["alkol", "tütün", "silah", "ilaç", "narkotik", "patlayıcı"],
                "izne_tabi_urunler": {
                    "kozmetik": ["MFDS onayı"],
                    "takviye_gida": ["MFDS onayı"],
                    "elektronik": ["KC sertifikası"],
                    "medikal": ["MFDS onayı"],
                    "oyuncak": ["KC sertifikası"]
                },
                "vergi_oranlari": {
                    "elektronik": {"gumruk_vergisi": 8, "kdv": 10},
                    "giyim": {"gumruk_vergisi": 13, "kdv": 10},
                    "kozmetik": {"gumruk_vergisi": 8, "kdv": 10},
                    "takviye_gida": {"gumruk_vergisi": 8, "kdv": 10},
                    "ev_esyalari": {"gumruk_vergisi": 8, "kdv": 10}
                },
                "ticaret_mevzuati": {
                    "kftc": True,
                    "consumer_protection": True,
                    "advertising_law": True
                }
            },
            "hollanda": {
                "ulke_adi": "Hollanda",
                "bireysel_ithalat_limitleri": {
                    "de_minimis_limit_eu": 150,  # Euro (AB içi)
                    "de_minimis_limit_diger": 22,  # Euro (AB dışı)
                    "yillik_limit": 1000  # Euro
                },
                "yasakli_urunler": ["alkol", "tütün", "silah", "ilaç", "narkotik", "patlayıcı"],
                "izne_tabi_urunler": {
                    "kozmetik": ["CE sertifikası", "GMP"],
                    "takviye_gida": ["CE sertifikası", "Gıda İzin"],
                    "elektronik": ["CE sertifikası"],
                    "medikal": ["CE sertifikası"],
                    "oyuncak": ["CE sertifikası", "EN71"]
                },
                "vergi_oranlari": {
                    "elektronik": {"gumruk_vergisi": 0, "kdv": 21},
                    "giyim": {"gumruk_vergisi": 12, "kdv": 21},
                    "kozmetik": {"gumruk_vergisi": 0, "kdv": 21},
                    "takviye_gida": {"gumruk_vergisi": 0, "kdv": 9},
                    "ev_esyalari": {"gumruk_vergisi": 0, "kdv": 21}
                },
                "ticaret_mevzuati": {
                    "acm": True,
                    "consumer_protection": True,
                    "price_indication": True
                }
           }
        }
    
    def _kuresel_pazar_veritabani_olustur(self) -> Dict[str, Any]:
        """Küresel pazar veritabanı"""
        return {
            "abd": {
                "ulke": "Amerika Birleşik Devletleri",
                "afiliye_aglari": ["Amazon Associates", "eBay Partner Network", "ShareASale", "CJ Affiliate"],
                "populer_kategoriler": ["elektronik", "giyim", "ev_esyalari", "kozmetik"],
                "odeme_yontemleri": ["PayPal", "Kredi Kartı", "Banka Havalesi"]
            },
            "cin": {
                "ulke": "Çin",
                "afiliye_aglari": ["AliExpress Affiliate", "DHgate", "Banggood Affiliate"],
                "populer_kategoriler": ["elektronik", "ev_esyalari", "giyim", "takviye_gida"],
                "odeme_yontemleri": ["Alipay", "WeChat Pay", "Banka Havalesi"]
            },
            "avrupa": {
                "ulke": "Avrupa Birliği",
                "afiliye_aglari": ["Amazon EU", "eBay EU", "Zalando Partner", "Awin"],
                "populer_kategoriler": ["giyim", "kozmetik", "elektronik", "takviye_gida"],
                "odeme_yontemleri": ["PayPal", "SEPA", "Kredi Kartı"]
            }
        }
    
    def _urun_kategori_tespit(self, urun_adi: str) -> str:
        """Ürün kategorisini tespit et"""
        urun_adi_lower = urun_adi.lower()
        
        kategori_keywords = {
            "elektronik": ["telefon", "laptop", "tablet", "kulaklık", "şarj", "kablo", "hoparlör", "kamera"],
            "giyim": ["tişört", "pantolon", "ayakkabı", "elbise", "ceket", "mont", "çorap", "şapka"],
            "kozmetik": ["makyaj", "krem", "parfüm", "ruj", "far", "losyon", "sabun", "şampuan"],
            "takviye_gida": ["vitamin", "protein", "takviye", "gıda", "supplement", "kapsül"],
            "ev_esyalari": ["mobilya", "dekorasyon", "mutfak", "banyo", "halı", "perde", "lamba"]
        }
        
        for kategori, keywords in kategori_keywords.items():
            if any(keyword in urun_adi_lower for keyword in keywords):
                return kategori
        
        return "diger"
    
    def _gumruk_risk_analizi(self, urun: Dict[str, Any], hedef_ulke: str = "turkiye") -> Dict[str, Any]:
        """Hedef ülke bazlı gümrük risk analizi"""
        urun_adi = urun.get("urun_adi", "")
        kategori = urun.get("kategori", self._urun_kategori_tespit(urun_adi))
        fiyat = urun.get("fiyat", 0)
        menşe = urun.get("mense", "bilinmiyor")
        
        # Hedef ülke veritabanını al
        ulke_verisi = self.kuresel_gumruk_mevzuat_db.get(hedef_ulke)
        if not ulke_verisi:
            return {
                "urun_adi": urun_adi,
                "kategori": kategori,
                "fiyat": fiyat,
                "mense": menşe,
                "hedef_ulke": hedef_ulke,
                "risk_skoru": 100,
                "riskler": [f"BİLİNMEYEN HEDEF ÜLKE: {hedef_ulke}"],
                "gumruk_bilgileri": {}
            }
        
        risk_analizi = {
            "urun_adi": urun_adi,
            "kategori": kategori,
            "fiyat": fiyat,
            "mense": menşe,
            "hedef_ulke": hedef_ulke,
            "ulke_adi": ulke_verisi["ulke_adi"],
            "risk_skoru": 0,
            "riskler": [],
            "gumruk_bilgileri": {}
        }
        
        # 1. Yasaklı ürün kontrolü
        urun_adi_lower = urun_adi.lower()
        for yasakli in ulke_verisi["yasakli_urunler"]:
            if yasakli in urun_adi_lower:
                risk_analizi["risk_skoru"] = self.risk_esikleri["yasakli_urun"]
                risk_analizi["riskler"].append(f"YASAKLI ÜRÜN: {yasakli}")
                return risk_analizi  # Yasaklı ürün için direkt return
        
        # 2. İzne tabi ürün kontrolü
        if kategori in ulke_verisi["izne_tabi_urunler"]:
            gerekli_sertifikalar = ulke_verisi["izne_tabi_urunler"][kategori]
            mevcut_sertifikalar = urun.get("sertifikalar", [])
            
            eksik_sertifikalar = [s for s in gerekli_sertifikalar if s not in mevcut_sertifikalar]
            if eksik_sertifikalar:
                risk_analizi["risk_skoru"] = max(risk_analizi["risk_skoru"], self.risk_esikleri["izne_tabi"])
                risk_analizi["riskler"].append(f"İZNE TABİ: Eksik sertifikalar - {', '.join(eksik_sertifikalar)}")
        
        # 3. De Minimis limit kontrolü
        limitler = ulke_verisi["bireysel_ithalat_limitleri"]
        
        if hedef_ulke == "turkiye":
            if menşe.lower() == "abd":
                limit = limitler["de_minimis_limit_abd"]
            elif menşe.lower() in ["avrupa", "ab", "almanya", "fransa", "italya", "hollanda"]:
                limit = limitler["de_minimis_limit_eu"]
            else:
                limit = limitler["de_minimis_limit_diger"]
        elif hedef_ulke in ["almanya", "hollanda"]:
            if menşe.lower() in ["avrupa", "ab", "almanya", "fransa", "italya", "hollanda"]:
                limit = limitler["de_minimis_limit_eu"]
            else:
                limit = limitler["de_minimis_limit_diger"]
        else:
            limit = limitler.get("de_minimis_limit", 100)
        
        if fiyat > limit:
            risk_analizi["risk_skoru"] = max(risk_analizi["risk_skoru"], self.risk_esikleri["limit_ustu"])
            risk_analizi["riskler"].append(f"LIMIT ÜSTÜ: {fiyat} USD > {limit} USD")
        
        # 4. Vergi analizi
        if kategori in ulke_verisi["vergi_oranlari"]:
            vergi_bilgileri = ulke_verisi["vergi_oranlari"][kategori]
            risk_analizi["gumruk_bilgileri"] = {
                "gumruk_vergisi": vergi_bilgileri["gumruk_vergisi"],
                "kdv": vergi_bilgileri["kdv"],
                "toplam_vergi": vergi_bilgileri["gumruk_vergisi"] + vergi_bilgileri["kdv"]
            }
            
            if vergi_bilgileri["gumruk_vergisi"] >= 20:
                risk_analizi["risk_skoru"] = max(risk_analizi["risk_skoru"], self.risk_esikleri["vergi_yuksek"])
                risk_analizi["riskler"].append(f"YÜKSEK VERGİ: %{vergi_bilgileri['gumruk_vergisi']}")
        
        # 5. Ticaret mevzuat uyumu
        mevzuat_uyumu = True
        for mevzuat, gerekli in ulke_verisi["ticaret_mevzuati"].items():
            if gerekli and not urun.get(mevzuat, False):
                mevzuat_uyumu = False
                risk_analizi["risk_skoru"] = max(risk_analizi["risk_skoru"], 30)
                risk_analizi["riskler"].append(f"MEVZUAT UYUMSUZLUĞU: {mevzuat}")
        
        return risk_analizi
    
    def _hukuki_risk_skoru_hesapla(self, urun: Dict[str, Any], gumruk_risk: Dict[str, Any], hedef_ulke: str = "turkiye") -> Dict[str, Any]:
        """Hukuki uyum ajanı ile çapraz bağlayarak yasal risk skoru üretir"""
        
        # Hukuki analiz yap (hedef ülke bazlı)
        faaliyet_tanimi = f"Küresel ürün ithalatı: {urun.get('urun_adi', '')} ({urun.get('mense', 'bilinmiyor')}) -> {hedef_ulke}"
        hukuki_analiz = self.hukuki_ajan.hukuki_analiz_yap(faaliyet_tanimi)
        
        # Gümrük ve hukuki riskleri birleştir
        gumruk_skor = gumruk_risk["risk_skoru"]
        hukuki_risk = 10 if hukuki_analiz["durum"] == "Başarılı" else 50
        
        # Ağırlıklı ortalama
        toplam_risk_skoru = (gumruk_skor * 0.7) + (hukuki_risk * 0.3)
        
        return {
            "gumruk_risk_skoru": gumruk_skor,
            "hukuki_risk_skoru": hukuki_risk,
            "toplam_risk_skoru": round(toplam_risk_skoru, 2),
            "hukuki_analiz": hukuki_analiz,
            "hedef_ulke": hedef_ulke,
            "onay_durumu": "ONAYLI" if toplam_risk_skoru < 50 else "RISKLI"
        }
    
    def kuresel_urun_tara(self, pazar: str = "abd", kategori: str = None) -> List[Dict[str, Any]]:
        """Küresel ürün taraması"""
        self.log(f"🌍 Küresel ürün taraması başlatılıyor: {pazar}", "INFO")
        
        # Simüle edilmiş ürün veritabanı (gerçek uygulamada API'den çekilecek)
        ornek_urunler = [
            {
                "urun_adi": "iPhone 15 Pro Max",
                "kategori": "elektronik",
                "fiyat": 1200,
                "mense": "abd",
                "sertifikalar": ["CE sertifikası"],
                "afiliye_ag": "Amazon Associates"
            },
            {
                "urun_adi": "Organik Vitamin C Takviyesi",
                "kategori": "takviye_gida",
                "fiyat": 45,
                "mense": "abd",
                "sertifikalar": [],
                "afiliye_ag": "ShareASale"
            },
            {
                "urun_adi": "Doğal Yüz Kremi",
                "kategori": "kozmetik",
                "fiyat": 35,
                "mense": "avrupa",
                "sertifikalar": ["GMP sertifikası"],
                "afiliye_ag": "Awin"
            },
            {
                "urun_adi": "Kablosuz Kulaklık",
                "kategori": "elektronik",
                "fiyat": 80,
                "mense": "cin",
                "sertifikalar": ["CE sertifikası"],
                "afiliye_ag": "AliExpress Affiliate"
            },
            {
                "urun_adi": "Pamuk Tişört",
                "kategori": "giyim",
                "fiyat": 25,
                "mense": "cin",
                "sertifikalar": [],
                "afiliye_ag": "AliExpress Affiliate"
            }
        ]
        
        # Kategori filtreleme
        if kategori:
            ornek_urunler = [u for u in ornek_urunler if u["kategori"] == kategori]
        
        # Menşe filtreleme
        if pazar:
            ornek_urunler = [u for u in ornek_urunler if u["mense"] == pazar]
        
        return ornek_urunler
    
    def istihbarat_raporu_olustur(self, pazar: str = "abd", kategori: str = None, hedef_ulkeler: List[str] = None) -> Dict[str, Any]:
        """İstihbarat raporu oluşturur (çoklu hedef ülke desteği)"""
        self.log(f"📊 Küresel istihbarat raporu oluşturuluyor: {pazar}", "INFO")
        
        # Hedef ülkeleri belirle
        if hedef_ulkeler is None:
            hedef_ulkeler = ["turkiye", "abd", "almanya", "cin", "guney_kore", "hollanda"]
        
        # Ürünleri tara
        urunler = self.kuresel_urun_tara(pazar, kategori)
        
        # Her ürün için her hedef ülke analizini yap
        analiz_sonuclari = []
        onayli_urunler = []
        riskli_urunler = []
        ulke_bazli_sonuclar = {}
        
        for hedef_ulke in hedef_ulkeler:
            ulke_analizleri = []
            ulke_onayli = []
            ulke_riskli = []
            
            for urun in urunler:
                # Gümrük risk analizi (hedef ülke bazlı)
                gumruk_risk = self._gumruk_risk_analizi(urun, hedef_ulke)
                
                # Hukuki risk skoru hesapla (hedef ülke bazlı)
                hukuki_risk = self._hukuki_risk_skoru_hesapla(urun, gumruk_risk, hedef_ulke)
                
                urun_analizi = {
                    "urun": urun,
                    "hedef_ulke": hedef_ulke,
                    "gumruk_risk_analizi": gumruk_risk,
                    "hukuki_risk_analizi": hukuki_risk
                }
                
                ulke_analizleri.append(urun_analizi)
                analiz_sonuclari.append(urun_analizi)
                
                if hukuki_risk["onay_durumu"] == "ONAYLI":
                    ulke_onayli.append(urun_analizi)
                    onayli_urunler.append(urun_analizi)
                else:
                    ulke_riskli.append(urun_analizi)
                    riskli_urunler.append(urun_analizi)
            
            ulke_bazli_sonuclar[hedef_ulke] = {
                "ulke_adi": self.kuresel_gumruk_mevzuat_db[hedef_ulke]["ulke_adi"],
                "toplam_urun": len(urunler),
                "onayli_urun_sayisi": len(ulke_onayli),
                "riskli_urun_sayisi": len(ulke_riskli),
                "onay_orani": round((len(ulke_onayli) / len(urunler)) * 100, 2) if urunler else 0,
                "analizleri": ulke_analizleri
            }
        
        # Rapor oluştur
        rapor = {
            "rapor_id": f"ISTIHBARAT_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "rapor_tarihi": datetime.now().isoformat(),
            "raporlayan": f"{self.agent_name} (ID: {self.agent_id})",
            "kaynak_pazar": pazar,
            "kategori": kategori,
            "hedef_ulkeler": hedef_ulkeler,
            "toplam_urun": len(urunler),
            "toplam_analiz": len(analiz_sonuclari),
            "onayli_urun_sayisi": len(onayli_urunler),
            "riskli_urun_sayisi": len(riskli_urunler),
            "ulke_bazli_sonuclar": ulke_bazli_sonuclar,
            "analiz_sonuclari": analiz_sonuclari,
            "onayli_urunler": onayli_urunler,
            "riskli_urunler": riskli_urunler
        }
        
        return rapor
    
    def rapor_kaydet(self, rapor: Dict[str, Any]) -> str:
        """Raporu dosyaya kaydeder"""
        try:
            # Mevcut raporları oku
            mevcut_raporlar = []
            if self.rapor_dosyasi.exists():
                with open(self.rapor_dosyasi, "r", encoding="utf-8") as f:
                    mevcut_raporlar = json.load(f)
            
            # Yeni raporu ekle
            mevcut_raporlar.append(rapor)
            
            # Kaydet
            with open(self.rapor_dosyasi, "w", encoding="utf-8") as f:
                json.dump(mevcut_raporlar, f, indent=4, ensure_ascii=False)
            
            self.log(f"📁 İstihbarat raporu kaydedildi: {self.rapor_dosyasi}", "INFO")
            return str(self.rapor_dosyasi)
            
        except Exception as e:
            self.log(f"❌ Rapor kayıt hatası: {e}", "ERROR")
            raise
    
    def stop(self) -> Dict[str, Any]:
        self.is_running = False
        self.status = "stopped"
        return {"status": "stopped", "agent_id": self.agent_id}
    
    def restart(self) -> Dict[str, Any]:
        self.status = "ready"
        self.is_running = True
        return {"status": "restarted", "agent_id": self.agent_id}
    
    def run(self, operation: str = "tara", **kwargs) -> Dict[str, Any]:
        if operation == "tara":
            pazar = kwargs.get("pazar", "abd")
            kategori = kwargs.get("kategori", None)
            hedef_ulkeler = kwargs.get("hedef_ulkeler", None)
            
            rapor = self.istihbarat_raporu_olustur(pazar, kategori, hedef_ulkeler)
            rapor_dosyasi = self.rapor_kaydet(rapor)
            
            return {
                "durum": "basarili",
                "rapor": rapor,
                "rapor_dosyasi": rapor_dosyasi
            }
        return {"hata": "Bilinmeyen işlem"}


if __name__ == "__main__":
    print("Kuresel Istihbarat Ajan Test Basliyor...")
    ajan = KureselIstihbaratAjani(agent_id=176)
    sonuc = ajan.run(operation="tara", pazar="abd", hedef_ulkeler=["turkiye", "abd", "almanya"])
    
    print(f"\nDurum: {sonuc['durum']}")
    print(f"Toplam Urun: {sonuc['rapor']['toplam_urun']}")
    print(f"Toplam Analiz: {sonuc['rapor']['toplam_analiz']}")
    print(f"Onayli Urun: {sonuc['rapor']['onayli_urun_sayisi']}")
    print(f"Riskli Urun: {sonuc['rapor']['riskli_urun_sayisi']}")
    print(f"Hedef Ulkeler: {sonuc['rapor']['hedef_ulkeler']}")
    
    for ulke, ulke_sonuc in sonuc['rapor']['ulke_bazli_sonuclar'].items():
        print(f"\n{ulke_sonuc['ulke_adi']}:")
        print(f"  - Onay Orani: %{ulke_sonuc['onay_orani']}")
        print(f"  - Onayli: {ulke_sonuc['onayli_urun_sayisi']}")
        print(f"  - Riskli: {ulke_sonuc['riskli_urun_sayisi']}")
    
    print(f"\nRapor Dosyasi: {sonuc['rapor_dosyasi']}")
