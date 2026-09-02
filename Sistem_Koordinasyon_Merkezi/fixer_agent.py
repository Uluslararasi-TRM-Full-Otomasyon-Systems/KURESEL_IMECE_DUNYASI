import json
import sys
from datetime import datetime
from pathlib import Path


CURRENT_DIR = Path(__file__).resolve().parent
ROOT_DIR = CURRENT_DIR.parent
GURUPLAR_DIR = ROOT_DIR / "Uluslararası TRM Otonom Ekosistemi grupları"
ANALIZ_DOSYASI = CURRENT_DIR / "affiliate_hata_analizi.json"
MUDAHALE_LOG_DOSYASI = CURRENT_DIR / "müdahale_logları.jsonl"

if str(ROOT_DIR) not in sys.path:
    sys.path.append(str(ROOT_DIR))

from guardian_daemon import clear_tenant_cache, restart_tenant_service  # noqa: E402


def analiz_verisini_yukle():
    if not ANALIZ_DOSYASI.exists():
        return {}
    try:
        return json.loads(ANALIZ_DOSYASI.read_text(encoding="utf-8"))
    except Exception:
        return {}


def mudahale_kaydini_yaz(payload):
    MUDAHALE_LOG_DOSYASI.parent.mkdir(parents=True, exist_ok=True)
    with MUDAHALE_LOG_DOSYASI.open("a", encoding="utf-8") as stream:
        stream.write(json.dumps(payload, ensure_ascii=False) + "\n")


def tenant_log_icerigini_topla(tenant_bilgisi):
    metinler = []
    for relative_path in tenant_bilgisi.get("taranan_loglar", []):
        log_path = ROOT_DIR / relative_path
        if not log_path.exists():
            continue
        try:
            content = log_path.read_text(encoding="utf-8", errors="ignore")
            metinler.append(content[-3000:])
        except Exception:
            continue
    return "\n".join(metinler).lower()


def hata_tipini_analiz_et(tenant_adi, tenant_bilgisi):
    havuz = " ".join(
        [
            tenant_adi,
            str(tenant_bilgisi.get("baskin_hata_tipi", "")),
            str(tenant_bilgisi.get("yonetici_ozeti", "")),
            str(tenant_bilgisi.get("operasyon_karari", "")),
            tenant_log_icerigini_topla(tenant_bilgisi),
        ]
    ).lower()

    if any(keyword in havuz for keyword in ("cache", "__pycache__", ".cache", "cache_hatasi", "cache hatasi")):
        return "cache_hatasi"
    if any(keyword in havuz for keyword in ("timeout", "api_timeout", "connection timed out", "read timed out", "gateway timeout")):
        return "api_timeout"
    if any(
        keyword in havuz
        for keyword in (
            "permission denied",
            "access is denied",
            "dosya",
            "file not found",
            "errno 2",
            "no such file",
            "path not found",
            "dosya_erişim_hatası",
            "dosya_erisim_hatasi",
        )
    ):
        return "dosya_erişim_hatası"
    return "operasyon_hatasi"


def tenant_yolu_bul(tenant_adi):
    return GURUPLAR_DIR / tenant_adi


def tenant_mudahalesi_yap(tenant_adi, tenant_bilgisi):
    tenant_yolu = tenant_yolu_bul(tenant_adi)
    hata_tipi = hata_tipini_analiz_et(tenant_adi, tenant_bilgisi)
    cozumler = []
    sonuc_detaylari = []

    if not tenant_yolu.exists():
        cozum = "tenant_klasoru_bulunamadi"
        payload = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "tenant": tenant_adi,
            "hata": hata_tipi,
            "cozum": cozum,
            "kayit": f"Tenant: {tenant_adi}, Hata: {hata_tipi}, Çözüm: {cozum}",
        }
        mudahale_kaydini_yaz(payload)
        return payload

    if hata_tipi == "cache_hatasi":
        temizleme = clear_tenant_cache(tenant_yolu)
        cozumler.append("cache_temizligi")
        sonuc_detaylari.append(temizleme)
    elif hata_tipi == "api_timeout":
        yeniden_baslat = restart_tenant_service(tenant_yolu)
        cozumler.append("servis_yeniden_baslatma")
        sonuc_detaylari.append(yeniden_baslat)
    elif hata_tipi == "dosya_erişim_hatası":
        temizleme = clear_tenant_cache(tenant_yolu)
        yeniden_baslat = restart_tenant_service(tenant_yolu)
        cozumler.extend(["cache_temizligi", "servis_yeniden_baslatma"])
        sonuc_detaylari.extend([temizleme, yeniden_baslat])
    else:
        temizleme = clear_tenant_cache(tenant_yolu)
        yeniden_baslat = restart_tenant_service(tenant_yolu)
        cozumler.extend(["genel_cache_temizligi", "servis_yeniden_baslatma"])
        sonuc_detaylari.extend([temizleme, yeniden_baslat])

    cozum = " + ".join(cozumler) if cozumler else "müdahale_yok"
    payload = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "tenant": tenant_adi,
        "hata": hata_tipi,
        "cozum": cozum,
        "detaylar": sonuc_detaylari,
        "kayit": f"Tenant: {tenant_adi}, Hata: {hata_tipi}, Çözüm: {cozum}",
    }
    mudahale_kaydini_yaz(payload)
    return payload


def otonom_tamir_merkezi_calistir():
    analizler = analiz_verisini_yukle()
    if not isinstance(analizler, dict):
        return []

    mudahale_sonuclari = []
    for tenant_adi, tenant_bilgisi in analizler.items():
        risk = str(tenant_bilgisi.get("risk_seviyesi", "")).lower()
        if risk != "yuksek":
            continue
        mudahale_sonuclari.append(tenant_mudahalesi_yap(tenant_adi, tenant_bilgisi))

    return mudahale_sonuclari


if __name__ == "__main__":
    sonuclar = otonom_tamir_merkezi_calistir()
    print(json.dumps(sonuclar, ensure_ascii=False, indent=2))
