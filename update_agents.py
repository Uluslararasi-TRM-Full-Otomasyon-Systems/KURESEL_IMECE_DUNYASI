import os
import glob

# Enjekte edilecek kamuflaj kodu
stealth_code = """
import random
import time

def random_delay(min_sec=5, max_sec=60):
    time.sleep(random.uniform(min_sec, max_sec))

def get_user_agent():
    return random.choice([
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) Chrome/120.0.0.0"
    ])
"""

def inject_stealth_to_agents():
    agent_files = glob.glob("trm_agents/*.py")
    for file in agent_files:
        with open(file, 'r+', encoding='utf-8') as f:
            content = f.read()
            # Eğer zaten eklenmemişse ekle
            if "random_delay" not in content:
                f.seek(0, 0)
                f.write(stealth_code + "\n" + content)
                print(f"[KAMUFLAJ] {file} ajanına görünmezlik eklendi.")

if __name__ == "__main__":
    inject_stealth_to_agents()
    print("[BAŞARI] Tüm ajanlar 'İnsan Davranışı Simülasyonu' ile güncellendi.")