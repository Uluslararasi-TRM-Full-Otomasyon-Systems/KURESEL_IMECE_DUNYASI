import base64
import copy
import ctypes
import hashlib
import json
import os
import secrets
from ctypes import wintypes


DEFAULT_AGENT_POLICIES = {
    "CamouflageAgent": {
        "capabilities": ["session_masking"],
        "context_allowlist": ["worker_mode"],
    },
    "AccountManagerAgent": {
        "capabilities": ["identity_assignment"],
        "context_allowlist": ["worker_mode"],
    },
    "Content_Generator_Agent": {
        "capabilities": ["content_generation"],
        "context_allowlist": ["trend_report", "worker_mode", "active_agents", "smart_parameters", "bridge_network_reports"],
    },
    "QueueAgent": {
        "capabilities": ["queue_management"],
        "context_allowlist": ["content_payload", "worker_mode"],
    },
    "PosterAgent": {
        "capabilities": ["platform_publishing"],
        "context_allowlist": ["queue_payload", "worker_mode"],
    },
    "HealthCheckAgent": {
        "capabilities": ["system_health_audit"],
        "context_allowlist": [
            "queue_payload", "poster_payload", "active_agents", "worker_mode",
            "security_status", "market_intelligence_reports", "bridge_network_reports",
            "sentinel_alerts", "agent_capacity_snapshot"
        ],
    },
}

SENSITIVE_KEYWORDS = {
    "email",
    "password",
    "token",
    "secret",
    "commission",
    "earning",
    "profit",
    "revenue",
    "receiver",
    "sender",
    "operator_identity",
}


class DATA_BLOB(ctypes.Structure):
    _fields_ = [("cbData", wintypes.DWORD), ("pbData", ctypes.POINTER(ctypes.c_char))]


class ZeroTrustSecurityManager:
    """
    Savunma odakli sifir-guven modeli:
    - ajan bazli token
    - minimum baglam erisimi
    - hassas veri tespiti
    - Windows DPAPI ile yerel sifreleme
    """

    def __init__(self, zero_trust=True, stealth_mode=True):
        self.zero_trust = zero_trust
        self.stealth_mode = stealth_mode
        self.agent_policies = {}
        self.agent_tokens = {}
        self.protected_snapshots = {}

    def register_agent(self, agent_name, capabilities=None, context_allowlist=None):
        defaults = DEFAULT_AGENT_POLICIES.get(agent_name, {})
        policy = {
            "capabilities": list(capabilities or defaults.get("capabilities", [])),
            "context_allowlist": list(context_allowlist or defaults.get("context_allowlist", [])),
        }
        self.agent_policies[agent_name] = policy
        self.agent_tokens[agent_name] = secrets.token_urlsafe(24)
        return policy

    def authorize(self, agent_name, token):
        if not self.zero_trust:
            return True
        return bool(token) and self.agent_tokens.get(agent_name) == token

    def build_agent_context(self, agent_name, shared_context):
        if not self.zero_trust:
            return copy.deepcopy(shared_context)

        policy = self.agent_policies.get(agent_name, {})
        allowed_keys = set(policy.get("context_allowlist", []))
        return {
            key: copy.deepcopy(value)
            for key, value in shared_context.items()
            if key in allowed_keys
        }

    def fingerprint(self, value):
        text = json.dumps(value, ensure_ascii=False, sort_keys=True, default=str)
        return hashlib.sha256(text.encode("utf-8")).hexdigest()

    def contains_sensitive_data(self, payload):
        if isinstance(payload, dict):
            for key, value in payload.items():
                lowered = str(key).lower()
                if any(keyword in lowered for keyword in SENSITIVE_KEYWORDS):
                    return True
                if self.contains_sensitive_data(value):
                    return True
            return False
        if isinstance(payload, list):
            return any(self.contains_sensitive_data(item) for item in payload)
        return False

    def _encrypt_bytes_dpapi(self, raw_bytes):
        if os.name != "nt":
            raise OSError("DPAPI yalnizca Windows uzerinde desteklenir.")

        crypt32 = ctypes.windll.crypt32
        kernel32 = ctypes.windll.kernel32
        buffer = ctypes.create_string_buffer(raw_bytes, len(raw_bytes))
        in_blob = DATA_BLOB(len(raw_bytes), buffer)
        out_blob = DATA_BLOB()
        if not crypt32.CryptProtectData(
            ctypes.byref(in_blob),
            "TRM Zero Trust",
            None,
            None,
            None,
            0,
            ctypes.byref(out_blob),
        ):
            raise ctypes.WinError()

        try:
            encrypted = ctypes.string_at(out_blob.pbData, out_blob.cbData)
            return base64.b64encode(encrypted).decode("ascii")
        finally:
            kernel32.LocalFree(out_blob.pbData)

    def protect_snapshot(self, snapshot_name, payload):
        if not self.contains_sensitive_data(payload):
            return None

        try:
            serialized = json.dumps(payload, ensure_ascii=False, default=str).encode("utf-8")
            encrypted = self._encrypt_bytes_dpapi(serialized)
            self.protected_snapshots[snapshot_name] = encrypted
            return encrypted
        except Exception:
            return None

    def get_security_report(self):
        return {
            "zero_trust_enabled": self.zero_trust,
            "stealth_mode_enabled": self.stealth_mode,
            "registered_agents": list(self.agent_policies.keys()),
            "encrypted_snapshots": len(self.protected_snapshots),
            "protection_backend": "windows-dpapi" if os.name == "nt" else "unavailable",
        }
