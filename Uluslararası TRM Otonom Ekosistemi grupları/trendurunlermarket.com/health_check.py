import os
import sys
import sqlite3
import psutil
import platform
from datetime import datetime
import subprocess

# ============================================
# SİSTEM SAĞLIK KONTROLÜ
# ============================================

class HealthCheck:
    def __init__(self):
        self.status = {
            'tarih': datetime.now().strftime('%d.%m.%Y %H:%M:%S'),
            'durum': 'İYİ',
            'kontroller': []
        }
    
    # ============================================
    # 1. DİSK KONTROLÜ
    # ============================================
    def check_disk(self):
        """Disk kullanımını kontrol eder"""
        try:
            disk = psutil.disk_usage('/')
            free_gb = disk.free / (1024**3)
            total_gb = disk.total / (1024**3)
            percent_used = disk.percent
            
            result = {
                'kontrol': '💾 Disk',
                'durum': '✅ İYİ' if percent_used < 90 else '⚠️ UYARI',
                'detay': f'{percent_used}% dolu ({free_gb:.1f} GB boş / {total_gb:.1f} GB toplam)'
            }
            
            if percent_used >= 90:
                self.status['durum'] = 'UYARI'
            
            return result
        except Exception as e:
            return {
                'kontrol': '💾 Disk',
                'durum': '❌ HATA',
                'detay': str(e)
            }
    
    # ============================================
    # 2. BELLEK KONTROLÜ
    # ============================================
    def check_memory(self):
        """RAM kullanımını kontrol eder"""
        try:
            memory = psutil.virtual_memory()
            percent_used = memory.percent
            available_gb = memory.available / (1024**3)
            
            result = {
                'kontrol': '🧠 Bellek',
                'durum': '✅ İYİ' if percent_used < 85 else '⚠️ UYARI',
                'detay': f'{percent_used}% kullanım ({available_gb:.1f} GB boş)'
            }
            
            if percent_used >= 85:
                self.status['durum'] = 'UYARI'
            
            return result
        except Exception as e:
            return {
                'kontrol': '🧠 Bellek',
                'durum': '❌ HATA',
                'detay': str(e)
            }
    
    # ============================================
    # 3. İŞLEMCİ KONTROLÜ
    # ============================================
    def check_cpu(self):
        """CPU kullanımını kontrol eder"""
        try:
            cpu_percent = psutil.cpu_percent(interval=1)
            
            result = {
                'kontrol': '⚙️ İşlemci',
                'durum': '✅ İYİ' if cpu_percent < 80 else '⚠️ UYARI',
                'detay': f'{cpu_percent}% kullanım'
            }
            
            if cpu_percent >= 80:
                self.status['durum'] = 'UYARI'
            
            return result
        except Exception as e:
            return {
                'kontrol': '⚙️ İşlemci',
                'durum': '❌ HATA',
                'detay': str(e)
            }
    
    # ============================================
    # 4. VERİTABANI KONTROLÜ
    # ============================================
    def check_database(self):
        """Veritabanı dosyalarını kontrol eder"""
        dbs = ['sales.db', 'team_list.csv']
        results = []
        
        for db in dbs:
            try:
                if os.path.exists(db):
                    size = os.path.getsize(db) / 1024  # KB
                    results.append({
                        'kontrol': f'🗄️ {db}',
                        'durum': '✅ VAR',
                        'detay': f'{size:.1f} KB'
                    })
                else:
                    results.append({
                        'kontrol': f'🗄️ {db}',
                        'durum': '⚠️ YOK',
                        'detay': 'Oluşturulacak'
                    })
                    self.status['durum'] = 'UYARI'
            except Exception as e:
                results.append({
                    'kontrol': f'🗄️ {db}',
                    'durum': '❌ HATA',
                    'detay': str(e)
                })
        
        return results
    
    # ============================================
    # 5. PYTHON MODÜLLERİ KONTROLÜ
    # ============================================
    def check_modules(self):
        """Gerekli Python modüllerini kontrol eder"""
        required = ['telebot', 'dotenv', 'requests', 'schedule', 'psutil']
        results = []
        
        for module in required:
            try:
                __import__(module)
                results.append({
                    'kontrol': f'📦 {module}',
                    'durum': '✅ VAR',
                    'detay': 'Yüklü'
                })
            except ImportError:
                results.append({
                    'kontrol': f'📦 {module}',
                    'durum': '❌ YOK',
                    'detay': 'pip install ile kur'
                })
                self.status['durum'] = 'HATA'
        
        return results
    
    # ============================================
    # 6. İNTERNET BAĞLANTISI KONTROLÜ
    # ============================================
    def check_internet(self):
        """İnternet bağlantısını kontrol eder"""
        try:
            subprocess.run(['ping', '-n', '1', '8.8.8.8'], 
                         capture_output=True, timeout=5)
            return {
                'kontrol': '🌐 İnternet',
                'durum': '✅ BAĞLI',
                'detay': 'Bağlantı var'
            }
        except:
            return {
                'kontrol': '🌐 İnternet',
                'durum': '❌ YOK',
                'detay': 'Bağlantı kontrolü başarısız'
            }
    
    # ============================================
    # 7. SİSTEM BİLGİSİ
    # ============================================
    def system_info(self):
        """Sistem bilgilerini gösterir"""
        return {
            'kontrol': '🖥️ Sistem',
            'durum': 'ℹ️ BİLGİ',
            'detay': f'{platform.system()} {platform.release()}'
        }
    
    # ============================================
    # 8. TÜM KONTROLLERİ ÇALIŞTIR
    # ============================================
    def run_all_checks(self):
        """Tüm sağlık kontrollerini çalıştırır"""
        
        print("\n" + "="*70)
        print("🏥 SİSTEM SAĞLIK KONTROLÜ")
        print("="*70)
        print(f"📅 Tarih: {self.status['tarih']}")
        print("="*70)
        
        # Temel kontroller
        self.status['kontroller'].append(self.system_info())
        self.status['kontroller'].append(self.check_internet())
        self.status['kontroller'].append(self.check_disk())
        self.status['kontroller'].append(self.check_memory())
        self.status['kontroller'].append(self.check_cpu())
        
        # Veritabanı kontrolleri
        for result in self.check_database():
            self.status['kontroller'].append(result)
        
        # Modül kontrolleri
        for result in self.check_modules():
            self.status['kontroller'].append(result)
        
        # Sonuçları göster
        for kontrol in self.status['kontroller']:
            print(f"{kontrol['kontrol']}: {kontrol['durum']}")
            print(f"   📌 {kontrol['detay']}")
            print()
        
        print("="*70)
        print(f"📊 GENEL DURUM: {self.status['durum']}")
        print("="*70)
        
        # Raporu dosyaya kaydet
        self.save_report()
        
        return self.status
    
    # ============================================
    # 9. RAPORU KAYDET
    # ============================================
    def save_report(self):
        """Sağlık raporunu dosyaya kaydeder"""
        filename = f"health_report_{datetime.now().strftime('%Y%m%d_%H%M')}.txt"
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("="*70 + "\n")
            f.write("🏥 SİSTEM SAĞLIK RAPORU\n")
            f.write("="*70 + "\n")
            f.write(f"Tarih: {self.status['tarih']}\n")
            f.write("="*70 + "\n\n")
            
            for kontrol in self.status['kontroller']:
                f.write(f"{kontrol['kontrol']}: {kontrol['durum']}\n")
                f.write(f"   {kontrol['detay']}\n\n")
            
            f.write("="*70 + "\n")
            f.write(f"GENEL DURUM: {self.status['durum']}\n")
            f.write("="*70 + "\n")
        
        print(f"✅ Rapor kaydedildi: {filename}")
        return filename

# ============================================
# 10. ANA PROGRAM
# ============================================
if __name__ == "__main__":
    print("🚀 SAĞLIK KONTROL SİSTEMİ BAŞLATILIYOR...")
    
    health = HealthCheck()
    
    while True:
        print("\n1️⃣ Tüm kontrolleri çalıştır")
        print("2️⃣ Disk kontrolü")
        print("3️⃣ Bellek kontrolü")
        print("4️⃣ Veritabanı kontrolü")
        print("5️⃣ Modül kontrolü")
        print("6️⃣ Raporları listele")
        print("7️⃣ Otomatik kontrol (10 saniyede bir)")
        print("8️⃣ Çıkış")
        
        choice = input("\nSeçiminiz: ")
        
        if choice == '1':
            health.run_all_checks()
        
        elif choice == '2':
            print(health.check_disk())
        
        elif choice == '3':
            print(health.check_memory())
        
        elif choice == '4':
            for r in health.check_database():
                print(r)
        
        elif choice == '5':
            for r in health.check_modules():
                print(r)
        
        elif choice == '6':
            import glob
            reports = glob.glob("health_report_*.txt")
            if reports:
                print("\n📋 SAĞLIK RAPORLARI:")
                for r in sorted(reports, reverse=True)[:10]:
                    size = os.path.getsize(r) / 1024
                    print(f"   📄 {r} ({size:.1f} KB)")
            else:
                print("❌ Henüz rapor yok!")
        
        elif choice == '7':
            print("🔄 Otomatik kontrol başlatılıyor (10 saniyede bir)...")
            print("   Durdurmak için CTRL+C")
            try:
                while True:
                    import time
                    health.run_all_checks()
                    print("\n⏰ 10 saniye bekleniyor...")
                    time.sleep(10)
            except KeyboardInterrupt:
                print("\n🛑 Otomatik kontrol durduruldu.")
        
        elif choice == '8':
            print("👋 Sağlıklı günler!")
            break
