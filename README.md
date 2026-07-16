# AuraNews - Intelligent News Summarization & Sentiment Analysis System

A modern, modular NLP and LLM-powered news intelligence dashboard built using Python FastAPI, NLTK, and the Google Gemini API.

This project is structured using the standard MLOps prediction pipeline architecture, ensuring configuration tracking and clean modular code separation.

---

## 🚀 Quick Start Guide (How to Run on Your Laptop)

To share this project, send others the link to your GitHub repository:
👉 **`https://github.com/pranjals2004/text-summerizer-project`**

Here are the step-by-step instructions they need to run to set it up:

### 1. Prerequisites
Ensure you have **Python 3.10 or newer** installed on your laptop. (Fully compatible with Python 3.12, 3.13, and 3.14).

### 2. Clone the Repository
Open a terminal (or Git Bash) and run:
```bash
git clone https://github.com/pranjals2004/text-summerizer-project.git
cd text-summerizer-project
```

### 3. Create & Activate a Virtual Environment
- **On Windows (PowerShell/CMD)**:
  ```powershell
  python -m venv venv
  .\venv\Scripts\activate
  ```
- **On macOS/Linux**:
  ```bash
  python3 -m venv venv
  source venv/bin/activate
  ```

### 4. Install Dependencies
Install all the required python libraries (including FastAPI, Uvicorn, NLTK, python-box, etc.):
```bash
pip install -r requirements.txt
pip install -e .
```

---

## 🏃 How to Start the App

1. **Verify Setup (Pipeline test)**:
   Run the CLI test script to verify imports and folder configurations are working:
   ```bash
   python main.py
   ```

2. **Start the Web Dashboard**:
   Run the FastAPI application server:
   ```bash
   python -m uvicorn app:app --reload --host 127.0.0.1 --port 8000
   ```

3. **Open the Web Browser**:
   Navigate to the following address:
   👉 **[http://127.0.0.1:8000](http://127.0.0.1:8000)**

---

## 🎨 Interactive Dashboard Features
- **Demo Mode**: Includes 4 pre-baked articles (Tech, Space, Green Business, and Deep Sea Science) with complete summaries, emotional ratings, entities, and preloaded Q&A. Works immediately without an API key!
- **Local NLP Mode**: Parses custom pasted text using local NLTK tokenizers, computes readability scores (Flesch-Kincaid Ease index), maps Parts-of-Speech distributions, and generates keyword clouds.
- **Live AI Mode**: Paste your **Gemini API Key** in the settings panel (gear icon) to unlock real-time summaries, detailed emotional scales (Joy, Trust, Fear, Anger, Sadness), structured named-entity extraction, and context-aware conversational Q&A chat for any article.