# -*- coding: utf-8 -*-
"""
TRM Nirvana v3.0 - Central Configuration Module
Centralized settings for all 161 agents in the ecosystem.
"""
import os

# SYSTEM MODES
# True: Run with real APIs, False: Run in Mock/Simulation mode for safety
LIVE_MODE = False 

# BASE PATHS
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_DIR = os.path.join(BASE_DIR, "logs")
REPORT_DIR = os.path.join(BASE_DIR, "reports")

# Ensure necessary directories exist
os.makedirs(LOG_DIR, exist_ok=True)
os.makedirs(REPORT_DIR, exist_ok=True)

# API CONFIGURATIONS (FALLBACKS TO ENV VARIABLES OR PLACEHOLDERS)
API_CONFIG = {
    "OPENAI_API_KEY": os.getenv("OPENAI_API_KEY", "trm_mock_openai_key_24_7"),
    "AMAZON_AFFILIATE_ID": os.getenv("AMAZON_AFFILIATE_ID", "trendurunler-20"),
    "CLICKBANK_DEVELOPER_KEY": os.getenv("CLICKBANK_KEY", "cb_trm_global_dev_key"),
}

# SOCIAL MEDIA LIMITS & TIMEOUTS
AUTOMATION_LIMITS = {
    "YOUTUBE_DAILY_MAX": 5,
    "TIKTOK_DAILY_MAX": 5,
    "INSTAGRAM_DAILY_MAX": 3,
    "REQUEST_TIMEOUT": 30, # seconds
}

# LOGGING SETTINGS
LOGGING_CONFIG = {
    "LEVEL": "INFO",
    "FORMAT": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    "MAIN_LOG_FILE": os.path.join(LOG_DIR, "system_manager.log")
}

def get_path(folder_name):
    """Dynamic path resolver helper for agents"""
    path = os.path.join(BASE_DIR, folder_name)
    os.makedirs(path, exist_ok=True)
    return path

print("[CONFIG] Central configuration loaded successfully for 161 agents.")