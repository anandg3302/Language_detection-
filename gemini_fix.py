# Fixed Gemini translation function
def translate_with_gemini_improved(text: str) -> dict:
    """Translate text using Gemini AI with better prompt for accurate translations."""
    try:
        from google.generativeai import GenerativeModel, configure
        import os
        from dotenv import load_dotenv
        
        load_dotenv()
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

# Test the function
if __name__ == "__main__":
    test_text = "నమస్కారం ఎలా ఉన్నారు"
    result = translate_with_gemini_improved(test_text)
    print(f"Telugu: {test_text}")
    print(f"English: {result['translated_text']}")
    print(f"Success: {result['success']}")
    if not result['success']:
        print(f"Error: {result['error']}")
