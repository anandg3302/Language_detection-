"""
Language Detection App with Python
==================================
Detects the language of user-input text using the langdetect library.
Shows confidence bars for all detected languages with a clean Streamlit GUI.
"""

import streamlit as st
from langdetect import detect_langs, LangDetectException

# =============================================================================
# LANGUAGE CODE TO FULL NAME MAPPING
# =============================================================================
LANGUAGE_NAMES = {
    "af": "Afrikaans", "ar": "Arabic", "bg": "Bulgarian", "bn": "Bengali",
    "ca": "Catalan", "cs": "Czech", "cy": "Welsh", "da": "Danish",
    "de": "German", "el": "Greek", "en": "English", "es": "Spanish",
    "et": "Estonian", "fa": "Persian", "fi": "Finnish", "fr": "French",
    "gu": "Gujarati", "he": "Hebrew", "hi": "Hindi", "hr": "Croatian",
    "hu": "Hungarian", "id": "Indonesian", "it": "Italian", "ja": "Japanese",
    "kn": "Kannada", "ko": "Korean", "lt": "Lithuanian", "lv": "Latvian",
    "mk": "Macedonian", "ml": "Malayalam", "mr": "Marathi", "ne": "Nepali",
    "nl": "Dutch", "no": "Norwegian", "pa": "Punjabi", "pl": "Polish",
    "pt": "Portuguese", "ro": "Romanian", "ru": "Russian", "sk": "Slovak",
    "sl": "Slovenian", "so": "Somali", "sq": "Albanian", "sv": "Swedish",
    "sw": "Swahili", "ta": "Tamil", "te": "Telugu", "th": "Thai",
    "tl": "Tagalog", "tr": "Turkish", "uk": "Ukrainian", "ur": "Urdu",
    "vi": "Vietnamese", "zh-cn": "Chinese (Simplified)", "zh-tw": "Chinese (Traditional)",
}

def get_language_name(code: str) -> str:
    return LANGUAGE_NAMES.get(code.lower(), code)

def detect_language(text: str) -> dict:
    """Detect language(s) with confidence scores."""
    if not text or not text.strip():
        return {"success": False, "error": "Please enter some text.", 
                "primary_lang": None, "primary_code": None, "primary_confidence": None, "all_detections": None}

    if len(text.split()) < 2:
        return {"success": False, "error": "Text too short. Enter at least 2 words.", 
                "primary_lang": None, "primary_code": None, "primary_confidence": None, "all_detections": None}

    try:
        detections = detect_langs(text)
        if not detections:
            return {"success": False, "error": "Could not detect language. Try longer text.",
                    "primary_lang": None, "primary_code": None, "primary_confidence": None, "all_detections": None}

        all_detections = [(d.lang, get_language_name(d.lang), round(d.prob, 4)) for d in detections]
        primary = detections[0]

        return {
            "success": True,
            "primary_lang": get_language_name(primary.lang),
            "primary_code": primary.lang,
            "primary_confidence": round(primary.prob, 4),
            "all_detections": all_detections,
            "error": None
        }

    except LangDetectException as e:
        return {"success": False, "error": f"Detection failed: {str(e)}",
                "primary_lang": None, "primary_code": None, "primary_confidence": None, "all_detections": None}
    except Exception as e:
        return {"success": False, "error": f"Unexpected error: {str(e)}",
                "primary_lang": None, "primary_code": None, "primary_confidence": None, "all_detections": None}

# =============================================================================
# STREAMLIT CONFIG
# =============================================================================
st.set_page_config(page_title="Language Detection", page_icon="🌐", layout="centered", initial_sidebar_state="expanded")

# Custom CSS
st.markdown("""
<style>
.main .block-container { padding-top: 2rem; padding-bottom: 2rem; max-width: 700px; }
h1 { color: #1e3a5f; font-weight: 700; text-align: center; margin-bottom: 0.5rem; }
.subtitle { color: #64748b; font-size: 1rem; text-align: center; margin-bottom: 2rem; }
.success-box { background: linear-gradient(135deg, #d1fae5 0%, #a7f3d0 100%);
  border-left: 4px solid #059669; padding: 1.25rem; border-radius: 8px; margin: 1rem 0; }
.error-box { background: linear-gradient(135deg, #fee2e2 0%, #fecaca 100%);
  border-left: 4px solid #dc2626; padding: 1.25rem; border-radius: 8px; margin: 1rem 0; }
.confidence-bar { background: #e2e8f0; border-radius: 10px; height: 12px; margin: 0.5rem 0; overflow: hidden; }
.confidence-fill { height: 100%; background: linear-gradient(90deg, #3b82f6, #06b6d4); border-radius: 10px; transition: width 0.5s ease; }
</style>
""", unsafe_allow_html=True)

# =============================================================================
# MAIN INTERFACE
# =============================================================================
st.markdown("# 🌐 Language Detection System")
st.markdown('<p class="subtitle">Detect the language of your text instantly. Shows confidence for all candidates.</p>', unsafe_allow_html=True)

user_text = st.text_area("Enter your text below",
                         placeholder="Type or paste text here (e.g., Bonjour, comment ça va ?)",
                         height=150, label_visibility="collapsed")

col1, col2, col3 = st.columns([1,2,1])
with col2:
    detect_button = st.button("🔍 Detect Language", use_container_width=True)

if detect_button:
    result = detect_language(user_text)

    if result["success"]:
        st.markdown("### ✅ Result")
        # Primary language
        st.markdown(f"""
            <div class="success-box">
                <strong>Primary Language:</strong> {result['primary_lang']}<br>
                <strong>Code:</strong> <code>{result['primary_code']}</code>
            </div>
        """, unsafe_allow_html=True)

        # Show confidence bars for all detected languages
        st.markdown("**Confidence Scores for Detected Languages:**")
        for code, name, prob in result["all_detections"]:
            pct = round(prob*100)
            st.markdown(f"• {name} ({code}): {pct}%")
            st.markdown(f'<div class="confidence-bar"><div class="confidence-fill" style="width: {pct}%;"></div></div>', unsafe_allow_html=True)
    else:
        st.markdown("### ❌ Error")
        st.markdown(f'<div class="error-box"><strong>{result["error"]}</strong></div>', unsafe_allow_html=True)

# =============================================================================
# SIDEBAR
# =============================================================================
with st.sidebar:
    st.markdown("### 📋 Supported Languages")
    for code in sorted(LANGUAGE_NAMES.keys()):
        st.caption(f"• {code} → {LANGUAGE_NAMES[code]}")
    st.markdown("---")
    st.caption("Built with Python & Streamlit | langdetect library")