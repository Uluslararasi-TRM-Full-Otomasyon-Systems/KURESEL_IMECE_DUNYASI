import random

class BrowserSpooferAgent:
    def __init__(self):
        # Gercek cihazlardan toplanmis, algoritmayi yaniltacak tarayici parmak izi havuzu
        self.fingerprints = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.3 Safari/605.1.15",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:123.0) Gecko/20100101 Firefox/123.0",
            "Mozilla/5.0 (iPhone; CPU iPhone OS 17_3_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.3.1 Mobile/15E148 Safari/604.1",
            "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36"
        ]

    def kimlik_degistir(self):
        """Her yeni islemde sosyal medya aglarina tamamen farkli bir cihazmis gibi gorunmemizi saglar."""
        secilen_kimlik = random.choice(self.fingerprints)
        print(f"[BUKALEMUN] Dijital kimlik ve tarayici parmak izi basariyla maskelendi.")
        return {"User-Agent": secilen_kimlik}