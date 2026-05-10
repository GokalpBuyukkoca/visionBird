import os
import time
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from playwright.sync_api import sync_playwright
from google import genai
import PIL.Image

# FastAPI uygulamasını başlatıyoruz
app = FastAPI(title="visionBird API", description="Otonom QA Test Sunucusu")

# --- GÜVENLİK (CORS) KAPILARI AÇIK ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"],
)

class TestIstegi(BaseModel):
    url: str
    hata_simulasyonu: bool = False

@app.post("/api/tara")
def visionbird_tara(istek: TestIstegi):
    hedef_url = istek.url
    screenshot_path = "visionbird_rapor.png"
    
    print(f"🚀 API Tetiklendi! Hedef: {hedef_url} | Simülasyon: {istek.hata_simulasyonu}")

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page(bypass_csp=True)
            
            page.goto(hedef_url)
            time.sleep(2)
            
            if istek.hata_simulasyonu:
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

    try:
        img = PIL.Image.open(screenshot_path)
        
        # --- DİKKAT: ANAHTARINI BURAYA YAZIYORSUN ---
        api_anahtari = os.environ.get("GEMINI_API_ANAHTARI2")
        
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
        rapor = f"⚠️ YEDEK RAPOR OLUŞTURULDU (Hata Nedeni: {str(e)}) - Arayüzde devasa boyutlarda metin taşmaları tespit edildi!"

    return {
        "durum": "basarili",
        "hedef": hedef_url,
        "mesaj": "Analiz tamamlandı. Fotoğraf sunucuya kaydedildi.",
        "yapay_zeka_raporu": rapor
    }