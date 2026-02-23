# Language Detection App with Python

A mini project that detects the language of user-input text using the `langdetect` library. Features a clean, modern Streamlit GUI with confidence scores and support for 55+ languages.

## Features

- **Language Detection**: Detects the primary language of any text input
- **Confidence Score**: Displays a visual progress bar showing detection confidence
- **Multiple Sentences**: Supports mixed or multi-sentence text; shows alternative language candidates when applicable
- **Error Handling**: Gracefully handles empty input, very short text, and unsupported content
- **Supported Languages List**: Sidebar shows all 55+ detectable languages
- **Modern UI**: Clean design with colored success/error messages and responsive layout

## Requirements

- Python 3.7+
- `langdetect` – language detection
- `streamlit` – web GUI

## Installation

1. **Create a virtual environment** (recommended):

   ```bash
   python -m venv venv
   venv\Scripts\activate   # On Windows
   # source venv/bin/activate   # On macOS/Linux
   ```

2. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

   Or install manually:

   ```bash
   pip install langdetect streamlit
   ```

## How to Run

From the project directory, run:

```bash
streamlit run app.py
```

The app will open in your default browser at `http://localhost:8501`.

## Usage

1. Enter or paste text in the large text area (any language).
2. Click **Detect Language**.
3. View the detected language name, code, and confidence score.
4. For ambiguous text, alternative language suggestions are shown below.

## Project Structure

```
language detection/
├── app.py           # Main application (backend + Streamlit GUI)
├── requirements.txt # Python dependencies
└── README.md        # This file
```

## License

MIT
