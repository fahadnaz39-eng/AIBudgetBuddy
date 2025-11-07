# Financial Advisor Chatbot

A Streamlit-based chatbot powered by Google's Gemini AI that provides financial advice and guidance.

## Features

- Personal financial advice
- Budgeting guidance
- Debt management strategies
- Saving and investment tips
- Interactive chat interface

## Setup on Hugging Face Spaces

1. Fork this space
2. Add your Gemini API key as a secret:
   - Go to Settings → Secrets
   - Add `GEMINI_API_KEY` with your actual API key
3. The app will automatically deploy

## Local Development

```bash
pip install -r requirements.txt
streamlit run app.py
