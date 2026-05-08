# 🦅 visionBird: Otonom UI/UX Kalite Güvence (QA) Asistanı

visionBird, modern web uygulamalarının arayüz (UI) ve kullanıcı deneyimi (UX) testlerini otomatize etmek için geliştirilmiş yapay zeka destekli bir QA (Kalite Güvence) botudur. 

Geleneksel testlerin aksine sadece kodları değil, sayfanın **görsel bütünlüğünü** de tıpkı bir insan gözüyle analiz eder, hataları kanıtlar ve detaylı raporlar sunar.

## 🚀 Öne Çıkan Özellikler

* **🤖 Otonom Test Süreci (CI/CD):** GitHub Actions entegrasyonu sayesinde kod her güncellendiğinde testler bulut sunucularında otomatik olarak tetiklenir.
* **💥 Görsel Hata Simülasyonu:** Canlı ortamlarda karşılaşılabilecek potansiyel UI çökmelerini (üst üste binen elementler, bozulan CSS'ler) sayfaya dinamik stil enjekte ederek test eder.
* **📸 Kuş Bakışı Kanıt Toplama:** Playwright motorunu kullanarak sayfanın boydan boya (full-page) ekran görüntüsünü alır ve bunu bir `.png` artefaktı (kanıtı) olarak buluta kaydeder.
* **🧠 Yapay Zeka ile Piksel Analizi:** Toplanan görsel kanıtlar Google Gemini 2.0 Flash Vision modeline gönderilir. Yapay zeka, metin okunabilirliği, element yerleşimi ve marka bütünlüğü gibi konularda acımasız ve detaylı bir analiz raporu yazar.
* **🛡️ Güvenlik Kalkanı (Mocking):** Beklenmedik API kesintilerinde veya kota aşımlarında (Rate Limit) sistem çökmez; otomatik olarak "Yedek Simülasyon" moduna geçerek test sürecini başarıyla tamamlar (Fail-safe mekanizması).

## 🛠️ Kullanılan Teknolojiler

* **Dil:** Python 3.x
* **Tarayıcı Otomasyonu:** Playwright (Chromium - Headless)
* **Yapay Zeka:** Google GenAI (Gemini 2.0 Flash)
* **Görüntü İşleme:** PIL (Pillow)
* **Bulut / CI-CD:** GitHub Actions & Artifacts

## ⚙️ Nasıl Çalışır?

1. **Uçuş (Tetiklenme):** GitHub sunucusu Ubuntu tabanlı bir sanal makine ayağa kaldırır.
2. **Sızma & Simülasyon:** Hedeflenen URL'ye (Örn: Iceberg Digital) girilir, güvenlik duvarları geçilir (bypass_csp) ve sayfaya hatalı CSS kodları enjekte edilir.
3. **Kanıt Kaydı:** Bozulmuş arayüzün yüksek çözünürlüklü ekran görüntüsü `visionbird_rapor.png` adıyla kaydedilir.
4. **Analiz:** Yapay zeka veya yedek mock sistemi bu kanıtı inceleyip detaylı bir **Hata Analiz Raporu** oluşturur.
5. **Raporlama:** Tüm analiz loglara yazdırılır ve fotoğraf dosyası Actions sekmesinde indirilebilir bir paket (Artifact) olarak sunulur.

## 💡 Kullanım Senaryosu
Bu araç, bir Frontend geliştiricisinin yaptığı ufak bir kod değişikliğinin sayfanın başka bir yerindeki tasarımı (marka renkleri, buton pozisyonları, okunabilirlik vb.) bozup bozmadığını **yayına almadan önce** otonom olarak denetlemek için tasarlanmıştır.

---
*Geliştirici:* Gökalp Büyükkoca
