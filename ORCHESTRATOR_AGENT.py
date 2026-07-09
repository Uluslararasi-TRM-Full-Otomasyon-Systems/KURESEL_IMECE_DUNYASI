import os
import sys

# Sistemin ana dizinini (KURESEL_IMECE_DUNYASI) otomatik bulur
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)

from trm_agents.kuresel_video_fabrikasi_ajani import trigger_video_production
from trm_agents.social_uploader_agent import trigger_social_upload
from trm_agents.SUPER_AUDITOR_AGENT import trigger_system_audit

def main(product="High_End_Electronics", pazarlar=None):
    """Ana orkestrasyon fonksiyonu - parametreli çalışabilir"""
    if pazarlar is None:
        pazarlar = ["Japanese", "German", "English", "Spanish", "Turkish"]
    
    # 1. Önce pinpirikli sistem denetimini yap
    trigger_system_audit()

    # 2. Üretim ve Dağıtım Operasyonu
    print(f"\n[BAŞLAT] Otonom üretim ve dağıtım döngüsü: {product}")
    
    results = []
    for dil in pazarlar:
        print(f"\n--- [ORCHESTRATOR] {dil} pazarı için operasyon başlatılıyor ---")
        try:
            # Üretim
            video_path = trigger_video_production(product, language=dil)
            # Yükleme
            upload_result = trigger_social_upload(video_path, language=dil)
            print(f"[BAŞARI] {dil} pazarı için içerik yayında.")
            results.append({
                "market": dil,
                "status": "BAŞARI",
                "video_path": video_path,
                "upload_result": upload_result
            })
        except Exception as e:
            print(f"[HATA] {dil} pazarı operasyonunda sorun oluştu: {e}")
            results.append({
                "market": dil,
                "status": "HATA",
                "error": str(e)
            })
    
    return results

if __name__ == "__main__":
    main()