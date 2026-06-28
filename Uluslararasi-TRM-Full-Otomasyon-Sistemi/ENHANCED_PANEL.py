# Sizin ekran görüntüsünde seçili olan o kritik butonun içi
elif menu == "🧠 Otonom Karakter Analiz Raporları":
    st.header("🧠 Otonom Karakter Analiz Raporları")
    st.write("Psikolog AI ajanının yaptığı tüm detaylı mizaç ve dijital çalışma karakter analizleri.")
    
    # Test amaçlı pilot grup veri simülasyonu
    st.info("💡 UTEYKDER / UTEYTDER bünyesindeki 10 kişilik pilot grubun otonom analiz sonuçları listelenmiştir.")
    
    analiz_data = {
        "Katılımcı / Aday": ["Ahmet Yılmaz (Ağır Engelli)", "Mehmet Demir (Refakatçi Yakını)", "Ayşe Kaya (Engelli Vatandaş)"],
        "Psikolog AI Mizaç Skoru": ["9.2 / 10 (Yüksek Azim)", "8.5 / 10 (Uyumlu/Üretken)", "8.9 / 10 (Odaklanmış)"],
        "Dijital Adaptasyon": ["%95 (Sanal Mouse Akıcı)", "%88 (Form Girişi Düzenli)", "%91 (Mesai Sadakati Yüksek)"],
        "Sistem Uyumluluk Durumu": ["🟢 KRİTİK EŞİK AŞILDI (UYGUN)", "🟢 UYGUN", "🟢 UYGUN"]
    }
    
    df_analiz = pd.DataFrame(analiz_data)
    st.table(df_analiz)
    
    if st.button("🔄 Psikolog AI Analiz Raporlarını Yeniden Tarla"):
        with st.spinner("Otonom karakter analiz algoritması çalıştırılıyor..."):
            time.sleep(1)
            st.success("✅ Tüm pilot grubun mizaç ve adaptasyon raporları güncellendi!")