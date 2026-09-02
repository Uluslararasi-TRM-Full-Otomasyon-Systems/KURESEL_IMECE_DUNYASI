import random
import time
import math
from typing import Tuple, List

class HumanBehaviorEngine:
    """İnsan davranışlarını simüle eden stochastic motor."""
    
    @staticmethod
    def reading_time(text_length: int, words_per_minute: int = 250) -> float:
        """Bir metni 'okuma' süresini simüle eder (saniye)."""
        # Ortalama okuma hızı: ~250 kelime/dakika
        words = text_length / 5  # yaklaşık karakter/kelime oranı
        minutes = words / words_per_minute
        # %20 varyasyon ekle
        variation = random.uniform(0.8, 1.2)
        return minutes * 60 * variation

    @staticmethod
    def scroll_jitter() -> float:
        """Sayfa kaydırma hızı (rastgele jitter)."""
        # Ortalama 200-800ms arası, rastgele
        return random.uniform(0.2, 0.8)

    @staticmethod
    def between_actions(min_seconds: float = 2.0, max_seconds: float = 15.0) -> float:
        """İki aksiyon arası bekleme süresi (insan gibi)."""
        # Log-normal dağılım benzeri (uzun kuyruk)
        # 2-15 saniye arası, ancak ara sıra daha uzun
        if random.random() < 0.1:  # %10 ihtimalle uzun bekleme
            return random.uniform(15.0, 60.0)
        return random.uniform(min_seconds, max_seconds)

    @staticmethod
    def mouse_movement(start: Tuple[int, int], end: Tuple[int, int], steps: int = 20) -> List[Tuple[int, int]]:
        """Fare hareketini simüle eder (rastgele eğriler)."""
        points = []
        for i in range(steps + 1):
            t = i / steps
            # Bezier benzeri eğri (rastgele sapma)
            x = start[0] + (end[0] - start[0]) * t + random.randint(-10, 10) * math.sin(t * math.pi)
            y = start[1] + (end[1] - start[1]) * t + random.randint(-10, 10) * math.cos(t * math.pi)
            points.append((int(x), int(y)))
        return points

    @staticmethod
    def non_action_browsing(duration_range: Tuple[float, float] = (30.0, 120.0)) -> float:
        """'Aktif kullanıcı' gibi sayfada gezinti (non-action) süresi."""
        # Kullanıcı sayfayı okuyor veya sekmeler arası geçiş yapıyor
        return random.uniform(*duration_range)

    @staticmethod
    def random_pause() -> None:
        """Rastgele bir bekleme yapar (insan düşünme süresi)."""
        time.sleep(HumanBehaviorEngine.between_actions(0.5, 3.0))