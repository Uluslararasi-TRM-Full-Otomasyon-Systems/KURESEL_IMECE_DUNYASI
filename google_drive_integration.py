#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TRM Google Drive Integration - Veri depolama ve analitik
"""

import asyncio
import logging
import json
import os

import os as _os_gdrive
_TRM_MODE_GDRIVE = _os_gdrive.getenv("TRM_MODE", "live").lower()
_MOCK_ALLOWED_GDRIVE = _TRM_MODE_GDRIVE in ("test", "demo")

import re
from datetime import datetime, timedelta
from typing import Dict, List, Optional

# Google Drive kutuphaneleri
try:
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from google.auth.transport.requests import Request
    from googleapiclient.discovery import build
    from googleapiclient.http import MediaFileUpload
    GOOGLE_DRIVE_AVAILABLE = True
except ImportError:
    GOOGLE_DRIVE_AVAILABLE = False
    print("⚠️ Google Drive kutuphaneleri kurulu degil. Mock mod kullanilacak.")

try:
    import pandas as pd
    PANDAS_AVAILABLE = True
except ImportError:
    PANDAS_AVAILABLE = False
    print("⚠️ Pandas kurulu degil. Mock mod kullanilacak.")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MockGoogleDrive:
    """Mock Google Drive for testing"""
    def __init__(self):
        self.files = {}
        self.folder_id = "mock_folder_id"
        
    async def upload_file(self, file_path: str, folder_id: str = None) -> Optional[str]:
        """Mock dosya yukleme"""
        file_name = os.path.basename(file_path)
        file_id = f"mock_{datetime.now().timestamp()}"
        
        self.files[file_id] = {
            'name': file_name,
            'folder_id': folder_id or self.folder_id,
            'uploaded_at': datetime.now().isoformat()
        }
        
        logger.info(f"Mock dosya yuklendi: {file_name} -> {file_id}")
        return file_id
    
    async def create_spreadsheet(self, title: str, data: List[Dict]) -> Optional[str]:
        """Mock spreadsheet olusturma"""
        sheet_id = f"mock_sheet_{datetime.now().timestamp()}"
        
        self.files[sheet_id] = {
            'name': title,
            'type': 'spreadsheet',
            'data': data,
            'created_at': datetime.now().isoformat()
        }
        
        logger.info(f"Mock spreadsheet olusturuldu: {title} -> {sheet_id}")
        return sheet_id

class GoogleDriveManager:
    def __init__(self, credentials_file: str = "credentials.json"):
        self.credentials_file = credentials_file
        self.SCOPES = ['https://www.googleapis.com/auth/drive']
        self.creds = None
        self.service = None
        self.folder_id = os.getenv("GOOGLE_DRIVE_FOLDER_ID", "")
        
        if GOOGLE_DRIVE_AVAILABLE:
            self.authenticate()
        else:
            self.service = MockGoogleDrive()
            logger.warning("Mock Google Drive kullaniliyor")
    
    def authenticate(self):
        """Google kimlik dogrulama - browser yoksa manuel auth code akisi"""
        try:
            # 1) Var olan token'i yukle
            if os.path.exists('token.json'):
                self.creds = Credentials.from_authorized_user_file('token.json', self.SCOPES)

            # 2) Token'i refresh et
            if self.creds and self.creds.expired and self.creds.refresh_token:
                try:
                    self.creds.refresh(Request())
                    logger.info("✅ Google token otomatik yenilendi")
                except Exception as refresh_err:
                    logger.warning(f"Token yenileme basarisiz, yeniden auth gerekecek: {refresh_err}")
                    self.creds = None

            # 3) Gecerli credential yoksa yeni auth baslat
            if not self.creds or not self.creds.valid:
                if not os.path.exists(self.credentials_file):
                    logger.warning(
                        f"⚠️ {self.credentials_file} bulunamadi. Mock moda geciliyor.\n"
                        f"   Cozum: Google Cloud Console → OAuth Client ID (Desktop) → "
                        f"credentials.json olarak indirin."
                    )
                    self.service = MockGoogleDrive()
                    return

                # InstalledAppFlow ile auth - browser acabiliyorsa local_server, yoksa console
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.credentials_file, self.SCOPES
                )

                try:
                    # Once browser deneyelim
                    self.creds = flow.run_local_server(port=0, open_browser=True)
                except Exception as browser_err:
                    logger.warning(f"Browser acilamadi ({browser_err}), manuel auth code akisina geciliyor")
                    # Konsoldan auth code iste
                    flow.redirect_uri = "urn:ietf:wg:oauth:2.0:oob"
                    auth_url, _ = flow.authorization_url(prompt='consent')
                    print("\n" + "=" * 70)
                    print("🔐 GOOGLE DRIVE MANUEL YETKILENDIRME")
                    print("=" * 70)
                    print("1. Asagidaki URL'yi tarayicida ac:")
                    print(f"\n{auth_url}\n")
                    print("2. Hesabinizla giris yapin ve izin verin")
                    print("3. Size verilen kodu kopyalayip buraya yapistirin")
                    print("=" * 70)
                    code = input("Auth code: ").strip()
                    flow.fetch_token(code=code)
                    self.creds = flow.credentials

                # Token'i kaydet
                with open('token.json', 'w') as token:
                    token.write(self.creds.to_json())
                logger.info("✅ Yeni Google token kaydedildi")

            self.service = build('drive', 'v3', credentials=self.creds)
            logger.info("✅ Google Drive kimlik dogrulamasi basarili")

        except Exception as e:
            logger.error(f"❌ Google Drive auth hatasi: {e} - Mock moda geciliyor")
            self.service = MockGoogleDrive()
    
    async def upload_file(self, file_path: str, folder_id: str = None) -> Optional[str]:
        """Dosya yukle"""
        try:
            if isinstance(self.service, MockGoogleDrive):
                return await self.service.upload_file(file_path, folder_id)
            
            file_metadata = {
                'name': os.path.basename(file_path)
            }
            
            if folder_id or self.folder_id:
                file_metadata['parents'] = [folder_id or self.folder_id]
            
            media = MediaFileUpload(file_path, resumable=True)
            
            file = self.service.files().create(
                body=file_metadata,
                media_body=media,
                fields='id'
            ).execute()
            
            file_id = file.get('id')
            logger.info(f"Dosya yuklendi: {os.path.basename(file_path)} -> {file_id}")
            return file_id
            
        except Exception as e:
            logger.error(f"Dosya yukleme hatasi: {e}")
            return None
    
    async def create_folder(self, folder_name: str, parent_folder_id: str = None) -> Optional[str]:
        """Klasor olustur"""
        try:
            if isinstance(self.service, MockGoogleDrive):
                folder_id = f"mock_folder_{datetime.now().timestamp()}"
                logger.info(f"Mock klasor olusturuldu: {folder_name} -> {folder_id}")
                return folder_id
            
            file_metadata = {
                'name': folder_name,
                'mimeType': 'application/vnd.google-apps.folder'
            }
            
            if parent_folder_id or self.folder_id:
                file_metadata['parents'] = [parent_folder_id or self.folder_id]
            
            folder = self.service.files().create(
                body=file_metadata,
                fields='id'
            ).execute()
            
            folder_id = folder.get('id')
            logger.info(f"Klasor olusturuldu: {folder_name} -> {folder_id}")
            return folder_id
            
        except Exception as e:
            logger.error(f"Klasor olusturma hatasi: {e}")
            return None
    
    async def list_files(self, folder_id: str = None, query: str = None) -> List[Dict]:
        """Dosyalari listele"""
        try:
            if isinstance(self.service, MockGoogleDrive):
                return list(self.service.files.values())
            
            q = f"'{folder_id or self.folder_id}' in parents"
            if query:
                q += f" and name contains '{query}'"
            
            results = self.service.files().list(
                q=q,
                pageSize=100,
                fields="files(id, name, mimeType, createdTime, size)"
            ).execute()
            
            files = results.get('files', [])
            logger.info(f"{len(files)} dosya bulundu")
            return files
            
        except Exception as e:
            logger.error(f"Dosya listeleme hatasi: {e}")
            return []
    
    async def delete_file(self, file_id: str) -> bool:
        """Dosya sil"""
        try:
            if isinstance(self.service, MockGoogleDrive):
                if file_id in self.service.files:
                    del self.service.files[file_id]
                    logger.info(f"Mock dosya silindi: {file_id}")
                    return True
                return False
            
            self.service.files().delete(fileId=file_id).execute()
            logger.info(f"Dosya silindi: {file_id}")
            return True
            
        except Exception as e:
            logger.error(f"Dosya silme hatasi: {e}")
            return False

class AnalyticsManager:
    """Analitik ve raporlama yoneticisi"""
    def __init__(self, drive_manager: GoogleDriveManager):
        self.drive_manager = drive_manager
        self.analytics_file = "trm_analytics.json"
        self.reports_folder = "TRM_Raporlar"
        
        # Analitik verileri
        self.analytics_data = {
            'products': [],
            'social_media': [],
            'commissions': [],
            'daily_stats': {},
            'created_at': datetime.now().isoformat()
        }
        
        self.load_analytics()
    
    def load_analytics(self):
        """Analitik verilerini yukle"""
        try:
            if os.path.exists(self.analytics_file):
                with open(self.analytics_file, 'r', encoding='utf-8') as f:
                    self.analytics_data = json.load(f)
                logger.info("Analitik verileri yuklendi")
            else:
                logger.info("Yeni analitik dosyasi olusturuluyor")
                self.save_analytics()
        except Exception as e:
            logger.error(f"Analitik yukleme hatasi: {e}")
    
    def save_analytics(self):
        """Analitik verilerini kaydet"""
        try:
            with open(self.analytics_file, 'w', encoding='utf-8') as f:
                json.dump(self.analytics_data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            logger.error(f"Analitik kaydetme hatasi: {e}")
    
    async def add_product_analytics(self, product_data: Dict, content_result: Dict, social_result: Dict):
        """Urun analitigi ekle"""
        analytics_entry = {
            'product_id': product_data.get('message_id', ''),
            'title': product_data.get('title', ''),
            'price': product_data.get('price', ''),
            'commission_rate': product_data.get('commission_rate', 0),
            'priority': product_data.get('priority', 'medium'),
            'source': product_data.get('source', ''),
            'captured_at': product_data.get('captured_at', ''),
            'ai_processed': content_result.get('success', False),
            'social_published': social_result.get('summary', {}).get('successful_platforms', 0),
            'total_platforms': social_result.get('summary', {}).get('total_platforms', 0),
            'publish_success_rate': social_result.get('summary', {}).get('success_rate', 0),
            'processed_at': datetime.now().isoformat()
        }
        
        self.analytics_data['products'].append(analytics_entry)
        
        # Gunluk istatistikleri guncelle
        today = datetime.now().strftime('%Y-%m-%d')
        if today not in self.analytics_data['daily_stats']:
            self.analytics_data['daily_stats'][today] = {
                'products_captured': 0,
                'high_commission': 0,
                'social_published': 0,
                'total_impressions': 0,
                'estimated_commission': 0
            }
        
        daily_stats = self.analytics_data['daily_stats'][today]
        daily_stats['products_captured'] += 1
        
        if product_data.get('commission_rate', 0) >= 20:
            daily_stats['high_commission'] += 1
        
        daily_stats['social_published'] += social_result.get('summary', {}).get('successful_platforms', 0)
        
        # Tahmini komisyon hesapla
        price = product_data.get('price', '0')
        if price:
            try:
                price_num = float(re.sub(r'[^\d.]', '', price))
                commission_rate = product_data.get('commission_rate', 0) / 100
                estimated_commission = price_num * commission_rate * 0.1  # %10 satis varsayimi
                daily_stats['estimated_commission'] += estimated_commission
            except:
                pass
        
        self.save_analytics()
        logger.info(f"Urun analitigi eklendi: {product_data.get('title', '')}")
    
    async def generate_daily_report(self) -> Dict:
        """Gunluk rapor olustur"""
        today = datetime.now().strftime('%Y-%m-%d')
        yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
        
        # Dunku istatistikleri al
        daily_stats = self.analytics_data['daily_stats'].get(yesterday, {
            'products_captured': 0,
            'high_commission': 0,
            'social_published': 0,
            'total_impressions': 0,
            'estimated_commission': 0
        })
        
        # Haftalik ve aylik ozet
        weekly_stats = self.get_period_stats(7)
        monthly_stats = self.get_period_stats(30)
        
        report = {
            'date': yesterday,
            'daily': daily_stats,
            'weekly': weekly_stats,
            'monthly': monthly_stats,
            'total_products': len(self.analytics_data['products']),
            'top_products': self.get_top_products(5),
            'generated_at': datetime.now().isoformat()
        }
        
        return report
    
    def get_period_stats(self, days: int) -> Dict:
        """Belirtilen gun icin istatistikler"""
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        period_stats = {
            'products_captured': 0,
            'high_commission': 0,
            'social_published': 0,
            'estimated_commission': 0
        }
        
        for date_str, stats in self.analytics_data['daily_stats'].items():
            try:
                date = datetime.strptime(date_str, '%Y-%m-%d')
                if start_date <= date <= end_date:
                    for key in period_stats:
                        period_stats[key] += stats.get(key, 0)
            except:
                continue
        
        return period_stats
    
    def get_top_products(self, limit: int = 5) -> List[Dict]:
        """En iyi urunleri getir"""
        products = sorted(
            self.analytics_data['products'],
            key=lambda x: (x.get('commission_rate', 0), x.get('publish_success_rate', 0)),
            reverse=True
        )
        
        return products[:limit]
    
    async def export_to_google_sheets(self, report_data: Dict) -> Optional[str]:
        """Raporu Google Sheets'e aktar"""
        try:
            if not PANDAS_AVAILABLE:
                logger.warning("Pandas kurulu degil. Mock export kullaniliyor.")
                return await self.drive_manager.create_spreadsheet(
                    f"TRM Rapor {report_data['date']}",
                    [report_data]
                )
            
            # DataFrame olustur
            df_data = []
            
            # Gunluk veriler
            daily = report_data['daily']
            df_data.append({
                'Kategori': 'Gunluk',
                'Tarih': report_data['date'],
                'Yakalanan Urun': daily['products_captured'],
                '%20+ Urun': daily['high_commission'],
                'Sosyal Paylasim': daily['social_published'],
                'Tahmini Komisyon': f"{daily['estimated_commission']:.2f} TL"
            })
            
            # Haftalik veriler
            weekly = report_data['weekly']
            df_data.append({
                'Kategori': 'Haftalik',
                'Tarih': f"Son 7 gun",
                'Yakalanan Urun': weekly['products_captured'],
                '%20+ Urun': weekly['high_commission'],
                'Sosyal Paylasim': weekly['social_published'],
                'Tahmini Komisyon': f"{weekly['estimated_commission']:.2f} TL"
            })
            
            # Aylik veriler
            monthly = report_data['monthly']
            df_data.append({
                'Kategori': 'Aylik',
                'Tarih': f"Son 30 gun",
                'Yakalanan Urun': monthly['products_captured'],
                '%20+ Urun': monthly['high_commission'],
                'Sosyal Paylasim': monthly['social_published'],
                'Tahmini Komisyon': f"{monthly['estimated_commission']:.2f} TL"
            })
            
            # Google Sheets'e yukle
            if isinstance(self.drive_manager.service, MockGoogleDrive):
                return await self.drive_manager.service.create_spreadsheet(
                    f"TRM Rapor {report_data['date']}",
                    df_data
                )
            
            # Gercek Google Sheets API cagrisi buraya eklenecek
            # Simdilik mock kullaniyoruz
            return await self.drive_manager.service.create_spreadsheet(
                f"TRM Rapor {report_data['date']}",
                df_data
            )
            
        except Exception as e:
            logger.error(f"Google Sheets export hatasi: {e}")
            return None
    
    def get_dashboard_stats(self) -> Dict:
        """Dashboard istatistikleri"""
        today = datetime.now().strftime('%Y-%m-%d')
        daily_stats = self.analytics_data['daily_stats'].get(today, {
            'products_captured': 0,
            'high_commission': 0,
            'social_published': 0,
            'estimated_commission': 0
        })
        
        # Toplam istatistikler
        total_products = len(self.analytics_data['products'])
        high_commission_products = sum(1 for p in self.analytics_data['products'] if p.get('commission_rate', 0) >= 20)
        avg_commission_rate = sum(p.get('commission_rate', 0) for p in self.analytics_data['products']) / max(total_products, 1)
        
        return {
            'today_products': daily_stats['products_captured'],
            'today_high_commission': daily_stats['high_commission'],
            'today_social_published': daily_stats['social_published'],
            'today_estimated_commission': daily_stats['estimated_commission'],
            'total_products': total_products,
            'total_high_commission': high_commission_products,
            'avg_commission_rate': round(avg_commission_rate, 1),
            'success_rate': sum(p.get('publish_success_rate', 0) for p in self.analytics_data['products']) / max(total_products, 1)
        }

# Test ve ornek kullanim
async def test_google_drive_integration():
    """Google Drive entegrasyonunu test et"""
    drive_manager = GoogleDriveManager()
    analytics_manager = AnalyticsManager(drive_manager)
    
    logger.info("Google Drive entegrasyonu test ediliyor...")
    
    # Test analitigi ekle
    test_product = {
        'title': 'Test Urun - %25 Komisyon',
        'price': '299 TL',
        'commission_rate': 25,
        'priority': 'high',
        'source': 'test',
        'message_id': 999,
        'captured_at': datetime.now().isoformat()
    }
    
    test_content = {'success': True}
    test_social = {
        'summary': {
            'successful_platforms': 4,
            'total_platforms': 5,
            'success_rate': 80
        }
    }
    
    await analytics_manager.add_product_analytics(test_product, test_content, test_social)
    
    # Rapor olustur
    report = await analytics_manager.generate_daily_report()
    logger.info(f"Test raporu: {report}")
    
    # Dashboard istatistikleri
    dashboard_stats = analytics_manager.get_dashboard_stats()
    logger.info(f"Dashboard istatistikleri: {dashboard_stats}")

if __name__ == "__main__":
    asyncio.run(test_google_drive_integration())
