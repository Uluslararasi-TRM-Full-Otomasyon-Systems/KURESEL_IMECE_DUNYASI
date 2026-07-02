import os
import sys
import sqlite3
import psutil
import platform
from datetime import datetime
import subprocess

# ============================================
# SISTEM SAGLIK KONTROLU
# ============================================

class HealthCheck:
    def __init__(self):
        self.status = {
            'tarih': datetime.now().strftime('%d.%m.%Y %H:%M:%S'),
            'durum': 'IYI',
            'kontroller': []
        }
    
    # ============================================
    # 1. DISK KONTROLU
    # ============================================
    def check_disk(self):
        """Disk kullanimini kontrol eder"""
        try:
            disk = psutil.disk_usage('/')
            free_gb = disk.free / (1024**3)
            total_gb = disk.total / (1024**3)
            percent_used = disk.percent
            
            result = {
                'kontrol': '💾 Disk',
                'durum': '✅ IYI' if percent_used < 90 else '⚠️ UYARI',
                'detay': f'{percent_used}% dolu ({free_gb:.1f} GB bos / {total_gb:.1f} GB toplam)'
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
    # 2. BELLEK KONTROLU
    # ============================================
    def check_memory(self):
        """RAM kullanimini kontrol eder"""
        try:
            memory = psutil.virtual_memory()
            percent_used = memory.percent
            available_gb = memory.available / (1024**3)
            
            result = {
                'kontrol': '🧠 Bellek',
                'durum': '✅ IYI' if percent_used < 85 else '⚠️ UYARI',
                'detay': f'{percent_used}% kullanim ({available_gb:.1f} GB bos)'
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
    # 3. ISLEMCI KONTROLU
    # ============================================
    def check_cpu(self):
        """CPU kullanimini kontrol eder"""
        try:
            cpu_percent = psutil.cpu_percent(interval=1)
            
            result = {
                'kontrol': '⚙️ Islemci',
                'durum': '✅ IYI' if cpu_percent < 80 else '⚠️ UYARI',
                'detay': f'{cpu_percent}% kullanim'
            }
            
            if cpu_percent >= 80:
                self.status['durum'] = 'UYARI'
            
            return result
        except Exception as e:
            return {
                'kontrol': '⚙️ Islemci',
                'durum': '❌ HATA',
                'detay': str(e)
            }
    
    # ============================================
    # 4. VERITABANI KONTROLU
    # ============================================
    def check_database(self):
        """Veritabani dosyalarini kontrol eder"""
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
                        'detay': 'Olusturulacak'
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
    # 5. PYTHON MODULLERI KONTROLU
    # ============================================
    def check_modules(self):
        """Gerekli Python modullerini kontrol eder"""
        required = ['telebot', 'dotenv', 'requests', 'schedule', 'psutil']
        results = []
        
        for module in required:
            try:
                __import__(module)
                results.append({
                    'kontrol': f'📦 {module}',
                    'durum': '✅ VAR',
                    'detay': 'Yuklu'
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
    # 6. INTERNET BAGLANTISI KONTROLU
    # ============================================
    def check_internet(self):
        """Internet baglantisini kontrol eder"""
        try:
            subprocess.run(['ping', '-n', '1', '8.8.8.8'], 
                         capture_output=True, timeout=5)
            return {
                'kontrol': '🌐 Internet',
                'durum': '✅ BAGLI',
                'detay': 'Baglanti var'
            }
        except:
            return {
                'kontrol': '🌐 Internet',
                'durum': '❌ YOK',
                'detay': 'Baglanti kontrolu basarisiz'
            }
    
    # ============================================
    # 7. SISTEM BILGISI
    # ============================================
    def system_info(self):
        """Sistem bilgilerini gosterir"""
        return {
            'kontrol': '🖥️ Sistem',
            'durum': 'ℹ️ BILGI',
            'detay': f'{platform.system()} {platform.release()}'
        }
    
    # ============================================
    # 8. TUM KONTROLLERI CALISTIR
    # ============================================
    def run_all_checks(self):
        """Tum saglik kontrollerini calistirir"""
        
        print("\n" + "="*70)
        print("🏥 SISTEM SAGLIK KONTROLU")
        print("="*70)
        print(f"📅 Tarih: {self.status['tarih']}")
        print("="*70)
        
        # Temel kontroller
        self.status['kontroller'].append(self.system_info())
        self.status['kontroller'].append(self.check_internet())
        self.status['kontroller'].append(self.check_disk())
        self.status['kontroller'].append(self.check_memory())
        self.status['kontroller'].append(self.check_cpu())
        
        # Veritabani kontrolleri
        for result in self.check_database():
            self.status['kontroller'].append(result)
        
        # Modul kontrolleri
        for result in self.check_modules():
            self.status['kontroller'].append(result)
        
        # Sonuclari goster
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
        """Saglik raporunu dosyaya kaydeder"""
        filename = f"health_report_{datetime.now().strftime('%Y%m%d_%H%M')}.txt"
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("="*70 + "\n")
            f.write("🏥 SISTEM SAGLIK RAPORU\n")
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
    print("🚀 SAGLIK KONTROL SISTEMI BASLATILIYOR...")
    
    health = HealthCheck()
    
    while True:
        print("\n1️⃣ Tum kontrolleri calistir")
        print("2️⃣ Disk kontrolu")
        print("3️⃣ Bellek kontrolu")
        print("4️⃣ Veritabani kontrolu")
        print("5️⃣ Modul kontrolu")
        print("6️⃣ Raporlari listele")
        print("7️⃣ Otomatik kontrol (10 saniyede bir)")
        print("8️⃣ Cikis")
        
        choice = input("\nSeciminiz: ")
        
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
                print("\n📋 SAGLIK RAPORLARI:")
                for r in sorted(reports, reverse=True)[:10]:
                    size = os.path.getsize(r) / 1024
                    print(f"   📄 {r} ({size:.1f} KB)")
            else:
                print("❌ Henuz rapor yok!")
        
        elif choice == '7':
            print("🔄 Otomatik kontrol baslatiliyor (10 saniyede bir)...")
            print("   Durdurmak icin CTRL+C")
            try:
                while True:
                    import time
                    health.run_all_checks()
                    print("\n⏰ 10 saniye bekleniyor...")
                    time.sleep(10)
            except KeyboardInterrupt:
                print("\n🛑 Otomatik kontrol durduruldu.")
        
        elif choice == '8':
            print("👋 Saglikli gunler!")
            break
