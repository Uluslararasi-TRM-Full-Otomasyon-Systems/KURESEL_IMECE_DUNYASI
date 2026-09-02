# drive_yukle_test.py
import os
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# ---------- KESINLIKLE DUZENLEMEN GEREKEN YERLER ----------
# 1. JSON dosyanin TAM ADI (Uzantisi .json OLMALI)
SERVICE_ACCOUNT_FILE = 'robot JSON dosyasi.json'  # 📍 Burayi duzelttik

# 2. Drive'daki hedef klasorunun ID'si
KLASOR_ID = '1-Pzln6xLr71sPOQsd4CXi49ERMIc9tmr'

# 3. Yuklenecek test dosyasinin YOLU (Bu klasorde basit bir test.txt olustur)
DOSYA_YOLU = 'test.txt'  # 📍 Bu dosyayi da olusturman lazim
# ------------------------------------------------

SCOPES = ['https://www.googleapis.com/auth/drive']

def drive_yukle():
    print("="*50)
    print("🔄 DRIVE'A YUKLEME BASLIYOR...")
    print("="*50)

    # 1. JSON dosyasini kontrol et
    if not os.path.exists(SERVICE_ACCOUNT_FILE):
        print(f"❌ HATA: JSON dosyasi BULUNAMADI! \n   Aranan: '{SERVICE_ACCOUNT_FILE}'")
        print("💡 COZUM: Dosya adini kontrol et ve script'le ayni klasorde oldugundan emin ol.")
        return

    print(f"✅ 1/3 JSON dosyasi bulundu: {SERVICE_ACCOUNT_FILE}")

    # 2. Test dosyasini kontrol et
    if not os.path.exists(DOSYA_YOLU):
        print(f"❌ HATA: Yuklenecek dosya BULUNAMADI! \n   Aranan: '{DOSYA_YOLU}'")
        print("💡 COZUM: Bu klasore 'test.txt' adinda bir dosya olustur.")
        return

    print(f"✅ 2/3 Yuklenecek dosya bulundu: {DOSYA_YOLU}")

    try:
        # 3. Servis hesabi ile baglan
        creds = service_account.Credentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE, scopes=SCOPES)
        service = build('drive', 'v3', credentials=creds)

        print(f"✅ 3/3 Drive baglantisi basarili. Yukleniyor...")

        # 4. Dosyayi yukle
        file_metadata = {'name': os.path.basename(DOSYA_YOLU), 'parents': [KLASOR_ID]}
        media = MediaFileUpload(DOSYA_YOLU, resumable=True)

        yuklenen_dosya = service.files().create(body=file_metadata,
                                              media_body=media,
                                              fields='id, webViewLink').execute()

        print("\n" + "="*50)
        print("🎉 TEBRIKLER! YUKLEME BASARILI! 🎉")
        print(f"📄 Dosya Adi: {os.path.basename(DOSYA_YOLU)}")
        print(f"🆔 Dosya ID'si: {yuklenen_dosya.get('id')}")
        print(f"🌐 Drive'daki Linki: {yuklenen_dosya.get('webViewLink')}")
        print("="*50)

    except Exception as e:
        print(f"\n❌ KRITIK HATA: {e}")
        print("💡 GENEL COZUM: Internet baglantini kontrol et, proje ID'ni ve JSON'u kontrol et.")

if __name__ == '__main__':
    drive_yukle()
