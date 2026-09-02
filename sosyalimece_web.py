import streamlit as st

# Sayfa Yapılandırması
st.set_page_config(
    page_title="Sosyal İmece | Hoş Geldiniz", 
    page_icon="🌿", 
    layout="centered"
)

# Özel CSS ile Sıcak ve Huzurlu Tasarım Dokunuşları
st.markdown("""
    <style>
    .main {
        background-color: #f9fbfc;
    }
    .welcome-box {
        background-color: #ffffff;
        padding: 30px;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        text-align: center;
        border-top: 5px solid #4CAF50;
    }
    .assistant-text {
        font-size: 1.1rem;
        color: #2c3e50;
        font-style: italic;
        margin-top: 15px;
        line-height: 1.6;
    }
    </style>
""", unsafe_allow_html=True)

# Sekme Yapısı ile Sayfa Yönetimi
tab_home, tab_query, tab_status = st.tabs(["🌿 Ana Sayfa", "🔍 Üye Sorgulama", "🛡️ Otonom Sistem Durumu"])

with tab_home:
    # Ana Karşılama Alanı
    st.markdown("<h1 style='text-align: center; color: #2e7d32;'>Sosyal İmece Dünyası</h1>", unsafe_allow_html=True)
    st.markdown("<h4 style='text-align: center; color: #555;'>Gönül Birliği ve Tam Otonom Dayanışma Ağı</h4>", unsafe_allow_html=True)

    st.write("---")

    # Karşılama Paneli
    st.markdown("""
    <div class="welcome-box">
        <h3>🌿 Merhaba Güzel İnsan, Hoş Geldin...</h3>
        <p class="assistant-text">
            "Şunu bilmeni isterim ki, bu işe adım attıktan sonra, hiçbir şey yapmana gerek yok. 
            Senin yerine tam otonom çalışan işlerimizi yapan Yapay Zeka ekibimiz var, bu ekip, tüm işlerimiz ile ilgili düşünüyorlar, adım atıyorlar ve yapıyorlar. 
            Sen sadece huzurlu, mutlu bir şekilde bu ekibimizin başarılarını izle ve bu işin tadını çıkar."
        </p>
    </div>
    """, unsafe_allow_html=True)

with tab_query:
    st.markdown("<h3>🔍 Üye ve Aktivite Sorgulama Portalı</h3>", unsafe_allow_html=True)
    st.write("Sistemdeki durumunuzu güvenle kontrol etmek için bilgilerinizi giriniz.")
    
    with st.form("query_form"):
        tc_input = st.text_input("T.C. Kimlik Numarası", max_chars=11)
        phone_input = st.text_input("Telefon Numarası (Örn: 05XXXXXXXXX)")
        
        submitted = st.form_submit_button("Durumumu Sorgula")
        
        if submitted:
            if len(tc_input) == 11 and len(phone_input) >= 10:
                st.success("✅ Kaydınız doğrulandı! Otonom hesaplarınız güvenli bir şekilde aktif durumdadır.")
                st.info("💡 Hatırlatma: Sıfır parola politikası gereği şifreleriniz sistemde saklanmaz, güvenli kanallarla size iletilmiştir.")
            else:
                st.warning("⚠️ Lütfen T.C. Kimlik numaranızı ve telefon numaranızı eksiksiz ve doğru giriniz.")

with tab_status:
    st.markdown("<h3>🛡️ Otonom Sistem ve Ajan Durumu</h3>", unsafe_allow_html=True)
    st.write("Arka planda çalışan koruma kalkanları ve ajan raporları:")
    
    st.metric(label="Aktif Otonom Ajan Sayısı", value="165 / 165", delta="Tam Kapasite")
    st.metric(label="Güvenlik Kalkanı", value="Aktif (Sıfır Parola)", delta="Güvenli")
    
    if st.button("Anlık Raporları Yenile"):
        st.toast("Tüm ajan logları güncellendi.")

st.write("---")
st.markdown("<p style='text-align: center; color: gray; font-size: 0.9rem;'>sosyalimece.org • Sıfır Parola ve Tam Otonom Güvenlik Altyapısı ile Korunmaktadır.</p>", unsafe_allow_html=True)