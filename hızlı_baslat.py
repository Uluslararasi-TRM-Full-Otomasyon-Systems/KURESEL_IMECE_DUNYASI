import subprocess
import sys
import traceback

def system_start():
    print("SISTEM TETIKLENIYOR: Master Controller baslatiliyor...")
    try:
        # Hata mesajlarini gormek icin subprocess ciktisini yonetelim
        process = subprocess.Popen(
            ["python", "MASTER_CONTROLLER.py"],
            stdout=sys.stdout, 
            stderr=sys.stderr
        )
        process.wait()
    except Exception as e:
        print("\n--- KRITIK HATA ---")
        traceback.print_exc()
    
    input("\nIslem bitti. Kapatmak icin ENTER'a basin...")

if __name__ == "__main__":
    system_start()