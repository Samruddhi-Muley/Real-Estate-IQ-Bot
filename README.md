# 🏠 RealEstate IQ Bot

An **AI-powered interactive quiz platform** for learning Real Estate concepts — focused on **Property Listings, valuation, compliance, and strategy**.

Built using **Python, Streamlit, and Groq (Llama 3.3 70B)**, this app delivers **real-time AI explanations**, tracks user performance, and enables **personalized learning paths**.

---

##  Key Features

* AI-Powered Answer Evaluation — Every answer is evaluated by Llama 3.3 70B via Groq
* Contextual Explanation Generation — Deep, domain-specific explanations after every question
* Topic & Difficulty Selection — Users choose what to study before starting
* Weak Topic Detection & Re-Quiz — Automatically routes users back to weak areas
* Question Timer — 30-second countdown per question with auto-submission
* Performance Dashboard — Accuracy, grade, topic and difficulty breakdown
* Multi-User Login System — Register, login, password-protected accounts
* Persistent Score History — SQLite stores all attempts across sessions
* PDF Report Export — Downloadable report with AI explanations for revision

---

##  Project Architecture

```
real_estate_bot/
├── app.py               # Streamlit UI — main entry point, all screens and router
├── question_bank.py     # 20 property listing questions across 7 topics, 3 difficulties
├── evaluator.py         # Groq API evaluation + retry logic + fallback handling
├── session_manager.py   # Quiz state, scoring, weak topic detection, progress tracking
├── config.py            # Groq API key setup and client initialization
├── database.py          # SQLite — users, attempts, responses, history
├── pdf_generator.py     # ReportLab PDF report generation
├── real_estate_bot.db   # SQLite database file (auto-created on first run)
├── .env                 # Your secret API key (never commit this!)
├── .gitignore           # Keeps .env, .db, venv, and cache off GitHub
├── requirements.txt     # Python dependencies
└── README.md
```

---

## 🔄 Application Flow

```
App opens
     ↓
Login / Register screen — credentials verified against SQLite
     ↓
Welcome screen — username shown, past attempt count, navigation
     ↓
Filter screen — select topics and difficulty levels
     ↓
Quiz screen — one question at a time with 30-second timer
     ↓
Each answer → Groq AI evaluates → score + explanation + pro tip
     ↓
After all questions → attempt saved to SQLite automatically
     ↓
Summary dashboard — accuracy, grade, topic breakdown, weak areas
     ↓
Weak topics found → "Practice Weak Topics" re-quiz starts
No weak topics   → "Retake Quiz" or "View History"
     ↓
PDF export — full report downloaded to device
```

---

##  Setup Instructions

### 1️⃣ Get your free Groq API Key
1. Go to: https://console.groq.com
2. Sign up for free — no credit card needed
3. Click API Keys → Create API Key
4. Copy the key (looks like: gsk_...)

---

### 2️⃣ Open Project in Pycharm
1. Open PyCharm → File → Open → select the real_estate_bot folder
2. PyCharm will detect requirements.txt and suggest creating a virtual environment
3. Click "Create virtualenv" and let it install dependencies
OR manually via terminal:

```bash
python -m venv venv
   venv\Scripts\activate        # Windows
   source venv/bin/activate     # Mac/Linux
   pip install -r requirements.txt
```

---

### 3️⃣ Add your API Key
1. Open the .env file in PyCharm
2. Replace your_groq_api_key_here with your actual key:

```bash
GROQ_API_KEY=gsk_XXXXXXXXXXXXXXXXXXXX
```

3. Save the file

---

### 4️⃣ Verify the key works

Before running the full app, test quickly in the terminal:

```
python -c "
from groq import Groq
client = Groq(api_key='gsk_your_key_here')
r = client.chat.completions.create(model='llama-3.3-70b-versatile', messages=[{'role':'user','content':'Say hello'}])
print('SUCCESS:', r.choices[0].message.content)
"
```

---

### 5️⃣ Run the Application

```bash
streamlit run app.py
```

Open in browser:
👉 http://localhost:8501

The SQLite database real_estate_bot.db is created automatically on first run — no setup needed.

---


##  Database Design (SQLite)

### Tables:

* **users**

  * Stores unique usernames

* **quiz_attempts**

  * Stores overall quiz performance

* **question_responses**

  * Stores per-question data:

    * answer
    * correctness
    * explanation
    * score

---

##  Example Use Cases

*  Students preparing for real estate exams
*  Professionals revising domain concepts
*  Learning how LLMs can power educational tools
*  Demonstrating full-stack AI + analytics projects

---

##  Performance & Limits (Groq Free Tier)

| Metric       | Value  |
| ------------ | ------ |
| Requests/min | 30     |
| Requests/day | 14,400 |
| Tokens/min   | 6,000  |
| Cost         | Free   |

---

##  Tech Stack

| Layer      | Technology               |
| ---------- | ------------------------ |
| Frontend   | Streamlit                |
| Backend    | Python                   |
| AI Engine  | Llama 3.3 70B (Groq API) |
| Database   | SQLite                   |
| State Mgmt | Streamlit session_state  |
| Config     | python-dotenv            |

---

##  Future Improvements

* [ ] Deploy on Streamlit Cloud (free, shareable via URL)
* [ ] RAG-based Study Mode using uploaded real estate documents
* [ ] Adaptive difficulty based on historical performance
* [ ] Leaderboard across multiple users
* [ ] Email weekly performance summaries
* [ ] Certification mode with pass/fail and printable certificate

---

##  Troubleshooting

| Issue            | Solution                          |
| ---------------- | --------------------------------- |
| API key error    | Check `.env` file                 |
| Module not found | `pip install -r requirements.txt` |
| Rate limit       | Wait a few seconds                |
| DB not created   | Ensure `init_db()` runs           |

---

##  Notes

* `.db` file is excluded via `.gitignore`
* No external DB required (fully local)
* Lightweight and deployable

---

## Author

Built as an **AI + Full-Stack Learning Project** demonstrating:

* LLM integration
* Stateful applications
* Data persistence
* Adaptive learning systems

---

