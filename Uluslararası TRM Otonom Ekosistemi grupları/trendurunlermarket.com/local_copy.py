import shutil
import os
import sys

# Ana klasorumuzun yolunu al
source_dir = os.path.dirname(os.path.abspath(__file__))
# Hedef klasorumuzu masaustunde olustur
dest_dir = os.path.join(os.path.dirname(source_dir), "TRM_ACIL_NAKIT_OTOMASYONU")

# Izin sorunlari olacak klasorleri haric tut
exclude_dirs = [".user-python", ".git", "__pycache__", "tmp", ".venv", "env", ".ngrok-lib", ".streamlit-lib", ".lt-lib"]

# Hedef klasoru olustur
os.makedirs(dest_dir, exist_ok=True)
print("Hedef klasor olusturuldu:", dest_dir)

# Tum dosyalari ve klasorleri kopyala
for item in os.listdir(source_dir):
    s = os.path.join(source_dir, item)
    d = os.path.join(dest_dir, item)
    
    # Haric tutulan klasorleri atla
    if os.path.isdir(s) and item in exclude_dirs:
        print("Atlandi:", item)
        continue
        
    try:
        if os.path.isdir(s):
            shutil.copytree(s, d, dirs_exist_ok=True)
        else:
            shutil.copy2(s, d)
        print("Kopyalandi:", item)
    except Exception as e:
        print("Atlandi:", item, "- Hata:", str(e))

print("\nKopyalama islemi TAMAMLANDI!")
print("Yeni klasor:", dest_dir)
