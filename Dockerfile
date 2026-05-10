# Daha stabil bir temel imaj seçiyoruz
FROM python:3.11-slim

# Çalışma klasörü
WORKDIR /app

# Pip'i güncelliyoruz
RUN pip install --upgrade pip

# Gereksinimleri kopyalayıp kuruyoruz
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# --- İŞTE BURASI KRİTİK ---
# Önce Playwright'ı kuruyoruz
RUN playwright install chromium

# Sonra Playwright'ın kendi sistem komutuyla TÜM eksik kütüphaneleri 
# (libnss3, libgbm1 vb.) otomatik olarak sisteme kurduruyoruz.
# 'apt-get update' hatalarını bu komut kendi içinde çözer.
RUN playwright install-deps
# --------------------------

# Proje dosyalarını kopyalıyoruz
COPY . .

# Portu tanımlıyoruz
ENV PORT=8000

# API anahtarını Docker'a tanıtıyoruz (Render'daki isimle birebir aynı olmalı)
ENV GEMINI_API_ANAHARTARI2=$GEMINI_API_ANAHARTARI2

# Uygulamayı başlatıyoruz
CMD uvicorn api:app --host 0.0.0.0 --port $PORT