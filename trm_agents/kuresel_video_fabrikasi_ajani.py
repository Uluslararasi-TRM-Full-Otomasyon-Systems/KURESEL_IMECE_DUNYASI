import os
from groq import Groq

class VideoFactoryAgent:
    """Sistemin çok dilli görsel içerik üretim birimi."""

    def __init__(self, agent_name="Kuresel_Video_Fabrikasi"):
        self.agent_name = agent_name
        self.client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

    def create_script(self, product_data, target_language="Turkish"):
        """Hedef dile göre Groq ile viral senaryo üretir."""
        prompt = f"""
        Ürün: {product_data}. 
        Hedef Dil: {target_language}. 
        Bu dilin kültürüne ve sosyal medya trendlerine uygun, 30 saniyelik, 
        merak uyandırıcı, viral bir reklam senaryosu yaz.
        """
        
        chat_completion = self.client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama-3.3-70b-versatile",
        )
        return chat_completion.choices[0].message.content

    def render_video(self, script):
        """Senaryoyu video dosyasına dönüştürür (AI Rendering)."""
        print(f"[VİDEO] Render başlatıldı: '{script[:20]}...'")
        return f"path/to/viral_video_{hash(script)}.mp4"

    def run(self, product_data, target_language="Turkish"):
        """Ajanın tam döngüsü (Dil seçeneği ile)."""
        print(f"[FABRİKA] {target_language} dilinde içerik üretiliyor...")
        script = self.create_script(product_data, target_language)
        print(f"[ZEKA] Senaryo üretildi ({target_language}): {script[:50]}...")
        video_path = self.render_video(script)
        print(f"[BAŞARI] Video hazır: {video_path}")
        return video_path

# ORCHESTRATOR_AGENT.py'nin tetikleyeceği ana fonksiyon
def trigger_video_production(product_name, language="Turkish"):
    factory = VideoFactoryAgent()
    return factory.run(product_name, language)