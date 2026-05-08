import os
from playwright.sync_api import sync_playwright
from google import genai
import time

# API anahtarını koddan değil, GitHub'ın güvenli kasasından çekiyoruz
api_anahtari = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_anahtari)

# ... (Kodun geri kalanı aynı kalıyor)

def visionbird_scan_and_simulate(test_url):
    print(f"🦅 visionBird havalandı. Hedef taranıyor: {test_url}")
    # Gerçek fotoğraftan ayırt etmek için ismini değiştirelim
    screenshot_path = "visionbird_HATA_SIMULASYONU.png" 

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True) 
        # Güvenlik kalkanını (CSP) aşmak için özel yetki veriyoruz:
        page = browser.new_page(bypass_csp=True)
        
        
        # Sitenin orijinaline gidiyoruz
        page.goto(test_url)
        # Sayfanın yüklenmesi için bekleyelim
        page.wait_for_selector("h1") 
        time.sleep(2) 

        print("\n💥 [SİMÜLASYON] visionBird arayüze sızıyor ve hata simüle ediyor...")
        
        # --- BURASI KRİTİK: CANLI SAYFAYA HATA ENJEKTE EDİYORUZ ---
        # Sadece bu tarayıcı oturumunda geçerli olacak CSS müdahalesi:
        # H1 başlığını devasa yap ve butonu kırmızı yapıp üzerine bindir.
        css_sabotaji = """
            h1 {
                font-size: 150px !important;
                line-height: 0.5 !important;
                color: magenta !important;
                position: relative !important;
                z-index: 1 !important;
            }
            .valpal-valuation-button { 
                background-color: red !important;
                position: absolute !important;
                top: 50px !important;
                left: 0 !important;
                transform: rotate(-20deg) !important;
                z-index: 9999 !important;
                border: 10px solid yellow !important;
            }
        """
        page.add_style_tag(content=css_sabotaji)
        # Değişikliklerin uygulanması için yarım saniye bekle
        time.sleep(0.5) 
        # -----------------------------------------------------------

        print("📸 visionBird 'bozuk' arayüzün kuş bakışı görüntüsünü alıyor...")
        page.screenshot(path=screenshot_path, full_page=True)
        browser.close()

    import PIL.Image
    img = PIL.Image.open(screenshot_path)
    
    # Yapay zekaya verdiğimiz komutu biraz daha detaylandıralım
    prompt = """
    Sen visionBird adında, Frontend UI/UX testlerinde uzmanlaşmış keskin gözlü bir yapay zeka QA mühendisisin. 
    Sana bir web sitesinin ekran görüntüsünü veriyorum. Lütfen bu görüntüyü piksel piksel incele ve bir insan tester gibi şu görsel hataları (Visual Bugs) raporla:
    
    1. Metinlerin okunabilirliği: Üst üste binen (overlapping), ekranın dışına taşan veya çok absürt boyutta metinler var mı?
    2. Element yerleşimi: Butonlar veya diğer UI öğeleri marka bütünlüğünü bozacak şekilde yanlış yerde mi?
    3. Genel görsel kalite: Kullanıcıyı rahatsız edecek, bozuk görünen herhangi bir tasarım hatası görüyor musun?
    
    Raporunu net ve maddeler halinde yaz. Eğer her şey kusursuz görünüyorsa 'Görsel bir hata tespit edilmedi, arayüz temiz.' de.
    """
    
    print("🧠 visionBird bozuk arayüzü analiz ediyor... (Bu biraz sürebilir)\n")
    
    # Analizi gönderiyoruz
    response = client.models.generate_content(
        model='gemini-1.5-pro', # Görsel QA (Kalite Güvence) için en güçlü model
        contents=[prompt, img]
    )
    
    
    print("-" * 40)
    print("📋 visionBird HATA ANALİZ RAPORU:")
    print(response.text)
    print("-" * 40)
    print(f"💡 İncelemek istersen çektiğimiz bozuk fotoğraf burada: {screenshot_path}")

if __name__ == "__main__":
    visionbird_scan_and_simulate("https://www.iceberg-digital.co.uk/")