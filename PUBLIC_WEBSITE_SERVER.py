#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ULUSLARARASI TRM FULL OTOMASYON v3.0
Küresel İmece Dünyası - Halk İçin Ön Yüz Sunucusu
"""

from http.server import HTTPServer, SimpleHTTPRequestHandler
import json
import os
from datetime import datetime
from trm_agents.trm_gatekeeper_agent import TRMGatekeeperAgent

# Initialize the gatekeeper agent
gatekeeper = TRMGatekeeperAgent()

class PublicWebsiteHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/' or self.path == '/index.html':
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            html_content = self.get_homepage_content()
            self.wfile.write(html_content.encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write('Sayfa bulunamadı'.encode('utf-8'))
    
    def do_POST(self):
        # Read POST data
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        
        try:
            data = json.loads(post_data.decode('utf-8'))
            
            if self.path == '/api/basvuru':
                # Handle application submission
                application = {
                    "application_id": f"APP-{datetime.now().strftime('%Y%m%d%H%M%S')}",
                    "name": data.get('ad', '') + ' ' + data.get('soyad', ''),
                    "email": data.get('eposta', ''),
                    "phone": data.get('telefon', ''),
                    "motivation": data.get('motivasyon', ''),
                    "document_note": data.get('belge_aciklamasi', ''),
                    "document_names": data.get('belge_dosyalari', []),
                    "experience": "Web sitesi başvurusu",
                    "submitted_at": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                }
                gatekeeper.manage_website_api([application])
                
                self.send_response(200)
                self.send_header('Content-type', 'application/json; charset=utf-8')
                self.end_headers()
                response = {"status": "success", "message": "Başvurunuz başarıyla alındı! Teşekkür ederiz."}
                self.wfile.write(json.dumps(response, ensure_ascii=False).encode('utf-8'))
                
            elif self.path == '/api/yardim':
                # Handle help request
                help_request = {
                    "request_id": f"SUPPORT-{datetime.now().strftime('%Y%m%d%H%M%S')}",
                    "name": (data.get('ad', '') + ' ' + data.get('soyad', '')).strip(),
                    "email": data.get('eposta', ''),
                    "phone": data.get('telefon', ''),
                    "issue": "Form doldurma ve belge fotoğrafı yükleme yardımı istendi",
                    "requested_at": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    "status": "BEKLEMEDE"
                }
                gatekeeper.trigger_applicant_contact([help_request])
                
                self.send_response(200)
                self.send_header('Content-type', 'application/json; charset=utf-8')
                self.end_headers()
                response = {"status": "success", "message": "Yardım talebiniz alındı. Telefon numaranız kaydedildi, yetkililerimiz sizi arayıp başvuru ve belge yükleme sürecinde destek olacaktır."}
                self.wfile.write(json.dumps(response, ensure_ascii=False).encode('utf-8'))
                
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'application/json; charset=utf-8')
            self.end_headers()
            response = {"status": "error", "message": f"Bir hata oluştu: {str(e)}"}
            self.wfile.write(json.dumps(response, ensure_ascii=False).encode('utf-8'))
    
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
    port = 8080  # Herkese açık port
    server = HTTPServer(('0.0.0.0', port), PublicWebsiteHandler)
    print("=" * 60)
    print("🌍 KÜRESEL İMECE DÜNYASI - HALK İÇİN WEB SİTESİ")
    print("=" * 60)
    print(f"+ Web sitesi aktif: http://localhost:{port}")
    print(f"+ Herkese açık: http://0.0.0.0:{port}")
    print(f"+ API uç noktaları: /api/basvuru ve /api/yardim")
    print("\nDurdurmak için Ctrl+C")
    print("=" * 60)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nSunucu durduruldu.")
        server.shutdown()

if __name__ == "__main__":
    start_public_server()
