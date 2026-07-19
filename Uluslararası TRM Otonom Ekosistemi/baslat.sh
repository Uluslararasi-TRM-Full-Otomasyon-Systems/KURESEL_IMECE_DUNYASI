#!/bin/bash
# TRM Full Otomasyon v5.0 - Linux/Mac Launcher
cd "$(dirname "$0")"
export PYTHONIOENCODING=utf-8
export PYTHONUTF8=1
PY=python3
command -v python3 >/dev/null 2>&1 || PY=python

if [ ! -f ".deps_v5" ]; then
    echo "Bagimliliklar yukleniyor..."
    $PY -m pip install -r requirements.txt --quiet && touch .deps_v5
fi

while true; do
    clear
    echo ""
    echo "  ===================================================="
    echo "    TRM FULL OTOMASYON v5.0  |  trendurunlermarket.com"
    echo "  ===================================================="
    echo ""
    echo "  [1] Sistemi Baslat             (run.py)"
    echo "  [2] Watchdog ile 7/24 Baslat   (WATCHDOG.py)"
    echo "  [3] Daemon Baslat              (DAEMON_MANAGER start)"
    echo "  [4] Daemon Durdur              (DAEMON_MANAGER stop)"
    echo "  [5] Daemon Durumu              (DAEMON_MANAGER status)"
    echo ""
    echo "  [6] Sadece Telegram Dinle      (run.py telegram)"
    echo "  [7] Sadece Web Scraper         (run.py scraper)"
    echo "  [8] Sosyal Medya Testi         (run.py social)"
    echo "  [9] AI Icerik Testi            (ai_integration.py)"
    echo ""
    echo "  [s] Satis Dashboard            (SALES_DASHBOARD.py)"
    echo "  [p] Yayin Plani                (CONTENT_SCHEDULER.py)"
    echo "  [g] Guvenlik Denetimi          (SECURITY_MANAGER.py)"
    echo "  [q] Kuyruk Durumu              (QUEUE_MANAGER.py)"
    echo ""
    echo "  [d] DM Otomatik Yanit           (DM_AUTO_REPLY.py)
  [m] E-posta Kampanyasi         (EMAIL_AUTOMATION.py)
  [z] Platform Kurulum Rehberi   (PLATFORM_SETUP_WIZARD.py)
  [e] secrets.env Duzenle        (nano)"
    echo "  [t] Testleri Calistir          (pytest)"
    echo "  [x] Cikis"
    echo "  ===================================================="
    read -p "  Seciminiz: " s

    case "$s" in
        1) $PY run.py ;;
        2) $PY WATCHDOG.py ;;
        3) $PY DAEMON_MANAGER.py start ;;
        4) $PY DAEMON_MANAGER.py stop ;;
        5) $PY DAEMON_MANAGER.py status ;;
        6) $PY run.py telegram ;;
        7) $PY run.py scraper ;;
        8) $PY run.py social ;;
        9) $PY ai_integration.py ;;
        s) $PY SALES_DASHBOARD.py ;;
        p) $PY CONTENT_SCHEDULER.py ;;
        g) $PY SECURITY_MANAGER.py ;;
        q) $PY QUEUE_MANAGER.py ;;
        d) $PY DM_AUTO_REPLY.py ;;
        m) $PY EMAIL_AUTOMATION.py ;;
        z) $PY PLATFORM_SETUP_WIZARD.py ;;
        e) nano secrets.env ;;
        t) $PY -m pytest test_trm.py -v --tb=short ;;
        x) exit 0 ;;
        *) echo "Gecersiz secim" ;;
    esac
    read -p "  Devam icin ENTER..."
done
