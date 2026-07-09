# instagram_bot.py
from instagrapi import Client
import time
import random

class InstagramBot:
    def __init__(self, username, password):
        self.client = Client()
        self.username = username
        self.password = password
        
    def giris_yap(self):
        """Instagram'a giris yapar"""
        try:
            self.client.login(self.username, self.password)
            print(f"✅ Instagram: @{self.username} giris basarili")
            return True
        except Exception as e:
            print(f"❌ Instagram giris hatasi: {e}")
            return False
    
    def fotografli_gonderi_paylas(self, foto_yolu, aciklama):
        """Fotografli gonderi paylasir"""
        try:
            media = self.client.photo_upload(
                foto_yolu,
                aciklama
            )
            print(f"✅ Instagram: Fotografli gonderi paylasildi")
            return media
        except Exception as e:
            print(f"❌ Instagram paylasim hatasi: {e}")
            return None
    
    def hikaye_paylas(self, foto_yolu):
        """Hikaye (story) paylasir"""
        try:
            self.client.photo_upload_to_story(foto_yolu)
            print(f"✅ Instagram: Hikaye paylasildi")
        except Exception as e:
            print(f"❌ Instagram hikaye hatasi: {e}")
    
    def reels_paylas(self, video_yolu, aciklama):
        """Reels (kisa video) paylasir"""
        try:
            self.client.clip_upload(
                video_yolu,
                aciklama
            )
            print(f"✅ Instagram: Reels paylasildi")
        except Exception as e:
            print(f"❌ Instagram Reels hatasi: {e}")
