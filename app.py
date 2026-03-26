# app.py
# ------------------------------------------------
# Main Streamlit application entry point.
# Run with:  streamlit run app.py
# ------------------------------------------------

import streamlit as st
from pdf_generator import generate_pdf
from datetime import datetime
from evaluator import evaluate_answer

from session_manager import (
    init_session, get_current_question, record_result,
    advance_question, get_progress, get_final_stats, reset_quiz,
    apply_filters, start_weak_topics_requiz    # ADD start_weak_topics_requiz
)

from question_bank import TOPICS, DIFFICULTIES

from database import (
    init_db, register_user, login_user, save_attempt,
    get_user_history, get_historical_weak_topics,
    delete_user_data
)
init_db()   # creates tables on first run, no-op after that


QUESTION_TIME_LIMIT = 30   # seconds per question

# ── PAGE CONFIG ──────────────────────────────────────────────────────────
st.set_page_config(
    page_title="RealEstate IQ Bot",
    page_icon="🏠",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ── CUSTOM CSS ───────────────────────────────────────────────────────────
st.markdown("""
<style>
    /* Main container */
    .block-container { max-width: 780px; padding-top: 2rem; }

    /* Topic badge */
    .topic-badge {
        display: inline-block;
        background: #EEF2FF;
        color: #4338CA !important;
        font-size: 0.75rem;
        font-weight: 600;
        padding: 3px 10px;
        border-radius: 20px;
        margin-bottom: 0.5rem;
    }

    /* Difficulty badge */
    .diff-beginner    { background:#D1FAE5; color:#065F46 !important; }
    .diff-intermediate{ background:#FEF3C7; color:#92400E !important; }
    .diff-advanced    { background:#FFE4E6; color:#9F1239 !important; }

    /* Question card */
    .question-card {
        background: #F8FAFC;
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        padding: 1.5rem 1.75rem;
        margin: 1rem 0;
        color: #1E293B !important;
    }

    /* Result feedback box */
    .correct-box {
        background: #D1FAE5;
        border-left: 4px solid #10B981;
        border-radius: 8px;
        padding: 1rem 1.25rem;
        margin: 0.75rem 0;
        color: #064E3B !important;
    }
    .correct-box b { color: #064E3B !important; }

    .wrong-box {
        background: #FEE2E2;
        border-left: 4px solid #EF4444;
        border-radius: 8px;
        padding: 1rem 1.25rem;
        margin: 0.75rem 0;
        color: #7F1D1D !important;
    }
    .wrong-box b { color: #7F1D1D !important; }

    /* Explanation box */
    .explanation-box {
        background: #EFF6FF;
        border: 1px solid #BFDBFE;
        border-radius: 8px;
        padding: 1rem 1.25rem;
        margin: 0.75rem 0;
        font-size: 0.93rem;
        line-height: 1.6;
        color: #1E3A5F !important;
    }
    .explanation-box b { color: #1E3A5F !important; }

    /* Pro tip */
    .pro-tip {
        background: #FFFBEB;
        border: 1px solid #FDE68A;
        border-radius: 8px;
        padding: 0.8rem 1.25rem;
        margin: 0.5rem 0;
        font-size: 0.88rem;
        color: #78350F !important;
    }
    .pro-tip b { color: #78350F !important; }

    /* Score card on summary */
    .score-big {
        font-size: 3.5rem;
        font-weight: 700;
        text-align: center;
        line-height: 1;
    }

    /* Topic row in summary */
    .topic-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 0.5rem 0;
        border-bottom: 1px solid #F1F5F9;
        font-size: 0.9rem;
    }
</style>
""", unsafe_allow_html=True)


# ── INITIALIZE SESSION ───────────────────────────────────────────────────
init_session()

# ════════════════════════════════════════════════════════════════════════
# the login screen function
# ════════════════════════════════════════════════════════════════════════


def show_login():
    st.markdown("## 🏠 RealEstate IQ Bot")
    st.markdown("##### *AI-powered Property Listings Assessment*")
    st.divider()

    # Tab switcher — Login vs Register
    tab1, tab2 = st.tabs(["🔑  Login", "📝  Register"])

    # ── LOGIN TAB ────────────────────────────────────────────────────────
    with tab1:
        st.markdown("#### Welcome back")
        login_user_input = st.text_input(
            "Username", key="login_username",
            placeholder="Enter your username"
        )
        login_pass_input = st.text_input(
            "Password", type="password",
            key="login_password",
            placeholder="Enter your password"
        )

        if st.button("🔑  Login", type="primary",
                     use_container_width=True,
                     key="btn_login"):
            if not login_user_input.strip() or not login_pass_input:
                st.error("Please enter both username and password.")
            else:
                result = login_user(login_user_input, login_pass_input)
                if result["success"]:
                    st.session_state.user_id = result["user_id"]
                    st.session_state.username = result["username"]
                    st.session_state.phase = "welcome"
                    st.rerun()
                else:
                    st.error(f"❌ {result['error']}")

    # ── REGISTER TAB ─────────────────────────────────────────────────────
    with tab2:
        st.markdown("#### Create a new account")
        st.markdown("Your quiz history will be saved so you can "
                    "track your progress over time.")

        reg_username = st.text_input(
            "Choose a username", key="reg_username",
            placeholder="e.g. Sam",
            max_chars=30
        )
        reg_pass = st.text_input(
            "Choose a password", type="password",
            key="reg_password",
            placeholder="Min. 4 characters"
        )
        reg_pass_confirm = st.text_input(
            "Confirm password", type="password",
            key="reg_password_confirm",
            placeholder="Repeat your password"
        )

        if st.button("📝  Create Account", type="primary",
                     use_container_width=True,
                     key="btn_register"):
            if not reg_username.strip():
                st.error("Please enter a username.")
            elif len(reg_pass) < 4:
                st.error("Password must be at least 4 characters.")
            elif reg_pass != reg_pass_confirm:
                st.error("Passwords do not match.")
            else:
                result = register_user(reg_username, reg_pass)
                if result["success"]:
                    st.session_state.user_id = result["user_id"]
                    st.session_state.username = reg_username.strip()
                    st.session_state.phase = "welcome"
                    st.success("✅ Account created! Redirecting...")
                    st.rerun()
                else:
                    st.error(f"❌ {result['error']}")


# ════════════════════════════════════════════════════════════════════════
# WELCOME SCREEN
# ════════════════════════════════════════════════════════════════════════
def show_welcome():
    name = st.session_state.get("username", "")
    # ── Logout button top right ───────────────────────────────────────────
    col_title, col_logout = st.columns([5, 1])
    with col_title:
        st.markdown(f"## 🏠 Welcome back, {name}!" if name
                    else "## 🏠 RealEstate IQ Bot")
        st.markdown("##### *AI-powered Property Listings Assessment*")
    with col_logout:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🚪 Logout", key="btn_logout",
                     use_container_width=True):
            st.session_state.pop("user_id", None)
            st.session_state.pop("username", None)
            st.session_state.phase = "login"
            st.rerun()

    st.divider()

    col1, col2, col3 = st.columns(3)
    col1.metric("📋 Questions", "20")
    col2.metric("🏷️ Topics", "7")
    col3.metric("🤖 Powered by", "Groq AI")

    st.markdown("""
    **What you'll be tested on:**
    - MLS & Listing Basics
    - Listing Agreements (Exclusive, Open, Net)
    - Property Valuation & CMAs
    - Disclosure Requirements
    - Listing Price Strategy
    - Property Types & Zoning
    - Listing Descriptions & Fair Housing

    > 💡 After each answer, Groq AI (Llama 3.3 70B) will give you a **detailed explanation** — so you learn whether you're right or wrong.
    """)

    st.divider()
    if st.button("🚀  Start Quiz", type="primary", use_container_width=True):
        st.session_state.phase = "filter"
        st.rerun()
    if st.button("📈  View My History",
                 use_container_width=True,
                 key="btn_view_history"):
        st.session_state.phase = "history"
        st.rerun()

    st.divider()
    if st.button("🚀  Start Quiz", type="primary",
                 use_container_width=True,
                 key="btn_start_quiz"):
        st.session_state.phase = "filter"
        st.rerun()


# ════════════════════════════════════════════════════════════════════════
# QUIZ SCREEN
# ════════════════════════════════════════════════════════════════════════
def show_quiz():
    import time

    question = get_current_question()
    if question is None:
        st.session_state.phase = "summary"
        st.rerun()
        return

    progress = get_progress()

    # ── Start timer when question first loads ────────────────────────────
    if st.session_state.question_start_time is None:
        st.session_state.question_start_time = time.time()

    # ── Calculate time remaining ─────────────────────────────────────────
    elapsed = time.time() - st.session_state.question_start_time
    time_remaining = max(0, QUESTION_TIME_LIMIT - int(elapsed))

    # ── Header ───────────────────────────────────────────────────────────
    st.markdown("### 🏠 RealEstate IQ Bot")
    st.progress(progress["percent"],
                text=f"Question {progress['done'] + 1} of {progress['total']}")
    # ── NEW: re-quiz mode banner ──────────────────────────────────────────
    if len(st.session_state.selected_topics) < 7:  # not all topics = filtered
        topics_str = ", ".join(st.session_state.selected_topics)
        st.info(f"🎯 Re-quiz mode — practising: **{topics_str}**")

    # ── Timer bar ────────────────────────────────────────────────────────
    if not st.session_state.answer_submitted:
        timer_ratio = time_remaining / QUESTION_TIME_LIMIT

        # colour shifts green → amber → red as time runs out
        if timer_ratio > 0.5:
            colour = "🟢"
        elif timer_ratio > 0.25:
            colour = "🟡"
        else:
            colour = "🔴"

        timer_placeholder = st.empty()
        timer_placeholder.progress(
            timer_ratio,
            text=f"{colour}  {time_remaining}s remaining"
        )

    # ── Badges ───────────────────────────────────────────────────────────
    diff = question["difficulty"]
    diff_color = {"beginner": "diff-beginner",
                  "intermediate": "diff-intermediate",
                  "advanced": "diff-advanced"}.get(diff, "")
    st.markdown(
        f'<span class="topic-badge">{question["topic"]}</span> '
        f'<span class="topic-badge {diff_color}">{diff.capitalize()}</span>',
        unsafe_allow_html=True
    )

    # ── Question card ────────────────────────────────────────────────────
    st.markdown(
        f'<div class="question-card"><b>Q{progress["done"] + 1}.</b> '
        f'{question["question"]}</div>',
        unsafe_allow_html=True
    )

    # ── Handle time expiry ───────────────────────────────────────────────
    if time_remaining == 0 and not st.session_state.answer_submitted:
        st.session_state.time_expired = True
        # auto-submit with no answer selected
        result = evaluate_answer(question, "X")   # "X" matches nothing → wrong
        result["user_answer"] = "⏰ Time expired"
        result["is_correct"] = False
        result["score"] = 0
        record_result(result, question)
        st.session_state.answer_submitted = True
        st.session_state.phase = "result"
        st.rerun()

    # ── Answer options ───────────────────────────────────────────────────
    if not st.session_state.answer_submitted:
        options = question["options"]
        chosen = st.radio(
            "Choose your answer:",
            options=list(options.keys()),
            format_func=lambda k: f"{k})  {options[k]}",
            index=None,
            key=f"radio_{question['id']}"
        )

        submit = st.button("✅  Submit Answer", type="primary",
                           use_container_width=True,
                           disabled=(chosen is None))

        if submit and chosen:
            with st.spinner("🤖 Groq AI is evaluating your answer..."):
                result = evaluate_answer(question, chosen)
                result["user_answer"] = chosen
                record_result(result, question)
                st.session_state.answer_submitted = True
                st.session_state.phase = "result"
            st.rerun()

        # ── Auto-rerun every second to update the countdown ──────────────
        import time as t
        t.sleep(1)
        st.rerun()

    # ── Result panel ─────────────────────────────────────────────────────
    if st.session_state.answer_submitted and st.session_state.last_result:
        # Show time expired warning if applicable
        if st.session_state.time_expired:
            st.markdown(
                '<div class="wrong-box">⏰ <b>Time expired!</b> '
                'You ran out of time for this question.</div>',
                unsafe_allow_html=True
            )
        show_result_panel(st.session_state.last_result)

# ════════════════════════════════════════════════════════════════════════
# RESULT PANEL (inline, after answer)
# ════════════════════════════════════════════════════════════════════════
def show_result_panel(result: dict):
    is_correct = result["is_correct"]

    # ── Correct / Wrong Banner ───────────────────────────────────────────
    if is_correct:
        st.markdown(
            f'<div class="correct-box">✅ <b>Correct!</b> &nbsp; Score: <b>{result["score"]}</b>/100</div>',
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            f'<div class="wrong-box">❌ <b>Incorrect.</b> &nbsp; '
            f'Correct answer: <b>{result["correct_answer"]}</b></div>',
            unsafe_allow_html=True
        )

    # ── Key Concept ──────────────────────────────────────────────────────
    st.markdown(f"**📌 Key Concept:** {result.get('key_concept', '')}")

    # ── AI Explanation ───────────────────────────────────────────────────
    st.markdown(
        f'<div class="explanation-box">🤖 <b>Groq AI Explanation</b><br><br>{result["explanation"]}</div>',
        unsafe_allow_html=True
    )

    # ── Pro Tip ──────────────────────────────────────────────────────────
    st.markdown(
        f'<div class="pro-tip">💼 <b>Pro Tip:</b> {result["pro_tip"]}</div>',
        unsafe_allow_html=True
    )

    st.divider()

    # ── Next Button ──────────────────────────────────────────────────────
    progress = get_progress()
    is_last = (progress["done"] + 1) >= progress["total"]
    btn_label = "📊  View Final Results" if is_last else "➡️  Next Question"

    if st.button(btn_label, type="primary", use_container_width=True):
        advance_question()
        if is_last:
            st.session_state.phase = "summary"
        st.rerun()


def show_filter():
    st.markdown("### 🎯 Customize Your Quiz")
    st.markdown("Select the topics and difficulty levels you want to practice.")
    st.divider()

    # ── Topic selector ───────────────────────────────────────────────────
    st.markdown("**📚 Topics** — pick one or more")
    col1, col2 = st.columns(2)
    selected_topics = []
    for i, topic in enumerate(sorted(TOPICS)):
        col = col1 if i % 2 == 0 else col2
        default = topic in st.session_state.selected_topics
        if col.checkbox(topic, value=default, key=f"topic_{topic}"):
            selected_topics.append(topic)

    st.markdown("**🎓 Difficulty** — pick one or more")
    col1, col2, col3 = st.columns(3)
    diff_cols = {"beginner": col1, "intermediate": col2, "advanced": col3}
    selected_difficulties = []
    for diff in DIFFICULTIES:
        default = diff in st.session_state.selected_difficulties
        if diff_cols[diff].checkbox(diff.capitalize(), value=default, key=f"diff_{diff}"):
            selected_difficulties.append(diff)

    # Live count of how many questions match
    from question_bank import QUESTIONS
    matching = [
        q for q in QUESTIONS
        if q["topic"] in selected_topics
        and q["difficulty"] in selected_difficulties
    ]
    st.divider()
    if matching:
        st.info(f"✅ {len(matching)} question(s) match your filters.")
    else:
        st.error("⚠️ No questions match. Please select at least one topic and one difficulty.")

    if st.button("🚀  Start Quiz", type="primary",
                 use_container_width=True, disabled=(len(matching) == 0)):
        st.session_state.selected_topics = selected_topics
        st.session_state.selected_difficulties = selected_difficulties
        success = apply_filters()
        if success:
            st.session_state.phase = "quiz"
            st.rerun()


# ════════════════════════════════════════════════════════════════════════
# SUMMARY / RESULTS SCREEN
# ════════════════════════════════════════════════════════════════════════
def show_summary():
    stats = get_final_stats()
    accuracy = stats["accuracy"]

    # ── Save to DB once per attempt ──────────────────────────────────────
    if (st.session_state.get("user_id")
            and not st.session_state.get("attempt_saved", False)):
        save_attempt(
            user_id=st.session_state.user_id,
            stats=stats,
            selected_topics=st.session_state.selected_topics,
            selected_difficulties=st.session_state.selected_difficulties,
        )
        st.session_state.attempt_saved = True

    # ── Grade ────────────────────────────────────────────────────────────
    if accuracy >= 90:
        grade, emoji, color = "A", "🏆", "#059669"
    elif accuracy >= 75:
        grade, emoji, color = "B", "⭐", "#0284C7"
    elif accuracy >= 60:
        grade, emoji, color = "C", "📘", "#D97706"
    else:
        grade, emoji, color = "D", "📖", "#DC2626"

    st.markdown(f"## {emoji} Quiz Complete!")
    st.divider()

    # ── Score Overview ───────────────────────────────────────────────────
    col1, col2, col3 = st.columns(3)
    col1.metric("✅ Correct", f"{stats['correct']} / {stats['total_questions']}")
    col2.metric("🎯 Accuracy", f"{accuracy:.1f}%")
    col3.metric("🏅 Grade", grade)

    # ── Topic Breakdown ──────────────────────────────────────────────────
    st.markdown("### 📊 Topic Breakdown")
    for topic, data in stats["topic_scores"].items():
        pct = (data["correct"] / data["total"] * 100) if data["total"] > 0 else 0
        col_a, col_b = st.columns([3, 1])
        col_a.write(f"**{topic}**")
        col_b.write(f"{data['correct']}/{data['total']} ({pct:.0f}%)")
        st.progress(pct / 100)

    # ── Weak Areas ───────────────────────────────────────────────────────
    if stats["weak_topics"]:
        st.markdown("### 🔴 Areas to Review")
        for t in stats["weak_topics"]:
            st.warning(f"📚 {t} — scored below 60%. Consider revisiting this topic.")

    # ── Difficulty Breakdown ─────────────────────────────────────────────
    st.markdown("### 🎓 Difficulty Breakdown")
    dcols = st.columns(3)
    labels = ["beginner", "intermediate", "advanced"]
    emojis = ["🟢", "🟡", "🔴"]
    for i, (d, em) in enumerate(zip(labels, emojis)):
        data = stats["difficulty_breakdown"][d]
        pct = (data["c"] / data["t"] * 100) if data["t"] > 0 else 0
        dcols[i].metric(f"{em} {d.capitalize()}", f"{data['c']}/{data['t']} ({pct:.0f}%)")

    # ── Answer History Expander ──────────────────────────────────────────
    st.markdown("### 📋 Answer Review")
    for i, h in enumerate(stats["history"], 1):
        icon = "✅" if h["is_correct"] else "❌"
        with st.expander(f"{icon} Q{i}: {h['question'][:70]}..."):
            st.write(f"**Your answer:** {h['user_answer']}")
            st.write(f"**Correct answer:** {h['correct_answer']}")
            st.markdown(
                f'<div class="explanation-box">{h["explanation"]}</div>',
                unsafe_allow_html=True
            )
            st.markdown(f'<div class="pro-tip">💼 {h["pro_tip"]}</div>',
                        unsafe_allow_html=True)

    # ── Past Attempts History ────────────────────────────────────────────
    user_id = st.session_state.get("user_id")
    if user_id:
        history = get_user_history(user_id)
        if len(history) > 1:   # only show if more than current attempt
            st.markdown("### 📈 Your Progress Over Time")
            for i, attempt in enumerate(history):
                attempt_label = (
                    f"Attempt {len(history) - i} — "
                    f"{attempt['attempted_at'][:16].replace('T', ' ')} — "
                    f"Accuracy: {attempt['accuracy']:.1f}% "
                    f"({attempt['correct_count']}/{attempt['total_questions']})"
                )
                st.write(attempt_label)

    # ↑ for loop ends here — notice the dedent below
    
    # ── Button section ───────────────────────────────────────────────────

    # ── PDF Download ─────────────────────────────────────────────────────
    username = st.session_state.get("username", "User")
    pdf_bytes = generate_pdf(username, stats)
    filename = f"RealEstate_IQ_{username}_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf"

    st.download_button(
        label="📄  Download My Report (PDF)",
        data=pdf_bytes,
        file_name=filename,
        mime="application/pdf",
        use_container_width=True,
        key="btn_download_pdf"
    )

    st.divider()

    weak = stats["weak_topics"]

    if weak:
        st.markdown("### 🎯 Ready to improve?")
        weak_list = ", ".join(weak)
        st.markdown(
            f'<div class="wrong-box">📉 You scored below 60% in: '
            f'<b>{weak_list}</b><br><br>'
            f'The re-quiz below will focus <b>only</b> on these topics '
            f'across all difficulty levels.</div>',
            unsafe_allow_html=True
        )
        st.markdown("")

        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔁  Practice Weak Topics",
                         type="primary",
                         use_container_width=True,
                         key="btn_weak_requiz"):
                start_weak_topics_requiz()
                st.rerun()
        with col2:
            if st.button("🔄  Retake Full Quiz",
                         use_container_width=True,
                         key="btn_retake_full"):
                reset_quiz()
                st.rerun()

    else:
        st.success("🏆 Great job! You scored above 60% in all topics.")
        if st.button("🔄  Retake Quiz",
                     type="primary",
                     use_container_width=True,
                     key="btn_retake_clean"):
            reset_quiz()
            st.rerun()

def show_history():
    username = st.session_state.get("username", "User")
    user_id  = st.session_state.get("user_id")

    st.markdown(f"### 📈 {username}'s Quiz History")
    st.divider()

    history = get_user_history(user_id)

    if not history:
        st.info("You haven't completed any quizzes yet. "
                "Take your first quiz to see your history here!")
    else:
        # Summary stats across all attempts
        all_accuracies = [h["accuracy"] for h in history]
        best  = max(all_accuracies)
        avg   = sum(all_accuracies) / len(all_accuracies)

        col1, col2, col3 = st.columns(3)
        col1.metric("🗂️ Total Attempts", len(history))
        col2.metric("🏆 Best Accuracy",  f"{best:.1f}%")
        col3.metric("📊 Average Accuracy", f"{avg:.1f}%")

        st.markdown("### All Attempts")
        for i, attempt in enumerate(history):
            date_str = attempt["attempted_at"][:16].replace("T", " ")
            label = (
                f"Attempt {len(history) - i} — {date_str} — "
                f"{attempt['accuracy']:.1f}% "
                f"({attempt['correct_count']}/{attempt['total_questions']})"
            )
            st.write(f"**{label}**")
            st.progress(attempt["accuracy"] / 100)

    st.divider()

    # ── Delete data option ────────────────────────────────────────────────
    with st.expander("⚠️ Danger Zone"):
        st.warning("Deleting your data is permanent and cannot be undone.")
        confirm = st.text_input(
            f"Type your username **{username}** to confirm deletion:",
            key="delete_confirm_input"
        )
        if st.button("🗑️ Delete All My Data",
                     type="primary",
                     key="btn_delete_data"):
            if confirm == username:
                delete_user_data(user_id)
                for key in list(st.session_state.keys()):
                    del st.session_state[key]
                st.success("All your data has been deleted.")
                st.rerun()
            else:
                st.error("Username does not match. Deletion cancelled.")

    if st.button("← Back", key="btn_history_back"):
        st.session_state.phase = "welcome"
        st.rerun()

# ════════════════════════════════════════════════════════════════════════
# ROUTER — pick screen based on phase
# ════════════════════════════════════════════════════════════════════════
phase = st.session_state.get("phase", "login")   # default is now "login"

if phase == "login":
    show_login()
elif phase == "welcome":
    show_welcome()
elif phase == "filter":
    show_filter()
elif phase in ("quiz", "result"):
    show_quiz()
elif phase == "summary":
    show_summary()
elif phase == "history":
    show_history()
