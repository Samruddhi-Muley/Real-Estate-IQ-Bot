# 🏠 RealEstate IQ Bot

An AI-powered educational quiz bot for the Real Estate domain, focused on Property Listings.
Built with **Python + Streamlit + Google Gemini API**.

---

## 📁 Project Structure

```
real_estate_bot/
├── app.py                # Streamlit UI — main entry point
├── question_bank.py      # 20 property listing questions across 7 topics
├── evaluator.py          # Gemini API evaluation + retry logic
├── session_manager.py    # Quiz state, scoring, progress tracking
├── config.py             # Gemini API key setup
├── .env                  # Your secret API key (never commit this!)
├── requirements.txt      # Python dependencies
└── README.md
```

---

## ⚙️ Setup Instructions (PyCharm)

### Step 1 — Get Your Free Gemini API Key
1. Go to: https://aistudio.google.com/apikey
2. Sign in with your Google account
3. Click **"Create API Key"**
4. Copy the key (looks like: `AIzaSy...`)

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
2. Replace `your_gemini_api_key_here` with your actual key:
   ```
   GEMINI_API_KEY=AIzaSyXXXXXXXXXXXXXXXXXX
   ```
3. Save the file

### Step 4 — Run the App
In the PyCharm terminal (bottom panel):
```bash
streamlit run app.py
```

Your browser will automatically open at: **http://localhost:8501**

---

## 🎮 How the App Works

```
Welcome Screen
     ↓
Question shown (topic badge + difficulty badge)
     ↓
User selects A/B/C/D and clicks Submit
     ↓
Gemini AI evaluates the answer
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

## ⚡ Free Tier Limits (Gemini 2.0 Flash Lite)

| Limit | Value |
|-------|-------|
| Requests per minute | 15 |
| Requests per day | 1,000 |
| Cost | Free |

Each quiz question = 1 API call. So 1,000 RPD = **50 full quizzes per day** for free.

---

## 🐛 Troubleshooting

| Problem | Fix |
|---------|-----|
| `ValueError: Gemini API key not found` | Check your `.env` file has the real key |
| `429 RESOURCE_EXHAUSTED` | You hit the rate limit — app will auto-retry, just wait 15s |
| `ModuleNotFoundError` | Run `pip install -r requirements.txt` in your venv |
| App opens but shows error | Make sure you're running `streamlit run app.py`, not `python app.py` |

---

## 🚀 Next Steps to Extend the Project

- [ ] Add user login + store history in SQLite
- [ ] Add a "Weak Topics Mode" that only quizzes low-scoring areas
- [ ] Export results as PDF report
- [ ] Add timer per question
- [ ] Add image-based questions (listing photos)
