import csv
import sqlite3
from datetime import datetime, timedelta

# ============================================
# KOMISYON HESAPLAMA SISTEMI
# ============================================

TEAM_FILE = "team_list.csv"
SALES_DB = "sales.db"

# ============================================
# 1. VERITABANI OLUSTUR
# ============================================
def init_database():
    """Satis veritabanini olusturur"""
    conn = sqlite3.connect(SALES_DB)
    c = conn.cursor()
    
    c.execute('''CREATE TABLE IF NOT EXISTS sales
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  member_id INTEGER,
                  member_name TEXT,
                  product_name TEXT,
                  product_price REAL,
                  commission_rate REAL,
                  commission_amount REAL,
                  sale_date TEXT,
                  status TEXT)''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS payments
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  member_id INTEGER,
                  member_name TEXT,
                  amount REAL,
                  iban TEXT,
                  payment_date TEXT,
                  month TEXT)''')
    
    conn.commit()
    conn.close()
    print("✅ Veritabani hazir!")

# ============================================
# 2. YENI SATIS EKLE
# ============================================
def add_sale(member_id, product_name, product_price):
    """Yeni satis ekler ve komisyonu hesaplar"""
    
    # Ekip uyesini bul ve komisyon oranini al
    commission_rate = 0
    member_name = ""
    
    with open(TEAM_FILE, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        next(reader)  # Basligi atla
        for row in reader:
            if row[0] == str(member_id):
                commission_rate = float(row[6])
                member_name = row[1]
                break
    
    if commission_rate == 0:
        print(f"❌ Uye ID {member_id} bulunamadi!")
        return False
    
    # Komisyon hesapla
    commission_amount = product_price * commission_rate / 100
    
    # Veritabanina ekle
    conn = sqlite3.connect(SALES_DB)
    c = conn.cursor()
    
    c.execute('''INSERT INTO sales 
                 (member_id, member_name, product_name, product_price, 
                  commission_rate, commission_amount, sale_date, status)
                 VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
              (member_id, member_name, product_name, product_price,
               commission_rate, commission_amount, datetime.now().strftime("%d.%m.%Y %H:%M"), "Beklemede"))
    
    conn.commit()
    conn.close()
    
    print(f"✅ Satis eklendi: {product_name} - {product_price} TL")
    print(f"💰 Komisyon: {commission_amount} TL (%{commission_rate})")
    return True

# ============================================
# 3. GUNLUK KOMISYON RAPORU
# ============================================
def daily_report():
    """Gunluk komisyon raporu hazirlar"""
    
    conn = sqlite3.connect(SALES_DB)
    c = conn.cursor()
    
    today = datetime.now().strftime("%d.%m.%Y")
    
    c.execute('''SELECT member_name, COUNT(*), SUM(commission_amount)
                 FROM sales WHERE sale_date LIKE ? GROUP BY member_name''',
              (f"{today}%",))
    
    rows = c.fetchall()
    
    print("\n" + "="*60)
    print(f"📊 GUNLUK KOMISYON RAPORU - {today}")
    print("="*60)
    
    if not rows:
        print("Bugun henuz satis yok!")
    else:
        total = 0
        for row in rows:
            print(f"👤 {row[0]}: {row[1]} satis - {row[2]:.2f} TL")
            total += row[2]
        print("-"*60)
        print(f"💰 TOPLAM: {total:.2f} TL")
    
    conn.close()

# ============================================
# 4. AYLIK KOMISYON RAPORU
# ============================================
def monthly_report(month=None):
    """Aylik komisyon raporu hazirlar"""
    
    if month is None:
        month = datetime.now().strftime("%m.%Y")
    
    conn = sqlite3.connect(SALES_DB)
    c = conn.cursor()
    
    c.execute('''SELECT member_name, COUNT(*), SUM(commission_amount)
                 FROM sales WHERE sale_date LIKE ? GROUP BY member_name''',
              (f"%{month}%",))
    
    rows = c.fetchall()
    
    print("\n" + "="*60)
    print(f"📅 AYLIK KOMISYON RAPORU - {month}")
    print("="*60)
    
    if not rows:
        print("Bu ay henuz satis yok!")
    else:
        total = 0
        for row in rows:
            print(f"👤 {row[0]}: {row[1]} satis - {row[2]:.2f} TL")
            total += row[2]
        print("-"*60)
        print(f"💰 TOPLAM: {total:.2f} TL")
    
    conn.close()
    return total

# ============================================
# 5. ODEME YAP
# ============================================
def make_payments():
    """Aylik odemeleri hazirlar"""
    
    conn = sqlite3.connect(SALES_DB)
    c = conn.cursor()
    
    month = datetime.now().strftime("%m.%Y")
    
    # Ekip uyelerini ve IBAN'larini al
    members = {}
    with open(TEAM_FILE, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            members[row[0]] = {
                'name': row[1],
                'iban': row[5]
            }
    
    # Bu ayki komisyonlari topla
    c.execute('''SELECT member_id, member_name, SUM(commission_amount)
                 FROM sales WHERE sale_date LIKE ? AND status = "Beklemede"
                 GROUP BY member_id''', (f"%{month}%",))
    
    payments = c.fetchall()
    
    if not payments:
        print("❌ Odenecek komisyon yok!")
        return
    
    print("\n" + "="*70)
    print(f"💰 AYLIK ODEME LISTESI - {month}")
    print("="*70)
    
    total = 0
    for payment in payments:
        member_id = str(payment[0])
        amount = payment[2]
        total += amount
        
        print(f"👤 {payment[1]} (ID: {member_id})")
        print(f"   IBAN: {members.get(member_id, {}).get('iban', 'BULUNAMADI')}")
        print(f"   TUTAR: {amount:.2f} TL")
        print("-"*40)
    
    print(f"💰 TOPLAM ODEME: {total:.2f} TL")
    
    # Onay
    confirm = input("\nOdemeleri kaydet ve durumu guncelle? (e/h): ")
    if confirm.lower() == 'e':
        for payment in payments:
            c.execute('''UPDATE sales SET status = "Odendi" 
                         WHERE member_id = ? AND sale_date LIKE ? AND status = "Beklemede"''',
                      (payment[0], f"%{month}%"))
            
            c.execute('''INSERT INTO payments (member_id, member_name, amount, iban, payment_date, month)
                         VALUES (?, ?, ?, ?, ?, ?)''',
                      (payment[0], payment[1], payment[2], 
                       members.get(str(payment[0]), {}).get('iban', ''),
                       datetime.now().strftime("%d.%m.%Y"), month))
        
        conn.commit()
        print("✅ Odemeler kaydedildi!")
    
    conn.close()

# ============================================
# 6. TEST KOMUTLARI
# ============================================
if __name__ == "__main__":
    print("💰 KOMISYON HESAPLAMA SISTEMI")
    print("="*40)
    
    # Veritabanini hazirla
    init_database()
    
    while True:
        print("\n1️⃣ Yeni satis ekle")
        print("2️⃣ Gunluk rapor")
        print("3️⃣ Aylik rapor")
        print("4️⃣ Odeme yap")
        print("5️⃣ Cikis")
        
        choice = input("\nSeciminiz: ")
        
        if choice == '1':
            member_id = input("Uye ID: ")
            product = input("Urun adi: ")
            price = float(input("Satis fiyati (TL): "))
            add_sale(member_id, product, price)
        
        elif choice == '2':
            daily_report()
        
        elif choice == '3':
            month = input("Ay (Ornek: 02.2026) - Bos birakirsan bu ay: ")
            if month:
                monthly_report(month)
            else:
                monthly_report()
        
        elif choice == '4':
            make_payments()
        
        elif choice == '5':
            print("👋 Gorusmek uzere!")
            break
