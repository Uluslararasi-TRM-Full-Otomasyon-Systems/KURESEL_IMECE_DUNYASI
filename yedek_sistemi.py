import os
import zipfile
from datetime import datetime
import glob

class BackupSystem:
    def __init__(self):
        self.yedek_klasor = "yedekler"
        if not os.path.exists(self.yedek_klasor):
            os.makedirs(self.yedek_klasor)
            
    def tam_yedek_al(self):
        tarih = datetime.now().strftime("%Y%m%d_%H%M%S")
        yedek_yolu = os.path.join(self.yedek_klasor, f"tam_yedek_{tarih}.zip")
        
        with zipfile.ZipFile(yedek_yolu, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for dosya in glob.glob("*.py"):
                zipf.write(dosya)
            for dosya in ['sales.db', 'team_list.csv', 'secrets.env']:
                if os.path.exists(dosya):
                    zipf.write(dosya)
            if os.path.exists('core'):
                for root, dirs, files in os.walk('core'):
                    for file in files:
                        zipf.write(os.path.join(root, file))
                        
        print(f"Tam yedek oluşturuldu: {yedek_yolu}")
        return yedek_yolu

if __name__ == "__main__":
    BackupSystem().tam_yedek_al()