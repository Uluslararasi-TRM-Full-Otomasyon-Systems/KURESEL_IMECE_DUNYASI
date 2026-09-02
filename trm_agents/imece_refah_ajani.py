#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
İmece Refah Ajanı (Ajan 177) - Sosyal Refah ve Periyodik Gelir Denetim Modülü
Versiyon: 1.0.0

İl bazlı yoksulluk sınırı ve %20 İmece Refah Payı hesaplar, 40-50 yaş Anaç Asistan
periyodik denetim yapar, kademeli uyarı ve cezalandırma sistemi işletir.
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


class ImeceRefahAjani(BaseAgent):
    def __init__(self, agent_id: Optional[int] = None):
        super().__init__(
            agent_name="İmece Refah Ajanı",
            agent_id=agent_id if agent_id else 177
        )
        
        # Dosya yolları
        self.refah_odemeleri_dir = Path("data/imece_refah_odemeleri")
        self.refah_odemeleri_dir.mkdir(parents=True, exist_ok=True)
        self.odeme_dosyasi = self.refah_odemeleri_dir / "imece_refah_odemeleri.json"
        self.denetim_dosyasi = self.refah_odemeleri_dir / "periyodik_denetim_loglari.json"
        
        # İl bazlı yoksulluk sınırı veritabanı (2024 TÜİK verileri)
        self.il_yoksulluk_siniri = self._il_yoksulluk_veritabani_olustur()
        
        # Refah payı oranı
        self.refah_payi_orani = 0.20  # %20
        
        # Denetim periyodu (ay)
        self.denetim_periyodu = 3
        
        # Cezalandırma seviyeleri
        self.ceza_seviyeleri = {
            "ilk_ceza": 3,  # 3 ay
            "ikinci_ceza": 9,  # 9 ay
            "son_ceza": "sistemden_cikarilma"  # Sistemden çıkarılma
        }
        
        # Kullanıcı veritabanı
        self.kullanici_veritabani = self._kullanici_veritabani_yukle()
        
        self.log(f"🏛️ İmece Refah Ajanı (Ajan 177) devrede. Sayın {CEO_TITLE}", "INFO")
    
    def _il_yoksulluk_veritabani_olustur(self) -> Dict[str, int]:
        """İl bazlı yoksulluk sınırı veritabanı (aylık TL)"""
        return {
            "istanbul": 18000,
            "ankara": 16000,
            "izmir": 15500,
            "bursa": 14000,
            "antalya": 13500,
            "kocaeli": 14500,
            "adana": 13000,
            "mersin": 12500,
            "gaziantep": 12000,
            "konya": 11500,
            "diğer": 11000  # Varsayılan değer
        }
    
    def _kullanici_veritabani_yukle(self) -> Dict[str, Any]:
        """Kullanıcı veritabanını yükler"""
        if self.denetim_dosyasi.exists():
            with open(self.denetim_dosyasi, "r", encoding="utf-8") as f:
                return json.load(f)
        return {"kullanicilar": {}}
    
    def _kullanici_veritabani_kaydet(self):
        """Kullanıcı veritabanını kaydeder"""
        with open(self.denetim_dosyasi, "w", encoding="utf-8") as f:
            json.dump(self.kullanici_veritabani, f, indent=4, ensure_ascii=False)
    
    def _refah_tabani_hesapla(self, il: str) -> int:
        """İl bazlı refah tabanını hesapla (yoksulluk sınırı + %20 refah payı)"""
        yoksulluk_siniri = self.il_yoksulluk_siniri.get(il.lower(), self.il_yoksulluk_siniri["diğer"])
        refah_tabani = int(yoksulluk_siniri * (1 + self.refah_payi_orani))
        return refah_tabani
    
    def _net_destek_hesapla(self, refah_tabani: int, mevcut_gelir: int) -> int:
        """Net destek tutarını hesapla"""
        net_destek = max(0, refah_tabani - mevcut_gelir)
        return net_destek
    
    def kullanici_kaydet(self, kullanici_id: str, ad_soyad: str, il: str, 
                       yas: int, mevcut_gelir: int, gelir_beyan_tarihi: str) -> Dict[str, Any]:
        """Yeni kullanıcı kaydeder"""
        refah_tabani = self._refah_tabani_hesapla(il)
        net_destek = self._net_destek_hesapla(refah_tabani, mevcut_gelir)
        
        kullanici_bilgisi = {
            "kullanici_id": kullanici_id,
            "ad_soyad": ad_soyad,
            "il": il,
            "yas": yas,
            "mevcut_gelir": mevcut_gelir,
            "gelir_beyan_tarihi": gelir_beyan_tarihi,
            "refah_tabani": refah_tabani,
            "net_destek": net_destek,
            "son_denetim_tarihi": gelir_beyan_tarihi,
            "sonraki_denetim_tarihi": (datetime.strptime(gelir_beyan_tarihi, "%Y-%m-%d") + timedelta(days=self.denetim_periyodu*30)).strftime("%Y-%m-%d"),
            "ceza_durumu": "aktif",
            "ceza_sayisi": 0,
            "denetim_gecmisi": []
        }
        
        self.kullanici_veritabani["kullanicilar"][kullanici_id] = kullanici_bilgisi
        self._kullanici_veritabani_kaydet()
        
        self.log(f"👤 Kullanıcı kaydedildi: {ad_soyad} ({il}) - Net Destek: {net_destek} TL", "INFO")
        
        return kullanici_bilgisi
    
    def periyodik_denetim_yap(self, kullanici_id: str, yeni_gelir: int, 
                             belge_tarihi: str, belge_turu: str = "bordro") -> Dict[str, Any]:
        """Periyodik gelir denetimi yapar"""
        kullanici = self.kullanici_veritabani["kullanicilar"].get(kullanici_id)
        
        if not kullanici:
            return {"hata": "Kullanıcı bulunamadı"}
        
        # 40-50 yaş kontrolü (Anaç Asistan kategorisi)
        if 40 <= kullanici["yas"] <= 50:
            self.log(f"🔍 Anaç Asistan denetimi: {kullanici['ad_soyad']} ({kullanici['yas']} yaş)", "INFO")
        
        # Denetim tarihi kontrolü
        bugun = datetime.now()
        sonraki_denetim = datetime.strptime(kullanici["sonraki_denetim_tarihi"], "%Y-%m-%d")
        
        if bugun < sonraki_denetim:
            return {
                "durum": "erken_denetim",
                "mesaj": f"Denetim tarihi henüz gelmedi. Sonraki denetim: {kullanici['sonraki_denetim_tarihi']}"
            }
        
        # Gelir değişikliği kontrolü
        gelir_farki = yeni_gelir - kullanici["mevcut_gelir"]
        gelir_degisim_orani = abs(gelir_farki / kullanici["mevcut_gelir"]) if kullanici["mevcut_gelir"] > 0 else 0
        
        denetim_sonucu = {
            "kullanici_id": kullanici_id,
            "denetim_tarihi": bugun.strftime("%Y-%m-%d"),
            "eski_gelir": kullanici["mevcut_gelir"],
            "yeni_gelir": yeni_gelir,
            "gelir_farki": gelir_farki,
            "gelir_degisim_orani": round(gelir_degisim_orani * 100, 2),
            "belge_tarihi": belge_tarihi,
            "belge_turu": belge_turu,
            "denetim_sonucu": "basarili"
        }
        
        # Gelir değişikliği %10'dan fazlaysa uyarı
        if gelir_degisim_orani > 0.10:
            denetim_sonucu["denetim_sonucu"] = "uyari"
            denetim_sonucu["mesaj"] = f"Gelir değişikliği %{round(gelir_degisim_orani * 100, 2)} - Belge gerekiyor"
            self.log(f"⚠️ Gelir değişikliği uyarısı: {kullanici['ad_soyad']}", "WARNING")
        
        # Kullanıcı bilgilerini güncelle
        kullanici["mevcut_gelir"] = yeni_gelir
        kullanici["son_denetim_tarihi"] = bugun.strftime("%Y-%m-%d")
        kullanici["sonraki_denetim_tarihi"] = (bugun + timedelta(days=self.denetim_periyodu*30)).strftime("%Y-%m-%d")
        
        # Refah tabanını yeniden hesapla
        refah_tabani = self._refah_tabani_hesapla(kullanici["il"])
        net_destek = self._net_destek_hesapla(refah_tabani, yeni_gelir)
        kullanici["refah_tabani"] = refah_tabani
        kullanici["net_destek"] = net_destek
        
        # Denetim geçmişine ekle
        kullanici["denetim_gecmisi"].append(denetim_sonucu)
        
        self._kullanici_veritabani_kaydet()
        
        self.log(f"✅ Denetim tamamlandı: {kullanici['ad_soyad']} - Yeni Net Destek: {net_destek} TL", "INFO")
        
        return denetim_sonucu
    
    def cezalandirma_sistemi(self, kullanici_id: str, ihmal_turu: str) -> Dict[str, Any]:
        """Kademeli cezalandırma sistemi"""
        kullanici = self.kullanici_veritabani["kullanicilar"].get(kullanici_id)
        
        if not kullanici:
            return {"hata": "Kullanıcı bulunamadı"}
        
        kullanici["ceza_sayisi"] += 1
        ceza_sayisi = kullanici["ceza_sayisi"]
        
        ceza_karari = {
            "kullanici_id": kullanici_id,
            "ihmal_turu": ihmal_turu,
            "ceza_sayisi": ceza_sayisi,
            "ceza_tarihi": datetime.now().strftime("%Y-%m-%d")
        }
        
        if ceza_sayisi == 1:
            ceza_karari["ceza_turu"] = "ilk_ceza"
            ceza_karari["ceza_suresi"] = f"{self.ceza_seviyeleri['ilk_ceza']} ay"
            kullanici["ceza_durumu"] = "cezali"
            kullanici["ceza_bitis_tarihi"] = (datetime.now() + timedelta(days=self.ceza_seviyeleri['ilk_ceza']*30)).strftime("%Y-%m-%d")
            self.log(f"🚫 İlk ceza: {kullanici['ad_soyad']} - 3 ay ceza", "WARNING")
            
        elif ceza_sayisi == 2:
            ceza_karari["ceza_turu"] = "ikinci_ceza"
            ceza_karari["ceza_suresi"] = f"{self.ceza_seviyeleri['ikinci_ceza']} ay"
            kullanici["ceza_durumu"] = "agir_cezali"
            kullanici["ceza_bitis_tarihi"] = (datetime.now() + timedelta(days=self.ceza_seviyeleri['ikinci_ceza']*30)).strftime("%Y-%m-%d")
            self.log(f"🚫 İkinci ceza: {kullanici['ad_soyad']} - 9 ay ceza", "WARNING")
            
        else:
            ceza_karari["ceza_turu"] = "son_ceza"
            ceza_karari["ceza_suresi"] = "sistemden_cikarilma"
            kullanici["ceza_durumu"] = "sistemden_cikarildi"
            del self.kullanici_veritabani["kullanicilar"][kullanici_id]
            self._kullanici_veritabani_kaydet()
            self.log(f"❌ Sistemden çıkarıldı: {kullanici['ad_soyad']}", "ERROR")
            return ceza_karari
        
        self._kullanici_veritabani_kaydet()
        return ceza_karari
    
    def odeme_raporu_olustur(self, ay: int = None, yil: int = None) -> Dict[str, Any]:
        """Ödeme raporu oluşturur"""
        if ay is None:
            ay = datetime.now().month
        if yil is None:
            yil = datetime.now().year
        
        rapor = {
            "rapor_id": f"REFAH_{yil}_{ay}",
            "rapor_tarihi": datetime.now().isoformat(),
            "raporlayan": f"{self.agent_name} (ID: {self.agent_id})",
            "ay": ay,
            "yil": yil,
            "toplam_kullanici": len(self.kullanici_veritabani["kullanicilar"]),
            "toplam_odeme": 0,
            "il_bazli_odemeler": {},
            "aktif_kullanicilar": 0,
            "cezali_kullanicilar": 0,
            "odemeler": []
        }
        
        for kullanici_id, kullanici in self.kullanici_veritabani["kullanicilar"].items():
            if kullanici["ceza_durumu"] == "aktif":
                rapor["aktif_kullanicilar"] += 1
                rapor["toplam_odeme"] += kullanici["net_destek"]
                
                # İl bazlı ödemeler
                il = kullanici["il"]
                if il not in rapor["il_bazli_odemeler"]:
                    rapor["il_bazli_odemeler"][il] = 0
                rapor["il_bazli_odemeler"][il] += kullanici["net_destek"]
                
                rapor["odemeler"].append({
                    "kullanici_id": kullanici_id,
                    "ad_soyad": kullanici["ad_soyad"],
                    "il": il,
                    "net_destek": kullanici["net_destek"],
                    "refah_tabani": kullanici["refah_tabani"]
                })
            else:
                rapor["cezali_kullanicilar"] += 1
        
        # Raporu kaydet
        self._odeme_raporu_kaydet(rapor)
        
        return rapor
    
    def _odeme_raporu_kaydet(self, rapor: Dict[str, Any]):
        """Ödeme raporunu kaydeder"""
        mevcut_raporlar = []
        if self.odeme_dosyasi.exists():
            with open(self.odeme_dosyasi, "r", encoding="utf-8") as f:
                mevcut_raporlar = json.load(f)
        
        mevcut_raporlar.append(rapor)
        
        with open(self.odeme_dosyasi, "w", encoding="utf-8") as f:
            json.dump(mevcut_raporlar, f, indent=4, ensure_ascii=False)
        
        self.log(f"📁 Ödeme raporu kaydedildi: {self.odeme_dosyasi}", "INFO")
    
    def stop(self) -> Dict[str, Any]:
        self.is_running = False
        self.status = "stopped"
        return {"status": "stopped", "agent_id": self.agent_id}
    
    def restart(self) -> Dict[str, Any]:
        self.status = "ready"
        self.is_running = True
        return {"status": "restarted", "agent_id": self.agent_id}
    
    def run(self, operation: str = "rapor", **kwargs) -> Dict[str, Any]:
        if operation == "kullanici_ekle":
            return self.kullanici_kaydet(
                kwargs.get("kullanici_id"),
                kwargs.get("ad_soyad"),
                kwargs.get("il"),
                kwargs.get("yas"),
                kwargs.get("mevcut_gelir"),
                kwargs.get("gelir_beyan_tarihi")
            )
        elif operation == "denetim":
            return self.periyodik_denetim_yap(
                kwargs.get("kullanici_id"),
                kwargs.get("yeni_gelir"),
                kwargs.get("belge_tarihi"),
                kwargs.get("belge_turu", "bordro")
            )
        elif operation == "ceza":
            return self.cezalandirma_sistemi(
                kwargs.get("kullanici_id"),
                kwargs.get("ihmal_turu")
            )
        elif operation == "rapor":
            return self.odeme_raporu_olustur(
                kwargs.get("ay"),
                kwargs.get("yil")
            )
        return {"hata": "Bilinmeyen işlem"}


if __name__ == "__main__":
    print("Imece Refah Ajan Test Basliyor...")
    ajan = ImeceRefahAjani(agent_id=177)
    
    # Test kullanıcısı ekle
    sonuc = ajan.run(
        operation="kullanici_ekle",
        kullanici_id="K001",
        ad_soyad="Ayşe Yılmaz",
        il="istanbul",
        yas=45,
        mevcut_gelir=15000,
        gelir_beyan_tarihi="2024-01-15"
    )
    
    print(f"\nKullanıcı Kayıt Sonucu:")
    print(f"Ad Soyad: {sonuc['ad_soyad']}")
    print(f"Refah Tabanı: {sonuc['refah_tabani']} TL")
    print(f"Net Destek: {sonuc['net_destek']} TL")
    
    # Periyodik denetim test
    denetim = ajan.run(
        operation="denetim",
        kullanici_id="K001",
        yeni_gelir=15500,
        belge_tarihi="2024-04-15"
    )
    
    print(f"\nDenetim Sonucu:")
    print(f"Durum: {denetim['denetim_sonucu']}")
    print(f"Gelir Farkı: {denetim['gelir_farki']} TL")
    
    # Ödeme raporu
    rapor = ajan.run(operation="rapor")
    print(f"\nÖdeme Raporu:")
    print(f"Toplam Kullanıcı: {rapor['toplam_kullanici']}")
    print(f"Aktif Kullanıcı: {rapor['aktif_kullanicilar']}")
    print(f"Toplam Ödeme: {rapor['toplam_odeme']} TL")
