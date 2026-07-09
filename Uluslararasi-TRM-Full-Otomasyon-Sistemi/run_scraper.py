import sys
import os

def main():
    print("=== ACIL SATIS HAVUZU - URUN CEKME BASLIYOR ===")
    print()
    
    # Ornek urun listesi
    sample_products = [
        {
            "title": "Organik Zeytin Yağı 1L",
            "product_url": "https://www.trendyol.com/gida-saglik-ve-ozel-bakim/organik-urunler/organik-zeytin-yagi"
        },
        {
            "title": "Kozmetik Cilt Bakım Seti",
            "product_url": "https://www.trendyol.com/kozmetik/cilt-bakim/cilt-bakim-seti"
        },
        {
            "title": "Nemlendirici Krem",
            "product_url": "https://www.trendyol.com/kozmetik/cilt-bakim/nemlendirici-krem"
        },
        {
            "title": "Şampuan 500ml",
            "product_url": "https://www.trendyol.com/kozmetik/sac-bakim/sampuan"
        },
        {
            "title": "Bal 1kg",
            "product_url": "https://www.trendyol.com/gida-saglik-ve-ozel-bakim/tatli-urunler/bal"
        }
    ]
    
    # Dosyaya kaydet
    output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ACIL_SATIS_HAVUZU.txt")
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("=========================================\n")
        f.write("TRM ACIL NAKIT OTOMASYONU - ACIL SATIS HAVUZU\n")
        f.write("=========================================\n")
        f.write(f"Baslama Zamani: {__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Toplam Urun: {len(sample_products)}\n")
        f.write("=========================================\n\n")
        
        # Affiliate ID
        affiliate_id = "trendurunlermarket"
        
        for product in sample_products:
            # Linki affiliate linkine cevir
            affiliate_link = product['product_url']
            if "?" in affiliate_link:
                affiliate_link += f"&affiliate={affiliate_id}"
            else:
                affiliate_link += f"?affiliate={affiliate_id}"
            
            f.write(f"{product['title']} - {affiliate_link}\n")
    
    print(f"URUNLER DOSYAYA KAYDEDILDI!")
    print(f"Dosya Yolu: {output_path}")
    print()
    print("=== ISLEM TAMAMLANDI ===")
    
    print()
    print("Aciklama: Bu ornek listeyi gercek urunler ile guncelleyebilirsiniz!")

if __name__ == "__main__":
    main()
