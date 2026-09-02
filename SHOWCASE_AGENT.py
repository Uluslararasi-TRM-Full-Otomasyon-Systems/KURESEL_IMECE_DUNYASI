import streamlit as st
import pyttsx3
import threading
import time

# Sesli Komut Motoru
def sesli_anons(metin):
    def run():
        engine = pyttsx3.init()
        engine.setProperty('rate', 130) # Biraz daha tok ve otoriter
        engine.say(metin)
        engine.runAndWait()
    threading.Thread(target=run).start()

st.set_page_config(page_title="MARASAL ROBOTIK KOMUTA", layout="wide")

# Lider Robot ve Asker Robot Gorselleri (Sizin otoritenizi temsil eden buyuk robot ve sahada kosan minikler)
col1, col2 = st.columns([1, 2])
with col1:
    st.image("https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExNHJqZ2h1bW56ZzM0eXo5ZWU5ZzM0eXo5ZWU5ZzM0eXo5ZWU5ZzM0JmVwPXYxX2ludGVybmFsX2dpZl9ieV9pZCZjdD1n/12bNCUZS34tTXi/giphy.gif", width=250) # Otoriter lider robot
    st.markdown("### 👑 MARASAL FAHRI BEY")

with col2:
    st.image("https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExNHJqZ2h1bW56ZzM0eXo5ZWU5ZzM0eXo5ZWU5ZzM0eXo5ZWU5ZzM0JmVwPXYxX2ludGVybmFsX2dpZl9ieV9pZCZjdD1n/3o7TKMGpxxHOGTdzJC/giphy.gif", width=400) # Sahada kosan robotlar
    st.write("### 🤖 220 Otonom Ajan - Sahada Operasyonel")

st.write("---")

if st.button("🚀 KOMUTANI EMRETTI: HAREKETE GECIN!"):
    sesli_anons("Dikkat 220 ajan, Marasal Fahri Bey'in emriyle operasyon basliyor. Kuresel agda yerinizi alin.")
    st.success("Komut iletildi. Ajanlar dagiliyor...")
    time.sleep(2)
    st.info("Islem Gunlugu: Uluslararasi firmalar ile baglanti kuruldu, veri akisi aktif.")
    sesli_anons("Islem tamamlandi, verimlilik yuzde 100.")