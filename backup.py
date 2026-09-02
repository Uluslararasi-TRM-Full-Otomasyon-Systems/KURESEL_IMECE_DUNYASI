import os
import shutil
import zipfile
from datetime import datetime
import glob

# ============================================
# YEDEKLEME SISTEMI
# TURKCE ACIKLAMALI
# ============================================

class BackupSystem:
    def __init__(self):
        """Yedekleme sistemini baslatir"""
        self.yedek_klasor = "yedekler"
        self.kaynak_dosyalar = [
            'team_list.csv',
            'sales.db',
            'secrets.env',
            'telegram_bot.py',
            'team_manager.py',
            'commission.py',
            'daily_report.py',
            'health_check.py'
        ]
        
        # Yedek klasoru yoksa olustur
        if not os.path.exists(self.yedek_klasor):
            os.makedirs(self.yedek_klasor)
            print(f"✅ Yedek klasoru olusturuldu: {self.yedek_klasor}")
    
    # ============================================
    # 1. TAM YEDEK AL
    # ============================================
    def tam_yedek_al(self):
        """Tum sistemin tam yedegini alir"""
        
        tarih = datetime.now().strftime("%Y%m%d_%H%M%S")
        yedek_adi = f"tam_yedek_{tarih}.zip"
        yedek_yolu = os.path.join(self.yedek_klasor, yedek_adi)
        
        print(f"\n📦 TAM YEDEK ALINIYOR: {yedek_adi}")
        print("="*60)
        
        with zipfile.ZipFile(yedek_yolu, 'w', zipfile.ZIP_DEFLATED) as zipf:
            # Python dosyalarini ekle
            for dosya in glob.glob("*.py"):
                zipf.write(dosya)
                print(f"   📄 {dosya} eklendi")
            
            # Veritabani dosyalarini ekle
            for dosya in ['sales.db', 'team_list.csv']:
                if os.path.exists(dosya):
                    zipf.write(dosya)
                    print(f"   🗄️ {dosya} eklendi")
            
            # .env dosyasini ekle
            if os.path.exists('secrets.env'):
                zipf.write('secrets.env')
                print(f"   🔐 secrets.env eklendi")
            
            # core klasorunu ekle
            if os.path.exists('core'):
                for root, dirs, files in os.walk('core'):
                    for file in files:
                        dosya_yolu = os.path.join(root, file)
                        zipf.write(dosya_yolu)
                print(f"   📁 core/ klasoru eklendi")
        
        # Dosya boyutunu hesapla
        boyut_mb = os.path.getsize(yedek_yolu) / (1024*1024)
        print("-"*60)
        print(f"✅ Tam yedek alindi: {yedek_adi} ({boyut_mb:.2f} MB)")
        
        return yedek_yolu
    
    # ============================================
    # 2. HIZLI YEDEK AL (SADECE ONEMLI DOSYALAR)
    # ============================================
    def hizli_yedek_al(self):
        """Sadece onemli dosyalarin yedegini alir"""
        
        tarih = datetime.now().strftime("%Y%m%d_%H%M%S")
        yedek_adi = f"hizli_yedek_{tarih}.zip"
        yedek_yolu = os.path.join(self.yedek_klasor, yedek_adi)
        
        print(f"\n⚡ HIZLI YEDEK ALINIYOR: {yedek_adi}")
        print("="*60)
        
        with zipfile.ZipFile(yedek_yolu, 'w', zipfile.ZIP_DEFLATED) as zipf:
            # Onemli dosyalari ekle
            for dosya in self.kaynak_dosyalar:
                if os.path.exists(dosya):
                    zipf.write(dosya)
                    print(f"   ✅ {dosya} eklendi")
        
        # Dosya boyutunu hesapla
        boyut_mb = os.path.getsize(yedek_yolu) / (1024*1024)
        print("-"*60)
        print(f"✅ Hizli yedek alindi: {yedek_adi} ({boyut_mb:.2f} MB)")
        
        return yedek_yolu
    
    # ============================================
    # 3. OTOMATIK YEDEKLEME (GUNLUK)
    # ============================================
    def otomatik_yedekle(self):
        """Her gun otomatik yedek alir (eski yedekleri temizler)"""
        
        tarih = datetime.now().strftime("%Y%m%d")
        yedek_adi = f"gunluk_yedek_{tarih}.zip"
        yedek_yolu = os.path.join(self.yedek_klasor, yedek_adi)
        
        # Bugun zaten yedek alinmis mi?
        if os.path.exists(yedek_yolu):
            print(f"⚠️ Bugun icin yedek zaten var: {yedek_adi}")
            return yedek_yolu
        
        print(f"\n📅 GUNLUK OTOMATIK YEDEK: {yedek_adi}")
        
        with zipfile.ZipFile(yedek_yolu, 'w', zipfile.ZIP_DEFLATED) as zipf:
            # Python dosyalarini ekle
            for dosya in glob.glob("*.py"):
                if os.path.exists(dosya):
                    zipf.write(dosya)
            
            # Veritabani dosyalarini ekle
            for dosya in ['sales.db', 'team_list.csv']:
                if os.path.exists(dosya):
                    zipf.write(dosya)
        
        print(f"✅ Gunluk yedek alindi: {yedek_adi}")
        
        # 30 gunden eski yedekleri temizle
        self.eski_yedekleri_temizle(30)
        
        return yedek_yolu
    
    # ============================================
    # 4. YEDEKLERI LISTELE
    # ============================================
    def yedekleri_listele(self):
        """Tum yedekleri listeler"""
        
        yedekler = glob.glob(os.path.join(self.yedek_klasor, "*.zip"))
        
        if not yedekler:
            print("\n📭 Henuz yedek bulunmuyor.")
            return
        
        print("\n" + "="*70)
        print("📋 MEVCUT YEDEKLER")
        print("="*70)
        
        # Tarihe gore sirala (yeniden eskiye)
        yedekler.sort(reverse=True)
        
        toplam_boyut = 0
        for yedek in yedekler[:20]:  # Son 20 yedegi goster
            ad = os.path.basename(yedek)
            boyut_mb = os.path.getsize(yedek) / (1024*1024)
            tarih = datetime.fromtimestamp(os.path.getmtime(yedek))
            print(f"📦 {ad}")
            print(f"   📅 {tarih.strftime('%d.%m.%Y %H:%M')} | 💾 {boyut_mb:.2f} MB")
            toplam_boyut += boyut_mb
        
        print("-"*70)
        print(f"📊 Toplam: {len(yedekler)} yedek, {toplam_boyut:.2f} MB")
    
    # ============================================
    # 5. ESKI YEDEKLERI TEMIZLE
    # ============================================
    def eski_yedekleri_temizle(self, gun_sayisi=30):
        """Belirtilen gunden eski yedekleri siler"""
        
        yedekler = glob.glob(os.path.join(self.yedek_klasor, "*.zip"))
        simdi = datetime.now().timestamp()
        silinen = 0
        
        for yedek in yedekler:
            # Dosyanin yasini hesapla (saniye cinsinden)
            dosya_zamani = os.path.getmtime(yedek)
            yas = (simdi - dosya_zamani) / (24*3600)  # Gun cinsinden
            
            if yas > gun_sayisi:
                os.remove(yedek)
                silinen += 1
                print(f"🗑️ Silindi: {os.path.basename(yedek)} ({yas:.1f} gun)")
        
        if silinen > 0:
            print(f"✅ {silinen} eski yedek temizlendi.")
    
    # ============================================
    # 6. YEDEKTEN GERI YUKLE
    # ============================================
    def geri_yukle(self, yedek_dosyasi):
        """Yedek dosyasindan sistemi geri yukler"""
        
        if not os.path.exists(yedek_dosyasi):
            print(f"❌ Yedek dosyasi bulunamadi: {yedek_dosyasi}")
            return False
        
        print(f"\n🔄 YEDEKTEN GERI YUKLENIYOR: {yedek_dosyasi}")
        print("="*60)
        
        # Gecici bir klasor olustur
        gecici_klasor = "gecici_yedek"
        if not os.path.exists(gecici_klasor):
            os.makedirs(gecici_klasor)
        
        # Yedegi ac
        with zipfile.ZipFile(yedek_dosyasi, 'r') as zipf:
            zipf.extractall(gecici_klasor)
            print("📂 Yedek dosyalari acildi")
        
        # Dosyalari geri yukle
        for dosya in os.listdir(gecici_klasor):
            kaynak = os.path.join(gecici_klasor, dosya)
            hedef = dosya
            
            # Eger hedef varsa yedekle
            if os.path.exists(hedef):
                yedek_hedef = hedef + ".yedek"
                shutil.copy2(hedef, yedek_hedef)
                print(f"📌 Eski dosya yedeklendi: {yedek_hedef}")
            
            # Yeni dosyayi kopyala
            if os.path.isfile(kaynak):
                shutil.copy2(kaynak, hedef)
                print(f"✅ Geri yuklendi: {dosya}")
            elif os.path.isdir(kaynak):
                if os.path.exists(hedef):
                    shutil.rmtree(hedef)
                shutil.copytree(kaynak, hedef)
                print(f"✅ Klasor geri yuklendi: {dosya}")
        
        # Gecici klasoru temizle
        shutil.rmtree(gecici_klasor)
        print("-"*60)
        print("✅ Geri yukleme tamamlandi!")
        
        return True

# ============================================
# ANA PROGRAM
# ============================================
if __name__ == "__main__":
    print("""
┌─────────────────────────────────────┐
│  💾 TRM YEDEKLEME SISTEMI          │
│  TURKCE ACIKLAMALI                  │
│  v1.0 - 2026                        │
└─────────────────────────────────────┘
    """)
    
    yedek = BackupSystem()
    
    while True:
        print("\n" + "="*50)
        print("📋 YEDEKLEME MENUSU")
        print("="*50)
        print("1️⃣  Tam yedek al (Tum sistem)")
        print("2️⃣  Hizli yedek al (Onemli dosyalar)")
        print("3️⃣  Gunluk otomatik yedek")
        print("4️⃣  Yedekleri listele")
        print("5️⃣  Eski yedekleri temizle")
        print("6️⃣  Yedekten geri yukle")
        print("7️⃣  Cikis")
        print("-"*50)
        
        secim = input("👉 Seciminiz: ")
        
        if secim == '1':
            yedek.tam_yedek_al()
        
        elif secim == '2':
            yedek.hizli_yedek_al()
        
        elif secim == '3':
            yedek.otomatik_yedekle()
        
        elif secim == '4':
            yedek.yedekleri_listele()
        
        elif secim == '5':
            gun = input("📅 Kac gunden eski yedekler silinsin? (varsayilan: 30): ")
            gun = int(gun) if gun else 30
            yedek.eski_yedekleri_temizle(gun)
        
        elif secim == '6':
            yedekler = glob.glob(os.path.join(yedek.yedek_klasor, "*.zip"))
            if yedekler:
                print("\n📋 MEVCUT YEDEKLER:")
                for i, y in enumerate(yedekler[:10], 1):
                    print(f"   {i}. {os.path.basename(y)}")
                sec = input("📂 Geri yuklenecek yedek numarasi: ")
                try:
                    yedek_dosyasi = yedekler[int(sec)-1]
                    yedek.geri_yukle(yedek_dosyasi)
                except:
                    print("❌ Gecersiz secim!")
            else:
                print("❌ Yedek bulunamadi!")
        
        elif secim == '7':
            print("\n👋 Saglicakla kalin!")
            break
