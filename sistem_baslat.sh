#!/bin/bash
# TRM Full Otomasyon v4.0 - Linux/Mac Stable Launcher
cd "$(dirname "$0")"
export PYTHONIOENCODING=utf-8
export PYTHONUTF8=1

PY_CMD="python3"
command -v python3 >/dev/null 2>&1 || PY_CMD="python"

# İlk çalıştırmada bağımlılıkları kur
if [ ! -f ".deps_v4_installed" ]; then
    echo "============================================================"
    echo "  İLK KURULUM - Bağımlılıklar yükleniyor..."
    echo "============================================================"
    $PY_CMD -m pip install --upgrade pip --quiet
    $PY_CMD -m pip install -r requirements.txt
    if [ $? -eq 0 ]; then
        touch .deps_v4_installed
        echo "  ✅ Bağımlılıklar kuruldu."
    else
        echo "  ❌ HATA: pip install -r requirements.txt komutunu manuel çalıştırın."
        read -p "Devam etmek için ENTER..."
    fi
fi

while true; do
    clear
    echo ""
    echo "  ============================================================"
    echo "    TRM FULL OTOMASYON v4.0  -  Stable Launcher"
    echo "  ============================================================"
    echo ""
    echo "    SİSTEM"
    echo "    [1] Tüm Sistemi Başlat           (main_orchestrator)"
    echo "    [2] Daemon Başlat (arka plan)     (DAEMON_MANAGER start)"
    echo "    [3] Daemon Durdur                 (DAEMON_MANAGER stop)"
    echo "    [4] Daemon Durumu / Health        (DAEMON_MANAGER status)"
    echo ""
    echo "    MODÜLLER"
    echo "    [5] Sadece Telegram Dinleyici     (run.py telegram)"
    echo "    [6] Sadece Web Scraper            (run.py scraper)"
    echo "    [7] Sadece AI Testi               (run.py ai)"
    echo "    [8] Sadece Sosyal Medya Testi     (run.py social)"
    echo ""
    echo "    SATIŞ ve RAPOR"
    echo "    [9] Satış Dönüş Zinciri Raporu    (SATIS_DONUS_ZINCIRI.py)"
    echo "    [a] Komisyon Takip Raporu         (trm_tracking.py)"
    echo "    [b] API / Platform Durumu         (run.py status)"
    echo ""
    echo "    YAPILANDIRMA"
    echo "    [c] secrets.env Düzenle           (nano)"
    echo "    [d] API Anahtarları Rehberi       (cat)"
    echo ""
    echo "    TEST ve BAKIM"
    echo "    [f] Birim Testleri                (pytest test_trm.py -v)"
    echo "    [g] Parser Testi                  (telegram_parser.py)"
    echo "    [h] Sistem Tam Test               (run.py test)"
    echo ""
    echo "    [x] Çıkış"
    echo "  ============================================================"
    read -p "  Seçiminiz: " secim

    case "$secim" in
        1) $PY_CMD run.py ;;
        2) $PY_CMD DAEMON_MANAGER.py start ;;
        3) $PY_CMD DAEMON_MANAGER.py stop ;;
        4) $PY_CMD DAEMON_MANAGER.py status && $PY_CMD DAEMON_MANAGER.py health ;;
        5) $PY_CMD run.py telegram ;;
        6) $PY_CMD run.py scraper ;;
        7) $PY_CMD run.py ai ;;
        8) $PY_CMD run.py social ;;
        9) $PY_CMD SATIS_DONUS_ZINCIRI.py ;;
        a) $PY_CMD trm_tracking.py ;;
        b) $PY_CMD run.py status ;;
        c) nano secrets.env ;;
        d) cat API_ANAHTARLARI_REHBERI.md | more ;;
        f) $PY_CMD -m pytest test_trm.py -v --tb=short ;;
        g) $PY_CMD telegram_parser.py ;;
        h) $PY_CMD run.py test ;;
        x|X|0) exit 0 ;;
        *) echo "  Geçersiz seçim!"; sleep 1 ;;
    esac
    read -p "  Devam etmek için ENTER..."
done
