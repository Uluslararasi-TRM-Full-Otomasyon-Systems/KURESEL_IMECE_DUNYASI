import subprocess
import time

SERVICES = {
    "orchestrator": {"cmd": ["python", "MASTER_CONTROLLER.py"]}
}

def monitor():
    while True:
        for name, info in SERVICES.items():
            print(f"GÖZCÜ: {name} kontrol ediliyor...")
            subprocess.Popen(info["cmd"])
        time.sleep(3600)

if __name__ == "__main__":
    monitor()