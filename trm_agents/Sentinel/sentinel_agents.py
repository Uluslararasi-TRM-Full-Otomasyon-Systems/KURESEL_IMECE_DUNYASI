class SentinelAgent:
    """
    Kuyruk, API ve guvenlik durumundan savunma sinyalleri uretir.
    """

    def __init__(self, agent_id, watch_zone):
        self.agent_id = agent_id
        self.watch_zone = watch_zone

    def sync(self, context=None):
        context = context or {}
        queue_payload = context.get("queue_payload") or {}
        poster_payload = context.get("poster_payload") or {}
        security_status = context.get("security_status") or {}

        queue_items = queue_payload.get("items", [])
        pending_retry = len([item for item in queue_items if item.get("status") == "pending_retry"])
        poster_retries = int(poster_payload.get("retry_count", 0))
        encrypted_snapshots = int(security_status.get("encrypted_snapshots", 0))

        severity = "info"
        anomaly = "normal_traffic"
        if pending_retry > 0 or poster_retries > 0:
            severity = "warning"
            anomaly = "api_retry_pressure"
        if not security_status.get("zero_trust_enabled", False):
            severity = "critical"
            anomaly = "zero_trust_disabled"
        elif encrypted_snapshots == 0:
            severity = "warning"
            anomaly = "unencrypted_sensitive_surface"

        return {
            "agent_id": self.agent_id,
            "watch_zone": self.watch_zone,
            "severity": severity,
            "anomaly": anomaly,
            "pending_retry_count": pending_retry,
            "poster_retry_count": poster_retries,
            "encrypted_snapshots": encrypted_snapshots,
        }


def build_sentinel_agents():
    watch_zones = [
        "Gateway", "API", "Queue", "Worker", "Health",
        "Identity", "ZeroTrust", "Network", "Content", "Publishing",
    ]
    return [
        (f"SentinelAgent_{index:02d}", SentinelAgent(index, zone))
        for index, zone in enumerate(watch_zones, start=1)
    ]
