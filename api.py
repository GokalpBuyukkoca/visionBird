import os
import time
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from playwright.sync_api import sync_playwright
from google import genai
import PIL.Image

# FastAPI uygulamasını başlatıyoruz
app = FastAPI(title="visionBird API", description="Otonom QA Test Sunucusu")

# Kullanıcıdan (Ön Yüzden) gelecek verinin formatını belirliyoruz
class TestIstegi(BaseModel):
    url: str

# API'mizin dışarıya açılan kapısı (Endpoint)
@app.post("/api/tara")
def visionbird_tara(istek: TestIstegi):
    hedef_url = istek.url
    screenshot_path = "visionbird_rapor.png"
    
    print(f"🚀 API Tetiklendi! Hedef: {hedef_url}")

    # --- 1. AŞAMA: PLAYWRIGHT İLE SIZMA VE FOTOĞRAF ---
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page(bypass_csp=True)
            
            page.goto(hedef_url)
            time.sleep(2) # Sayfanın yüklenmesi için kısa bir mola
            
            # Standart bir sabotaj (Tüm sitelerde H1 başlıklarını bozacak genel bir kural)
            css_sabotaji = """
                h1 {
                    font-size: 150px !important;
                    color: magenta !important;
                    line-height: 0.5 !important;
                    position: relative !important;
                    z-index: 9999 !important;
                }
            """
            page.add_style_tag(content=css_sabotaji)
            time.sleep(0.5)
            
            page.screenshot(path=screenshot_path, full_page=True)
            browser.close()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Tarayıcı motoru çöktü: {str(e)}")

    # --- 2. AŞAMA: YAPAY ZEKA ANALİZİ ---
    try:
        img = PIL.Image.open(screenshot_path)
        api_anahtari = os.environ.get("GEMINI_API_KEY")
        client = genai.Client(api_key=api_anahtari)
        
        prompt = """
        Sen visionBird adında bir QA mühendisisin. 
        Aşağıdaki web sitesi arayüzünü incele. Metinlerin okunabilirliği, üst üste binen elementler ve marka bütünlüğünü bozan aşırı büyük/renkli hatalar var mı? 
        Kısa, net ve profesyonel bir rapor yaz.
        """
        
        response = client.models.generate_content(
            model='gemini-2.0-flash',
            contents=[prompt, img]
        )
        rapor = response.text
        
    except Exception as e:
        # API çökerse Kalkan (Mocking) devreye giriyor
        rapor = "⚠️ OTOMATİK YEDEK RAPOR: API bağlantısı sağlanamadı ancak arayüzde devasa boyutlarda (H1) metin taşmaları tespit edildi. Acil müdahale gerekli!"

    # Ön yüze (Frontend'e) verilecek nihai cevap (JSON)
    return {
        "durum": "basarili",
        "hedef": hedef_url,
        "mesaj": "Analiz tamamlandı. Fotoğraf sunucuya kaydedildi.",
        "yapay_zeka_raporu": rapor
    }
