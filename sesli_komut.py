import os
import time

def metni_sese_cevir_ve_oku(metin, hiz=1.0):
    """
    TRM Otonom Ekosistemi için Sesli Asistan Motoru.
    Gelişmiş aşamada ElevenLabs ve gTTS API'leri buraya bağlanacaktır.
    """
    print(f"\n🎙️ [TRM ASİSTAN] Okunuyor (Hız: {hiz}): '{metin}'")
    
    # İşletim sisteminin kendi ses motorunu kullanarak ilk testi yapıyoruz
    try:
        if os.name == 'nt': # Windows işletim sistemi için
            import win32com.client
            speaker = win32com.client.Dispatch("SAPI.SpVoice")
            # Ses hızını ayarlama (SAPI hızı -10 ile 10 arasındadır)
            speaker.Rate = int((hiz - 1.0) * 10)
            speaker.Speak(metin)
        else:
            # Mac veya Linux için terminal sesini tetikler
            os.system(f"say '{metin}'")
            
    except Exception as e:
        print(f"⚠️ Ses çalınırken bir mikron hata oluştu: {e}")

if __name__ == "__main__":
    print("==================================================")
    print("🔊 TRM SESLİ ASİSTAN MOTORU (`sesli_komut.py`) AKTİF")
    print("==================================================")
    
    # İlk açılış ve hoş geldiniz testi
    test_mesaji = "Merhaba Fahri Bey. TRM Küresel İmece Dünyası ses motoru başarıyla çalıştırıldı. Sisteminiz sıfır hata ile nöbette."
    metni_sese_cevir_ve_oku(test_mesaji, hiz=1.0)
