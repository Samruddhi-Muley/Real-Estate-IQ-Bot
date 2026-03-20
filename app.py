# app.py
# ------------------------------------------------
# Main Streamlit application entry point.
# Run with:  streamlit run app.py
# ------------------------------------------------

import streamlit as st  
from evaluator import evaluate_answer

from session_manager import (
    init_session, get_current_question, record_result,
    advance_question, get_progress, get_final_stats, reset_quiz,
    apply_filters
)
from question_bank import TOPICS, DIFFICULTIES


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
# WELCOME SCREEN
# ════════════════════════════════════════════════════════════════════════
def show_welcome():
    st.markdown("## 🏠 RealEstate IQ Bot")
    st.markdown("##### *AI-powered Property Listings Assessment*")
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


# ════════════════════════════════════════════════════════════════════════
# QUIZ SCREEN
# ════════════════════════════════════════════════════════════════════════
def show_quiz():
    question = get_current_question()

    # All questions done → go to summary
    if question is None:
        st.session_state.phase = "summary"
        st.rerun()
        return

    progress = get_progress()

    # ── Header ──────────────────────────────────────────────────────────
    st.markdown(f"### 🏠 RealEstate IQ Bot")
    st.progress(progress["percent"],
                text=f"Question {progress['done'] + 1} of {progress['total']}")

    # ── Badges ──────────────────────────────────────────────────────────
    diff = question["difficulty"]
    diff_color = {"beginner": "diff-beginner",
                  "intermediate": "diff-intermediate",
                  "advanced": "diff-advanced"}.get(diff, "")

    st.markdown(
        f'<span class="topic-badge">{question["topic"]}</span> '
        f'<span class="topic-badge {diff_color}">{diff.capitalize()}</span>',
        unsafe_allow_html=True
    )

    # ── Question Card ────────────────────────────────────────────────────
    st.markdown(
        f'<div class="question-card"><b>Q{progress["done"] + 1}.</b> {question["question"]}</div>',
        unsafe_allow_html=True
    )

    # ── Answer Options ───────────────────────────────────────────────────
    if not st.session_state.answer_submitted:
        options = question["options"]
        chosen = st.radio(
            "Choose your answer:",
            options=list(options.keys()),
            format_func=lambda k: f"{k})  {options[k]}",
            index=None,
            key=f"radio_{question['id']}"
        )

        col1, col2 = st.columns([3, 1])
        with col1:
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

    # ── Result Panel (shown after submit) ────────────────────────────────
    if st.session_state.answer_submitted and st.session_state.last_result:
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
        bar_color = "green" if pct >= 60 else "red"
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

    st.divider()
    if st.button("🔄  Retake Quiz", type="primary", use_container_width=True):
        reset_quiz()
        st.rerun()


# ════════════════════════════════════════════════════════════════════════
# ROUTER — pick screen based on phase
# ════════════════════════════════════════════════════════════════════════
phase = st.session_state.get("phase", "welcome")

if phase == "welcome":
    show_welcome()
elif phase == "filter":          
    show_filter()                
elif phase in ("quiz", "result"):
    show_quiz()
elif phase == "summary":
    show_summary()
