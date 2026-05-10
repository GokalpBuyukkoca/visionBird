# Resmi Python işletim sistemini indiriyoruz
FROM python:3.11-slim

# Çalışma masamızı kuruyoruz
WORKDIR /app
ARG GEMINI_API_ANAHARTARI2
ENV GEMINI_API_ANAHARTARI2=$GEMINI_API_ANAHARTARI2

# Alışveriş listemizi verip kütüphaneleri yüklüyoruz
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# İŞTE SİHİR BURADA! En yetkili kişi olarak (Root) Chrome'u ve eksik tüm dosyaları zorla kuruyoruz
RUN playwright install chromium
RUN playwright install-deps

# Kodlarımızın tamamını kopyalıyoruz
COPY . .

# Bulutun bize verdiği Port ile motoru ateşliyoruz
CMD uvicorn api:app --host 0.0.0.0 --port ${PORT:-8000}