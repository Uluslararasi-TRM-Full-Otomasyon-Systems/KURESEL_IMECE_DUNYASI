# Sosyal İmece - Windows Deployment Rehberi

Bu rehber, Sosyal İmece projesini Windows işletim sisteminde arka planda 7/24 kesintisiz çalışacak şekilde yapılandırmanız için adım adım talimatlar içerir.

## Ön Hazırlık

### 1. Sistem Gereksinimleri
- Windows 10 veya üzeri
- Python 3.8+ 
- En az 2GB RAM
- 20GB disk alanı

### 2. Python Kurulumu (Henüz Yüklü Değilse)

1. [Python.org](https://www.python.org/downloads/) adresinden Python 3.8+ indirin
2. Kurulum sırasında "Add Python to PATH" seçeneğini işaretleyin
3. Kurulumu tamamlayın

## Kurulum Adımları

### 1. Proje Dosyalarını Hazırlama

Proje dosyalarının doğru dizinde olduğundan emin olun:
```
C:\Users\Habitat\Desktop\SOSYAL _İMECE\
```

### 2. Sanal Ortam Oluşturma (Önerilir)

```cmd
cd "C:\Users\Habitat\Desktop\SOSYAL _İMECE"
python -m venv venv
venv\Scripts\activate
```

### 3. Bağımlılıkları Yükleme

```cmd
pip install -r requirements.txt
```

## Arka Planda Çalıştırma Yöntemleri

### Yöntem 1: VBScript ile Tam Arka Plan (Önerilen)

**start_background.vbs** dosyasını kullanarak hiçbir pencere açmadan çalıştırın:

```cmd
wscript start_background.vbs
```

Bu yöntem:
- Hiçbir komut penceresi açmaz
- Sistem tepsisinde görünmez
- Logları `orchestrator_service.log` dosyasına yazar
- En temiz arka plan çalışması sağlar

### Yöntem 2: Batch Dosyası ile Arka Plan

**run_service.bat** dosyasını çalıştırın:

```cmd
run_service.bat
```

Bu yöntem:
- Kısa bir başlatma penceresi gösterir
- Otomatik olarak kapanır
- Logları `orchestrator_service.log` dosyasına yazar

## Bilgisayar Açılışında Otomatik Başlatma

### Yöntem 1: Başlangıç Klasörüne Kısayol Ekleme (En Kolay)

1. **Win + R** tuşlarına basın
2. `shell:startup` yazın ve Enter'a basın
3. Başlangıç klasörü açılacaktır
4. Proje dizinindeki `start_background.vbs` dosyasına sağ tıklayın
5. **Kopyala** seçeneğini seçin
6. Başlangıç klasörüne sağ tıklayın ve **Kısayol Yapıştır** seçeneğini seçin
7. Artık bilgisayar her açıldığında otomatik başlayacaktır

### Yöntem 2: Görev Zamanlayıcı ile Otomatik Başlatma (Daha Gelişmiş)

1. **Görev Zamanlayıcı**'yı açın (Start menüsünde arayın)
2. Sağ panelde **Görev Oluştur** seçeneğine tıklayın
3. **Genel** sekmesinde:
   - **Ad**: `Sosyal İmece API Service`
   - **Kullanıcı oturum açtığında çalıştır** seçeneğini işaretleyin
   - **En yüksek ayrıcalıklarla çalıştır** seçeneğini işaretleyin
4. **Tetikleyiciler** sekmesine gidin:
   - **Yeni** butonuna tıklayın
   - **Başlangıçta** seçeneğini seçin
   - **Tamam**'a tıklayın
5. **Eylemler** sekmesine gidin:
   - **Yeni** butonuna tıklayın
   - **Programı başlat** seçeneğini seçin
   - **Program/komut dosyası**: `wscript.exe`
   - **Bağımsız değişkenleri ekle**: `"C:\Users\Habitat\Desktop\SOSYAL _İMECE\start_background.vbs"`
   - **Başla**: `C:\Users\Habitat\Desktop\SOSYAL _İMECE\`
   - **Tamam**'a tıklayın
6. **Koşullar** sekmesine gidin:
   - **Bilgisayar AC gücüne bağlıyken görevi başlat** seçeneğini işaretleyin (isteğe bağlı)
7. **Tamam** butonuna tıklayarak görevi kaydedin

### Yöntem 3: Kayıt Defteri ile Otomatik Başlatma (Gelişmiş Kullanıcılar)

⚠️ **Dikkat**: Kayıt defteri düzenlemeleri önceden yedek almayı gerektirir.

1. **Win + R** tuşlarına basın
2. `regedit` yazın ve Enter'a basın
3. Aşağıdaki anahtara gidin:
   ```
   HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Run
   ```
4. Sağ panelde boş alana sağ tıklayın
5. **Yeni > Dize Değeri** seçeneğini seçin
6. Ad olarak `SosyalImeceAPI` yazın
7. Oluşturduğunuz değere çift tıklayın
8. **Değer verisi** olarak şunu yazın:
   ```
   wscript.exe "C:\Users\Habitat\Desktop\SOSYAL _İMECE\start_background.vbs"
   ```
9. **Tamam**'a tıklayın
10. Kayıt defteri düzenleyicisini kapatın

## Servis Yönetimi

### Servisin Çalışıp Çalışmadığını Kontrol Etme

API'nin çalışıp çalışmadığını test edin:

```cmd
curl http://localhost:5000/api/status
```

Veya tarayıcıda açın:
```
http://localhost:5000/api/status
```

### Servisi Durdurma

Çalışan Python işlemini durdurmak için:

```cmd
taskkill /f /im python.exe
```

Belirli bir işlemi durdurmak için:

```cmd
tasklist | findstr python
taskkill /f /pid <PID>
```

### Logları Görüntüleme

Log dosyasını açın:
```
orchestrator_service.log
```

Veya komut satırından:
```cmd
type orchestrator_service.log
```

## Güvenlik Duvarı Ayarları

API'ye ağ üzerinden erişim için:

1. **Windows Defender Güvenlik Duvarı**'nı açın
2. **Gelişmiş ayarlar** seçeneğine tıklayın
3. **Gelen Kurallar** > **Yeni Kural** seçeneğine tıklayın
4. **Bağlantı noktası** seçeneğini seçin
5. **TCP** > **Belirli yerel bağlantı noktaları**: `5000`
6. **İzin ver** seçeneğini seçin
7. **Etki alanı**, **Özel**, **Genel** seçeneklerini işaretleyin
8. Kurala `Sosyal İmece API` adını verin ve tamamlayın

## Sorun Giderme

### Python Bulunamadı Hatası

```cmd
# Python yüklü mü kontrol et
python --version

# Yüklü değilse Python.org'dan indirin ve PATH'e ekleyin
```

### Port Zaten Kullanımda Hatası

```cmd
# Hangi işlem 5000 portunu kullanıyor kontrol et
netstat -ano | findstr :5000

# İşlemi sonlandır
taskkill /f /pid <PID>
```

### Bağımlılık Yükleme Hatası

```cmd
# Sanal ortamı yeniden oluştur
rmdir /s /q venv
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### Otomatik Başlatma Çalışmıyor

1. Görev Zamanlayıcı'da görevin durumunu kontrol edin
2. Log dosyasını kontrol edin (`orchestrator_service.log`)
3. Dosya yollarının doğru olduğunu doğrulayın
4. Kullanıcı izinlerini kontrol edin

## Performans İpuçları

1. **Sanal Ortam Kullanın**: Daha iyi performans ve izolasyon için
2. **Log Döngüsü**: Log dosyası çok büyürse düzenli olarak temizleyin
3. **Kaynak Kullanımı**: Görev Yöneticisi'nden CPU/RAM kullanımını izleyin
4. **Güncellemeler**: Python ve bağımlılıkları düzenli güncelleyin

## Özet

Sosyal İmece sistemi artık Windows'ta 7/24 kesintisiz çalışmaya hazır:

- **start_background.vbs**: Tam arka plan çalışması (önerilen)
- **run_service.bat**: Alternatif başlatma yöntemi
- **Otomatik başlatma**: Başlangıç klasörü, Görev Zamanlayıcı veya Kayıt Defteri ile

**İletişim**: Herhangi bir sorun yaşarsanız logları kontrol edin ve yukarıdaki sorun giderme adımlarını izleyin.
