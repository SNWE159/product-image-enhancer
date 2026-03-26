import streamlit as st
from PIL import Image, ImageFilter, ImageEnhance
import io
import base64
import time
import os

# ─── Page Config ────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="PixelForge AI",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─── Custom CSS ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:ital,wght@0,300;0,400;0,500;1,300&display=swap');

/* ── Reset & Base ── */
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body, .stApp {
    background: #080810;
    color: #f0eee8;
    font-family: 'DM Sans', sans-serif;
}

/* Hide default Streamlit elements */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 0 !important; max-width: 100% !important; }
.stDeployButton { display: none; }

/* ── Animated Background ── */
.stApp::before {
    content: '';
    position: fixed;
    inset: 0;
    background:
        radial-gradient(ellipse 80% 50% at 20% 10%, rgba(99,60,255,0.18) 0%, transparent 60%),
        radial-gradient(ellipse 60% 40% at 80% 80%, rgba(255,90,130,0.12) 0%, transparent 60%),
        radial-gradient(ellipse 50% 60% at 60% 30%, rgba(0,210,200,0.08) 0%, transparent 55%);
    pointer-events: none;
    z-index: 0;
    animation: bgShift 12s ease-in-out infinite alternate;
}

@keyframes bgShift {
    0%   { opacity: 1; transform: scale(1); }
    100% { opacity: 0.8; transform: scale(1.04); }
}

/* ── Grid Overlay ── */
.stApp::after {
    content: '';
    position: fixed;
    inset: 0;
    background-image:
        linear-gradient(rgba(255,255,255,0.025) 1px, transparent 1px),
        linear-gradient(90deg, rgba(255,255,255,0.025) 1px, transparent 1px);
    background-size: 60px 60px;
    pointer-events: none;
    z-index: 0;
}

/* ── Layout Wrapper ── */
.main-wrapper {
    position: relative;
    z-index: 1;
    padding: 0 40px 60px 40px;
    max-width: 1300px;
    margin: 0 auto;
}

/* ── Hero Section ── */
.hero {
    padding: 60px 0 48px 0;
    text-align: center;
    position: relative;
}

.hero-badge {
    display: inline-block;
    background: rgba(99,60,255,0.15);
    border: 1px solid rgba(99,60,255,0.4);
    color: #a78bfa;
    font-family: 'DM Sans', sans-serif;
    font-size: 11px;
    font-weight: 500;
    letter-spacing: 3px;
    text-transform: uppercase;
    padding: 6px 18px;
    border-radius: 100px;
    margin-bottom: 28px;
}

.hero-title {
    font-family: 'Syne', sans-serif;
    font-size: clamp(48px, 7vw, 88px);
    font-weight: 800;
    line-height: 0.95;
    letter-spacing: -3px;
    background: linear-gradient(135deg, #ffffff 30%, #a78bfa 65%, #f472b6 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 20px;
}

.hero-sub {
    font-size: 17px;
    font-weight: 300;
    color: rgba(240,238,232,0.5);
    letter-spacing: 0.2px;
    max-width: 500px;
    margin: 0 auto 44px auto;
    line-height: 1.7;
}

/* ── Pipeline Strip ── */
.pipeline {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 0;
    margin-bottom: 56px;
    flex-wrap: wrap;
    gap: 4px;
}

.pipe-step {
    display: flex;
    align-items: center;
    gap: 10px;
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 12px;
    padding: 10px 20px;
    font-size: 13px;
    font-weight: 500;
    color: rgba(240,238,232,0.7);
    letter-spacing: 0.3px;
    transition: all 0.25s;
}

.pipe-step .icon { font-size: 18px; }

.pipe-step.active {
    background: rgba(99,60,255,0.18);
    border-color: rgba(99,60,255,0.5);
    color: #c4b5fd;
    box-shadow: 0 0 24px rgba(99,60,255,0.2);
}

.pipe-arrow {
    color: rgba(255,255,255,0.15);
    font-size: 18px;
    margin: 0 4px;
}

/* ── Upload Zone ── */
.upload-zone {
    background: rgba(255,255,255,0.025);
    border: 2px dashed rgba(99,60,255,0.35);
    border-radius: 24px;
    padding: 56px 40px;
    text-align: center;
    transition: all 0.3s ease;
    cursor: pointer;
    position: relative;
    overflow: hidden;
}

.upload-zone::before {
    content: '';
    position: absolute;
    inset: 0;
    background: radial-gradient(ellipse at center, rgba(99,60,255,0.06) 0%, transparent 70%);
    pointer-events: none;
}

.upload-zone:hover {
    border-color: rgba(99,60,255,0.7);
    background: rgba(99,60,255,0.06);
    box-shadow: 0 0 40px rgba(99,60,255,0.12);
}

.upload-icon { font-size: 52px; margin-bottom: 16px; display: block; }
.upload-title {
    font-family: 'Syne', sans-serif;
    font-size: 22px;
    font-weight: 700;
    color: #e8e4ff;
    margin-bottom: 8px;
}
.upload-sub { font-size: 14px; color: rgba(240,238,232,0.4); }

/* ── Control Panel ── */
.control-card {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 20px;
    padding: 28px;
    margin-bottom: 16px;
    position: relative;
    overflow: hidden;
}

.control-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, #633cff, #f472b6, transparent);
}

.control-title {
    font-family: 'Syne', sans-serif;
    font-size: 13px;
    font-weight: 700;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: rgba(240,238,232,0.4);
    margin-bottom: 18px;
    display: flex;
    align-items: center;
    gap: 8px;
}

/* ── Process Button ── */
.stButton > button {
    width: 100%;
    background: linear-gradient(135deg, #633cff 0%, #a855f7 50%, #f472b6 100%) !important;
    color: white !important;
    border: none !important;
    border-radius: 14px !important;
    padding: 16px 32px !important;
    font-family: 'Syne', sans-serif !important;
    font-size: 15px !important;
    font-weight: 700 !important;
    letter-spacing: 0.5px !important;
    cursor: pointer !important;
    transition: all 0.3s ease !important;
    box-shadow: 0 8px 32px rgba(99,60,255,0.35) !important;
    position: relative !important;
    overflow: hidden !important;
}

.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 14px 44px rgba(99,60,255,0.5) !important;
}

.stButton > button:active {
    transform: translateY(0px) !important;
}

/* ── Result Card ── */
.result-card {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 24px;
    overflow: hidden;
    position: relative;
}

.result-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, transparent, #633cff, #f472b6, transparent);
}

.result-header {
    padding: 20px 28px 16px 28px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    border-bottom: 1px solid rgba(255,255,255,0.06);
}

.result-label {
    font-family: 'Syne', sans-serif;
    font-size: 12px;
    font-weight: 700;
    letter-spacing: 2.5px;
    text-transform: uppercase;
    color: rgba(240,238,232,0.35);
}

.result-badge {
    background: rgba(99,60,255,0.2);
    border: 1px solid rgba(99,60,255,0.4);
    color: #a78bfa;
    font-size: 11px;
    font-weight: 600;
    padding: 3px 12px;
    border-radius: 100px;
    letter-spacing: 1px;
}

.result-body { padding: 24px 28px 28px 28px; }

/* ── Stats Bar ── */
.stats-row {
    display: flex;
    gap: 12px;
    margin-bottom: 24px;
    flex-wrap: wrap;
}

.stat-chip {
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 10px;
    padding: 10px 16px;
    flex: 1;
    min-width: 90px;
    text-align: center;
}

.stat-value {
    font-family: 'Syne', sans-serif;
    font-size: 18px;
    font-weight: 800;
    color: #c4b5fd;
    display: block;
}

.stat-key {
    font-size: 10px;
    color: rgba(240,238,232,0.35);
    letter-spacing: 1.5px;
    text-transform: uppercase;
    margin-top: 2px;
    display: block;
}

/* ── Streamlit Overrides ── */
.stSelectbox > div > div {
    background: rgba(255,255,255,0.05) !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    border-radius: 12px !important;
    color: #f0eee8 !important;
}

.stSlider > div > div > div {
    background: rgba(99,60,255,0.4) !important;
}

.stSlider > div > div > div > div {
    background: #633cff !important;
    box-shadow: 0 0 12px rgba(99,60,255,0.6) !important;
}

.stCheckbox > label {
    color: rgba(240,238,232,0.7) !important;
    font-size: 14px !important;
}

label[data-testid="stWidgetLabel"] {
    color: rgba(240,238,232,0.6) !important;
    font-size: 13px !important;
    font-weight: 500 !important;
    letter-spacing: 0.3px !important;
    margin-bottom: 6px !important;
}

/* ── Divider ── */
.divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.08), transparent);
    margin: 32px 0;
}

/* ── Checkerboard for transparency ── */
.checker-bg {
    background-image:
        linear-gradient(45deg, #1a1a2e 25%, transparent 25%),
        linear-gradient(-45deg, #1a1a2e 25%, transparent 25%),
        linear-gradient(45deg, transparent 75%, #1a1a2e 75%),
        linear-gradient(-45deg, transparent 75%, #1a1a2e 75%);
    background-size: 20px 20px;
    background-position: 0 0, 0 10px, 10px -10px, -10px 0px;
    background-color: #12121f;
    border-radius: 12px;
    overflow: hidden;
}

/* ── Progress animation ── */
@keyframes pulse-ring {
    0%   { transform: scale(0.8); opacity: 1; }
    100% { transform: scale(2.0); opacity: 0; }
}

.stProgress > div > div > div {
    background: linear-gradient(90deg, #633cff, #f472b6) !important;
    border-radius: 100px !important;
}

/* Footer */
.footer {
    text-align: center;
    padding: 40px 0 20px 0;
    font-size: 12px;
    color: rgba(240,238,232,0.2);
    letter-spacing: 1px;
}

/* Image display */
.stImage img {
    border-radius: 12px;
}

/* Notification pills */
.success-pill {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: rgba(34,197,94,0.12);
    border: 1px solid rgba(34,197,94,0.3);
    color: #4ade80;
    font-size: 13px;
    font-weight: 500;
    padding: 8px 18px;
    border-radius: 100px;
    margin-bottom: 16px;
}

</style>
""", unsafe_allow_html=True)

# ─── Helper: image → base64 ──────────────────────────────────────────────────
def img_to_b64(img: Image.Image, fmt="PNG") -> str:
    buf = io.BytesIO()
    img.save(buf, format=fmt)
    return base64.b64encode(buf.getvalue()).decode()

def img_to_bytes(img: Image.Image, fmt="PNG") -> bytes:
    buf = io.BytesIO()
    img.save(buf, format=fmt)
    return buf.getvalue()

# ─── Core Pipeline Functions ─────────────────────────────────────────────────

def remove_background(img: Image.Image) -> Image.Image:
    try:
        from rembg import remove
        return remove(img)
    except ImportError:
        st.warning("⚠️ `rembg` not installed. Run: `pip install rembg`. Skipping BG removal.")
        return img

def enhance_image(img: Image.Image, brightness=1.0, contrast=1.0, sharpness=1.0, saturation=1.0) -> Image.Image:
    img = ImageEnhance.Brightness(img).enhance(brightness)
    img = ImageEnhance.Contrast(img).enhance(contrast)
    img = ImageEnhance.Sharpness(img).enhance(sharpness)
    img = ImageEnhance.Color(img).enhance(saturation)
    return img

def upscale_image(img: Image.Image, scale: int = 2) -> Image.Image:
    w, h = img.size
    try:
        from PIL import Image as PILImage
        return img.resize((w * scale, h * scale), PILImage.LANCZOS)
    except Exception:
        return img.resize((w * scale, h * scale))

def apply_shadow(img: Image.Image, blur_radius=20, opacity=120) -> Image.Image:
    if img.mode != "RGBA":
        img = img.convert("RGBA")
    shadow_layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    alpha = img.split()[3]
    shadow = Image.new("L", img.size, 0)
    shadow.paste(alpha, (8, 8))
    shadow = shadow.filter(ImageFilter.GaussianBlur(blur_radius))
    shadow_rgba = Image.new("RGBA", img.size, (0, 0, 0, opacity))
    shadow_rgba.putalpha(shadow)
    shadow_layer.paste(shadow_rgba, (0, 0))
    out = Image.alpha_composite(shadow_layer, img)
    return out

def apply_white_background(img: Image.Image) -> Image.Image:
    if img.mode != "RGBA":
        img = img.convert("RGBA")
    bg = Image.new("RGBA", img.size, (255, 255, 255, 255))
    return Image.alpha_composite(bg, img).convert("RGB")

def run_pipeline(
    img: Image.Image,
    do_remove_bg: bool,
    do_enhance: bool,
    do_upscale: bool,
    upscale_factor: int,
    do_shadow: bool,
    brightness: float,
    contrast: float,
    sharpness: float,
    saturation: float,
    output_size: tuple,
    bg_choice: str,
    progress_bar,
    status_text,
) -> Image.Image:

    steps = []
    if do_remove_bg:  steps.append("bg")
    if do_enhance:    steps.append("enhance")
    if do_upscale:    steps.append("upscale")
    if do_shadow:     steps.append("shadow")
    steps.append("resize")

    total = len(steps)
    done = 0

    def tick(msg):
        nonlocal done
        done += 1
        progress_bar.progress(done / total)
        status_text.markdown(f"<div style='color:rgba(240,238,232,0.5);font-size:13px;text-align:center;margin-top:8px;'>{msg}</div>", unsafe_allow_html=True)
        time.sleep(0.35)

    result = img.copy()

    if do_remove_bg:
        result = remove_background(result)
        tick("✦ Background removed")

    if do_enhance:
        result = enhance_image(result, brightness, contrast, sharpness, saturation)
        tick("✦ Enhancement applied")

    if do_upscale:
        result = upscale_image(result, upscale_factor)
        tick(f"✦ Upscaled {upscale_factor}×")

    if do_shadow:
        result = apply_shadow(result)
        tick("✦ Drop shadow added")

    # Resize to output
    if output_size[0] > 0:
        result = result.resize(output_size, Image.LANCZOS)
    tick("✦ Output rendered")

    # Background handling
    if bg_choice == "White Background":
        result = apply_white_background(result)
    elif bg_choice == "Keep Transparent":
        if result.mode != "RGBA":
            result = result.convert("RGBA")
    else:  # Transparent (PNG)
        if result.mode != "RGBA":
            result = result.convert("RGBA")

    return result

# ─── UI ─────────────────────────────────────────────────────────────────────

st.markdown('<div class="main-wrapper">', unsafe_allow_html=True)

# ── Hero ──
st.markdown("""
<div class="hero">
    <div class="hero-badge">✦ AI-Powered Image Pipeline</div>
    <div class="hero-title">PixelForge</div>
    <div class="hero-sub">Remove backgrounds, enhance details, upscale resolution — all in one intelligent pipeline.</div>
</div>
""", unsafe_allow_html=True)

# ── Pipeline Visualization ──
st.markdown("""
<div class="pipeline">
    <div class="pipe-step"><span class="icon">🖼️</span> Input</div>
    <span class="pipe-arrow">→</span>
    <div class="pipe-step"><span class="icon">✂️</span> Remove BG</div>
    <span class="pipe-arrow">→</span>
    <div class="pipe-step"><span class="icon">🎨</span> Enhance</div>
    <span class="pipe-arrow">→</span>
    <div class="pipe-step"><span class="icon">🔍</span> Upscale</div>
    <span class="pipe-arrow">→</span>
    <div class="pipe-step active"><span class="icon">⚡</span> Output</div>
</div>
""", unsafe_allow_html=True)

# ── Main Columns ──
col_left, col_right = st.columns([1, 1.5], gap="large")

# ── LEFT: Controls ──
with col_left:

    # Upload
    st.markdown('<div class="control-card">', unsafe_allow_html=True)
    st.markdown('<div class="control-title">📁 &nbsp;Upload Image</div>', unsafe_allow_html=True)
    uploaded = st.file_uploader(
        "Drop your product image here",
        type=["png", "jpg", "jpeg", "webp"],
        label_visibility="collapsed"
    )

    if not uploaded:
        st.markdown("""
        <div class="upload-zone">
            <span class="upload-icon">📤</span>
            <div class="upload-title">Drop your image here</div>
            <div class="upload-sub">PNG · JPG · WEBP · up to 50MB</div>
        </div>
        """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    if uploaded:
        orig_img = Image.open(uploaded)
        st.markdown('<div class="control-card">', unsafe_allow_html=True)
        st.markdown(f"""
        <div class="success-pill">✓ Image loaded — {orig_img.size[0]}×{orig_img.size[1]}px · {uploaded.size // 1024} KB</div>
        """, unsafe_allow_html=True)
        st.image(orig_img, use_container_width=True, caption="Original")
        st.markdown('</div>', unsafe_allow_html=True)

    # Pipeline Toggles
    st.markdown('<div class="control-card">', unsafe_allow_html=True)
    st.markdown('<div class="control-title">⚙️ &nbsp;Pipeline Steps</div>', unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        do_remove_bg = st.checkbox("✂️ Remove Background", value=True)
        do_enhance   = st.checkbox("🎨 Enhance Image",     value=True)
    with c2:
        do_upscale   = st.checkbox("🔍 Upscale",           value=False)
        do_shadow    = st.checkbox("🌑 Drop Shadow",        value=False)
    st.markdown('</div>', unsafe_allow_html=True)

    # Enhancement Controls
    if do_enhance:
        st.markdown('<div class="control-card">', unsafe_allow_html=True)
        st.markdown('<div class="control-title">🎛️ &nbsp;Enhancement Controls</div>', unsafe_allow_html=True)
        brightness = st.slider("☀️ Brightness", 0.5, 2.0, 1.05, 0.05)
        contrast   = st.slider("◐ Contrast",   0.5, 2.0, 1.10, 0.05)
        sharpness  = st.slider("🔪 Sharpness",  0.0, 3.0, 1.20, 0.10)
        saturation = st.slider("🎨 Saturation", 0.5, 2.0, 1.05, 0.05)
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        brightness = contrast = sharpness = saturation = 1.0

    # Output Options
    st.markdown('<div class="control-card">', unsafe_allow_html=True)
    st.markdown('<div class="control-title">📦 &nbsp;Output Options</div>', unsafe_allow_html=True)

    col_a, col_b = st.columns(2)
    with col_a:
        out_size_label = st.selectbox(
            "Output Size",
            ["Original", "512 × 512", "1024 × 1024", "2048 × 2048", "800 × 800"],
        )
    with col_b:
        upscale_factor = st.selectbox("Upscale Factor", [2, 3, 4], disabled=not do_upscale)

    bg_choice = st.selectbox(
        "Background",
        ["Keep Transparent", "White Background", "Transparent (PNG)"],
    )

    out_fmt = st.selectbox("Export Format", ["PNG", "JPEG", "WEBP"])
    st.markdown('</div>', unsafe_allow_html=True)

    size_map = {
        "Original": (0, 0),
        "512 × 512":   (512, 512),
        "1024 × 1024": (1024, 1024),
        "2048 × 2048": (2048, 2048),
        "800 × 800":   (800, 800),
    }
    output_size = size_map[out_size_label]

    # Process Button
    process_clicked = st.button("⚡  Process Image", disabled=(uploaded is None))

# ── RIGHT: Output ──
with col_right:
    st.markdown('<div class="result-card">', unsafe_allow_html=True)
    st.markdown("""
    <div class="result-header">
        <span class="result-label">Output Preview</span>
        <span class="result-badge">LIVE</span>
    </div>
    <div class="result-body">
    """, unsafe_allow_html=True)

    if not uploaded:
        st.markdown("""
        <div style="
            height:380px;
            display:flex;
            flex-direction:column;
            align-items:center;
            justify-content:center;
            color:rgba(240,238,232,0.2);
            font-size:14px;
            letter-spacing:1px;
        ">
            <div style="font-size:48px;margin-bottom:16px;">✦</div>
            Awaiting image upload
        </div>
        """, unsafe_allow_html=True)

    elif not process_clicked:
        # Show original with instructions
        st.image(orig_img, use_container_width=True)
        st.markdown("""
        <div style="text-align:center;margin-top:16px;color:rgba(240,238,232,0.35);font-size:13px;letter-spacing:0.5px;">
            Configure your pipeline ← then hit ⚡ Process
        </div>
        """, unsafe_allow_html=True)

    else:
        # Run pipeline
        st.markdown("""
        <div style="text-align:center;padding:16px 0 8px 0;">
            <div style="font-family:'Syne',sans-serif;font-size:15px;font-weight:700;color:#c4b5fd;letter-spacing:1px;">
                Processing your image...
            </div>
        </div>
        """, unsafe_allow_html=True)

        progress_bar = st.progress(0)
        status_text  = st.empty()

        with st.spinner(""):
            result_img = run_pipeline(
                img           = orig_img,
                do_remove_bg  = do_remove_bg,
                do_enhance    = do_enhance,
                do_upscale    = do_upscale,
                upscale_factor= upscale_factor,
                do_shadow     = do_shadow,
                brightness    = brightness,
                contrast      = contrast,
                sharpness     = sharpness,
                saturation    = saturation,
                output_size   = output_size,
                bg_choice     = bg_choice,
                progress_bar  = progress_bar,
                status_text   = status_text,
            )

        progress_bar.empty()
        status_text.empty()

        # Stats
        w, h = result_img.size
        orig_w, orig_h = orig_img.size
        img_bytes = img_to_bytes(result_img, out_fmt)
        size_kb = len(img_bytes) // 1024

        st.markdown(f"""
        <div class="stats-row">
            <div class="stat-chip">
                <span class="stat-value">{w}×{h}</span>
                <span class="stat-key">Resolution</span>
            </div>
            <div class="stat-chip">
                <span class="stat-value">{size_kb} KB</span>
                <span class="stat-key">File Size</span>
            </div>
            <div class="stat-chip">
                <span class="stat-value">{out_fmt}</span>
                <span class="stat-key">Format</span>
            </div>
            <div class="stat-chip">
                <span class="stat-value">✓</span>
                <span class="stat-key">Done</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Show result
        if result_img.mode == "RGBA":
            # Checkerboard
            st.markdown('<div class="checker-bg">', unsafe_allow_html=True)
            st.image(result_img, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.image(result_img, use_container_width=True)

        # Download
        st.markdown("<div style='margin-top:20px;'>", unsafe_allow_html=True)
        st.download_button(
            label=f"⬇️  Download {out_fmt}",
            data=img_bytes,
            file_name=f"pixelforge_output.{out_fmt.lower()}",
            mime=f"image/{out_fmt.lower()}",
            use_container_width=True,
        )
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('</div></div>', unsafe_allow_html=True)

# ── Footer ──
st.markdown("""
<div class="divider"></div>
<div class="footer">
    PIXELFORGE AI &nbsp;·&nbsp; Background Removal · Enhancement · Upscaling &nbsp;·&nbsp; Built with Streamlit
</div>
""", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)
