#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TRM FULL OTOMASYON - MERKEZİ YAPILANDIRMA SİSTEMİ
Tüm API anahtarlarını ve ayarları tek yerden yönetir
Auto-refresh token sistemi ile kullanıcı müdahalesi gerektirmez
"""

import os
import json
import logging
from pathlib import Path
from typing import Dict, Any, Optional
from datetime import datetime, timedelta
import pickle

# Google API imports
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

logger = logging.getLogger(__name__)

class TRMConfig:
    """Merkezi yapılandırma sınıfı"""
    
    def __init__(self):
        self.system_path = Path(__file__).parent
        self.env_file = self.system_path / "secrets.env"
        self.credentials_file = self.system_path / "credentials.json"
        self.token_file = self.system_path / "token.pickle"
        
        self.config = {}
        self.credentials_cache = {}
        self.load_environment()
        
    def load_environment(self):
        """.env dosyasını yükle ve os.environ'a aktar"""
        try:
            if not self.env_file.exists():
                logger.warning(f"⚠️ {self.env_file} dosyası bulunamadı")
                return False

            with open(self.env_file, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith('#') or '=' not in line:
                        continue
                    key, value = line.split('=', 1)
                    key = key.strip()
                    value = value.strip().strip('"').strip("'")
                    self.config[key] = value
                    # KRİTİK: Diğer modüller os.getenv() ile arıyor
                    os.environ[key] = value

            logger.info("✅ Ortam değişkenleri yüklendi")
            return True

        except Exception as e:
            logger.error(f"❌ Ortam değişkenleri yüklenemedi: {e}")
            return False
    
    def get(self, key: str, default: Any = None) -> Any:
        """Yapılandırma değeri al"""
        return self.config.get(key, default)
    
    def get_telegram_config(self) -> Dict[str, str]:
        """Telegram yapılandırması"""
        return {
            'api_id': self.get('TELEGRAM_API_ID'),
            'api_hash': self.get('TELEGRAM_API_HASH'),
            'bot_token': self.get('TELEGRAM_BOT_TOKEN'),
            'notification_token': self.get('TELEGRAM_BOT_TOKEN_NOTIFICATION'),
            'chat_id': self.get('TELEGRAM_CHAT_ID')
        }
    
    def get_openai_config(self) -> Dict[str, str]:
        """OpenAI yapılandırması"""
        return {
            'api_key': self.get('OPENAI_API_KEY')
        }
    
    def get_google_credentials(self, service: str = 'drive', scopes: list = None) -> Optional[Credentials]:
        """
        Google servisleri için kimlik doğrulama
        Auto-refresh token sistemi ile çalışır
        """
        try:
            # Default scopes
            if scopes is None:
                if service == 'drive':
                    scopes = ['https://www.googleapis.com/auth/drive']
                elif service == 'youtube':
                    scopes = ['https://www.googleapis.com/auth/youtube.readonly']
                elif service == 'blogger':
                    scopes = ['https://www.googleapis.com/auth/blogger']
                else:
                    scopes = ['https://www.googleapis.com/auth/drive']
            
            # Token cache'i kontrol et
            creds = None
            if self.token_file.exists():
                with open(self.token_file, 'rb') as token:
                    creds = pickle.load(token)
            
            # Token geçerli mi kontrol et
            if creds and creds.expired and creds.refresh_token:
                logger.info(f"🔄 {service} token yenileniyor...")
                creds.refresh(Request())
                self.save_token(creds)
                return creds
            
            # Yeni token gerekli
            if not creds or not creds.valid:
                if not self.credentials_file.exists():
                    logger.error(f"❌ {self.credentials_file} bulunamadı")
                    return None
                
                # OAuth 2.0 flow
                flow = InstalledAppFlow.from_client_config(
                    self._load_credentials_json(),
                    scopes=scopes
                )
                
                # Local server ile authentication
                creds = flow.run_local_server(port=0)
                self.save_token(creds)
                
            logger.info(f"✅ {service} kimlik doğrulaması başarılı")
            return creds
            
        except Exception as e:
            logger.error(f"❌ {service} kimlik doğrulaması başarısız: {e}")
            return None
    
    def _load_credentials_json(self) -> Dict[str, Any]:
        """credentials.json dosyasını yükle"""
        try:
            with open(self.credentials_file, 'r') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"❌ credentials.json yüklenemedi: {e}")
            return {}
    
    def save_token(self, credentials: Credentials):
        """Token'i kaydet"""
        try:
            with open(self.token_file, 'wb') as token:
                pickle.dump(credentials, token)
            logger.info("✅ Token kaydedildi")
        except Exception as e:
            logger.error(f"❌ Token kaydedilemedi: {e}")
    
    def get_google_service(self, service: str = 'drive', version: str = 'v3'):
        """
        Google servisi oluştur
        Auto-refresh ile credentials yönetimi
        """
        try:
            credentials = self.get_google_credentials(service)
            if not credentials:
                return None
            
            service_obj = build(service, version, credentials=credentials)
            logger.info(f"✅ {service} servisi oluşturuldu")
            return service_obj
            
        except Exception as e:
            logger.error(f"❌ {service} servisi oluşturulamadı: {e}")
            return None
    
    def get_youtube_config(self) -> Dict[str, str]:
        """YouTube yapılandırması"""
        return {
            'api_key': self.get('YOUTUBE_API_KEY'),
            'service': self.get_google_service('youtube', 'v3')
        }
    
    def get_social_media_config(self) -> Dict[str, Dict[str, str]]:
        """Sosyal medya yapılandırması"""
        return {
            'messaging': {
                'api_token': self.get('DISCORD_BOT_TOKEN'),
                'phone_number': self.get('DISCORD_CHANNEL_ID')
            },
            'facebook': {
                'access_token': self.get('FACEBOOK_ACCESS_TOKEN')
            },
            'instagram': {
                'access_token': self.get('INSTAGRAM_ACCESS_TOKEN')
            },
            'twitter': {
                'api_key': self.get('TWITTER_API_KEY'),
                'api_secret': self.get('TWITTER_API_SECRET')
            }
        }
    
    def get_ecommerce_config(self) -> Dict[str, str]:
        """E-ticaret platformları yapılandırması"""
        return {
            'trendyol': {'api_key': self.get('TRENDYOL_API_KEY')},
            'hepsiburada': {'api_key': self.get('HEPSIBURADA_API_KEY')},
            'n11': {'api_key': self.get('N11_API_KEY')}
        }
    
    def get_cloud_config(self) -> Dict[str, str]:
        """Cloud deployment yapılandırması"""
        return {
            'railway': {'token': self.get('RAILWAY_TOKEN')},
            'render': {'api_key': self.get('RENDER_API_KEY')},
            'heroku': {'api_key': self.get('HEROKU_API_KEY')}
        }
    
    def get_system_config(self) -> Dict[str, Any]:
        """Sistem ayarları"""
        return {
            'name': self.get('SYSTEM_NAME', 'TRM FULL OTOMASYON'),
            'debug_mode': self.get('DEBUG_MODE', 'false').lower() == 'true',
            'log_level': self.get('LOG_LEVEL', 'INFO'),
            'max_retries': int(self.get('MAX_RETRIES', '3')),
            'api_rate_limit': int(self.get('API_RATE_LIMIT', '100')),
            'request_timeout': int(self.get('REQUEST_TIMEOUT', '30')),
            'database_url': self.get('DATABASE_URL', 'sqlite:///trm_automation.db'),
            'database_backup_path': self.get('DATABASE_BACKUP_PATH', './backups/'),
            'secret_key': self.get('SECRET_KEY'),
            'jwt_secret': self.get('JWT_SECRET'),
            'max_concurrent_tasks': int(self.get('MAX_CONCURRENT_TASKS', '10')),
            'cache_duration_minutes': int(self.get('CACHE_DURATION_MINUTES', '30')),
            'auto_restart_enabled': self.get('AUTO_RESTART_ENABLED', 'true').lower() == 'true',
            'health_check_interval': int(self.get('HEALTH_CHECK_INTERVAL_MINUTES', '15'))
        }
    
    def validate_critical_configs(self) -> Dict[str, bool]:
        """Kritik yapılandırmaları doğrula (varlığını kontrol eder, içerik karşılaştırması yapmaz)"""
        validation = {}

        # Telegram - sadece anahtarların DOLU olduğunu kontrol et
        telegram = self.get_telegram_config()
        validation['telegram'] = all([
            telegram['api_id'],
            telegram['api_hash'],
            telegram['bot_token'],
        ])

        # OpenAI/DeepSeek
        openai_cfg = self.get_openai_config()
        validation['openai'] = bool(
            openai_cfg['api_key'] and openai_cfg['api_key'].startswith('sk-')
        )

        # YouTube
        youtube = self.get_youtube_config()
        validation['youtube'] = bool(
            youtube['api_key'] and youtube['api_key'].startswith('AIza')
        )

        # Google Services
        validation['google_services'] = self.credentials_file.exists()

        return validation
    
    def get_status_report(self) -> str:
        """Durum raporu oluştur"""
        validation = self.validate_critical_configs()
        
        report = f"""
🔧 TRM FULL OTOMASYON - YAPILANDIRMA DURUMU
{'=' * 50}

📱 TELEGRAM: {'✅ Yapılandırıldı' if validation['telegram'] else '❌ Eksik'}
🤖 OPENAI: {'✅ Yapılandırıldı' if validation['openai'] else '❌ Eksik'}
📺 YOUTUBE: {'✅ Yapılandırıldı' if validation['youtube'] else '❌ Eksik'}
☁️ GOOGLE SERVİSLERİ: {'✅ Yapılandırıldı' if validation['google_services'] else '❌ Eksik'}

📁 DOSYA YOLLARI:
• Config: {self.env_file}
• Credentials: {self.credentials_file}
• Token Cache: {self.token_file}

🔄 AUTO-REFRESH SİSTEMİ: ✅ Aktif
📅 Son Kontrol: {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}
        """
        
        return report

# Global config instance
config = TRMConfig()

# Easy access functions
def get_telegram_config():
    return config.get_telegram_config()

def get_openai_config():
    return config.get_openai_config()

def get_youtube_config():
    return config.get_youtube_config()

def get_google_service(service='drive', version='v3'):
    return config.get_google_service(service, version)

def get_social_media_config():
    return config.get_social_media_config()

def get_ecommerce_config():
    return config.get_ecommerce_config()

def get_system_config():
    return config.get_system_config()

def get_status_report():
    return config.get_status_report()

if __name__ == "__main__":
    print(get_status_report())
