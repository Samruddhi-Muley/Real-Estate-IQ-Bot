# 🏠 RealEstate IQ Bot

An **AI-powered interactive quiz platform** for learning Real Estate concepts — focused on **Property Listings, valuation, compliance, and strategy**.

Built using **Python, Streamlit, and Groq (Llama 3.3 70B)**, this app delivers **real-time AI explanations**, tracks user performance, and enables **personalized learning paths**.

---

## 🚀 Key Features

### 🧠 AI-Powered Learning

* Each answer is evaluated using **Llama 3.3 70B (via Groq API)**
* Instant feedback with:

  * ✅ Correct/Incorrect result
  * 📌 Key concept
  * 🤖 Detailed explanation
  * 💼 Practical pro tip

---

### 🎯 Personalized Quiz Experience

* Select:

  * Topics (7 real estate domains)
  * Difficulty (Beginner / Intermediate / Advanced)
* Dynamic filtering ensures **targeted practice**

---

### ⏱️ Timed Quiz System

* 30-second countdown per question
* Auto-submit on timeout
* Visual timer (🟢🟡🔴 urgency indicator)

---

### 📊 Performance Analytics Dashboard

After each quiz:

* Accuracy score & grade
* Topic-wise performance breakdown
* Difficulty-level analysis
* Full answer review with explanations

---

### 🔁 Weak Topic Re-Quiz (Adaptive Learning)

* Automatically detects weak areas (<60%)
* Generates a **focused re-quiz** on those topics
* Helps users improve efficiently

---

### 🗂️ Persistent User History (SQLite Integration)

* Login system (username-based)
* Stores:

  * Quiz attempts
  * Scores
  * Topic performance
* View **progress over time**
* Data persists across sessions

---

## 🏗️ Project Architecture

```
real_estate_bot/
├── app.py                # Streamlit UI + routing + screens
├── session_manager.py    # Quiz state, scoring, progression logic
├── database.py           # SQLite DB (users, attempts, responses)
├── evaluator.py          # Groq AI evaluation engine
├── question_bank.py      # Questions (topics + difficulty)
├── config.py             # API key config
├── .env                  # Secret keys (excluded from Git)
├── requirements.txt
└── README.md
```

---

## 🔄 Application Flow

```
Login Screen
    ↓
Welcome Screen
    ↓
Filter Selection (Topics + Difficulty)
    ↓
Quiz Engine (Timed Questions)
    ↓
AI Evaluation (Groq LLM)
    ↓
Instant Feedback (Explanation + Tips)
    ↓
Summary Dashboard
    ↓
 ├── Retake Full Quiz
 └── Practice Weak Topics
```

---

## ⚙️ Setup Instructions

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/Samruddhi-Muley/Real-Estate-IQ-Bot
cd real_estate_bot
```

---

### 2️⃣ Create Virtual Environment

```bash
python -m venv venv

# Activate
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac/Linux
```

---

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 4️⃣ Add Groq API Key

Create a `.env` file:

```
GROQ_API_KEY=your_api_key_here
```

Get your key from: https://console.groq.com

---

### 5️⃣ Run the Application

```bash
streamlit run app.py
```

Open in browser:
👉 http://localhost:8501

---

## 🧪 How to Use

1. Enter your **username**
2. Customize quiz:

   * Select topics
   * Select difficulty
3. Answer timed questions
4. Review AI-generated explanations
5. Analyze performance
6. Retry weak areas or full quiz

---

## 🗄️ Database Design (SQLite)

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

## 📈 Example Use Cases

* 📚 Students preparing for real estate exams
* 🧑‍💼 Professionals revising domain concepts
* 🤖 Learning how LLMs can power educational tools
* 📊 Demonstrating full-stack AI + analytics projects

---

## ⚡ Performance & Limits (Groq Free Tier)

| Metric       | Value  |
| ------------ | ------ |
| Requests/min | 30     |
| Requests/day | 14,400 |
| Tokens/min   | 6,000  |
| Cost         | Free   |

---

## 🛠️ Tech Stack

| Layer      | Technology               |
| ---------- | ------------------------ |
| Frontend   | Streamlit                |
| Backend    | Python                   |
| AI Engine  | Llama 3.3 70B (Groq API) |
| Database   | SQLite                   |
| State Mgmt | Streamlit session_state  |
| Config     | python-dotenv            |

---

## 🔍 Future Improvements

* [ ] User authentication (email/password)
* [ ] Leaderboard system
* [ ] Export results (PDF/CSV)
* [ ] Analytics charts (graphs)
* [ ] Deploy on Streamlit Cloud / AWS
* [ ] Multi-domain quiz support

---

## ⚠️ Troubleshooting

| Issue            | Solution                          |
| ---------------- | --------------------------------- |
| API key error    | Check `.env` file                 |
| Module not found | `pip install -r requirements.txt` |
| Rate limit       | Wait a few seconds                |
| DB not created   | Ensure `init_db()` runs           |

---

## 📌 Notes

* `.db` file is excluded via `.gitignore`
* No external DB required (fully local)
* Lightweight and deployable

---

## 👨‍💻 Author

Built as an **AI + Full-Stack Learning Project** demonstrating:

* LLM integration
* Stateful applications
* Data persistence
* Adaptive learning systems

---

## ⭐ If you found this useful

Give it a star ⭐ on GitHub — it helps others discover the project!
