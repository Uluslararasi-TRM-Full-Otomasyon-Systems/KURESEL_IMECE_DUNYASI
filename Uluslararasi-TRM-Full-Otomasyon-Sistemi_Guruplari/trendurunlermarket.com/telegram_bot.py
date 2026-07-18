# ============================================
# AI DESTEKLİ TELEGRAM MÜŞTERİ ASİSTANI
# Claude API ile akıllı cevaplar
# ============================================

import os
import telebot
import anthropic
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
CLAUDE_API_KEY = os.getenv('CLAUDE_API_KEY')

bot = telebot.TeleBot(TOKEN)
claude = anthropic.Anthropic(api_key=CLAUDE_API_KEY)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    welcome_text = (
        "🤖 Merhaba! Ben TRM AI Asistan.\n\n"
        "Bana istediğin soruyu sorabilirsin: ürünler, fiyatlar, kargo, stok...\n"
        "Hemen cevaplayayım! 💬"
    )
    bot.reply_to(message, welcome_text)

@bot.message_handler(commands=['urunler'])
def send_products(message):
    # Ürün listesini buraya ekleyebilirsin (isteğe bağlı)
    urunler = """
    🛍️ Popüler Ürünlerimiz:
    - Xiaomi Akıllı Bileklik - 449 TL
    - ChefMax Doğrayıcı - 449 TL
    - Korkmaz Tava - 199 TL
    - Termal Çorap - 49 TL
    """
    bot.reply_to(message, urunler)

@bot.message_handler(func=lambda m: True)
def ai_responder(message):
    """Gelen her mesajı Claude'a sor ve cevap ver"""
    try:
        # Kullanıcı mesajını al
        user_message = message.text
        
        # Claude'a sor
        prompt = f"""
        Bir müşteri soru soruyor. Nazik, yardımsever ve kısa cevap ver.
        Müşteri: {user_message}
        
        Cevap:
        """
        
        response = claude.messages.create(
            model="claude-3-sonnet-20241022",
            max_tokens=300,
            temperature=0.7,
            messages=[{"role": "user", "content": prompt}]
        )
        
        answer = response.content[0].text.strip()
        
        # Cevabı gönder
        bot.reply_to(message, answer)
        
    except Exception as e:
        bot.reply_to(message, "😔 Şu anda teknik bir sorun var. Lütfen daha sonra tekrar dene.")
        print(f"Hata: {e}")

print("🤖 AI Asistan başlatıldı...")
bot.infinity_polling()
