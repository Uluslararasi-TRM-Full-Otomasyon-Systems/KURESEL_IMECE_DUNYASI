#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TRM Nirvana v3.0 - Cloud Deployment Manager
Bulut deployment icin otomatik kurulum
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
                'install_cmd': 'echo "Render web interface kullanilacak"'
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
        """Baslik goster"""
        print("""
===============================================
    TRM NIRVANA v3.0 - CLOUD DEPLOYER
===============================================
  ☁️  Bulut deployment yoneticisi
  🚀 7/24 calismaya devam eder
  💾 Veri bulutta saklanir
  🔄 Otomatik yeniden baslar
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
        """Docker dosyalarini olustur"""
        print("🐳 Docker dosyalari kontrol ediliyor...")
        
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
        """Heroku Procfile olustur"""
        procfile_content = "web: python main_orchestrator.py\n"
        
        with open('Procfile', 'w', encoding='utf-8') as f:
            f.write(procfile_content)
        
        print("✅ Procfile olusturuldu")
    
    def create_runtime_txt(self):
        """Python runtime dosyasi olustur"""
        runtime_content = "python-3.11.0\n"
        
        with open('runtime.txt', 'w', encoding='utf-8') as f:
            f.write(runtime_content)
        
        print("✅ runtime.txt olusturuldu")
    
    def deploy_to_railway(self):
        """Railway'e deploy et"""
        print("🚂 Railway deployment baslatiliyor...")
        
        # Railway CLI kontrol
        try:
            subprocess.run(['railway', '--version'], check=True, capture_output=True)
        except:
            print("📦 Railway CLI kuruluyor...")
            subprocess.run(['npm', 'install', '-g', '@railway/cli'], check=True)
        
        # Login
        print("🔑 Railway login yapin...")
        subprocess.run(['railway', 'login'], check=True)
        
        # Deploy
        print("🚀 Railway'e deploy ediliyor...")
        subprocess.run(['railway', 'deploy'], check=True)
        
        print("✅ Railway deployment tamamlandi!")
        return True
    
    def deploy_to_render(self):
        """Render'a deploy et"""
        print("🎨 Render deployment baslatiliyor...")
        
        print("📝 Render web arayuzunu kullanin:")
        print("1. https://render.com adresine gidin")
        print("2. GitHub reposu olusturun")
        print("3. Render'da 'New Web Service' secin")
        print("4. Repoyu baglayin")
        print("5. render.yaml konfigurasyonu otomatik kullanilacak")
        
        return True
    
    def deploy_to_heroku(self):
        """Heroku'ya deploy et"""
        print("🍃 Heroku deployment baslatiliyor...")
        
        # Heroku CLI kontrol
        try:
            subprocess.run(['heroku', '--version'], check=True, capture_output=True)
        except:
            print("📦 Heroku CLI kuruluyor...")
            subprocess.run(['pip', 'install', 'heroku'], check=True)
        
        # Heroku dosyalarini olustur
        self.create_procfile()
        self.create_runtime_txt()
        
        # Login
        print("🔑 Heroku login yapin...")
        subprocess.run(['heroku', 'login'], check=True)
        
        # App olustur
        app_name = f"trm-nirvana-{int(time.time())}"
        subprocess.run(['heroku', 'create', app_name], check=True)
        
        # Deploy
        print("🚀 Heroku'ya deploy ediliyor...")
        subprocess.run(['git', 'add', '.'])
        subprocess.run(['git', 'commit', '-m', 'TRM Nirvana Cloud Deployment'])
        subprocess.run(['git', 'push', 'heroku', 'main'], check=True)
        
        print("✅ Heroku deployment tamamlandi!")
        return True
    
    def deploy_docker_local(self):
        """Docker container'i yerinde calistir"""
        print("🐳 Docker container baslatiliyor...")
        
        # Docker build
        print("📦 Docker image olusturuluyor...")
        subprocess.run(['docker', 'build', '-t', 'trm-nirvana', '.'], check=True)
        
        # Container calistir
        print("🚀 Container baslatiliyor...")
        subprocess.run([
            'docker', 'run', '-d',
            '--name', 'trm-nirvana-cloud',
            '-p', '9000:9000',
            '--restart', 'unless-stopped',
            'trm-nirvana'
        ], check=True)
        
        print("✅ Docker container calisiyor!")
        print("🌐 Panel: http://localhost:9000")
        return True
    
    def show_cloud_status(self):
        """Bulut durumunu goster"""
        print("☁️  Bulut deployment durumu:")
        print("=" * 50)
        
        # Container durum
        try:
            result = subprocess.run(['docker', 'ps'], capture_output=True, text=True)
            if 'trm-nirvana' in result.stdout:
                print("✅ Docker container: Calisiyor")
            else:
                print("❌ Docker container: Calismiyor")
        except:
            print("❌ Docker kontrol edilemedi")
        
        print("\n📋 Cloud Platformlari:")
        for key, platform in self.platforms.items():
            print(f"  • {platform['name']}: {platform['url']}")
        
        print("\n💡 Cloud Avantajlari:")
        print("  ✅ 7/24 calisma")
        print("  ✅ Otomatik yeniden baslatma")
        print("  ✅ Veri yedekleme")
        print("  ✅ Olceklenebilirlik")
        print("  ✅ Guvenlik")
    
    def main_menu(self):
        """Ana menu"""
        while True:
            print("\n🎯 DEPLOYMENT SECENEKLERI:")
            print("=" * 40)
            print("1. 🐳 Docker Local (Test)")
            print("2. 🚂 Railway Cloud")
            print("3. 🎨 Render Cloud")
            print("4. 🍃 Heroku Cloud")
            print("5. 📊 Cloud Durumu")
            print("6. ❌ Cikis")
            print("=" * 40)
            
            try:
                choice = input("\nSeciminiz (1-6): ").strip()
                
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
                    print("👋 Cikis yapiliyor...")
                    break
                else:
                    print("❌ Gecersiz secenek!")
                    
            except KeyboardInterrupt:
                print("\n👋 Iptal edildi")
                break
            except Exception as e:
                print(f"❌ Hata: {e}")
    
    def run(self):
        """Ana calistirici"""
        self.show_banner()
        
        # Gereksinimleri kontrol et
        if not self.check_requirements():
            input("Gereksinimleri karsilayip tekrar deneyin. Enter'a basin...")
            return
        
        # Docker dosyalarini kontrol et
        if not self.create_docker_files():
            input("Docker dosyalari eksik. Enter'a basin...")
            return
        
        # Ana menu
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
        input("Devam etmek icin Enter'a basin...")

if __name__ == "__main__":
    main()
