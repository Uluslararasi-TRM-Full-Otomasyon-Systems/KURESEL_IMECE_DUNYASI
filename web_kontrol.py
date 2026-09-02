from flask import Flask, render_template_string
import os
import subprocess

app = Flask(__name__)

# Ajanların yolu
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

HTML_PANEL = """
<!DOCTYPE html>
<html>
<head><title>TRM Kontrol Paneli</title></head>
<body>
    <h1>TRM Otonom Kontrol</h1>
    <a href="/run/dagitici"><button>DAGITICI AJAN</button></a>
    <a href="/run/analiz"><button>ANALIZ AJANI</button></a>
    <a href="/run/gozlemci"><button>GOZLEMCU AJAN</button></a>
    <hr>
    <h2>Son Loglar</h2>
    <pre>{{ logs }}</pre>
</body>
</html>
"""

def get_logs():
    log_path = os.path.join(BASE_DIR, 'logs', 'trm_sistem.log')
    if os.path.exists(log_path):
        with open(log_path, 'r', encoding='utf-8') as f:
            return "".join(f.readlines()[-20:])
    return "Log bulunamadı."

@app.route('/')
def index():
    return render_template_string(HTML_PANEL, logs=get_logs())

@app.route('/run/<agent_type>')
def run_agent(agent_type):
    scripts = {
        'dagitici': 'dagitici_ajan.py',
        'analiz': 'analiz_ajani.py',
        'gozlemci': 'gozlemci_ajan.py'
    }
    if agent_type in scripts:
        subprocess.Popen(['python', os.path.join(BASE_DIR, scripts[agent_type])])
        return f"<h1>{agent_type} tetiklendi!</h1><a href='/'>Geri Dön</a>"
    return "Hata!"

if __name__ == '__main__':
    # Yerel IP'den erişim için 0.0.0.0
    app.run(host='0.0.0.0', port=5000)