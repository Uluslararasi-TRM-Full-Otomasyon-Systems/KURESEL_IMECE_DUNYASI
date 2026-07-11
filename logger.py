import logging
import os

# logs klasörünü oluştur
if not os.path.exists("logs"):
    os.makedirs("logs")

def get_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    
    # Dosyaya yazma ayarı
    handler = logging.FileHandler("logs/system_monitor.log")
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    
    if not logger.handlers:
        logger.addHandler(handler)
        
    return logger