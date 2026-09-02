import sqlite3
import csv
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# ============================================
# GÜNLÜK RAPORLAMA SİSTEMİ
# ============================================

TEAM_FILE = "team_list.csv"
SALES_DB = "sales.db"
REPORT_FILE = "gunluk_rapor.txt"

# ============================================
# 1. GÜNLÜK SATIŞ RAPORU OLUŞTUR
# ============================================
def create_daily_report():
    """Günlük satış raporu oluşturur"""
    
    conn = sqlite3.connect(SALES_DB)
    c = conn.cursor()
    
    today = datetime.now().strftime("%d.%m.%Y")
    
    # Bugünkü satışları al
    c.execute('''SELECT member_name, COUNT(*), SUM(commission_amount)
                 FROM sales WHERE sale_date LIKE ? GROUP BY member_name''',
              (f"{today}%",))
    
    sales = c.fetchall()
    
    # Bugünkü toplam komisyon
    c.execute('''SELECT SUM(commission_amount)
                 FROM sales WHERE sale_date LIKE ?''',
              (f"{today}%",))
    
    total = c.fetchone()[0] or 0
    
    conn.close()
    
    # Raporu oluştur
    report = []
    report.append("="*60)
    report.append(f"📊 GÜNLÜK SATIŞ RAPORU - {today}")
    report.append("="*60)
    report.append("")
    
    if not sales:
        report.append("❌ Bugün henüz satış yapılmamış.")
    else:
        for sale in sales:
            report.append(f"👤 {sale[0]}: {sale[1]} satış - {sale[2]:.2f} TL")
        report.append("")
        report.append("-"*60)
        report.append(f"💰 TOPLAM KOMİSYON: {total:.2f} TL")
    
    report.append("")
    report.append(f"📱 Rapor Tarihi: {datetime.now().strftime('%d.%m.%Y %H:%M')}")
    report.append("="*60)
    
    # Dosyaya kaydet
    with open(REPORT_FILE, 'w', encoding='utf-8') as f:
        f.write("\n".join(report))
    
    return "\n".join(report)

# ============================================
# 2. EKİP DURUM RAPORU
# ============================================
def team_status_report():
    """Ekip üyelerinin durum raporu"""
    
    report = []
    report.append("\n" + "="*60)
    report.append("👥 EKİP DURUM RAPORU")
    report.append("="*60)
    
    try:
        with open(TEAM_FILE, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            rows = list(reader)
        
        if len(rows) <= 1:
            report.append("⚠️ Henüz ekip üyesi yok!")
        else:
            for row in rows[1:]:
                report.append(f"🆔 {row[0]} | {row[1]} | {row[2]} | {row[3]} | Kazanç: {row[8]} TL")
    
    except FileNotFoundError:
        report.append("❌ Ekip listesi bulunamadı!")
    
    return "\n".join(report)

# ============================================
# 3. WHATSAPP MESAJI HAZIRLA
# ============================================
def create_whatsapp_message():
    """WhatsApp için kısa mesaj hazırlar"""
    
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
    
    message = f"🔔 *GÜNLÜK ÖZET - {today}*\n\n"
    message += f"📊 Bugün {count} satış\n"
    message += f"💰 Toplam komisyon: {total:.2f} TL\n\n"
    
    if count > 0:
        message += "🎉 Başarılı bir gün! 👏"
    else:
        message += "😴 Henüz satış yok. Paylaşımlar devam!"
    
    return message

# ============================================
# 4. TELEGRAM MESAJI HAZIRLA
# ============================================
def create_telegram_message():
    """Telegram için mesaj hazırlar"""
    
    report = create_daily_report()
    
    # Telegram için kısalt
    lines = report.split('\n')
    short_report = lines[:15]  # İlk 15 satır
    
    return '\n'.join(short_report)

# ============================================
# 5. E-POSTA GÖNDER (OPSİYONEL)
# ============================================
def send_email_report(receiver_email):
    """E-posta ile rapor gönderir"""
    
    report = create_daily_report()
    
    # E-posta ayarları (kendi bilgilerini gir)
    sender_email = "your-email@gmail.com"
    password = "your-password"
    
    message = MIMEMultipart("alternative")
    message["Subject"] = f"📊 Günlük Satış Raporu - {datetime.now().strftime('%d.%m.%Y')}"
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
        print("✅ E-posta gönderildi!")
    except Exception as e:
        print(f"❌ E-posta gönderilemedi: {e}")

# ============================================
# 6. RAPORLARI GÖSTER
# ============================================
def show_all_reports():
    """Tüm raporları gösterir"""
    
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
# 7. OTOMATİK RAPORLAMA (Scheduler için)
# ============================================
def auto_report():
    """Otomatik raporlama için"""
    
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
    
    # Burada Telegram botuna gönderme kodu eklenebilir
    # telegram_bot.send_message(chat_id, telegram)
    
    return filename

# ============================================
# 8. TEST KOMUTLARI
# ============================================
if __name__ == "__main__":
    print("📊 GÜNLÜK RAPORLAMA SİSTEMİ")
    print("="*40)
    
    while True:
        print("\n1️⃣ Günlük satış raporu göster")
        print("2️⃣ Ekip durum raporu göster")
        print("3️⃣ WhatsApp mesajı hazırla")
        print("4️⃣ Telegram mesajı hazırla")
        print("5️⃣ Tüm raporları göster")
        print("6️⃣ Otomatik rapor kaydet")
        print("7️⃣ E-posta gönder")
        print("8️⃣ Çıkış")
        
        choice = input("\nSeçiminiz: ")
        
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
            print("👋 Görüşmek üzere!")
            break
