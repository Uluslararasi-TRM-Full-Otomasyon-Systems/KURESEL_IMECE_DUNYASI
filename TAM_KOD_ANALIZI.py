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
                        print(f"   📁 {dosya_yolu} eklendi")
                        
        print(f"✅ Tam yedek başarıyla oluşturuldu: {yedek_yolu}")
        return yedek_yolu

if __name__ == "__main__":
    backup = BackupSystem()
    backup.tam_yedek_al()