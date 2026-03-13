# AURA · Personal Style Advisor

An AI-powered personal stylist that analyzes your photo + measurements and generates personalized recommendations for clothes, hairstyle, watches, accessories, and overall personality styling.

## Features
- 📸 Upload your photo for AI visual analysis
- 👔 Clothing recommendations based on body type & skin tone
- 💇 Hairstyle suggestions for your face shape
- ⌚ Watch & accessories guide
- 👟 Footwear recommendations
- ✦ Complete personal style formula
- ⬇ Download your style report

## Files
```
style-advisor/
├── app.py               # Full app — one file!
├── requirements.txt     # Dependencies
├── .gitignore
└── .streamlit/
    └── secrets.toml.example
```

## Run Locally
```bash
pip install streamlit google-generativeai Pillow
streamlit run app.py
```

Add your Gemini API key in `.streamlit/secrets.toml`:
```toml
GEMINI_API_KEY = "AIza-your-key-here"
```

## Deploy FREE on Streamlit Cloud
1. Push `app.py`, `requirements.txt`, `.gitignore` to GitHub
2. Go to share.streamlit.io → New App → select repo → Deploy
3. In Settings → Secrets, add:
```toml
GEMINI_API_KEY = "AIza-your-key-here"
```

## Get Free Gemini API Key
1. Go to aistudio.google.com
2. Sign in with Google
3. Click "Get API Key" → "Create API Key"
4. Copy and paste into Streamlit Secrets — done!
