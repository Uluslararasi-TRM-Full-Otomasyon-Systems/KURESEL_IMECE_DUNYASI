#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TRM Nirvana v3.0 - Google Drive Veri Toplama ve Sosyal Medya Otomatik Paylasim
trendurunlermarket@gmail hesabina bagli Drive alaninda urunlerle ilgili tum bilgi,
gorsel ve videolarin otomatik olarak toplanmasi, ardindan gerekli verilerin
cekilerek sosyal medya platformlarinda otomatik paylasim yapilmasi
"""

import asyncio
import logging
import json
import os
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import requests
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

# Sistem modulleri
from ai_integration import AIContentGenerator
from social_media_automation import SocialMediaManager

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/drive_social_manager.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class DriveSocialManager:
    def __init__(self):
        self.ai_generator = AIContentGenerator()
        self.social_automation = SocialMediaManager()
        
        # Google Drive ayarlari
        self.drive_settings = {
            'credentials_file': 'credentials.json',
            'token_file': 'token.json',
            'scopes': ['https://www.googleapis.com/auth/drive'],
            'service_account_file': 'service_account.json'
        }
        
        # Sosyal medya ayarlari
        self.social_settings = {
            'auto_post': True,
            'post_interval': 1800,  # 30 dakika
            'max_daily_posts': 50,
            'platforms': ['facebook', 'instagram', 'twitter', 'tiktok', 'youtube'],
            'content_types': ['image', 'video', 'text', 'story']
        }
        
        # Veri toplama ayarlari
        self.data_collection_settings = {
            'scan_interval': 600,  # 10 dakika
            'file_types': ['jpg', 'jpeg', 'png', 'gif', 'mp4', 'mov', 'avi'],
            'folder_structure': {
                'products': 'TRM_Urunler',
                'images': 'TRM_Gorseller',
                'videos': 'TRM_Videolar',
                'content': 'TRM_Icerikler',
                'posted': 'TRM_Paylasilanlar'
            }
        }
        
        # Drive servisi
        self.drive_service = None
        self.collected_data = []
        self.posted_content = []
        
    async def initialize_drive_service(self):
        """Google Drive servisini baslat"""
        try:
            logger.info("🌐 Google Drive servisi baslatiliyor...")
            
            # Credentials kontrolu
            creds = None
            if os.path.exists(self.drive_settings['token_file']):
                creds = Credentials.from_authorized_user_file(
                    self.drive_settings['token_file'],
                    self.drive_settings['scopes']
                )
            
            if not creds or not creds.valid:
                if creds and creds.expired and creds.refresh_token:
                    creds.refresh(Request())
                else:
                    flow = InstalledAppFlow.from_client_secrets_file(
                        self.drive_settings['credentials_file'],
                        self.drive_settings['scopes']
                    )
                    creds = flow.run_local_server(port=0)
                
                # Token'i kaydet
                with open(self.drive_settings['token_file'], 'w') as token:
                    token.write(creds.to_json())
            
            # Drive servisi olustur
            self.drive_service = build('drive', 'v3', credentials=creds)
            
            logger.info("✅ Google Drive servisi baslatildi")
            return True
            
        except Exception as e:
            logger.error(f"❌ Google Drive servisi baslatma hatasi: {e}")
            return False
    
    async def scan_drive_for_content(self):
        """Drive'dan icerik tara"""
        try:
            if not self.drive_service:
                logger.info("Google Drive bagli degil, senkronizasyon pasif.")
                return []
            
            logger.info("📁 Drive icerik taraniyor...")
            
            collected_items = []
            
            # Urun klasorunu tara
            products_folder = await self.find_folder(
                self.data_collection_settings['folder_structure']['products']
            )
            
            if products_folder:
                products = await self.list_files_in_folder(products_folder['id'])
                collected_items.extend(products)
            
            # Gorsel klasorunu tara
            images_folder = await self.find_folder(
                self.data_collection_settings['folder_structure']['images']
            )
            
            if images_folder:
                images = await self.list_files_in_folder(
                    images_folder['id'], 
                    file_types=self.data_collection_settings['file_types'][:4]  # Sadece gorseller
                )
                collected_items.extend(images)
            
            # Video klasorunu tara
            videos_folder = await self.find_folder(
                self.data_collection_settings['folder_structure']['videos']
            )
            
            if videos_folder:
                videos = await self.list_files_in_folder(
                    videos_folder['id'],
                    file_types=self.data_collection_settings['file_types'][4:]  # Sadece videolar
                )
                collected_items.extend(videos)
            
            # Icerik klasorunu tara
            content_folder = await self.find_folder(
                self.data_collection_settings['folder_structure']['content']
            )
            
            if content_folder:
                content = await self.list_files_in_folder(content_folder['id'])
                collected_items.extend(content)
            
            self.collected_data = collected_items
            logger.info(f"✅ {len(collected_items)} adet icerik toplandi")
            
            return collected_items
            
        except Exception as e:
            logger.error(f"❌ Drive icerik tarama hatasi: {e}")
            return []
    
    async def find_folder(self, folder_name: str) -> Optional[Dict]:
        """Klasor bul"""
        try:
            if not self.drive_service:
                logger.info("Google Drive bagli degil, klasor islemi pasif.")
                return None
            
            results = self.drive_service.files().list(
                q=f"mimeType='application/vnd.google-apps.folder' and name='{folder_name}'",
                spaces='drive',
                fields='files(id, name, createdTime, modifiedTime)'
            ).execute()
            
            folders = results.get('files', [])
            if folders:
                return folders[0]
            else:
                # Klasor yoksa olustur
                return await self.create_folder(folder_name)
                
        except Exception as e:
            logger.error(f"❌ Klasor bulma hatasi: {e}")
            return None
    
    async def create_folder(self, folder_name: str) -> Optional[Dict]:
        """Klasor olustur"""
        try:
            if not self.drive_service:
                logger.info("Google Drive bagli degil, klasor olusturma pasif.")
                return None
            
            folder_metadata = {
                'name': folder_name,
                'mimeType': 'application/vnd.google-apps.folder'
            }
            
            folder = self.drive_service.files().create(
                body=folder_metadata,
                fields='id, name, createdTime'
            ).execute()
            
            logger.info(f"✅ Klasor olusturuldu: {folder_name}")
            return folder
            
        except Exception as e:
            logger.error(f"❌ Klasor olusturma hatasi: {e}")
            return None
    
    async def list_files_in_folder(self, folder_id: str, file_types: List[str] = None) -> List[Dict]:
        """Klasordeki dosyalari listele"""
        try:
            if not self.drive_service:
                logger.info("Google Drive bagli degil, dosya listeleme pasif.")
                return []
            
            query = f"'{folder_id}' in parents"
            
            if file_types:
                file_type_query = " or ".join([f"mimeType contains '{ft}'" for ft in file_types])
                query += f" and ({file_type_query})"
            
            results = self.drive_service.files().list(
                q=query,
                spaces='drive',
                fields='files(id, name, mimeType, size, createdTime, modifiedTime, webViewLink, thumbnailLink)'
            ).execute()
            
            files = results.get('files', [])
            
            # Dosya bilgilerini zenginlestir
            enriched_files = []
            for file in files:
                enriched_file = {
                    'id': file['id'],
                    'name': file['name'],
                    'mimeType': file['mimeType'],
                    'size': file.get('size', 0),
                    'createdTime': file['createdTime'],
                    'modifiedTime': file['modifiedTime'],
                    'webViewLink': file.get('webViewLink', ''),
                    'thumbnailLink': file.get('thumbnailLink', ''),
                    'folder_id': folder_id,
                    'file_type': self.get_file_type(file['mimeType']),
                    'processed': False,
                    'posted': False
                }
                enriched_files.append(enriched_file)
            
            return enriched_files
            
        except Exception as e:
            logger.error(f"❌ Dosya listeleme hatasi: {e}")
            return []
    
    def get_file_type(self, mime_type: str) -> str:
        """Dosya tipini belirle"""
        if 'image' in mime_type:
            return 'image'
        elif 'video' in mime_type:
            return 'video'
        elif 'text' in mime_type:
            return 'text'
        else:
            return 'other'
    
    async def process_content_with_ai(self, content_items: List[Dict]) -> List[Dict]:
        """Icerigi AI ile isle"""
        try:
            logger.info("🤖 Icerik AI ile isleniyor...")
            
            processed_content = []
            
            for item in content_items:
                if not item.get('processed', False):
                    # AI ile icerik analizi
                    ai_analysis = await self.ai_generator.analyze_content(
                        item['name'],
                        item.get('webViewLink', ''),
                        item['file_type']
                    )
                    
                    # AI ile icerik uretimi
                    if item['file_type'] in ['image', 'video']:
                        ai_content = await self.ai_generator.generate_social_media_content(
                            item['name'],
                            item['file_type'],
                            ai_analysis
                        )
                    else:
                        ai_content = await self.ai_generator.generate_text_content(
                            item['name'],
                            ai_analysis
                        )
                    
                    processed_item = item.copy()
                    processed_item.update({
                        'processed': True,
                        'ai_analysis': ai_analysis,
                        'ai_content': ai_content,
                        'processed_time': datetime.now().isoformat()
                    })
                    
                    processed_content.append(processed_item)
                else:
                    processed_content.append(item)
            
            logger.info(f"✅ {len(processed_content)} adet icerik islendi")
            return processed_content
            
        except Exception as e:
            logger.error(f"❌ AI icerik isleme hatasi: {e}")
            return content_items
    
    async def post_to_social_media(self, content_items: List[Dict]) -> List[Dict]:
        """Sosyal medyada paylas"""
        try:
            logger.info("📱 Sosyal medyada paylasiliyor...")
            
            posted_items = []
            daily_post_count = len([p for p in self.posted_content 
                                  if datetime.fromisoformat(p['post_time']).date() == datetime.now().date()])
            
            for item in content_items:
                if (not item.get('posted', False) and 
                    daily_post_count < self.social_settings['max_daily_posts'] and
                    self.social_settings['auto_post']):
                    
                    # Sosyal medya paylasimi
                    post_result = await self.social_automation.post_content(
                        item['ai_content'],
                        item['file_type'],
                        item.get('webViewLink', ''),
                        self.social_settings['platforms']
                    )
                    
                    posted_item = item.copy()
                    posted_item.update({
                        'posted': True,
                        'post_time': datetime.now().isoformat(),
                        'post_result': post_result,
                        'platforms': post_result.get('posted_platforms', [])
                    })
                    
                    posted_items.append(posted_item)
                    daily_post_count += 1
                    
                    # Paylasilan dosyayi posted klasorune tasi
                    await self.move_to_posted_folder(item['id'])
                    
                    # Paylasim araligi
                    await asyncio.sleep(self.social_settings['post_interval'])
                else:
                    posted_items.append(item)
            
            self.posted_content = posted_items
            logger.info(f"✅ {len([p for p in posted_items if p['posted']])} adet icerik paylasildi")
            
            return posted_items
            
        except Exception as e:
            logger.error(f"❌ Sosyal medya paylasim hatasi: {e}")
            return content_items
    
    async def move_to_posted_folder(self, file_id: str):
        """Dosyayi paylasilanlar klasorune tasi"""
        try:
            if not self.drive_service:
                logger.info("Google Drive bagli degil, dosya tasima pasif.")
                return
            
            posted_folder = await self.find_folder(
                self.data_collection_settings['folder_structure']['posted']
            )
            
            if posted_folder:
                # Dosyayi tasi
                self.drive_service.files().update(
                    fileId=file_id,
                    addParents=[posted_folder['id']],
                    removeParents=[self.get_file_folder(file_id)]
                ).execute()
                
                logger.info(f"✅ Dosya paylasilanlar klasorune tasindi: {file_id}")
                
        except Exception as e:
            logger.error(f"❌ Dosya tasima hatasi: {e}")
    
    def get_file_folder(self, file_id: str) -> str:
        """Dosyanin bulundugu klasoru al"""
        try:
            if not self.drive_service:
                logger.info("Google Drive bagli degil, dosya klasoru alma pasif.")
                return None
            
            file = self.drive_service.files().get(
                fileId=file_id,
                fields='parents'
            ).execute()
            
            if file.get('parents'):
                return file['parents'][0]
            return None
            
        except Exception as e:
            logger.error(f"❌ Dosya klasoru alma hatasi: {e}")
            return None
    
    async def update_dashboard_data(self):
        """Panel verilerini guncelle"""
        try:
            dashboard_data = {
                'total_collected': len(self.collected_data),
                'total_posted': len([p for p in self.posted_content if p['posted']]),
                'daily_posts': len([p for p in self.posted_content 
                                   if datetime.fromisoformat(p['post_time']).date() == datetime.now().date()]),
                'last_collection': datetime.now().isoformat(),
                'last_post': None,
                'platform_status': {},
                'content_types': {
                    'images': len([c for c in self.collected_data if c['file_type'] == 'image']),
                    'videos': len([c for c in self.collected_data if c['file_type'] == 'video']),
                    'text': len([c for c in self.collected_data if c['file_type'] == 'text'])
                }
            }
            
            # Son paylasim zamani
            posted_items = [p for p in self.posted_content if p['posted']]
            if posted_items:
                dashboard_data['last_post'] = max(p['post_time'] for p in posted_items)
            
            # Platform durumlari
            for platform in self.social_settings['platforms']:
                dashboard_data['platform_status'][platform] = await self.social_automation.get_platform_status(platform)
            
            # Dashboard verisini kaydet
            with open('drive_social_dashboard.json', 'w', encoding='utf-8') as f:
                json.dump(dashboard_data, f, ensure_ascii=False, indent=2)
            
            logger.info("✅ Dashboard verileri guncellendi")
            
        except Exception as e:
            logger.error(f"❌ Dashboard verileri guncelleme hatasi: {e}")
    
    async def run_continuous_collection(self):
        """Surekli veri toplama ve paylasim"""
        try:
            logger.info("🔄 Surekli veri toplama ve paylasim baslatiliyor...")
            
            while True:
                try:
                    # Drive'dan icerik tara
                    new_content = await self.scan_drive_for_content()
                    
                    # Yeni icerik varsa isle
                    if new_content:
                        # AI ile isle
                        processed_content = await self.process_content_with_ai(new_content)
                        
                        # Sosyal medyada paylas
                        posted_content = await self.post_to_social_media(processed_content)
                        
                        # Dashboard'i guncelle
                        await self.update_dashboard_data()
                    
                    # Belirtilen aralikta bekle
                    await asyncio.sleep(self.data_collection_settings['scan_interval'])
                    
                except Exception as e:
                    logger.error(f"❌ Surekli toplama dongu hatasi: {e}")
                    await asyncio.sleep(60)  # Hata durumunda 1 dakika bekle
                    
        except Exception as e:
            logger.error(f"❌ Surekli toplama baslatma hatasi: {e}")
    
    def get_system_status(self) -> Dict:
        """Sistem durumunu al"""
        return {
            'drive_service_active': self.drive_service is not None,
            'total_collected': len(self.collected_data),
            'total_posted': len([p for p in self.posted_content if p['posted']]),
            'daily_posts': len([p for p in self.posted_content 
                               if datetime.fromisoformat(p['post_time']).date() == datetime.now().date()]),
            'last_collection': max([c['createdTime'] for c in self.collected_data]) if self.collected_data else None,
            'last_post': max([p['post_time'] for p in self.posted_content if p['posted']]) if self.posted_content else None,
            'auto_post_enabled': self.social_settings['auto_post'],
            'scan_interval': self.data_collection_settings['scan_interval'],
            'post_interval': self.social_settings['post_interval']
        }

# Ana baslatici
async def main():
    """Ana fonksiyon"""
    print("""
===============================================
    TRM NIRVANA v3.0 - DRIVE VE SOSYAL MEDYA
===============================================
  📁 Google Drive Veri Toplama
  🤖 AI Icerik Isleme
  📱 Sosyal Medya Otomatik Paylasim
  📊 Gercek Zamanli Dashboard
  🔄 Surekli Veri Akisi
===============================================
    """)
    
    # Drive ve sosyal medya yoneticisi olustur
    drive_social_manager = DriveSocialManager()
    
    try:
        # Google Drive servisini baslat
        if await drive_social_manager.initialize_drive_service():
            logger.info("🚀 Drive ve sosyal medya sistemi baslatiliyor...")
            
            # Surekli veri toplama ve paylasimi baslat
            await drive_social_manager.run_continuous_collection()
        else:
            logger.error("❌ Google Drive servisi baslatilamadi")
            
    except KeyboardInterrupt:
        logger.info("👋 Drive ve sosyal medya sistemi durduruldu")
    except Exception as e:
        logger.error(f"❌ Ana sistem hatasi: {e}")

if __name__ == "__main__":
    asyncio.run(main())
