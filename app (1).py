import streamlit as st
import google.generativeai as genai
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

/* Sidebar */
section[data-testid="stSidebar"] {
    background: #0d0b0b !important;
    border-right: 1px solid #2a2020 !important;
}

/* Inputs */
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

.stSlider > div { color: #d4a373 !important; }
.stSlider [data-testid="stThumbValue"] { color: #d4a373 !important; }

/* Upload box */
div[data-testid="stFileUploader"] {
    background: #1a1412 !important;
    border: 1px dashed #3a2e2e !important;
    border-radius: 12px !important;
    padding: 1rem !important;
}

/* Analyze button */
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

/* Result card */
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

.result-section {
    margin-bottom: 1.5rem;
}

.result-section-title {
    font-family: 'Cormorant Garamond', serif;
    font-size: 1.1rem;
    font-weight: 600;
    color: #d4a373;
    letter-spacing: 0.1em;
    margin-bottom: 0.5rem;
    display: flex;
    align-items: center;
    gap: 8px;
}

.result-text {
    color: #c8b8a8;
    font-size: 0.88rem;
    line-height: 1.8;
}

.tag {
    display: inline-block;
    background: rgba(212,163,115,0.1);
    border: 1px solid rgba(212,163,115,0.25);
    border-radius: 20px;
    padding: 3px 12px;
    font-size: 0.75rem;
    color: #d4a373;
    margin: 3px;
}

.personality-badge {
    display: inline-block;
    background: linear-gradient(135deg, rgba(212,163,115,0.15), rgba(184,134,11,0.1));
    border: 1px solid rgba(212,163,115,0.3);
    border-radius: 8px;
    padding: 6px 16px;
    font-family: 'Cormorant Garamond', serif;
    font-size: 1rem;
    color: #d4a373;
    letter-spacing: 0.05em;
    margin: 4px;
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

# ── Sidebar — API Key ─────────────────────────────────────────────────────────
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
    st.markdown("<small style='color:#7d6e5e'>Upload your photo, fill in your measurements and skin tone, then click Analyze. AURA will generate a full personalized style report just for you.</small>", unsafe_allow_html=True)
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
    st.markdown('<div class="section-label">Your Measurements</div>', unsafe_allow_html=True)

    gender = st.selectbox("Gender", ["Male", "Female", "Non-binary"], label_visibility="collapsed")

    height_cm = st.number_input(
        "Height (cm)", min_value=140, max_value=220, value=170,
        help="Your height in centimeters"
    )

    weight_kg = st.number_input(
        "Weight (kg)", min_value=40, max_value=200, value=70,
        help="Your weight in kilograms"
    )

    age = st.number_input("Age", min_value=13, max_value=80, value=25)

    skin_tone = st.selectbox(
        "Skin Tone",
        ["Fair / Light", "Light Medium", "Medium / Olive", "Medium Dark", "Dark / Deep", "Very Dark"],
    )

    style_vibe = st.selectbox(
        "Style You Like",
        ["No preference — surprise me!", "Casual & Relaxed", "Smart Casual", "Formal / Business", "Streetwear", "Luxury / High Fashion", "Minimalist", "Sporty / Athletic"],
    )

st.markdown('<hr>', unsafe_allow_html=True)

# ── Analyze button ────────────────────────────────────────────────────────────
analyze = st.button("✦  Analyze My Style")

# ── Analysis ─────────────────────────────────────────────────────────────────
if analyze:
    if not api_key:
        st.error("Please enter your Gemini API key in the sidebar.", icon="🔑")
        st.stop()

    if not uploaded:
        st.warning("Please upload a photo to analyze.", icon="📸")
        st.stop()

    # BMI calculation
    height_m = height_cm / 100
    bmi = round(weight_kg / (height_m ** 2), 1)
    if bmi < 18.5:
        body_type = "Slim / Lean"
    elif bmi < 25:
        body_type = "Athletic / Average"
    elif bmi < 30:
        body_type = "Medium / Full"
    else:
        body_type = "Broad / Heavy-set"

    # Height category
    if gender == "Male":
        if height_cm < 170:
            height_cat = "Petite / Short"
        elif height_cm < 180:
            height_cat = "Average Height"
        elif height_cm < 188:
            height_cat = "Tall"
        else:
            height_cat = "Very Tall"
    else:
        if height_cm < 158:
            height_cat = "Petite / Short"
        elif height_cm < 168:
            height_cat = "Average Height"
        elif height_cm < 175:
            height_cat = "Tall"
        else:
            height_cat = "Very Tall"

    # Show stats
    st.markdown(f"""
    <div class="stat-row">
        <div class="stat-chip">Height <span>{height_cm} cm · {height_cat}</span></div>
        <div class="stat-chip">Weight <span>{weight_kg} kg</span></div>
        <div class="stat-chip">BMI <span>{bmi} · {body_type}</span></div>
        <div class="stat-chip">Skin <span>{skin_tone}</span></div>
        <div class="stat-chip">Age <span>{age}</span></div>
    </div>
    """, unsafe_allow_html=True)

    # Build prompt
    prompt = f"""
You are AURA, a world-class personal stylist, fashion consultant, and image advisor with expertise in color theory, body proportions, and luxury fashion.

Analyze the person's photo and their stats below to generate a COMPLETE, highly personalized style report.

PERSON'S STATS:
- Gender: {gender}
- Age: {age}
- Height: {height_cm} cm ({height_cat})
- Weight: {weight_kg} kg
- BMI: {bmi} ({body_type})
- Skin Tone: {skin_tone}
- Style Preference: {style_vibe}

Analyze their facial features, face shape, and overall appearance from the photo.

Generate a detailed style report with these exact sections:

1. 🧠 PERSONALITY ARCHETYPE
Describe their overall style personality in 2-3 sentences. Give them 2-3 personality archetype labels (e.g. "The Modern Gentleman", "The Creative Rebel").

2. 👔 CLOTHING RECOMMENDATIONS
- Best outfit styles and cuts that flatter their body type and height
- Specific clothing items they should own
- What to avoid
- Best colors for their skin tone (give specific color names)
- Color combinations that work best

3. 💇 HAIRSTYLE RECOMMENDATIONS
- Best hairstyle options for their face shape
- Specific haircut names
- Hair color suggestions that complement their skin tone
- Styling tips

4. ⌚ WATCH & ACCESSORIES
- Best watch styles (dress, sport, casual) and specific recommendations
- Watch case size that suits their wrist proportions
- Other accessories: belts, shoes, bags, jewelry
- Metals and materials that work with their skin tone

5. 👟 FOOTWEAR
- Best shoe styles for their height and body type
- Specific shoe types to own
- Colors and materials

6. ✦ COMPLETE STYLE FORMULA
A concise 3-4 sentence summary of their perfect style formula — the one thing they should remember about dressing themselves.

Be specific, confident, and luxurious in your language. Avoid generic advice — tailor everything to THIS person's exact measurements and appearance.
"""

    with st.spinner("✦ Analyzing your style..."):
        try:
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel("gemini-1.5-flash")

            img_bytes = uploaded.getvalue()
            image_part = {
                "mime_type": uploaded.type,
                "data": img_bytes
            }

            response = model.generate_content([prompt, image_part])
            result = response.text

            # Display result
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

            # Download button
            st.download_button(
                label="⬇  Download My Style Report",
                data=result,
                file_name="aura_style_report.txt",
                mime="text/plain",
            )

        except Exception as e:
            err = str(e)
            if "API_KEY" in err.upper() or "invalid" in err.lower():
                st.error("Invalid API key. Please check your Gemini API key.", icon="🔑")
            elif "quota" in err.lower():
                st.error("API quota exceeded. Please try again later.", icon="⚠")
            else:
                st.error(f"Something went wrong: {err}", icon="⚠")

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown('<hr>', unsafe_allow_html=True)
st.markdown("""
<div style="text-align:center;color:#3a2e2e;font-size:0.7rem;letter-spacing:0.1em;">
    AURA · Personal Style Intelligence · Powered by Google Gemini Vision AI
</div>
""", unsafe_allow_html=True)
