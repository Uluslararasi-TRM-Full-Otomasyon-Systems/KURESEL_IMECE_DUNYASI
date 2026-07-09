# get_refresh_token.py
# Google Drive Refresh Token Alma - 2FA Destekli
# Bu script, 2 Adimli Dogrulama (2FA) acik hesaplarla da calisir

import os
import json
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials

# Google Drive API icin gerekli izinler
SCOPES = ['https://www.googleapis.com/auth/drive']

def main():
    print("=" * 60)
    print("🔄 GOOGLE DRIVE REFRESH TOKEN ALMA (2FA DESTEKLI)")
    print("=" * 60)
    
    # credentials.json dosyasini kontrol et
    if not os.path.exists('credentials.json'):
        print("❌ HATA: credentials.json dosyasi bulunamadi!")
        print("📁 Lutfen credentials.json dosyasini bu klasore koyun.")
        return
    
    print("✅ credentials.json bulundu.")
    print("🌐 Tarayici acilacak...")
    print("⚠️ Lutfen Google hesabiniza giris yapin ve izin verin.")
    print("=" * 60)
    
    try:
        # OAuth akisini baslat
        flow = InstalledAppFlow.from_client_secrets_file(
            'credentials.json', 
            SCOPES
        )
        
        # Local server ile yetkilendirme
        # authorization_prompt='force' ile taze token almayi zorlar
        creds = flow.run_local_server(
            port=8080,
            authorization_prompt='force',
            open_browser=True
        )
        
        print("\n" + "=" * 60)
        print("✅ BASARILI! Token bilgileri alindi:")
        print("=" * 60)
        
        # Refresh Token'i goster
        if creds.refresh_token:
            print(f"\n🔑 REFRESH TOKEN:")
            print(f"{creds.refresh_token}")
        else:
            print("\n⚠️ Refresh token alinamadi!")
            print("📝 Eger zaten bir token aldiysaniz, bu normal olabilir.")
            print("🔄 Varolan token'i kullanmaya devam edin.")
        
        # Access Token'i goster (gecici)
        if creds.token:
            print(f"\n🎫 ACCESS TOKEN (gecici):")
            print(f"{creds.token[:50]}...")
        
        # Token'lari dosyaya kaydet
        token_data = {
            'token': creds.token,
            'refresh_token': creds.refresh_token,
            'token_uri': creds.token_uri,
            'client_id': creds.client_id,
            'client_secret': creds.client_secret,
            'scopes': creds.scopes
        }
        
        with open('token.json', 'w') as f:
            json.dump(token_data, f, indent=2)
        
        print(f"\n💾 Token bilgileri 'token.json' dosyasina kaydedildi.")
        
        print("\n" + "=" * 60)
        print("📋 secrets.env dosyasina EKLEYIN:")
        print("=" * 60)
        
        if creds.refresh_token:
            print(f"GOOGLE_REFRESH_TOKEN={creds.refresh_token}")
        else:
            print("GOOGLE_REFRESH_TOKEN= (refresh_token alinamadi, varolani kullanin)")
        
        print(f"GOOGLE_CLIENT_ID={creds.client_id}")
        print(f"GOOGLE_CLIENT_SECRET={creds.client_secret}")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ HATA: {e}")
        print("\n🔧 COZUM ONERILERI:")
        print("1. credentials.json dosyasinin dogru oldugundan emin olun")
        print("2. Tarayicida dogru Google hesabiyla giris yaptiginizdan emin olun")
        print("3. Izin ekraninda 'Devam Et' butonuna tiklayin")
        print("4. Guvenlik duvari 8080 portunu engellemiyor mu kontrol edin")

if __name__ == '__main__':
    main()
