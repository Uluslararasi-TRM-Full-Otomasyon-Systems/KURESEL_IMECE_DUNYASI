# -*- coding: utf-8 -*-
"""
TRM Nirvana v3.0 - Central Configuration Module
Centralized settings for all 161 agents in the ecosystem.
"""
import os
import logging
import re

# Sensitive data patterns to mask
SENSITIVE_PATTERNS = [
    r'(?i)private[_-]?key["\']?\s*[=:]\s*["\']?([^\s"\'}{,]+)',
    r'(?i)client[_-]?email["\']?\s*[=:]\s*["\']?([^\s"\'}{,]+)',
    r'(?i)token["\']?\s*[=:]\s*["\']?([^\s"\'}{,]+)',
    r'(?i)password["\']?\s*[=:]\s*["\']?([^\s"\'}{,]+)',
    r'(?i)secret["\']?\s*[=:]\s*["\']?([^\s"\'}{,]+)',
    r'(?i)api[_-]?key["\']?\s*[=:]\s*["\']?([^\s"\'}{,]+)',
]

class SensitiveDataFilter(logging.Filter):
    """Custom filter to mask sensitive data in log messages"""
    def filter(self, record):
        # Mask sensitive data in log message
        record.msg = self.mask_sensitive_data(record.msg)
        return True

    def mask_sensitive_data(self, text):
        masked_text = text
        for pattern in SENSITIVE_PATTERNS:
            masked_text = re.sub(pattern, lambda m: m.group(0).replace(m.group(1), '********'), masked_text)
        return masked_text

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

# Configure root logger with sensitive data filter
def configure_global_logger():
    """Apply sensitive data masking to all loggers in the system"""
    root_logger = logging.getLogger()
    # Remove existing handlers to prevent duplicates
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)
    
    # Create console handler
    console_handler = logging.StreamHandler()
    console_handler.addFilter(SensitiveDataFilter())
    formatter = logging.Formatter(LOGGING_CONFIG["FORMAT"])
    console_handler.setFormatter(formatter)
    
    # Create file handler
    file_handler = logging.FileHandler(LOGGING_CONFIG["MAIN_LOG_FILE"], encoding='utf-8')
    file_handler.addFilter(SensitiveDataFilter())
    file_handler.setFormatter(formatter)
    
    # Add handlers to root logger
    root_logger.addHandler(console_handler)
    root_logger.addHandler(file_handler)
    root_logger.setLevel(getattr(logging, LOGGING_CONFIG["LEVEL"]))

configure_global_logger()

def get_path(folder_name):
    """Dynamic path resolver helper for agents"""
    path = os.path.join(BASE_DIR, folder_name)
    os.makedirs(path, exist_ok=True)
    return path

print("[CONFIG] Central configuration loaded successfully for 164 agents.")