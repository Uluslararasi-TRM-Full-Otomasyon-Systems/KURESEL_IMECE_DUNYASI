import os
from trm_agents.monetization_manager import trigger_monetization_cycle
from trm_agents.kuresel_video_fabrikasi_ajani import trigger_video_production

class SwarmMemory:
    memory = {}
    @classmethod
    def set_data(cls, key, value): cls.memory[key] = value

def run_autonomous_cycle(product_name):
    print(f"[BAŞLAT] Otonom üretim ve kazanç döngüsü: {product_name}")
    
    # 1. Sürü Zekası veri paylaşımı
    SwarmMemory.set_data("Aktif_Urun", product_name)
    
    # 2. Video Üretimi (Fabrikayı çalıştır)
    video_path = trigger_video_production(product_name)
    
    # 3. Ticari Motorun Tetiklenmesi
    success = trigger_monetization_cycle(product_name)
    
    if success and video_path:
        print("[BAŞARI] Video üretildi ve kazanç hattına aktarıldı. Sistem 7/24 hazır.")
    else:
        print("[HATA] Üretim hattında bir sorun oluştu.")

if __name__ == "__main__":
    try:
        run_autonomous_cycle("High_End_Electronics")
    except Exception as e:
        print(f"[HATA] Sistem durdu: {e}")