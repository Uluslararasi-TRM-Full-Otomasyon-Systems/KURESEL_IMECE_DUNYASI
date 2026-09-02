#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ULUSLARARASI TRM FULL OTOMASYON v3.0
Trend Ürünler Market - WhatsApp Bildirim Sistemi
Flash Bellek Mobil Bildirimler - Sistem Olayları ve Alışveriş Bildirimleri
"""

import json
import time
import random
import threading
import requests
from datetime import datetime, timedelta
from pathlib import Path

from trm_paths import flash_sync_root

class WhatsAppNotificationSystem:
    def __init__(self):
        self.running = True
        self.phone_number = "+90 542 623 5116"
        self.api_key = "demo_whatsapp_api_key"
        self.notification_queue = []
        self.sent_notifications = []
        self.system_events = []
        self.sales_events = []
        self.flash_drive_path = flash_sync_root()
        self.notification_settings = {
            "system_alerts": True,
            "sales_notifications": True,
            "daily_summary": True,
            "error_reports": True,
            "performance_warnings": True,
            "flash_drive_status": True
        }
        self.start_notification_system()

    def send_whatsapp_message(self, message, priority="normal"):
        """WhatsApp mesajı gönder (simülasyon)"""
        try:
            # Gerçek WhatsApp API entegrasyonu için burası kullanılacak
            # Şimdilik simülasyon olarak logluyoruz
            
            notification = {
                "id": len(self.sent_notifications) + 1,
                "phone": self.phone_number,
                "message": message,
                "timestamp": datetime.now().isoformat(),
                "priority": priority,
                "status": "SENT",
                "type": "WHATSAPP"
            }
            
            self.sent_notifications.append(notification)
            
            # Log kaydı
            print(f"📱 WhatsApp Bildirimi Gönderildi:")
            print(f"   📞 Telefon: {self.phone_number}")
            print(f"   💬 Mesaj: {message}")
            print(f"   ⏰ Zaman: {datetime.now().strftime('%H:%M:%S')}")
            print(f"   🎯 Öncelik: {priority}")
            print("-" * 50)
            
            return True
            
        except Exception as e:
            print(f"❌ WhatsApp gönderim hatası: {e}")
            return False

    def check_flash_drive_status(self):
        """Flash bellek durumunu kontrol et"""
        try:
            flash_path = Path(self.flash_drive_path)
            if flash_path.exists():
                return {
                    "status": "CONNECTED",
                    "path": str(flash_path),
                    "free_space": "Yeterli",
                    "last_check": datetime.now().isoformat()
                }
            else:
                return {
                    "status": "DISCONNECTED",
                    "error": "Flash bellek bulunamadı",
                    "last_check": datetime.now().isoformat()
                }
        except Exception as e:
            return {
                "status": "ERROR",
                "error": str(e),
                "last_check": datetime.now().isoformat()
            }

    def generate_system_notification(self, event_type, details):
        """Sistem olay bildirimi oluştur"""
        messages = {
            "system_start": f"🚀 TRM OTOMASYON BAŞLADI\n\nSistem tam otomasyon modunda çalışıyor.\n⏰ Başlangıç: {datetime.now().strftime('%H:%M:%S')}\n🌐 Tüm paneller aktif",
            
            "system_error": f"⚠️ SİSTEM HATASI\n\n{details}\n⏰ {datetime.now().strftime('%H:%M:%S')}\n🔧 Lütfen kontrol edin",
            
            "performance_warning": f"⚡ PERFORMANS UYARISI\n\n{details}\n⏰ {datetime.now().strftime('%H:%M:%S')}\n📊 Sistem yükü yüksek",
            
            "flash_drive_disconnected": f"🔌 FLASH BELLEK AYRILDI\n\nFlash bellek sistemden ayrıldı!\n⏰ {datetime.now().strftime('%H:%M:%S')}\n📁 Lütfen bağlayın",
            
            "flash_drive_connected": f"🔌 FLASH BELLEK BAĞLANDI\n\nFlash bellek sisteme bağlandı!\n⏰ {datetime.now().strftime('%H:%M:%S')}\n📁 Otomasyon devam ediyor",
            
            "ai_module_restart": f"🤖 AI MODÜL YENİDEN BAŞLATILDI\n\n{details}\n⏰ {datetime.now().strftime('%H:%M:%S')}\n✅ Sistem stabilize edildi",
            
            "social_media_error": f"📱 SOSYAL MEDYA HATASI\n\n{details}\n⏰ {datetime.now().strftime('%H:%M:%S')}\n🔄 Otomatik yeniden deneme"
        }
        
        return messages.get(event_type, f"📢 SİSTEM BİLDİRİMİ\n\n{details}\n⏰ {datetime.now().strftime('%H:%M:%S')}")

    def generate_sales_notification(self, event_type, details):
        """Satış bildirimi oluştur"""
        if event_type == "new_sale":
            sale = details
            return f"💰 YENİ SATIŞ!\n\n🛍️ Ürün: {sale['product_name']}\n💸 Tutar: ₺{sale['amount']:,}\n💎 Komisyon: ₺{sale['commission']:,}\n📦 Kategori: {sale['category']}\n⏰ {sale['time']}\n🎯 Hedefe yaklaştınız!"
        
        elif event_type == "high_comission_sale":
            sale = details
            return f"🎉 YÜKSEK KOMİSYONLU SATIŞ!\n\n🛍️ Ürün: {sale['product_name']}\n💸 Tutar: ₺{sale['amount']:,}\n💎 Komisyon: ₺{sale['commission']:,} (%{sale['commission_rate']}%)\n📦 Kategori: {sale['category']}\n⏰ {sale['time']}\n🚀 Harika!"
        
        elif event_type == "daily_target_reached":
            return f"🎯 GÜNLÜK HEDEF TAMAMLANDI!\n\n💰 Günlük Hedef: ₺{details['target']:,}\n✅ Elde Edilen: ₺{details['achieved']:,}\n📈 Başarı Oranı: %{details['percentage']}\n⏰ {datetime.now().strftime('%H:%M:%S')}\n🏆 Tebrikler!"
        
        elif event_type == "weekly_summary":
            summary = details
            return f"📊 HAFTALIK ÖZET\n\n💰 Toplam Satış: ₺{summary['total_sales']:,}\n🛍️ Ürün Sayısı: {summary['product_count']}\n💎 Toplam Komisyon: ₺{summary['total_commission']:,}\n📈 Ortalama Komisyon: %{summary['avg_commission']}\n🎯 Hedef Başarısı: %{summary['target_success']}\n⏰ {datetime.now().strftime('%H:%M:%S')}"
        
        return f"💰 SATIŞ BİLDİRİMİ\n\n{details}\n⏰ {datetime.now().strftime('%H:%M:%S')}"

    def notification_monitor(self):
        """Bildirim izleyici - Ana döngü"""
        last_flash_check = time.time()
        daily_summary_sent = False
        
        while self.running:
            try:
                current_time = time.time()
                
                # Flash bellek durum kontrolü (her 30 saniyede bir)
                if current_time - last_flash_check >= 30:
                    flash_status = self.check_flash_drive_status()
                    
                    if flash_status["status"] == "DISCONNECTED":
                        self.send_whatsapp_message(
                            self.generate_system_notification("flash_drive_disconnected", flash_status["error"]),
                            "high"
                        )
                    elif flash_status["status"] == "CONNECTED":
                        # Sadece bağlandığında bildirim gönder
                        if not hasattr(self, 'flash_connected'):
                            self.send_whatsapp_message(
                                self.generate_system_notification("flash_drive_connected", "Sistem stabil"),
                                "normal"
                            )
                            self.flash_connected = True
                    
                    last_flash_check = current_time
                
                # Rastgele sistem olayları oluştur (simülasyon)
                if random.random() < 0.05:  # %5 ihtimalle
                    event_types = ["system_error", "performance_warning", "ai_module_restart", "social_media_error"]
                    event_type = random.choice(event_types)
                    details = f"Otomatik tespit edilen {event_type}"
                    
                    if self.notification_settings["system_alerts"]:
                        message = self.generate_system_notification(event_type, details)
                        self.send_whatsapp_message(message, "medium")
                
                # Rastgele satış olayları oluştur (simülasyon)
                if random.random() < 0.08:  # %8 ihtimalle
                    sale = {
                        "product_name": f"Trend Ürün {random.randint(1, 999)}",
                        "amount": random.randint(500, 5000),
                        "commission": random.randint(100, 1500),
                        "commission_rate": round(random.uniform(20, 40), 1),
                        "category": random.choice(["Elektronik", "Giyim", "Ev", "Spor", "Teknoloji"]),
                        "time": datetime.now().strftime('%H:%M')
                    }
                    
                    if self.notification_settings["sales_notifications"]:
                        if sale["commission_rate"] > 30:
                            event_type = "high_comission_sale"
                            priority = "high"
                        else:
                            event_type = "new_sale"
                            priority = "normal"
                        
                        message = self.generate_sales_notification(event_type, sale)
                        self.send_whatsapp_message(message, priority)
                
                # Günlük özet (her gün saat 18:00'da)
                if datetime.now().hour == 18 and datetime.now().minute == 0 and not daily_summary_sent:
                    if self.notification_settings["daily_summary"]:
                        summary = {
                            "total_sales": random.randint(50000, 150000),
                            "product_count": random.randint(50, 200),
                            "total_commission": random.randint(15000, 45000),
                            "avg_commission": round(random.uniform(25, 35), 1),
                            "target_success": random.randint(85, 120)
                        }
                        
                        message = self.generate_sales_notification("weekly_summary", summary)
                        self.send_whatsapp_message(message, "low")
                        daily_summary_sent = True
                
                # Gün değiştiğinde daily_summary'ı sıfırla
                if datetime.now().hour == 0 and datetime.now().minute == 0:
                    daily_summary_sent = False
                
                time.sleep(10)  # 10 saniye bekle
                
            except Exception as e:
                print(f"❌ Bildirim izleyici hatası: {e}")
                time.sleep(30)

    def send_manual_notification(self, message, priority="normal"):
        """Manuel bildirim gönder"""
        return self.send_whatsapp_message(message, priority)

    def get_notification_history(self):
        """Bildirim geçmişini al"""
        return {
            "total_sent": len(self.sent_notifications),
            "recent_notifications": self.sent_notifications[-10:],
            "system_events": len([n for n in self.sent_notifications if "SİSTEM" in n["message"]]),
            "sales_notifications": len([n for n in self.sent_notifications if "SATIŞ" in n["message"]]),
            "flash_drive_events": len([n for n in self.sent_notifications if "FLASH" in n["message"]])
        }

    def start_notification_system(self):
        """Bildirim sistemini başlat"""
        notification_thread = threading.Thread(target=self.notification_monitor, daemon=True)
        notification_thread.start()
        
        # Başlangıç bildirimi gönder
        if self.notification_settings["system_alerts"]:
            startup_message = self.generate_system_notification("system_start", "Tüm modüller aktif")
            self.send_whatsapp_message(startup_message, "high")

def main():
    print("# -*- coding: utf-8 -*-")
    print("📱 ULUSLARASI TRM FULL OTOMASYON v3.0")
    print("🔔 WhatsApp Bildirim Sistemi")
    print("🌐 Flash Bellek Mobil Bildirimler")
    print("=" * 60)
    
    # WhatsApp bildirim sistemini başlat
    whatsapp_system = WhatsAppNotificationSystem()
    
    print(f"\n✅ WhatsApp Bildirim Sistemi Başlatıldı!")
    print(f"📞 Bildirim Telefonu: {whatsapp_system.phone_number}")
    print(f"📁 Flash Bellek Yolu: {whatsapp_system.flash_drive_path}")
    print(f"⚙️ Bildirim Ayarları:")
    print(f"   • Sistem Uyarıları: {'✅' if whatsapp_system.notification_settings['system_alerts'] else '❌'}")
    print(f"   • Satış Bildirimleri: {'✅' if whatsapp_system.notification_settings['sales_notifications'] else '❌'}")
    print(f"   • Günlük Özet: {'✅' if whatsapp_system.notification_settings['daily_summary'] else '❌'}")
    print(f"   • Hata Raporları: {'✅' if whatsapp_system.notification_settings['error_reports'] else '❌'}")
    print(f"   • Performans Uyarıları: {'✅' if whatsapp_system.notification_settings['performance_warnings'] else '❌'}")
    print(f"   • Flash Bellek Durumu: {'✅' if whatsapp_system.notification_settings['flash_drive_status'] else '❌'}")
    
    print("\n🔔 AKTİF BİLDİRİM TİPLERİ:")
    print("   🚀 Sistem başlatma/durdurma")
    print("   💰 Yeni satışlar")
    print("   🎉 Yüksek komisyonlu satışlar")
    print("   🎯 Hedef tamamlanmaları")
    print("   ⚠️ Sistem hataları")
    print("   ⚡ Performans uyarıları")
    print("   🔌 Flash bellek bağlantı durumları")
    print("   📊 Günlük/haftalık özetler")
    
    print("\n📱 WhatsApp bildirimleri aktif!")
    print("👋 Durdurmak için Ctrl+C")
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n👋 WhatsApp bildirim sistemi durduruluyor...")
        whatsapp_system.running = False
        print("✅ Bildirim sistemi durduruldu")

if __name__ == "__main__":
    main()
