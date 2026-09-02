# Sosyal İmece - Bulut Deployment Rehberi

Bu rehber, Sosyal İmece projesini Ubuntu tabanlı bir VPS sunucusunda 7/24 kesintisiz çalışacak şekilde部署 etmeniz için adım adım talimatlar içerir.

## Ön Hazırlık

### 1. Sunucu Gereksinimleri
- Ubuntu 20.04 veya üzeri
- En az 2GB RAM
- 20GB disk alanı
- Python 3.8+ (veya sistemde yoksa yükleyeceğiz)

### 2. Proje Dosyalarını Sunucuya Yükleme

```bash
# Yerel makineden sunucuya dosya transferi (SCP kullanarak)
scp -r "SOSYAL _İMECE/" ubuntu@your-server-ip:/home/ubuntu/sosyal-imece

# Alternatif: Git kullanarak
git clone <repository-url> /home/ubuntu/sosyal-imece
cd /home/ubuntu/sosyal-imece
```

## Kurulum Adımları

### 1. Sistem Güncellemesi

```bash
sudo apt update && sudo apt upgrade -y
```

### 2. Python ve Gerekli Paketlerin Kurulumu

```bash
# Python 3 ve pip kurulumu
sudo apt install python3 python3-pip python3-venv -y

# Proje dizinine git
cd /home/ubuntu/sosyal-imece

# Sanal ortam oluştur
python3 -m venv venv

# Sanal ortamı aktifleştir
source venv/bin/activate

# Bağımlılıkları yükle
pip install -r requirements.txt
```

### 3. Dizin İzinlerini Ayarla

```bash
# Veri dizini için yazma izni
sudo mkdir -p data
sudo chown -R ubuntu:ubuntu /home/ubuntu/sosyal-imece
chmod -R 755 /home/ubuntu/sosyal-imece
```

### 4. Systemd Servisi Kurulumu

```bash
# Servis dosyasını kopyala
sudo cp sosyal-imece.service /etc/systemd/system/

# Servisi yeniden yükle
sudo systemctl daemon-reload

# Servisi başlat
sudo systemctl start sosyal-imece

# Servisi otomatik başlatma ayarla
sudo systemctl enable sosyal-imece

# Servis durumunu kontrol et
sudo systemctl status sosyal-imece
```

## Servis Yönetimi

### Servis Durumunu Kontrol Etme

```bash
sudo systemctl status sosyal-imece
```

### Servisi Yeniden Başlatma

```bash
sudo systemctl restart sosyal-imece
```

### Servisi Durdurma

```bash
sudo systemctl stop sosyal-imece
```

### Logları Görüntüleme

```bash
# Son 50 satır log
sudo journalctl -u sosyal-imece -n 50

# Canlı log izleme
sudo journalctl -u sosyal-imece -f
```

## Firewall Ayarları

```bash
# UFW firewall aktifleştir (eğer kurulu değilse)
sudo apt install ufw -y

# HTTP ve HTTPS portlarına izin ver
sudo ufw allow 5000/tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp

# Firewall'ı aktifleştir
sudo ufw enable

# Durumu kontrol et
sudo ufw status
```

## Nginx Reverse Proxy (Opsiyonel ama Önerilir)

### Nginx Kurulumu

```bash
sudo apt install nginx -y
```

### Nginx Konfigürasyonu

```bash
sudo nano /etc/nginx/sites-available/sosyal-imece
```

Aşağıdaki konfigürasyonu yapıştırın:

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_read_timeout 86400;
    }
}
```

### Site'ı Aktifleştir

```bash
sudo ln -s /etc/nginx/sites-available/sosyal-imece /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

## SSL Sertifikası (Let's Encrypt)

```bash
# Certbot kurulumu
sudo apt install certbot python3-certbot-nginx -y

# SSL sertifikası al
sudo certbot --nginx -d your-domain.com
```

## Güvenlik İpuçları

1. **SSH Anahtar Tabanlı Kimlik Doğrulama**: Parola kimlik doğrulamasını devre dışı bırakın
2. **Fail2Ban Kurulumu**: Brute force saldırılarına karşı koruma
3. **Düzenli Yedekleme**: `data/` dizinini düzenli olarak yedekleyin
4. **Güncellemeler**: Sistemi ve paketleri düzenli güncelleyin

## Sorun Giderme

### Servis Başlamıyor

```bash
# Detaylı logları kontrol et
sudo journalctl -u sosyal-imece -n 100 --no-pager

# Manuel çalıştırma (hata ayıklama için)
cd /home/ubuntu/sosyal-imece
source venv/bin/activate
python orchestrator_api.py
```

### Port Zaten Kullanımda

```bash
# Hangi işlem 5000 portunu kullanıyor kontrol et
sudo lsof -i :5000

# İşlemi sonlandır
sudo kill -9 <PID>
```

### Veritabanı İzin Hataları

```bash
sudo chown -R ubuntu:ubuntu /home/ubuntu/sosyal-imece/data
chmod -R 755 /home/ubuntu/sosyal-imece/data
```

## API Test

Servis çalıştıktan sonra API'yi test edin:

```bash
# Durum kontrolü
curl http://localhost:5000/api/status

# Sağlık kontrolü
curl http://localhost:5000/api/health

# İstihbarat kaydı testi
curl -X POST http://localhost:5000/api/intelligence/record \
  -H "Content-Type: application/json" \
  -d '{"competitor_name":"Test","promotional_strategy":"Test","customer_reaction":"Test","success_score":0.5,"our_action_plan":"Test"}'
```

## Özet

Sosyal İmece sistemi artık 7/24 kesintisiz çalışmaya hazır. Systemd servisi sayesinde:
- Sunucu yeniden başlatıldığında otomatik başlar
- Çökerse otomatik olarak yeniden başlar
- Logları sistem loglarında tutulur
- Kolayca yönetilebilir

**İletişim**: Herhangi bir sorun yaşarsanız logları kontrol edin ve yukarıdaki sorun giderme adımlarını izleyin.
