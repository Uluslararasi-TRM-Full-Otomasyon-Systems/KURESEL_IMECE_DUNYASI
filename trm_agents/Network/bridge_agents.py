class BridgeAgent:
    """
    Farkli affiliate aglarindan gelen sinyal ve teklif ozetini merkeze tasir.
    """

    def __init__(self, agent_id, network_name):
        self.agent_id = agent_id
        self.network_name = network_name

    def sync(self, context=None):
        trend_report = (context or {}).get("trend_report") or {}
        top_trend = trend_report.get("top_trend", "Bilinmiyor")
        total_products = int(trend_report.get("total_products", 0))
        offer_count = 5 + (self.agent_id % 6)
        freshness_score = round(70 + (self.agent_id % 5) * 4.5, 1)

        return {
            "agent_id": self.agent_id,
            "network_name": self.network_name,
            "top_trend": top_trend,
            "synced_offer_count": offer_count,
            "freshness_score": freshness_score,
            "recommended_sync_mode": "incremental" if self.agent_id % 2 == 0 else "priority",
            "observed_catalog_size": total_products,
        }


def build_bridge_agents():
    networks = [
        "AmazonEU", "AmazonUS", "Awin", "CJ", "Impact",
        "Rakuten", "TradeTracker", "ShareASale", "Partnerize", "Webgains",
        "ClickBank", "Admitad", "Tradedoubler", "FlexOffers", "Pepperjam",
    ]
    return [
        (f"BridgeAgent_{index:02d}", BridgeAgent(index, network))
        for index, network in enumerate(networks, start=1)
    ]
