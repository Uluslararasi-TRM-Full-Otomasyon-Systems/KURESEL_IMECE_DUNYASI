# TRM FULL OTOMASYON SİSTEMİ - SİSTEM BAKIM VE OPTİMİZASYON KILAVUZU

## 📋 İÇERİK TABLOSU

1. [Sistem Bakım Planı](#sistem-bakım-planı)
2. [Performans Optimizasyonu](#performans-optimizasyonu)
3. [Veri Yönetimi](#veri-yönetimi)
4. [Güvenlik Bakımı](#güvenlik-bakımı)
5. [Sorun Önleme](#sorun-önleme)
6. [Yedekleme ve Kurtarma](#yedekleme-ve-kurtarma)
7. [Sistem Güncellemeleri](#sistem-güncellemeleri)
8. [İzleme ve Raporlama](#izleme-ve-raporlama)

---

## 🔄 SİSTEM BAKIM PLANI

### Günlük Bakım (Her Gün)
**Zaman:** 09:00 - 09:30

**Görevler:**
- [ ] Sistem durumunu kontrol et
- [ ] Hata loglarını gözden geçir
- [ ] Performans metriklerini kaydet
- [ ] Bellek ve CPU kullanımını kontrol et
- [ ] Disk alanını kontrol et
- [ ] Yedekleme durumunu doğrula
- [ ] API anahtarlarının geçerliliğini kontrol et

**Otomatik Script:**
```batch
@echo off
echo 🔍 Günlük Bakım Başlatılıyor...
cd /d "G:\Uluslararasi-TRM-Full-Otomasyon-Sistemi"
call CHECK_SYSTEM.bat
echo ✅ Günlük Bakım Tamamlandı
```

### Haftalık Bakım (Her Pazar)
**Zaman:** 10:00 - 11:00

**Görevler:**
- [ ] Log dosyalarını temizle (30 günden eski)
- [ ] Veri tabanını optimize et
- [ ] Sistem performansını analiz et
- [ ] Güncelleme kontrolü yap
- [ ] Tam sistem yedeği al
- [ ] Port taraması yap
- [ ] Sistem kaynaklarını optimize et

**Otomatik Script:**
```batch
@echo off
echo 🗂️ Haftalık Bakım Başlatılıyor...
cd /d "G:\Uluslararasi-TRM-Full-Otomasyon-Sistemi"

# Log temizleme
forfiles /P logs /M *.log /D -30 /C "cmd /c del @path"

# Veri tabanı optimizasyonu
python -c "
import sqlite3
conn = sqlite3.connect('trm_dashboard.db')
conn.execute('VACUUM')
conn.close()
print('✅ Veri tabanı optimize edildi')
"

echo ✅ Haftalık Bakım Tamamlandı
```

### Aylık Bakım (Her Ayın İlk Günü)
**Zaman:** 14:00 - 16:00

**Görevler:**
- [ ] Tüm sistemi durdur
- [ ] Tam sistem yedeği al
- [ ] Sistem güncellemelerini kontrol et
- [ ] Python kütüphanelerini güncelle
- [ ] Sistem ayarlarını gözden geçir
- [ ] Güvenlik taraması yap
- [ ] Performans testleri çalıştır
- [ ] Sistemi yeniden başlat
- [ ] Tüm fonksiyonları test et

**Otomatik Script:**
```batch
@echo off
echo 🔄 Aylık Bakım Başlatılıyor...
cd /d "G:\Uluslararasi-TRM-Full-Otomasyon-Sistemi"

# Sistemi durdur
taskkill /f /im python.exe

# Yedekleme
xcopy "." "..\TRM_Yedek_%date:~0,10%" /E /I /H /Y

# Python güncelleme
pip install --upgrade -r requirements.txt

# Sistemi başlat
start MASTER_BASLATICI.bat

echo ✅ Aylık Bakım Tamamlandı
```

---

## ⚡ PERFORMANS OPTİMİZASYONU

### Bellek Optimizasyonu

#### 🧹 Bellek Temizleme
```python
import psutil
import gc
import os

def optimize_memory():
    # Garbage collection
    gc.collect()
    
    # Bellek kullanımını kontrol et
    memory = psutil.virtual_memory()
    if memory.percent > 80:
        print(f"⚠️ Yüksek bellek kullanımı: {memory.percent}%")
        
        # Gereksiz değişkenleri temizle
        for obj in gc.get_objects():
            if isinstance(obj, (list, dict, set)):
                if len(obj) > 10000:  # Büyük objeleri temizle
                    del obj
        
        gc.collect()
        print("✅ Bellek optimize edildi")

optimize_memory()
```

#### 📊 Bellek İzleme
```python
import psutil
import time

def monitor_memory():
    while True:
        memory = psutil.virtual_memory()
        cpu = psutil.cpu_percent(interval=1)
        
        print(f"Bellek: {memory.percent}%, CPU: {cpu}%")
        
        if memory.percent > 90:
            print("⚠️ Kritik bellek kullanımı!")
            
        time.sleep(60)  # Her dakika

# monitor_memory()
```

### CPU Optimizasyonu

#### 🔄 İşlemci Yönetimi
```python
import multiprocessing
import threading

def optimize_cpu_usage():
    # İşlemci sayısını al
    cpu_count = multiprocessing.cpu_count()
    
    # İşlem parçacığı havuzu oluştur
    max_workers = min(cpu_count - 1, 4)  # 1 çekirdek bırak
    
    print(f"📊 CPU optimizasyonu: {max_workers} worker")
    
    return max_workers

optimize_cpu_usage()
```

#### 🌡️ Sıcaklık İzleme
```python
import psutil

def check_cpu_temperature():
    try:
        temps = psutil.sensors_temperatures()
        if 'coretemp' in temps:
            for temp in temps['coretemp']:
                print(f"CPU Sıcaklığı: {temp.current}°C")
                
                if temp.current > 80:
                    print("⚠️ Yüksek CPU sıcaklığı!")
    except:
        print("Sıcaklık sensörü bulunamadı")

check_cpu_temperature()
```

### Disk Optimizasyonu

#### 💾 Disk Temizleme
```python
import os
import shutil

def clean_temp_files():
    temp_dirs = [
        'temp_photos',
        'temp_docs',
        'logs',
        '__pycache__'
    ]
    
    for temp_dir in temp_dirs:
        if os.path.exists(temp_dir):
            try:
                shutil.rmtree(temp_dir)
                os.makedirs(temp_dir)
                print(f"✅ {temp_dir} temizlendi")
            except Exception as e:
                print(f"❌ {temp_dir} temizlenemedi: {e}")

clean_temp_files()
```

#### 📈 Disk Analizi
```python
import psutil

def analyze_disk_usage():
    disk = psutil.disk_usage('/')
    
    total = disk.total / (1024**3)  # GB
    used = disk.used / (1024**3)
    free = disk.free / (1024**3)
    percent = (used / total) * 100
    
    print(f"💾 Disk Kullanımı:")
    print(f"   Toplam: {total:.1f} GB")
    print(f"   Kullanılan: {used:.1f} GB ({percent:.1f}%)")
    print(f"   Boş: {free:.1f} GB")
    
    if percent > 90:
        print("⚠️ Düşük disk alanı!")

analyze_disk_usage()
```

---

## 📁 VERİ YÖNETİMİ

### Log Yönetimi

#### 📋 Log Rotasyonu
```python
import os
import gzip
import shutil
from datetime import datetime, timedelta

def rotate_logs():
    log_dir = 'logs'
    max_age_days = 30
    
    for filename in os.listdir(log_dir):
        if filename.endswith('.log'):
            filepath = os.path.join(log_dir, filename)
            file_age = datetime.now() - datetime.fromtimestamp(os.path.getmtime(filepath))
            
            if file_age.days > max_age_days:
                # Log'u sıkıştır
                with open(filepath, 'rb') as f_in:
                    with gzip.open(f"{filepath}.gz", 'wb') as f_out:
                        shutil.copyfileobj(f_in, f_out)
                
                # Orijinal log'u sil
                os.remove(filepath)
                print(f"✅ {filename} sıkıştırıldı")

rotate_logs()
```

#### 📊 Log Analizi
```python
import re
from collections import Counter

def analyze_logs():
    log_files = ['logs/system_manager.log', 'logs/auto_restart.log']
    
    error_patterns = [
        r'ERROR',
        r'CRITICAL',
        r'Exception',
        r'Failed'
    ]
    
    for log_file in log_files:
        if os.path.exists(log_file):
            with open(log_file, 'r') as f:
                content = f.read()
                
                # Hata sayısını say
                error_count = 0
                for pattern in error_patterns:
                    errors = re.findall(pattern, content, re.IGNORECASE)
                    error_count += len(errors)
                
                print(f"📋 {log_file}: {error_count} hata")

analyze_logs()
```

### Veri Tabanı Bakımı

#### 🗄️ Veri Tabanı Optimizasyonu
```python
import sqlite3
import json

def optimize_database():
    db_files = ['trm_dashboard.db', 'trm_system.db']
    
    for db_file in db_files:
        if os.path.exists(db_file):
            try:
                conn = sqlite3.connect(db_file)
                
                # Tabloları optimize et
                cursor = conn.cursor()
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
                tables = cursor.fetchall()
                
                for table in tables:
                    table_name = table[0]
                    cursor.execute(f"VACUUM {table_name}")
                    cursor.execute(f"REINDEX {table_name}")
                    print(f"✅ {table_name} optimize edildi")
                
                conn.commit()
                conn.close()
                
                # Veri tabanı boyutunu göster
                size = os.path.getsize(db_file) / (1024*1024)  # MB
                print(f"📊 {db_file}: {size:.1f} MB")
                
            except Exception as e:
                print(f"❌ {db_file} optimize edilemedi: {e}")

optimize_database()
```

#### 📈 Veri Temizleme
```python
import sqlite3
from datetime import datetime, timedelta

def clean_old_data():
    db_file = 'trm_dashboard.db'
    
    if os.path.exists(db_file):
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()
        
        # 30 günden eski verileri temizle
        cutoff_date = datetime.now() - timedelta(days=30)
        
        tables_to_clean = [
            'error_logs',
            'social_posts',
            'notifications'
        ]
        
        for table in tables_to_clean:
            try:
                cursor.execute(f"DELETE FROM {table} WHERE timestamp < ?", (cutoff_date,))
                deleted = cursor.rowcount
                print(f"🗑️ {table}: {deleted} kayıt silindi")
            except Exception as e:
                print(f"❌ {table} temizlenemedi: {e}")
        
        conn.commit()
        conn.close()

clean_old_data()
```

---

## 🔒 GÜVENLİK BAKIMI

### API Anahtar Yönetimi

#### 🔑 Anahtar Güvenliği
```python
import os
import json
from cryptography.fernet import Fernet

def encrypt_api_keys():
    # API anahtarlarını şifrele
    api_keys = {
        'TELEGRAM_API_ID': os.getenv('TELEGRAM_API_ID'),
        'DEEPSEEK_API_KEY': os.getenv('DEEPSEEK_API_KEY'),
        'CLAUDE_API_KEY': os.getenv('CLAUDE_API_KEY')
    }
    
    # Şifreleme anahtarı oluştur
    key = Fernet.generate_key()
    cipher_suite = Fernet(key)
    
    # Anahtarları şifrele
    encrypted_keys = {}
    for key_name, key_value in api_keys.items():
        if key_value:
            encrypted_keys[key_name] = cipher_suite.encrypt(key_value.encode()).decode()
    
    # Şifreli anahtarları kaydet
    with open('encrypted_keys.json', 'w') as f:
        json.dump(encrypted_keys, f)
    
    # Şifreleme anahtarını güvenli bir yere kaydet
    with open('encryption_key.key', 'wb') as f:
        f.write(key)
    
    print("✅ API anahtarları şifrelendi")

encrypt_api_keys()
```

#### 🔍 Anahtar Geçerliliği
```python
import requests
import json

def validate_api_keys():
    api_endpoints = {
        'DEEPSEEK': 'https://api.deepseek.com/v1/models',
        'CLAUDE': 'https://api.anthropic.com/v1/messages'
    }
    
    for service, endpoint in api_endpoints.items():
        api_key = os.getenv(f'{service}_API_KEY')
        
        if api_key:
            try:
                headers = {'Authorization': f'Bearer {api_key}'}
                response = requests.get(endpoint, headers=headers, timeout=10)
                
                if response.status_code == 200:
                    print(f"✅ {service} API anahtarı geçerli")
                else:
                    print(f"❌ {service} API anahtarı geçersiz: {response.status_code}")
                    
            except Exception as e:
                print(f"❌ {service} API anahtarı kontrol edilemedi: {e}")

validate_api_keys()
```

### Sistem Güvenliği

#### 🛡️ Port Taraması
```python
import socket
import threading

def scan_ports():
    ports_to_check = [9000, 9001, 9002, 9003, 9004, 9005]
    
    def check_port(port):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        
        result = sock.connect_ex(('localhost', port))
        if result == 0:
            print(f"✅ Port {port}: Açık")
        else:
            print(f"❌ Port {port}: Kapalı")
        
        sock.close()
    
    threads = []
    for port in ports_to_check:
        thread = threading.Thread(target=check_port, args=(port,))
        threads.append(thread)
        thread.start()
    
    for thread in threads:
        thread.join()

scan_ports()
```

#### 🔒 Firewall Kontrolü
```batch
@echo off
echo 🔒 Firewall Durumu Kontrol Ediliyor...

# Windows Firewall durumunu kontrol et
netsh advfirewall show allprofiles

# Portların açık olup olmadığını kontrol et
netsh advfirewall firewall show rule name="TRM Panel" >nul 2>&1
if errorlevel 1 (
    echo ❌ TRM Panel kuralı bulunamadı
    echo 📝 Port kuralı ekleniyor...
    netsh advfirewall firewall add rule name="TRM Panel" dir=in action=allow protocol=TCP localport=9000-9005
    echo ✅ Port kuralı eklendi
) else (
    echo ✅ TRM Panel kuralı mevcut
)

pause
```

---

## 🛡️ SORUN ÖNLEME

### Hata Tahmini

#### 🤖 Hata Tahmin Sistemi
```python
import psutil
import time
from datetime import datetime

class ErrorPredictor:
    def __init__(self):
        self.history = []
        self.thresholds = {
            'memory': 85,  # %
            'cpu': 90,     # %
            'disk': 90      # %
        }
    
    def collect_metrics(self):
        metrics = {
            'timestamp': datetime.now(),
            'memory': psutil.virtual_memory().percent,
            'cpu': psutil.cpu_percent(interval=1),
            'disk': psutil.disk_usage('/').percent
        }
        
        self.history.append(metrics)
        
        # Son 100 kaydı tut
        if len(self.history) > 100:
            self.history.pop(0)
        
        return metrics
    
    def predict_errors(self):
        if len(self.history) < 10:
            return None
        
        # Son 10 ölçümün ortalamasını al
        recent = self.history[-10:]
        avg_memory = sum(m['memory'] for m in recent) / 10
        avg_cpu = sum(m['cpu'] for m in recent) / 10
        avg_disk = sum(m['disk'] for m in recent) / 10
        
        warnings = []
        
        if avg_memory > self.thresholds['memory']:
            warnings.append(f"⚠️ Yüksek bellek kullanımı tahmini: {avg_memory:.1f}%")
        
        if avg_cpu > self.thresholds['cpu']:
            warnings.append(f"⚠️ Yüksek CPU kullanımı tahmini: {avg_cpu:.1f}%")
        
        if avg_disk > self.thresholds['disk']:
            warnings.append(f"⚠️ Düşük disk alanı tahmini: {avg_disk:.1f}%")
        
        return warnings
    
    def run_monitoring(self):
        while True:
            metrics = self.collect_metrics()
            warnings = self.predict_errors()
            
            if warnings:
                for warning in warnings:
                    print(f"🔮 {warning}")
            
            time.sleep(60)  # Her dakika

# predictor = ErrorPredictor()
# predictor.run_monitoring()
```

#### 📊 Performans Trend Analizi
```python
import matplotlib.pyplot as plt
import json
from datetime import datetime, timedelta

def analyze_performance_trends():
    # Son 7 günlük veriyi yükle
    with open('performance_data.json', 'r') as f:
        data = json.load(f)
    
    # Grafik oluştur
    fig, axes = plt.subplots(2, 2, figsize=(12, 8))
    
    # CPU grafiği
    cpu_data = [d['cpu'] for d in data]
    axes[0, 0].plot(cpu_data)
    axes[0, 0].set_title('CPU Kullanımı (%)')
    axes[0, 0].set_ylim(0, 100)
    
    # Bellek grafiği
    memory_data = [d['memory'] for d in data]
    axes[0, 1].plot(memory_data)
    axes[0, 1].set_title('Bellek Kullanımı (%)')
    axes[0, 1].set_ylim(0, 100)
    
    # Disk grafiği
    disk_data = [d['disk'] for d in data]
    axes[1, 0].plot(disk_data)
    axes[1, 0].set_title('Disk Kullanımı (%)')
    axes[1, 0].set_ylim(0, 100)
    
    # Yanıt süresi grafiği
    response_time = [d['response_time'] for d in data]
    axes[1, 1].plot(response_time)
    axes[1, 1].set_title('Yanıt Süresi (ms)')
    
    plt.tight_layout()
    plt.savefig('performance_trends.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    print("✅ Performans trend grafiği oluşturuldu")

analyze_performance_trends()
```

### Otomatik Kurtarma

#### 🔄 Otomatik Sistem Kurtarma
```python
import subprocess
import time
import os

class SystemRecovery:
    def __init__(self):
        self.max_restarts = 3
        self.restart_count = 0
        self.last_restart = time.time()
    
    def check_system_health(self):
        # Sistem sağlığını kontrol et
        try:
            import requests
            response = requests.get('http://localhost:9001/status', timeout=5)
            return response.status_code == 200
        except:
            return False
    
    def restart_system(self):
        if self.restart_count >= self.max_restarts:
            print("❌ Maksimum yeniden başlatma sayısına ulaşıldı")
            return False
        
        # Son yeniden başlatmadan 5 dakika geçmiş mi?
        if time.time() - self.last_restart < 300:
            print("❌ Yeniden başlatma için çok erken")
            return False
        
        print("🔄 Sistem yeniden başlatılıyor...")
        
        # Sistemi durdur
        subprocess.run(['taskkill', '/f', '/im', 'python.exe'], shell=True)
        time.sleep(10)
        
        # Sistemi başlat
        subprocess.run(['start', 'MASTER_BASLATICI.bat'], shell=True)
        
        self.restart_count += 1
        self.last_restart = time.time()
        
        print(f"✅ Sistem yeniden başlatıldı ({self.restart_count}/{self.max_restarts})")
        return True
    
    def run_recovery(self):
        while True:
            if not self.check_system_health():
                print("❌ Sistem sağlığı kritik!")
                
                if not self.restart_system():
                    print("❌ Otomatik kurtarma başarısız!")
                    break
                
                time.sleep(60)  # 1 dakika bekle
            else:
                self.restart_count = 0  # Başarılı olunca sıfırla
            
            time.sleep(30)  # 30 saniyede bir kontrol et

# recovery = SystemRecovery()
# recovery.run_recovery()
```

---

## 💾 YEDEKLEME VE KURTARMA

### Otomatik Yedekleme

#### 📅 Zamanlanmış Yedekleme
```python
import shutil
import os
from datetime import datetime
import schedule

def create_backup():
    backup_dir = f"../TRM_Yedek_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    try:
        # Yedekleme klasörünü oluştur
        os.makedirs(backup_dir, exist_ok=True)
        
        # Önemli dosyaları yedekle
        files_to_backup = [
            'secrets.env',
            'config.py',
            'trm_dashboard.db',
            'logs/',
            'data/'
        ]
        
        for item in files_to_backup:
            src = item
            dst = os.path.join(backup_dir, item)
            
            if os.path.isdir(src):
                shutil.copytree(src, dst)
            else:
                shutil.copy2(src, dst)
            
            print(f"✅ {src} yedeklendi")
        
        # Yedek boyutunu hesapla
        total_size = sum(os.path.getsize(os.path.join(dirpath, filename)) 
                      for dirpath, dirnames, filenames in os.walk(backup_dir) 
                      for filename in filenames)
        
        size_mb = total_size / (1024 * 1024)
        print(f"📊 Yedek boyutu: {size_mb:.1f} MB")
        print(f"📂 Yedek konumu: {backup_dir}")
        
    except Exception as e:
        print(f"❌ Yedekleme başarısız: {e}")

# Her gün saat 02:00'da yedekle
schedule.every().day.at("02:00").do(create_backup)

def run_backup_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(60)

# run_backup_scheduler()
```

#### 🗜️ Yedek Temizleme
```python
import os
from datetime import datetime, timedelta

def clean_old_backups():
    backup_parent = "../"
    max_age_days = 30
    
    for item in os.listdir(backup_parent):
        if item.startswith("TRM_Yedek_"):
            backup_path = os.path.join(backup_parent, item)
            
            # Yedek yaşını hesapla
            backup_date = datetime.strptime(item.split('_')[1], "%Y%m%d_%H%M%S")
            age = datetime.now() - backup_date
            
            if age.days > max_age_days:
                try:
                    shutil.rmtree(backup_path)
                    print(f"🗑️ Eski yedek silindi: {item}")
                except Exception as e:
                    print(f"❌ Yedek silinemedi: {item} - {e}")

clean_old_backups()
```

### Kurtarma İşlemleri

#### 🔄 Sistem Kurtarma
```python
import shutil
import os

def restore_system(backup_date):
    backup_dir = f"../TRM_Yedek_{backup_date}"
    
    if not os.path.exists(backup_dir):
        print(f"❌ Yedek bulunamadı: {backup_dir}")
        return False
    
    try:
        # Mevcut sistem dosyalarını yedekle
        current_backup = f"../TRM_BeforeRestore_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        shutil.copytree(".", current_backup)
        
        # Yedekten geri yükle
        files_to_restore = [
            'secrets.env',
            'config.py',
            'trm_dashboard.db',
            'logs/',
            'data/'
        ]
        
        for item in files_to_restore:
            src = os.path.join(backup_dir, item)
            dst = item
            
            if os.path.exists(dst):
                if os.path.isdir(dst):
                    shutil.rmtree(dst)
                else:
                    os.remove(dst)
            
            if os.path.isdir(src):
                shutil.copytree(src, dst)
            else:
                shutil.copy2(src, dst)
            
            print(f"✅ {item} geri yüklendi")
        
        print(f"✅ Sistem {backup_date} yedekten geri yüklendi")
        return True
        
    except Exception as e:
        print(f"❌ Kurtarma başarısız: {e}")
        return False

# Kullanım: restore_system("20240115_020000")
```

---

## 🔄 SİSTEM GÜNCELLEMELERİ

### Otomatik Güncelleme Kontrolü

#### 📲 Güncelleme Kontrolü
```python
import requests
import json
from datetime import datetime

def check_updates():
    current_version = "3.0.0"
    update_url = "https://api.trmnirvana.com/updates"
    
    try:
        response = requests.get(update_url, timeout=10)
        update_info = response.json()
        
        latest_version = update_info.get('latest_version')
        release_notes = update_info.get('release_notes', [])
        download_url = update_info.get('download_url')
        
        if latest_version > current_version:
            print(f"🆕 Yeni sürüm mevcut: {latest_version}")
            print(f"📝 Mevcut sürüm: {current_version}")
            print("\n📋 Yenilikler:")
            for note in release_notes:
                print(f"  • {note}")
            
            print(f"\n📥 İndirme linki: {download_url}")
            
            return {
                'update_available': True,
                'latest_version': latest_version,
                'download_url': download_url,
                'release_notes': release_notes
            }
        else:
            print("✅ Sistem güncel")
            return {'update_available': False}
            
    except Exception as e:
        print(f"❌ Güncelleme kontrol edilemedi: {e}")
        return None

update_info = check_updates()
```

#### 📥 Otomatik Güncelleme
```python
import requests
import zipfile
import os

def auto_update(update_info):
    if not update_info or not update_info.get('update_available'):
        return False
    
    download_url = update_info['download_url']
    latest_version = update_info['latest_version']
    
    try:
        print(f"📥 Güncelleme indiriliyor: {latest_version}")
        
        # Güncelleme dosyasını indir
        response = requests.get(download_url, stream=True)
        update_file = f"TRM_Update_{latest_version}.zip"
        
        with open(update_file, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        print(f"✅ Güncelleme indirildi: {update_file}")
        
        # Sistemi durdur
        print("⏹️ Sistem durduruluyor...")
        os.system("taskkill /f /im python.exe")
        
        # Güncellemeyi çıkar
        print("📦 Güncelleme açılıyor...")
        with zipfile.ZipFile(update_file, 'r') as zip_ref:
            zip_ref.extractall(".")
        
        # Eski dosyaları temizle
        os.remove(update_file)
        
        # Sistemi yeniden başlat
        print("🚀 Sistem yeniden başlatılıyor...")
        os.system("start MASTER_BASLATICI.bat")
        
        print(f"✅ Sistem {latest_version} sürümüne güncellendi")
        return True
        
    except Exception as e:
        print(f"❌ Güncelleme başarısız: {e}")
        return False

# update_info = check_updates()
# if update_info and update_info.get('update_available'):
#     auto_update(update_info)
```

---

## 📊 İZLEME VE RAPORLAMA

### Performans İzleme

#### 📈 Gerçek Zamanlı İzleme
```python
import psutil
import time
import json
from datetime import datetime

class PerformanceMonitor:
    def __init__(self):
        self.metrics = []
        self.monitoring = False
    
    def collect_metrics(self):
        metrics = {
            'timestamp': datetime.now().isoformat(),
            'cpu': psutil.cpu_percent(interval=1),
            'memory': psutil.virtual_memory().percent,
            'disk': psutil.disk_usage('/').percent,
            'network_sent': psutil.net_io_counters().bytes_sent,
            'network_recv': psutil.net_io_counters().bytes_recv,
            'processes': len(psutil.pids())
        }
        
        self.metrics.append(metrics)
        
        # Son 1000 kaydı tut
        if len(self.metrics) > 1000:
            self.metrics.pop(0)
        
        return metrics
    
    def save_metrics(self):
        with open('performance_metrics.json', 'w') as f:
            json.dump(self.metrics, f, indent=2, default=str)
    
    def generate_report(self):
        if not self.metrics:
            return None
        
        # Son 24 saatin metriklerini al
        cutoff_time = datetime.now() - timedelta(hours=24)
        recent_metrics = [m for m in self.metrics 
                        if datetime.fromisoformat(m['timestamp']) > cutoff_time]
        
        if not recent_metrics:
            return None
        
        # İstatistikleri hesapla
        avg_cpu = sum(m['cpu'] for m in recent_metrics) / len(recent_metrics)
        avg_memory = sum(m['memory'] for m in recent_metrics) / len(recent_metrics)
        max_cpu = max(m['cpu'] for m in recent_metrics)
        max_memory = max(m['memory'] for m in recent_metrics)
        
        report = {
            'period': 'Son 24 saat',
            'avg_cpu': avg_cpu,
            'avg_memory': avg_memory,
            'max_cpu': max_cpu,
            'max_memory': max_memory,
            'data_points': len(recent_metrics),
            'generated_at': datetime.now().isoformat()
        }
        
        return report
    
    def run_monitoring(self):
        self.monitoring = True
        
        while self.monitoring:
            metrics = self.collect_metrics()
            
            # Her saat bir rapor oluştur
            if datetime.now().minute == 0:
                report = self.generate_report()
                if report:
                    print(f"📊 Saatlik rapor: CPU {report['avg_cpu']:.1f}%, Bellek {report['avg_memory']:.1f}%")
            
            # Her 10 dakikada bir metrikleri kaydet
            if datetime.now().minute % 10 == 0:
                self.save_metrics()
            
            time.sleep(60)  # Her dakika

# monitor = PerformanceMonitor()
# monitor.run_monitoring()
```

#### 📊 Rapor Oluşturma
```python
import matplotlib.pyplot as plt
import json
from datetime import datetime

def generate_performance_report():
    # Metrikleri yükle
    with open('performance_metrics.json', 'r') as f:
        metrics = json.load(f)
    
    if not metrics:
        print("❌ Performans verisi bulunamadı")
        return
    
    # Rapor oluştur
    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    fig.suptitle('TRM Full Otomasyon Sistemi - Performans Raporu', fontsize=16)
    
    timestamps = [datetime.fromisoformat(m['timestamp']) for m in metrics]
    
    # CPU grafiği
    cpu_data = [m['cpu'] for m in metrics]
    axes[0, 0].plot(timestamps, cpu_data, color='red', linewidth=2)
    axes[0, 0].set_title('CPU Kullanımı (%)')
    axes[0, 0].set_ylim(0, 100)
    axes[0, 0].grid(True, alpha=0.3)
    
    # Bellek grafiği
    memory_data = [m['memory'] for m in metrics]
    axes[0, 1].plot(timestamps, memory_data, color='blue', linewidth=2)
    axes[0, 1].set_title('Bellek Kullanımı (%)')
    axes[0, 1].set_ylim(0, 100)
    axes[0, 1].grid(True, alpha=0.3)
    
    # Disk grafiği
    disk_data = [m['disk'] for m in metrics]
    axes[1, 0].plot(timestamps, disk_data, color='green', linewidth=2)
    axes[1, 0].set_title('Disk Kullanımı (%)')
    axes[1, 0].set_ylim(0, 100)
    axes[1, 0].grid(True, alpha=0.3)
    
    # Process grafiği
    process_data = [m['processes'] for m in metrics]
    axes[1, 1].plot(timestamps, process_data, color='purple', linewidth=2)
    axes[1, 1].set_title('Aktif Process Sayısı')
    axes[1, 1].grid(True, alpha=0.3)
    
    # Grafikleri kaydet
    plt.tight_layout()
    report_file = f'performance_report_{datetime.now().strftime("%Y%m%d_%H%M%S")}.png'
    plt.savefig(report_file, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"📊 Performans raporu oluşturuldu: {report_file}")
    
    return report_file

# generate_performance_report()
```

---

## 📋 BAKIM KONTROL LİSTESİ

### Günlük Kontrol
- [ ] Sistem durumu normal
- [ ] Paneller erişilebilir
- [ ] API yanıtları doğru
- [ ] Log dosyaları temiz
- [ ] Performans metrikleri iyi
- [ ] Hata sayısı < 5
- [ ] Yedekleme tamamlandı

### Haftalık Kontrol
- [ ] Log temizleme yapıldı
- [ ] Veri tabanı optimize edildi
- [ ] Disk alanı kontrol edildi
- [ ] Güncelleme kontrolü yapıldı
- [ ] Güvenlik taraması yapıldı
- [ ] Performans testleri çalıştırıldı
- [ ] Yedekleme doğrulandı

### Aylık Kontrol
- [ ] Tam sistem yedeği alındı
- [ ] Python kütüphaneleri güncellendi
- [ ] Sistem ayarları gözden geçirildi
- [ ] Güvenlik duvarı kontrol edildi
- [ ] Port taraması yapıldı
- [ ] Sistem kaynakları optimize edildi
- [ ] Tüm fonksiyonlar test edildi

---

## 🚨 KRİTİK DURUMLAR

### Hata Kodları ve Çözümleri

#### 🚨 Kritik Hatalar
- **E001:** Bellek kullanımı > 95%
  - Çözüm: Sistemi yeniden başlat, gereksiz process'leri sonlandır
  
- **E002:** CPU kullanımı > 98%
  - Çözüm: Sistemi yeniden başlat, process'leri optimize et
  
- **E003:** Disk alanı < 5%
  - Çözüm: Eski dosyaları temizle, yedekleri dışarı aktar
  
- **E004:** Paneller erişilemiyor
  - Çözüm: Sistemi yeniden başlat, portları kontrol et
  
- **E005:** API anahtarları geçersiz
  - Çözüm: API anahtarlarını güncelle, servis sağlayıcıyı kontrol et

#### ⚠️ Uyarılar
- **W001:** Bellek kullanımı > 80%
  - Çözüm: Gereksiz sekmeleri kapat, belleği temizle
  
- **W002:** CPU kullanımı > 85%
  - Çözüm: Gereksiz programları kapat, işlemci yükünü azalt
  
- **W003:** Disk alanı < 15%
  - Çözüm: Eski logları temizle, temp dosyalarını boşalt

---

**TRM FULL OTOMASYON SİSTEMİ v3.0 - Sistem Bakım ve Optimizasyon Kılavuzu**

*Bu kılavuz ile sisteminizi her zaman en iyi performansta tutabilir ve olası sorunları önleyebilirsiniz.*
