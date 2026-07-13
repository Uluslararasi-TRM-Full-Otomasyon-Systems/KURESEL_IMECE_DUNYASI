import json
import os
from datetime import datetime, timedelta

try:
    from google.oauth2 import service_account
    from googleapiclient.discovery import build
    from googleapiclient.errors import HttpError
    import socket
    socket.setdefaulttimeout(30)
except ImportError:
    print("HATA: Google Sheets API kütüphaneleri yüklü değil.")
    print("Lütfen şu komutu çalıştırın: pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib")
    exit(1)

def poster_agent():
    # Dosyaların bulunduğu ana dizini otomatik tespit et
    base_dir = os.path.dirname(os.path.abspath(__file__))
    input_file = os.path.join(base_dir, 'trend_raporlari.json')
    credentials_file = os.path.join(base_dir, 'service_account.json')
    
    # Google Sheets ID
    SPREADSHEET_ID = '1Ttk5BFBmcrbKaEzMrvykOALcGYj18wibb7ctNsqIOQM'
    
    # Kimlik doğrulama dosyası kontrolü
    if not os.path.exists(credentials_file):
        print(f"HATA: {credentials_file} dosyası bulunamadı!")
        print(f"Lütfen service_account.json dosyasını şu klasöre koyun: {base_dir}")
        return
    
    try:
        # credentials.json dosyasını okuyarak service account email'ini al
        with open(credentials_file, 'r') as f:
            creds_data = json.load(f)
            service_account_email = creds_data.get('client_email', 'Bilinmiyor')
        
        credentials = service_account.Credentials.from_service_account_file(
            credentials_file,
            scopes=['https://www.googleapis.com/auth/spreadsheets']
        )
        service = build('sheets', 'v4', credentials=credentials)
    except Exception as e:
        print(f"HATA: credentials.json dosyası okunamadı veya geçersiz: {e}")
        return
    
    # JSON verisini oku
    if not os.path.exists(input_file):
        print(f"HATA: {input_file} dosyası bulunamadı!")
        return
        
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Verileri hazırla
    baslangic_tarihi = datetime.now() + timedelta(days=1)
    urun_sayac = 0
    rows_to_add = []
    
    for entry in data:
        products = entry.get('product_details', []) if 'product_details' in entry else [entry]
        
        for item in products:
            urun_adi = item.get('product_name', item.get('urun_adi', 'Trend Ürün'))
            urun_adi = str(urun_adi).replace('┼', '').strip()
            url = item.get('product_url', '')
            
            reklam_metni = (
                f"🔥 {urun_adi} - Şu an trendlerde!\n"
                f"💰 Kazandıran fırsat sizlerle.\n"
                f"Detaylar ve güncel fiyatlar için linke tıklayın! 👇"
            )
            
            planlanan_zaman = baslangic_tarihi + timedelta(hours=urun_sayac * 4)
            
            rows_to_add.append([
                planlanan_zaman.strftime('%d/%m/%Y'),
                planlanan_zaman.strftime('%H:%M'),
                reklam_metni,
                url,
                url
            ])
            urun_sayac += 1
    
    try:
        body = {'values': rows_to_add}
        result = service.spreadsheets().values().append(
            spreadsheetId=SPREADSHEET_ID,
            range='Sheet1!A2:E',
            valueInputOption='RAW',
            insertDataOption='INSERT_ROWS',
            body=body
        ).execute()
        
        print(f"İşlem tamam! {urun_sayac} adet ürün başarıyla Google Sheets'e aktarıldı.")
        print(f"Eklenen satır sayısı: {result.get('updates').get('updatedRows')}")
        
    except HttpError as e:
        print(f"Google Sheets API Hatası: {e}")
        print(f"İZİN HATASI: Service account email'i ({service_account_email}) Google Sheets'e 'Düzenleyici' olarak eklenmedi!")
        print(f"Lütfen şu adımları yapın:")
        print(f"1. Google Sheets'i açın: https://docs.google.com/spreadsheets/d/{SPREADSHEET_ID}")
        print(f"2. Paylaş butonuna tıklayın")
        print(f"3. Bu email'i girin: {service_account_email}")
        print(f"4. 'Düzenleyici' izni verin")
    except Exception as e:
        print(f"Beklenmeyen bir hata oluştu: {e}")

if __name__ == "__main__":
    poster_agent()