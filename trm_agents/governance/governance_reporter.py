import json
import os


def update_health_record(agent_name, status, message):
    report_path = os.path.join("trm_agents", "governance", "governance_report.json")
    data = {}
    if os.path.exists(report_path):
        with open(report_path, "r", encoding="utf-8") as file:
            try:
                data = json.load(file)
            except Exception:
                data = {}

    data[agent_name] = {
        "status": status,
        "message": message,
        "timestamp": "current",
    }
    with open(report_path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)
