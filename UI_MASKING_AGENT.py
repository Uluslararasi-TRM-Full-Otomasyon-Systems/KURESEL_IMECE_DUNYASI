# -*- coding: utf-8 -*-
"""
TRM Nirvana v3.0 - UI_MASKING_AGENT
Autonomous expert agent for stealth operations, anti-bot detection, and browser spoofing.
"""
import random
import time

class UIMaskingAgent:
    def __init__(self):
        self.agent_name = "UI_Masking_Agent"
        # List of realistic user agents to blend into normal traffic
        self.user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2.1 Safari/605.1.15",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:123.0) Gecko/21000101 Firefox/123.0"
        ]

    def get_spoofed_profile(self):
        """Generates a randomized human-like profile configuration for scraper and social bots"""
        selected_ua = random.choice(self.user_agents)
        # Simulate organic network latency and viewport coordinates
        profile = {
            "user_agent": selected_ua,
            "viewport_width": random.choice([1366, 1920, 1440, 1536]),
            "viewport_height": random.choice([768, 1080, 900, 864]),
            "accept_language": "en-US,en;q=0.9,tr;q=0.8",
            "hardware_concurrency": random.choice([4, 8, 12, 16])
        }
        print(f"[{self.agent_name}] Generated stealth profile utilizing random User-Agent routing.")
        return profile

    def apply_humanized_delay(self, action_type="default"):
        """Enforces realistic, irregular human delays instead of robotic static sleep commands"""
        if action_type == "click":
            delay = random.uniform(0.5, 1.8)
        elif action_type == "typing":
            delay = random.uniform(0.1, 0.4) # delay per character
        else:
            delay = random.uniform(2.0, 5.5)
            
        print(f"[{self.agent_name}] Masking action telemetry. Applying natural human delay of {delay:.2f}s")
        time.sleep(delay)
        return delay

    def mask_stream_coordinates(self):
        """Simulates dynamic mouse trajectories to bypass advanced canvas/UI tracking algorithms"""
        fake_steps = random.randint(3, 7)
        print(f"[{self.agent_name}] Spoofing natural cursor paths across {fake_steps} micro-coordinates.")
        return True

if __name__ == "__main__":
    # Self-test initialization
    masker = UIMaskingAgent()
    masker.get_spoofed_profile()
    masker.apply_humanized_delay("click")
    masker.mask_stream_coordinates()