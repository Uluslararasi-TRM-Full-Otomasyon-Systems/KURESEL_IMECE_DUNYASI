#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script to verify sensitive data masking filter
"""
import logging
import config

# Test logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

print("=== Sensitive Data Masking Test ===")
print()

# Test cases
test_logs = [
    "User logged in with API_KEY=sk-proj-1234567890abcdef1234567890abcdef",
    "Private key loaded: private_key='-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCx..."
    "Client email: client_email='trm-service@trm-project.iam.gserviceaccount.com'",
    "Token expired, refreshing: token='ya29.a0AeTM1i2b3c4d5e6f7g8h9i0j1k2l3m4n5o6p7q8r9s0t1u2v3w4x5y6z'",
    "Password set successfully: password='MySuperSecretPassword123!'"
]

for log_msg in test_logs:
    logger.info(log_msg)

print()
print("=== Test Complete! All sensitive data should be masked with '********' ===")