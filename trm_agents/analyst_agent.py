import json
import os
from datetime import datetime
from collections import Counter
import re

class AnalystAgent:
    def __init__(self):
        self.trend_keywords = {
            'organic': ['organik', 'doğal', 'bitkisel'],
            'beauty': ['kozmetik', 'cilt', 'bakım', 'krem', 'nemlendirici'],
            'food': ['zeytin', 'bal', 'gıda', 'sağlık', 'besin'],
            'personal_care': ['şampuan', 'saç', 'duş', 'kişisel bakım']
        }
    
    def analyze_pool(self, pool_path):
        """
        ACIL_SATIS_HAVUZU.txt dosyasını okur ve ürünleri analiz eder.
        En çok ilgi çekme potansiyeli olan ürünü belirler.
        """
        try:
            if not os.path.exists(pool_path):
                print(f"[AnalystAgent] Havuz dosyası bulunamadı: {pool_path}")
                return None
            
            products = []
            with open(pool_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                for line in lines:
                    if '-' in line and 'http' in line:
                        # Ürün başlığını çıkar
                        parts = line.split(' - ')
                        if len(parts) >= 2:
                            product_title = parts[0].strip()
                            products.append(product_title)
            
            if not products:
                print("[AnalystAgent] Analiz edilecek ürün bulunamadı.")
                return None
            
            # Trend analizi
            trend_scores = {}
            for product in products:
                score = self._calculate_trend_score(product)
                trend_scores[product] = score
            
            # En yüksek skora sahip ürünü bul
            top_product = max(trend_scores, key=trend_scores.get)
            
            analysis_result = {
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'total_products': len(products),
                'top_trend': top_product,
                'trend_score': trend_scores[top_product],
                'all_products': products,
                'scores': trend_scores
            }
            
            return analysis_result
            
        except Exception as e:
            print(f"[AnalystAgent] Analiz hatası: {str(e)}")
            return None
    
    def _calculate_trend_score(self, product_title):
        """
        Ürün başlığına göre trend skoru hesaplar.
        Anahtar kelime frekansına göre puanlama yapar.
        """
        score = 0
        title_lower = product_title.lower()
        
        # Trend anahtar kelimelerini kontrol et
        for category, keywords in self.trend_keywords.items():
            for keyword in keywords:
                if keyword in title_lower:
                    score += 10  # Her eşleşme için 10 puan
        
        # Başlık uzunluğuna göre bonus (daha spesifik başlıklar daha yüksek puan)
        if len(product_title.split()) >= 3:
            score += 5
        
        # Sayısal değer varsa bonus (1L, 500ml vb.)
        if re.search(r'\d+', product_title):
            score += 3
        
        return score
    
    def save_trend_report(self, analysis_result, output_path):
        """
        Analiz sonucunu trend_raporlari.json dosyasına kaydeder.
        """
        try:
            # Mevcut raporları oku (varsa)
            existing_reports = []
            if os.path.exists(output_path):
                with open(output_path, 'r', encoding='utf-8') as f:
                    existing_reports = json.load(f)
            
            # Yeni raporu ekle
            existing_reports.append(analysis_result)
            
            # Son 10 raporu tut (dosya büyümesini önlemek için)
            if len(existing_reports) > 10:
                existing_reports = existing_reports[-10:]
            
            # Kaydet
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(existing_reports, f, ensure_ascii=False, indent=2)
            
            print(f"[AnalystAgent] Trend raporu kaydedildi: {output_path}")
            return True
            
        except Exception as e:
            print(f"[AnalystAgent] Rapor kayıt hatası: {str(e)}")
            return False
    
    def get_trend_summary(self, analysis_result):
        """
        E-posta için trend özeti döndürür.
        """
        if not analysis_result:
            return "Trend analizi yapılamadı."
        
        return f"Bugünün Öne Çıkan Trendi: {analysis_result['top_trend']}"
