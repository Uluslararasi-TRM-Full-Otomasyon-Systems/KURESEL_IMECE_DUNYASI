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
        """Instagram'a giriş yapar"""
        try:
            self.client.login(self.username, self.password)
            print(f"✅ Instagram: @{self.username} giriş başarılı")
            return True
        except Exception as e:
            print(f"❌ Instagram giriş hatası: {e}")
            return False
    
    def fotografli_gonderi_paylas(self, foto_yolu, aciklama):
        """Fotoğraflı gönderi paylaşır"""
        try:
            media = self.client.photo_upload(
                foto_yolu,
                aciklama
            )
            print(f"✅ Instagram: Fotoğraflı gönderi paylaşıldı")
            return media
        except Exception as e:
            print(f"❌ Instagram paylaşım hatası: {e}")
            return None
    
    def hikaye_paylas(self, foto_yolu):
        """Hikaye (story) paylaşır"""
        try:
            self.client.photo_upload_to_story(foto_yolu)
            print(f"✅ Instagram: Hikaye paylaşıldı")
        except Exception as e:
            print(f"❌ Instagram hikaye hatası: {e}")
    
    def reels_paylas(self, video_yolu, aciklama):
        """Reels (kısa video) paylaşır"""
        try:
            self.client.clip_upload(
                video_yolu,
                aciklama
            )
            print(f"✅ Instagram: Reels paylaşıldı")
        except Exception as e:
            print(f"❌ Instagram Reels hatası: {e}")
