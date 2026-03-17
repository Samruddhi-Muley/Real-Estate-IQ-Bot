# config.py
# ------------------------------------------------
# Loads environment variables and configures the
# Google Gemini API client.
# ------------------------------------------------

import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY or GROQ_API_KEY == "your_groq_api_key_here":
    raise ValueError(
        "\n\n❌ Groq API key not found!\n"
        "   1. Go to https://console.groq.com\n"
        "   2. Sign up for free (no credit card needed)\n"
        "   3. Click API Keys → Create API Key\n"
        "   4. Open .env and set GROQ_API_KEY=your_key\n"
    )

# Single shared Groq client
CLIENT = Groq(api_key=GROQ_API_KEY)

# Free model — fast, capable, no billing required
GROQ_MODEL = "llama-3.3-70b-versatile"