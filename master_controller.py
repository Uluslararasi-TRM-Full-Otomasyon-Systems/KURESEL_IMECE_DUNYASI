import os
import asyncio
from groq import Groq
from dotenv import load_dotenv

load_dotenv('config.env')
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

class GucluSistem:
    def __init__(self):
        self.model = "llama-3.3-70b-versatile"

    async def ajan_gorev_yurut(self, ajan_id, uzmanlik, gorev):
        try:
            # Hata olduğunda sistemin durmaması için burada kısa bir rastgele bekleme ekleyebiliriz
            response = client.chat.completions.create(
                messages=[{"role": "user", "content": f"{uzmanlik} olarak: {gorev}"}],
                model=self.model,
            )
            return f"Ajan_{ajan_id}: {response.choices[0].message.content}"
        except Exception:
            return f"Ajan_{ajan_id}: Geçici olarak meşgul."

    async def imece_yurut(self, gorev):
        if not os.path.exists("raporlar"):
            os.makedirs("raporlar")
            
        print(f"--- OPERASYON BAŞLADI ---")
        
        # 'a' (append) modu ile dosyayı açıyoruz ki her seferinde silinmesin
        with open("raporlar/toplanan_veriler.txt", "a", encoding="utf-8") as f:
            for grup_no in range(0, 200, 5): # 10'ar değil 5'erli grup
                print(f"Grup {grup_no//5 + 1} iş başında...")
                tasks = [self.ajan_gorev_yurut(f"{i:03d}", "Uzman", gorev) for i in range(grup_no + 1, grup_no + 6)]
                sonuclar = await asyncio.gather(*tasks)
                
                for s in sonuclar:
                    f.write(s + "\n")
                    print(s)
                
                # API limitine takılmamak için bekleme süresini 5 saniyeye çıkardık
                await asyncio.sleep(5) 
        
        print(f"\n--- OPERASYON TAMAMLANDI. Veriler 'raporlar/toplanan_veriler.txt' içinde. ---")

if __name__ == "__main__":
    sistem = GucluSistem()
    asyncio.run(sistem.imece_yurut("Türkiye e-ticaret fırsatı öner."))