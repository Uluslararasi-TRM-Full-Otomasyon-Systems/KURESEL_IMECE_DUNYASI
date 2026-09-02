# trm_agents/guardian_agent.py
import os
import re
import json
import time
import glob
from datetime import datetime
from typing import Dict, List, Any

# Güvenlik modülleri
from trm_agents.security_logger import SecurityLogger
from trm_agents.traffic_policeman import TrafficPoliceman

class GuardianAgent:
    """
    Gözcü Ajan – Log dosyalarını izler, hataları ve güvenlik tehditlerini tespit eder.
    TrafficPoliceman ile entegre çalışarak 429 ve ban risklerine karşı karantina başlatır.
    """
    def __init__(self, log_dir: str = "logs", alert_log: str = "intelligence_log.json"):
        self.log_dir = log_dir
        self.alert_log = alert_log
        self.patterns = {
            # Mevcut hata desenleri
            "timeout": re.compile(r"(timeout|timed out|connection timed out)", re.IGNORECASE),
            "file_not_found": re.compile(r"(file not found|no such file|filenotfounderror)", re.IGNORECASE),
            "api_error": re.compile(r"(api error|http error|status code [45]\d\d)", re.IGNORECASE),
            "memory_error": re.compile(r"(memoryerror|out of memory)", re.IGNORECASE),
            "cpu_throttle": re.compile(r"(cpu throttled|high cpu)", re.IGNORECASE),
            "ssl_cert_error": re.compile(r"(ssl certificate|ssl: certificate|self-signed certificate)", re.IGNORECASE),
            "db_connection_refused": re.compile(r"(database connection refused|could not connect to database|db error)", re.IGNORECASE),
            "unauthorized_api": re.compile(r"(unauthorized|401|forbidden|access denied)", re.IGNORECASE),
            
            # YENİ GÜVENLİK DESENLERİ
            "traffic_spike": re.compile(r"(traffic spike|high request rate|ddos|rate limit)", re.IGNORECASE),
            "unauthorized_access": re.compile(r"(unauthorized access|invalid token|login failed|brute force)", re.IGNORECASE),
            "port_scan": re.compile(r"(port scan|nmap|masscan|port knocking|scanning)", re.IGNORECASE),
            "sql_injection": re.compile(r"(union select|drop table|' or '1'='1|--|;|select.*from)", re.IGNORECASE),
            "xss_attempt": re.compile(r"(<script|alert\(|onerror=|javascript:|onload=)", re.IGNORECASE),
            
            # TRAFFIC POLICEMAN DESENLERİ
            "rate_limit_429": re.compile(r"(429|too many requests|rate limit exceeded)", re.IGNORECASE),
            "ban_risk": re.compile(r"(blocked|suspended|banned|account disabled|permanently banned)", re.IGNORECASE),
        }
        self.last_scan = 0
        self.scan_interval = 60  # saniye
        self.policeman = TrafficPoliceman()
        self.logger = SecurityLogger()

    def scan_logs(self) -> List[Dict[str, Any]]:
        """
        Log dosyalarını tarar ve desenlerle eşleşen hata/güvenlik olaylarını döndürür.
        """
        alerts = []
        log_files = glob.glob(os.path.join(self.log_dir, "*.log"))
        for log_file in log_files:
            agent_name = os.path.basename(log_file).replace(".log", "")
            try:
                with open(log_file, "r", encoding="utf-8") as f:
                    lines = f.readlines()
                for line in lines:
                    for error_type, pattern in self.patterns.items():
                        if pattern.search(line):
                            # Severity belirleme: kritik güvenlik desenleri ve traffic/ban desenleri
                            critical_types = [
                                "ssl_cert_error", "db_connection_refused",
                                "unauthorized_access", "port_scan",
                                "sql_injection", "xss_attempt", "traffic_spike",
                                "rate_limit_429", "ban_risk"
                            ]
                            severity = "critical" if error_type in critical_types else "warning"
                            alerts.append({
                                "timestamp": datetime.now().isoformat(),
                                "agent": agent_name,
                                "error_type": error_type,
                                "log_line": line.strip(),
                                "severity": severity
                            })
                            break  # Bir desen eşleştiyse diğerlerine bakma
            except Exception as e:
                alerts.append({
                    "timestamp": datetime.now().isoformat(),
                    "agent": "GuardianAgent",
                    "error_type": "log_access",
                    "log_line": f"Log dosyası okunamadı: {log_file} - {str(e)}",
                    "severity": "critical"
                })
        return alerts

    def report_alerts(self, alerts: List[Dict[str, Any]]):
        """
        Tespit edilen alert'leri işler:
        - intelligence_log.json'a yazar.
        - Güvenlik tehditlerini security_threats.json'a yazar.
        - Rate-limit ve ban risklerinde TrafficPoliceman'ı çağırır.
        """
        if not alerts:
            return

        # 1. Ana intelligence_log.json'a yaz
        try:
            with open(self.alert_log, "r", encoding="utf-8") as f:
                data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            data = {}
        if "guardian_alerts" not in data:
            data["guardian_alerts"] = []
        data["guardian_alerts"].extend(alerts)
        data["guardian_alerts"] = data["guardian_alerts"][-500:]
        with open(self.alert_log, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        # 2. Güvenlik tehditlerini security_threats.json'a yaz ve TrafficPoliceman'ı tetikle
        for alert in alerts:
            error_type = alert.get("error_type")
            # Güvenlik tehditlerini logla
            if error_type in ["unauthorized_access", "sql_injection", "xss_attempt", 
                              "port_scan", "traffic_spike"]:
                self.logger.log_threat(
                    threat_type=error_type,
                    details={
                        "agent": alert.get("agent"),
                        "log_line": alert.get("log_line"),
                        "source": "GuardianAgent"
                    },
                    severity=alert.get("severity", "critical")
                )

            # Rate-limit ve ban risklerinde TrafficPoliceman'i çağır
            if error_type in ["rate_limit_429", "ban_risk"]:
                agent_name = alert.get("agent")
                if agent_name:
                    # Karantina başlat
                    self.policeman.quarantine_agent(agent_name, alert.get("log_line"))
                    # Emergency Stop kontrolü
                    if self.policeman.is_emergency_stop():
                        print(f"[Guardian] Emergency Stop aktif! Tüm işlemler durduruluyor. Sebep: {self.policeman._load_emergency_stop().get('reason')}")
                        # Guardian döngüsünü kırmak için bir flag kullanılabilir, 
                        # burada sadece log bırakıyoruz, döngü run_once içinde kontrol edilecek.

    def _load_emergency_stop(self) -> Dict:
        """Emergency Stop dosyasını okur."""
        try:
            with open("emergency_stop.flag", "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return {"active": False}

    def run_once(self):
        """
        Tek bir tarama döngüsü çalıştırır.
        Emergency Stop aktifse tarama yapmaz.
        """
        # Emergency Stop kontrolü
        if self.policeman.is_emergency_stop():
            print("[Guardian] Emergency Stop aktif – tarama atlandı.")
            return []

        alerts = self.scan_logs()
        if alerts:
            self.report_alerts(alerts)
            print(f"[GuardianAgent] {len(alerts)} hata/tehdit tespit edildi.")
        return alerts

    def start_daemon(self):
        """
        Sonsuz döngü ile periyodik tarama başlatır.
        Emergency Stop aktif olduğunda döngü kırılır ve daemon durur.
        """
        while True:
            # Emergency Stop kontrolü – aktifse döngüyü kır
            if self.policeman.is_emergency_stop():
                print("[Guardian] Emergency Stop algılandı. Daemon durduruluyor.")
                break
            self.run_once()
            time.sleep(self.scan_interval)