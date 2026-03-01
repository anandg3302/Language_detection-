"""
Language Detection App with Python - Improved Gemini Translation
==================================
Detects the language of user-input text using the langdetect library.
Shows confidence bars for all detected languages with a clean Streamlit GUI.
Generates text using the Generative AI model with improved translation.
"""

import streamlit as st
from langdetect import detect_langs, LangDetectException
from googletrans import Translator
from google.generativeai import GenerativeModel, configure
import json
import time
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

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

# Simplified Telugu keyboard layout - optimized for speed
telugu_keyboard = {
    'Vowels': ['అ', 'ఆ', 'ఇ', 'ఈ', 'ఉ', 'ఊ', 'ఋ', 'ఎ', 'ఏ', 'ఐ', 'ఒ', 'ఓ', 'ఔ'],
    'Common': ['క', 'గ', 'జ', 'ట', 'డ', 'ణ', 'త', 'ద', 'న', 'ప', 'ర', 'ల', 'వ', 'స', 'హ'],
    'Rare': ['ఖ', 'ఘ', 'ఙ', 'చ', 'ఛ', 'ఝ', 'ఞ', 'ఠ', 'ఢ', 'థ', 'ధ', 'భ', 'మ', 'య', 'శ', 'ష', 'ళ', 'క్ష'],
    'Modifiers': ['ం', 'ః', '్', 'ా', 'ి', 'ీ', 'ు', 'ూ', 'ృ', 'ౄ', 'ె', 'ే', 'ై', 'ొ', 'ో', 'ౌ', 'ౕ', 'ౖ'],
    'Numbers': ['౦', '౧', '౨', '౩', '౪', '౫', '౬', '౭', '౮', '౯'],
    'Actions': ['␣ Space', '⌫ Backspace']
}

# English keyboard layout
english_keyboard = {
    'Row1': ['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P'],
    'Row2': ['A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L'],
    'Row3': ['Z', 'X', 'C', 'V', 'B', 'N', 'M'],
    'Numbers': ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0'],
    'Actions': ['␣ Space', '⌫ Backspace', '⇧ Shift', '?', '!', '.', ',']
}

def translate_text_gemini(text: str) -> dict:
    """Translate text using Gemini AI with improved prompt for accurate translations."""
    try:
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            return {"success": False, "translated_text": None, "error": "Please configure Gemini API key first"}
        
        configure(api_key=api_key)
        model = GenerativeModel("gemini-2.5-flash")
        chat = model.start_chat(history=[])
        
        # Improved prompt that focuses on meaning over transliteration
        prompt = f"""You are a professional Telugu to English translator. Your task is to translate the following Telugu text to natural, fluent English.

IMPORTANT: 
- Focus on the MEANING, not just transliteration
- Translate what the text MEANS in English
- Do NOT just transliterate Telugu sounds
- Provide natural English that a native speaker would use

Telugu text: {text}

English translation (meaning-based):"""
        
        response = chat.send_message(prompt)
        
        if response and response.text:
            # Extract just the translation part
            translated_text = response.text.strip()
            if "English translation" in translated_text:
                translated_text = translated_text.split("English translation")[-1].strip()
                if ":" in translated_text:
                    translated_text = translated_text.split(":", 1)[-1].strip()
            
            return {
                "success": True,
                "translated_text": translated_text,
                "source_lang": "te",
                "dest_lang": "en",
                "error": None
            }
        else:
            return {"success": False, "translated_text": None, "error": "Failed to get response from Gemini API"}
            
    except Exception as e:
        return {"success": False, "translated_text": None, "error": f"Gemini API error: {str(e)}"}

def translate_english_to_telugu(text: str) -> dict:
    """Translate English text to Telugu using Gemini AI."""
    try:
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            return {"success": False, "translated_text": None, "error": "Please configure Gemini API key first"}
        
        configure(api_key=api_key)
        model = GenerativeModel("gemini-2.5-flash")
        chat = model.start_chat(history=[])
        
        # Prompt for English to Telugu translation
        prompt = f"""You are a professional English to Telugu translator. Your task is to translate the following English text to natural, fluent Telugu.

IMPORTANT: 
- Translate the meaning accurately to Telugu
- Use proper Telugu grammar and vocabulary
- Provide natural Telugu that a native speaker would use
- Do NOT just transliterate English sounds

English text: {text}

Telugu translation:"""
        
        response = chat.send_message(prompt)
        
        if response and response.text:
            # Extract just the translation part
            translated_text = response.text.strip()
            if "Telugu translation:" in translated_text:
                translated_text = translated_text.split("Telugu translation:")[-1].strip()
            
            return {
                "success": True,
                "translated_text": translated_text,
                "source_lang": "en",
                "dest_lang": "te",
                "error": None
            }
        else:
            return {"success": False, "translated_text": None, "error": "Failed to get response from Gemini API"}
            
    except Exception as e:
        return {"success": False, "translated_text": None, "error": f"Gemini API error: {str(e)}"}

def translate_text(text: str, dest_lang: str = 'en') -> dict:
    """Translate text to destination language using available APIs."""
    # Try Gemini API first (better quality)
    gemini_result = translate_text_gemini(text)
    if gemini_result["success"]:
        return gemini_result
    
    # Fallback to Google Translate if Gemini fails
    try:
        translator = Translator()
        result = translator.translate(text, dest=dest_lang)
        return {
            "success": True,
            "translated_text": result.text,
            "source_lang": result.src,
            "dest_lang": dest_lang,
            "error": None
        }
    except Exception as e:
        return {
            "success": False,
            "translated_text": None,
            "source_lang": None,
            "dest_lang": dest_lang,
            "error": f"Translation failed: {str(e)}"
        }

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
.main .block-container { padding-top: 2rem; padding-bottom: 2rem; max-width: 900px; }
h1 { color: #1e3a5f; font-weight: 700; text-align: center; margin-bottom: 0.5rem; }
.subtitle { color: #64748b; font-size: 1rem; text-align: center; margin-bottom: 2rem; }
.success-box { background: linear-gradient(135deg, #d1fae5 0%, #a7f3d0 100%);
  border-left: 4px solid #059669; padding: 1.25rem; border-radius: 8px; margin: 1rem 0; }
.error-box { background: linear-gradient(135deg, #fee2e2 0%, #fecaca 100%);
  border-left: 4px solid #dc2626; padding: 1.25rem; border-radius: 8px; margin: 1rem 0; }
.confidence-bar { background: #e2e8f0; border-radius: 10px; height: 12px; margin: 0.5rem 0; overflow: hidden; }
.confidence-fill { height: 100%; background: linear-gradient(90deg, #3b82f6, #06b6d4); border-radius: 10px; transition: width 0.5s ease; }
.keyboard-container { background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 8px; padding: 0.75rem; margin: 1rem 0; }
.keyboard-row { display: flex; gap: 0.2rem; margin-bottom: 0.2rem; justify-content: center; flex-wrap: wrap; }
.keyboard-btn { background: #ffffff; border: 1px solid #d1d5db; border-radius: 4px; padding: 0.4rem 0.6rem; font-size: 0.9rem; cursor: pointer; transition: all 0.2s; min-width: 2rem; text-align: center; font-weight: 500; }
.keyboard-btn:hover { background: #3b82f6; color: white; transform: translateY(-1px); }
.keyboard-btn.space { min-width: 6rem; }
.keyboard-btn.backspace { min-width: 3rem; background: #fef3c7; }
.keyboard-btn.backspace:hover { background: #f59e0b; }
.tab-container { border-bottom: 2px solid #e2e8f0; margin-bottom: 1rem; }
.tab-btn { background: none; border: none; padding: 0.75rem 1.5rem; font-weight: 600; color: #64748b; cursor: pointer; transition: all 0.2s; }
.tab-btn.active { color: #1e3a5f; border-bottom: 2px solid #3b82f6; }
.translation-box { background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%); border-left: 4px solid #3b82f6; padding: 1.25rem; border-radius: 8px; margin: 1rem 0; }
</style>
""", unsafe_allow_html=True)

# =============================================================================
# MAIN INTERFACE
# =============================================================================
st.markdown("# 🌐 Language Detection & Translation System")
st.markdown('<p class="subtitle">Detect languages, type in Telugu with virtual keyboard, and translate to English.</p>', unsafe_allow_html=True)

# Tab navigation
col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
with col1:
    if st.button("🔍 Detection", key="detect_tab", use_container_width=True):
        st.session_state.active_tab = "detection"
with col2:
    if st.button("⌨️ Telugu Keyboard", key="keyboard_tab", use_container_width=True):
        st.session_state.active_tab = "keyboard"
with col3:
    if st.button("🔤 English Keyboard", key="english_keyboard_tab", use_container_width=True):
        st.session_state.active_tab = "english_keyboard"
with col4:
    if st.button("🔄 Translation", key="translation_tab", use_container_width=True):
        st.session_state.active_tab = "translation"

# Initialize session state
if "active_tab" not in st.session_state:
    st.session_state.active_tab = "detection"
if "telugu_text" not in st.session_state:
    st.session_state.telugu_text = ""
if "english_text" not in st.session_state:
    st.session_state.english_text = ""
if "translation_history" not in st.session_state:
    st.session_state.translation_history = []
if "gemini_api_key" not in st.session_state:
    st.session_state.gemini_api_key = os.getenv("GEMINI_API_KEY", "")
if "use_gemini" not in st.session_state:
    st.session_state.use_gemini = False

# Configure Gemini API with the key from environment
if st.session_state.gemini_api_key:
    try:
        configure(api_key=st.session_state.gemini_api_key)
    except Exception as e:
        st.error(f"Gemini API configuration failed: {str(e)}")

# Detection Tab
if st.session_state.active_tab == "detection":

    st.markdown("### 🔍 Language Detection")
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

# Telugu Keyboard Tab
elif st.session_state.active_tab == "keyboard":

    st.markdown("### ⌨️ Telugu Virtual Keyboard - Auto Translation")
    
    # Display current text
    st.markdown("**Current Telugu Text:**")
    if st.session_state.telugu_text:
        st.markdown(f'<div style="background: #f0f9ff; border: 1px solid #0ea5e9; padding: 1rem; border-radius: 8px; font-size: 1.2rem; text-align: center;">{st.session_state.telugu_text}</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div style="background: #f8fafc; border: 1px solid #e2e8f0; padding: 1rem; border-radius: 8px; text-align: center; color: #64748b;">Click buttons below to start typing...</div>', unsafe_allow_html=True)
    
    # Auto-translation settings
    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        auto_translate = st.checkbox("🔄 Auto-Translate", value=False, help="Automatically translate Telugu text to English (disabled by default)")
    with col2:
        min_chars = st.number_input("Min characters", value=5, min_value=1, max_value=20, help="Minimum characters before auto-translation")
    with col3:
        translate_delay = st.number_input("Delay (seconds)", value=3, min_value=1, max_value=10, help="Delay between translations to avoid API limits")
    
    # Smart auto-translate logic - only translate when text ends with space or has complete words
    if auto_translate and len(st.session_state.telugu_text.strip()) >= min_chars:
        # Check if text ends with space (complete word) or contains punctuation
        telugu_text = st.session_state.telugu_text.strip()
        should_translate = (
            telugu_text.endswith(' ') or  # Ends with space (complete word)
            telugu_text.endswith('.') or   # Ends with period
            telugu_text.endswith('?') or   # Ends with question mark  
            telugu_text.endswith('!') or   # Ends with exclamation mark
            '  ' in telugu_text or         # Contains double space (sentence end)
            len(telugu_text.split()) >= 3  # Has at least 3 words
        )
        
        if should_translate:
            # Check if we should translate (avoid too frequent API calls)
            current_time = time.time()
            last_translation_time = st.session_state.get('last_translation_time', 0)
            if current_time - last_translation_time >= translate_delay:
                with st.spinner("Translating with Gemini AI..."):
                    translation_result = translate_text_gemini(telugu_text)
                    if translation_result["success"]:
                        st.session_state.last_translation = translation_result
                        st.session_state.last_translation_time = current_time
                        st.rerun()
    
    st.markdown("**Click the buttons below to type in Telugu:**")
    
    # Virtual keyboard with improved layout
    st.markdown('<div class="keyboard-container">', unsafe_allow_html=True)
    
    for row_name, keys in telugu_keyboard.items():
        if row_name == 'Actions':
            st.markdown(f"**{row_name}:**")
            cols = st.columns([1, 1])
            for i, key in enumerate(keys):
                with cols[i]:
                    if "Space" in key:
                        if st.button("␣", key=f"space_btn", use_container_width=True, help="Add Space"):
                            st.session_state.telugu_text += " "
                            st.rerun()
                    elif "Backspace" in key:
                        if st.button("⌫", key=f"backspace_btn", use_container_width=True, help="Delete Last Character"):
                            if st.session_state.telugu_text:
                                st.session_state.telugu_text = st.session_state.telugu_text[:-1]
                            st.rerun()
        else:
            st.markdown(f"**{row_name}:**")
            cols = st.columns([1] * len(keys))
            for i, key in enumerate(keys):
                with cols[i]:
                    # Create unique key for each button using hash
                    btn_key = f"btn_{row_name}_{i}_{hash(key)}"
                    if st.button(key, key=btn_key, use_container_width=True):
                        st.session_state.telugu_text += key
                        st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Action buttons
    col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
    with col1:
        if st.button("🗑️ Clear All", use_container_width=True):
            st.session_state.telugu_text = ""
            st.rerun()
    with col2:
        if st.button("🔄 Translate Now", use_container_width=True, type="primary"):
            if st.session_state.telugu_text.strip():
                with st.spinner("Translating..."):
                    translation_result = translate_text(st.session_state.telugu_text, 'en')
                    st.session_state.last_translation = translation_result
                    st.session_state.last_translation_time = time.time()
                    st.rerun()
    with col3:
        if st.button("📋 Copy Text", use_container_width=True):
            if st.session_state.telugu_text:
                # Use JavaScript to copy to clipboard
                st.markdown(f"""
                <script>
                navigator.clipboard.writeText('{st.session_state.telugu_text}');
                </script>
                """, unsafe_allow_html=True)
                st.success("Text copied to clipboard!")
    with col4:
        if st.button("🔍 Detect", use_container_width=True):
            if st.session_state.telugu_text.strip():
                result = detect_language(st.session_state.telugu_text)
                st.session_state.detection_result = result
                st.rerun()
    
    # Show automatic translation if available
    if hasattr(st.session_state, 'last_translation') and st.session_state.last_translation:
        result = st.session_state.last_translation
        if result["success"]:
            st.markdown("### 🔄 Live Translation")
            st.markdown(f"""
                <div class="translation-box">
                    <strong>Telugu:</strong> {st.session_state.telugu_text}<br><br>
                    <strong>English:</strong> {result['translated_text']}
                </div>
            """, unsafe_allow_html=True)
        else:
            st.error(f"Translation Error: {result['error']}")
    
    # Show detection result if available
    if hasattr(st.session_state, 'detection_result') and st.session_state.detection_result:
        result = st.session_state.detection_result
        if result["success"]:
            st.markdown(f"""
            <div class="success-box">
                <strong>Detected Language:</strong> {result['primary_lang']}<br>
                <strong>Confidence:</strong> {round(result['primary_confidence']*100)}%
            </div>
            """, unsafe_allow_html=True)
        else:
            st.error(f"Detection Error: {result['error']}")
    
    # Instructions
    st.markdown("---")
    st.markdown("**Instructions:**")
    st.markdown("1. Click Telugu character buttons to type")
    st.markdown("2. 🔄 Auto-Translate is OFF by default (enable if needed)")
    st.markdown("3. Use ␣ for spaces and ⌫ to delete")
    st.markdown("4. Click 🔄 **Translate Now** to translate your text")
    st.markdown("5. Translation only happens when you click the button")
    st.markdown("6. Adjust settings if you enable auto-translation")

# English Keyboard Tab
elif st.session_state.active_tab == "english_keyboard":

    st.markdown("### 🔤 English to Telugu Translation")
    
    # Text input area for English
    english_input = st.text_area("Type your English text here:",
                                   placeholder="Type your English text here and click translate to convert to Telugu...",
                                   height=150,
                                   key="english_input_area")
    
    # Update session state with input
    if english_input != st.session_state.get("english_text", ""):
        st.session_state.english_text = english_input
    
    # Display current English text
    if st.session_state.english_text:
        st.markdown(f'<div style="background: #f0f9ff; border: 1px solid #0ea5e9; padding: 1rem; border-radius: 8px; font-size: 1.2rem; text-align: center;">{st.session_state.english_text}</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div style="background: #f8fafc; border: 1px solid #e2e8f0; padding: 1rem; border-radius: 8px; text-align: center; color: #64748b;">Start typing English text above...</div>', unsafe_allow_html=True)
    
    # Action buttons
    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        if st.button("🔄 Translate to Telugu", use_container_width=True, type="primary"):
            if st.session_state.english_text.strip():
                with st.spinner("Translating to Telugu..."):
                    translation_result = translate_english_to_telugu(st.session_state.english_text)
                    st.session_state.last_english_translation = translation_result
                    st.session_state.last_english_translation_time = time.time()
                    st.rerun()
    with col2:
        if st.button("🗑️ Clear Text", use_container_width=True):
            st.session_state.english_text = ""
            st.rerun()
    with col3:
        if st.button("📋 Copy Text", use_container_width=True):
            if st.session_state.english_text:
                st.markdown(f"""
                <script>
                navigator.clipboard.writeText('{st.session_state.english_text}');
                </script>
                """, unsafe_allow_html=True)
                st.success("Text copied to clipboard!")
    
    # Show translation result if available
    if hasattr(st.session_state, 'last_english_translation') and st.session_state.last_english_translation:
        result = st.session_state.last_english_translation
        if result["success"]:
            st.markdown("### 🔄 Translation Result")
            st.markdown(f"""
                <div class="translation-box">
                    <strong>English:</strong> {st.session_state.english_text}<br><br>
                    <strong>Telugu:</strong> {result['translated_text']}
                </div>
            """, unsafe_allow_html=True)
        else:
            st.error(f"Translation Error: {result['error']}")
    
    # Instructions
    st.markdown("---")
    st.markdown("**Instructions:**")
    st.markdown("1. Type English text in the text area above")
    st.markdown("2. Click 🔄 **Translate to Telugu** to convert")
    st.markdown("3. Translation only happens when you click the button")
    st.markdown("4. Use Clear Text to start over")
    st.markdown("5. Copy Text to copy your English input")

# Translation Tab
elif st.session_state.active_tab == "translation":
    st.markdown("### 🔄 Telugu to English Translation")
    
    # Input text area
    translation_input = st.text_area("Enter Telugu text to translate:",
                                   placeholder="నమస్కారం ఎలా ఉన్నారు? (Type your Telugu text here...)",
                                   height=100,
                                   key="translation_input")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        translate_button = st.button("🔄 Translate to English", use_container_width=True, type="primary")
    
    if translate_button and translation_input:
        with st.spinner("Translating..."):
            translation_result = translate_text(translation_input, 'en')
            
            if translation_result["success"]:
                st.markdown("### ✅ Translation Result")
                st.markdown(f"""
                    <div class="translation-box">
                        <strong>Original ({translation_result['source_lang']}):</strong><br>
                        {translation_input}<br><br>
                        <strong>Translation (English):</strong><br>
                        {translation_result['translated_text']}
                    </div>
                """, unsafe_allow_html=True)
                
                # Add to history
                history_entry = {
                    "original": translation_input,
                    "translated": translation_result["translated_text"],
                    "source_lang": translation_result["source_lang"],
                    "timestamp": str(st.session_state.get('current_time', ''))
                }
                st.session_state.translation_history.append(history_entry)
                
            else:
                st.markdown("### ❌ Translation Error")
                st.markdown(f'<div class="error-box"><strong>{translation_result["error"]}</strong></div>', unsafe_allow_html=True)
    
    # Translation History
    if st.session_state.translation_history:
        st.markdown("### 📜 Translation History")
        for i, entry in enumerate(reversed(st.session_state.translation_history[-5:])):
            with st.expander(f"Translation {i+1} ({entry['source_lang']} → en)"):
                st.write(f"**Original:** {entry['original']}")
                st.write(f"**Translation:** {entry['translated']}")

# =============================================================================
# SIDEBAR
# =============================================================================
with st.sidebar:
    st.markdown("### 🔧 Gemini API Configuration")
    
    # Show API status
    if st.session_state.gemini_api_key:
        st.success("🟢 Gemini API is configured")
        st.caption("Using improved translation model")
    else:
        st.warning("🟡 Please enter Gemini API key")
    
    st.markdown("---")
    st.markdown("### 📋 Supported Languages")
    for code in sorted(LANGUAGE_NAMES.keys()):
        st.caption(f"• {code} → {LANGUAGE_NAMES[code]}")
    st.markdown("---")
    st.caption("Built with Python & Streamlit | Gemini AI 2.5 Flash")
