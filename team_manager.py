import csv
import os
from datetime import datetime

# ============================================
# ENGELLI EKIP YONETIM SISTEMI
# ============================================

TEAM_FILE = "team_list.csv"

# ============================================
# 1. YENI EKIP UYESI EKLEME
# ============================================
def add_team_member(name, disability, platform, account, iban, commission_rate):
    """Yeni engelli ekip uyesi ekler"""
    
    # Dosya yoksa basliklari olustur
    if not os.path.exists(TEAM_FILE):
        with open(TEAM_FILE, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['ID', 'Ad Soyad', 'Engel Durumu', 'Platform', 
                            'Hesap', 'IBAN', 'Komisyon %', 'Kayit Tarihi', 'Toplam Kazanc'])
    
    # Yeni ID olustur
    with open(TEAM_FILE, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        next(reader)  # Basligi atla
        rows = list(reader)
        new_id = len(rows) + 1001
    
    # Yeni uyeyi ekle
    with open(TEAM_FILE, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([
            new_id, name, disability, platform, account, 
            iban, commission_rate, datetime.now().strftime("%d.%m.%Y"), 0
        ])
    
    print(f"✅ Yeni uye eklendi: {name} (ID: {new_id})")
    return new_id

# ============================================
# 2. EKIP LISTESINI GOSTER
# ============================================
def show_team():
    """Tum ekip uyelerini listeler"""
    
    if not os.path.exists(TEAM_FILE):
        print("⚠️ Henuz ekip uyesi yok!")
        return
    
    with open(TEAM_FILE, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        rows = list(reader)
    
    if len(rows) <= 1:
        print("⚠️ Henuz ekip uyesi yok!")
        return
    
    print("\n" + "="*80)
    print(f"👥 ENGELLI EKIP LISTESI - {len(rows)-1} KISI")
    print("="*80)
    
    for row in rows[1:]:  # Basligi atla
        print(f"🆔 {row[0]} | {row[1]} | {row[2]} | {row[3]} | {row[4]} | {row[7]} TL")

# ============================================
# 3. KOMISYON EKLE
# ============================================
def add_commission(member_id, sale_amount):
    """Satistan komisyon ekler"""
    
    if not os.path.exists(TEAM_FILE):
        print("❌ Ekip listesi bulunamadi!")
        return
    
    # Dosyayi oku
    with open(TEAM_FILE, 'r', encoding='utf-8') as f:
        rows = list(csv.reader(f))
    
    # Uyeyi bul
    found = False
    for i, row in enumerate(rows):
        if i > 0 and row[0] == str(member_id):  # Baslik degilse ve ID eslesiyorsa
            commission_rate = float(row[6])
            commission = sale_amount * commission_rate / 100
            current_total = float(row[8])
            row[8] = str(current_total + commission)
            found = True
            print(f"💰 {row[1]}'e {commission} TL komisyon eklendi (Toplam: {row[8]} TL)")
            break
    
    if not found:
        print(f"❌ ID {member_id} bulunamadi!")
        return
    
    # Dosyayi guncelle
    with open(TEAM_FILE, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerows(rows)

# ============================================
# 4. AYLIK ODEME RAPORU
# ============================================
def payment_report():
    """Aylik odeme raporu hazirlar"""
    
    if not os.path.exists(TEAM_FILE):
        print("⚠️ Ekip listesi yok!")
        return
    
    with open(TEAM_FILE, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        rows = list(reader)
    
    if len(rows) <= 1:
        print("⚠️ Ekip uyesi yok!")
        return
    
    print("\n" + "="*80)
    print(f"💰 AYLIK ODEME RAPORU - {datetime.now().strftime('%B %Y')}")
    print("="*80)
    
    total = 0
    for row in rows[1:]:
        print(f"🆔 {row[0]} | {row[1]} | IBAN: {row[5]} | {row[8]} TL")
        total += float(row[8])
    
    print("="*80)
    print(f"TOPLAM ODEME: {total} TL")
    
    # Odeme yapildiktan sonra sifirla
    confirm = input("\nOdemeler yapildi mi? (e/h): ")
    if confirm.lower() == 'e':
        for i in range(1, len(rows)):
            rows[i][8] = '0'
        
        with open(TEAM_FILE, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerows(rows)
        print("✅ Odemeler yapildi, hesaplar sifirlandi!")

# ============================================
# 5. TEST KOMUTLARI
# ============================================
if __name__ == "__main__":
    print("🚀 ENGELLI EKIP YONETIM SISTEMI")
    print("="*40)
    
    while True:
        print("\n1️⃣ Yeni uye ekle")
        print("2️⃣ Ekip listesini goster")
        print("3️⃣ Komisyon ekle")
        print("4️⃣ Aylik odeme raporu")
        print("5️⃣ Cikis")
        
        choice = input("\nSeciminiz: ")
        
        if choice == '1':
            name = input("Ad Soyad: ")
            disability = input("Engel durumu: ")
            platform = input("Platform: ")
            account = input("Hesap adi: ")
            iban = input("IBAN: ")
            rate = float(input("Komisyon orani (%): "))
            add_team_member(name, disability, platform, account, iban, rate)
        
        elif choice == '2':
            show_team()
        
        elif choice == '3':
            member_id = input("Uye ID: ")
            amount = float(input("Satis tutari (TL): "))
            add_commission(member_id, amount)
        
        elif choice == '4':
            payment_report()
        
        elif choice == '5':
            print("👋 Gorusmek uzere!")
            break
