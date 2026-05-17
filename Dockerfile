FROM python:3.11-slim

WORKDIR /app

# İşletim sistemine doğrudan Chromium kuruyoruz
RUN apt-get update && apt-get install -y \
    chromium \
    chromium-driver \
    && rm -rf /var/lib/apt/lists/*

# ... Geri kalan Dockerfile kodun AYNEN devam ediyor ...

# Gereksinimleri kopyalayıp kuruyoruz
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 🚨 İŞTE EN KRİTİK ADIM: 
# Playwright'a tarayıcıları geçici klasörlere değil, projenin tam içine kurmasını söylüyoruz.
# Böylece Render sistemi ayağa kaldırdığında tarayıcıyı asla kaybetmeyecek.
ENV PLAYWRIGHT_BROWSERS_PATH=/app/pw-browsers

# Şimdi kurduruyoruz
RUN playwright install chromium
RUN playwright install-deps

COPY . .

ENV PORT=8000
ENV OPENAI_API_KEY=$OPENAI_API_KEY
# Koddaki Playwright'ın da bu yolu okuması için Docker seviyesinde sabitliyoruz
ENV PLAYWRIGHT_BROWSERS_PATH=/app/pw-browsers

CMD uvicorn api:app --host 0.0.0.0 --port $PORT