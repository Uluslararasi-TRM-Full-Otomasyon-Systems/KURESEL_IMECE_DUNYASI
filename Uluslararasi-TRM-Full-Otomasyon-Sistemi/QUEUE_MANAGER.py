import os
import json
import fcntl # Windows'ta çalışması için gerekirse bu kütüphaneyi dikkate alacağız
from filelock import FileLock # Güvenli dosya erişimi için

class QueueManager:
    def __init__(self, queue_file="system_queue.json"):
        self.queue_file = queue_file
        self.lock = FileLock(f"{queue_file}.lock")
        if not os.path.exists(self.queue_file):
            with open(self.queue_file, 'w') as f:
                json.dump([], f)
        print("QUEUE MANAGER: Haberleşme hattı aktif.")

    def push_data(self, sender, receiver, payload):
        """Ajanlar arası veri aktarımı."""
        with self.lock:
            with open(self.queue_file, 'r+') as f:
                data = json.load(f)
                data.append({"sender": sender, "receiver": receiver, "payload": payload})
                f.seek(0)
                json.dump(data, f)
                f.truncate()
        print(f"QUEUE: {sender}'den {receiver}'e veri gönderildi.")

    def pop_data(self, agent_name):
        """İlgili ajan kendi verisini çeker."""
        with self.lock:
            with open(self.queue_file, 'r+') as f:
                data = json.load(f)
                agent_tasks = [item for item in data if item['receiver'] == agent_name]
                remaining = [item for item in data if item['receiver'] != agent_name]
                f.seek(0)
                json.dump(remaining, f)
                f.truncate()
                return agent_tasks