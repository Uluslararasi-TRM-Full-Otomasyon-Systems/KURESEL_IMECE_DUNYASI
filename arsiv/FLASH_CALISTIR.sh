#!/bin/bash
# TRM Nirvana v3.0 - Flash Bellekten Çalıştırıcı

echo "==============================================="
echo "    TRM NİRVANA v3.0 - FLASH BELLEK"
echo "==============================================="
echo "🚀 Flash bellekten direkt çalıştırılıyor..."
echo ""

# Flash bellekteki dizine git
cd "/media/$(whoami)/ULUSLARASI-TRM-FULL-OTOMASYON-SISTEMI" 2>/dev/null || \
cd "/mnt/$(whoami)/ULUSLARASI-TRM-FULL-OTOMASYON-SISTEMI" 2>/dev/null || \
cd "$(find /media -name 'ULUSLARASI-TRM-FULL-OTOMASYON-SISTEMI' -type d 2>/dev/null | head -1)" 2>/dev/null || {
    echo "❌ Flash bellek bulunamadı!"
    exit 1
}

if [ ! -f "START_NIRVANA.py" ]; then
    echo "❌ START_NIRVANA.py bulunamadı!"
    exit 1
fi

echo "✅ Flash bellekteki sistem bulundu."

# Python kontrol
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 kurulu değil!"
    exit 1
fi

echo "✅ Python3 mevcut."

# Kütüphaneleri kontrol et
python3 -c "import telethon, aiohttp, bs4, openai, anthropic, pandas, requests" 2>/dev/null || {
    echo "⚠️  Kütüphaneler eksik, yükleniyor..."
    pip3 install -r requirements.txt --quiet
}

echo "✅ Kütüphaneler hazır."

# Ortam değişkenleri
if [ ! -f "secrets.env" ]; then
    echo "⚠️  secrets.env oluşturuluyor..."
    cat > secrets.env << EOF
# TRM Full Otomasyon Sistemi - Ortam Değişkenleri
TELEGRAM_API_ID=your_telegram_api_id
TELEGRAM_API_HASH=your_telegram_api_hash
TELEGRAM_PHONE=+90555xxxxxxx
DEEPSEEK_API_KEY=your_deepseek_api_key
CLAUDE_API_KEY=your_claude_api_key
FACEBOOK_ACCESS_TOKEN=your_facebook_access_token
INSTAGRAM_ACCESS_TOKEN=your_instagram_access_token
TIKTOK_ACCESS_TOKEN=your_tiktok_access_token
YOUTUBE_API_KEY=your_youtube_api_key
GOOGLE_DRIVE_FOLDER_ID=your_google_drive_folder_id
STORE_URL=https://trendurunlermarket.com
COMMISSION_THRESHOLD=20.0
CHECK_INTERVAL=300
MAX_PRODUCTS_PER_DAY=50
EOF
    echo "✅ secrets.env oluşturuldu."
fi

# Dizinleri oluştur
mkdir -p logs data temp_photos temp_docs

echo "✅ Dizinler hazır."

echo ""
echo "🎯 BAŞLATMA SEÇENEKLERİ:"
echo "1. 🚀 Sadece Panel"
echo "2. 🤖 Full Otomasyon"
echo "3. 📊 Sadece Orchestrator"
echo "4. ❌ Çıkış"

while true; do
    read -p "Seçiminiz (1-4): " choice
    
    case $choice in
        1)
            echo "🚀 Panel başlatılıyor..."
            python3 START_NIRVANA.py &
            echo "🌐 http://localhost:9000"
            break
            ;;
        2)
            echo "🤖 Full otomasyon başlatılıyor..."
            python3 START_NIRVANA.py &
            sleep 3
            python3 main_orchestrator.py
            break
            ;;
        3)
            echo "📊 Orchestrator başlatılıyor..."
            python3 main_orchestrator.py
            break
            ;;
        4)
            echo "👋 Çıkış yapılıyor..."
            exit 0
            ;;
        *)
            echo "❌ Geçersiz seçenek!"
            ;;
    esac
done

echo "✅ TRM Nirvana çalışıyor..."
