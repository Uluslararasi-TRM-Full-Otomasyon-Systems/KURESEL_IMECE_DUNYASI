from trm_agents.kuresel_video_fabrikasi_ajani import trigger_video_production
from trm_agents.social_uploader_agent import trigger_social_upload
from trm_agents.SUPER_AUDITOR_AGENT import trigger_system_audit

def main():
    # 1. Önce pinpirikli sistem denetimini yap
    trigger_system_audit()

    # 2. Üretim ve Dağıtım Operasyonu
    product = "High_End_Electronics"
    pazarlar = ["Japanese", "German", "English", "Spanish", "Turkish"]
    
    print(f"\n[BAŞLAT] Otonom üretim ve dağıtım döngüsü: {product}")
    
    for dil in pazarlar:
        print(f"\n--- [ORCHESTRATOR] {dil} pazarı için operasyon başlatılıyor ---")
        try:
            # Üretim
            video_path = trigger_video_production(product, language=dil)
            # Yükleme
            trigger_social_upload(video_path, language=dil)
            print(f"[BAŞARI] {dil} pazarı için içerik yayında.")
        except Exception as e:
            print(f"[HATA] {dil} pazarı operasyonunda sorun oluştu: {e}")

if __name__ == "__main__":
    main()