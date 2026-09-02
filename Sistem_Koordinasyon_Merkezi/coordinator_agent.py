import json
import sys
from datetime import datetime
from pathlib import Path


CURRENT_DIR = Path(__file__).resolve().parent
ROOT_DIR = CURRENT_DIR.parent

if str(ROOT_DIR) not in sys.path:
    sys.path.append(str(ROOT_DIR))

from koordinasyon_kurulumu import (  # noqa: E402
    AFFILIATE_ANALIZ_DOSYASI,
    AKILLI_ANALIZ_PROMPT_DOSYASI,
    AKILLI_ANALIZ_PROMPTU,
    GURUPLAR_DIR,
    KOORDINASYON_MERKEZI,
    MERKEZI_KONTROL_LOG,
    affiliate_loglarini_analiz_et,
    log_dosyalarini_bul,
    yaz_jsonl,
)


def merkezi_analiz_yap():
    KOORDINASYON_MERKEZI.mkdir(parents=True, exist_ok=True)
    AKILLI_ANALIZ_PROMPT_DOSYASI.write_text(AKILLI_ANALIZ_PROMPTU, encoding="utf-8")

    tum_tenantlar = {}
    analiz_sonuclari = affiliate_loglarini_analiz_et()

    for analiz in analiz_sonuclari:
        tenant = analiz["tenant_adi"]
        tenant_yolu = GURUPLAR_DIR / tenant
        taranan_loglar = []
        if tenant_yolu.exists():
            taranan_loglar = [str(path.relative_to(ROOT_DIR)) for path in log_dosyalarini_bul(tenant_yolu)]

        tum_tenantlar[tenant] = {
            "durum": "aktif" if analiz["risk_seviyesi"] != "yuksek" else "kritik_izleme",
            "taranan_loglar": taranan_loglar,
            "toplam_olay": analiz["toplam_olay"],
            "hata_sayisi": analiz["hata_sayisi"],
            "kritik_hata_sayisi": analiz["kritik_hata_sayisi"],
            "hata_orani_yuzde": analiz["hata_orani_yuzde"],
            "risk_seviyesi": analiz["risk_seviyesi"],
            "operasyon_karari": analiz["operasyon_karari"],
            "son_hata_zamani": analiz["son_hata_zamani"],
            "baskin_hata_tipi": analiz["baskin_hata_tipi"],
            "yonetici_ozeti": analiz["yonetici_ozeti"],
        }

    AFFILIATE_ANALIZ_DOSYASI.write_text(
        json.dumps(tum_tenantlar, ensure_ascii=False, indent=4),
        encoding="utf-8",
    )

    yaz_jsonl(
        MERKEZI_KONTROL_LOG,
        {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "event": "koordinator_merkezi_analiz",
            "tenant_sayisi": len(tum_tenantlar),
            "rapor_dosyasi": str(AFFILIATE_ANALIZ_DOSYASI),
        },
    )

    print(f"Analiz raporu güncellendi: {AFFILIATE_ANALIZ_DOSYASI}")
    return tum_tenantlar


if __name__ == "__main__":
    merkezi_analiz_yap()
