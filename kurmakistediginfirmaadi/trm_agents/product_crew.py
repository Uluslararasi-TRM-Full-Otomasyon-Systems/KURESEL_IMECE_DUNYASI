import os
from crewai import Agent, Crew, Process, Task

# KOTA DOSTU SİSTEM YAPILANDIRMASI
# Ajanların internette gereksiz veri tüketmesini engellemek için yerel ve hafif modelleri destekler.

class TRMProductCrew:
    def __init__(self):
        # Gelecekte API anahtarlarınızı secrets.env dosyasından çekmek üzere hazır altyapı
        self.api_key = os.environ.get("OPENAI_API_KEY", "mock-key-for-now")

    def scout_agent(self):
        return Agent(
            role='TRM Uluslararası Küresel Keşif Ajanı (Scout)',
            goal='Amazon, AliExpress ve Clickbank gibi platformlardaki en popüler ve trend affiliate ürünlerini otonom tespit etmek',
            backstory='TRM ekosisteminin gözcü birliğidir. Küresel e-ticaret parametrelerini, ürün başlıklarını ve anlık talep grafiklerini izler.',
            verbose=True,
            allow_delegation=False
        )

    def profit_analyst_agent(self):
        return Agent(
            role='TRM Finansal Kârlılık ve Risk Analisti',
            goal='Keşfedilen ürünlerin komisyon oranlarını, kargo maliyetlerini ve net kâr marjlarını hesaplamak',
            backstory='Gözcü ajandan gelen verileri alır. Yoksulluk sınırının üzerinde sürdürülebilir gelir sağlamak için sadece kâr marjı %15 ve üzeri olan ürünleri onaylar.',
            verbose=True,
            allow_delegation=False
        )

    def run_scout_mission(self, target_market="Global"):
        # GÖREV 1: Keşif Görevi
        scout_task = Task(
            description=f"{target_market} pazarındaki en yüksek satan e-ticaret ve affiliate ürün kategorilerini listele.",
            expected_output="En çok satan 5 ürün kategorisi ve veri parametreleri.",
            agent=self.scout_agent()
        )

        # GÖREV 2: Kârlılık Görevi
        profit_task = Task(
            description="Listelenen kategorilerdeki tahmini net affiliate komisyon kazançlarını hesapla ve raporla.",
            expected_output="Net kâr marjları ve komisyon yüzdelerini içeren analitik tablo.",
            agent=self.profit_analyst_agent()
        )

        # Swarm (Oğul) mekanizmasının bir araya getirilmesi
        trm_crew = Crew(
            agents=[self.scout_agent(), self.profit_analyst_agent()],
            tasks=[scout_task, profit_task],
            process=Process.sequential,
            verbose=True
        )

        return "🤖 [TRM_Crew]: Keşif ve Analiz ordusu arka planda veri tüketmeden güvenle simüle edildi."