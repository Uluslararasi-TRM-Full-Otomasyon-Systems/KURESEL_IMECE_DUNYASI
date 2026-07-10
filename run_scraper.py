import os
import sys
import streamlit as st
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
import atexit
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Sörf alanı: Sistemin ana klasörünü otomatik tanı (otomatik path fix)
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from trm_agents.CoreNexus import CoreNexus
from trm_agents.camouflage_agent import CamouflageAgent
from trm_agents.account_manager_agent import AccountManagerAgent
from trm_agents.analyst_agent import AnalystAgent

def send_notification_email(product_count, output_path, trend_summary=""):
    """
    Otonom üretim tamamlandığında e-posta bildirimi gönderir.
    st.secrets üzerinden e-posta konfigürasyonunu çeker.
    """
    try:
        # Streamlit secrets'tan e-posta bilgilerini al
        email_sender = st.secrets.get("EMAIL_SENDER", "")
        email_password = st.secrets.get("EMAIL_PASSWORD", "")
        email_receiver = st.secrets.get("EMAIL_RECEIVER", "")
        smtp_server = st.secrets.get("SMTP_SERVER", "smtp.gmail.com")
        smtp_port = st.secrets.get("SMTP_PORT", 587)
        
        # Eğer gerekli bilgiler yoksa uyarı ver ve çık
        if not all([email_sender, email_password, email_receiver]):
            print("[NotificationAgent] E-posta konfigürasyonu eksik, bildirim gönderilemedi.")
            return False
        
        # E-posta içeriğini hazırla
        subject = "Otonom Üretim Başarıyla Tamamlandı"
        body = f"""
TRM Otonom Üretim Sistemi - Üretim Raporu

========================================
Üretim Zamanı: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Toplam Ürün Sayısı: {product_count}
Çıktı Dosyası: {output_path}
========================================

📊 {trend_summary}

Sistem otonom modda çalışmaya devam ediyor.
Her 6 saatte bir otomatik güncelleme yapılacak.

TRM-Operations Otonom Scraper
"""
        
        # MIME mesajı oluştur
        message = MIMEMultipart()
        message["From"] = email_sender
        message["To"] = email_receiver
        message["Subject"] = subject
        message.attach(MIMEText(body, "plain"))
        
        # SMTP bağlantısı ve e-posta gönderme
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(email_sender, email_password)
            server.sendmail(email_sender, email_receiver, message.as_string())
        
        print(f"[NotificationAgent] E-posta başarıyla gönderildi: {email_receiver}")
        return True
        
    except Exception as e:
        print(f"[NotificationAgent] E-posta gönderme hatası: {str(e)}")
        return False

def run_scraper_logic(show_ui=True):
    # 1. CoreNexus'u başlat ve tüm ajanları bağla
    nexus = CoreNexus()
    camou = CamouflageAgent()
    account_mgr = AccountManagerAgent()
    
    # Ajanları sisteme bağla
    nexus.connect_agent("CamouflageAgent", camou)
    nexus.connect_agent("AccountManagerAgent", account_mgr)
    
    # 2. Operatör kimliği ataması
    operator_identity = account_mgr.assign_operator_identity("TR")
    if show_ui:
        st.write(f"Operatör Kimliği: {operator_identity['identity']}")
        st.write(f"E-posta: {operator_identity['email']}")
    
    # 3. Maskeyi tak (CoreNexus üzerinden maskelenmiş operasyon)
    mask_id = camou.mask_identity()
    if show_ui:
        st.write(f"Maskeli Operasyon Aktif: {mask_id}")
    
    # 4. Veri işleme havuzu (CoreNexus senkronizasyonu ile)
    nexus.run_system_sync()
    
    sample_products = [
        {"title": "Organik Zeytin Yagi 1L", "product_url": "https://www.trendyol.com/gida-saglik-ve-ozel-bakim/organik-urunler/organik-zeytin-yagi"},
        {"title": "Kozmetik Cilt Bakim Seti", "product_url": "https://www.trendyol.com/kozmetik/cilt-bakim/cilt-bakim-seti"},
        {"title": "Nemlendirici Krem", "product_url": "https://www.trendyol.com/kozmetik/cilt-bakim/nemlendirici-krem"},
        {"title": "Şampuan 500ml", "product_url": "https://www.trendyol.com/kozmetik/sac-bakim/sampuan"},
        {"title": "Bal 1kg", "product_url": "https://www.trendyol.com/gida-saglik-ve-ozel-bakim/tatli-urunler/bal"}
    ]
    
    output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ACIL_SATIS_HAVUZU.txt")
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("=========================================\n")
        f.write("TRM ACIL NAKIT OTOMASYONU - ACIL SATIS HAVUZU\n")
        f.write("=========================================\n")
        f.write(f"Baslama Zamani: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Maske ID: {mask_id}\n")
        f.write(f"Operatör: {operator_identity['identity']}\n")
        f.write(f"E-posta: {operator_identity['email']}\n")
        f.write(f"Domain: {operator_identity['domain_authority']}\n")
        f.write(f"Toplam Urun: {len(sample_products)}\n")
        f.write("=========================================\n\n")
        
        affiliate_id = "trendurunlermarket"
        
        for p in sample_products:
            affiliate_link = p['product_url']
            if "?" in affiliate_link:
                affiliate_link += f"&affiliate={affiliate_id}"
            else:
                affiliate_link += f"?affiliate={affiliate_id}"
            f.write(f"{p['title']} - {affiliate_link}\n")
            
    if show_ui:
        st.success(f"Havuz güncellendi! Dosya: {output_path}")
    else:
        print(f"[Otonom Mod] Havuz güncellendi: {output_path}")
    
    # Trend analizi (sadece otonom modda)
    trend_summary = ""
    if not show_ui:
        try:
            analyst = AnalystAgent()
            analysis_result = analyst.analyze_pool(output_path)
            
            if analysis_result:
                # Trend raporunu kaydet
                trend_report_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "trend_raporlari.json")
                analyst.save_trend_report(analysis_result, trend_report_path)
                
                # Trend özetini al
                trend_summary = analyst.get_trend_summary(analysis_result)
                print(f"[AnalystAgent] {trend_summary}")
        except Exception as e:
            print(f"[AnalystAgent] Trend analizi hatası: {str(e)}")
            trend_summary = "Trend analizi yapılamadı."
    
    # E-posta bildirimi gönder (sadece otonom modda)
    if not show_ui:
        try:
            send_notification_email(len(sample_products), output_path, trend_summary)
        except Exception as e:
            print(f"[Otonom Mod] E-posta gönderme hatası (sistem çökmedi): {str(e)}")

# --- BackgroundScheduler Setup ---
scheduler = BackgroundScheduler()
scheduler.add_job(run_scraper_logic, 'interval', hours=6, args=[False])
scheduler.start()

# Shutdown scheduler when app exits
atexit.register(lambda: scheduler.shutdown())

# --- Streamlit Arayüzü (Tek tuşla sörf) ---
st.title("TRM-Operations Otonom Scraper")

# Otonom Mod Status Bar
st.info("🟢 Sistem: Otonom Modda (Her 6 saatte bir otomatik güncelleme)")

if st.button("Sistemi Başlat ve Havuzu Çek"):
    run_scraper_logic()