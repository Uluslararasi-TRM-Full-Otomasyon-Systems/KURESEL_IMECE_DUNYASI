#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ULUSLARARASI TRM FULL OTOMASYON v3.0
Küresel İmece Dünyası - Halk İçin Ön Yüz Sunucusu
"""

from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
import json
import os
import socket
from datetime import datetime
from trm_agents.trm_gatekeeper_agent import TRMGatekeeperAgent

PUBLIC_DOMAIN = os.getenv("TRM_PUBLIC_DOMAIN", "kureselimecedunyasi.org.tr")
PUBLIC_SCHEME = os.getenv("TRM_PUBLIC_SCHEME", "https")
PUBLIC_HOST = os.getenv("TRM_PUBLIC_HOST", "0.0.0.0")
PUBLIC_PORT = int(os.getenv("PORT", os.getenv("TRM_PUBLIC_PORT", "8080")))
MAX_REQUEST_SIZE = int(os.getenv("TRM_MAX_REQUEST_SIZE", "1048576"))

# Initialize the gatekeeper agent
gatekeeper = TRMGatekeeperAgent()


def get_local_network_ip():
    """Yerel agda diger cihazlarin kullanabilecegi IPv4 adresini bul."""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.connect(("8.8.8.8", 80))
        local_ip = sock.getsockname()[0]
        sock.close()
        return local_ip
    except OSError:
        try:
            return socket.gethostbyname(socket.gethostname())
        except OSError:
            return None


class ProductionHTTPServer(ThreadingHTTPServer):
    daemon_threads = True
    allow_reuse_address = True


def get_public_base_url():
    if PUBLIC_DOMAIN:
        return f"{PUBLIC_SCHEME}://{PUBLIC_DOMAIN}"
    return f"http://localhost:{PUBLIC_PORT}"

class PublicWebsiteHandler(SimpleHTTPRequestHandler):
    server_version = "TRMPublicWebsite/1.0"

    def _set_common_headers(self):
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("X-Frame-Options", "SAMEORIGIN")
        self.send_header("Referrer-Policy", "strict-origin-when-cross-origin")
        self.send_header("Cache-Control", "no-store")

    def _send_html(self, status_code, html_content):
        self.send_response(status_code)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self._set_common_headers()
        self.end_headers()
        self.wfile.write(html_content.encode("utf-8"))

    def _send_json(self, status_code, payload):
        self.send_response(status_code)
        self.send_header("Content-type", "application/json; charset=utf-8")
        self._set_common_headers()
        self.end_headers()
        self.wfile.write(json.dumps(payload, ensure_ascii=False).encode("utf-8"))

    def _read_json_body(self):
        content_length = int(self.headers.get("Content-Length", "0"))
        if content_length <= 0:
            raise ValueError("Bos istek govdesi gonderildi.")
        if content_length > MAX_REQUEST_SIZE:
            raise ValueError("Istek boyutu izin verilen siniri asti.")
        post_data = self.rfile.read(content_length)
        return json.loads(post_data.decode("utf-8"))

    def do_GET(self):
        if self.path == "/" or self.path == "/index.html":
            self._send_html(200, self.get_homepage_content())
        elif self.path == "/healthz":
            self._send_json(
                200,
                {
                    "status": "ok",
                    "service": "public-website",
                    "domain": PUBLIC_DOMAIN,
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                },
            )
        else:
            self._send_html(404, "Sayfa bulunamadi")
    
    def do_POST(self):
        try:
            data = self._read_json_body()
            
            if self.path == "/api/basvuru":
                application = {
                    "application_id": f"APP-{datetime.now().strftime('%Y%m%d%H%M%S')}",
                    "name": (data.get("ad", "") + " " + data.get("soyad", "")).strip(),
                    "email": data.get("eposta", ""),
                    "phone": data.get("telefon", ""),
                    "motivation": data.get("motivasyon", ""),
                    "document_note": data.get("belge_aciklamasi", ""),
                    "document_names": data.get("belge_dosyalari", []),
                    "experience": "Web sitesi başvurusu",
                    "submitted_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                }
                gatekeeper.manage_website_api([application])
                self._send_json(
                    200,
                    {
                        "status": "success",
                        "message": "Basvurunuz basariyla alindi. Tesekkur ederiz.",
                    },
                )

            elif self.path == "/api/yardim":
                help_request = {
                    "request_id": f"SUPPORT-{datetime.now().strftime('%Y%m%d%H%M%S')}",
                    "name": (data.get("ad", "") + " " + data.get("soyad", "")).strip(),
                    "email": data.get("eposta", ""),
                    "phone": data.get("telefon", ""),
                    "issue": "Form doldurma ve belge fotoğrafı yükleme yardımı istendi",
                    "requested_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "status": "BEKLEMEDE",
                }
                gatekeeper.trigger_applicant_contact([help_request])
                self._send_json(
                    200,
                    {
                        "status": "success",
                        "message": "Yardim talebiniz alindi. Telefon numaraniz kaydedildi, yetkililerimiz sizi arayip basvuru ve belge yukleme surecinde destek olacaktir.",
                    },
                )
            else:
                self._send_json(404, {"status": "error", "message": "API yolu bulunamadi."})
        except Exception as e:
            self._send_json(500, {"status": "error", "message": f"Bir hata olustu: {str(e)}"})
    
    def get_homepage_content(self):
        """Halk için ana sayfa içeriği - büyük fontlar, sade tasarım"""
        return """
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Küresel İmece Dünyası</title>
    <style>
        * {
            box-sizing: border-box;
        }
        body {
            font-family: "Arial", sans-serif;
            background-color: #f0f8ff;
            color: #222222;
            margin: 0;
            padding: 20px;
            line-height: 1.8;
        }
        .container {
            max-width: 800px;
            margin: 0 auto;
            background-color: white;
            padding: 40px;
            border-radius: 15px;
            box-shadow: 0 0 20px rgba(0,0,0,0.1);
        }
        h1 {
            font-size: 42px;
            color: #1e40af;
            text-align: center;
            margin-bottom: 30px;
        }
        h2 {
            font-size: 32px;
            color: #1e40af;
            margin-top: 40px;
            margin-bottom: 20px;
        }
        h3 {
            font-size: 26px;
            color: #1f2937;
            margin: 0 0 12px 0;
        }
        p, li, label {
            font-size: 22px;
        }
        ul {
            padding-left: 30px;
        }
        .intro-box {
            background-color: #dbeafe;
            padding: 30px;
            border-radius: 10px;
            margin-bottom: 30px;
        }
        .step {
            background-color: #f0fdf4;
            padding: 20px;
            margin: 15px 0;
            border-radius: 10px;
            border-left: 8px solid #22c55e;
        }
        .step-number {
            font-size: 28px;
            font-weight: bold;
            color: #22c55e;
            margin-right: 15px;
        }
        .step-content {
            display: inline;
        }
        .notice-box {
            background-color: #eff6ff;
            padding: 24px;
            border-radius: 12px;
            border: 2px solid #93c5fd;
            margin: 25px 0;
        }
        .support-box {
            background-color: #fef2f2;
            padding: 24px;
            border-radius: 12px;
            border: 2px solid #fca5a5;
            margin-top: 25px;
        }
        form {
            background-color: #fffbeb;
            padding: 40px;
            border-radius: 15px;
            margin-top: 30px;
        }
        label {
            display: block;
            margin-top: 25px;
            margin-bottom: 10px;
            font-weight: bold;
            color: #92400e;
        }
        input[type="text"],
        input[type="email"],
        input[type="tel"],
        input[type="file"],
        textarea {
            width: 100%;
            font-size: 22px;
            padding: 15px;
            border: 3px solid #d97706;
            border-radius: 8px;
            background-color: #ffffff;
        }
        textarea {
            min-height: 180px;
            resize: vertical;
        }
        .helper-text {
            font-size: 18px;
            color: #374151;
            margin-top: 8px;
        }
        .file-list {
            font-size: 18px;
            color: #1f2937;
            margin-top: 10px;
        }
        .submit-btn {
            background-color: #22c55e;
            color: white;
            font-size: 28px;
            font-weight: bold;
            padding: 20px 40px;
            border: none;
            border-radius: 12px;
            cursor: pointer;
            margin-top: 30px;
            width: 100%;
        }
        .submit-btn:hover {
            background-color: #16a34a;
        }
        .help-btn {
            background-color: #dc2626;
            color: white;
            font-size: 24px;
            font-weight: bold;
            padding: 18px 30px;
            border: none;
            border-radius: 12px;
            cursor: pointer;
            margin-top: 25px;
            width: 100%;
        }
        .help-btn:hover {
            background-color: #b91c1c;
        }
        .message {
            margin-top: 25px;
            padding: 20px;
            border-radius: 10px;
            font-size: 24px;
            text-align: center;
            font-weight: bold;
            display: none;
        }
        .message.success {
            background-color: #d1fae5;
            color: #065f46;
        }
        .message.error {
            background-color: #fee2e2;
            color: #991b1b;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Küresel İmece Dünyası</h1>
        
        <div class="intro-box">
            <h2>Hoş Geldiniz!</h2>
            <p>Burada amaç, uluslararası ortaklıklar ve yardımlaşma havuzu içinde vatandaşlarımız için düzenli dijital gelir kapısı oluşturmaktır.</p>
            <p>Süreç olabildiğince sade ilerler. Başvurunuzu yaparsınız, uygunluk görüşmesi tamamlanır, onaydan sonra hesap isimlerinizi verirsiniz. Geri kalan işleri sistem takip eder.</p>
        </div>
        
        <h2>Sistem Nasıl Çalışır?</h2>
        <p><strong>Sadece 3 Adımda Dijital Gelir Kapınız Hazır:</strong></p>
        
        <div class="step">
            <span class="step-number">1.</span>
            <span class="step-content"><strong>Ön Başvurunuzu Yapın ve Belgelerinizi Hazırlayın:</strong> Aşağıdaki basit formu doldurarak ilk adımınızı atın.</span>
            <p>Kayıt esnasında sistemimize; en az %40 engelli olunduğuna dair belgeyi (varsa vasi belgesiyle birlikte), eğer bir yerde çalışılıyorsa son geriye dönük 3 aylık maaş bordrosunu ve sistemin isteyeceği diğer gerekli evrakları telefonunuzla çekeceğiniz net birer fotoğraf olarak hazırlamanız gerekmektedir.</p>
        </div>
        
        <div class="step">
            <span class="step-number">2.</span>
            <span class="step-content"><strong>Güvenlik ve Uyumluluk Testini Geçin:</strong> Belgeleriniz geldikten sonra sizinle veya gerekiyorsa vasinizle kısa bir telefon görüşmesi yapılır.</span>
            <p>Amacımız sistemin dürüstlüğünü ve yardımlaşma ruhunu korumak, suistimalleri daha kapıda engellemek ve gerçekten ihtiyacı olan doğru kişilere ulaşmaktır.</p>
        </div>
        
        <div class="step">
            <span class="step-number">3.</span>
            <span class="step-content"><strong>Hesaplarınızı Açın ve Sadece Hesap İsimlerinizi Verin:</strong> Onaylandıktan sonra yapmanız gereken tek şey, çalışılacak sosyal medya hesaplarını açıp yalnızca hesap isimlerinizi bildirmektir.</span>
            <p>Şifre gibi gizli bilgileri paylaşmanız istenmez. Sonrasında ürün bulma, paylaşım yapma, video hazırlama veya reklamla uğraşma kısmı arka planda yürütülür. Oluşan havuz gelirinden payınıza düşen komisyon gelirleri muhasebe sistemi üzerinden banka hesabınıza aktarılır.</p>
        </div>

        <div class="support-box">
            <h3>Teknolojiden Anlamıyorsanız Sorun Değil</h3>
            <p>Formun altındaki <strong>"Yapamıyorum, Yardım Et!"</strong> butonuna basmanız yeterlidir. Sistem telefon numaranızı kaydeder ve yetkililerimiz sizi arayıp bu süreci sizin adınıza tamamlamak için destek olur.</p>
        </div>
        
        <h2>Ön Kayıt Başvuru Formu</h2>
        <div class="notice-box">
            <h3>Belge Fotoğrafı Hazırlama Bilgisi</h3>
            <p>Belgelerinizi telefonunuzla net şekilde fotoğraflayıp bu başvuru sırasında seçebilirsiniz. Fotoğraf yüklemekte zorlanırsanız yardım butonuna basın; sizi arayıp adım adım destek olalım.</p>
        </div>
        
        <form id="basvuruForm">
            <label for="ad">Adınız:</label>
            <input type="text" id="ad" name="ad" required>
            
            <label for="soyad">Soyadınız:</label>
            <input type="text" id="soyad" name="soyad" required>
            
            <label for="telefon">Telefon Numaranız:</label>
            <input type="tel" id="telefon" name="telefon" required>
            
            <label for="eposta">E-posta Adresiniz:</label>
            <input type="email" id="eposta" name="eposta" required>
            
            <label for="motivasyon">Neden bu yardımlaşma hareketine katılmak istiyorsunuz?</label>
            <textarea id="motivasyon" name="motivasyon" required placeholder="Lütfen düşüncelerinizi buraya yazın..."></textarea>

            <label for="belgeler">Belgelerinizin Fotoğrafları:</label>
            <input type="file" id="belgeler" name="belgeler" accept="image/*" multiple>
            <div class="helper-text">Telefonunuzla çektiğiniz belge fotoğraflarını buradan seçebilirsiniz. Örnek: engellilik belgesi, varsa vasi belgesi, 3 aylık maaş bordrosu ve diğer gerekli evraklar.</div>
            <div id="fileList" class="file-list"></div>
            
            <button type="submit" class="submit-btn">Başvurumu Gönder</button>
            
            <div id="message" class="message"></div>
        </form>
        
        <button type="button" id="yardimBtn" class="help-btn">Yapamıyorum, Yardım Et!</button>
    </div>

    <script>
        const form = document.getElementById('basvuruForm');
        const messageDiv = document.getElementById('message');
        const yardimBtn = document.getElementById('yardimBtn');
        const belgelerInput = document.getElementById('belgeler');
        const fileList = document.getElementById('fileList');

        belgelerInput.addEventListener('change', function() {
            const names = Array.from(belgelerInput.files).map(file => file.name);
            fileList.textContent = names.length
                ? 'Seçilen belge fotoğrafları: ' + names.join(', ')
                : '';
        });
        
        form.addEventListener('submit', async function(e) {
            e.preventDefault();

            const belgeDosyalari = Array.from(belgelerInput.files).map(file => file.name);
            
            const formData = {
                ad: document.getElementById('ad').value,
                soyad: document.getElementById('soyad').value,
                telefon: document.getElementById('telefon').value,
                eposta: document.getElementById('eposta').value,
                motivasyon: document.getElementById('motivasyon').value,
                belge_dosyalari: belgeDosyalari,
                belge_aciklamasi: belgeDosyalari.length
                    ? 'Vatandaş belge fotoğraflarını telefon üzerinden seçti.'
                    : 'Belge fotoğrafı seçilmedi.'
            };
            
            try {
                const response = await fetch('/api/basvuru', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(formData)
                });
                
                const result = await response.json();
                
                messageDiv.className = 'message success';
                messageDiv.textContent = result.message;
                messageDiv.style.display = 'block';
                
                form.reset();
                fileList.textContent = '';
                
            } catch (error) {
                messageDiv.className = 'message error';
                messageDiv.textContent = 'Bir hata oluştu, lütfen tekrar deneyin.';
                messageDiv.style.display = 'block';
            }
        });
        
        yardimBtn.addEventListener('click', async function() {
            const formData = {
                ad: document.getElementById('ad').value || 'Belirtilmedi',
                soyad: document.getElementById('soyad').value || 'Belirtilmedi',
                telefon: document.getElementById('telefon').value || 'Belirtilmedi',
                eposta: document.getElementById('eposta').value || 'Belirtilmedi'
            };
            
            try {
                const response = await fetch('/api/yardim', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(formData)
                });
                
                const result = await response.json();
                
                messageDiv.className = 'message success';
                messageDiv.textContent = result.message;
                messageDiv.style.display = 'block';
                
            } catch (error) {
                messageDiv.className = 'message error';
                messageDiv.textContent = 'Bir hata oluştu, lütfen tekrar deneyin.';
                messageDiv.style.display = 'block';
            }
        });
    </script>
</body>
</html>
        """
    
    def log_message(self, format, *args):
        # Basit loglama
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {format % args}")

def start_public_server():
    """Halk için web sunucusunu başlat"""
    local_ip = get_local_network_ip()
    public_url = get_public_base_url()
    server = ProductionHTTPServer((PUBLIC_HOST, PUBLIC_PORT), PublicWebsiteHandler)
    print("=" * 60)
    print("🌍 KÜRESEL İMECE DÜNYASI - HALK İÇİN WEB SİTESİ")
    print("=" * 60)
    print(f"+ Web sitesi aktif: http://localhost:{PUBLIC_PORT}")
    if PUBLIC_HOST == "0.0.0.0" and local_ip:
        print(f"+ Yerel ag adresi: http://{local_ip}:{PUBLIC_PORT}")
    else:
        print("+ Yerel ag IP adresi otomatik bulunamadi.")
    print(f"+ Canli alan adi: {public_url}")
    print(f"+ Health kontrolu: http://localhost:{PUBLIC_PORT}/healthz")
    print("+ API uç noktaları: /api/basvuru ve /api/yardim")
    print("\nDurdurmak için Ctrl+C")
    print("=" * 60)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nSunucu durduruldu.")
    finally:
        server.shutdown()
        server.server_close()

if __name__ == "__main__":
    start_public_server()
