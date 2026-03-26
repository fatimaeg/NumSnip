# ✂️ NumSnip

**NumSnip** is a lightweight, open-source Python utility designed to instantly extract numbers (IDs, serial codes, or data points) from any application on your screen and copy them directly to your clipboard. 

By using a "Freeze & Snip" workflow, NumSnip allows you to bypass messy backgrounds, UI borders, and adjacent text, ensuring high-accuracy OCR every time.

---

## ✨ Features
* **Precision Sniping:** Freeze the screen and draw a box exactly around the digits you need.
* **High-Contrast Processing:** Automatically cleans and scales the image to improve OCR accuracy for screen photos or low-resolution PDFs.
* **Visual Confirmation:** Displays the captured number in a large, bold font for immediate verification.
* **Privacy-First:** Processes everything locally using Tesseract OCR. No data is sent to the cloud.

---

## 💻 Developer Setup

To run NumSnip from source, you need to have **Python 3.x** and the **Tesseract OCR engine** installed on your machine.

### 1. Install Tesseract OCR (Windows)
NumSnip requires the Tesseract binary to perform text recognition.
* Download the installer from the [UB-Mannheim Tesseract Repository](https://github.com/UB-Mannheim/tesseract/wiki).
* Install it to the default path: `C:\Program Files\Tesseract-OCR\`.
* *(Note: If you install it elsewhere, update the path at the top of `numsnip.py`.)*

### 2. Clone and Install Dependencies
Clone this repository and install the required Python libraries:

```bash
git clone [https://github.com/YOUR_USERNAME/NumSnip.git](https://github.com/YOUR_USERNAME/NumSnip.git)
cd NumSnip
pip install -r requirements.txt
```
### 3. Run the Application
```bash
python numsnip.py
```
---
## 📖 How to Use

1. Click the ✂ SNIP NUMBER button.
2. The screen will "freeze." Click and drag a tight box around the number you want to copy.
3. Release the mouse button.
4. The app will flash green and display the result. The number is now in your clipboard, ready to be pasted (Ctrl + V).

---
## 💡 Best Practices for 100% Accuracy
* **Tight Cropping:** Draw your box as close to the numbers as possible. Excluding nearby letters or table borders significantly improves accuracy.

* **Zoom In:** For very small fonts (like in some PDFs), zoom in on the document before snipping. Larger pixels lead to better recognition.

* **Standard Fonts:** Works best on clear, sans-serif fonts typically found in web portals and business documents.

---
## 🛠️ Built With

* **[PyTesseract](https://github.com/madmaze/pytesseract)** - Python wrapper for Tesseract OCR.

* **[Pillow (PIL)](https://www.google.com/search?q=https://python-pillow.org/)** - Image processing and enhancement.

* **[mss](https://www.google.com/search?q=https://github.com/boboTI/python-mss)** - Ultra-fast cross-platform screen shooting.

* **[pyperclip](https://github.com/asweigart/pyperclip)** - Cross-platform clipboard management.
---
### ⚖️ License

This project is licensed under the MIT License - see the [LICENSE](/LICENSE) file for details.

