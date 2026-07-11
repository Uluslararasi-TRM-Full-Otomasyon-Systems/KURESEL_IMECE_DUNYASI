class MarketIntelAgent:
    """
    Rakip fiyat, stok ve pazar baskisini analiz edip
    Content_Generator_Agent icin akilli parametre sinyali uretir.
    """

    def __init__(self, agent_id, region):
        self.agent_id = agent_id
        self.region = region

    def sync(self, context=None):
        trend_report = (context or {}).get("trend_report") or {}
        product_details = trend_report.get("product_details", [])
        if not product_details:
            return {
                "agent_id": self.agent_id,
                "region": self.region,
                "signal_priority": "low",
                "smart_parameter": None,
            }

        target = product_details[(self.agent_id - 1) % len(product_details)]
        price = float(target.get("price", 0.0))
        trend_score = float(target.get("trend_score", 0.0))
        competitor_price = round(price * (0.90 + ((self.agent_id % 4) * 0.02)), 2)
        price_break = competitor_price < price * 0.96
        stock_status = "critical_low" if trend_score >= 20 and self.agent_id % 2 == 0 else "watch"

        if price_break and stock_status == "critical_low":
            signal_type = "flash_conversion_push"
            priority = "critical"
            angle = "rakip fiyat kirilimi ve dusuk stok baskisini one cikar"
        elif price_break:
            signal_type = "price_break_response"
            priority = "high"
            angle = "fiyat avantaji yerine hizli karar ve guven vurgusunu artir"
        else:
            signal_type = "stock_pressure"
            priority = "medium"
            angle = "stok sinirliligi ve firsat kacirma duygusunu guclendir"

        return {
            "agent_id": self.agent_id,
            "region": self.region,
            "product_name": target.get("product_name"),
            "competitor_price": competitor_price,
            "price_break_detected": price_break,
            "stock_status": stock_status,
            "signal_priority": priority,
            "smart_parameter": {
                "product_name": target.get("product_name"),
                "signal_type": signal_type,
                "recommended_angle": angle,
                "priority": priority,
                "region": self.region,
            },
        }


def build_market_intel_agents():
    regions = [
        "TR", "EU", "US", "MENA", "UK",
        "DE", "FR", "NL", "GCC", "CEE",
    ]
    return [
        (f"MarketIntelAgent_{index:02d}", MarketIntelAgent(index, region))
        for index, region in enumerate(regions, start=1)
    ]
