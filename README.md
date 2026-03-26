# ⚡ PixelForge AI

PixelForge AI is a powerful image processing web app built with Streamlit.  
It combines multiple AI-based image editing steps into one simple pipeline.

---

## 🚀 Features

- ✂️ Background Removal (rembg)
- 🎨 Image Enhancement (brightness, contrast, sharpness, saturation)
- 🔍 Image Upscaling (2x, 3x, 4x)
- 🌑 Drop Shadow Effect
- 📦 Resize & Export Options

---

## 🛠️ Tech Stack

- Python
- Streamlit
- Pillow (PIL)
- rembg

---

## 📂 Project Structure

```
pixelforge-ai/
│
├── app.py
├── requirements.txt
├── README.md
```

---

## ⚙️ Installation

### 1. Clone repo
```bash
git clone https://github.com/your-username/pixelforge-ai.git
cd pixelforge-ai
```

### 2. Create virtual environment
```bash
python -m venv venv
```

Activate it:

**Windows**
```bash
venv\Scripts\activate
```

**Mac/Linux**
```bash
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Install rembg
```bash
pip install rembg
```

---

## ▶️ Run the App

```bash
streamlit run app.py
```

Open in browser:
```
http://localhost:8501
```

---

## 📸 How to Use

1. Upload an image (PNG, JPG, WEBP)
2. Select processing options:
   - Remove background
   - Enhance image
   - Upscale
   - Add shadow
3. Adjust sliders if needed
4. Choose output format and size
5. Click **Process Image**
6. Download result

---

## 📦 requirements.txt

```
streamlit
pillow
rembg
```

---

## ⚠️ Notes

- PNG format supports transparency
- Large images may take more time
- rembg may install extra dependencies automatically

---

## 💡 Future Improvements

- AI super-resolution (Real-ESRGAN)
- Object detection
- API deployment
- Cloud hosting

---

## 👨‍💻 Author

Siyath Epa  
Sri Lanka 🇱🇰

---

## 📄 License

MIT License
