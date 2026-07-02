#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TRM Full Otomasyon - Tek Nokta Calistirici

Kullanim:
    python run.py              # Tum sistemi baslat
    python run.py status       # Konfigurasyonu kontrol et
    python run.py test         # Tum modulleri test et
    python run.py telegram     # Sadece Telegram dinleyici
    python run.py scraper      # Sadece web scraper
    python run.py ai           # Sadece AI testi
    python run.py social       # Sadece sosyal medya testi
"""

import asyncio
import sys
import os
import io

# ============================================
# UTF-8 ENCODING DUZELTMESI (Windows icin kritik!)
# Turkce karakterlerin "TÃ¼rkÃ§e" gibi bozulmasini onler
# ============================================
if sys.platform == "win32":
    # Windows konsolunu UTF-8'e zorla
    os.system("chcp 65001 > nul")
    # stdout/stderr'i UTF-8 yap
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')
os.environ['PYTHONIOENCODING'] = 'utf-8'

# Once config'i yukle (os.environ'a anahtarlari aktarir)
import config  # noqa: F401


def cmd_status():
    """Konfigurasyon durumunu goster"""
    print(config.get_status_report())


async def cmd_test():
    """Tum modulleri test et"""
    print("=" * 60)
    print("🧪 TRM Sistem Testi")
    print("=" * 60)

    results = {}

    # Config
    validation = config.config.validate_critical_configs()
    results['config'] = validation
    print(f"\n📋 Config: {validation}")

    # AI
    try:
        from ai_integration import AIContentGenerator
        ai = AIContentGenerator()
        test_product = {'title': 'Test Urun', 'price': '299 TL', 'commission_rate': 25}
        result = await ai.process_product_pipeline(test_product)
        results['ai'] = result['success']
        print(f"🤖 AI: {'✅ OK' if result['success'] else '❌ FAIL'}")
    except Exception as e:
        results['ai'] = False
        print(f"🤖 AI: ❌ {e}")

    # Web Scraper
    try:
        from web_scraper import WebScraper
        scraper = WebScraper()
        await scraper.init_session()
        results['scraper'] = True
        print("🌐 Web Scraper: ✅ Hazir")
        await scraper.close()
    except Exception as e:
        results['scraper'] = False
        print(f"🌐 Web Scraper: ❌ {e}")

    # Social Media
    try:
        from social_media_automation import SocialMediaManager
        sm = SocialMediaManager()
        test_content = {'content': 'Test', 'title': 'Test', 'link': '', 'image_url': ''}
        r = await sm.publish_to_all_platforms(test_content)
        results['social'] = r['summary']['successful_platforms'] > 0
        print(f"📱 Sosyal Medya: ✅ {r['summary']['successful_platforms']}/{r['summary']['total_platforms']} basarili")
    except Exception as e:
        results['social'] = False
        print(f"📱 Sosyal Medya: ❌ {e}")

    # Drive / Analytics
    try:
        from google_drive_integration import GoogleDriveManager, AnalyticsManager
        dm = GoogleDriveManager()
        am = AnalyticsManager(dm)
        stats = am.get_dashboard_stats()
        results['drive'] = True
        print(f"☁️  Google Drive: ✅ Dashboard stats: {stats['total_products']} urun")
    except Exception as e:
        results['drive'] = False
        print(f"☁️  Google Drive: ❌ {e}")

    print("\n" + "=" * 60)
    all_ok = all(v if not isinstance(v, dict) else any(v.values()) for v in results.values())
    print(f"🎯 Genel Sonuc: {'✅ TUM TESTLER GECTI' if all_ok else '⚠️ BAZI HATALAR VAR'}")
    print("=" * 60)


async def cmd_full():
    """Tum sistemi orkestrator ile baslat"""
    from main_orchestrator import TRMOrchestrator
    orchestrator = TRMOrchestrator()
    try:
        await orchestrator.start()
    except KeyboardInterrupt:
        print("\n👋 Kullanici tarafindan durduruldu")
    finally:
        await orchestrator.shutdown()


async def cmd_telegram():
    from telegram_listener import test_telegram_listener
    await test_telegram_listener()


async def cmd_scraper():
    from web_scraper import test_web_scraper
    await test_web_scraper()


async def cmd_ai():
    from ai_integration import test_ai_integration
    await test_ai_integration()


async def cmd_social():
    from social_media_automation import test_social_media_automation
    await test_social_media_automation()


def main():
    cmd = sys.argv[1] if len(sys.argv) > 1 else "full"

    print("=" * 60)
    print("🚀 ULUSLARARASI TRM FULL OTOMASYON SISTEMI v3.1")
    print("=" * 60)

    if cmd == "status":
        cmd_status()
        return

    cmds = {
        "full": cmd_full,
        "test": cmd_test,
        "telegram": cmd_telegram,
        "scraper": cmd_scraper,
        "ai": cmd_ai,
        "social": cmd_social,
    }

    if cmd not in cmds:
        print(f"❌ Bilinmeyen komut: {cmd}")
        print(__doc__)
        sys.exit(1)

    try:
        asyncio.run(cmds[cmd]())
    except KeyboardInterrupt:
        print("\n👋 Durduruldu")


# ── TRM v5.0 Yeni Moduller ────────────────────────────────────────────────
try:
    from MONITOR import setup_logging, monitor
    import os as _os
    setup_logging(_os.getenv('TRM_LOG_LEVEL', 'INFO'))
except Exception:
    pass
try:
    from SECURITY_MANAGER import rate_limiter, spam_guard
except Exception:
    rate_limiter = None; spam_guard = None
try:
    from QUEUE_MANAGER import product_queue, content_queue, publish_queue
except Exception:
    product_queue = content_queue = publish_queue = None
try:
    from CONTENT_SCHEDULER import scheduler
except Exception:
    scheduler = None
# ─────────────────────────────────────────────────────────────────────────


# ── TRM v5.0 Iletisim Modulleri ──────────────────────────────────────────
try:
    from DM_AUTO_REPLY import auto_reply
except Exception:
    auto_reply = None
try:
    from EMAIL_AUTOMATION import email_manager
except Exception:
    email_manager = None
# ─────────────────────────────────────────────────────────────────────────


if __name__ == "__main__":
    main()
