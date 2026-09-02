import os
import shutil
import json
from datetime import datetime

# 1. Sabit Ana Klasör ve Yedekler Yolu
base_dir = r"C:\Users\Habitat\Desktop\SOSYAL _İMECE"
backup_dir = os.path.join(base_dir, "yedekler")

# Klasörlerin var olduğundan emin olalım
os.makedirs(base_dir, exist_ok=True)
os.makedirs(backup_dir, exist_ok=True)

# 2. Tam Dosya Yolları
config_filename = "nirvana_shield_config.json"
audit_filename = "ultra_guardian_audit.json"

config_path = os.path.join(base_dir, config_filename)
audit_path = os.path.join(base_dir, audit_filename)

# 3. Örnek Verilerle Dosyaları Ana Klasörde Oluşturma
config_data = {
    "system_name": "Ultra Nirvana Guardian",
    "status": "Active",
    "human_behavior_simulation": True,
    "created_at": str(datetime.now())
}

audit_data = {
    "audit_status": "Secure",
    "anti_ban_shield": "Enabled",
    "last_check": str(datetime.now())
}

# Config dosyasını ana klasöre kaydet
with open(config_path, "w", encoding="utf-8") as f:
    json.dump(config_data, f, indent=4)

# Audit dosyasını ana klasöre kaydet
with open(audit_path, "w", encoding="utf-8") as f:
    json.dump(audit_data, f, indent=4)

print(f"✅ Dosyalar ana klasörde oluşturuldu:\n- {config_path}\n- {audit_path}")

# 4. Aynı Anda Yedekler Klasörüne Kopyalama (Yedekleme İşlemi)
shutil.copy(config_path, os.path.join(backup_dir, config_filename))
shutil.copy(audit_path, os.path.join(backup_dir, audit_filename))

print(f"📦 Dosyaların yedekleri başarıyla 'yedekler' klasörüne alındı: {backup_dir}")