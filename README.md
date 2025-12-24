# Araç Plaka Tanımlama ve Ücretlendirme Sistemi

Bu proje, YOLO tabanlı plaka tespiti ve Tesseract OCR ile plaka okuma yapan modern bir **Tkinter GUI uygulamasıdır**. Python ile geliştirilmiş olup, araç plakalarını tespit eder, OCR ile okur ve süreye bağlı olarak ücretlendirme yapar. Uygulama Windows ortamına yönelik olarak hazırlanmıştır.

---

## Gereksinimler

* **İşletim Sistemi:** Windows 10/11 (64-bit)
* **Python:** 3.8 veya üstü
* **Gerekli Python Kütüphaneleri:**

  ```text
  ultralytics
  opencv-python
  numpy
  pillow
  pytesseract
  torch
  tkinter (Python ile birlikte gelir)
  ```

> Not: `torch` kurulumu sırasında CPU veya GPU (CUDA) uyumlu sürüm seçilmelidir.

---

## Zorunlu Dosya/Yol Bilgileri

1. **YOLO Modeli**

   * Uygulamanın çalışması için YOLO ile eğitilmiş plaka modeli (`.pt` uzantılı) gereklidir.
   * Dosya, uygulama içinde GUI üzerinden **Model Dosyası Seç** butonuyla yüklenmelidir.

2. **Tesseract OCR (Windows için zorunlu)**

   * [UB Mannheim Tesseract](https://github.com/UB-Mannheim/tesseract/wiki) sürümünü indirip kurun.
   * `tesseract.exe` dosyasını **`D:\Tesseract\tesseract.exe`** konumuna yerleştirin.
   * Kodda şu satır ile yol belirtilmiştir:

     ```python
     pytesseract.pytesseract.tesseract_cmd = r'D:\Tesseract\tesseract.exe'
     ```

---
## Kurulum ve Çalıştırma

1. Proje dosyalarını indirin veya klonlayın.
2. Sanal ortam oluşturun (opsiyonel):

   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```
3. Gerekli kütüphaneleri "pip install" kullanarak yükleyin
4. Tesseract OCR'yi indirin ve `D:\Tesseract\` içine kurun.
5. Uygulamayı çalıştırın:

   ```bash
   python main.py
   ```

---

## GUI Kullanımı

* **📁 Model Dosyası Seç:** YOLO modelini (`.pt`) yükler. (Hazır olarak "Model_Sonuçları/plaka_model/weights/best.pt" yolunda eğtilmiş bir model bulunmaktadır.)
* **📷 Fotoğraf Seç:** Plaka içeren bir fotoğraf açar.
* **🔍 Plaka Tespit Et:** Model ile plakayı bulur.
* **📝 OCR Çalıştır:** Tespit edilen plakayı metne çevirir.
* **💰 Süre Seçimi:** Park süresine göre fiyatlandırma yapılır.
* **💳 Tabloya Ekle:** Plaka ve ücret bilgisi tabloya eklenir.
* **🗑️ Temizle:** Tüm alanları sıfırlar.

---

## Hızlı Sorun Giderme

* **Model yüklenmiyor:** `.pt` dosyası uyumlu mu, doğru seçildi mi?
* **OCR çalışmıyor:** `D:\Tesseract\tesseract.exe` doğru mu? Yol ayarı kontrol edin.
* **Yanlış plaka metni çıkıyor:** `thresh` ile OCR deneyin veya görüntüyü daha net kırpın.

---

## Notlar

* Kod, koyu tema desteği ile modern bir GUI arayüzüne sahiptir.
* OCR için `tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789` kullanıldığından yalnızca rakam ve büyük harfler okunur.

---
## Arayüz 

<img width="1615" height="914" alt="Ekran görüntüsü 2025-09-21 180752" src="https://github.com/user-attachments/assets/2e215490-d252-4251-9e5d-dd32b123420c" />


