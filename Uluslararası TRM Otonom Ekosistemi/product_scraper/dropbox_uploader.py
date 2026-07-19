import dropbox
import json
from datetime import datetime

class DropboxUploader:
    def __init__(self, access_token):
        self.dbx = dropbox.Dropbox(access_token)
    
    def upload_product(self, product_json, folder_path):
        """Ürün JSON'ını Dropbox'a kaydet"""
        filename = f"{product_json['urun_adi'][:50]}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        dropbox_path = f"{folder_path}/{filename}"
        
        # JSON'ı string'e çevir
        json_str = json.dumps(product_json, ensure_ascii=False, indent=2)
        
        # Dropbox'a yükle
        self.dbx.files_upload(
            json_str.encode('utf-8'),
            dropbox_path,
            mode=dropbox.files.WriteMode.overwrite
        )
        print(f"✅ Ürün yüklendi: {dropbox_path}")
        return dropbox_path
