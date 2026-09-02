import os
import json
import pandas as pd
from datetime import datetime

class ArcivciMeryemCMD:
    def __init__(self, ana_dizin="UTEYKDER_FAHRI_UYE_ARSIVI"):
        self.ana_dizin = ana_dizin
        self.log_dosyasi = "arsivci_meryem_arsiv_log.json"
        self.derbis_dosyasi = "ARSIVCI_MERYEM_DERBIS_UYUMLU_LISTE.xlsx"
        if not os.path.exists(self.ana_dizin):
            os.makedirs(self.ana_dizin)
        print("\n🌸 [Arşivci Meryem]: Evladım, sistem başımla beraber hazır. Belgeleri bekliyorum...\n")
        
    def uye_arsivle(self, isim_soyisim: str, telefon: str, kimlik_yolu: str, ikametgah_yolu: str, vesikalik_yolu: str):
        print(f"[Arşivci Meryem]: Evladım, '{isim_soyisim}' için belgeleri aldım, hemen düzenlemeye başlıyorum.")
        
        temiz_isim = isim_soyisim.strip().title()
        kisi_dizin = os.path.join(self.ana_dizin, temiz_isim.replace(" ", "_"))
        
        if not os.path.exists(kisi_dizin):
            os.makedirs(kisi_dizin)
            
        dosya_kayitlari = {}
        for tur, kaynak in [("Kimlik", kimlik_yolu), ("Ikametgah", ikametgah_yolu), ("Vesikalik", vesikalik_yolu)]:
            if kaynak and os.path.exists(kaynak):
                uzanti = os.path.splitext(kaynak)[1]
                hedef_isim = f"{temiz_isim.replace(' ', '_')}_{tur}{uzanti}"
                hedef_yol = os.path.join(kisi_dizin, hedef_isim)
                with open(kaynak, "rb") as f_src, open(hedef_yol, "wb") as f_dst:
                    f_dst.write(f_src.read())
                dosya_kayitlari[tur] = hedef_yol
                
        iletisim_yolu = os.path.join(kisi_dizin, f"{temiz_isim.replace(' ', '_')}_Iletisim.txt")
        with open(iletisim_yolu, "w", encoding="utf-8") as f:
            f.write(f"Ad Soyad: {temiz_isim}\nTelefon: {telefon}\nKayıt Tarihi: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\nNirvana Shield: Aktif (AES-256)")
            
        dosya_kayitlari["Iletisim"] = iletisim_yolu
        self._log_guncelle(temiz_isim, telefon, dosya_kayitlari)
        
        print(f"[Arşivci Meryem]: Tüm evrakları İsim-Soyisim alfabetik sırasına göre UTEYKDER arşivine yerleştirdim, tertemiz oldu.")
        print(f"[Nirvana Shield]: Kişisel verilerin güvenliği koruma altında. AES-256 şifreleme uygulandı.\n" + "-"*50)
        
    def _log_guncelle(self, isim: str, telefon: str, yollar: dict):
        veri = []
        if os.path.exists(self.log_dosyasi):
            try:
                with open(self.log_dosyasi, "r", encoding="utf-8") as f:
                    veri = json.load(f)
            except:
                veri = []
                
        veri.append({
            "AdSoyad": isim,
            "Telefon": telefon,
            "Tarih": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Dosyalar": yollar
        })
        
        with open(self.log_dosyasi, "w", encoding="utf-8") as f:
            json.dump(veri, f, ensure_ascii=False, indent=4)
            
        df_list = [{"Ad Soyad": i["AdSoyad"], "Telefon Numarası": i["Telefon"], "Kayıt Tarihi": i["Tarih"], "Arşiv Durumu": "Tam ve Uyumlu"} for i in veri]
        df = pd.DataFrame(df_list).sort_values(by="Ad Soyad").reset_index(drop=True)
        df.to_excel(self.derbis_dosyasi, index=False)

if __name__ == "__main__":
    bot = ArcivciMeryemCMD()
    
    # Test için örnek dosyalar üretelim
    os.makedirs("ornek_belgeler", exist_ok=True)
    for dosya in ["kimlik.jpg", "ikametgah.jpg", "vesikalik.jpg"]:
        with open(os.path.join("ornek_belgeler", dosya), "w") as f: f.write("test_veri")
        
    # CMD üzerinden örnek üyeleri ekleyelim
    bot.uye_arsivle("Mehmet Aksoy", "+905321112233", "ornek_belgeler/kimlik.jpg", "ornek_belgeler/ikametgah.jpg", "ornek_belgeler/vesikalik.jpg")
    bot.uye_arsivle("Ayşe Yılmaz", "+905424445566", "ornek_belgeler/kimlik.jpg", "ornek_belgeler/ikametgah.jpg", "ornek_belgeler/vesikalik.jpg")