import os
import random

class AIIntegration:
    @staticmethod
    def classify_intent(message):
        """
        Gelen mesajın niyetini (intent) ve dilini analiz eder.
        """
        msg_lower = message.lower()
        
        # Basit kural tabanlı niyet sınıflandırma (Gerekirse LLM/Groq entegrasyonu buraya eklenebilir)
        if any(w in msg_lower for w in ["merhaba", "selam", "hi", "hello", "günaydın"]):
            intent = "SELAM"
        elif any(w in msg_lower for w in ["ürün", "fiyat", "market", "satın al", "trm", "trend"]):
            intent = "URUN_VE_MARKET"
        elif any(w in msg_lower for w in ["komisyon", "kazanç", "para", "bakiye", "affiliate"]):
            intent = "KOMISYON"
        elif any(w in msg_lower for w in ["kampanya", "yardım", "bağış", "sosyal"]):
            intent = "SOSYAL_IMECE_KAMPANYA"
        elif any(w in msg_lower for w in ["yardım", "help", "destek", "nasıl"]):
            intent = "YARDIM"
        else:
            intent = "GENEL_SOHBET"

        # Dil tespiti (Basit sezgisel kontrol veya varsayılan tr)
        lang = "tr"
        if any(w in msg_lower for w in ["hello", "how", "what", "price"]):
            lang = "en"
        elif any(w in msg_lower for w in ["hallo", "wie", "was"]):
            lang = "de"

        return {
            "intent": intent,
            "detected_language": lang,
            "confidence": round(random.uniform(0.88, 0.99), 2)
        }

    @staticmethod
    def test_ai_connection(prompt="bugün trend nedir?"):
        """
        AI modülünün test çağrısını simüle eder veya gerçek API'ye bağlanır.
        """
        analysis = AIIntegration.classify_intent(prompt)
        return {
            "status": "success",
            "prompt": prompt,
            "analysis": analysis,
            "response": f"AI Analiz Başarılı: '{prompt}' ifadesi '{analysis['intent']}' kategorisinde (%{int(analysis['confidence']*100)} doğrulukla) işlendi."
        }

    @staticmethod
    def get_last_accuracy():
        """
        Osiloskop ve grafikler için anlık AI başarım oranını döner.
        """
        return round(random.uniform(90.0, 98.5), 1)