from datetime import datetime
from pathlib import Path

OUT = Path(r"c:\Users\Habitat\Desktop\SOSYAL İMECE_200_AJAN_NIHAI_DOKUMAN_TAM_TURKCE.txt")
LINE = "=" * 78


def add(buf, text=""):
    buf.append(text)


def main():
    now = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
    lines = []

    add(lines, LINE)
    add(lines, "SOSYAL İMECE")
    add(lines, "200 YAPAY ZEKA AJANLI SISTEM")
    add(lines, "NIHAI BILGILENDIRME DOKUMANI")
    add(lines, LINE)
    add(lines)
    add(lines, "Dokuman Turu : Profesyonel Nihai Surum")
    add(lines, f"Hazirlanma   : {now}")
    add(lines, "Dil          : Tam Turkce karakterli")
    add(lines, "Kapsam       : 200 ajanlik mimari, gorev alanlari ve calisma duzeni")
    add(lines)
    add(lines, "KAPAK NOTU")
    add(lines, "Bu dokuman, SOSYAL İMECE projesindeki 200 ajanlik operasyon")
    add(lines, "modelini daha profesyonel, daha okunakli ve Turkce karakterleri korunmus")
    add(lines, "nihai formatta aciklamak icin hazirlanmistir.")
    add(lines)
    add(lines, "ONEMLI ACIKLAMA")
    add(lines, "Bu sistemde '200 ajan' ifadesi, iki katmandan olusan operasyonel mimariyi")
    add(lines, "ifade eder:")
    add(lines, "1. 165 ajanlik temel operasyon havuzu")
    add(lines, "2. Kod tabaninda acik tanimli 35 genisleme ajani")
    add(lines)
    add(lines, "Baska bir deyisle, projede 200 ayri sinif dosyasi bulunmasi zorunlu degildir.")
    add(lines, "Mimari; gorev havuzlari, uzman ajanlar, cekirdek orkestrasyon ve genisleme")
    add(lines, "modulleri birlikte calisacak sekilde tasarlanmistir.")
    add(lines)

    add(lines, LINE)
    add(lines, "1. YONETICI OZETI")
    add(lines, LINE)
    add(lines, "Sistem genel olarak su zincirle calisir:")
    for item in [
        "Veri toplar",
        "Veriyi analiz eder",
        "Icerige donusturur",
        "Yayin kuyruguna alir",
        "Planli paylasim yapar",
        "Performansi ve guvenligi izler",
        "Saglik raporu ve durum ozeti uretir",
    ]:
        add(lines, f"- {item}")
    add(lines)
    add(lines, "Bu zincirin merkezi beyni CoreNexus'tur. CoreNexus; ajanlari baglar,")
    add(lines, "baglami yonetir, Zero-Trust denetimi uygular ve ajan ciktilarinin")
    add(lines, "birbirine kontrollu bicimde aktarilmasini saglar.")
    add(lines)

    add(lines, LINE)
    add(lines, "2. 165 AJANLIK TEMEL OPERASYON HAVUZU")
    add(lines, LINE)
    add(lines, "Asagidaki yapi, 001-165 arasindaki temel ajan kapasitesini temsil eder.")
    add(lines, "Bu bolumde bircok ajan ayni gorevi paylasan operasyon slotlari seklinde")
    add(lines, "tasarlanmistir. Bu nedenle profesyonel surumde tekrara dusmeden grup")
    add(lines, "mantigiyla aciklama yapilmistir.")
    add(lines)

    base_groups = [
        ("Ajan 001-020", "Veri Toplama Ajanlari", "Dis kaynaklardan urun, kampanya, baglanti ve trend verisi toplar.", "Web, kanal, liste ve urun akislarini izler; veriyi temizleyip cekirdege aktarir."),
        ("Ajan 021-040", "Trend ve Analiz Ajanlari", "Toplanan verileri puanlar, siralar ve firsatlari belirler.", "Baslik, ilgi duzeyi, fiyat, potansiyel donusum ve trend skoru uzerinden oncelik uretir."),
        ("Ajan 041-060", "Icerik Fabrikasi Ajanlari", "Trend raporlarini satis odakli iceriklere donusturur.", "Baslik, tanitim metni, sosyal medya kopyasi, cagri metni ve etiket uretir."),
        ("Ajan 061-080", "Kuyruk ve Yayin Ajanlari", "Icerigi zaman planina gore yayin sirasina alir.", "Gonderileri takvime isler, platform bazli siraya koyar ve yayin sonucunu isler."),
        ("Ajan 081-100", "Maskeleme ve Guvenlik Ajanlari", "Daha kontrollu ve dusuk gorunurluklu calisma saglar.", "Oturum izi, davranis modeli, cihaz sinyali ve risk seviyesini yonetir."),
        ("Ajan 101-120", "Affiliate ve Ag Ajanlari", "Harici ortaklik aglarini ve teklif akislarini sisteme baglar.", "Katalog, teklif tazeligi, ag sagligi ve baglanti verilerini merkeze tasir."),
        ("Ajan 121-140", "Operasyon ve Saglik Ajanlari", "Sistemin kesintisiz calisma durumunu takip eder.", "Heartbeat, servis durumu, kuyruk sagligi, kurtarma akisi ve saglik ozeti uretir."),
        ("Ajan 141-155", "Finans ve Uyum Ajanlari", "Gelir, komisyon, odeme ve uyum sureclerini yonetir.", "Finansal ozet, odeme listesi, vergi hesabi ve raporlama ciktisi uretir."),
        ("Ajan 156-161", "Uyelik ve Denetim Ajanlari", "Yeni kullanici ve ortak adaylarini sisteme dahil eder.", "Basvuru alir, uygunluk sinyallerini degerlendirir ve destek akisini baslatir."),
    ]
    for kod, baslik, gorev, calisma in base_groups:
        add(lines, f"{kod} | {baslik}")
        add(lines, f"Gorev        : {gorev}")
        add(lines, f"Nasil calisir: {calisma}")
        add(lines)

    for kod, ad, gorev, calisma in [
        ("Ajan 162", "TRMGlobalAffiliateRecruiterAgent", "Kuresel affiliate ortaklarini ve uluslararasi is birliklerini sisteme kazandirir.", "Hedef pazarlari tarar, aday ortak listesi olusturur, tanitim mesaji hazirlar ve partner verisini gunceller."),
        ("Ajan 163", "TRMHumanAuditorAgent", "Adaylarin samimiyetini, motivasyonunu ve sistem uyumunu degerlendirir.", "Soru seti uretir, yanitlari analiz eder ve denetim kaydi olusturur."),
        ("Ajan 164", "TRMLocalRecruiterAgent", "Turkiye icindeki KOBI, esnaf ve yerli ureticileri sisteme dahil eder.", "Sehir bazli tarama yapar, tanitim metni hazirlar ve yerel partner kaydi acar."),
        ("Ajan 165", "TRMAccountingAgent", "Gelir, vergi, stopaj, odeme ve destek butcelerini hesaplar.", "Komisyon ve gelir verilerini isleyerek net kar, odeme listesi ve dagitim ozeti uretir."),
    ]:
        add(lines, f"{kod} | {ad}")
        add(lines, f"Gorev        : {gorev}")
        add(lines, f"Nasil calisir: {calisma}")
        add(lines)

    add(lines, LINE)
    add(lines, "3. KODDA ACIK TANIMLI 35 GENISLEME AJANI")
    add(lines, LINE)
    add(lines, "Bu ajanlar sistemde acik bicimde olusturulur ve CoreNexus uzerinden")
    add(lines, "senkronize edilir. Uc ana aileden olusurlar:")
    for item in ["10 MarketIntelAgent", "15 BridgeAgent", "10 SentinelAgent"]:
        add(lines, f"- {item}")
    add(lines)

    for i, region in enumerate(["TR", "EU", "US", "MENA", "UK", "DE", "FR", "NL", "GCC", "CEE"], 1):
        add(lines, f"MarketIntelAgent_{i:02d} | Bolge: {region}")
        add(lines, "Gorev        : Bolgesel fiyat, stok baskisi ve satis stratejisi sinyali uretir.")
        add(lines, "Nasil calisir: Trend raporundaki urun detaylarini okuyup rekabet kirilimi, oncelik seviyesi ve icerik yonu belirler.")
        add(lines)

    for i, name in enumerate([
        "AmazonEU", "AmazonUS", "Awin", "CJ", "Impact", "Rakuten", "TradeTracker",
        "ShareASale", "Partnerize", "Webgains", "ClickBank", "Admitad",
        "Tradedoubler", "FlexOffers", "Pepperjam",
    ], 1):
        add(lines, f"BridgeAgent_{i:02d} | Ag: {name}")
        add(lines, "Gorev        : Affiliate agindan teklif, katalog ve senkron saglik verisi tasir.")
        add(lines, "Nasil calisir: Trend baglamini okur; teklif sayisi, ag tazeligi, katalog buyuklugu ve onerilen senkron modunu uretir.")
        add(lines)

    for i, area in enumerate(["Gateway", "API", "Queue", "Worker", "Health", "Identity", "ZeroTrust", "Network", "Content", "Publishing"], 1):
        add(lines, f"SentinelAgent_{i:02d} | Alan: {area}")
        add(lines, "Gorev        : Anomali, retry baskisi ve guvenlik riskini izler.")
        add(lines, "Nasil calisir: Kuyruk, paylasim ve guvenlik durumunu okuyup uyari seviyesi belirler; ciktiyi HealthCheckAgent'a tasir.")
        add(lines)

    add(lines, LINE)
    add(lines, "4. CEKIRDEKTE DOGRUDAN CALISAN TEMEL AJANLAR")
    add(lines, LINE)
    for name, gorev, calisma in [
        ("CoreNexus", "Tum ajanlari baglayan merkez orkestrasyon cekirdegidir.", "Ajanlari kaydeder, baglami paylastirir, Zero-Trust filtresi uygular ve sonuclari ortak yapiya geri yazar."),
        ("CamouflageAgent", "Dil ve oturum maskelemesi yapar.", "Terimleri donusturur, maskeleme moduna gore iz uretir ve koruyucu katman saglar."),
        ("AccountManagerAgent", "Operator kimligi ve kurumsal e-posta uretir.", "Ulke koduna gore rumuz olusturur ve hesap bilgisini yapilandirir."),
        ("AnalystAgent", "Urun havuzunu trend skoruna gore analiz eder.", "Metin, ilgi ve firsat sinyallerini puanlayarak trend raporu cikarir."),
        ("ContentGeneratorAgent", "Trend ve komisyon bilgisini satis kopyasina donusturur.", "Baslik, satis metni, sosyal gonderi ve CTA uretir; istihbarat sinyallerini tona isler."),
        ("QueueAgent", "Uretilen icerikleri yayin kuyruguna aktarir.", "Icerik paketini okuyup 30 dakikalik planla siraya dizer."),
        ("PosterAgent", "Zamani gelen postlari platformlara gonderir.", "Kuyruktaki kaydi isler; sonucu posted veya pending_retry olarak isaretler."),
        ("HealthCheckAgent", "Sistemin genel saglik ozetini cikarir.", "Internet, API, kuyruk, Sentinel ve guvenlik durumunu birlestirir."),
        ("StatsAgent", "Panel icin canli metrik uretir.", "Aktif kullanici, havuz ve paylasim sayilari gibi ozet olcumleri hesaplar."),
        ("SocialUploaderAgent", "Sosyal medya yukleme hazirligini yonetir.", "Platform secimi, API uygunlugu ve yukleme akisina rehberlik eder veya sureci simule eder."),
    ]:
        add(lines, name)
        add(lines, f"Gorev        : {gorev}")
        add(lines, f"Nasil calisir: {calisma}")
        add(lines)

    add(lines, LINE)
    add(lines, "5. KOD TABANINDA GORULEN EK VE ESKI NESIL AJANLAR")
    add(lines, LINE)
    for name, desc in [
        ("MobileGatewayAgent", "Mobil onay akisi ve sanal mobil ortam hazirligi saglar."),
        ("CyberGuardianAgent", "Yetkisiz giris ve butunluk ihlallerine karsi savunma taramasi yapar."),
        ("Agent168_LegalTax", "Uluslararasi vergi ve fatura uyumunu temsil eder."),
        ("Agent169_MFABridge", "SMS ve cok faktorlu dogrulama koprusu islevi gorur."),
        ("Agent170_AlgorithmShield", "Iade ve sikayet baskisinda magaza koruma aksiyonlari tanimlar."),
        ("Agent171_PayoutDistribution", "Odeme dagitimi ve transfer emri mantigini temsil eder."),
        ("Agent172_PolicyCopyrightFilter", "Telif ve platform politika taramasi yapar."),
        ("BrowserSpooferAgent", "Tarayici parmak izi cesitlendirir."),
        ("HumanizerAgent", "Davranisi daha insan benzeri gecikme ve yazim akisiyla yumusatir."),
        ("SentimentTrendAgent", "Viral egilimleri tarar ve vitrin yonu onerir."),
        ("Legacy SentinelAgent", "Etkilesim dususu ve benzeri riskleri karantina mantigiyla izler."),
    ]:
        add(lines, f"- {name}: {desc}")
    add(lines)

    add(lines, LINE)
    add(lines, "6. SISTEMIN CALISMA AKISI")
    add(lines, LINE)
    for step in [
        "1. Veri kaynaklarindan urun ve trend sinyalleri toplanir.",
        "2. AnalystAgent ve ilgili analiz katmani firsatlari puanlar.",
        "3. MarketIntelAgent ailesi fiyat ve rekabet zekasi ekler.",
        "4. ContentGeneratorAgent satis odakli icerik uretir.",
        "5. QueueAgent icerikleri zaman planina yerlestirir.",
        "6. PosterAgent zamani gelen gonderileri yayinlar.",
        "7. BridgeAgent ailesi ag ve teklif sagligini gunceller.",
        "8. SentinelAgent ailesi risk ve anomali denetimi yapar.",
        "9. HealthCheckAgent tum zincirin saglik raporunu uretir.",
        "10. Streamlit paneli ve worker dosyalari durumu gorunur kilar.",
    ]:
        add(lines, step)
    add(lines)

    add(lines, LINE)
    add(lines, "7. SONUC")
    add(lines, LINE)
    add(lines, "SOSYAL İMECE icindeki 200 ajanlik sistem, yalnizca cok sayida ajan")
    add(lines, "isminden olusan bir liste degil; veri toplama, analiz, icerik uretimi, yayin,")
    add(lines, "guvenlik, ag senkronizasyonu ve saglik izleme katmanlarinin birbirine bagli")
    add(lines, "calistigi tam bir operasyon mimarisidir.")
    add(lines)
    add(lines, "Bu nihai surum ozellikle su hedeflerle hazirlanmistir:")
    for goal in [
        "Turkce karakter bozulmalarini gidermek",
        "Tekrarli anlatimi azaltmak",
        "Daha profesyonel baslikli ve kapakli bir sunum vermek",
        "165 + 35 mimarisini net bicimde aciklamak",
        "Kodda gorulen gercek ajan yapisini okunakli sekilde ozetlemek",
    ]:
        add(lines, f"- {goal}")
    add(lines)
    add(lines, "Dokuman sonu.")

    text = "\n".join(lines)
    replacements = {
        "KURESEL": "KÜRESEL",
        "IMECE": "İMECE",
        "DUNYASI": "DÜNYASI",
        "YAPAY ZEKA": "YAPAY ZEKA",
        "SISTEM": "SİSTEM",
        "NIHAI": "NİHAİ",
        "BILGILENDIRME": "BİLGİLENDİRME",
        "DOKUMANI": "DOKÜMANI",
        "Dokuman": "Doküman",
        "Turu": "Türü",
        "Surum": "Sürüm",
        "Hazirlanma": "Hazırlanma",
        "Turkce": "Türkçe",
        "gorev": "görev",
        "Gorev": "Görev",
        "Nasil": "Nasıl",
        "calisir": "çalışır",
        "calisma": "çalışma",
        "duzeni": "düzeni",
        "korunmus": "korunmuş",
        "aciklamak": "açıklamak",
        "hazirlanmistir": "hazırlanmıştır",
        "ONEMLI ACIKLAMA": "ÖNEMLİ AÇIKLAMA",
        "katmandan olusan": "katmandan oluşan",
        "genisleme ajani": "genişleme ajanı",
        "Baska": "Başka",
        "deyisle": "deyişle",
        "ayri": "ayrı",
        "sinif": "sınıf",
        "bulunmasi": "bulunması",
        "zorunlu degildir": "zorunlu değildir",
        "gorev havuzlari": "görev havuzları",
        "cekirdek": "çekirdek",
        "modulleri": "modülleri",
        "calisacak": "çalışacak",
        "sekilde": "şekilde",
        "tasarlanmistir": "tasarlanmıştır",
        "YONETICI OZETI": "YÖNETİCİ ÖZETİ",
        "su zincirle calisir": "şu zincirle çalışır",
        "Icerige": "İçeriğe",
        "donusturur": "dönüştürür",
        "kuyruguna": "kuyruğuna",
        "Planli": "Planlı",
        "guvenligi": "güvenliği",
        "Saglik": "Sağlık",
        "ozeti": "özeti",
        "uretir": "üretir",
        "ajarlari": "ajanları",
        "baglar": "bağlar",
        "baglami": "bağlamı",
        "yonetir": "yönetir",
        "ciktilarinin": "çıktılarının",
        "birbirine kontrollu bicimde aktarilmasini saglar": "birbirine kontrollü biçimde aktarılmasını sağlar",
        "TEMEL OPERASYON HAVUZU": "TEMEL OPERASYON HAVUZU",
        "Asagidaki yapi": "Aşağıdaki yapı",
        "arasindaki": "arasındaki",
        "kapasitesini": "kapasitesini",
        "temsil eder": "temsil eder",
        "bolumde": "bölümde",
        "bircok": "birçok",
        "ayni": "aynı",
        "seklinde": "şeklinde",
        "tekrara dusmeden": "tekrara düşmeden",
        "mantigiyla": "mantığıyla",
        "yapilmistir": "yapılmıştır",
        "Ajanlari": "Ajanları",
        "Dis": "Dış",
        "urun": "ürün",
        "baglanti": "bağlantı",
        "Toplanan": "Toplanan",
        "siralar": "sıralar",
        "firsatlari": "fırsatları",
        "belirler": "belirler",
        "Baslik": "Başlık",
        "duzeyi": "düzeyi",
        "potansiyel donusum": "potansiyel dönüşüm",
        "uzerinden": "üzerinden",
        "oncelik": "öncelik",
        "Fabrikasi": "Fabrikası",
        "satis": "satış",
        "donusturur": "dönüştürür",
        "tanitim": "tanıtım",
        "cagri": "çağrı",
        "Icerigi": "İçeriği",
        "gore": "göre",
        "sirasina": "sırasına",
        "Gonderileri": "Gönderileri",
        "isler": "işler",
        "bazli": "bazlı",
        "Maskeleme ve Guvenlik": "Maskeleme ve Güvenlik",
        "kontrollu": "kontrollü",
        "dusuk gorunurluklu": "düşük görünürlüklü",
        "Oturum izi, davranis modeli, cihaz sinyali ve risk seviyesini yonetir.": "Oturum izi, davranış modeli, cihaz sinyali ve risk seviyesini yönetir.",
        "Ag": "Ağ",
        "ortaklik": "ortaklık",
        "akislarini": "akışlarını",
        "baglar": "bağlar",
        "tazeligi": "tazeliği",
        "Operasyon ve Saglik": "Operasyon ve Sağlık",
        "kesintisiz calisma": "kesintisiz çalışma",
        "durumunu takip eder": "durumunu takip eder",
        "kuyruk sagligi": "kuyruk sağlığı",
        "ozeti": "özeti",
        "Finans ve Uyum": "Finans ve Uyum",
        "odeme": "ödeme",
        "sureclerini": "süreçlerini",
        "Finansal ozet": "Finansal özet",
        "vergi hesabi": "vergi hesabı",
        "raporlama ciktisi": "raporlama çıktısı",
        "Uyelik": "Üyelik",
        "adaylarini": "adaylarını",
        "Basvuru": "Başvuru",
        "degerlendirir": "değerlendirir",
        "Kuresel": "Küresel",
        "uluslararasi": "uluslararası",
        "birliklerini": "birliklerini",
        "kazandirir": "kazandırır",
        "pazarlari": "pazarları",
        "olusturur": "oluşturur",
        "mesaji": "mesajı",
        "gunceller": "günceller",
        "Adaylarin": "Adayların",
        "samimiyetini": "samimiyetini",
        "uyumunu": "uyumunu",
        "Soru seti uretir, yanitlari analiz eder ve denetim kaydi olusturur.": "Soru seti üretir, yanıtları analiz eder ve denetim kaydı oluşturur.",
        "Turkiye": "Türkiye",
        "icindeki": "içindeki",
        "KOBI": "KOBİ",
        "yerli ureticileri": "yerli üreticileri",
        "Sehir": "Şehir",
        "hazirlar": "hazırlar",
        "acar": "açar",
        "stopaj": "stopaj",
        "butcelerini": "bütçelerini",
        "isleyerek": "işleyerek",
        "kar": "kâr",
        "dagitim": "dağıtım",
        "KODDA ACIK TANIMLI 35 GENISLEME AJANI": "KODDA AÇIK TANIMLI 35 GENİŞLEME AJANI",
        "acik bicimde": "açık biçimde",
        "olusturulur": "oluşturulur",
        "uzerinden": "üzerinden",
        "senkronize edilir": "senkronize edilir",
        "Uc": "Üç",
        "aileden olusurlar": "aileden oluşurlar",
        "Bolgesel": "Bölgesel",
        "stok baskisi": "stok baskısı",
        "detaylarini": "detaylarını",
        "rekabet kirilimi": "rekabet kırılımı",
        "icerik yonu": "içerik yönü",
        "Affiliate agindan teklif, katalog ve senkron saglik verisi tasir.": "Affiliate ağından teklif, katalog ve senkron sağlık verisi taşır.",
        "baglamini": "bağlamını",
        "sayisi": "sayısı",
        "buyuklugu": "büyüklüğü",
        "onerilen": "önerilen",
        "Alan": "Alan",
        "Anomali, retry baskisi ve guvenlik riskini izler.": "Anomali, retry baskısı ve güvenlik riskini izler.",
        "paylasim": "paylaşım",
        "uyari": "uyarı",
        "ciktiyi": "çıktıyı",
        "tasir": "taşır",
        "CEKIRDEKTE DOGRUDAN CALISAN TEMEL AJANLAR": "ÇEKİRDEKTE DOĞRUDAN ÇALIŞAN TEMEL AJANLAR",
        "Tum": "Tüm",
        "orkestrasyon cekirdegidir": "orkestrasyon çekirdeğidir",
        "paylastirir": "paylaştırır",
        "sonuclari": "sonuçları",
        "yapiya": "yapıya",
        "Dil ve oturum maskelemesi yapar.": "Dil ve oturum maskelemesi yapar.",
        "donusturur": "dönüştürür",
        "Operator": "Operatör",
        "Ulke": "Ülke",
        "rumuz olusturur": "rumuz oluşturur",
        "yapilandirir": "yapılandırır",
        "Urun": "Ürün",
        "firsat": "fırsat",
        "cikarir": "çıkarır",
        "komisyon bilgisini satis kopyasina donusturur": "komisyon bilgisini satış kopyasına dönüştürür",
        "sosyal gonderi": "sosyal gönderi",
        "istihbarat sinyallerini tona isler": "istihbarat sinyallerini tona işler",
        "Uretilen": "Üretilen",
        "kuyruguna": "kuyruğuna",
        "Icerik paketini okuyup 30 dakikalik planla siraya dizer.": "İçerik paketini okuyup 30 dakikalık planla sıraya dizer.",
        "Zamani": "Zamanı",
        "postlari": "postları",
        "gonderir": "gönderir",
        "kaydi": "kaydı",
        "isaretler": "işaretler",
        "saglik ozetini": "sağlık özetini",
        "Internet": "İnternet",
        "birlestirir": "birleştirir",
        "icin canli": "için canlı",
        "kullanici": "kullanıcı",
        "sayilari": "sayıları",
        "olcumleri": "ölçümleri",
        "Sosyal medya yukleme hazirligini yonetir.": "Sosyal medya yükleme hazırlığını yönetir.",
        "secimi": "seçimi",
        "uygunlugu": "uygunluğu",
        "rehberlik eder": "rehberlik eder",
        "simule eder": "simüle eder",
        "GORULEN EK VE ESKI NESIL AJANLAR": "GÖRÜLEN EK VE ESKİ NESİL AJANLAR",
        "Mobil onay akisi ve sanal mobil ortam hazirligi saglar.": "Mobil onay akışı ve sanal mobil ortam hazırlığı sağlar.",
        "Yetkisiz giris ve butunluk ihlallerine karsi savunma taramasi yapar.": "Yetkisiz giriş ve bütünlük ihlallerine karşı savunma taraması yapar.",
        "cok faktorlu dogrulama koprusu islevi gorur.": "çok faktörlü doğrulama köprüsü işlevi görür.",
        "sikayet baskisinda magaza koruma aksiyonlari tanimlar.": "şikâyet baskısında mağaza koruma aksiyonları tanımlar.",
        "Odeme dagitimi ve transfer emri mantigini temsil eder.": "Ödeme dağıtımı ve transfer emri mantığını temsil eder.",
        "Telif ve platform politika taramasi yapar.": "Telif ve platform politika taraması yapar.",
        "Tarayici parmak izi cesitlendirir.": "Tarayıcı parmak izi çeşitlendirir.",
        "Davranisi daha insan benzeri gecikme ve yazim akisiyla yumusatir.": "Davranışı daha insan benzeri gecikme ve yazım akışıyla yumuşatır.",
        "Viral egilimleri tarar ve vitrin yonu onerir.": "Viral eğilimleri tarar ve vitrin yönü önerir.",
        "Etkilesim dususu ve benzeri riskleri karantina mantigiyla izler.": "Etkileşim düşüşü ve benzeri riskleri karantina mantığıyla izler.",
        "SISTEMIN CALISMA AKISI": "SİSTEMİN ÇALIŞMA AKIŞI",
        "kaynaklarindan": "kaynaklarından",
        "toplanir": "toplanır",
        "ilgili analiz katmani firsatlari puanlar.": "ilgili analiz katmanı fırsatları puanlar.",
        "fiyat ve rekabet zekasi ekler.": "fiyat ve rekabet zekâsı ekler.",
        "zamani": "zamanı",
        "gonderileri": "gönderileri",
        "ag ve teklif sagligini gunceller.": "ağ ve teklif sağlığını günceller.",
        "tum zincirin saglik raporunu uretir.": "tüm zincirin sağlık raporunu üretir.",
        "dosyalari durumu gorunur kilar.": "dosyaları durumu görünür kılar.",
        "SONUC": "SONUÇ",
        "yalnizca cok sayida ajan": "yalnızca çok sayıda ajan",
        "isminden olusan": "isminden oluşan",
        "degil; veri toplama, analiz, icerik uretimi, yayin,": "değil; veri toplama, analiz, içerik üretimi, yayın,",
        "guvenlik, ag senkronizasyonu ve saglik izleme katmanlarinin birbirine bagli": "güvenlik, ağ senkronizasyonu ve sağlık izleme katmanlarının birbirine bağlı",
        "calistigi": "çalıştığı",
        "ozellikle su hedeflerle hazirlanmistir": "özellikle şu hedeflerle hazırlanmıştır",
        "Turkce karakter bozulmalarini gidermek": "Türkçe karakter bozulmalarını gidermek",
        "Tekrarli anlatimi azaltmak": "Tekrarlı anlatımı azaltmak",
        "Daha profesyonel baslikli ve kapakli bir sunum vermek": "Daha profesyonel başlıklı ve kapaklı bir sunum vermek",
        "net bicimde aciklamak": "net biçimde açıklamak",
        "gorulen gercek ajan yapisini okunakli sekilde ozetlemek": "görülen gerçek ajan yapısını okunaklı şekilde özetlemek",
        "Dokuman sonu.": "Doküman sonu.",
    }
    for old, new in sorted(replacements.items(), key=lambda item: len(item[0]), reverse=True):
        text = text.replace(old, new)

    OUT.write_text(text, encoding="utf-8-sig")
    print(OUT)


if __name__ == "__main__":
    main()
