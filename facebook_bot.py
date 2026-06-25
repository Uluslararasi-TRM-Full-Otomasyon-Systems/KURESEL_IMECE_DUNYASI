# facebook_bot.py
import facebook
import requests

class FacebookBot:
    def __init__(self, access_token, page_id):
        self.graph = facebook.GraphAPI(access_token=access_token)
        self.page_id = page_id
        self.access_token = access_token
    
    def sayfa_gonderisi_paylas(self, mesaj, link=None, resim_yolu=None):
        """Facebook sayfasına gönderi paylaşır"""
        try:
            if resim_yolu:
                # Resimli paylaşım
                with open(resim_yolu, 'rb') as foto:
                    self.graph.put_photo(
                        image=foto,
                        message=mesaj
                    )
            else:
                # Sadece metin paylaşımı
                self.graph.put_object(
                    parent_object='me',
                    connection_name='feed',
                    message=mesaj,
                    link=link
                )
            print(f"✅ Facebook: Gönderi paylaşıldı")
        except Exception as e:
            print(f"❌ Facebook hatası: {e}")
    
    def gruba_gonderi_paylas(self, grup_id, mesaj):
        """Facebook grubuna gönderi paylaşır"""
        try:
            self.graph.put_object(
                parent_object=grup_id,
                connection_name='feed',
                message=mesaj
            )
            print(f"✅ Facebook Grubu: Gönderi paylaşıldı")
        except Exception as e:
            print(f"❌ Facebook grup hatası: {e}")
