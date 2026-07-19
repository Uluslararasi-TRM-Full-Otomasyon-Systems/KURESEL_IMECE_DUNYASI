# -*- coding: utf-8 -*-
"""
TRM Nirvana v3.0 - MASTER CONTROLLER
config/global_config.json içindeki max_ajan_sayisi kadar ajanı,
trm_agents paketinde GERÇEKTEN bulunan ajan sınıflarından dinamik olarak yükler.

NOT: Bu dosya artık "sabit 165/166" gibi hayali sayılar içermiyor. Sistem
kaç ajan başlatacağını iki şeyin kesişiminden belirler:
  1) config/global_config.json -> sistem.max_ajan_sayisi (HEDEF sayı)
  2) trm_agents paketinde fiilen bulunan, çalıştırılabilir ajan sınıfları (GERÇEK sayı)
Bu iki sayı her zaman aynı olmayabilir - kod bunu gizlemek yerine açıkça raporlar.
"""
import os
import importlib
import inspect
import logging
import pkgutil

from config import MAX_AJAN_SAYISI, LOG_DIR, REPORT_DIR
from trm_agents.governance.integration_hook import GovernanceBridge

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(os.path.join(LOG_DIR, "master_controller.log"), encoding="utf-8"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("MASTER_CONTROLLER")

AGENTS_PACKAGE = "trm_agents"


def discover_agent_classes():
    """trm_agents paketindeki her modülü tarar, içinde 'Agent' ile biten ve
    çalıştırılabilir bir .run() metoduna sahip sınıfları bulur.

    Her modül import edilirken oluşabilecek hata (eksik dosya, syntax hatası,
    bozuk bağımlılık vb.) tek tek yakalanır; bir ajanın çökmesi diğerlerinin
    yüklenmesini engellemez.
    """
    discovered = []  # [(sınıf_adı, sınıf, modül_adı)]

    try:
        package = importlib.import_module(AGENTS_PACKAGE)
    except ModuleNotFoundError:
        logger.error(f"'{AGENTS_PACKAGE}' paketi bulunamadı. Hiç ajan yüklenemedi.")
        return discovered

    package_path = getattr(package, "__path__", None)
    if package_path is None:
        logger.error(f"'{AGENTS_PACKAGE}' bir paket değil (namespace/__init__ eksik olabilir).")
        return discovered

    for _, module_name, _ in sorted(pkgutil.iter_modules(package_path), key=lambda m: m.name):
        full_module_name = f"{AGENTS_PACKAGE}.{module_name}"
        try:
            module = importlib.import_module(full_module_name)
        except Exception as e:
            logger.error(f"⚠️ '{full_module_name}' import edilemedi, atlanıyor: {e}")
            continue

        for cls_name, cls in inspect.getmembers(module, inspect.isclass):
            if cls.__module__ != full_module_name:
                continue  # başka modülden import edilmiş sınıfları tekrar sayma
            if not cls_name.endswith("Agent"):
                continue
            if not hasattr(cls, "run"):
                logger.warning(f"⚠️ '{cls_name}' bulundu ama .run() metodu yok, atlanıyor.")
                continue
            discovered.append((cls_name, cls, full_module_name))

    return discovered


class TRMMasterController:
    def __init__(self):
        logger.info("TRM Master Controller karargahı başlatılıyor...")
        self.max_ajan_sayisi = MAX_AJAN_SAYISI  # HEDEF: global_config.json'dan
        self.agent_classes = discover_agent_classes()  # GERÇEK: koddan bulunanlar
        self.agent_instances = []
        self.governance = GovernanceBridge()

        logger.info(
            f"Hedef ajan sayısı (config): {self.max_ajan_sayisi} | "
            f"trm_agents paketinde bulunan gerçek ajan sınıfı: {len(self.agent_classes)}"
        )

        for cls_name, cls, module_name in self.agent_classes:
            try:
                instance = cls()
                self.agent_instances.append((cls_name, instance))
                logger.info(f"✅ '{cls_name}' ({module_name}) initialize edildi.")
            except Exception as e:
                logger.error(f"⚠️ '{cls_name}' initialize edilirken hata: {e}")

    def start_all_services(self):
        """trm_agents paketinde bulunan tüm ajanların .run() metodunu tetikler."""
        logger.info("Otonom servisler sırayla devreye alınıyor...")

        started = 0
        for cls_name, instance in self.agent_instances:
            current_log = {
                "agent_name": cls_name,
                "status": "pending",
            }
            try:
                instance.run()
                started += 1
                current_log["status"] = "success"
                logger.info(f"✅ '{cls_name}' başarıyla tetiklendi.")
            except Exception as e:
                current_log["status"] = "error"
                current_log["error"] = str(e)
                logger.error(f"⚠️ '{cls_name}' çalıştırılırken hata: {e}")
            self.governance.run_governance_cycle(current_log)

        eksik = self.max_ajan_sayisi - started
        logger.info(
            f"Karargah aktif! {started}/{self.max_ajan_sayisi} ajan fiilen çalışıyor."
        )
        if eksik > 0:
            logger.warning(
                f"⚠️ Hedeflenen {self.max_ajan_sayisi} ajanın {eksik} tanesi için "
                f"henüz trm_agents paketinde kod yok. Bu ajanlar 'çalışıyor' olarak "
                f"raporlanmıyor çünkü fiilen mevcut değiller."
            )
        return started

    def generate_system_status_report(self):
        """Genel durum raporunu üretir - hedef ile gerçek ajan sayısını ayrı ayrı içerir."""
        import json
        from datetime import datetime

        report_path = os.path.join(REPORT_DIR, "system_status.json")
        report = {
            "timestamp": datetime.now().isoformat(),
            "hedef_ajan_sayisi": self.max_ajan_sayisi,
            "kodda_bulunan_ajan_sayisi": len(self.agent_classes),
            "fiilen_calisan_ajan_sayisi": len(self.agent_instances),
            "ajanlar": [cls_name for cls_name, _ in self.agent_instances],
        }
        with open(report_path, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=4, ensure_ascii=False)

        logger.info(f"Sistem durum raporu oluşturuldu: {report_path}")
        return report_path


if __name__ == "__main__":
    controller = TRMMasterController()
    controller.start_all_services()
    controller.generate_system_status_report()
