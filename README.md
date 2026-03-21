# RealEstate IQ Bot

An AI-powered educational quiz bot for the Real Estate domain, focused on Property Listings.
Built with **Python + Streamlit + Groq API (Llama 3.3 70B)**.

---

## 📁 Project Structure

```
real_estate_bot/
├── app.py                # Streamlit UI — main entry point
├── question_bank.py      # 20 property listing questions across 7 topics
├── evaluator.py          # Groq API evaluation + retry logic
├── session_manager.py    # Quiz state, filters, scoring, progress tracking
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

---

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

---

### Step 3 — Add Your API Key

1. Open the `.env` file in PyCharm
2. Replace `your_groq_api_key_here` with your actual key:

```
GROQ_API_KEY=gsk_XXXXXXXXXXXXXXXXXXXX
```

3. Save the file

---

### Step 4 — Verify the Key Works

```bash
python -c "
from groq import Groq
client = Groq(api_key='gsk_your_key_here')
r = client.chat.completions.create(model='llama-3.3-70b-versatile', messages=[{'role':'user','content':'Say hello'}])
print('SUCCESS:', r.choices[0].message.content)
"
```

---

### Step 5 — Run the App

```bash
streamlit run app.py
```

👉 Opens at: **http://localhost:8501**

---

## 🚀 New Feature: Personalized Quiz (Step 2)

The quiz now includes a **filter screen** before starting, allowing users to:

* Select **topics**
* Select **difficulty levels** (Beginner / Intermediate / Advanced)

👉 The quiz dynamically filters questions based on user selection, enabling **focused and personalized learning**.

---

## How the App Works

```
Welcome Screen
     ↓
Filter Screen (NEW 🚀)
  - Select Topics
  - Select Difficulty
     ↓
Filtered Quiz Starts
     ↓
User selects A/B/C/D and clicks Submit
     ↓
Groq AI (Llama 3.3 70B) evaluates the answer
     ↓
Shows: ✅/❌ result + score + key concept + explanation + pro tip
     ↓
Next Question → ... → after filtered questions
     ↓
Summary Dashboard (accuracy, topic breakdown, weak areas, full review)
     ↓
Retake Quiz (returns to Welcome)
```

---

## 🧪 How to Test the New Feature

1. Run the app
2. Click **Start Quiz** → Filter screen appears
3. Select topics & difficulty
4. Start quiz → only selected questions appear
5. Complete quiz → view summary
6. Click **Retake Quiz** → returns to Welcome

---

## ⚡ Free Tier Limits (Groq — Llama 3.3 70B)

| Limit               | Value  |
| ------------------- | ------ |
| Requests per minute | 30     |
| Requests per day    | 14,400 |
| Tokens per minute   | 6,000  |
| Cost                | Free   |

Each quiz question = 1 API call. So 14,400 RPD = **720 full quizzes per day** for free.
This is ~14x more generous than Gemini's free tier was.

---

## Troubleshooting

| Problem                              | Fix                                   |
| ------------------------------------ | ------------------------------------- |
| `ValueError: Groq API key not found` | Check your `.env` file                |
| `429 rate_limit_exceeded`            | Wait 10–15 seconds                    |
| `ModuleNotFoundError: groq`          | Run `pip install groq`                |
| `ModuleNotFoundError: streamlit`     | Run `pip install -r requirements.txt` |
| App error                            | Use `streamlit run app.py`            |
| `.env` issue                         | Ensure correct filename               |

---

## Next Steps to Extend the Project

* [x] Add countdown timer per question
* [x] Add "Weak Topics Re-Quiz" mode
* [ ] Store score history in database
* [ ] Export results as PDF
* [ ] Add user authentication
* [ ] Deploy on Streamlit Cloud

---

## Tech Stack

| Layer    | Technology               |
| -------- | ------------------------ |
| UI       | Streamlit                |
| AI Model | Llama 3.3 70B (via Groq) |
| Language | Python 3.10+             |
| State    | Streamlit session_state  |
| Config   | python-dotenv            |
| IDE      | PyCharm                  |

```
```
