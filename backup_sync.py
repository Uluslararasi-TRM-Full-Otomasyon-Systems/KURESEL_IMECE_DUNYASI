import os
import shutil
import subprocess
import sys
from datetime import datetime

# Dosyalarının olduğu klasör yolu
SOURCE = r"C:\Users\Habitat\Desktop\SOSYAL İMECE"
# Yedeklerin gideceği klasör yolu
DEST = r"E:\YEDEK_IMECE"

def run_robocopy():
    """Windows'un kendi hızlı kopyalama aracı robocopy ile yedekleme yapar"""
    print(f"[⏳] Yedekleme başlatılıyor: {SOURCE} -> {DEST}")
    try:
        # /E: Alt klasörleri de al
        # /COPY:DAT: Veri, öznitelik ve zaman damgalarını koru
        # /XD: İstemediğimiz klasörleri hariç tut
        cmd = [
            "robocopy", SOURCE, DEST,
            "/E", "/COPY:DAT", "/DCOPY:T",
            "/XD", ".git", "__pycache__", "logs",
            "/XF", "*.log", ".env", "secrets.toml",
            "/R:3", "/W:10", "/NP", "/NFL"
        ]
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        # Robocopy'nin 8'den küçük dönüş kodları başarıyı ifade eder
        if result.returncode < 8:
            print("[✅] Yedekleme başarıyla tamamlandı.")
        else:
            print(f"[⚠️] Yedekleme uyarısı (Kod: {result.returncode})")
    except Exception as e:
        print(f"[❌] Hata oluştu: {e}")

if __name__ == "__main__":
    if not os.path.exists(DEST):
        os.makedirs(DEST)
        print(f"[📁] Hedef klasör oluşturuldu: {DEST}")
    
    run_robocopy()