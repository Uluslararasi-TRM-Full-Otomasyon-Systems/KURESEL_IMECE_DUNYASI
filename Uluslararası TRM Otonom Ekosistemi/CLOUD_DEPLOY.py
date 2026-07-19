#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TRM Nirvana v3.0 - Cloud Deployment Manager
Bulut deployment için otomatik kurulum
"""

import os
import sys
import subprocess
import json
import time
from pathlib import Path

class CloudDeployer:
    def __init__(self):
        self.platforms = {
            'railway': {
                'name': 'Railway',
                'url': 'https://railway.app',
                'config': 'railway.yaml',
                'docker': 'Dockerfile',
                'install_cmd': 'npm install -g @railway/cli'
            },
            'render': {
                'name': 'Render',
                'url': 'https://render.com',
                'config': 'render.yaml',
                'docker': 'Dockerfile',
                'install_cmd': 'echo "Render web interface kullanılacak"'
            },
            'heroku': {
                'name': 'Heroku',
                'url': 'https://heroku.com',
                'config': 'Procfile',
                'docker': 'Dockerfile',
                'install_cmd': 'pip install heroku'
            }
        }
    
    def show_banner(self):
        """Başlık göster"""
        print("""
===============================================
    TRM NİRVANA v3.0 - CLOUD DEPLOYER
===============================================
  ☁️  Bulut deployment yöneticisi
  🚀 7/24 çalışmaya devam eder
  💾 Veri bulutta saklanır
  🔄 Otomatik yeniden başlar
===============================================
        """)
    
    def check_requirements(self):
        """Gereksinimleri kontrol et"""
        print("🔍 Deployment gereksinimleri kontrol ediliyor...")
        
        # Docker kontrol
        try:
            subprocess.run(['docker', '--version'], check=True, capture_output=True)
            print("✅ Docker mevcut")
        except:
            print("❌ Docker gerekli")
            print("📦 Kurulum: https://docs.docker.com/get-docker/")
            return False
        
        # Git kontrol
        try:
            subprocess.run(['git', '--version'], check=True, capture_output=True)
            print("✅ Git mevcut")
        except:
            print("❌ Git gerekli")
            print("📦 Kurulum: https://git-scm.com/downloads")
            return False
        
        return True
    
    def create_docker_files(self):
        """Docker dosyalarını oluştur"""
        print("🐳 Docker dosyaları kontrol ediliyor...")
        
        required_files = [
            'Dockerfile',
            'docker-compose.yml',
            'docker_entrypoint.sh'
        ]
        
        for file_name in required_files:
            if not os.path.exists(file_name):
                print(f"❌ {file_name} eksik")
                return False
            print(f"✅ {file_name} mevcut")
        
        return True
    
    def create_procfile(self):
        """Heroku Procfile oluştur"""
        procfile_content = "web: python main_orchestrator.py\n"
        
        with open('Procfile', 'w', encoding='utf-8') as f:
            f.write(procfile_content)
        
        print("✅ Procfile oluşturuldu")
    
    def create_runtime_txt(self):
        """Python runtime dosyası oluştur"""
        runtime_content = "python-3.11.0\n"
        
        with open('runtime.txt', 'w', encoding='utf-8') as f:
            f.write(runtime_content)
        
        print("✅ runtime.txt oluşturuldu")
    
    def deploy_to_railway(self):
        """Railway'e deploy et"""
        print("🚂 Railway deployment başlatılıyor...")
        
        # Railway CLI kontrol
        try:
            subprocess.run(['railway', '--version'], check=True, capture_output=True)
        except:
            print("📦 Railway CLI kuruluyor...")
            subprocess.run(['npm', 'install', '-g', '@railway/cli'], check=True)
        
        # Login
        print("🔑 Railway login yapın...")
        subprocess.run(['railway', 'login'], check=True)
        
        # Deploy
        print("🚀 Railway'e deploy ediliyor...")
        subprocess.run(['railway', 'deploy'], check=True)
        
        print("✅ Railway deployment tamamlandı!")
        return True
    
    def deploy_to_render(self):
        """Render'a deploy et"""
        print("🎨 Render deployment başlatılıyor...")
        
        print("📝 Render web arayüzünü kullanın:")
        print("1. https://render.com adresine gidin")
        print("2. GitHub reposu oluşturun")
        print("3. Render'da 'New Web Service' seçin")
        print("4. Repoyu bağlayın")
        print("5. render.yaml konfigürasyonu otomatik kullanılacak")
        
        return True
    
    def deploy_to_heroku(self):
        """Heroku'ya deploy et"""
        print("🍃 Heroku deployment başlatılıyor...")
        
        # Heroku CLI kontrol
        try:
            subprocess.run(['heroku', '--version'], check=True, capture_output=True)
        except:
            print("📦 Heroku CLI kuruluyor...")
            subprocess.run(['pip', 'install', 'heroku'], check=True)
        
        # Heroku dosyalarını oluştur
        self.create_procfile()
        self.create_runtime_txt()
        
        # Login
        print("🔑 Heroku login yapın...")
        subprocess.run(['heroku', 'login'], check=True)
        
        # App oluştur
        app_name = f"trm-nirvana-{int(time.time())}"
        subprocess.run(['heroku', 'create', app_name], check=True)
        
        # Deploy
        print("🚀 Heroku'ya deploy ediliyor...")
        subprocess.run(['git', 'add', '.'])
        subprocess.run(['git', 'commit', '-m', 'TRM Nirvana Cloud Deployment'])
        subprocess.run(['git', 'push', 'heroku', 'main'], check=True)
        
        print("✅ Heroku deployment tamamlandı!")
        return True
    
    def deploy_docker_local(self):
        """Docker container'ı yerinde çalıştır"""
        print("🐳 Docker container başlatılıyor...")
        
        # Docker build
        print("📦 Docker image oluşturuluyor...")
        subprocess.run(['docker', 'build', '-t', 'trm-nirvana', '.'], check=True)
        
        # Container çalıştır
        print("🚀 Container başlatılıyor...")
        subprocess.run([
            'docker', 'run', '-d',
            '--name', 'trm-nirvana-cloud',
            '-p', '9000:9000',
            '--restart', 'unless-stopped',
            'trm-nirvana'
        ], check=True)
        
        print("✅ Docker container çalışıyor!")
        print("🌐 Panel: http://localhost:9000")
        return True
    
    def show_cloud_status(self):
        """Bulut durumunu göster"""
        print("☁️  Bulut deployment durumu:")
        print("=" * 50)
        
        # Container durum
        try:
            result = subprocess.run(['docker', 'ps'], capture_output=True, text=True)
            if 'trm-nirvana' in result.stdout:
                print("✅ Docker container: Çalışıyor")
            else:
                print("❌ Docker container: Çalışmıyor")
        except:
            print("❌ Docker kontrol edilemedi")
        
        print("\n📋 Cloud Platformları:")
        for key, platform in self.platforms.items():
            print(f"  • {platform['name']}: {platform['url']}")
        
        print("\n💡 Cloud Avantajları:")
        print("  ✅ 7/24 çalışma")
        print("  ✅ Otomatik yeniden başlatma")
        print("  ✅ Veri yedekleme")
        print("  ✅ Ölçeklenebilirlik")
        print("  ✅ Güvenlik")
    
    def main_menu(self):
        """Ana menü"""
        while True:
            print("\n🎯 DEPLOYMENT SEÇENEKLERİ:")
            print("=" * 40)
            print("1. 🐳 Docker Local (Test)")
            print("2. 🚂 Railway Cloud")
            print("3. 🎨 Render Cloud")
            print("4. 🍃 Heroku Cloud")
            print("5. 📊 Cloud Durumu")
            print("6. ❌ Çıkış")
            print("=" * 40)
            
            try:
                choice = input("\nSeçiminiz (1-6): ").strip()
                
                if choice == "1":
                    self.deploy_docker_local()
                elif choice == "2":
                    self.deploy_to_railway()
                elif choice == "3":
                    self.deploy_to_render()
                elif choice == "4":
                    self.deploy_to_heroku()
                elif choice == "5":
                    self.show_cloud_status()
                elif choice == "6":
                    print("👋 Çıkış yapılıyor...")
                    break
                else:
                    print("❌ Geçersiz seçenek!")
                    
            except KeyboardInterrupt:
                print("\n👋 İptal edildi")
                break
            except Exception as e:
                print(f"❌ Hata: {e}")
    
    def run(self):
        """Ana çalıştırıcı"""
        self.show_banner()
        
        # Gereksinimleri kontrol et
        if not self.check_requirements():
            input("Gereksinimleri karşılayıp tekrar deneyin. Enter'a basın...")
            return
        
        # Docker dosyalarını kontrol et
        if not self.create_docker_files():
            input("Docker dosyaları eksik. Enter'a basın...")
            return
        
        # Ana menü
        self.main_menu()

def main():
    """Ana fonksiyon"""
    deployer = CloudDeployer()
    
    try:
        deployer.run()
    except KeyboardInterrupt:
        print("\n👋 Cloud deployer durduruldu")
    except Exception as e:
        print(f"❌ Hata: {e}")
        input("Devam etmek için Enter'a basın...")

if __name__ == "__main__":
    main()
