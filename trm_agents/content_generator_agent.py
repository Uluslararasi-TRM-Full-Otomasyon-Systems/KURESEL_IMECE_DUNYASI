import json
import os
from datetime import datetime


class ContentGeneratorAgent:
    """
    Trend raporundaki fiyat ve komisyon verilerini kullanarak
    agresif ve ikna edici satış içerikleri üretir.
    """

    def __init__(self, reports_path=None, output_path=None):
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        self.reports_path = reports_path or os.path.join(base_dir, "trend_raporlari.json")
        self.output_path = output_path or os.path.join(base_dir, "content_generator_outputs.json")
        self.generated_contents = []

    def _load_reports(self):
        if not os.path.exists(self.reports_path):
            return []

        with open(self.reports_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        return data if isinstance(data, list) else []

    def load_latest_trend_report(self):
        reports = self._load_reports()
        if not reports:
            return None
        return reports[-1]

    def _extract_product_details(self, trend_report):
        details = trend_report.get("product_details", [])
        if details:
            return details

        fallback_scores = trend_report.get("scores", {})
        extracted = []
        for product_name, trend_score in fallback_scores.items():
            extracted.append(
                {
                    "product_name": product_name,
                    "trend_score": trend_score,
                    "price": 0.0,
                    "commission_rate": 0.0,
                    "estimated_commission": 0.0,
                    "product_url": "",
                }
            )
        return extracted

    def _rank_products(self, product_details):
        return sorted(
            product_details,
            key=lambda item: (
                item.get("commission_rate", 0.0),
                item.get("estimated_commission", 0.0),
                item.get("trend_score", 0.0),
                item.get("price", 0.0),
            ),
            reverse=True,
        )

    def _select_strategy_signal(self, product_name, smart_parameters):
        for signal in smart_parameters:
            if signal.get("product_name") == product_name:
                return signal
        return smart_parameters[0] if smart_parameters else None

    def _build_content_bundle(self, product, position, strategy_signal=None):
        product_name = product.get("product_name", "Bilinmeyen Ürün")
        trend_score = product.get("trend_score", 0)
        price = product.get("price", 0.0)
        commission_rate = product.get("commission_rate", 0.0)
        estimated_commission = product.get("estimated_commission", 0.0)
        product_url = product.get("product_url", "")
        signal_line = ""

        if position == 1:
            urgency = "En yüksek komisyonlu sıcak fırsat"
            angle = "hemen aksiyon aldıran agresif satış kurgusu"
        else:
            urgency = "Satışa dönmeye çok yakın ürün"
            angle = "kararsız müşteriyi ikna eden güçlü teklif dili"

        if strategy_signal:
            signal_line = (
                f" Pazar istihbarat sinyali: {strategy_signal.get('recommended_angle', '-')}. "
                f"Oncelik: {strategy_signal.get('priority', '-')}, bolge: {strategy_signal.get('region', '-')}. "
            )

        short_caption = (
            f"{urgency}: {product_name}. "
            f"Fiyat {price:.2f} TL, komisyon %{commission_rate:.1f}, beklenen kazanç {estimated_commission:.2f} TL."
        )
        promo_text = (
            f"{product_name} şu anda yalnızca trend olduğu için değil, aynı zamanda "
            f"%{commission_rate:.1f} komisyon oranıyla öne çıktığı için agresif biçimde itilmeli. "
            f"{price:.2f} TL fiyat bandındaki bu ürün için {angle}. "
            f"{signal_line}Mesajın merkezine fırsat, sınırlı zaman ve net fayda koy."
        )
        social_post = (
            f"{product_name} için alarm verildi.\n"
            f"Fiyat: {price:.2f} TL\n"
            f"Komisyon: %{commission_rate:.1f} | Tahmini kazanç: {estimated_commission:.2f} TL\n"
            "Bu ürün şu an paylaşılmazsa fırsat kaçabilir. Hemen linke yönlendir."
        )
        hashtags = [
            "#trendurun",
            "#yuksekkomisyon",
            "#satisfirsati",
            "#hemenincele",
            "#eticaret",
        ]

        return {
            "product_name": product_name,
            "trend_score": trend_score,
            "price": round(price, 2),
            "commission_rate": round(commission_rate, 2),
            "estimated_commission": round(estimated_commission, 2),
            "position": position,
            "product_url": product_url,
            "short_caption": short_caption,
            "promo_text": promo_text,
            "social_post": social_post,
            "hashtags": hashtags,
            "call_to_action": "Yüksek komisyon fırsatını öne çıkar ve hemen yönlendir.",
            "strategy_signal": strategy_signal or {},
        }

    def generate_from_report(self, trend_report=None, smart_parameters=None, bridge_network_reports=None):
        trend_report = trend_report or self.load_latest_trend_report()
        if not trend_report:
            return None

        product_details = self._extract_product_details(trend_report)
        ranked_products = self._rank_products(product_details)
        smart_parameters = smart_parameters or []
        bridge_network_reports = bridge_network_reports or []

        bundles = []
        for index, product in enumerate(ranked_products[:3], start=1):
            signal = self._select_strategy_signal(product.get("product_name"), smart_parameters)
            bundles.append(self._build_content_bundle(product, index, signal))

        lead_product = bundles[0] if bundles else {}
        payload = {
            "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "source_report_timestamp": trend_report.get("timestamp"),
            "top_trend": trend_report.get("top_trend"),
            "lead_product": lead_product.get("product_name"),
            "lead_commission_rate": lead_product.get("commission_rate", 0.0),
            "lead_estimated_commission": lead_product.get("estimated_commission", 0.0),
            "total_products": trend_report.get("total_products", 0),
            "smart_parameter_count": len(smart_parameters),
            "bridge_sync_count": len(bridge_network_reports),
            "contents": bundles,
        }

        self.generated_contents = bundles
        return payload

    def save_generated_contents(self, payload):
        if not payload:
            return False

        existing_payloads = []
        if os.path.exists(self.output_path):
            try:
                with open(self.output_path, "r", encoding="utf-8") as f:
                    existing_payloads = json.load(f)
                if not isinstance(existing_payloads, list):
                    existing_payloads = []
            except Exception:
                existing_payloads = []

        existing_payloads.append(payload)
        existing_payloads = existing_payloads[-10:]

        with open(self.output_path, "w", encoding="utf-8") as f:
            json.dump(existing_payloads, f, ensure_ascii=False, indent=2)

        return True

    def get_latest_generated_contents(self):
        if not os.path.exists(self.output_path):
            return None

        with open(self.output_path, "r", encoding="utf-8") as f:
            payloads = json.load(f)

        if not payloads:
            return None

        return payloads[-1]

    def sync(self, context=None):
        trend_report = None
        smart_parameters = []
        bridge_network_reports = []
        if context:
            trend_report = context.get("trend_report")
            smart_parameters = context.get("smart_parameters", [])
            bridge_network_reports = context.get("bridge_network_reports", [])

        payload = self.generate_from_report(trend_report, smart_parameters, bridge_network_reports)
        if payload:
            self.save_generated_contents(payload)
        return payload

# SATIR SİLİNDİ – Artık hata yok