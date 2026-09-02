import os
import shutil
import zipfile
from datetime import datetime
import glob

# ============================================
# YEDEKLEME SİSTEMİ
# TÜRKÇE AÇIKLAMALI
# ============================================

class BackupSystem:
    def __init__(self):
        """Yedekleme sistemini başlatır"""
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
        
        # Yedek klasörü yoksa oluştur
        if not os.path.exists(self.yedek_klasor):
            os.makedirs(self.yedek_klasor)
            print(f"✅ Yedek klasörü oluşturuldu: {self.yedek_klasor}")
    
    # ============================================
    # 1. TAM YEDEK AL
    # ============================================
    def tam_yedek_al(self):
        """Tüm sistemin tam yedeğini alır"""
        
        tarih = datetime.now().strftime("%Y%m%d_%H%M%S")
        yedek_adi = f"tam_yedek_{tarih}.zip"
        yedek_yolu = os.path.join(self.yedek_klasor, yedek_adi)
        
        print(f"\n📦 TAM YEDEK ALINIYOR: {yedek_adi}")
        print("="*60)
        
        with zipfile.ZipFile(yedek_yolu, 'w', zipfile.ZIP_DEFLATED) as zipf:
            # Python dosyalarını ekle
            for dosya in glob.glob("*.py"):
                zipf.write(dosya)
                print(f"   📄 {dosya} eklendi")
            
            # Veritabanı dosyalarını ekle
            for dosya in ['sales.db', 'team_list.csv']:
                if os.path.exists(dosya):
                    zipf.write(dosya)
                    print(f"   🗄️ {dosya} eklendi")
            
            # .env dosyasını ekle
            if os.path.exists('secrets.env'):
                zipf.write('secrets.env')
                print(f"   🔐 secrets.env eklendi")
            
            # core klasörünü ekle
            if os.path.exists('core'):
                for root, dirs, files in os.walk('core'):
                    for file in files:
                        dosya_yolu = os.path.join(root, file)
                        zipf.write(dosya_yolu)
                print(f"   📁 core/ klasörü eklendi")
        
        # Dosya boyutunu hesapla
        boyut_mb = os.path.getsize(yedek_yolu) / (1024*1024)
        print("-"*60)
        print(f"✅ Tam yedek alındı: {yedek_adi} ({boyut_mb:.2f} MB)")
        
        return yedek_yolu
    
    # ============================================
    # 2. HIZLI YEDEK AL (SADECE ÖNEMLİ DOSYALAR)
    # ============================================
    def hizli_yedek_al(self):
        """Sadece önemli dosyaların yedeğini alır"""
        
        tarih = datetime.now().strftime("%Y%m%d_%H%M%S")
        yedek_adi = f"hizli_yedek_{tarih}.zip"
        yedek_yolu = os.path.join(self.yedek_klasor, yedek_adi)
        
        print(f"\n⚡ HIZLI YEDEK ALINIYOR: {yedek_adi}")
        print("="*60)
        
        with zipfile.ZipFile(yedek_yolu, 'w', zipfile.ZIP_DEFLATED) as zipf:
            # Önemli dosyaları ekle
            for dosya in self.kaynak_dosyalar:
                if os.path.exists(dosya):
                    zipf.write(dosya)
                    print(f"   ✅ {dosya} eklendi")
        
        # Dosya boyutunu hesapla
        boyut_mb = os.path.getsize(yedek_yolu) / (1024*1024)
        print("-"*60)
        print(f"✅ Hızlı yedek alındı: {yedek_adi} ({boyut_mb:.2f} MB)")
        
        return yedek_yolu
    
    # ============================================
    # 3. OTOMATİK YEDEKLEME (GÜNLÜK)
    # ============================================
    def otomatik_yedekle(self):
        """Her gün otomatik yedek alır (eski yedekleri temizler)"""
        
        tarih = datetime.now().strftime("%Y%m%d")
        yedek_adi = f"gunluk_yedek_{tarih}.zip"
        yedek_yolu = os.path.join(self.yedek_klasor, yedek_adi)
        
        # Bugün zaten yedek alınmış mı?
        if os.path.exists(yedek_yolu):
            print(f"⚠️ Bugün için yedek zaten var: {yedek_adi}")
            return yedek_yolu
        
        print(f"\n📅 GÜNLÜK OTOMATİK YEDEK: {yedek_adi}")
        
        with zipfile.ZipFile(yedek_yolu, 'w', zipfile.ZIP_DEFLATED) as zipf:
            # Python dosyalarını ekle
            for dosya in glob.glob("*.py"):
                if os.path.exists(dosya):
                    zipf.write(dosya)
            
            # Veritabanı dosyalarını ekle
            for dosya in ['sales.db', 'team_list.csv']:
                if os.path.exists(dosya):
                    zipf.write(dosya)
        
        print(f"✅ Günlük yedek alındı: {yedek_adi}")
        
        # 30 günden eski yedekleri temizle
        self.eski_yedekleri_temizle(30)
        
        return yedek_yolu
    
    # ============================================
    # 4. YEDEKLERİ LİSTELE
    # ============================================
    def yedekleri_listele(self):
        """Tüm yedekleri listeler"""
        
        yedekler = glob.glob(os.path.join(self.yedek_klasor, "*.zip"))
        
        if not yedekler:
            print("\n📭 Henüz yedek bulunmuyor.")
            return
        
        print("\n" + "="*70)
        print("📋 MEVCUT YEDEKLER")
        print("="*70)
        
        # Tarihe göre sırala (yeniden eskiye)
        yedekler.sort(reverse=True)
        
        toplam_boyut = 0
        for yedek in yedekler[:20]:  # Son 20 yedeği göster
            ad = os.path.basename(yedek)
            boyut_mb = os.path.getsize(yedek) / (1024*1024)
            tarih = datetime.fromtimestamp(os.path.getmtime(yedek))
            print(f"📦 {ad}")
            print(f"   📅 {tarih.strftime('%d.%m.%Y %H:%M')} | 💾 {boyut_mb:.2f} MB")
            toplam_boyut += boyut_mb
        
        print("-"*70)
        print(f"📊 Toplam: {len(yedekler)} yedek, {toplam_boyut:.2f} MB")
    
    # ============================================
    # 5. ESKİ YEDEKLERİ TEMİZLE
    # ============================================
    def eski_yedekleri_temizle(self, gun_sayisi=30):
        """Belirtilen günden eski yedekleri siler"""
        
        yedekler = glob.glob(os.path.join(self.yedek_klasor, "*.zip"))
        simdi = datetime.now().timestamp()
        silinen = 0
        
        for yedek in yedekler:
            # Dosyanın yaşını hesapla (saniye cinsinden)
            dosya_zamani = os.path.getmtime(yedek)
            yas = (simdi - dosya_zamani) / (24*3600)  # Gün cinsinden
            
            if yas > gun_sayisi:
                os.remove(yedek)
                silinen += 1
                print(f"🗑️ Silindi: {os.path.basename(yedek)} ({yas:.1f} gün)")
        
        if silinen > 0:
            print(f"✅ {silinen} eski yedek temizlendi.")
    
    # ============================================
    # 6. YEDEKTEN GERİ YÜKLE
    # ============================================
    def geri_yukle(self, yedek_dosyasi):
        """Yedek dosyasından sistemi geri yükler"""
        
        if not os.path.exists(yedek_dosyasi):
            print(f"❌ Yedek dosyası bulunamadı: {yedek_dosyasi}")
            return False
        
        print(f"\n🔄 YEDEKTEN GERİ YÜKLENİYOR: {yedek_dosyasi}")
        print("="*60)
        
        # Geçici bir klasör oluştur
        gecici_klasor = "gecici_yedek"
        if not os.path.exists(gecici_klasor):
            os.makedirs(gecici_klasor)
        
        # Yedeği aç
        with zipfile.ZipFile(yedek_dosyasi, 'r') as zipf:
            zipf.extractall(gecici_klasor)
            print("📂 Yedek dosyaları açıldı")
        
        # Dosyaları geri yükle
        for dosya in os.listdir(gecici_klasor):
            kaynak = os.path.join(gecici_klasor, dosya)
            hedef = dosya
            
            # Eğer hedef varsa yedekle
            if os.path.exists(hedef):
                yedek_hedef = hedef + ".yedek"
                shutil.copy2(hedef, yedek_hedef)
                print(f"📌 Eski dosya yedeklendi: {yedek_hedef}")
            
            # Yeni dosyayı kopyala
            if os.path.isfile(kaynak):
                shutil.copy2(kaynak, hedef)
                print(f"✅ Geri yüklendi: {dosya}")
            elif os.path.isdir(kaynak):
                if os.path.exists(hedef):
                    shutil.rmtree(hedef)
                shutil.copytree(kaynak, hedef)
                print(f"✅ Klasör geri yüklendi: {dosya}")
        
        # Geçici klasörü temizle
        shutil.rmtree(gecici_klasor)
        print("-"*60)
        print("✅ Geri yükleme tamamlandı!")
        
        return True

# ============================================
# ANA PROGRAM
# ============================================
if __name__ == "__main__":
    print("""
┌─────────────────────────────────────┐
│  💾 TRM YEDEKLEME SİSTEMİ          │
│  TÜRKÇE AÇIKLAMALI                  │
│  v1.0 - 2026                        │
└─────────────────────────────────────┘
    """)
    
    yedek = BackupSystem()
    
    while True:
        print("\n" + "="*50)
        print("📋 YEDEKLEME MENÜSÜ")
        print("="*50)
        print("1️⃣  Tam yedek al (Tüm sistem)")
        print("2️⃣  Hızlı yedek al (Önemli dosyalar)")
        print("3️⃣  Günlük otomatik yedek")
        print("4️⃣  Yedekleri listele")
        print("5️⃣  Eski yedekleri temizle")
        print("6️⃣  Yedekten geri yükle")
        print("7️⃣  Çıkış")
        print("-"*50)
        
        secim = input("👉 Seçiminiz: ")
        
        if secim == '1':
            yedek.tam_yedek_al()
        
        elif secim == '2':
            yedek.hizli_yedek_al()
        
        elif secim == '3':
            yedek.otomatik_yedekle()
        
        elif secim == '4':
            yedek.yedekleri_listele()
        
        elif secim == '5':
            gun = input("📅 Kaç günden eski yedekler silinsin? (varsayılan: 30): ")
            gun = int(gun) if gun else 30
            yedek.eski_yedekleri_temizle(gun)
        
        elif secim == '6':
            yedekler = glob.glob(os.path.join(yedek.yedek_klasor, "*.zip"))
            if yedekler:
                print("\n📋 MEVCUT YEDEKLER:")
                for i, y in enumerate(yedekler[:10], 1):
                    print(f"   {i}. {os.path.basename(y)}")
                sec = input("📂 Geri yüklenecek yedek numarası: ")
                try:
                    yedek_dosyasi = yedekler[int(sec)-1]
                    yedek.geri_yukle(yedek_dosyasi)
                except:
                    print("❌ Geçersiz seçim!")
            else:
                print("❌ Yedek bulunamadı!")
        
        elif secim == '7':
            print("\n👋 Sağlıcakla kalın!")
            break
