import json
import os
from datetime import datetime, timedelta

try:
    from google.oauth2 import service_account
    from googleapiclient.discovery import build
except ImportError:
    print("HATA: Gerekli kütüphaneler yüklü değil.")
    exit(1)

def dnp_ajan_islem(urun_adi):
    # 161. Ajan: Parametreleri uluslararası ağa uygun hale getirir
    print(f"🧠 161. Ajan (DNP) Aktif: '{urun_adi}' için parametreler optimize ediliyor...")
    return True

def poster_agent():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    input_file = os.path.join(base_dir, 'trend_raporlari.json')
    credentials_file = os.path.join(base_dir, 'service_account.json')
    SPREADSHEET_ID = '1Ttk5BFBmcrbKaEzMrvykOALcGYj18wibb7ctNsqIOQM'
    
    if not os.path.exists(credentials_file):
        print(f"HATA: {credentials_file} bulunamadı!")
        return
    
    try:
        credentials = service_account.Credentials.from_service_account_file(
            credentials_file, scopes=['https://www.googleapis.com/auth/spreadsheets']
        )
        service = build('sheets', 'v4', credentials=credentials)
    except Exception as e:
        print(f"HATA: Kimlik doğrulama başarısız: {e}")
        return
    
    if not os.path.exists(input_file):
        print(f"HATA: {input_file} bulunamadı!")
        return
        
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    baslangic_tarihi = datetime.now() + timedelta(days=1)
    urun_sayac = 0
    rows_to_add = []
    
    for item in data:
        urun_adi = item.get('product_name') or item.get('title') or "Trend Ürün"
        url = item.get('product_url', 'https://trendurunlermarket.com')
        komisyon_orani = float(item.get('commission_rate', 0.15))
        
        if komisyon_orani < 0.10:
            print(f"[DNP-UYARI]: {urun_adi} elendi. Düşük kâr marjı.")
            continue 
        
        reklam_metni = f"🔥 {urun_adi} - Trendlerde! Detaylar için linke tıklayın! 👇"
        planlanan_zaman = baslangic_tarihi + timedelta(hours=urun_sayac * 4)
        
        rows_to_add.append([
            planlanan_zaman.strftime('%d/%m/%Y'),
            planlanan_zaman.strftime('%H:%M'),
            reklam_metni,
            url,
            url
        ])
        urun_sayac += 1
    
    if rows_to_add:
        try:
            body = {'values': rows_to_add}
            service.spreadsheets().values().append(
                spreadsheetId=SPREADSHEET_ID,
                range='Sheet1!A2:E',
                valueInputOption='RAW',
                insertDataOption='INSERT_ROWS',
                body=body
            ).execute()
            print(f"İşlem tamam! {urun_sayac} adet ürün başarıyla aktarıldı.")
            
            # 161. Ajan tetikleyici
            for item in data:
                dnp_ajan_islem(item.get('product_name') or item.get('title', 'Trend Ürün'))
        except Exception as e:
            print(f"Hata: {e}")
    else:
        print("Aktarılacak uygun ürün bulunamadı.")

if __name__ == "__main__":
    poster_agent()