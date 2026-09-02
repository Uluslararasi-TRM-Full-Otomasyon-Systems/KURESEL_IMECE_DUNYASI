import streamlit as st
import streamlit.components.v1 as components
import datetime

st.set_page_config(
    page_title="TRM Nirvana v3.0",
    layout="wide"
)

# --- HTML/CSS MODAL VE ARAYÜZ KODLARI ---
trm_interface_html = """
<style>
    :root { --primary-orange: #ffaa55; --bg-dark: #0a0f18; --panel-bg: #1a1f2e; }
    
    .container { display: flex; gap: 20px; justify-content: center; margin-top: 20px; }
    
    .btn { 
        background-color: var(--primary-orange); color: var(--bg-dark); 
        padding: 12px 24px; border: none; border-radius: 6px; 
        font-weight: bold; cursor: pointer; text-decoration: none; 
        font-family: sans-serif; transition: 0.3s;
    }
    .btn:hover { transform: scale(1.05); }

    /* Yumuşak Geçişli Modal */
    .modal {
        display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%;
        background: rgba(0, 0, 0, 0.7); justify-content: center; align-items: center;
        opacity: 0; transition: opacity 0.3s ease;
    }
    .modal.show { display: flex; opacity: 1; }
    .modal-content {
        background: var(--panel-bg); padding: 30px; border-radius: 12px;
        width: 400px; border: 1px solid var(--primary-orange); color: white;
        text-align: center;
    }
</style>

<div class="container">
    <a href="http://localhost:8501/" target="_blank" class="btn">Dashboard'u Aç</a>
    <button class="btn" onclick="openModal()">Küresel Entegrasyonlar</button>
</div>

<div id="firmaModal" class="modal" onclick="closeModal()">
    <div class="modal-content" onclick="event.stopPropagation()">
        <span style="float:right; cursor:pointer; color:var(--primary-orange);" onclick="closeModal()">X</span>
        <h3>TRM Küresel İşbirlikleri</h3>
        <p>Entegrasyon yönetimi aktif.</p>
    </div>
</div>

<script>
    function openModal() { document.getElementById('firmaModal').classList.add('show'); }
    function closeModal() { document.getElementById('firmaModal').classList.remove('show'); }
</script>
"""

# --- STREAMLIT ARAYÜZÜ ---
st.title("TRM NIRVANA v3.0 - Geliştirilmiş Yönetim Paneli")
st.markdown("---")

# HTML Bileşenini sayfaya ekle
components.html(trm_interface_html, height=150)

st.info("Sistem aktif - Streamlit headless modda çalışıyor")
st.success(f"Panel adresi: http://localhost:8501")
st.info(f"Başlangıç zamanı: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")