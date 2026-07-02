import sqlite3
import csv
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# ============================================
# GUNLUK RAPORLAMA SISTEMI
# ============================================

TEAM_FILE = "team_list.csv"
SALES_DB = "sales.db"
REPORT_FILE = "gunluk_rapor.txt"

# ============================================
# 1. GUNLUK SATIS RAPORU OLUSTUR
# ============================================
def create_daily_report():
    """Gunluk satis raporu olusturur"""
    
    conn = sqlite3.connect(SALES_DB)
    c = conn.cursor()
    
    today = datetime.now().strftime("%d.%m.%Y")
    
    # Bugunku satislari al
    c.execute('''SELECT member_name, COUNT(*), SUM(commission_amount)
                 FROM sales WHERE sale_date LIKE ? GROUP BY member_name''',
              (f"{today}%",))
    
    sales = c.fetchall()
    
    # Bugunku toplam komisyon
    c.execute('''SELECT SUM(commission_amount)
                 FROM sales WHERE sale_date LIKE ?''',
              (f"{today}%",))
    
    total = c.fetchone()[0] or 0
    
    conn.close()
    
    # Raporu olustur
    report = []
    report.append("="*60)
    report.append(f"📊 GUNLUK SATIS RAPORU - {today}")
    report.append("="*60)
    report.append("")
    
    if not sales:
        report.append("❌ Bugun henuz satis yapilmamis.")
    else:
        for sale in sales:
            report.append(f"👤 {sale[0]}: {sale[1]} satis - {sale[2]:.2f} TL")
        report.append("")
        report.append("-"*60)
        report.append(f"💰 TOPLAM KOMISYON: {total:.2f} TL")
    
    report.append("")
    report.append(f"📱 Rapor Tarihi: {datetime.now().strftime('%d.%m.%Y %H:%M')}")
    report.append("="*60)
    
    # Dosyaya kaydet
    with open(REPORT_FILE, 'w', encoding='utf-8') as f:
        f.write("\n".join(report))
    
    return "\n".join(report)

# ============================================
# 2. EKIP DURUM RAPORU
# ============================================
def team_status_report():
    """Ekip uyelerinin durum raporu"""
    
    report = []
    report.append("\n" + "="*60)
    report.append("👥 EKIP DURUM RAPORU")
    report.append("="*60)
    
    try:
        with open(TEAM_FILE, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            rows = list(reader)
        
        if len(rows) <= 1:
            report.append("⚠️ Henuz ekip uyesi yok!")
        else:
            for row in rows[1:]:
                report.append(f"🆔 {row[0]} | {row[1]} | {row[2]} | {row[3]} | Kazanc: {row[8]} TL")
    
    except FileNotFoundError:
        report.append("❌ Ekip listesi bulunamadi!")
    
    return "\n".join(report)

# ============================================
# 3. WHATSAPP MESAJI HAZIRLA
# ============================================
def create_whatsapp_message():
    """WhatsApp icin kisa mesaj hazirlar"""
    
    conn = sqlite3.connect(SALES_DB)
    c = conn.cursor()
    
    today = datetime.now().strftime("%d.%m.%Y")
    
    c.execute('''SELECT COUNT(*), SUM(commission_amount)
                 FROM sales WHERE sale_date LIKE ?''',
              (f"{today}%",))
    
    result = c.fetchone()
    count = result[0] or 0
    total = result[1] or 0
    
    conn.close()
    
    message = f"🔔 *GUNLUK OZET - {today}*\n\n"
    message += f"📊 Bugun {count} satis\n"
    message += f"💰 Toplam komisyon: {total:.2f} TL\n\n"
    
    if count > 0:
        message += "🎉 Basarili bir gun! 👏"
    else:
        message += "😴 Henuz satis yok. Paylasimlar devam!"
    
    return message

# ============================================
# 4. TELEGRAM MESAJI HAZIRLA
# ============================================
def create_telegram_message():
    """Telegram icin mesaj hazirlar"""
    
    report = create_daily_report()
    
    # Telegram icin kisalt
    lines = report.split('\n')
    short_report = lines[:15]  # Ilk 15 satir
    
    return '\n'.join(short_report)

# ============================================
# 5. E-POSTA GONDER (OPSIYONEL)
# ============================================
def send_email_report(receiver_email):
    """E-posta ile rapor gonderir"""
    
    report = create_daily_report()
    
    # E-posta ayarlari (kendi bilgilerini gir)
    sender_email = "your-email@gmail.com"
    password = "your-password"
    
    message = MIMEMultipart("alternative")
    message["Subject"] = f"📊 Gunluk Satis Raporu - {datetime.now().strftime('%d.%m.%Y')}"
    message["From"] = sender_email
    message["To"] = receiver_email
    
    # HTML versiyonu
    html = f"""
    <html>
      <body>
        <pre style="font-family: monospace; font-size: 14px;">
{report}
        </pre>
      </body>
    </html>
    """
    
    part = MIMEText(html, "html")
    message.attach(part)
    
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message.as_string())
        server.quit()
        print("✅ E-posta gonderildi!")
    except Exception as e:
        print(f"❌ E-posta gonderilemedi: {e}")

# ============================================
# 6. RAPORLARI GOSTER
# ============================================
def show_all_reports():
    """Tum raporlari gosterir"""
    
    print(create_daily_report())
    print(team_status_report())
    print("\n" + "="*60)
    print("📱 WHATSAPP MESAJI:")
    print("="*60)
    print(create_whatsapp_message())
    print("\n" + "="*60)
    print("📱 TELEGRAM MESAJI:")
    print("="*60)
    print(create_telegram_message())

# ============================================
# 7. OTOMATIK RAPORLAMA (Scheduler icin)
# ============================================
def auto_report():
    """Otomatik raporlama icin"""
    
    report = create_daily_report()
    whatsapp = create_whatsapp_message()
    telegram = create_telegram_message()
    
    # Dosyaya kaydet
    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    filename = f"rapor_{timestamp}.txt"
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(report)
        f.write("\n\n")
        f.write(team_status_report())
    
    print(f"✅ Rapor kaydedildi: {filename}")
    
    # Burada Telegram botuna gonderme kodu eklenebilir
    # telegram_bot.send_message(chat_id, telegram)
    
    return filename

# ============================================
# 8. TEST KOMUTLARI
# ============================================
if __name__ == "__main__":
    print("📊 GUNLUK RAPORLAMA SISTEMI")
    print("="*40)
    
    while True:
        print("\n1️⃣ Gunluk satis raporu goster")
        print("2️⃣ Ekip durum raporu goster")
        print("3️⃣ WhatsApp mesaji hazirla")
        print("4️⃣ Telegram mesaji hazirla")
        print("5️⃣ Tum raporlari goster")
        print("6️⃣ Otomatik rapor kaydet")
        print("7️⃣ E-posta gonder")
        print("8️⃣ Cikis")
        
        choice = input("\nSeciminiz: ")
        
        if choice == '1':
            print(create_daily_report())
        
        elif choice == '2':
            print(team_status_report())
        
        elif choice == '3':
            print("\n" + "="*60)
            print(create_whatsapp_message())
        
        elif choice == '4':
            print("\n" + "="*60)
            print(create_telegram_message())
        
        elif choice == '5':
            show_all_reports()
        
        elif choice == '6':
            filename = auto_report()
            print(f"✅ Rapor kaydedildi: {filename}")
        
        elif choice == '7':
            email = input("E-posta adresi: ")
            send_email_report(email)
        
        elif choice == '8':
            print("👋 Gorusmek uzere!")
            break
