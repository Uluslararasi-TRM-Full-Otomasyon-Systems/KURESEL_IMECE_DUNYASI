
import socket

class AgentBridge:
    def __init__(self, agent_id):
        self.agent_id = agent_id
    
    def listen_to_orchestrator(self):
        pass

# Ajan başlatıcı
bridge = AgentBridge(agent_id=40)
print(f"Agent-{str(40).zfill(3)} | Orchestrator'a bağlandı.")

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

# Ajan_040
# Uzmanlık: Pazar Araştırmacısı

def gorev_yap():
    return "Ben bir Pazar Araştırmacısı olarak görevimin başındayım."