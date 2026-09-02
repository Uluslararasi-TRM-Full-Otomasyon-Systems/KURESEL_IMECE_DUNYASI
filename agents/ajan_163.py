
import socket

class AgentBridge:
    def __init__(self, agent_id):
        self.agent_id = agent_id
    
    def listen_to_orchestrator(self):
        pass

# Ajan başlatıcı
bridge = AgentBridge(agent_id=163)
print(f"Agent-{str(163).zfill(3)} | Orchestrator'a bağlandı.")

import logging
import os

LOG_DIR = 'E:/TRM_Sistem/logs'
LOG_FILE = os.path.join(LOG_DIR, 'trm_sistem.log')
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('TRM_Ajan_Sistemi')
logger.info("Ajan başlatıldı ve merkezi sisteme bağlandı.")

# Ajan_163
# Uzmanlık: Duygusal İmece ve Motivasyon

def gorev_yap():
    import subprocess
    from datetime import datetime
    
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Ajan-163: Duygusal imece ve motivasyon mesajı gönderiliyor...")
    
    # Duygusal imece ajanını çağır
    try:
        subprocess.run(['python', 'E:/TRM_Sistem/duygusal_imece_ajan.py'], check=True)
        return "Duygusal imece mesajı gönderildi"
    except Exception as e:
        return f"Duygusal imece hatası: {str(e)}"
