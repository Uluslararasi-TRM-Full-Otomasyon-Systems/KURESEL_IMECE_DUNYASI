# -*- coding: utf-8 -*-
"""Masaüstü envanter TXT üretici — tek seferlik."""
import ast
import json
import os
from datetime import datetime
from pathlib import Path

ROOT = Path(r"C:\Users\Habitat\Desktop\sosyal_imece")
OUT = Path(r"C:\Users\Habitat\Desktop") / "Sosyal_Imece_Dosya_Envanteri_Olusturma_Hikayeleri.txt"
WORD_SRC = Path(r"C:\Users\Habitat\Desktop\Sosyal İmece ile İlgili Önemli Bölümleri")

SKIP_DIR_NAMES = {
    ".git", ".venv", "venv", "__pycache__", ".vendor", "node_modules",
    ".aider.tags.cache.v4", "Lib", "site-packages", ".streamlit",
}

SKIP_PATH_PARTS = {"site-packages", "Lib\\site-packages", "Scripts"}

STORY_BY_NAME = {
    "app.py": (
        "Ana Streamlit arayüzü ve komuta merkezi. Word belgesindeki Gemini sohbetlerinde "
        "sürekli 'Küresel İmece Dünyası & Otonom Ajanlar Komuta Merkezi' olarak anılır; "
        "streamlit run app.py ile ayağa kalkması istenir. Mevcut hali TRM Nirvana v3.0 "
        "Otonom Komuta Merkezi: kenar çubuğundan MASTER_CONTROLLER.start_all_services ve "
        "GeoEcommerceFusionEngine.run_fusion_analysis tetiklenir. Üç sekme reports/ altındaki "
        "system_status.json, geo_fusion_master_report.json ve dynamic_agent_*.json dosyalarını "
        "okur. Nedeni: kod ajanlarını tek tıkla yönetmek, 200 ajan kapasitesini ve coğrafi "
        "füzyonu görsel olarak izlemek; UTEYKDER/DERBİS sekmeleri belgede tarif edilmiş olsa da "
        "bu sürüme sadeleştirilmiş komuta paneli olarak şekillenmiştir."
    ),
    "behavioral_marketing_agent.py": (
        "Davranışsal pazarlama ve sosyal dağıtım ajanı. Orta/üst segment e-ticaret "
        "(trendurunlermarket.com / İR-SA AŞ afiliye) kullanıcı oturumunu (gezinti, sepet, niş) "
        "analiz eder, kişiselleştirilmiş mesaj üretir ve social_accounts_pool üzerinden 100 hesaplık "
        "dağıtımı tetikler. Keep-alive worker, APP_URL'e 10 dakikada bir ping atarak Render/Streamlit "
        "ücretsiz katmanın uykuya geçmesini önlemek için sonradan eklenmiştir. Nedeni: Sosyal İmece "
        "gelirinin sosyal medya üzerinden hedefli satışa bağlanması; belgedeki 'halka dokunan tanıtım' "
        "vizyonunun kod karşılığıdır."
    ),
    "requirements.txt": (
        "Python paket bağımlılık listesi. Word belgesi Streamlit Cloud derleme loglarını içerir: "
        "streamlit==1.59.2, pandas==3.0.3, numpy==1.26.4 vb. pip ile çekilir. Yorum satırı açıkça "
        "'Render Free Tier Optimized' ve 512MB RAM limiti der. GitHub'a git add requirements.txt "
        "ve --force ile gönderilerek Cloud'un 'hatasız derlenmesi' sağlanmıştır. Nedeni: her ortamda "
        "(yerel, Render, Streamlit Cloud, Hugging Face Spaces) aynı paket sürümlerinin kurulması."
    ),
    "runtime.txt": (
        "İçinde yalnızca '3.11' yazar. Heroku/Render/Streamlit tarzı PaaS, bu dosyayı görüp "
        "Python 3.11 runtime seçer. Nedeni: ajan kodunun 3.12/3.13 sapmalarına düşmeden belgelenen "
        "sürüme kilitlenmesi."
    ),
    ".gitignore": (
        "Git hariç tutma listesi. Mevcut içerik: büyük HTML panel zip'i, media_out/, *.mp3, "
        "tanitim_ses.mp3 ve .streamlit/secrets.toml. Nedeni: gizli anahtarların, ses/medya "
        "çıktılarının ve gereksiz büyük arşivlerin depoya sızmaması. Word belgesinde Nöbetçi ajanın "
        "*.py filtresiyle .gitignore satırını bile syntax sanması anlatılır; bu yüzden metin/rapor "
        "dosyalarının yanlışlıkla .py uzantısı alması da ayrı bir risk olarak belgelenmiştir."
    ),
    "system_status.json": (
        "Sistem sağlık ve durum raporu. MASTER_CONTROLLER.generate_system_status_report() "
        "tarafından reports/ altına yazılır. app.py kenar çubuğundaki 'Tüm Sistemi ve 200 Ajanı "
        "Tetikle' bu raporu üretir ve 1. sekmede metrik olarak gösterir. Örnek içerik (2026-09-01): "
        "hedef 200 ajan, kodda gerçek 22 sınıf, toplam aktif 200 (22 gerçek + 178 dinamik tamamlayıcı). "
        "Nedeni: '200 ajan vizyonu' ile diskteki gerçek kod sayısının farkını görünür kılmak."
    ),
    "geo_fusion_master_report.json": (
        "Coğrafi füzyon ve e-ticaret analiz raporu. trm_agents/geo_fusion_core.py içindeki "
        "GeoEcommerceFusionEngine.run_fusion_analysis() Hoodmaps + Endeksa + GeoSpy senkron özetini "
        "www.trendurunlermarket.com bölgesel lojistik/fiyat önerisiyle birleştirip yazar. app.py "
        "2. sekme bu JSON'u okur. Nedeni: Ege/Marmara/İç Anadolu (Kuşadası–Nazilli hattı) için "
        "bölge bazlı dinamik fiyat ve teslimat hazırlığını tek raporda tutmak."
    ),
    "MASTER_CONTROLLER.py": (
        "Dinamik fabrika entegreli ana orkestratör. config/global_config.json'daki max_ajan_sayisi "
        "kadar ajanı trm_agents gerçek sınıfları + dynamic_factory ile yükler; Flask API (port 5000), "
        "24/7 döngü, graceful shutdown ve system_status.json üretimi burada. Procfile 'web: python "
        "MASTER_CONTROLLER.py' der. Nedeni: Streamlit paneli (app.py) komuta yüzeyi iken bu dosya "
        "arka plandaki ajan ordusunun gerçek çalışma motorudur."
    ),
    "dynamic_factory.py": (
        "Eksik ajan üretici. Kodda ~22 gerçek ajan sınıfı varken hedef 200 olduğu için "
        "generate_missing_agents(start_id=23, total_target=200) Lojistik / Bölgesel Kalkınma / "
        "Dijital Pazarlama / Veri Doğrulama / Denetim Destek döngüsüyle TRM_Core_Agent_023..200 "
        "üretilir. Her ajan execute_task ile reports/dynamic_agent_NNN.json yazar. Nedeni: Word "
        "belgesindeki '200 ajan kapasitesi' vaadini kodda doldurmak; gerçek iş mantığı olmayan "
        "slotları rapor üreten iskelet ajanlarla tamamlamak."
    ),
    "geo_fusion_core.py": (
        "Hoodmaps, Endeksa, GeoSpy entegrasyon özetini e-ticaret operasyonuyla harmanlayan motor. "
        "geo_fusion_master_report.json'un tek yazıcısı. Nedeni: belgedeki 'il bazlı enflasyon katsayısı "
        "ve yerel ticaret' anlatısının coğrafi istihbarat katmanına bağlanması."
    ),
    "uteykder_veri_arsiv_ajani.py": (
        "Word belgesinin ikinci sohbetinin açılış konusu. UTEYKDER fahri üye kimlik/ikamet/telefon/"
        "vesikalık bilgilerini DERBİS uyumlu Ad_Soyad_TC klasörlerinde, uteykder_uye_arsivi.json ve "
        "UTYKDER_DERBIS_FAHRI_UYE_LISTESI.xlsx ile arşivler. Windsurf entegrasyonu sonrası 'sadece "
        "bunu yedekleyeyim' denerek ayrı tutulmuş; app.py'ye DERBİS sekmesi olarak bağlanması "
        "belgede tarif edilir. Nedeni: dernek resmi kaydını otonom sisteme taşımak."
    ),
    "anac_denetci_ajani.py": (
        "Belgede 'anaç ruhu ile konuşan 40-50 yaş asistan' olarak tarif edilir. Sisteme girmek "
        "isteyen kişinin gerçekten yalnız hayatını normal standartlarda sürdürmek isteyip "
        "istemediğini, takıntılı bilgi kırıntısı olup olmadığını sorgular; onaylamazsa kabul etmez. "
        "Nedeni: Sosyal İmece üye havuzuna niyet süzgeci koymak."
    ),
    "cerez_yoneticisi.py": (
        "Belgede Trae önbellek krizinde 'elinle yerleştirdiğin güncel dosyalar' arasında sayılır. "
        "E-ticaret sitelerindeki oturum çerezlerini yönetmek için yazılmıştır. Nedeni: Amazon vb. "
        "kaynaklardan ürün/fiyat çekiminde oturumun düşmemesi."
    ),
    "sesli_komut.py": (
        "Belgede Trae'in eski sekmede win32com barındıran ilk hali olarak geçer; hoparlör ikonu "
        "kaybolunca sesli dinleme ihtiyacı anlatılır. Nedeni: komutları yazmadan sesle vermek."
    ),
    "ses_motoru.py": (
        "Kurtarıcı .bat ile yedekten ana klasöre çekilecek 4 kritik dosyadan biri. Nedeni: "
        "TTS/ses motorunu ajan komuta döngüsüne bağlamak."
    ),
    "dns_ayarla.py": (
        "Belgede Dns_ayarla.py olarak yedekten kurtarılacak dosya. Nedeni: yerel ağ/DNS ayarını "
        "otomasyon ortamına sabitlemek."
    ),
    "README.md": (
        "Hugging Face Spaces YAML ön yüzü: title Sosyal Imece, sdk streamlit, app_file app.py. "
        "Nedeni: Spaces'in hangi dosyayı çalıştıracağını ve temayı okuması."
    ),
    "Procfile": (
        "PaaS süreç tanımı: web: python MASTER_CONTROLLER.py. Nedeni: Render/Heroku'nun web "
        "sürecini başlatması (Streamlit ayrı render.yaml startCommand ile app.py çalıştırır)."
    ),
    "render.yaml": (
        "Render ücretsiz katman: pip install -r requirements.txt, streamlit run app.py. "
        "Nedeni: bulut yayını tek dosyadan tanımlamak."
    ),
    "railway.toml": (
        "Railway yayını için TOML yapılandırma. Nedeni: alternatif PaaS hedefi."
    ),
    "Dockerfile": (
        "Konteyner imajı. Nedeni: Docker Desktop ile aynı ortamın taşınması."
    ),
}


def skip_dir(path: Path) -> bool:
    parts = set(path.parts)
    if parts & SKIP_DIR_NAMES:
        return True
    s = str(path)
    if "site-packages" in s or "\\venv\\" in s or "\\.venv\\" in s:
        return True
    return False


def extract_docstring(py_path: Path) -> str:
    try:
        src = py_path.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return ""
    if len(src) > 200_000:
        src = src[:200_000]
    try:
        tree = ast.parse(src)
        d = ast.get_docstring(tree)
        if d:
            return " ".join(d.split())[:420]
    except Exception:
        pass
    lines = []
    for line in src.splitlines()[:40]:
        t = line.strip()
        if t.startswith("#") and "coding" not in t:
            lines.append(t.lstrip("# ").strip())
        elif t.startswith('"""') or t.startswith("'''"):
            continue
        elif t and not t.startswith("import") and not t.startswith("from "):
            if "class " in t or "def " in t:
                lines.append(t[:120])
                break
    return " ".join(lines)[:420]


def infer_story(rel: str, name: str, suffix: str, extra: str) -> str:
    key = name
    if key in STORY_BY_NAME:
        return STORY_BY_NAME[key]
    if name.startswith("dynamic_agent_") and suffix == ".json":
        return (
            "Dinamik ajan çıktısı. trm_agents/dynamic_factory.py BaseDynamicAgent.execute_task "
            "tarafından reports/ altına yazılır. Gerçek ajan sınıfları 1–22 bandında kodda durur; "
            "23–200 numaraları 200'lük hedefi doldurmak için üretilen iskelet ajanların özet "
            "metrikleridir (kategori döngüsü: Lojistik, Bölgesel Kalkınma, Dijital Pazarlama, "
            "Veri Doğrulama, Denetim Destek). app.py 3. sekme bu dosyaları listeler. Nedeni: "
            "her ajan slotunun çalıştığına dair iz bırakmak ve komuta merkezinde seçilebilir rapor sunmak."
        )
    low = (rel + " " + name).lower()
    bits = []
    if extra:
        bits.append("Kod/dosya özeti: " + extra)
    if suffix == ".py":
        if "agent" in low or "ajan" in low:
            bits.append(
                "Oluşum: Sosyal İmece / TRM Nirvana ajan mimarisinde belirli bir görevi (güvenlik, "
                "içerik, finans, denetim, sosyal medya veya lojistik) otonom yürütsün diye yazıldı."
            )
        elif "test" in low:
            bits.append("Oluşum: bir modülün doğru çalıştığını doğrulamak için test betiği olarak eklendi.")
        elif "panel" in low or "dashboard" in low or "streamlit" in low:
            bits.append("Oluşum: görsel yönetim/denetim paneli ihtiyacından türedi; app.py öncesi veya paralel arayüz denemesi.")
        elif "scraper" in low or "bot" in low:
            bits.append("Oluşum: e-ticaret/sosyal platformlardan veri veya etkileşim çekmek için.")
        else:
            bits.append(
                "Oluşum: proje büyüdükçe (Haziran–Eylül 2026) Trae/Windsurf/Gemini sohbetleriyle "
                "eklenen Python modülü; ajan, yedek, panol veya entegrasyon ihtiyacına cevap verir."
            )
        bits.append("Nedeni: ilgili işi tekrar kullanılabilir kod olarak ayırmak.")
    elif suffix == ".txt":
        bits.append(
            "Oluşum: yapılandırma, kılavuz, log özeti veya düz metin bağımlılık/not dosyası. "
            "Nedeni: koddan ayrı okunabilir belge tutmak veya PaaS/araçların düz metin beklemesi."
        )
    elif suffix == ".json":
        bits.append(
            "Oluşum: çalışma zamanı veri/rapor deposu. Ajanlar ve paneller JSON okuyup yazar. "
            "Nedeni: durumun, arşivin veya analizin insan ve makine tarafından paylaşılması."
        )
    elif suffix == ".gitignore" or name == ".gitignore":
        bits.append(STORY_BY_NAME[".gitignore"])
    else:
        bits.append("Oluşum ve neden: uzantı ve konumdan proje yapı taşı olarak tutulmaktadır.")
    return " ".join(bits)


def collect():
    rows = []
    for dirpath, dirnames, filenames in os.walk(ROOT):
        p = Path(dirpath)
        if skip_dir(p):
            dirnames[:] = []
            continue
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIR_NAMES and "site-packages" not in d]
        for fn in filenames:
            fp = p / fn
            suf = fp.suffix.lower()
            if fn == ".gitignore" or suf in {".py", ".txt", ".json"}:
                rel = str(fp.relative_to(ROOT))
                try:
                    st = fp.stat()
                except OSError:
                    continue
                extra = extract_docstring(fp) if suf == ".py" else ""
                if suf == ".json" and fp.stat().st_size < 8000:
                    try:
                        data = json.loads(fp.read_text(encoding="utf-8", errors="replace"))
                        extra = "JSON anahtarları: " + ", ".join(list(data.keys())[:12]) if isinstance(data, dict) else "JSON dizi/değer"
                    except Exception:
                        extra = ""
                elif suf == ".txt":
                    try:
                        t = fp.read_text(encoding="utf-8", errors="replace")[:200]
                        extra = " ".join(t.split())[:200]
                    except Exception:
                        extra = ""
                rows.append({
                    "rel": rel.replace("/", "\\"),
                    "name": fn,
                    "suf": suf if suf else fn,
                    "size": st.st_size,
                    "mtime": datetime.fromtimestamp(st.st_mtime).strftime("%Y-%m-%d %H:%M"),
                    "story": infer_story(rel, fn, suf if suf else fn, extra),
                    "extra": extra,
                })
    rows.sort(key=lambda r: (r["suf"], r["rel"].lower()))
    return rows


def main():
    rows = collect()
    py = [r for r in rows if r["suf"] == ".py"]
    txt = [r for r in rows if r["suf"] == ".txt"]
    js = [r for r in rows if r["suf"] == ".json"]
    gi = [r for r in rows if r["name"] == ".gitignore"]
    dyn = [r for r in rows if r["name"].startswith("dynamic_agent_") and r["suf"] == ".json"]
    reports_json = [r for r in rows if r["rel"].startswith("reports\\") and r["suf"] == ".json"]

    lines = []
    a = lines.append
    a("=" * 92)
    a("SOSYAL İMECE — DOSYA ENVANTERİ, OLUŞTURULMA HİKÂYELERİ VE NEDENLERİ")
    a("Üretim tarihi: " + datetime.now().strftime("%Y-%m-%d %H:%M"))
    a("Kaynak 1: Word belgesi (Gemini sohbet arşivi)")
    a("Kaynak 2: C:\\Users\\Habitat\\Desktop\\sosyal_imece  (venv/site-packages/.git hariç)")
    a("=" * 92)
    a("")
    a("A) WORD BELGESİ NEDİR?")
    a("-" * 92)
    a("Dosya: 'Sosyal İmece ile İlgili Önemli Bölümleri  .doc'")
    a("Konum: C:\\Users\\Habitat\\Desktop\\Sosyal İmece ile İlgili Önemli Bölümleri\\")
    a("Boyut: ~1.09 MB  |  Son kayıt: 3.09.2026 23:07  |  Biçim: eski OLE .doc")
    a("")
    a("Bu Word dosyası tek parça bir teknik spesifikasyon değil; Gemini sohbetlerinin")
    a("birleştirilmiş 'önemli bölümler' arşividir. İçinde şu dönemler ve kararlar geçer:")
    a("")
    a("1) Trae IDE krizi (Temmuz 2026): Trae aniden kapatılınca eski sekmeler (sesli_komut.py")
    a("   win32com hali) cache'den açılır; 'Abnormally stopped' + Usage Limit Reached. Çözüm:")
    a("   güncel dosyaları Explorer'dan açmak, sohbeti sıfırlamak; kota dolunca Trae AI'sız")
    a("   kurtarici.bat ile yedekten 4 dosya çekmek: kuresel_imece_detayli_operasyon_rehberi.txt,")
    a("   Dns_ayarla.py, cerez_yoneticisi.py, ses_motoru.py. Klasör adı belgede KURESEL_IMECE_DUNYASI.")
    a("")
    a("2) Trae 'elim ayağım' kararı: Split Preview'da Workspace Kontrol Merkezi HTML paneli;")
    a("   Gemini'nin bir noktada 'bu isteğe yardımcı olamam' diye kesilmesi ve sohbetin yeni")
    a("   sayfaya devri.")
    a("")
    a("3) UTEYKDER / DERBİS: uteykder_veri_arsiv_ajani.py Windsurf ile entegre; 'sadece bunu")
    a("   yedekleyeyim' / 'hadi çalıştıralım' → streamlit run app.py ve DERBİS sekmesi.")
    a("")
    a("4) Kuşadası AK Parti binası görüşme metni: UTEYKDER toplantı yeri + Sosyal İmece'nin")
    a("   il bazlı enflasyon katsayısı, 55+ emekli 'imece zenginlik payı', Nazilli hemşehrilik.")
    a("")
    a("5) Anaç ruhlu niyet denetçisi: sisteme girişte gerçek ihtiyaç süzgeci; app.py'ye sekme.")
    a("")
    a("6) app.py komuta merkezi bloğu: belgede tam kod yedekleri (Veri Arşiv, Anaç Denetçi,")
    a("   entegre app.py) paylaşılır. Bugünkü app.py bu vizyonun sade TRM Nirvana v3.0 yüzüdür.")
    a("")
    a("7) GitHub / Streamlit Cloud: requirements.txt sürüm kilidi; git add requirements.txt;")
    a("   Cloud log'unda kuresel_imece_dunyasi/requirements.txt satır satır kurulur.")
    a("   reports/system_status.json belgede de geçer. .gitignore'u Nöbetçi ajanın *.py tarayıp")
    a("   yanlışlıkla syntax hatası sanması anlatılır (SISTEM_ENVANTERI.py).")
    a("")
    a("Özet bağ: Word = niyet, hikâye ve operasyon kararları. sosyal_imece = bu kararların")
    a("kod, config ve çalışma zamanı raporlarına dökülmüş hali.")
    a("")
    a("B) SAYILAR (venv / .git / site-packages hariç)")
    a("-" * 92)
    a(f"  .py     : {len(py)}")
    a(f"  .txt    : {len(txt)}")
    a(f"  .json   : {len(js)}   (reports/ altında {len(reports_json)}; dynamic_agent_* = {len(dyn)})")
    a(f"  .gitignore: {len(gi)}")
    a(f"  TOPLAM listelenen: {len(rows)}")
    a("")
    a("Hariç tutulanlar (neden): Python sanal ortamı, Git nesneleri, pip paketleri ve cache.")
    a("Bunlar proje hikâyesi değil, araç zincirinin kopyalarıdır.")
    a("")
    a("C) KULLANICININ ÖZEL OLARAK ADLANDIRDIĞI ÇEKİRDEK DOSYALAR")
    a("-" * 92)

    core_order = [
        ("app.py", "Python — Ana Streamlit arayüzü ve komuta merkezi"),
        ("behavioral_marketing_agent.py", "Python — Davranışsal pazarlama ve sosyal dağıtım ajanı"),
        ("requirements.txt", "TXT — Python paket bağımlılıkları"),
        ("runtime.txt", "TXT — Python sürüm sabitleme (3.11)"),
        (".gitignore", "Git hariç tutma"),
        ("reports\\system_status.json", "JSON — Sistem sağlık ve durum raporu"),
        ("reports\\geo_fusion_master_report.json", "JSON — Coğrafi füzyon ve e-ticaret analizi"),
    ]
    by_rel = {r["rel"]: r for r in rows}
    by_name = {}
    for r in rows:
        by_name.setdefault(r["name"], r)

    for key, label in core_order:
        r = by_rel.get(key) or by_name.get(key.split("\\")[-1])
        a("")
        a(f">>> {label}")
        if r:
            a(f"    Tam ad / yol : {r['rel']}")
            a(f"    Boyut / tarih: {r['size']} bayt  |  {r['mtime']}")
            a(f"    Hikâye/neden : {r['story']}")
        else:
            a(f"    (Beklenen yol: {key} — taramada bulunamadı)")

    a("")
    a(">>> dynamic_agent_*.json (Dinamik ajan çıktısı — tek hikâye, tam isim listesi aşağıda)")
    a("    Üretici: trm_agents\\dynamic_factory.py  |  Okuyan: app.py 3. sekme")
    a(f"    Adet: {len(dyn)}")
    a("    Hikâye/neden: " + STORY_BY_NAME["dynamic_factory.py"])
    a("")
    a("D) YAPILAR (UZANTILAR NE İŞE YARAR?)")
    a("-" * 92)
    a("  .py   Python kaynak. Ajan sınıfları, paneller, orkestratör, test, kazıyıcı, köprü.")
    a("  .txt  Bağımlılık (requirements), runtime, kılavuz, düz metin not, bazı yanlışlıkla")
    a("        .py olması gereken metinler (belgede requirements.py uyarısı).")
    a("  .json Çalışma verisi ve rapor. reports/ çalışma anında üretilir; kökteki json'lar")
    a("        arşiv, kuyruk, üye, sözleşme, sağlık, yapılandırma.")
    a("  .gitignore  Git'e gitmeyecek yollar (sırlar, medya, zip).")
    a("  İlişkili ama bu listede uzantı filtresi dışı: .md kılavuz, .bat başlatıcı, .html panel,")
    a("  .xlsx DERBİS listeleri, .yml/.yaml/.toml yayın, Dockerfile, Procfile, .db SQLite.")
    a("")
    a("E) TAM LİSTE — HER DOSYA: AD, TARİH, BOYUT, HİKÂYE VE NEDEN")
    a("-" * 92)

    current = None
    for r in rows:
        if r["suf"] != current:
            current = r["suf"]
            a("")
            a("")
            a("#" * 92)
            a(f"# GRUP: {current}   ({sum(1 for x in rows if x['suf']==current)} dosya)")
            a("#" * 92)
        a("")
        a(f"AD: {r['name']}")
        a(f"TAM YOL: sosyal_imece\\{r['rel']}")
        a(f"UZANTI: {r['suf']}  |  BOYUT: {r['size']} bayt  |  SON YAZIM: {r['mtime']}")
        if r["extra"]:
            a(f"İLK İZ / ÖZET: {r['extra']}")
        a(f"OLUŞTURULMA HİKÂYESİ VE NEDENİ: {r['story']}")
        a("-")

    a("")
    a("=" * 92)
    a("SON")
    a("Bu metin Word arşivi + disk taraması + app.py / MASTER_CONTROLLER / dynamic_factory /")
    a("geo_fusion_core kaynak okumasıyla 4 Eylül 2026'da üretilmiştir.")
    a("=" * 92)

    OUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"OK {OUT} bytes={OUT.stat().st_size} files={len(rows)}")


if __name__ == "__main__":
    main()
