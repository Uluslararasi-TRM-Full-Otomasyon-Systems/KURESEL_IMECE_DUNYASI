import os

class SwarmMemory:
    """Ajanların birbirine veri aktardığı ortak hafıza."""
    memory = {}

    @classmethod
    def set_data(cls, key, value):
        cls.memory[key] = value
        print(f"[SWARM] {key} verisi paylaşıma açıldı.")

    @classmethod
    def get_data(cls, key):
        return cls.memory.get(key)

# Ajanların birbirini tetikleme mantığı
def execute_swarm_task(task_name, data):
    print(f"[SWARM] Protokol Başlatıldı: {task_name}")
    # Burada ajanlar arası paslaşma gerçekleşir
    SwarmMemory.set_data(task_name, data)