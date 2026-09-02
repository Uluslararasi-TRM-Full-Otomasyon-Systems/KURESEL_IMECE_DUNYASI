#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
İç Denetim Ajanı (Ajan 175)
Versiyon: 1.0.0

Her ayın 1'inde otomatik tetiklenen, hukuki riskler ve sözleşme onayları 
arasında tutarlılık kontrolü yapan ve raporlayan otonom denetim ajanı.
"""

import os
import json
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
from pathlib import Path
import sys

# Path handling for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from trm_agents.base_agent_template import BaseAgent
from trm_agents.system_protocols import CEO_TITLE


class IcDenetimAjani(BaseAgent):
    def __init__(self, agent_id: Optional[int] = None):
        super().__init__(
            agent_name="İç Denetim Ajanı",
            agent_id=agent_id if agent_id else 175
        )
        
        # Dosya yolları
        self.hukuki_riskler_dosyasi = "hukuki_riskler.json"
        self.sozlesme_onaylari_dosyasi = "sozlesme_onaylari.json"
        self.denetim_raporlari_dir = Path("data/ic_denetim_raporlari")
        self.denetim_raporlari_dir.mkdir(parents=True, exist_ok=True)
        
        # Denetim parametreleri
        self.uyumsuzluk_esikleri = {
            "onay_eksik": 0,  # Hukuki analiz var ama onay yok
            "risk_yuksek": 0.8,  # %80 üzeri risk skoru
            "zaman_farki": 30  # 30 gün üzeri zaman farkı
        }
        
        self.log(f"🔍 İç Denetim Ajanı (Ajan 175) devrede. Sayın {CEO_TITLE}", "INFO")
    
    def _dosya_oku(self, dosya_yolu: str) -> List[Dict]:
        """JSON dosyasını okur"""
        try:
            if os.path.exists(dosya_yolu):
                with open(dosya_yolu, "r", encoding="utf-8") as f:
                    veri = json.load(f)
                return veri if isinstance(veri, list) else []
            return []
        except Exception as e:
            self.log(f"❌ Dosya okuma hatası ({dosya_yolu}): {e}", "ERROR")
            return []
    
    def _hukuki_riskleri_analiz_et(self, hukuki_riskler: List[Dict]) -> Dict[str, Any]:
        """Hukuki riskleri analiz eder"""
        analiz = {
            "toplam_kayit": len(hukuki_riskler),
            "riskli_kayitlar": 0,
            "faaliyet_turleri": {},
            "tarih_araligi": {"ilk": None, "son": None}
        }
        
        for kayit in hukuki_riskler:
            # Faaliyet türü analizi
            faaliyet = kayit.get("faaliyet", "bilinmiyor")
            analiz["faaliyet_turleri"][faaliyet] = analiz["faaliyet_turleri"].get(faaliyet, 0) + 1
            
            # Tarih aralığı
            tarih = kayit.get("tarih")
            if tarih:
                if analiz["tarih_araligi"]["ilk"] is None or tarih < analiz["tarih_araligi"]["ilk"]:
                    analiz["tarih_araligi"]["ilk"] = tarih
                if analiz["tarih_araligi"]["son"] is None or tarih > analiz["tarih_araligi"]["son"]:
                    analiz["tarih_araligi"]["son"] = tarih
        
        return analiz
    
    def _sozlesme_onaylarini_analiz_et(self, onaylar: List[Dict]) -> Dict[str, Any]:
        """Sözleşme onaylarını analiz eder"""
        analiz = {
            "toplam_onay": len(onaylar),
            "onayli_kullanicilar": set(),
            "sozlesme_versiyonlari": {},
            "tarih_araligi": {"ilk": None, "son": None},
            "ip_adresleri": set()
        }
        
        for onay in onaylar:
            # Kullanıcı analizi
            kullanici_id = onay.get("kullanici_id")
            if kullanici_id:
                analiz["onayli_kullanicilar"].add(kullanici_id)
            
            # Sözleşme versiyonu analizi
            versiyon = onay.get("sozlesme_versiyonu")
            if versiyon:
                analiz["sozlesme_versiyonlari"][versiyon] = analiz["sozlesme_versiyonlari"].get(versiyon, 0) + 1
            
            # Tarih aralığı
            timestamp = onay.get("timestamp")
            if timestamp:
                if analiz["tarih_araligi"]["ilk"] is None or timestamp < analiz["tarih_araligi"]["ilk"]:
                    analiz["tarih_araligi"]["ilk"] = timestamp
                if analiz["tarih_araligi"]["son"] is None or timestamp > analiz["tarih_araligi"]["son"]:
                    analiz["tarih_araligi"]["son"] = timestamp
            
            # IP adresi analizi
            ip_adresi = onay.get("ip_adresi")
            if ip_adresi:
                analiz["ip_adresleri"].add(ip_adresi)
        
        # Set'i listeye çevir
        analiz["onayli_kullanicilar"] = list(analiz["onayli_kullanicilar"])
        analiz["ip_adresleri"] = list(analiz["ip_adresleri"])
        
        return analiz
    
    def _tutarlilik_kontrolu(self, hukuki_riskler: List[Dict], onaylar: List[Dict]) -> Dict[str, Any]:
        """Hukuki riskler ve sözleşme onayları arası tutarlılık kontrolü"""
        tutarlilik = {
            "uyumsuzluklar": [],
            "eksik_onaylar": [],
            "riskli_durumlar": [],
            "genel_skor": 100  # Başlangıçta tam puan
        }
        
        # Hukuki riskleri ve onayları eşleştirme
        hukuki_kullanici_ids = set()
        for risk in hukuki_riskler:
            faaliyet = risk.get("faaliyet", "")
            # Kullanıcı ID'sini faaliyet metninden çıkarmaya çalış
            if "kullanici_" in faaliyet.lower():
                # Basit eşleştirme - geliştirilebilir
                parts = faaliyet.split()
                for part in parts:
                    if part.startswith("kullanici_"):
                        hukuki_kullanici_ids.add(part)
        
        onayli_kullanici_ids = set()
        for onay in onaylar:
            kullanici_id = onay.get("kullanici_id")
            if kullanici_id:
                onayli_kullanici_ids.add(kullanici_id)
        
        # Eksik onay kontrolü
        eksik_onaylar = hukuki_kullanici_ids - onayli_kullanici_ids
        if eksik_onaylar:
            tutarlilik["eksik_onaylar"] = list(eksik_onaylar)
            tutarlilik["uyumsuzluklar"].append({
                "tip": "eksik_onay",
                "aciklama": f"{len(eksik_onaylar)} kullanıcının onayı eksik",
                "kullanicilar": list(eksik_onaylar)
            })
            tutarlilik["genel_skor"] -= len(eksik_onaylar) * 10
        
        # Zaman tutarlılığı kontrolü
        if hukuki_riskler and onaylar:
            hukuki_son = hukuki_riskler[-1].get("tarih")
            onay_son = onaylar[-1].get("timestamp")
            
            if hukuki_son and onay_son:
                try:
                    hukuki_tarih = datetime.fromisoformat(hukuki_son)
                    onay_tarih = datetime.fromisoformat(onay_son)
                    fark = abs((hukuki_tarih - onay_tarih).days)
                    
                    if fark > self.uyumsuzluk_esikleri["zaman_farki"]:
                        tutarlilik["uyumsuzluklar"].append({
                            "tip": "zaman_farki",
                            "aciklama": f"Hukuki analiz ve onay arasında {fark} gun fark var",
                            "fark_gun": fark
                        })
                        tutarlilik["genel_skor"] -= 20
                except:
                    pass
        
        # Skoru 0-100 arasına sınırla
        tutarlilik["genel_skor"] = max(0, min(100, tutarlilik["genel_skor"]))
        
        return tutarlilik
    
    def denetim_yap(self) -> Dict[str, Any]:
        """
        Ana denetim metodu
        Her ayın 1'inde otomatik tetiklenir
        """
        self.log("🔍 Aylık iç denetim başlatılıyor...", "INFO")
        
        denetim_baslangic = datetime.now()
        rapor = {
            "denetim_id": f"DENETIM_{denetim_baslangic.strftime('%Y%m%d_%H%M%S')}",
            "denetim_tarihi": denetim_baslangic.isoformat(),
            "denetim_yapan": f"{self.agent_name} (ID: {self.agent_id})",
            "durum": "devam_ediyor",
            "sonuclar": {}
        }
        
        try:
            # 1. Hukuki riskleri oku ve analiz et
            self.log("📋 Hukuki riskler analiz ediliyor...", "INFO")
            hukuki_riskler = self._dosya_oku(self.hukuki_riskler_dosyasi)
            rapor["sonuclar"]["hukuki_riskler_analizi"] = self._hukuki_riskleri_analiz_et(hukuki_riskler)
            
            # 2. Sözleşme onaylarını oku ve analiz et
            self.log("✍️ Sözleşme onayları analiz ediliyor...", "INFO")
            onaylar = self._dosya_oku(self.sozlesme_onaylari_dosyasi)
            rapor["sonuclar"]["sozlesme_onaylari_analizi"] = self._sozlesme_onaylarini_analiz_et(onaylar)
            
            # 3. Tutarlılık kontrolü
            self.log("🔗 Tutarlılık kontrolü yapılıyor...", "INFO")
            rapor["sonuclar"]["tutarlilik_kontrolu"] = self._tutarlilik_kontrolu(hukuki_riskler, onaylar)
            
            # 4. Genel değerlendirme
            genel_skor = rapor["sonuclar"]["tutarlilik_kontrolu"]["genel_skor"]
            uyumsuzluk_sayisi = len(rapor["sonuclar"]["tutarlilik_kontrolu"]["uyumsuzluklar"])
            
            if genel_skor >= 80 and uyumsuzluk_sayisi == 0:
                rapor["genel_degerlendirme"] = "TAM UYUMLU"
                rapor["durum"] = "basarili"
                self.log("✅ Denetim tamamlandı: Tam uyumlu", "INFO")
            elif genel_skor >= 60:
                rapor["genel_degerlendirme"] = "KABUL EDİLEBİLİR"
                rapor["durum"] = "kabul_edilebilir"
                self.log(f"⚠️ Denetim tamamlandı: Kabul edilebilir (Skor: {genel_skor})", "WARNING")
            else:
                rapor["genel_degerlendirme"] = "KRİTİK UYUMSUZLUK"
                rapor["durum"] = "kritik"
                self.log(f"❌ Denetim tamamlandı: Kritik uyumsuzluk (Skor: {genel_skor})", "ERROR")
                
                # CEO'ya kritik uyarı gönder
                self._ceo_kritik_uyari(rapor)
            
            # 5. Raporu kaydet
            rapor_dosyasi = self.denetim_raporlari_dir / f"denetim_raporu_{denetim_baslangic.strftime('%Y%m')}.json"
            with open(rapor_dosyasi, "w", encoding="utf-8") as f:
                json.dump(rapor, f, indent=4, ensure_ascii=False)
            
            rapor["rapor_dosyasi"] = str(rapor_dosyasi)
            self.log(f"📊 Denetim raporu kaydedildi: {rapor_dosyasi}", "INFO")
            
        except Exception as e:
            rapor["durum"] = "hata"
            rapor["hata"] = str(e)
            self.log(f"❌ Denetim hatası: {e}", "ERROR")
        
        rapor["denetim_bitis"] = datetime.now().isoformat()
        
        return rapor
    
    def _ceo_kritik_uyari(self, rapor: Dict[str, Any]):
        """CEO'ya kritik uyarı gönder"""
        uyari_mesaji = f"""
        🔴 KRİTİK İÇ DENETİM UYARISI 🔴
        
        Sayın {CEO_TITLE},
        
        İç Denetim Ajanı (Ajan 175) tarafından yapılan aylık denetimde kritik uyumsuzluklar tespit edildi.
        
        Denetim ID: {rapor['denetim_id']}
        Denetim Tarihi: {rapor['denetim_tarihi']}
        Genel Değerlendirme: {rapor['genel_degerlendirme']}
        
        Tespit Edilen Uyumsuzluklar:
        """
        
        for uyumsuzluk in rapor["sonuclar"]["tutarlilik_kontrolu"]["uyumsuzluklar"]:
            uyari_mesaji += f"\n- {uyumsuzluk['tip']}: {uyumsuzluk['aciklama']}"
        
        uyari_mesaji += f"\n\nRapor Dosyası: {rapor.get('rapor_dosyasi', 'Bilinmiyor')}"
        uyari_mesaji += "\n\nLütfen acil inceleme yapınız."
        
        # Log olarak kaydet
        self.log(uyari_mesaji, "ERROR")
        
        # Sistem nöbetçisi üzerinden de logla
        try:
            from trm_agents.sistem_nobetcisi import SistemNobetcisiAjani
            nobetci = SistemNobetcisiAjani(agent_id=175)
            nobetci.log(uyari_mesaji, "ERROR")
        except Exception as e:
            self.log(f"⚠️ Sistem nöbetçisi uyarısı gönderilemedi: {e}", "WARNING")
    
    def stop(self) -> Dict[str, Any]:
        self.is_running = False
        self.status = "stopped"
        return {"status": "stopped", "agent_id": self.agent_id}
    
    def restart(self) -> Dict[str, Any]:
        self.status = "ready"
        self.is_running = True
        return {"status": "restarted", "agent_id": self.agent_id}
    
    def run(self, operation: str = "denetim", **kwargs) -> Dict[str, Any]:
        if operation == "denetim":
            return self.denetim_yap()
        return {"hata": "Bilinmeyen işlem"}


if __name__ == "__main__":
    import sys
    import os
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    
    print("Ic Denetim Ajan Test Basliyor...")
    ajan = IcDenetimAjani(agent_id=175)
    sonuc = ajan.denetim_yap()
    print(f"\nDenetim Sonucu: {sonuc['genel_degerlendirme']}")
    print(f"Durum: {sonuc['durum']}")
    print(f"Rapor Dosyasi: {sonuc.get('rapor_dosyasi', 'Olusturulmadi')}")
