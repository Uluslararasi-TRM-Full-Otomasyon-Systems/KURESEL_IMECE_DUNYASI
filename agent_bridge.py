from typing import Dict, Any, List
import json
import os
from datetime import datetime

class AgentBridge:
    def __init__(self, veri_dosyasi: str = "sozlesme_onaylari.json"):
        self.veri_dosyasi = veri_dosyasi
        self._dosya_kontrol()

    def _dosya_kontrol(self):
        if not os.path.exists(self.veri_dosyasi):
            with open(self.veri_dosyasi, "w", encoding="utf-8") as f:
                json.dump([], f, ensure_ascii=False, indent=4)

    def onay_gecmisi(self, kullanici_id: str = None) -> Dict[str, Any]:
        """
        Kayıtlı onay geçmişini getirir veya belirli bir kullanıcıyı arar.
        """
        try:
            with open(self.veri_dosyasi, "r", encoding="utf-8") as f:
                onaylar = json.load(f)
            
            if kullanici_id:
                filtrelenmis = [o for o in onaylar if o.get("kullanici_id") == kullanici_id]
                return {
                    "durum": "basarili",
                    "toplam_onay": len(filtrelenmis),
                    "onaylar": filtrelenmis
                }
            
            return {
                "durum": "basarili",
                "toplam_onay": len(onaylar),
                "onaylar": onaylar
            }
        except Exception as e:
            return {
                "durum": "hata",
                "mesaj": str(e),
                "onaylar": []
            }

    def kullanici_onayi_islet(self, kullanici_id: str, sozlesme_versiyonu: str) -> Dict[str, Any]:
        """
        Yeni bir kullanıcı onayını kayda geçirir.
        """
        try:
            timestamp = datetime.now().isoformat()
            yeni_kayit = {
                "onay_id": f"onay_{int(datetime.now().timestamp())}",
                "kullanici_id": kullanici_id,
                "sozlesme_versiyonu": sozlesme_versiyonu,
                "timestamp": timestamp,
                "durum": "onaylandi"
            }

            with open(self.veri_dosyasi, "r+", encoding="utf-8") as f:
                veriler = json.load(f)
                veriler.append(yeni_kayit)
                f.seek(0)
                json.dump(veriler, f, ensure_ascii=False, indent=4)

            return {
                "durum": "basarili",
                "mesaj": "Onay başarıyla kaydedildi.",
                "kayit": yeni_kayit
            }
        except Exception as e:
            return {
                "durum": "hata",
                "mesaj": str(e)
            }