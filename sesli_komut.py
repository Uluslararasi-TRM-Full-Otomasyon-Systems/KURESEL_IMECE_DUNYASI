import os
import time

def metni_sese_cevir_ve_oku(metin, hiz=1.0):
    """
    TRM Otonom Ekosistemi icin Sesli Asistan Motoru.
    Gelismis asamada ElevenLabs ve gTTS API'leri buraya baglanacaktir.
    """
    print(f"\n🎙️ [TRM ASISTAN] Okunuyor (Hiz: {hiz}): '{metin}'")
    
    # Isletim sisteminin kendi ses motorunu kullanarak ilk testi yapiyoruz
    try:
        if os.name == 'nt': # Windows isletim sistemi icin
            import win32com.client
            speaker = win32com.client.Dispatch("SAPI.SpVoice")
            # Ses hizini ayarlama (SAPI hizi -10 ile 10 arasindadir)
            speaker.Rate = int((hiz - 1.0) * 10)
            speaker.Speak(metin)
        else:
            # Mac veya Linux icin terminal sesini tetikler
            os.system(f"say '{metin}'")
            
    except Exception as e:
        print(f"⚠️ Ses calinirken bir mikron hata olustu: {e}")

if __name__ == "__main__":
    print("==================================================")
    print("🔊 TRM SESLI ASISTAN MOTORU (`sesli_komut.py`) AKTIF")
    print("==================================================")
    
    # Ilk acilis ve hos geldiniz testi
    test_mesaji = "Merhaba Fahri Bey. TRM Kuresel Imece Dunyasi ses motoru basariyla calistirildi. Sisteminiz sifir hata ile nobette."
    metni_sese_cevir_ve_oku(test_mesaji, hiz=1.0)
