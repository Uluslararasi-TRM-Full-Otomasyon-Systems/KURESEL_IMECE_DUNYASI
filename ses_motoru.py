import os
import shutil
from multiprocessing import get_context
from queue import Empty

try:
    from gtts import gTTS
except ModuleNotFoundError:
    gTTS = None

try:
    from pydub import AudioSegment
    from pydub.effects import speedup
except ModuleNotFoundError:
    AudioSegment = None
    speedup = None

try:
    import imageio_ffmpeg
except ModuleNotFoundError:
    imageio_ffmpeg = None


def _ses_hizlandir(dosya_yolu, hiz_orani):
    if AudioSegment is None or speedup is None:
        return dosya_yolu

    ffmpeg_yolu = shutil.which("ffmpeg")
    if not ffmpeg_yolu and imageio_ffmpeg is not None:
        try:
            ffmpeg_yolu = imageio_ffmpeg.get_ffmpeg_exe()
        except Exception:
            ffmpeg_yolu = None

    if not ffmpeg_yolu:
        return dosya_yolu

    try:
        AudioSegment.converter = ffmpeg_yolu
        ses = AudioSegment.from_file(dosya_yolu, format="mp3")
        hizli_ses = speedup(ses, playback_speed=hiz_orani, chunk_size=150, crossfade=25)
        hizli_ses.export(dosya_yolu, format="mp3")
        return dosya_yolu if os.path.exists(dosya_yolu) and os.path.getsize(dosya_yolu) > 0 else None
    except Exception:
        return dosya_yolu


def _ses_dosyasi_uret(metin, dosya_yolu, dil_kodu, tld, yavas_konusma, hiz_orani, sonuc_kuyrugu):
    try:
        if gTTS is None:
            sonuc_kuyrugu.put(None)
            return

        tts = gTTS(
            text=metin,
            lang=dil_kodu,
            tld=tld,
            slow=False,
        )
        tts.save(dosya_yolu)
        hizlandirilmis_dosya = _ses_hizlandir(dosya_yolu, hiz_orani)

        if hizlandirilmis_dosya and os.path.exists(hizlandirilmis_dosya) and os.path.getsize(hizlandirilmis_dosya) > 0:
            sonuc_kuyrugu.put(hizlandirilmis_dosya)
        else:
            sonuc_kuyrugu.put(None)
    except Exception:
        sonuc_kuyrugu.put(None)


class SanalElSesMotoru:
    def __init__(self):
        """
        Sanal El Ses Motoru altyapısını hazırlar.
        gTTS tabanli Turkce seslendirme altyapisini hazirlar.
        """
        self.dil_kodu = "tr"
        self.tld = "com.tr"
        self.yavas_konusma = False
        self.hiz_orani = 1.15
        self.timeout_saniye = 5

    def metni_seslendir(self, metin, dosya_adi="otonom_reklam.mp3"):
        """
        Icerik fabrikasindan gelen reklam metnini gTTS ile Turkce MP3 ses dosyasina donusturur.
        """
        print(f"[Sanal El] Seslendirme işlemi başlatıldı: '{metin[:30]}...'")

        if not metin or not metin.strip():
            print("Hata oluştu")
            return None

        if gTTS is None:
            print("Hata oluştu")
            return None

        dosya_yolu = os.path.abspath(dosya_adi)
        if not dosya_yolu.lower().endswith(".mp3"):
            dosya_yolu = f"{dosya_yolu}.mp3"
        os.makedirs(os.path.dirname(dosya_yolu) or ".", exist_ok=True)

        try:
            context = get_context("spawn")
            sonuc_kuyrugu = context.Queue()
            islem = context.Process(
                target=_ses_dosyasi_uret,
                args=(
                    metin,
                    dosya_yolu,
                    self.dil_kodu,
                    self.tld,
                    self.yavas_konusma,
                    self.hiz_orani,
                    sonuc_kuyrugu,
                ),
            )
            islem.start()
            islem.join(self.timeout_saniye)
            if islem.is_alive():
                try:
                    islem.terminate()
                except Exception:
                    pass
                try:
                    islem.join(1)
                except Exception:
                    pass
                print("Hata oluştu")
                return None

            try:
                sonuc = sonuc_kuyrugu.get_nowait()
            except Empty:
                sonuc = None

            if islem.exitcode == 0 and sonuc and os.path.exists(sonuc):
                print(f"[Sanal El] Turkce MP3 ses dosyasi basariyla uretildi: {sonuc}")
                return sonuc

            print("Hata oluştu")
            return None
        except Exception:
            print("Hata oluştu")
            return None
