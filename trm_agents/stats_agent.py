# trm_agents/stats_agent.py
from datetime import datetime

class StatsAgent:
    def __init__(self):
        self.pool_balance = 0.0 # Toplanan aylık havuz
        self.active_users = 200 # Pilot grup

    def get_live_data(self):
        """
        Dashboard için canlı verileri döndürür.
        """
        return {
            "toplanan_imece": self.pool_balance,
            "aktif_kullanici": self.active_users,
            "sabit_pay": self.calculate_individual_share()
        }

    def calculate_individual_share(self):
        """
        24:01'de hesaplanacak adil dağılım rakamı.
        """
        if self.active_users == 0: return 0
        return round(self.pool_balance / self.active_users, 2)

    def is_distribution_time(self):
        """
        Ayın son günü saat 00:01 kontrolü.
        """
        now = datetime.now()
        # Her ayın son günü ve saat 00:01 kontrolü
        return now.day == 30 and now.hour == 0 and now.minute == 1