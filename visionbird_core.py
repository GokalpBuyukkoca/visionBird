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
        page.screenshot(path="visionbird_rapor.png", full_page=True)
        browser.close()

    import PIL.Image
    img = PIL.Image.open("visionbird_rapor.png")
    
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
    
    # Gerçek API'ye bağlanmayı deniyoruz
    try:
        response = client.models.generate_content(
            model='gemini-2.0-flash',
            contents=[prompt, img]
        )
        print("-" * 40)
        print("📋 visionBird HATA ANALİZ RAPORU:")
        print(response.text)
        print("-" * 40)
        
    # Eğer Google API kotası (limit 0) veya başka bir hata verirse sistemi çökertme, Mock (Yedek) raporu bas!
    except Exception as e:
        print(f"⚠️ API Bağlantısı Reddedildi (Hata: {e})")
        print("🔄 visionBird 'Mocking' (Yedek Simülasyon) moduna geçiyor...\n")
        
        print("-" * 40)
        print("📋 visionBird HATA ANALİZ RAPORU (OTOMATİK YEDEK):")
        print("1. Metin Okunabilirliği: KRİTİK HATA! H1 başlığı devasa boyutlara ulaşmış (150px) ve sayfa yapısını bozuyor.")
        print("2. Element Yerleşimi: KRİTİK HATA! 'Valuation' butonu kırmızı renge dönmüş, yan yatmış ve başlığın tam üzerine binerek (overlapping) tıklanmasını engelliyor.")
        print("3. Genel Görsel Kalite: Arayüz tamamen kullanılamaz durumda. CSS düzenlemesi acilen geri alınmalı.")
        print("-" * 40)
        
    print(f"💡 İncelemek istersen çektiğimiz bozuk fotoğraf bulut sunucusunda kaydedildi.")
