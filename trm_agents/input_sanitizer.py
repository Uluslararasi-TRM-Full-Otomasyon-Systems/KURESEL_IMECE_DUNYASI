import re
import html
from typing import Any, Dict, List, Union

class InputSanitizer:
    """
    SQL Injection ve XSS saldırılarına karşı veri temizleme.
    Whitelist prensibiyle çalışır.
    """
    # İzin verilen karakter desenleri (alfanumerik, boşluk, bazı noktalama)
    ALLOWED_PATTERN = re.compile(r'^[a-zA-Z0-9ğüşıöçĞÜŞİÖÇ\s\.\,\-\_\:\/]+$')

    @staticmethod
    def sanitize_string(value: str) -> str:
        """String temizleme"""
        if not isinstance(value, str):
            return str(value)
        # HTML escape (XSS)
        cleaned = html.escape(value)
        # Sadece izin verilen karakterleri tut
        cleaned = ''.join(c for c in cleaned if InputSanitizer.ALLOWED_PATTERN.match(c))
        return cleaned.strip()

    @staticmethod
    def sanitize_dict(data: Dict[str, Any]) -> Dict[str, Any]:
        """Sözlük içindeki tüm string değerleri temizler"""
        result = {}
        for key, value in data.items():
            if isinstance(value, str):
                result[key] = InputSanitizer.sanitize_string(value)
            elif isinstance(value, dict):
                result[key] = InputSanitizer.sanitize_dict(value)
            elif isinstance(value, list):
                result[key] = InputSanitizer.sanitize_list(value)
            else:
                result[key] = value
        return result

    @staticmethod
    def sanitize_list(data: List[Any]) -> List[Any]:
        """Liste içindeki tüm string değerleri temizler"""
        result = []
        for item in data:
            if isinstance(item, str):
                result.append(InputSanitizer.sanitize_string(item))
            elif isinstance(item, dict):
                result.append(InputSanitizer.sanitize_dict(item))
            elif isinstance(item, list):
                result.append(InputSanitizer.sanitize_list(item))
            else:
                result.append(item)
        return result

    @staticmethod
    def sanitize_url(url: str) -> str:
        """URL temizleme (tehlikeli protokolleri engelle)"""
        if not url:
            return ""
        # Sadece http/https/ftp izin ver
        if not re.match(r'^https?://', url, re.IGNORECASE):
            return ""
        # Tehlikeli karakterleri temizle
        return InputSanitizer.sanitize_string(url)