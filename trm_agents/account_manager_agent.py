import random

class AccountManagerAgent:
    def __init__(self):
        # Artık domain tapusu bizde!
        self.domain = "trm-operations.net"
        self.prefixes = ["Trend", "Global", "Smart", "Eco", "Pro", "Prime", "Market", "Data"]
        self.suffixes = ["Pulse", "Watch", "Select", "Hub", "Guide", "Choice", "Core", "View"]

    def generate_alias(self, country_code):
        """Profesyonel kurumsal rumuz üretir."""
        alias = f"{random.choice(self.prefixes)}{random.choice(self.suffixes)}_{country_code}"
        return alias

    def generate_email(self, alias):
        """Domain ile kurumsal e-posta adresi oluşturur."""
        return f"{alias.lower()}@{self.domain}"

    def assign_operator_identity(self, country_code):
        """Sisteme giren kişiye otomatik kimlik atama."""
        alias = self.generate_alias(country_code)
        email = self.generate_email(alias)
        
        return {
            "identity": alias,
            "email": email,
            "status": "active",
            "domain_authority": self.domain
        }

# Kullanım Örneği:
# agent = AccountManagerAgent()
# print(agent.assign_operator_identity("TR"))
# Çıktı: {'identity': 'SmartPulse_TR', 'email': 'smartpulse_tr@trm-operations.net', ...}