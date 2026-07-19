import sys
import io
import json
import os
from datetime import datetime

# UTF-8 encoding fix for Windows console
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def generate_demo_products():
    """Demo ürün verisi oluştur"""
    
    demo_products = [
        {
            "firma": "Trendurunlermarket",
            "urun_adi": "Organik Zeytin Yağı 1L",
            "aciklama": "Organik Zeytin Yağı 1L 🔥 en uygun fiyat trendurunlermarket.com'da! #Trendurunlermarket",
            "gorsel_url": "https://example.com/zeytinyagi.jpg",
            "urun_linki": "https://www.trendurunlermarket.com/organik-zeytinyagi",
            "hashtagler": "#Trendurunlermarket #kampanya #indirim #alışveriş #fırsat",
            "fiyat": "250.00",
            "kaynak": "https://www.trendurunlermarket.com",
            "toplanma_tarihi": datetime.now().isoformat()
        },
        {
            "firma": "Trendurunlermarket",
            "urun_adi": "Kozmetik Cilt Bakım Seti",
            "aciklama": "Kozmetik Cilt Bakım Seti 🔥 en uygun fiyat trendurunlermarket.com'da! #Trendurunlermarket",
            "gorsel_url": "https://example.com/ciltbakim.jpg",
            "urun_linki": "https://www.trendurunlermarket.com/cilt-bakim-seti",
            "hashtagler": "#Trendurunlermarket #kampanya #indirim #alışveriş #fırsat",
            "fiyat": "450.00",
            "kaynak": "https://www.trendurunlermarket.com",
            "toplanma_tarihi": datetime.now().isoformat()
        },
        {
            "firma": "Trendurunlermarket",
            "urun_adi": "Nemlendirici Krem 50ml",
            "aciklama": "Nemlendirici Krem 50ml 🔥 en uygun fiyat trendurunlermarket.com'da! #Trendurunlermarket",
            "gorsel_url": "https://example.com/nemlendirici.jpg",
            "urun_linki": "https://www.trendurunlermarket.com/nemlendirici-krem",
            "hashtagler": "#Trendurunlermarket #kampanya #indirim #alışveriş #fırsat",
            "fiyat": "180.00",
            "kaynak": "https://www.trendurunlermarket.com",
            "toplanma_tarihi": datetime.now().isoformat()
        },
        {
            "firma": "Trendurunlermarket",
            "urun_adi": "Şampuan 500ml",
            "aciklama": "Şampuan 500ml 🔥 en uygun fiyat trendurunlermarket.com'da! #Trendurunlermarket",
            "gorsel_url": "https://example.com/sampuan.jpg",
            "urun_linki": "https://www.trendurunlermarket.com/sampuan",
            "hashtagler": "#Trendurunlermarket #kampanya #indirim #alışveriş #fırsat",
            "fiyat": "95.00",
            "kaynak": "https://www.trendurunlermarket.com",
            "toplanma_tarihi": datetime.now().isoformat()
        },
        {
            "firma": "Trendurunlermarket",
            "urun_adi": "Doğal Bal 1kg",
            "aciklama": "Doğal Bal 1kg 🔥 en uygun fiyat trendurunlermarket.com'da! #Trendurunlermarket",
            "gorsel_url": "https://example.com/bal.jpg",
            "urun_linki": "https://www.trendurunlermarket.com/dogal-bal",
            "hashtagler": "#Trendurunlermarket #kampanya #indirim #alışveriş #fırsat",
            "fiyat": "320.00",
            "kaynak": "https://www.trendurunlermarket.com",
            "toplanma_tarihi": datetime.now().isoformat()
        },
        {
            "firma": "Trendurunlermarket",
            "urun_adi": "Spirulina Tablet 100'lu",
            "aciklama": "Spirulina Tablet 100'lü 🔥 en uygun fiyat trendurunlermarket.com'da! #Trendurunlermarket",
            "gorsel_url": "https://example.com/spirulina.jpg",
            "urun_linki": "https://www.trendurunlermarket.com/spirulina",
            "hashtagler": "#Trendurunlermarket #kampanya #indirim #alışveriş #fırsat",
            "fiyat": "150.00",
            "kaynak": "https://www.trendurunlermarket.com",
            "toplanma_tarihi": datetime.now().isoformat()
        },
        {
            "firma": "Trendurunlermarket",
            "urun_adi": "Vitamin C Serum 30ml",
            "aciklama": "Vitamin C Serum 30ml 🔥 en uygun fiyat trendurunlermarket.com'da! #Trendurunlermarket",
            "gorsel_url": "https://example.com/vitaminc.jpg",
            "urun_linki": "https://www.trendurunlermarket.com/vitamin-c-serum",
            "hashtagler": "#Trendurunlermarket #kampanya #indirim #alışveriş #fırsat",
            "fiyat": "275.00",
            "kaynak": "https://www.trendurunlermarket.com",
            "toplanma_tarihi": datetime.now().isoformat()
        },
        {
            "firma": "Trendurunlermarket",
            "urun_adi": "Protein Tozu 1kg",
            "aciklama": "Protein Tozu 1kg 🔥 en uygun fiyat trendurunlermarket.com'da! #Trendurunlermarket",
            "gorsel_url": "https://example.com/protein.jpg",
            "urun_linki": "https://www.trendurunlermarket.com/protein-tozu",
            "hashtagler": "#Trendurunlermarket #kampanya #indirim #alışveriş #fırsat",
            "fiyat": "550.00",
            "kaynak": "https://www.trendurunlermarket.com",
            "toplanma_tarihi": datetime.now().isoformat()
        },
        {
            "firma": "Trendurunlermarket",
            "urun_adi": "Omega 3 Kapsül 60'lı",
            "aciklama": "Omega 3 Kapsül 60'lı 🔥 en uygun fiyat trendurunlermarket.com'da! #Trendurunlermarket",
            "gorsel_url": "https://example.com/omega3.jpg",
            "urun_linki": "https://www.trendurunlermarket.com/omega-3",
            "hashtagler": "#Trendurunlermarket #kampanya #indirim #alışveriş #fırsat",
            "fiyat": "185.00",
            "kaynak": "https://www.trendurunlermarket.com",
            "toplanma_tarihi": datetime.now().isoformat()
        },
        {
            "firma": "Trendurunlermarket",
            "urun_adi": "Aloe Vera Jel 200ml",
            "aciklama": "Aloe Vera Jel 200ml 🔥 en uygun fiyat trendurunlermarket.com'da! #Trendurunlermarket",
            "gorsel_url": "https://example.com/aloe.jpg",
            "urun_linki": "https://www.trendurunlermarket.com/aloe-vera",
            "hashtagler": "#Trendurunlermarket #kampanya #indirim #alışveriş #fırsat",
            "fiyat": "120.00",
            "kaynak": "https://www.trendurunlermarket.com",
            "toplanma_tarihi": datetime.now().isoformat()
        }
    ]
    
    return demo_products

def main():
    print("🚀 TRM Demo Ürün Oluşturucu Başlatılıyor...")
    print("🎯 Hedef: Sistemi test etmek için demo ürün verisi oluştur")
    print("=" * 60)
    
    demo_products = generate_demo_products()
    
    # Ürünleri JSON dosyasına kaydet
    output_dir = os.path.dirname(os.path.abspath(__file__))
    output_file = os.path.join(output_dir, "toplanan_urunler.json")
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(demo_products, f, ensure_ascii=False, indent=2)
    
    print(f"\n" + "=" * 60)
    print(f"🎉 DEMO ÜRÜNLER SİSTEME YÜKLENDİ!")
    print(f"📊 Toplam {len(demo_products)} demo ürün oluşturuldu")
    print(f"💾 Kayıt dosyası: {output_file}")
    print(f"⏰ Tamamlanma zamanı: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    print("\n📋 Ürün Listesi:")
    for i, product in enumerate(demo_products, 1):
        print(f"   {i}. {product['urun_adi']} - {product['fiyat']} TL")

if __name__ == "__main__":
    main()
