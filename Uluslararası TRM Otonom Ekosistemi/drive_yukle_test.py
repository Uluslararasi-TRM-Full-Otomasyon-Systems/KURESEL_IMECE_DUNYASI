# drive_yukle_test.py
import os
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# ---------- KESİNLİKLE DÜZENLEMEN GEREKEN YERLER ----------
# 1. JSON dosyanın TAM ADI (Uzantısı .json OLMALI)
SERVICE_ACCOUNT_FILE = 'robot JSON dosyası.json'  # 📍 Burayı düzelttik

# 2. Drive'daki hedef klasörünün ID'si
KLASOR_ID = '1-Pzln6xLr71sPOQsd4CXi49ERMIc9tmr'

# 3. Yüklenecek test dosyasının YOLU (Bu klasörde basit bir test.txt oluştur)
DOSYA_YOLU = 'test.txt'  # 📍 Bu dosyayı da oluşturman lazım
# ------------------------------------------------

SCOPES = ['https://www.googleapis.com/auth/drive']

def drive_yukle():
    print("="*50)
    print("🔄 DRIVE'A YÜKLEME BAŞLIYOR...")
    print("="*50)

    # 1. JSON dosyasını kontrol et
    if not os.path.exists(SERVICE_ACCOUNT_FILE):
        print(f"❌ HATA: JSON dosyası BULUNAMADI! \n   Aranan: '{SERVICE_ACCOUNT_FILE}'")
        print("💡 ÇÖZÜM: Dosya adını kontrol et ve script'le aynı klasörde olduğundan emin ol.")
        return

    print(f"✅ 1/3 JSON dosyası bulundu: {SERVICE_ACCOUNT_FILE}")

    # 2. Test dosyasını kontrol et
    if not os.path.exists(DOSYA_YOLU):
        print(f"❌ HATA: Yüklenecek dosya BULUNAMADI! \n   Aranan: '{DOSYA_YOLU}'")
        print("💡 ÇÖZÜM: Bu klasöre 'test.txt' adında bir dosya oluştur.")
        return

    print(f"✅ 2/3 Yüklenecek dosya bulundu: {DOSYA_YOLU}")

    try:
        # 3. Servis hesabı ile bağlan
        creds = service_account.Credentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE, scopes=SCOPES)
        service = build('drive', 'v3', credentials=creds)

        print(f"✅ 3/3 Drive bağlantısı başarılı. Yükleniyor...")

        # 4. Dosyayı yükle
        file_metadata = {'name': os.path.basename(DOSYA_YOLU), 'parents': [KLASOR_ID]}
        media = MediaFileUpload(DOSYA_YOLU, resumable=True)

        yuklenen_dosya = service.files().create(body=file_metadata,
                                              media_body=media,
                                              fields='id, webViewLink').execute()

        print("\n" + "="*50)
        print("🎉 TEBRİKLER! YÜKLEME BAŞARILI! 🎉")
        print(f"📄 Dosya Adı: {os.path.basename(DOSYA_YOLU)}")
        print(f"🆔 Dosya ID'si: {yuklenen_dosya.get('id')}")
        print(f"🌐 Drive'daki Linki: {yuklenen_dosya.get('webViewLink')}")
        print("="*50)

    except Exception as e:
        print(f"\n❌ KRİTİK HATA: {e}")
        print("💡 GENEL ÇÖZÜM: İnternet bağlantını kontrol et, proje ID'ni ve JSON'u kontrol et.")

if __name__ == '__main__':
    drive_yukle()
