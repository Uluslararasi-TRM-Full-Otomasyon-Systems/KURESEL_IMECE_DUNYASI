# trm_agents/guardian_crew.py
import time
import json
from crewai import Agent, Task, Crew
from typing import Dict, Any

# Mevcut sınıfları içe aktar
from trm_agents.dnp_guardian import DNPGuardian
from trm_agents.elci_validator import ElciValidator
from trm_agents.engagement_optimizer import EngagementOptimizer


class GuardianCrew:
    """
    CrewAI tabanlı Guardian ajanları (161-163) için orchestrator.
    Sıralı iş akışı: DNP-Guardian → Elçi-Validator → Engagement-Optimizer
    """
    def __init__(self):
        # 1. Mevcut sınıfların instance'larını oluştur
        self.dnp = DNPGuardian(trust_threshold=70, quarantine_duration=60)
        self.validator = ElciValidator()
        self.optimizer = EngagementOptimizer()

        # 2. CrewAI Agent'ları tanımla
        self.agent_dnp = Agent(
            role="Network Traffic & Trust Monitor",
            goal="Ağa giren IP/Cihaz verilerini anlık analiz et, spam/bot davranışlarını karantinaya al.",
            backstory="Türkiye dijital ihracat ağının dijital bekçisidir. Tüm giriş çıkış trafiğini trust score ile denetler.",
            allow_delegation=False,
            verbose=True
        )

        self.agent_validator = Agent(
            role="Ambassador Integration Specialist",
            goal="'ELÇİ_KODU' ile gelen yeni kullanıcıları doğrula ve P-Test'i Fast-Track protokolüyle tamamla.",
            backstory="Saha elçilerinin getirdiği verinin meşruiyetini onaylayan birimdir.",
            allow_delegation=False,
            verbose=True
        )

        self.agent_optimizer = Agent(
            role="Human Behavior Simulator",
            goal="Yeni açılan hesapların 30-60 dakika organik kullanıcı gibi görünmesini sağla.",
            backstory="Platform algoritmalarının, hesapları 'kaliteli içerik üreticisi' olarak etiketlemesini sağlar.",
            allow_delegation=False,
            verbose=True
        )

        # 3. Task'ları tanımla (sıralı çalışacak)
        self.task_dnp = Task(
            description="Tüm ajanların aktivite loglarını kontrol et. Şüpheli hareketleri karantinaya al. Çıktı olarak karantinaya alınan ajan listesini döndür.",
            agent=self.agent_dnp,
            expected_output="Karantinaya alınan ajanların listesi (JSON formatında).",
            # Bu task, dnp.run_guardian_cycle metodunu çağıracak
            # Ancak crewAI'de doğrudan fonksiyon çağrısı yok, tools ile yapılabilir.
            # Biz manuel olarak işleyeceğiz.
        )

        self.task_validator = Task(
            description="DNP-Guardian'dan gelen karantina listesindeki ajanları kontrol et. Eğer ajan 'ELÇİ_KODU' ile gelmişse, Fast-Track P-Test'i tamamla.",
            agent=self.agent_validator,
            expected_output="Fast-Track tamamlanan ajanların listesi.",
        )

        self.task_optimizer = Task(
            description="Elçi-Validator tarafından onaylanan ajanlar için 30-60 dakikalık insan davranış simülasyonu başlat.",
            agent=self.agent_optimizer,
            expected_output="Simülasyon başlatılan ajanların listesi ve durumları.",
        )

        # 4. Crew'u oluştur (sıralı iş akışı)
        self.crew = Crew(
            agents=[self.agent_dnp, self.agent_validator, self.agent_optimizer],
            tasks=[self.task_dnp, self.task_validator, self.task_optimizer],
            process="sequential",  # Sıralı çalıştır
            verbose=2
        )

    def run_guardian_cycle(self, agents_status: Dict[str, Dict]) -> Dict[str, Any]:
        """
        Guardian döngüsünü başlatır. 
        agents_status: tüm ajanların aktivite logları (isim -> log dict).
        """
        # 1. DNP-Guardian'ı çalıştır (karantina listesini al)
        self.dnp.run_guardian_cycle(agents_status)
        quarantined = list(self.dnp.quarantine_list.keys())

        # 2. Elçi-Validator: karantinadaki ajanları kontrol et (varsa ELÇİ_KODU ile)
        fast_tracked = []
        for agent_name in quarantined:
            # Örnek: elci kodu kontrolü (gerçekte dışarıdan alınmalı)
            # Burada simülasyon: eğer ajan adı "Elçi-" ile başlıyorsa doğrula
            if agent_name.startswith("Elçi-"):
                code = "ELCI123456"  # örnek kod
                if self.validator.validate_with_code(agent_name, code):
                    self.validator.complete_ptest_fast(agent_name)
                    fast_tracked.append(agent_name)

        # 3. Engagement-Optimizer: fast-track geçen ajanlar için simülasyon başlat
        for agent_name in fast_tracked:
            duration = 45  # 45 dakika
            self.optimizer.start_simulation(agent_name, duration)

        # 4. Sonuçları raporla
        result = {
            "quarantined": quarantined,
            "fast_tracked": fast_tracked,
            "simulation_started": fast_tracked  # hepsi için başlatıldı varsayalım
        }
        # Logları intelligence_log.json'a yaz
        self._log_guardian_activity(result)
        return result

    def _log_guardian_activity(self, data: Dict):
        """Guardian aktivitelerini intelligence_log.json'a ekler."""
        try:
            with open("intelligence_log.json", "r", encoding="utf-8") as f:
                log = json.load(f)
        except:
            log = {}
        if "guardian_crew_events" not in log:
            log["guardian_crew_events"] = []
        log["guardian_crew_events"].append({
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "data": data
        })
        with open("intelligence_log.json", "w", encoding="utf-8") as f:
            json.dump(log, f, ensure_ascii=False, indent=2)