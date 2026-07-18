# TRM Nirvana v3.0 + PAZARLAMA - Cloud Ready Docker Image
FROM python:3.11-slim

# Sistem ayarları
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Çalışma dizini
WORKDIR /app

# Sistem paketleri
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Python bağımlılıkları
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Tüm dosyaları kopyala
COPY . .

# Gerekli dizinleri oluştur
RUN mkdir -p logs data temp_photos temp_docs

# Port'u aç
EXPOSE 9000

# Başlangıç script'i
COPY docker_entrypoint.sh /docker_entrypoint.sh
RUN chmod +x /docker_entrypoint.sh

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:9000 || exit 1

# Komut
ENTRYPOINT ["/docker_entrypoint.sh"]
CMD ["python", "main_orchestrator.py"]
