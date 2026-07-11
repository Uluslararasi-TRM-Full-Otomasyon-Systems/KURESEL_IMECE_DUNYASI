import os
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import json

class VaultAgent:
    """
    Hassas verileri şifrelemek için Fernet kullanır.
    Anahtar .env veya secrets.toml'dan okunur.
    """
    def __init__(self, key_env_var: str = "VAULT_KEY", salt: bytes = b'trm_salt'):
        self.key_env_var = key_env_var
        self.salt = salt
        self.key = self._get_key()
        self.cipher = Fernet(self.key)

    def _get_key(self) -> bytes:
        """Anahtarı environment'dan al, yoksa oluştur ve kaydet."""
        key = os.environ.get(self.key_env_var)
        if key:
            return key.encode()
        else:
            # Yeni anahtar oluştur
            kdf = PBKDF2HMAC(
                algorithm=hashes.SHA256(),
                length=32,
                salt=self.salt,
                iterations=100000,
            )
            # Varsayılan parola (değiştirilmeli)
            password = os.environ.get("VAULT_PASSWORD", "TRM_SuperSecret_2026")
            key_bytes = base64.urlsafe_b64encode(kdf.derive(password.encode()))
            # Anahtarı environment'a yaz (geçici)
            os.environ[self.key_env_var] = key_bytes.decode()
            return key_bytes

    def encrypt(self, data: str) -> str:
        """String veriyi şifreler."""
        return self.cipher.encrypt(data.encode()).decode()

    def decrypt(self, encrypted: str) -> str:
        """Şifreli veriyi çözer."""
        return self.cipher.decrypt(encrypted.encode()).decode()

    def encrypt_dict(self, data: dict) -> dict:
        """Sözlüğü şifreler (sadece string değerleri)"""
        result = {}
        for key, value in data.items():
            if isinstance(value, str):
                result[key] = self.encrypt(value)
            else:
                result[key] = value
        return result

    def decrypt_dict(self, data: dict) -> dict:
        """Sözlüğü çözer"""
        result = {}
        for key, value in data.items():
            if isinstance(value, str):
                try:
                    result[key] = self.decrypt(value)
                except:
                    result[key] = value  # şifreli değilse olduğu gibi bırak
            else:
                result[key] = value
        return result