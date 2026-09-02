import csv
import sqlite3
from datetime import datetime, timedelta

# ============================================
# KOMİSYON HESAPLAMA SİSTEMİ
# ============================================

TEAM_FILE = "team_list.csv"
SALES_DB = "sales.db"

# ============================================
# 1. VERİTABANI OLUŞTUR
# ============================================
def init_database():
    """Satış veritabanını oluşturur"""
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
    print("✅ Veritabanı hazır!")

# ============================================
# 2. YENİ SATIŞ EKLE
# ============================================
def add_sale(member_id, product_name, product_price):
    """Yeni satış ekler ve komisyonu hesaplar"""
    
    # Ekip üyesini bul ve komisyon oranını al
    commission_rate = 0
    member_name = ""
    
    with open(TEAM_FILE, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        next(reader)  # Başlığı atla
        for row in reader:
            if row[0] == str(member_id):
                commission_rate = float(row[6])
                member_name = row[1]
                break
    
    if commission_rate == 0:
        print(f"❌ Üye ID {member_id} bulunamadı!")
        return False
    
    # Komisyon hesapla
    commission_amount = product_price * commission_rate / 100
    
    # Veritabanına ekle
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
    
    print(f"✅ Satış eklendi: {product_name} - {product_price} TL")
    print(f"💰 Komisyon: {commission_amount} TL (%{commission_rate})")
    return True

# ============================================
# 3. GÜNLÜK KOMİSYON RAPORU
# ============================================
def daily_report():
    """Günlük komisyon raporu hazırlar"""
    
    conn = sqlite3.connect(SALES_DB)
    c = conn.cursor()
    
    today = datetime.now().strftime("%d.%m.%Y")
    
    c.execute('''SELECT member_name, COUNT(*), SUM(commission_amount)
                 FROM sales WHERE sale_date LIKE ? GROUP BY member_name''',
              (f"{today}%",))
    
    rows = c.fetchall()
    
    print("\n" + "="*60)
    print(f"📊 GÜNLÜK KOMİSYON RAPORU - {today}")
    print("="*60)
    
    if not rows:
        print("Bugün henüz satış yok!")
    else:
        total = 0
        for row in rows:
            print(f"👤 {row[0]}: {row[1]} satış - {row[2]:.2f} TL")
            total += row[2]
        print("-"*60)
        print(f"💰 TOPLAM: {total:.2f} TL")
    
    conn.close()

# ============================================
# 4. AYLIK KOMİSYON RAPORU
# ============================================
def monthly_report(month=None):
    """Aylık komisyon raporu hazırlar"""
    
    if month is None:
        month = datetime.now().strftime("%m.%Y")
    
    conn = sqlite3.connect(SALES_DB)
    c = conn.cursor()
    
    c.execute('''SELECT member_name, COUNT(*), SUM(commission_amount)
                 FROM sales WHERE sale_date LIKE ? GROUP BY member_name''',
              (f"%{month}%",))
    
    rows = c.fetchall()
    
    print("\n" + "="*60)
    print(f"📅 AYLIK KOMİSYON RAPORU - {month}")
    print("="*60)
    
    if not rows:
        print("Bu ay henüz satış yok!")
    else:
        total = 0
        for row in rows:
            print(f"👤 {row[0]}: {row[1]} satış - {row[2]:.2f} TL")
            total += row[2]
        print("-"*60)
        print(f"💰 TOPLAM: {total:.2f} TL")
    
    conn.close()
    return total

# ============================================
# 5. ÖDEME YAP
# ============================================
def make_payments():
    """Aylık ödemeleri hazırlar"""
    
    conn = sqlite3.connect(SALES_DB)
    c = conn.cursor()
    
    month = datetime.now().strftime("%m.%Y")
    
    # Ekip üyelerini ve IBAN'larını al
    members = {}
    with open(TEAM_FILE, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            members[row[0]] = {
                'name': row[1],
                'iban': row[5]
            }
    
    # Bu ayki komisyonları topla
    c.execute('''SELECT member_id, member_name, SUM(commission_amount)
                 FROM sales WHERE sale_date LIKE ? AND status = "Beklemede"
                 GROUP BY member_id''', (f"%{month}%",))
    
    payments = c.fetchall()
    
    if not payments:
        print("❌ Ödenecek komisyon yok!")
        return
    
    print("\n" + "="*70)
    print(f"💰 AYLIK ÖDEME LİSTESİ - {month}")
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
    
    print(f"💰 TOPLAM ÖDEME: {total:.2f} TL")
    
    # Onay
    confirm = input("\nÖdemeleri kaydet ve durumu güncelle? (e/h): ")
    if confirm.lower() == 'e':
        for payment in payments:
            c.execute('''UPDATE sales SET status = "Ödendi" 
                         WHERE member_id = ? AND sale_date LIKE ? AND status = "Beklemede"''',
                      (payment[0], f"%{month}%"))
            
            c.execute('''INSERT INTO payments (member_id, member_name, amount, iban, payment_date, month)
                         VALUES (?, ?, ?, ?, ?, ?)''',
                      (payment[0], payment[1], payment[2], 
                       members.get(str(payment[0]), {}).get('iban', ''),
                       datetime.now().strftime("%d.%m.%Y"), month))
        
        conn.commit()
        print("✅ Ödemeler kaydedildi!")
    
    conn.close()

# ============================================
# 6. TEST KOMUTLARI
# ============================================
if __name__ == "__main__":
    print("💰 KOMİSYON HESAPLAMA SİSTEMİ")
    print("="*40)
    
    # Veritabanını hazırla
    init_database()
    
    while True:
        print("\n1️⃣ Yeni satış ekle")
        print("2️⃣ Günlük rapor")
        print("3️⃣ Aylık rapor")
        print("4️⃣ Ödeme yap")
        print("5️⃣ Çıkış")
        
        choice = input("\nSeçiminiz: ")
        
        if choice == '1':
            member_id = input("Üye ID: ")
            product = input("Ürün adı: ")
            price = float(input("Satış fiyatı (TL): "))
            add_sale(member_id, product, price)
        
        elif choice == '2':
            daily_report()
        
        elif choice == '3':
            month = input("Ay (Örnek: 02.2026) - Boş bırakırsan bu ay: ")
            if month:
                monthly_report(month)
            else:
                monthly_report()
        
        elif choice == '4':
            make_payments()
        
        elif choice == '5':
            print("👋 Görüşmek üzere!")
            break
