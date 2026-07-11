# trm_agents/scaling_agent.py
import os
import sys
import json
import time
import psutil
import subprocess
from datetime import datetime
from typing import Dict, List, Any

class ScalingAgent:
    """
    Ölçeklendirme Ajanı – Sistem yükünü izler ve gerektiğinde yeni ajanlar başlatır.
    """
    def __init__(self, agents_dir: str = "trm_agents",
                 alert_log: str = "intelligence_log.json",
                 cpu_threshold: float = 70.0,
                 memory_threshold: float = 80.0,
                 queue_threshold: int = 50):
        self.agents_dir = agents_dir
        self.alert_log = alert_log
        self.cpu_threshold = cpu_threshold
        self.memory_threshold = memory_threshold
        self.queue_threshold = queue_threshold
        self.scaling_history = []

    def get_system_load(self) -> Dict[str, float]:
        """CPU, RAM ve kuyruk yükünü döndürür."""
        cpu = psutil.cpu_percent(interval=1)
        mem = psutil.virtual_memory().percent
        # Queue yükü – mevcut queue_agent'ın kuyruk uzunluğunu oku
        queue_len = 0
        try:
            with open("sosyal_medya_kuyruk.json", "r", encoding="utf-8") as f:
                queue_data = json.load(f)
                if isinstance(queue_data, list):
                    queue_len = len(queue_data)
                elif isinstance(queue_data, dict):
                    queue_len = len(queue_data.get("items", []))
        except (FileNotFoundError, json.JSONDecodeError):
            pass
        return {"cpu": cpu, "memory": mem, "queue": queue_len}

    def scale_if_needed(self) -> List[Dict[str, Any]]:
        """
        Yük eşikleri aşılırsa yeni ajan instance'ları başlatır.
        """
        load = self.get_system_load()
        decisions = []

        if load["cpu"] > self.cpu_threshold:
            decisions.append(self._start_new_agent("cpu", load["cpu"]))
        if load["memory"] > self.memory_threshold:
            decisions.append(self._start_new_agent("memory", load["memory"]))
        if load["queue"] > self.queue_threshold:
            decisions.append(self._start_new_agent("queue", load["queue"]))

        if decisions:
            self._log_decisions(decisions)
        return decisions

    def _start_new_agent(self, reason: str, value: float) -> Dict[str, Any]:
        """
        Yeni bir ajan başlatır (örneğin PosterAgent veya QueueAgent).
        Burada subprocess ile yeni bir Python işlemi başlatılır.
        """
        # Basitlik için PosterAgent'ı başlatalım, istenirse genişletilebilir
        agent_script = os.path.join(self.agents_dir, "poster_agent.py")
        if not os.path.exists(agent_script):
            agent_script = os.path.join(self.agents_dir, "queue_agent.py")
        
        pid = None
        try:
            # subprocess ile yeni bir işlem başlat
            proc = subprocess.Popen([sys.executable, agent_script], 
                                    stdout=subprocess.DEVNULL, 
                                    stderr=subprocess.DEVNULL,
                                    cwd=os.path.dirname(os.path.abspath(__file__)))
            pid = proc.pid
            status = "success"
        except Exception as e:
            status = "failed"
            pid = None

        return {
            "timestamp": datetime.now().isoformat(),
            "reason": reason,
            "threshold_value": value,
            "agent_started": os.path.basename(agent_script),
            "pid": pid,
            "status": status
        }

    def _log_decisions(self, decisions: List[Dict[str, Any]]):
        """Ölçeklendirme kararlarını intelligence_log.json'a yazar."""
        try:
            with open(self.alert_log, "r", encoding="utf-8") as f:
                data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            data = {}

        if "scaling_events" not in data:
            data["scaling_events"] = []
        data["scaling_events"].extend(decisions)
        data["scaling_events"] = data["scaling_events"][-100:]

        with open(self.alert_log, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)