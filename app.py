import streamlit as st
import requests
import base64
from PIL import Image
import io

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="AURA · Personal Style Advisor",
    page_icon="✦",
    layout="centered",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,600;1,300;1,400&family=DM+Sans:wght@300;400;500&display=swap');

html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 1.5rem; padding-bottom: 2rem; max-width: 860px; }

.stApp {
    background: linear-gradient(160deg, #0f0c0c 0%, #1a1118 50%, #0d1117 100%);
    color: #f0e6d3;
    min-height: 100vh;
}

.aura-title {
    font-family: 'Cormorant Garamond', serif;
    font-weight: 300;
    font-size: 3rem;
    letter-spacing: 0.3em;
    color: #d4a373;
    text-align: center;
    margin-bottom: 0;
    line-height: 1;
}
.aura-sub {
    font-size: 0.65rem;
    letter-spacing: 0.28em;
    color: #7d6e5e;
    text-transform: uppercase;
    text-align: center;
    margin-bottom: 0.3rem;
}
.aura-tagline {
    font-family: 'Cormorant Garamond', serif;
    font-style: italic;
    font-size: 1rem;
    color: #9e8c7a;
    text-align: center;
    margin-bottom: 1.5rem;
}

hr { border: none; height: 1px; background: linear-gradient(90deg, transparent, #d4a37350, transparent); margin: 1.2rem 0; }

.section-label {
    font-size: 0.62rem;
    letter-spacing: 0.22em;
    text-transform: uppercase;
    color: #7d6e5e;
    margin-bottom: 0.4rem;
}

section[data-testid="stSidebar"] {
    background: #0d0b0b !important;
    border-right: 1px solid #2a2020 !important;
}

div[data-testid="stNumberInput"] input,
div[data-testid="stTextInput"] input {
    background: #1a1412 !important;
    border: 1px solid #3a2e2e !important;
    border-radius: 8px !important;
    color: #f0e6d3 !important;
    font-family: 'DM Sans', sans-serif !important;
}

div[data-testid="stSelectbox"] > div > div {
    background: #1a1412 !important;
    border: 1px solid #3a2e2e !important;
    border-radius: 8px !important;
    color: #f0e6d3 !important;
}

div[data-testid="stFileUploader"] {
    background: #1a1412 !important;
    border: 1px dashed #3a2e2e !important;
    border-radius: 12px !important;
    padding: 1rem !important;
}

div[data-testid="stButton"] > button {
    background: linear-gradient(135deg, #d4a373, #b8860b) !important;
    color: #0f0c0c !important;
    border: none !important;
    border-radius: 10px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 500 !important;
    font-size: 0.9rem !important;
    letter-spacing: 0.08em !important;
    padding: 0.6rem 2rem !important;
    width: 100% !important;
    transition: all 0.2s !important;
}

div[data-testid="stButton"] > button:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 8px 24px rgba(212,163,115,0.25) !important;
}

.result-card {
    background: linear-gradient(135deg, #1a1412, #14100e);
    border: 1px solid #3a2e2e;
    border-radius: 16px;
    padding: 2rem;
    margin-top: 1.5rem;
    position: relative;
    overflow: hidden;
}

.result-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, transparent, #d4a373, transparent);
}

.result-text {
    color: #c8b8a8;
    font-size: 0.88rem;
    line-height: 1.8;
}

.stat-row {
    display: flex;
    gap: 12px;
    flex-wrap: wrap;
    margin-bottom: 1rem;
}

.stat-chip {
    background: #1f1815;
    border: 1px solid #3a2e2e;
    border-radius: 8px;
    padding: 6px 14px;
    font-size: 0.78rem;
    color: #9e8c7a;
}

.stat-chip span { color: #d4a373; font-weight: 500; }
</style>
""", unsafe_allow_html=True)

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown('<div class="aura-title">✦ AURA</div>', unsafe_allow_html=True)
st.markdown('<div class="aura-sub">Personal Style Intelligence</div>', unsafe_allow_html=True)
st.markdown('<div class="aura-tagline">Your AI-powered stylist — clothes, hair, watches & personality</div>', unsafe_allow_html=True)
st.markdown('<hr>', unsafe_allow_html=True)

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### ✦ AURA Settings")
    st.markdown("---")
    st.markdown("<small style='color:#7d6e5e'>GEMINI API KEY</small>", unsafe_allow_html=True)

    api_key = ""
    try:
        api_key = st.secrets["GEMINI_API_KEY"]
        st.success("API key loaded ✓", icon="🔑")
    except:
        api_key = st.text_input("Paste your Gemini API Key", type="password", placeholder="AIza...")
        st.markdown("<small style='color:#7d6e5e'>Get free key at aistudio.google.com</small>", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("**How it works**")
    st.markdown("<small style='color:#7d6e5e'>Upload your photo, fill in your stats, then click Analyze. AURA generates a full personalized style report.</small>", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("<small style='color:#3a2e2e'>Powered by Google Gemini Vision AI</small>", unsafe_allow_html=True)

# ── Main form ─────────────────────────────────────────────────────────────────
col1, col2 = st.columns([1.2, 1])

with col1:
    st.markdown('<div class="section-label">Upload Your Photo</div>', unsafe_allow_html=True)
    uploaded = st.file_uploader(
        "Drop your photo here",
        type=["jpg", "jpeg", "png", "webp"],
        label_visibility="collapsed"
    )
    if uploaded:
        img = Image.open(uploaded)
        st.image(img, use_container_width=True, caption="Your photo")

with col2:
    st.markdown('<div class="section-label">Your Details</div>', unsafe_allow_html=True)

    gender = st.selectbox("Gender", ["Male", "Female", "Non-binary"])
    height_cm = st.number_input("Height (cm)", min_value=140, max_value=220, value=170)
    weight_kg = st.number_input("Weight (kg)", min_value=40, max_value=200, value=70)
    age = st.number_input("Age", min_value=13, max_value=80, value=25)
    skin_tone = st.selectbox("Skin Tone", [
        "Fair / Light", "Light Medium", "Medium / Olive",
        "Medium Dark", "Dark / Deep", "Very Dark"
    ])
    style_vibe = st.selectbox("Style Preference", [
        "No preference — surprise me!", "Casual & Relaxed",
        "Smart Casual", "Formal / Business", "Streetwear",
        "Luxury / High Fashion", "Minimalist", "Sporty / Athletic"
    ])

st.markdown('<hr>', unsafe_allow_html=True)
analyze = st.button("✦  Analyze My Style")

# ── Analysis ──────────────────────────────────────────────────────────────────
if analyze:
    if not api_key:
        st.error("Please enter your Gemini API key in the sidebar.", icon="🔑")
        st.stop()
    if not uploaded:
        st.warning("Please upload a photo.", icon="📸")
        st.stop()

    # BMI
    bmi = round(weight_kg / ((height_cm / 100) ** 2), 1)
    if bmi < 18.5:
        body_type = "Slim / Lean"
    elif bmi < 25:
        body_type = "Athletic / Average"
    elif bmi < 30:
        body_type = "Medium / Full"
    else:
        body_type = "Broad / Heavy-set"

    if gender == "Male":
        height_cat = "Petite" if height_cm < 170 else "Average" if height_cm < 180 else "Tall" if height_cm < 188 else "Very Tall"
    else:
        height_cat = "Petite" if height_cm < 158 else "Average" if height_cm < 168 else "Tall" if height_cm < 175 else "Very Tall"

    st.markdown(f"""
    <div class="stat-row">
        <div class="stat-chip">Height <span>{height_cm}cm · {height_cat}</span></div>
        <div class="stat-chip">Weight <span>{weight_kg}kg</span></div>
        <div class="stat-chip">BMI <span>{bmi} · {body_type}</span></div>
        <div class="stat-chip">Skin <span>{skin_tone}</span></div>
        <div class="stat-chip">Age <span>{age}</span></div>
    </div>
    """, unsafe_allow_html=True)

    prompt = f"""
You are AURA, a world-class personal stylist and image advisor.

Analyze the person's photo and stats to generate a COMPLETE personalized style report.

STATS:
- Gender: {gender}
- Age: {age}
- Height: {height_cm}cm ({height_cat})
- Weight: {weight_kg}kg — BMI: {bmi} ({body_type})
- Skin Tone: {skin_tone}
- Style Preference: {style_vibe}

Generate a detailed style report with these sections:

1. 🧠 PERSONALITY ARCHETYPE
Their style personality in 2-3 sentences. Give 2-3 archetype labels (e.g. "The Modern Gentleman").

2. 👔 CLOTHING RECOMMENDATIONS
- Best outfit styles and cuts for their body type and height
- Specific clothing items to own
- What to avoid
- Best colors for their skin tone (specific color names)
- Best color combinations

3. 💇 HAIRSTYLE RECOMMENDATIONS
- Best hairstyles for their face shape
- Specific haircut names
- Hair color suggestions
- Styling tips

4. ⌚ WATCHES & ACCESSORIES
- Best watch styles with specific recommendations
- Watch case size for their wrist
- Belts, shoes, bags, jewelry suggestions
- Best metals for their skin tone

5. 👟 FOOTWEAR
- Best shoe styles for their height and body
- Specific shoe types to own
- Colors and materials

6. ✦ COMPLETE STYLE FORMULA
3-4 sentence summary of their perfect style formula.

Be specific and confident. Tailor everything to THIS person exactly.
"""

    with st.spinner("✦ Analyzing your style..."):
        try:
            # Convert image to base64
            img_bytes = uploaded.getvalue()
            img_b64 = base64.b64encode(img_bytes).decode("utf-8")
            mime_type = uploaded.type

            # Call Gemini REST API directly — no SDK needed
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={api_key}"

            payload = {
                "contents": [
                    {
                        "parts": [
                            {"text": prompt},
                            {
                                "inline_data": {
                                    "mime_type": mime_type,
                                    "data": img_b64
                                }
                            }
                        ]
                    }
                ]
            }

            response = requests.post(url, json=payload, timeout=60)
            data = response.json()

            if response.status_code != 200:
                error_msg = data.get("error", {}).get("message", "Unknown error")
                st.error(f"API Error: {error_msg}", icon="⚠")
                st.stop()

            result = data["candidates"][0]["content"]["parts"][0]["text"]

            st.markdown('<hr>', unsafe_allow_html=True)
            st.markdown("""
                <div style="text-align:center;margin-bottom:1rem;">
                    <div style="font-family:'Cormorant Garamond',serif;font-size:1.5rem;color:#d4a373;letter-spacing:0.15em;">✦ Your Style Report</div>
                    <div style="font-size:0.65rem;letter-spacing:0.2em;color:#7d6e5e;text-transform:uppercase;">Personalized by AURA AI</div>
                </div>
            """, unsafe_allow_html=True)

            st.markdown(f"""
            <div class="result-card">
                <div class="result-text">{result.replace(chr(10), '<br>')}</div>
            </div>
            """, unsafe_allow_html=True)

            st.download_button(
                label="⬇  Download My Style Report",
                data=result,
                file_name="aura_style_report.txt",
                mime="text/plain",
            )

        except requests.exceptions.Timeout:
            st.error("Request timed out. Please try again.", icon="⏱")
        except Exception as e:
            st.error(f"Something went wrong: {str(e)}", icon="⚠")

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown('<hr>', unsafe_allow_html=True)
st.markdown("""
<div style="text-align:center;color:#3a2e2e;font-size:0.7rem;letter-spacing:0.1em;">
    AURA · Personal Style Intelligence · Powered by Google Gemini Vision AI
</div>
""", unsafe_allow_html=True)

