# Wallet_Agent.py içinde basitleştirilmiş mantık

def process_withdrawal(user_session, iban_number):
    # 1. IBAN'ı veritabanına KAYDETME, sadece ödeme API'sine gönder
    payment_status = payment_gateway.send_money(
        amount=user_session.balance, 
        destination=iban_number
    )
    
    # 2. İşlem biter bitmez IBAN değişkenini bellekten temizle
    iban_number = None 
    del iban_number
    
    return payment_status