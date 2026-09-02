import time
import subprocess
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def run_system():
    tasks = ["web_scraper.py", "poster_agent.py"]
    for task in tasks:
        try:
            logging.info(f"🚀 Başlatılıyor: {task}")
            # check=True sayesinde hata olursa Exception fırlatır
            subprocess.run(["python", task], check=True)
            time.sleep(5)
        except subprocess.CalledProcessError:
            logging.error(f"❌ {task} hata ile karşılaştı. 161. Ajan (DNP) hata yönetimine aktarılıyor.")
            continue # Bir sonraki ajana geç

if __name__ == "__main__":
    while True:
        run_system()
        logging.info("⏳ 24 saatlik döngü bekleniyor...")
        time.sleep(86400)