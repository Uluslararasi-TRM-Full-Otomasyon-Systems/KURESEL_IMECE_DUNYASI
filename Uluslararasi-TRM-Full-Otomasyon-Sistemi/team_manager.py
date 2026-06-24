import csv
import os
from datetime import datetime

# ============================================
# ENGELLİ EKİP YÖNETİM SİSTEMİ
# ============================================

TEAM_FILE = "team_list.csv"

# ============================================
# 1. YENİ EKİP ÜYESİ EKLEME
# ============================================
def add_team_member(name, disability, platform, account, iban, commission_rate):
    """Yeni engelli ekip üyesi ekler"""
    
    # Dosya yoksa başlıkları oluştur
    if not os.path.exists(TEAM_FILE):
        with open(TEAM_FILE, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['ID', 'Ad Soyad', 'Engel Durumu', 'Platform', 
                            'Hesap', 'IBAN', 'Komisyon %', 'Kayıt Tarihi', 'Toplam Kazanç'])
    
    # Yeni ID oluştur
    with open(TEAM_FILE, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        next(reader)  # Başlığı atla
        rows = list(reader)
        new_id = len(rows) + 1001
    
    # Yeni üyeyi ekle
    with open(TEAM_FILE, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([
            new_id, name, disability, platform, account, 
            iban, commission_rate, datetime.now().strftime("%d.%m.%Y"), 0
        ])
    
    print(f"✅ Yeni üye eklendi: {name} (ID: {new_id})")
    return new_id

# ============================================
# 2. EKİP LİSTESİNİ GÖSTER
# ============================================
def show_team():
    """Tüm ekip üyelerini listeler"""
    
    if not os.path.exists(TEAM_FILE):
        print("⚠️ Henüz ekip üyesi yok!")
        return
    
    with open(TEAM_FILE, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        rows = list(reader)
    
    if len(rows) <= 1:
        print("⚠️ Henüz ekip üyesi yok!")
        return
    
    print("\n" + "="*80)
    print(f"👥 ENGELLİ EKİP LİSTESİ - {len(rows)-1} KİŞİ")
    print("="*80)
    
    for row in rows[1:]:  # Başlığı atla
        print(f"🆔 {row[0]} | {row[1]} | {row[2]} | {row[3]} | {row[4]} | {row[7]} TL")

# ============================================
# 3. KOMİSYON EKLE
# ============================================
def add_commission(member_id, sale_amount):
    """Satıştan komisyon ekler"""
    
    if not os.path.exists(TEAM_FILE):
        print("❌ Ekip listesi bulunamadı!")
        return
    
    # Dosyayı oku
    with open(TEAM_FILE, 'r', encoding='utf-8') as f:
        rows = list(csv.reader(f))
    
    # Üyeyi bul
    found = False
    for i, row in enumerate(rows):
        if i > 0 and row[0] == str(member_id):  # Başlık değilse ve ID eşleşiyorsa
            commission_rate = float(row[6])
            commission = sale_amount * commission_rate / 100
            current_total = float(row[8])
            row[8] = str(current_total + commission)
            found = True
            print(f"💰 {row[1]}'e {commission} TL komisyon eklendi (Toplam: {row[8]} TL)")
            break
    
    if not found:
        print(f"❌ ID {member_id} bulunamadı!")
        return
    
    # Dosyayı güncelle
    with open(TEAM_FILE, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerows(rows)

# ============================================
# 4. AYLIK ÖDEME RAPORU
# ============================================
def payment_report():
    """Aylık ödeme raporu hazırlar"""
    
    if not os.path.exists(TEAM_FILE):
        print("⚠️ Ekip listesi yok!")
        return
    
    with open(TEAM_FILE, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        rows = list(reader)
    
    if len(rows) <= 1:
        print("⚠️ Ekip üyesi yok!")
        return
    
    print("\n" + "="*80)
    print(f"💰 AYLIK ÖDEME RAPORU - {datetime.now().strftime('%B %Y')}")
    print("="*80)
    
    total = 0
    for row in rows[1:]:
        print(f"🆔 {row[0]} | {row[1]} | IBAN: {row[5]} | {row[8]} TL")
        total += float(row[8])
    
    print("="*80)
    print(f"TOPLAM ÖDEME: {total} TL")
    
    # Ödeme yapıldıktan sonra sıfırla
    confirm = input("\nÖdemeler yapıldı mı? (e/h): ")
    if confirm.lower() == 'e':
        for i in range(1, len(rows)):
            rows[i][8] = '0'
        
        with open(TEAM_FILE, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerows(rows)
        print("✅ Ödemeler yapıldı, hesaplar sıfırlandı!")

# ============================================
# 5. TEST KOMUTLARI
# ============================================
if __name__ == "__main__":
    print("🚀 ENGELLİ EKİP YÖNETİM SİSTEMİ")
    print("="*40)
    
    while True:
        print("\n1️⃣ Yeni üye ekle")
        print("2️⃣ Ekip listesini göster")
        print("3️⃣ Komisyon ekle")
        print("4️⃣ Aylık ödeme raporu")
        print("5️⃣ Çıkış")
        
        choice = input("\nSeçiminiz: ")
        
        if choice == '1':
            name = input("Ad Soyad: ")
            disability = input("Engel durumu: ")
            platform = input("Platform: ")
            account = input("Hesap adı: ")
            iban = input("IBAN: ")
            rate = float(input("Komisyon oranı (%): "))
            add_team_member(name, disability, platform, account, iban, rate)
        
        elif choice == '2':
            show_team()
        
        elif choice == '3':
            member_id = input("Üye ID: ")
            amount = float(input("Satış tutarı (TL): "))
            add_commission(member_id, amount)
        
        elif choice == '4':
            payment_report()
        
        elif choice == '5':
            print("👋 Görüşmek üzere!")
            break
