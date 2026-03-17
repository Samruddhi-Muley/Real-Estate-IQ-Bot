#  RealEstate IQ Bot

An AI-powered educational quiz bot for the Real Estate domain, focused on Property Listings.
Built with **Python + Streamlit + Groq API (Llama 3.3 70B)**.

---

## 📁 Project Structure

```
real_estate_bot/
├── app.py                # Streamlit UI — main entry point
├── question_bank.py      # 20 property listing questions across 7 topics
├── evaluator.py          # Groq API evaluation + retry logic
├── session_manager.py    # Quiz state, scoring, progress tracking
├── config.py             # Groq API key setup
├── .env                  # Your secret API key (never commit this!)
├── .gitignore            # Keeps .env, venv, and cache off GitHub
├── requirements.txt      # Python dependencies
└── README.md
```

---

## ⚙️ Setup Instructions (PyCharm)

### Step 1 — Get Your Free Groq API Key
1. Go to: https://console.groq.com
2. Sign up for free — **no credit card needed**
3. Click **API Keys → Create API Key**
4. Copy the key (looks like: `gsk_...`)

### Step 2 — Open Project in PyCharm
1. Open PyCharm → **File → Open** → select the `real_estate_bot` folder
2. PyCharm will detect `requirements.txt` and suggest creating a virtual environment
3. Click **"Create virtualenv"** and let it install dependencies

   OR manually via terminal:
   ```bash
   python -m venv venv
   venv\Scripts\activate        # Windows
   source venv/bin/activate     # Mac/Linux
   pip install -r requirements.txt
   ```

### Step 3 — Add Your API Key
1. Open the `.env` file in PyCharm
2. Replace `your_groq_api_key_here` with your actual key:
   ```
   GROQ_API_KEY=gsk_XXXXXXXXXXXXXXXXXXXX
   ```
3. Save the file

### Step 4 — Verify the Key Works
Before running the full app, test quickly in the terminal:
```bash
python -c "
from groq import Groq
client = Groq(api_key='gsk_your_key_here')
r = client.chat.completions.create(model='llama-3.3-70b-versatile', messages=[{'role':'user','content':'Say hello'}])
print('SUCCESS:', r.choices[0].message.content)
"
```

### Step 5 — Run the App
In the PyCharm terminal (bottom panel):
```bash
streamlit run app.py
```

Your browser will automatically open at: **http://localhost:8501**

---

##   How the App Works

```
Welcome Screen
     ↓
Question shown (topic badge + difficulty badge)
     ↓
User selects A/B/C/D and clicks Submit
     ↓
Groq AI (Llama 3.3 70B) evaluates the answer
     ↓
Shows: ✅/❌ result + score + key concept + explanation + pro tip
     ↓
Next Question → ... → after 20 questions
     ↓
Summary Dashboard (accuracy, topic breakdown, weak areas, full review)
     ↓
Retake Quiz (reshuffled)
```

---

## ⚡ Free Tier Limits (Groq — Llama 3.3 70B)

| Limit | Value |
|-------|-------|
| Requests per minute | 30 |
| Requests per day | 14,400 |
| Tokens per minute | 6,000 |
| Cost | Free |

Each quiz question = 1 API call. So 14,400 RPD = **720 full quizzes per day** for free.
This is ~14x more generous than Gemini's free tier was.

---

##   Troubleshooting

| Problem | Fix |
|---------|-----|
| `ValueError: Groq API key not found` | Check your `.env` file has the real key starting with `gsk_` |
| `429 rate_limit_exceeded` | Hit the RPM cap — app auto-retries, just wait 15 seconds |
| `ModuleNotFoundError: groq` | Run `pip install groq` in your venv |
| `ModuleNotFoundError: streamlit` | Run `pip install -r requirements.txt` in your venv |
| App opens but shows error | Make sure you're running `streamlit run app.py`, not `python app.py` |
| `.env` not loading | Make sure the file is named `.env` (with the dot), not `env` or `.env.txt` |

---

##   Next Steps to Extend the Project

- [ ] Add topic & difficulty selector before quiz starts
- [ ] Add countdown timer per question
- [ ] Add "Weak Topics Re-Quiz" mode after summary
- [ ] Store score history in SQLite database
- [ ] Export results as a PDF report
- [ ] Add user login for multiple users
- [ ] Deploy on Streamlit Cloud (free, shareable via URL)

---

##   Tech Stack

| Layer | Technology |
|-------|-----------|
| UI | Streamlit |
| AI Model | Llama 3.3 70B (via Groq) |
| Language | Python 3.10+ |
| State | Streamlit session_state |
| Config | python-dotenv |
| IDE | PyCharm |