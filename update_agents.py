import os

# İletişim Bloğu (Süslü parantez çakışmaması için yer tutucu kullanıldı)
bridge_code = """
import socket

class AgentBridge:
    def __init__(self, agent_id):
        self.agent_id = agent_id
    
    def listen_to_orchestrator(self):
        pass

# Ajan başlatıcı
bridge = AgentBridge(agent_id=ID_PLACEHOLDER)
print(f"Agent-{str(ID_PLACEHOLDER).zfill(3)} | Orchestrator'a bağlandı.")

"""

agents_dir = "agents"

for i in range(1, 201):
    file_name = f"ajan_{str(i).zfill(3)}.py"
    file_path = os.path.join(agents_dir, file_name)
    
    if os.path.exists(file_path):
        with open(file_path, "r+", encoding="utf-8") as f:
            content = f.read()
            if "AgentBridge" not in content:
                final_bridge = bridge_code.replace("ID_PLACEHOLDER", str(i))
                f.seek(0, 0)
                f.write(final_bridge + content)
                print(f"✅ {file_name} başarıyla entegre edildi.")
            else:
                print(f"ℹ️ {file_name} zaten entegre edilmiş.")

print("🚀 Tüm ajanlar Orchestrator'a bağlanmaya hazır!")