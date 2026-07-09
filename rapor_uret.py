from fpdf import FPDF

class EnvanterPDF(FPDF):
    def header(self):
        self.set_font('Helvetica', 'B', 12)
        # Türkçe karakterleri desteklemesi için doğrudan çıktı veriyoruz
        self.cell(0, 10, 'TRM Nirvana v3.0 - Ajan ve Alt Modul Envanteri', new_x="LMARGIN", new_y="NEXT", align='C')
        self.ln(5)

def raporu_olustur():
    pdf = EnvanterPDF()
    pdf.add_page()
    
    # PDF içine fontu tanıtıyoruz (Unicode desteği için)
    pdf.set_font("Helvetica", size=10)
    
    yapı = {
        "1. ANA ORKESTRASYON": ["MASTER_CONTROLLER.py", "ORCHESTRATOR_AGENT.py", "HIZLI_BASLAT.py", "WATCHDOG.py"],
        "2. AJANLAR": ["sistem_muhafiz_ajani.py", "kuresel_video_fabrikasi_ajani.py", "cografi_arbitraj_ajani.py", "otonom_etkilesim_swarm_ajani.py", "kuresel_psikolog_ajani.py"],
        "3. YARDIMCI MODULLER": ["web_scraper.py", "google_drive_integration.py", "API_INTEGRATION_MANAGER.py", "config.py"],
        "4. KONFIGURASYON": ["credentials.json", "system_manager.log", "video_projeleri.json"]
    }

    for kategori, dosyalar in yapı.items():
        pdf.set_font("Helvetica", 'B', 12)
        # Türkçe karakterleri İngilizce karşılıklarıyla yazdırıyoruz (hata riskini sıfıra indirir)
        kategori_clean = kategori.replace('İ', 'I').replace('Ü', 'U').replace('Ö', 'O').replace('Ş', 'S').replace('Ç', 'C').replace('Ğ', 'G')
        pdf.cell(0, 10, kategori_clean, new_x="LMARGIN", new_y="NEXT")
        
        pdf.set_font("Helvetica", size=10)
        for dosya in dosyalar:
            pdf.cell(0, 8, f"- {dosya}", new_x="LMARGIN", new_y="NEXT")
        pdf.ln(5)

    pdf.output("TRM_Nirvana_Envanter.pdf")
    print("PDF basariyla olusturuldu: TRM_Nirvana_Envanter.pdf")

raporu_olustur()