#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TRM FULL OTOMASYON - GOOGLE DRIVE - FLASH BELLEK SENKRONIZASYONU
Google Drive'daki Uluslararasi-TRM-Full-Otomasyon-Sistemi klasorunu 
flash bellekteki klasor ile bire bir eslestirir
"""

import os
import sys
import json
import logging
import hashlib
import shutil
import time
from datetime import datetime
from pathlib import Path
import requests
from typing import Dict, Any, List, Optional, Tuple

from trm_paths import flash_sync_root

# Google Drive API imports
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
from google.auth.transport.requests import Request
import io

# Loglama ayarlari
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('drive_flash_sync.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

class DriveFlashSync:
    def __init__(self):
        self.system_path = Path(__file__).parent
        self.secrets_file = self.system_path / "secrets.env"
        self.credentials_file = os.path.join(os.path.dirname(__file__), 'credentials.json')
        self.config = {}
        self.flash_path = flash_sync_root()
        self.drive_folder_id = None
        self.drive_service = None
        self.sync_stats = {
            "files_in_flash": 0,
            "files_in_drive": 0,
            "files_to_upload": 0,
            "files_to_download": 0,
            "conflicts": 0,
            "sync_time": None
        }
        
    def load_config(self):
        """Yapilandirma dosyasini yukler"""
        try:
            with open(self.secrets_file, 'r', encoding='utf-8') as f:
                for line in f:
                    if '=' in line and not line.startswith('#'):
                        key, value = line.strip().split('=', 1)
                        self.config[key.strip()] = value.strip()
            
            logger.info("✅ Drive-Flash senkronizasyon yapilandirmasi yuklendi")
            return True
            
        except Exception as e:
            logger.error(f"❌ Yapilandirma yuklenemedi: {e}")
            return False
            
    def get_file_hash(self, file_path: Path) -> str:
        """Dosya hash'ini hesapla"""
        try:
            with open(file_path, 'rb') as f:
                return hashlib.md5(f.read()).hexdigest()
        except Exception as e:
            logger.error(f"❌ Hash hesaplanamadi {file_path}: {e}")
            return ""
            
    def get_flash_files(self) -> Dict[str, Dict[str, Any]]:
        """Flash bellekteki dosyalari listele"""
        files = {}
        
        if not self.flash_path.exists():
            logger.error(f"❌ Flash bellek yolu bulunamadi: {self.flash_path}")
            return files
            
        try:
            for file_path in self.flash_path.rglob('*'):
                if file_path.is_file():
                    relative_path = file_path.relative_to(self.flash_path)
                    file_size = file_path.stat().st_size
                    file_hash = self.get_file_hash(file_path)
                    
                    files[str(relative_path)] = {
                        "path": str(file_path),
                        "relative_path": str(relative_path),
                        "size": file_size,
                        "hash": file_hash,
                        "modified": datetime.fromtimestamp(file_path.stat().st_mtime).isoformat(),
                        "location": "flash"
                    }
                    
            logger.info(f"✅ Flash bellekte {len(files)} dosya bulundu")
            
        except Exception as e:
            logger.error(f"❌ Flash bellek dosyalari okunamadi: {e}")
            
        return files
        
    def authenticate_google_drive(self):
        """Google Drive API'ye kimlik dogrula - Basit API key approach"""
        try:
            # Check if we have API keys in config
            if not self.load_config():
                return False
                
            # Try using API key approach first
            api_key = self.config.get('GOOGLE_DRIVE_API_KEY')
            if api_key and api_key != 'your_google_drive_api_key_here':
                # Build service with API key
                from googleapiclient.discovery import build
                self.drive_service = build('drive', 'v3', developerKey=api_key)
                logger.info("✅ Google Drive API key ile baglanti basarili")
                return True
            
            # Try service account with simplified credentials
            if os.path.exists(self.credentials_file):
                try:
                    # Create minimal service account info
                    service_account_info = {
                        "type": "service_account",
                        "project_id": "trm-full-otomasyon-sistemi",
                        "private_key_id": "c340c3e5202249bcda2080c66db1d3eabe033546",
                        "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQDILLETEFHtMebB\nunakgXV0gZQQSYfAUK2rrdtFLgyH2UQ/VgO6p2WvWwpoW11kyMvLMe7rTG5qPPwx\nPphCgYx9nwNN2vhXYfst8WBaSvRaagOOlF7x/7hIslvPdwv3FV14IFx5laxD1Fs1\nwS8so8x4T7ngjHHIuxOQbFXrcpngBnVr5nujMLh3awyFKNgUkTzppfo0q09tEpei\nmfnsREgfRpKZg6BfxXZN1tGp+d+3pl/UMjUxTRZFw8S8mVfATPaqWbZGS7Msj823\nbpD9sKaPluMD4LnKe/Moj4Inlb5af8TgEile8OmaGV9Onab2BHo7xLoLL4jnul/H\n8WUUX8zLAgMBAAECggEAJsSFDNihzUrXUpi+xpBuA4DfAKKFAIl/gRrcNxM6iQra\njVumwD0QU/xRUTG0rkK3OWSzzW1RixDBlPX2/hZh86hatvbcFuxafaTcUNBob6RN\niQ0SMFMiyS2F23HGZvWD0zKNRlzm7oIPoiMGdGJKxNhH+wWoOcSFfviEUWOyCnFN\nwbpum9CdFKYqNjxne1PPPvcfQOY5jsP2J5nuXFb2ncgi1taSJgJPw88Hq/CK2ggv\nIRxhzn3XS8TZe4ce6ou3oFwutz77c8n/g+Q5Io9eltVUf8P3bKFaiWVamy3q0npr\nKdBfh1mOkO/ITqtdfM0u8JHoSPAasbkGB5x4g/jELQKBgQD3JTBgNihFYn0Yx7Ef\nMfUaFX7SyBf5s1TJBeNZjfV8z8oEHEInGrT52+lmvAlwUZYandv5zatTMPgGODw7\nSbBUEl8kjxhFm9xnoc9N53q52dCrkNx+1KOwCGn4HxoeJHkPzjhqfGLjTQTjxPXJ\nCZa5L0gtpWC7+1U0qHU+MuWxfwKBgQDPWLBFeV9H52Rju48vVdoYTgoLj0cDxwry\nT4sm7uAdk5VaOIfGPqGURdIzEii7bPsel42WqxbMmVYKaCec7czYugx6ZCOr9CrJ\nDD0RHINz6VbGJVMhD5Xcd+p7sSi4Mc5SJ4MCpk6dHitHdhkYPW+GLeZzZAj/IObc\n1TDltvGytQKBgAGK2N9w1xV/xNoXvPI95JKyGaWFHCkxxlCu2blgWmzZ+x/FcWA/\nGWwJxE4g1EpAKBiobYwEjZIqVxHq3e1cy13q828N+Y/NpjV7XAjXbfuk8VlwwP+F\nnojPiCY9D2mzfu2Wu2slHV3Kls2ccfpAvoCItulyWkKD7s49tkbW+qZJPAoGASKaH\npOAhHX2bNEK8qdZIA6ocZO5/8Hfmgv6SAENErbhPZXxXPoQlc2F/hDuBoCJQXui1\nSKyL4YZ8mkriTl8YHnwZ8SxzP0XfU/CA2SUHfi6tI+JiHTxrwwMVWt+5J8jzxN9p\nTR1egDjY60IbCt5D3Fzq2VWcvWAW5Bui9WpDh90CgYEAhTN64jD22PdS6VUsl2WT\nSUMpre2YhEhCwKdi3Z/WlBIhB0xslx/iSoV8SKK4k7hAp7XQsSpsAhWjsODKrd/M\nKyqLYi5ATnqi9hYXz/brVWAwMeOpV4fY4CZtMkOEaC8J0tHtbS51qZMtJEe6h9CR\nfZQg1uteOBVuAvGHCUp16Ao=\n-----END PRIVATE KEY-----\n",
                        "client_email": "trm-full-otomasyon-sistemi@trm-full-otomasyon-sistemi.iam.gserviceaccount.com",
                        "client_id": "112722806951435041982",
                        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                        "token_uri": "https://oauth2.googleapis.com/token",
                        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
                        "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/trm-full-otomasyon-sistemi%40trm-full-otomasyon-sistemi.iam.gserviceaccount.com"
                    }
                    
                    credentials = service_account.Credentials.from_service_account_info(
                        service_account_info,
                        scopes=['https://www.googleapis.com/auth/drive']
                    )
                    
                    self.drive_service = build('drive', 'v3', credentials=credentials)
                    logger.info("✅ Google Drive kimlik dogrulamasi basarili (Service Account)")
                    return True
                    
                except Exception as sa_error:
                    logger.warning(f"⚠️ Service account denemesi basarisiz: {sa_error}")
            
            # If all else fails, create a mock service for testing
            logger.warning("⚠️ Gercek Google Drive baglantisi kurulamadi, test modu aktif")
            self.drive_service = None  # Will trigger fallback behavior
            return False
            
        except Exception as e:
            logger.error(f"❌ Google Drive kimlik dogrulamasi basarisiz: {e}")
            return False
            
    def get_or_create_drive_folder(self):
        """Drive'da klasor bul veya olustur"""
        try:
            # Klasoru ara
            results = self.drive_service.files().list(
                q="name='Uluslararasi-TRM-Full-Otomasyon-Sistemi' and mimeType='application/vnd.google-apps.folder'",
                fields="files(id, name)"
            ).execute()
            
            folders = results.get('files', [])
            
            if folders:
                self.drive_folder_id = folders[0]['id']
                logger.info(f"✅ Mevcut Drive klasoru bulundu: {self.drive_folder_id}")
            else:
                # Yeni klasor olustur
                folder_metadata = {
                    'name': 'Uluslararasi-TRM-Full-Otomasyon-Sistemi',
                    'mimeType': 'application/vnd.google-apps.folder'
                }
                
                folder = self.drive_service.files().create(
                    body=folder_metadata,
                    fields='id'
                ).execute()
                
                self.drive_folder_id = folder.get('id')
                logger.info(f"✅ Yeni Drive klasoru olusturuldu: {self.drive_folder_id}")
                
            return True
            
        except Exception as e:
            logger.error(f"❌ Drive klasor islemi basarisiz: {e}")
            return False
        
    def get_drive_files(self) -> Dict[str, Dict[str, Any]]:
        """Google Drive'daki dosyalari listele"""
        files = {}
        
        if not self.drive_service:
            logger.error("❌ Google Drive service hazir degil")
            return files
            
        if not self.drive_folder_id:
            if not self.get_or_create_drive_folder():
                return files
                
        try:
            # Drive'daki tum dosyalari listele
            results = self.drive_service.files().list(
                q=f"' {self.drive_folder_id}' in parents and trashed=false",
                fields="files(id, name, size, modifiedTime, md5Checksum)"
            ).execute()
            
            drive_files = results.get('files', [])
            
            for file in drive_files:
                relative_path = file['name']
                file_size = int(file.get('size', 0))
                file_hash = file.get('md5Checksum', '')
                modified_time = file.get('modifiedTime', '')
                
                files[relative_path] = {
                    "path": f"drive://Uluslararasi-TRM-Full-Otomasyon-Sistemi/{relative_path}",
                    "relative_path": relative_path,
                    "size": file_size,
                    "hash": file_hash,
                    "modified": modified_time,
                    "location": "drive",
                    "drive_id": file['id']
                }
                
            logger.info(f"✅ Google Drive'da {len(files)} dosya bulundu")
            
        except Exception as e:
            logger.error(f"❌ Google Drive dosyalari okunamadi: {e}")
            
        return files
        
    def compare_files(self, flash_files: Dict[str, Dict[str, Any]], drive_files: Dict[str, Dict[str, Any]]) -> Dict[str, List[str]]:
        """Dosyalari karsilastir ve senkronizasyon plani olustur"""
        comparison = {
            "upload_to_drive": [],  # Flash'ta olan Drive'da olmayanlar
            "download_to_flash": [],  # Drive'da olan flash'ta olmayanlar
            "conflicts": [],  # Her ikisinde de olan ama farkli olanlar
            "identical": []  # Her ikisinde de ayni olanlar
        }
        
        flash_paths = set(flash_files.keys())
        drive_paths = set(drive_files.keys())
        
        # Flash'ta olan Drive'da olmayanlar (yuklenecek)
        upload_candidates = flash_paths - drive_paths
        for path in upload_candidates:
            if not self.should_ignore_file(path):
                comparison["upload_to_drive"].append(path)
                
        # Drive'da olan flash'ta olmayanlar (indirilecek)
        download_candidates = drive_paths - flash_paths
        for path in download_candidates:
            if not self.should_ignore_file(path):
                comparison["download_to_flash"].append(path)
                
        # Her ikisinde de olanlar
        common_files = flash_paths & drive_paths
        for path in common_files:
            flash_file = flash_files[path]
            drive_file = drive_files[path]
            
            if flash_file["hash"] != drive_file["hash"]:
                comparison["conflicts"].append(path)
            else:
                comparison["identical"].append(path)
                
        # Istatistikleri guncelle
        self.sync_stats.update({
            "files_in_flash": len(flash_files),
            "files_in_drive": len(drive_files),
            "files_to_upload": len(comparison["upload_to_drive"]),
            "files_to_download": len(comparison["download_to_flash"]),
            "conflicts": len(comparison["conflicts"]),
            "sync_time": datetime.now().isoformat()
        })
        
        return comparison
        
    def should_ignore_file(self, file_path: str) -> bool:
        """Dosyanin senkronizasyon disi kalip kalmayacagini kontrol et"""
        ignore_patterns = [
            "*.log", "*.tmp", "*.bak", "*.cache", "*.old",
            "__pycache__", ".git", "node_modules", ".DS_Store",
            "Thumbs.db", "desktop.ini"
        ]
        
        for pattern in ignore_patterns:
            if pattern.replace("*", "") in file_path:
                return True
                
        return False
        
    def upload_to_drive(self, file_path: str):
        """Dosyayi Google Drive'a yukle"""
        try:
            if not self.drive_service or not self.drive_folder_id:
                logger.error("❌ Google Drive service hazir degil")
                return False
                
            full_path = self.flash_path / file_path
            if not full_path.exists():
                logger.error(f"❌ Dosya bulunamadi: {full_path}")
                return False
                
            logger.info(f"📤 Google Drive'a yukleniyor: {file_path}")
            
            # Media metadata
            media = MediaFileUpload(str(full_path), resumable=True)
            
            # File metadata
            file_metadata = {
                'name': file_path,
                'parents': [self.drive_folder_id]
            }
            
            # Upload file
            file = self.drive_service.files().create(
                body=file_metadata,
                media_body=media,
                fields='id'
            ).execute()
            
            logger.info(f"✅ Yuklendi: {file_path} (ID: {file.get('id')})")
            return True
            
        except Exception as e:
            logger.error(f"❌ Yukleme basarisiz {file_path}: {e}")
            return False
            
    def download_from_drive(self, file_path: str):
        """Dosyayi Google Drive'dan indir"""
        try:
            if not self.drive_service:
                logger.error("❌ Google Drive service hazir degil")
                return False
                
            # Drive'daki dosyayi bul
            results = self.drive_service.files().list(
                q="name='{}' and '{}' in parents and trashed=false".format(
                    file_path.replace("'", "\\'"), self.drive_folder_id
                ),
                fields="files(id, name)"
            ).execute()
            
            files = results.get('files', [])
            
            if not files:
                logger.error(f"❌ Drive'da dosya bulunamadi: {file_path}")
                return False
                
            drive_file_id = files[0]['id']
            
            logger.info(f"📥 Google Drive'dan indiriliyor: {file_path}")
            
            # Hedef dosya yolu
            full_path = self.flash_path / file_path
            full_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Download request
            request = self.drive_service.files().get_media(fileId=drive_file_id)
            
            # File write
            with open(full_path, 'wb') as f:
                downloader = MediaIoBaseDownload(f, request)
                done = False
                while done is False:
                    status, done = downloader.next_chunk()
                    
            logger.info(f"✅ Indirildi: {file_path}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Indirme basarisiz {file_path}: {e}")
            return False
            
    def resolve_conflict(self, file_path: str, flash_files: Dict[str, Dict[str, Any]], drive_files: Dict[str, Dict[str, Any]]):
        """Dosya cakismasini coz"""
        flash_file = flash_files[file_path]
        drive_file = drive_files[file_path]
        
        flash_modified = datetime.fromisoformat(flash_file["modified"])
        drive_modified = datetime.fromisoformat(drive_file["modified"])
        
        logger.warning(f"⚠️ Cakisma: {file_path}")
        logger.info(f"  Flash: {flash_modified}")
        logger.info(f"  Drive: {drive_modified}")
        
        # En yeni olani kullan
        if flash_modified > drive_modified:
            logger.info(f"  → Flash surumu daha yeni, Drive'a yukleniyor")
            return self.upload_to_drive(file_path)
        else:
            logger.info(f"  → Drive surumu daha yeni, Flash'a indiriliyor")
            return self.download_from_drive(file_path)
            
    def sync_files(self, comparison: Dict[str, List[str]], flash_files: Dict[str, Dict[str, Any]], drive_files: Dict[str, Dict[str, Any]]):
        """Dosyalari senkronize et"""
        logger.info("🔄 Dosya senkronizasyonu baslatiliyor...")
        
        success_count = 0
        total_operations = (
            len(comparison["upload_to_drive"]) + 
            len(comparison["download_to_flash"]) + 
            len(comparison["conflicts"])
        )
        
        # Flash'tan Drive'a yukle
        for file_path in comparison["upload_to_drive"]:
            if self.upload_to_drive(file_path):
                success_count += 1
                
        # Drive'dan Flash'a indir
        for file_path in comparison["download_to_flash"]:
            if self.download_from_drive(file_path):
                success_count += 1
                
        # Cakismalari coz
        for file_path in comparison["conflicts"]:
            if self.resolve_conflict(file_path, flash_files, drive_files):
                success_count += 1
                
        logger.info(f"✅ Senkronizasyon tamamlandi: {success_count}/{total_operations} basarili")
        
        return success_count == total_operations
        
    def run_sync(self):
        """Tam senkronizasyon dongusunu calistir"""
        logger.info("🚀 Google Drive - Flash Bellek Senkronizasyonu Baslatiliyor")
        
        try:
            # 1. Yapilandirmayi yukle
            if not self.load_config():
                return False
                
            # 2. Google Drive kimlik dogrulamasi
            if not self.authenticate_google_drive():
                logger.error("❌ Google Drive baglantisi kurulamadi")
                return False
                
            # 3. Drive klasorunu bul/olustur
            if not self.get_or_create_drive_folder():
                return False
                
            # 4. Flash bellekteki dosyalari listele
            flash_files = self.get_flash_files()
            
            # 5. Google Drive'daki dosyalari listele
            drive_files = self.get_drive_files()
            
            # 6. Dosyalari karsilastir
            comparison = self.compare_files(flash_files, drive_files)
            
            # 7. Senkronizasyon raporu goster
            self.show_sync_report(comparison)
            
            # 8. Senkronizasyonu yap
            success = self.sync_files(comparison, flash_files, drive_files)
            
            if success:
                logger.info("🎉 Senkronizasyon basariyla tamamlandi!")
            else:
                logger.warning("⚠️ Senkronizasyon tam olarak tamamlanamadi")
                
            return success
            
        except Exception as e:
            logger.error(f"❌ Senkronizasyon hatasi: {e}")
            return False
            
    def show_sync_report(self, comparison: Dict[str, List[str]]):
        """Senkronizasyon raporu goster"""
        print(f"\n📊 SENKRONIZASYON RAPORU")
        print("=" * 50)
        print(f"📁 Flash Bellek: {self.sync_stats['files_in_flash']} dosya")
        print(f"☁️ Google Drive: {self.sync_stats['files_in_drive']} dosya")
        print(f"📤 Yuklenecek: {self.sync_stats['files_to_upload']} dosya")
        print(f"📥 Indirilecek: {self.sync_stats['files_to_download']} dosya")
        print(f"⚠️ Cakisan: {self.sync_stats['conflicts']} dosya")
        print(f"✅ Ayni: {len(comparison['identical'])} dosya")
        
        if comparison["upload_to_drive"]:
            print(f"\n📤 Drive'a Yuklenecek Dosyalar:")
            for file_path in comparison["upload_to_drive"][:5]:  # Ilk 5 dosya
                print(f"  • {file_path}")
            if len(comparison["upload_to_drive"]) > 5:
                print(f"  ... ve {len(comparison['upload_to_drive']) - 5} dosya daha")
                
        if comparison["download_to_flash"]:
            print(f"\n📥 Flash'a Indirilecek Dosyalar:")
            for file_path in comparison["download_to_flash"][:5]:  # Ilk 5 dosya
                print(f"  • {file_path}")
            if len(comparison["download_to_flash"]) > 5:
                print(f"  ... ve {len(comparison['download_to_flash']) - 5} dosya daha")
                
        if comparison["conflicts"]:
            print(f"\n⚠️ Cakisan Dosyalar:")
            for file_path in comparison["conflicts"]:
                print(f"  • {file_path}")
                
    def save_sync_report(self):
        """Senkronizasyon raporunu kaydet"""
        try:
            report = f"""
📊 GOOGLE DRIVE - FLASH BELLEK SENKRONIZASYON RAPORU
===============================================
📅 Rapor Tarihi: {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}

📈 ISTATISTIKLER:
• Flash Bellek: {self.sync_stats['files_in_flash']} dosya
• Google Drive: {self.sync_stats['files_in_drive']} dosya
• Yuklenecek: {self.sync_stats['files_to_upload']} dosya
• Indirilecek: {self.sync_stats['files_to_download']} dosya
• Cakisan: {self.sync_stats['conflicts']} dosya
• Senkronizasyon Zamani: {self.sync_stats['sync_time']}

🔄 SENKRONIZASYON PRENSIBI:
1. Flash bellekteki dosyalari tara
2. Google Drive'daki dosyalari listele
3. Dosyalari hash ile karsilastir
4. Eksik dosyalari senkronize et
5. Cakisan dosyalari coz (en yeni versiyon)
6. Basariyi raporla

📁 KLASOR YOLLARI:
• Flash Bellek: {self.flash_path}
• Google Drive: drive://Uluslararasi-TRM-Full-Otomasyon-Sistemi/

📞 DESTEK:
• Log dosyasi: drive_flash_sync.log
• Yapilandirma: secrets.env
• Durum kontrolu: --status parametresi
            """
            
            report_file = self.system_path / "drive_flash_sync_raporu.txt"
            with open(report_file, 'w', encoding='utf-8') as f:
                f.write(report)
                
            logger.info(f"✅ Rapor kaydedildi: {report_file}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Rapor kaydedilemedi: {e}")
            return False

def main():
    """Ana fonksiyon"""
    print(">> ULUSLARASI TRM FULL OTOMASYON - GOOGLE DRIVE FLASH SENKRONIZASYONU")
    print("Google Drive ve flash bellek klasorlerini bire bir eslestirir...")
    
    sync = DriveFlashSync()
    
    # Parametre kontrolu
    if len(sys.argv) > 1:
        if sys.argv[1] == "--status":
            # Yapilandirmayi yukle ve Google Drive baglantisi kur
            sync.load_config()
            sync.authenticate_google_drive()
            
            flash_files = sync.get_flash_files()
            drive_files = sync.get_drive_files()
            comparison = sync.compare_files(flash_files, drive_files)
            
            print(f"\n[STATUS] Senkronizasyon Durumu:")
            print(f"Flash: {sync.sync_stats['files_in_flash']} dosya")
            print(f"Drive: {sync.sync_stats['files_in_drive']} dosya")
            print(f"Yuklenecek: {sync.sync_stats['files_to_upload']}")
            print(f"Indirilecek: {sync.sync_stats['files_to_download']}")
            return
        elif sys.argv[1] == "--report":
            if sync.save_sync_report():
                print("✅ Senkronizasyon raporu olusturuldu!")
                print("📁 Dosya: drive_flash_sync_raporu.txt")
            else:
                print("❌ Rapor olusturulamadi!")
            return
        elif sys.argv[1] == "--dry-run":
            sync.load_config()
            flash_files = sync.get_flash_files()
            drive_files = sync.get_drive_files()
            comparison = sync.compare_files(flash_files, drive_files)
            sync.show_sync_report(comparison)
            print("\n⚠️ DRY RUN - Gercek senkronizasyon yapilmadi")
            return
    
    # Normal senkronizasyon
    if sync.run_sync():
        print("\n🎉 GOOGLE DRIVE - FLASH BELLEK SENKRONIZASYONU BASARILI!")
        print("📁 Tum dosyalar senkronize edildi")
    else:
        print("\n❌ SENKRONIZASYON BASARISIZ!")
        print("📞 Log dosyasini kontrol edin")

if __name__ == "__main__":
    main()
