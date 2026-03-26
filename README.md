---

# ⚡ PixelForge AI

**PixelForge AI** is an advanced image processing web app built with **Streamlit** that combines multiple AI-powered image enhancement steps into a single pipeline.

It allows users to:

* ✂️ Remove backgrounds
* 🎨 Enhance image quality
* 🔍 Upscale resolution
* 🌑 Add drop shadows
* 📦 Export in multiple formats

---

## 🚀 Features

### 🖼️ Image Processing Pipeline

* Background Removal (using `rembg`)
* Image Enhancement (brightness, contrast, sharpness, saturation)
* Image Upscaling (2×, 3×, 4×)
* Drop Shadow Effect
* Custom Output Resizing

### 🎛️ User Controls

* Interactive sliders for enhancement
* Toggle pipeline steps on/off
* Output size selection
* Background options:

  * Transparent
  * White background

### 📦 Export Options

* PNG (supports transparency)
* JPEG
* WEBP

### ⚡ UI/UX

* Modern animated UI
* Real-time progress tracking
* Live preview panel
* Download processed images instantly

---

## 🛠️ Tech Stack

* **Frontend/UI:** Streamlit + Custom CSS
* **Image Processing:** Pillow (PIL)
* **Background Removal:** rembg
* **Language:** Python

---

## 📂 Project Structure

```
pixelforge-ai/
│
├── app.py                # Main Streamlit application
├── requirements.txt     # Dependencies
├── README.md            # Project documentation
└── assets/              # (Optional) images/screenshots
```

---

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/your-username/pixelforge-ai.git
cd pixelforge-ai
```

### 2. Create virtual environment (recommended)

```bash
python -m venv venv
source venv/bin/activate   # Mac/Linux
venv\Scripts\activate      # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Install rembg (for background removal)

```bash
pip install rembg
```

---

## ▶️ Run the App

```bash
streamlit run app.py
```

Then open:

```
http://localhost:8501
```

---

## 📸 Usage

1. Upload an image (PNG, JPG, WEBP)
2. Select processing steps:

   * Remove background
   * Enhance image
   * Upscale
   * Add shadow
3. Adjust sliders (optional)
4. Choose output format & size
5. Click **⚡ Process Image**
6. Download the result

---

## 📦 requirements.txt

Example:

```txt
streamlit
pillow
rembg
```

---

## ⚠️ Notes

* `rembg` requires additional dependencies (like `onnxruntime`)
* Large images may take more processing time
* Transparent output works best with PNG format

---

## 💡 Future Improvements

* 🤖 AI Super-Resolution (ESRGAN / Real-ESRGAN)
* 🎯 Object Detection & Auto-Cropping
* 🌐 API Deployment (Hugging Face / Replicate)
* ☁️ Cloud Storage Integration
* 📱 Mobile Optimization

---

## 🤝 Contributing

Pull requests are welcome!
For major changes, please open an issue first.

---

## 📄 License

This project is licensed under the **MIT License**.

---

## 👨‍💻 Author

**Siyath Epa**
Computer Science Undergraduate
Sri Lanka 🇱🇰

---
* Add **badges (build, license, stars)**
* Help you deploy this on **Hugging Face / Streamlit Cloud / Replicate (to earn money 💰)**
