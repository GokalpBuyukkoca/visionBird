import os
import base64
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from playwright.async_api import async_playwright
from openai import OpenAI

app = FastAPI()

# CORS İzinleri (Vercel bağlantısının hatasız çalışması için kesinlikle şart)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class UrlRequest(BaseModel):
    url: str

# ... önceki kodlar (importlar, app tanımı vs.) aynı ...

@app.post("/api/tara")
async def tara(request: UrlRequest):
    try:
        # 1. Aşama: Playwright ile ekran görüntüsü alma
        async with async_playwright() as p:
            # 🚨 İŞTE KRİTİK DEĞİŞİKLİK BURADA: 
            # executable_path ile tarayıcının tam konumunu gösteriyoruz.
            # Dockerfile'da PLAYWRIGHT_BROWSERS_PATH=/app/pw-browsers tanımladığımız için
            # chromium tarayıcısı büyük ihtimalle aşağıdaki yolda olacak.
            
            browser = await p.chromium.launch(
                headless=True, 
                args=["--no-sandbox", "--disable-setuid-sandbox", "--disable-dev-shm-usage"],
                # executable_path parametresini ekliyoruz. 
                # Not: Bu yol Render'daki Debian tabanlı imaj için genellikle doğrudur.
                executable_path="/usr/bin/google-chrome-stable" # VEYA "/usr/bin/chromium" olabilir.
            )
            
            page = await browser.new_page()
            await page.set_viewport_size({"width": 1280, "height": 800})
            
            await page.goto(request.url, wait_until="domcontentloaded", timeout=30000)
            
            screenshot_bytes = await page.screenshot(type="jpeg", quality=80)
            await browser.close()
            
            base64_image = base64.b64encode(screenshot_bytes).decode('utf-8')

        # ... 2. Aşama (OpenAI Bağlantısı) aynı şekilde devam ediyor ...

        # 2. Aşama: OpenAI Bağlantısı
        api_key = os.environ.get("OPENAI_API_KEY")
        if not api_key:
            return {"durum": "HATA", "analiz": "Sunucu hatası: OpenAI API anahtarı Render üzerinde bulunamadı."}

        client = OpenAI(api_key=api_key)
        
        # gpt-4o-mini modeline fotoğrafı ve talimatı gönderiyoruz
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text", 
                            "text": "Sen uzman bir UI/UX tasarımcısısın. Sana gönderilen bu web sitesi ekran görüntüsünü dikkatlice incele. Varsa arayüz hatalarını, metin taşmalarını, hizalama kusurlarını tespit et ve kullanıcıya Türkçe, profesyonel, maddeler halinde bir iyileştirme raporu sun."
                        },
                        {
                            "type": "image_url",
                            "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}
                        }
                    ]
                }
            ],
            max_tokens=600
        )
        
        return {"durum": "BAŞARILI", "analiz": response.choices[0].message.content}

    except Exception as e:
        # Olası bir hatada sistemin çökmesini önleyip arayüze hata detayını gönderiyoruz
        return {"durum": "HATA", "analiz": f"Analiz sırasında bir hata oluştu: {str(e)}"}