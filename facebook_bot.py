# facebook_bot.py
import facebook
import requests

class FacebookBot:
    def __init__(self, access_token, page_id):
        self.graph = facebook.GraphAPI(access_token=access_token)
        self.page_id = page_id
        self.access_token = access_token
    
    def sayfa_gonderisi_paylas(self, mesaj, link=None, resim_yolu=None):
        """Facebook sayfasina gonderi paylasir"""
        try:
            if resim_yolu:
                # Resimli paylasim
                with open(resim_yolu, 'rb') as foto:
                    self.graph.put_photo(
                        image=foto,
                        message=mesaj
                    )
            else:
                # Sadece metin paylasimi
                self.graph.put_object(
                    parent_object='me',
                    connection_name='feed',
                    message=mesaj,
                    link=link
                )
            print(f"✅ Facebook: Gonderi paylasildi")
        except Exception as e:
            print(f"❌ Facebook hatasi: {e}")
    
    def gruba_gonderi_paylas(self, grup_id, mesaj):
        """Facebook grubuna gonderi paylasir"""
        try:
            self.graph.put_object(
                parent_object=grup_id,
                connection_name='feed',
                message=mesaj
            )
            print(f"✅ Facebook Grubu: Gonderi paylasildi")
        except Exception as e:
            print(f"❌ Facebook grup hatasi: {e}")
