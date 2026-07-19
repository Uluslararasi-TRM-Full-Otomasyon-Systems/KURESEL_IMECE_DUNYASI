import json
import os
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

CONFIG_PATH = "config/global_config.json"

def load_config():
    if not os.path.exists(CONFIG_PATH):
        os.makedirs(os.path.dirname(CONFIG_PATH), exist_ok=True)
        default_config = {
            "sistem": {
                "max_ajan_sayisi": 200
            },
            "icerik": {
                "api_key": "",
                "hedef_dil": "tr",
                "günlük_limit": 100,
                "ton": "profesyonel"
            },
            "seo": {
                "hedef_pazar": "TR",
                "anahtar_kelime_stratejisi": "uzun_kuyruk",
                "backlink_kalitesi": 80,
                "günlük_denetim": True
            },
            "finans": {
                "kar_marji": 25,
                "affiliate_komisyon_orani": 15,
                "doviz_kuru_kaynak": "canli",
                "entegre_firmalar": ["Amazon", "Trendyol", "ClickBank"]
            },
            "dnp": {
                "optimizasyon_modu": "agresif",
                "denetim_araligi_sn": 300,
                "hedef_agent_senkronizasyonu": True,
                "parametre_esik_degerleri": {
                    "api_gectikme_ms": 200,
                    "cpu_esik_yuzde": 75
                }
            }
        }
        logger.info(f"Varsayılan config oluşturuldu: {CONFIG_PATH}, max ajan sayısı: {default_config['sistem']['max_ajan_sayisi']}")
        with open(CONFIG_PATH, "w", encoding="utf-8") as f:
            json.dump(default_config, f, indent=4, ensure_ascii=False)
        return default_config

    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        config = json.load(f)
        max_ajan = config.get("sistem", {}).get("max_ajan_sayisi", 200)
        logger.info(f"Config yüklendi: {CONFIG_PATH}, max ajan sayısı: {max_ajan}")
        return config

def save_config(config):
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=4, ensure_ascii=False)