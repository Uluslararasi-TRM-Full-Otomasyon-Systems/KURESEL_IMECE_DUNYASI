#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
İmece Denetim Ajanı
Versiyon: 2.1.0 (Google GenAI Güncel Paket ve Abstract Metot Uyumlu)
"""

import json
import os
import logging
from typing import Dict, Optional, Any
from datetime import datetime

# Yeni nesil Google GenAI SDK entegrasyonu
try:
    from google import genai
    GENAI_AVAILABLE = True
except ImportError:
    GENAI_AVAILABLE = False
    logging.warning("⚠️ Yeni google.genai kütüphanesi bulunamadı.")

from trm_agents.base_agent_template import BaseAgent
from trm_agents.system_protocols import CEO_TITLE


class ImeceDenetimAjani(BaseAgent):
    def __init__(self, agent_id: Optional[int] = None, veri_dosyasi: str = "harcama_kayitlari.json"):
        super().__init__(
            agent_name="İmece Denetim Ajanı",
            agent_id=agent_id if agent_id else 173
        )
        
        self.veri_dosyasi = veri_dosyasi
        self.denetim_orani = 0.80  # Aylık hak edişin %80'i kuralı
        self.dosya_kontrol()
        
        # Gemini API İstemcisi
        self.client = None
        self.gemini_vision_available = False
        
        self._load_gemini_config()
        self.log(f"🔍 İmece Denetim Ajanı başlatıldı. Sayın {CEO_TITLE}", "INFO")
    
    def _load_gemini_config(self):
        """global_config.json içindeki api_keys altından Gemini anahtarını güvenle yükler"""
        try:
            config = self.config
            api_keys_dict = config.get("api_keys", {})
            self.gemini_api_key = api_keys_dict.get("gemini_api_key") or config.get("gemini_api_key") or os.getenv("GEMINI_API_KEY")
            
            if self.gemini_api_key and GENAI_AVAILABLE:
                self.client = genai.Client(api_key=self.gemini_api_key)
                self.gemini_vision_available = True
                self.log("✅ Google GenAI Client başarıyla yapılandırıldı", "INFO")
            else:
                self.log("⚠️ Gemini API anahtarı global_config.json içinde bulunamadı veya kütüphane eksik", "WARNING")
                
        except Exception as e:
            self.log(f"❌ Gemini API yapılandırma hatası: {e}", "ERROR")
    
    def dosya_kontrol(self):
        if not os.path.exists(self.veri_dosyasi):
            with open(self.veri_dosyasi, "w", encoding="utf-8") as f:
                json.dump([], f, ensure_ascii=False, indent=4)
    
    def harcama_degerlendir(self, uye_adi: str, aylik_hak_edis: float, harcama_tutari: float, belge_tipi: str = "Fiş/Fatura") -> Dict[str, Any]:
        limit = aylik_hak_edis * self.denetim_orani
        durum = "Reddedildi"
        mesaj = ""

        if harcama_tutari >= limit:
            durum = "Onaylandı"
            mesaj = f"✅ Tebrikler {uye_adi}, harcamanız imece kriterlerine uygundur (Limit: {limit} TL)."
            self.log(f"✅ {uye_adi} harcaması onaylandı: {harcama_tutari} TL (Limit: {limit} TL)", "INFO")
        else:
            durum = "Şartlı / Tutar Yetersiz"
            mesaj = f"⚠️ Dikkat {uye_adi}, harcama tutarı imece ispat sınırının altındadır (Gerekli minimum: {limit} TL)."
            self.log(f"⚠️ {uye_adi} harcaması şartlı onay: {harcama_tutari} TL (Limit: {limit} TL)", "WARNING")

        kayit = {
            "uye": uye_adi,
            "hak_edis": aylik_hak_edis,
            "harcama": harcama_tutari,
            "durum": durum,
            "belge": belge_tipi,
            "tarih": datetime.now().isoformat(),
            "denetim_orani": self.denetim_orani
        }
        self.kayit_ekle(kayit)

        return {"mesaj": mesaj, "durum": durum, "limit": limit, "kayit": kayit}
    
    def fis_gorselinden_tutar_cikar(self, gorsel_yolu: str) -> Optional[float]:
        if not self.gemini_vision_available:
            return None
        
        try:
            with open(gorsel_yolu, "rb") as f:
                image_bytes = f.read()
            
            prompt = "Bu fiş/fatura görselinden sadece toplam tutarı sayısal değer olarak ver (Örn: 1250.50)."
            
            response = self.client.models.generate_content(
                model='gemini-2.5-flash',
                contents=[
                    prompt,
                    {"mime_type": "image/jpeg", "data": image_bytes}
                ]
            )
            tutar = float(response.text.strip().replace(",", ".").replace("TL", ""))
            return tutar
        except Exception as e:
            self.log(f"❌ Görsel işleme hatası: {e}", "ERROR")
            return None

    def whatsapp_mesaj_isle(self, mesaj: str, gorsel_yolu: Optional[str] = None) -> Dict[str, Any]:
        uye_adi = self._uye_adi_cikar(mesaj)
        hak_edis = self._hak_edis_cikar(mesaj)
        harcama_tutari = self.fis_gorselinden_tutar_cikar(gorsel_yolu) if gorsel_yolu else self._tutar_cikar(mesaj)
        
        if not all([uye_adi, hak_edis, harcama_tutari]):
            return {"hata": "Eksik bilgi", "mesaj": "⚠️ Üye adı, hak ediş veya harcama tutarı bulunamadı."}
        
        return self.harcama_degerlendir(uye_adi, hak_edis, harcama_tutari, "WhatsApp Fiş")

    def telegram_mesaj_isle(self, mesaj: str, gorsel_yolu: Optional[str] = None) -> Dict[str, Any]:
        return self.whatsapp_mesaj_isle(mesaj, gorsel_yolu)
    
    def _uye_adi_cikar(self, mesaj: str) -> Optional[str]:
        if "Üye:" in mesaj or "uye:" in mesaj:
            parts = mesaj.split(":")
            if len(parts) > 1: return parts[1].strip().split("\n")[0]
        return None
    
    def _hak_edis_cikar(self, mesaj: str) -> Optional[float]:
        for line in mesaj.split("\n"):
            if "hak ediş" in line.lower() or "hak_edis" in line.lower():
                try: return float(line.split(":")[1].strip())
                except: pass
        return None
    
    def _tutar_cikar(self, mesaj: str) -> Optional[float]:
        for line in mesaj.split("\n"):
            if "harcama" in line.lower():
                try: return float(line.split(":")[1].strip())
                except: pass
        return None
    
    def kayit_ekle(self, yeni_kayit: Dict[str, Any]):
        try:
            with open(self.veri_dosyasi, "r+", encoding="utf-8") as f:
                veriler = json.load(f)
                veriler.append(yeni_kayit)
                f.seek(0)
                json.dump(veriler, f, ensure_ascii=False, indent=4)
        except Exception as e:
            self.log(f"❌ Kayıt ekleme hatası: {e}", "ERROR")
    
    def kayitlari_getir(self) -> list:
        try:
            with open(self.veri_dosyasi, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return []
            
    def stop(self) -> Dict[str, Any]:
        """Ajanı durdurur"""
        self.log("🛑 İmece Denetim Ajanı durduruluyor", "INFO")
        self.is_running = False
        self.status = "stopped"
        return {"status": "stopped", "agent_id": self.agent_id}
    
    def restart(self) -> Dict[str, Any]:
        """Ajanı yeniden başlatır"""
        self.log("🔄 İmece Denetim Ajanı yeniden başlatılıyor", "INFO")
        self.status = "ready"
        self.is_running = True
        return {"status": "restarted", "agent_id": self.agent_id}

    def run(self, operation: str = "denetim", **kwargs) -> Dict[str, Any]:
        if operation == "denetim":
            return self.harcama_degerlendir(kwargs.get("uye_adi", ""), kwargs.get("aylik_hak_edis", 0), kwargs.get("harcama_tutari", 0))
        elif operation == "kayitlar":
            return {"kayitlar": self.kayitlari_getir()}
        return {"hata": "Bilinmeyen işlem"}

if __name__ == "__main__":
    print("🔍 İmece Denetim Ajanı (GenAI Güncel Sürüm) Test Başlıyor...")
    ajan = ImeceDenetimAjani(agent_id=173)
    sonuc = ajan.harcama_degerlendir("Ahmet Yılmaz", 5000, 4200)
    print(sonuc["mesaj"])