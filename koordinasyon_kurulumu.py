import json
import os
import shutil
from datetime import datetime
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parent
BASE_DIR = ROOT_DIR
GURUPLAR_DIR = BASE_DIR / "Uluslararası TRM Otonom Ekosistemi grupları"
ANA_SISTEM_KAYNAK = BASE_DIR / "Uluslararası TRM Otonom Ekosistemi"
KOORDINASYON_MERKEZI = BASE_DIR / "Sistem_Koordinasyon_Merkezi"
MERKEZI_KONTROL_LOG = KOORDINASYON_MERKEZI / "merkezi_kontrol_log.jsonl"
AKILLI_ANALIZ_PROMPT_DOSYASI = KOORDINASYON_MERKEZI / "akilli_analiz_promptu.txt"
AFFILIATE_ANALIZ_DOSYASI = KOORDINASYON_MERKEZI / "affiliate_hata_analizi.json"

HATA_ANAHTAR_KELIMELERI = (
    "error",
    "failed",
    "failure",
    "critical",
    "exception",
    "traceback",
    "timeout",
    "restore",
    "onarim yetersiz",
)

AKILLI_ANALIZ_PROMPTU = """
SENIN ROLUN:
- Sen, Sistem Koordinasyon Merkezi icin calisan bir log analiz koordinatörüsün.

GOREVIN:
- Affiliate firma klasorlerinden gelen guardian, worker ve operasyon loglarini oku.
- Her tenant icin toplam olay, hata olayi, kritik hata adedi, son hata zamani ve baskin hata tipini tespit et.
- Hata oranini su formulle hesapla:
  hata_orani = (hata_olayi / toplam_olay) * 100
- Aşağıdaki durumlarda kaydi "kritik" say:
  - satirda CRITICAL geciyorsa
  - status=FAILED varsa
  - exception/traceback varsa
  - onarim yetersiz ifadesi varsa

ANALIZ CIKTISI:
- Tenant adi
- Toplam olay sayisi
- Hata sayisi
- Kritik hata sayisi
- Hata orani yuzdesi
- Risk seviyesi:
  - 0-5   => dusuk
  - 5-15  => orta
  - 15+   => yuksek
- Operasyon karari:
  - dusuk => izlemeye devam et
  - orta  => guardian sikligini artir
  - yuksek => manuel inceleme ve backup dogrulamasi baslat

NOT:
- JSONL satirlarini once JSON olarak parse etmeyi dene.
- JSON parse olmuyorsa satiri serbest metin olarak tara.
- Analiz sonunda tek satirlik yonetici ozeti uret:
  "Tenant X son 24 saatte Y hata ve Z kritik olay uretmistir."
""".strip()


def yaz_jsonl(log_dosyasi, payload):
    log_dosyasi.parent.mkdir(parents=True, exist_ok=True)
    with log_dosyasi.open("a", encoding="utf-8") as stream:
        stream.write(json.dumps(payload, ensure_ascii=False) + "\n")


def akilli_analiz_promptunu_yaz():
    AKILLI_ANALIZ_PROMPT_DOSYASI.write_text(AKILLI_ANALIZ_PROMPTU, encoding="utf-8")


def log_dosyalarini_bul(tenant_klasoru):
    desenler = [
        "guardian_central_log.jsonl",
        "guardian_events.jsonl",
        "worker_status.json",
        "*.log",
        "logs/*.log",
    ]
    bulunanlar = []
    for desen in desenler:
        bulunanlar.extend(tenant_klasoru.glob(desen))
    return [path for path in bulunanlar if path.is_file()]


def log_kaydi_coz(satir):
    satir = satir.strip()
    if not satir:
        return None
    try:
        return json.loads(satir)
    except Exception:
        return {"raw_text": satir}


def kayit_hata_mi(kayit):
    metin = json.dumps(kayit, ensure_ascii=False).lower()
    if str(kayit.get("status", "")).upper() == "FAILED":
        return True
    return any(anahtar in metin for anahtar in HATA_ANAHTAR_KELIMELERI)


def kayit_kritik_mi(kayit):
    metin = json.dumps(kayit, ensure_ascii=False).lower()
    return (
        "critical" in metin
        or "onarim yetersiz" in metin
        or str(kayit.get("status", "")).upper() == "FAILED"
    )


def risk_seviyesi_hesapla(hata_orani):
    if hata_orani < 5:
        return "dusuk", "izlemeye devam et"
    if hata_orani < 15:
        return "orta", "guardian sikligini artir"
    return "yuksek", "manuel inceleme ve backup dogrulamasi baslat"


def tenant_loglarini_analiz_et(tenant_klasoru):
    log_dosyalari = log_dosyalarini_bul(tenant_klasoru)
    toplam_olay = 0
    hata_sayisi = 0
    kritik_sayisi = 0
    son_hata_zamani = ""
    baskin_hata_tipi = "normal"

    for log_dosyasi in log_dosyalari:
        if log_dosyasi.suffix.lower() == ".json":
            try:
                payload = json.loads(log_dosyasi.read_text(encoding="utf-8"))
                kayitlar = payload if isinstance(payload, list) else [payload]
            except Exception:
                kayitlar = [{"raw_text": log_dosyasi.read_text(encoding="utf-8", errors="ignore")}]
        else:
            kayitlar = [log_kaydi_coz(satir) for satir in log_dosyasi.read_text(encoding="utf-8", errors="ignore").splitlines()]

        for kayit in kayitlar:
            if not kayit:
                continue
            toplam_olay += 1
            if kayit_hata_mi(kayit):
                hata_sayisi += 1
                baskin_hata_tipi = kayit.get("event") or kayit.get("status") or "operasyon_hatasi"
                son_hata_zamani = kayit.get("timestamp", son_hata_zamani)
            if kayit_kritik_mi(kayit):
                kritik_sayisi += 1

    hata_orani = round((hata_sayisi / toplam_olay) * 100, 2) if toplam_olay else 0.0
    risk_seviyesi, operasyon_karari = risk_seviyesi_hesapla(hata_orani)
    tenant_adi = tenant_klasoru.name

    return {
        "tenant_adi": tenant_adi,
        "toplam_olay": toplam_olay,
        "hata_sayisi": hata_sayisi,
        "kritik_hata_sayisi": kritik_sayisi,
        "hata_orani_yuzde": hata_orani,
        "risk_seviyesi": risk_seviyesi,
        "operasyon_karari": operasyon_karari,
        "son_hata_zamani": son_hata_zamani,
        "baskin_hata_tipi": baskin_hata_tipi,
        "yonetici_ozeti": f"Tenant {tenant_adi} son 24 saatte {hata_sayisi} hata ve {kritik_sayisi} kritik olay uretmistir.",
    }


def affiliate_loglarini_analiz_et():
    if not GURUPLAR_DIR.exists():
        return []

    analiz_sonuclari = []
    for tenant_klasoru in sorted(GURUPLAR_DIR.iterdir()):
        if not tenant_klasoru.is_dir():
            continue
        sonuc = tenant_loglarini_analiz_et(tenant_klasoru)
        analiz_sonuclari.append(sonuc)

    AFFILIATE_ANALIZ_DOSYASI.write_text(
        json.dumps(analiz_sonuclari, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    yaz_jsonl(
        MERKEZI_KONTROL_LOG,
        {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "event": "affiliate_log_analizi",
            "tenant_sayisi": len(analiz_sonuclari),
            "analiz_sonuclari": analiz_sonuclari,
        },
    )
    return analiz_sonuclari


def tek_seferde_kurulum():
    for dizin in [GURUPLAR_DIR, KOORDINASYON_MERKEZI]:
        if not dizin.exists():
            dizin.mkdir(parents=True, exist_ok=True)
            print(f"Klasör oluşturuldu: {dizin}")

    hedef_ana_sistem = GURUPLAR_DIR / "trendurunlermarket.com"
    if ANA_SISTEM_KAYNAK.exists() and not hedef_ana_sistem.exists():
        shutil.copytree(ANA_SISTEM_KAYNAK, hedef_ana_sistem)
        print("Ana sistem 'trendurunlermarket.com' olarak klonlandı.")

    if not MERKEZI_KONTROL_LOG.exists():
        MERKEZI_KONTROL_LOG.write_text("", encoding="utf-8")

    akilli_analiz_promptunu_yaz()
    analiz_sonuclari = affiliate_loglarini_analiz_et()

    print("\n--- SİSTEM KURULUMU TAMAMLANDI ---")
    print("Yapı: Guruplar/trendurunlermarket.com ve Sistem_Koordinasyon_Merkezi hazır.")
    print(f"Akıllı analiz promptu: {AKILLI_ANALIZ_PROMPT_DOSYASI}")
    print(f"Analiz edilen tenant sayısı: {len(analiz_sonuclari)}")


if __name__ == "__main__":
    tek_seferde_kurulum()
