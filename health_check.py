# run_scraper.py içine eklenecek fonksiyon
def health_check_pre_flight(agent_name: str) -> bool:
    """
    Ajan çalıştırılmadan önce bağımlılıkları ve dosya bütünlüğünü kontrol eder.
    Uygun değilse False döner ve Guardian'a bildirir.
    """
    import os
    import json
    from datetime import datetime

    # Kontrol edilecek dosyalar (örnek)
    required_files = [
        os.path.join("trm_agents", f"{agent_name}.py"),
        # başka bağımlılıklar eklenebilir
    ]
    missing = []
    for file_path in required_files:
        if not os.path.exists(file_path):
            missing.append(file_path)

    if missing:
        # Guardian'a bildir (intelligence_log.json'a yaz)
        alert = {
            "timestamp": datetime.now().isoformat(),
            "agent": agent_name,
            "error_type": "pre_flight_failed",
            "log_line": f"Pre-flight check failed: missing files {missing}",
            "severity": "critical"
        }
        try:
            with open("intelligence_log.json", "r", encoding="utf-8") as f:
                data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            data = {}
        if "guardian_alerts" not in data:
            data["guardian_alerts"] = []
        data["guardian_alerts"].append(alert)
        with open("intelligence_log.json", "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        print(f"[Pre-flight] {agent_name} uygun değil, eksik dosyalar: {missing}")
        return False

    print(f"[Pre-flight] {agent_name} uygun, çalıştırılabilir.")
    return True