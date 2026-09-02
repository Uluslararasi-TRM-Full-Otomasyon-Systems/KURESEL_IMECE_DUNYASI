import shutil
import subprocess
import sys
import threading
import time
from datetime import datetime
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
CACHE_DIR_NAMES = {
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".cache",
    "cache",
    "temp",
    "tmp",
}
CACHE_FILE_PATTERNS = ("*.pyc", "*.pyo", "*.tmp", "*.temp", "*.cache")


def clear_tenant_cache(tenant_root):
    """Tenant klasöründeki güvenli cache/temp kalıntılarını temizle."""
    tenant_path = Path(tenant_root).resolve()
    removed_items = []

    for path in tenant_path.rglob("*"):
        if not path.exists():
            continue
        if path.is_dir() and path.name.lower() in CACHE_DIR_NAMES:
            shutil.rmtree(path, ignore_errors=True)
            removed_items.append(str(path))
        elif path.is_file():
            lower_name = path.name.lower()
            if any(lower_name.endswith(pattern.replace("*", "")) for pattern in CACHE_FILE_PATTERNS):
                try:
                    path.unlink()
                    removed_items.append(str(path))
                except Exception:
                    continue

    return {
        "action": "cache_temizlendi",
        "tenant_root": str(tenant_path),
        "removed_count": len(removed_items),
        "removed_items": removed_items[:20],
    }


def restart_tenant_service(tenant_root):
    """Tenant için uygun başlangıç scriptini ya da worker/guardian sürecini tetikle."""
    tenant_path = Path(tenant_root).resolve()
    start_candidates = [
        ("START_GUARDIAN.bat", "bat"),
        ("TRM_START.bat", "bat"),
        ("START.bat", "bat"),
        ("BASLAT.bat", "bat"),
        ("trm_worker.py", "python"),
        ("guardian_agent.py", "python"),
        ("run.py", "python"),
    ]

    for file_name, start_type in start_candidates:
        candidate = tenant_path / file_name
        if not candidate.exists():
            continue

        if start_type == "bat":
            process = subprocess.Popen(
                f'cmd /c "{candidate.name}"',
                cwd=str(tenant_path),
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                stdin=subprocess.DEVNULL,
                shell=True,
            )
        elif candidate.name == "trm_worker.py":
            process = subprocess.Popen(
                [sys.executable, candidate.name, "once"],
                cwd=str(tenant_path),
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                stdin=subprocess.DEVNULL,
            )
        elif candidate.name == "guardian_agent.py":
            process = subprocess.Popen(
                [sys.executable, candidate.name, "--once", "--dry-run"],
                cwd=str(tenant_path),
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                stdin=subprocess.DEVNULL,
            )
        else:
            process = subprocess.Popen(
                [sys.executable, candidate.name],
                cwd=str(tenant_path),
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                stdin=subprocess.DEVNULL,
            )

        return {
            "action": "servis_yeniden_baslatildi",
            "tenant_root": str(tenant_path),
            "start_target": str(candidate),
            "pid": process.pid,
        }

    return {
        "action": "servis_yeniden_baslatilamadi",
        "tenant_root": str(tenant_path),
        "start_target": "",
        "pid": None,
    }


def guardian_loop():
    from trm_agents.guardian_agent import GuardianAgent
    from trm_agents.self_healing import SelfHealingManager
    from trm_agents.scaling_agent import ScalingAgent

    guardian = GuardianAgent()
    healer = SelfHealingManager()
    scaler = ScalingAgent()
    
    print("[SİSTEM] 🛡️ Gözcü Ajanlar devrede, izleme başladı...")
    print("[SİSTEM] 🔄 Her 60 saniyede bir loglar taranacak.\n")
    
    while True:
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        # 1. Guardian tarama
        print(f"[{timestamp}] 📡 Guardian tarıyor...")
        alerts = guardian.run_once()
        
        # 2. Hataları onar
        if alerts:
            print(f"[{timestamp}] 🚨 {len(alerts)} hata bulundu! Onarılıyor...")
            healer.process_guardian_alerts(alerts)
        else:
            print(f"[{timestamp}] ✅ Hata tespit edilmedi.")
        
        # 3. Yük kontrolü
        scaling_decisions = scaler.scale_if_needed()
        if scaling_decisions:
            print(f"[{timestamp}] ⚖️ {len(scaling_decisions)} ölçeklendirme kararı alındı.")
        
        # 4. Kalp atışı
        print(f"[{timestamp}] 💓 Tarama tamamlandı, 60 saniye uyku...\n")
        time.sleep(60)

if __name__ == "__main__":
    # Daemon'u ayrı bir thread'de başlat
    t = threading.Thread(target=guardian_loop, daemon=True)
    t.start()
    
    # Ana thread'i canlı tut
    print("[SİSTEM] 🟢 Daemon arka planda çalışıyor. Çıkmak için Ctrl+C basın.\n")
    while True:
        time.sleep(10)
