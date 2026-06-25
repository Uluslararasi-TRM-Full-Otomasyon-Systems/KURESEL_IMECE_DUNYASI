# get_refresh_token.py
# Google Drive Refresh Token Alma - 2FA Destekli
# Bu script, 2 Adımlı Doğrulama (2FA) açık hesaplarla da çalışır

import os
import json
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials

# Google Drive API için gerekli izinler
SCOPES = ['https://www.googleapis.com/auth/drive']

def main():
    print("=" * 60)
    print("🔄 GOOGLE DRIVE REFRESH TOKEN ALMA (2FA DESTEKLİ)")
    print("=" * 60)
    
    # credentials.json dosyasını kontrol et
    if not os.path.exists('credentials.json'):
        print("❌ HATA: credentials.json dosyası bulunamadı!")
        print("📁 Lütfen credentials.json dosyasını bu klasöre koyun.")
        return
    
    print("✅ credentials.json bulundu.")
    print("🌐 Tarayıcı açılacak...")
    print("⚠️ Lütfen Google hesabınıza giriş yapın ve izin verin.")
    print("=" * 60)
    
    try:
        # OAuth akışını başlat
        flow = InstalledAppFlow.from_client_secrets_file(
            'credentials.json', 
            SCOPES
        )
        
        # Local server ile yetkilendirme
        # authorization_prompt='force' ile taze token almayı zorlar
        creds = flow.run_local_server(
            port=8080,
            authorization_prompt='force',
            open_browser=True
        )
        
        print("\n" + "=" * 60)
        print("✅ BAŞARILI! Token bilgileri alındı:")
        print("=" * 60)
        
        # Refresh Token'ı göster
        if creds.refresh_token:
            print(f"\n🔑 REFRESH TOKEN:")
            print(f"{creds.refresh_token}")
        else:
            print("\n⚠️ Refresh token alınamadı!")
            print("📝 Eğer zaten bir token aldıysanız, bu normal olabilir.")
            print("🔄 Varolan token'ı kullanmaya devam edin.")
        
        # Access Token'ı göster (geçici)
        if creds.token:
            print(f"\n🎫 ACCESS TOKEN (geçici):")
            print(f"{creds.token[:50]}...")
        
        # Token'ları dosyaya kaydet
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
        
        print(f"\n💾 Token bilgileri 'token.json' dosyasına kaydedildi.")
        
        print("\n" + "=" * 60)
        print("📋 secrets.env dosyasına EKLEYİN:")
        print("=" * 60)
        
        if creds.refresh_token:
            print(f"GOOGLE_REFRESH_TOKEN={creds.refresh_token}")
        else:
            print("GOOGLE_REFRESH_TOKEN= (refresh_token alınamadı, varolanı kullanın)")
        
        print(f"GOOGLE_CLIENT_ID={creds.client_id}")
        print(f"GOOGLE_CLIENT_SECRET={creds.client_secret}")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ HATA: {e}")
        print("\n🔧 ÇÖZÜM ÖNERİLERİ:")
        print("1. credentials.json dosyasının doğru olduğundan emin olun")
        print("2. Tarayıcıda doğru Google hesabıyla giriş yaptığınızdan emin olun")
        print("3. İzin ekranında 'Devam Et' butonuna tıklayın")
        print("4. Güvenlik duvarı 8080 portunu engellemiyor mu kontrol edin")

if __name__ == '__main__':
    main()
