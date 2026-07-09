#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TRM FULL OTOMASYON - SOSYAL MEDYA YONETICISI
Tum sosyal medya entegrasyonlarini merkezi config uzerinden yonetir
"""

import logging
import requests
from typing import Dict, Any, Optional
from config import get_social_media_config

logger = logging.getLogger(__name__)

class SocialMediaManager:
    """Sosyal medya yonetim sinifi"""
    
    def __init__(self):
        self.config = get_social_media_config()
        self.services = {}
        self.initialize_services()
    
    def initialize_services(self):
        """Sosyal medya servislerini baslat"""
        try:
            # Telegram/Discord/Viber
            if self.config['messaging']['api_token'] != 'your_messaging_api_token_here':
                self.services['messaging'] = MessagingService(self.config['messaging'])
                logger.info("✅ Telegram/Discord/Viber servisi baslatildi")
            
            # Facebook
            if self.config['facebook']['access_token'] != 'your_facebook_access_token_here':
                self.services['facebook'] = FacebookService(self.config['facebook'])
                logger.info("✅ Facebook servisi baslatildi")
            
            # Instagram
            if self.config['instagram']['access_token'] != 'your_instagram_access_token_here':
                self.services['instagram'] = InstagramService(self.config['instagram'])
                logger.info("✅ Instagram servisi baslatildi")
            
            # Twitter
            if (self.config['twitter']['api_key'] != 'your_twitter_api_key_here' and 
                self.config['twitter']['api_secret'] != 'your_twitter_api_secret_here'):
                self.services['twitter'] = TwitterService(self.config['twitter'])
                logger.info("✅ Twitter servisi baslatildi")
                
        except Exception as e:
            logger.error(f"❌ Sosyal medya servisleri baslatilamadi: {e}")
    
    def post_to_all(self, message: str, media_path: Optional[str] = None) -> Dict[str, bool]:
        """Tum servislere gonder"""
        results = {}
        
        for service_name, service in self.services.items():
            try:
                success = service.post(message, media_path)
                results[service_name] = success
                status = "✅" if success else "❌"
                logger.info(f"{status} {service_name}: gonderildi")
            except Exception as e:
                results[service_name] = False
                logger.error(f"❌ {service_name} gonderilemedi: {e}")
        
        return results
    
    def get_service_status(self) -> Dict[str, Dict[str, Any]]:
        """Servis durumlarini al"""
        status = {}
        
        for service_name, service in self.services.items():
            try:
                status[service_name] = {
                    'connected': service.check_connection(),
                    'account_info': service.get_account_info(),
                    'last_post': service.get_last_post()
                }
            except Exception as e:
                status[service_name] = {
                    'connected': False,
                    'error': str(e)
                }
        
        return status

class MessagingService:
    """Telegram + Discord + Viber mesajlasma servisi"""
    
    def __init__(self, config: Dict[str, str]):
        self.api_token = config['api_token']
        self.phone_number = config['phone_number']
        self.base_url = "https://api.telegram.org/bot"  # Telegram API
    
    def post(self, message: str, media_path: Optional[str] = None) -> bool:
        """Mesaj gonder (Telegram/Discord/Viber)"""
        try:
            url = f"https://api.telegram.org/bot{self.api_token}/sendMessage"
            
            data = {
                'chat_id': self.phone_number,
                'text': message
            }
            
            response = requests.post(url, json=data, timeout=30)
            return response.status_code == 200
            
        except Exception as e:
            logger.error(f"❌ Telegram/Discord/Viber gonderim hatasi: {e}")
            return False
    
    def check_connection(self) -> bool:
        """Baglanti kontrolu"""
        try:
            url = f"https://api.telegram.org/bot{self.api_token}/getMe"
            response = requests.get(url, timeout=10)
            return response.status_code == 200
        except:
            return False
    
    def get_account_info(self) -> Dict[str, str]:
        """Hesap bilgileri"""
        return {'service': 'Telegram/Discord/Viber', 'phone': self.phone_number}
    
    def get_last_post(self) -> Optional[str]:
        """Son gonderi"""
        return None

class FacebookService:
    """Facebook servisi"""
    
    def __init__(self, config: Dict[str, str]):
        self.access_token = config['access_token']
        self.base_url = "https://graph.facebook.com/v19.0"  # Facebook Graph API
    
    def post(self, message: str, media_path: Optional[str] = None) -> bool:
        """Facebook gonderisi"""
        try:
            url = f"{self.base_url}/me/feed"
            
            data = {'message': message, 'access_token': self.access_token}
            
            response = requests.post(url, data=data, timeout=30)
            return response.status_code == 200
            
        except Exception as e:
            logger.error(f"❌ Facebook gonderim hatasi: {e}")
            return False
    
    def check_connection(self) -> bool:
        """Baglanti kontrolu"""
        try:
            url = f"{self.base_url}/me"
            params = {'access_token': self.access_token}
            response = requests.get(url, params=params, timeout=10)
            return response.status_code == 200
        except:
            return False
    
    def get_account_info(self) -> Dict[str, str]:
        """Hesap bilgileri"""
        return {'service': 'Facebook'}
    
    def get_last_post(self) -> Optional[str]:
        """Son gonderi"""
        return None

class InstagramService:
    """Instagram servisi"""
    
    def __init__(self, config: Dict[str, str]):
        self.access_token = config['access_token']
        self.base_url = "https://graph.instagram.com"
    
    def post(self, message: str, media_path: Optional[str] = None) -> bool:
        """Instagram gonderisi"""
        try:
            # Instagram icin media gereklidir
            if not media_path:
                logger.warning("⚠️ Instagram icin media dosyasi gerekli")
                return False
            
            url = f"{self.base_url}/me/media"
            
            data = {
                'caption': message,
                'access_token': self.access_token
            }
            
            response = requests.post(url, data=data, timeout=30)
            return response.status_code == 200
            
        except Exception as e:
            logger.error(f"❌ Instagram gonderim hatasi: {e}")
            return False
    
    def check_connection(self) -> bool:
        """Baglanti kontrolu"""
        try:
            url = f"{self.base_url}/me"
            params = {'access_token': self.access_token}
            response = requests.get(url, params=params, timeout=10)
            return response.status_code == 200
        except:
            return False
    
    def get_account_info(self) -> Dict[str, str]:
        """Hesap bilgileri"""
        return {'service': 'Instagram'}
    
    def get_last_post(self) -> Optional[str]:
        """Son gonderi"""
        return None

class TwitterService:
    """Twitter servisi"""
    
    def __init__(self, config: Dict[str, str]):
        self.api_key = config['api_key']
        self.api_secret = config['api_secret']
        self.base_url = "https://api.twitter.com/2"
    
    def post(self, message: str, media_path: Optional[str] = None) -> bool:
        """Tweet gonder"""
        try:
            # Twitter icin bearer token gerekir
            bearer_token = self._get_bearer_token()
            if not bearer_token:
                return False
            
            url = f"{self.base_url}/tweets"
            
            headers = {
                'Authorization': f'Bearer {bearer_token}',
                'Content-Type': 'application/json'
            }
            
            data = {'text': message}
            
            response = requests.post(url, json=data, headers=headers, timeout=30)
            return response.status_code == 201
            
        except Exception as e:
            logger.error(f"❌ Twitter gonderim hatasi: {e}")
            return False
    
    def _get_bearer_token(self) -> Optional[str]:
        """Bearer token al"""
        try:
            url = "https://api.twitter.com/oauth2/token"
            
            data = {'grant_type': 'client_credentials'}
            auth = (self.api_key, self.api_secret)
            
            response = requests.post(url, data=data, auth=auth, timeout=10)
            if response.status_code == 200:
                return response.json().get('access_token')
            return None
        except:
            return None
    
    def check_connection(self) -> bool:
        """Baglanti kontrolu"""
        try:
            bearer_token = self._get_bearer_token()
            if not bearer_token:
                return False
            
            url = f"{self.base_url}/users/me"
            headers = {'Authorization': f'Bearer {bearer_token}'}
            response = requests.get(url, headers=headers, timeout=10)
            return response.status_code == 200
        except:
            return False
    
    def get_account_info(self) -> Dict[str, str]:
        """Hesap bilgileri"""
        return {'service': 'Twitter'}
    
    def get_last_post(self) -> Optional[str]:
        """Son gonderi"""
        return None

# Global instance
social_manager = SocialMediaManager()

def post_to_social_media(message: str, media_path: Optional[str] = None) -> Dict[str, bool]:
    """Tum sosyal medyaya gonder"""
    return social_manager.post_to_all(message, media_path)

def get_social_media_status() -> Dict[str, Dict[str, Any]]:
    """Sosyal medya durumunu al"""
    return social_manager.get_service_status()

if __name__ == "__main__":
    print("🔧 Sosyal Medya Yoneticisi Test")
    status = get_social_media_status()
    for service, info in status.items():
        print(f"{service}: {'✅' if info['connected'] else '❌'}")
