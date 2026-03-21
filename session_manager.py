# session_manager.py
# ------------------------------------------------
# Manages all quiz state in Streamlit's session_state.
# Tracks: score, history, weak topics, question order.
# ------------------------------------------------

import random
import streamlit as st
from question_bank import QUESTIONS, TOPICS, DIFFICULTIES


def init_session():
    """Initialize session state if starting fresh."""
    if "initialized" not in st.session_state:
        st.session_state.initialized = True
        st.session_state.selected_topics = TOPICS.copy()
        st.session_state.selected_difficulties = DIFFICULTIES.copy()
        st.session_state.questions = []        
        st.session_state.current_index = 0
        st.session_state.total_score = 0
        st.session_state.history = []
        st.session_state.topic_scores = {}
        st.session_state.phase = "welcome"
        st.session_state.last_result = None
        st.session_state.answer_submitted = False
        #timer keys
        st.session_state.question_start_time = None
        st.session_state.time_expired = False

def apply_filters():
    """
    Call this when the user clicks Start Quiz on the filter screen.
    Filters QUESTIONS by selected topics + difficulties, shuffles, saves to session.
    """
    filtered = [
        q for q in QUESTIONS
        if q["topic"] in st.session_state.selected_topics
        and q["difficulty"] in st.session_state.selected_difficulties
    ]
    if not filtered:
        return False   # caller should show a warning
    st.session_state.questions = random.sample(filtered, len(filtered))
    st.session_state.current_index = 0
    st.session_state.total_score = 0
    st.session_state.history = []
    st.session_state.topic_scores = {}
    st.session_state.last_result = None
    st.session_state.answer_submitted = False
    return True
    

def get_current_question() -> dict | None:
    """Returns the current question or None if quiz is done."""
    idx = st.session_state.current_index
    if idx < len(st.session_state.questions):
        return st.session_state.questions[idx]
    return None


def record_result(result: dict, question_data: dict):
    """Save evaluation result and update topic scores."""
    topic = question_data["topic"]

    if topic not in st.session_state.topic_scores:
        st.session_state.topic_scores[topic] = {"correct": 0, "total": 0}

    st.session_state.topic_scores[topic]["total"] += 1
    if result["is_correct"]:
        st.session_state.topic_scores[topic]["correct"] += 1

    st.session_state.total_score += result["score"]
    st.session_state.history.append({
        "question": question_data["question"],
        "topic": topic,
        "difficulty": question_data["difficulty"],
        "user_answer": result.get("user_answer", ""),
        "correct_answer": result["correct_answer"],
        "is_correct": result["is_correct"],
        "score": result["score"],
        "explanation": result["explanation"],
        "pro_tip": result["pro_tip"],
    })
    st.session_state.last_result = result


def advance_question():
    """Move to the next question."""
    st.session_state.current_index += 1
    st.session_state.phase = "quiz"
    st.session_state.answer_submitted = False
    st.session_state.last_result = None
    # ── NEW: reset timer for next question ───────────
    st.session_state.question_start_time = None
    st.session_state.time_expired = False


def get_progress() -> dict:
    """Returns progress stats for the progress bar."""
    total = len(st.session_state.questions)
    done = st.session_state.current_index
    return {
        "done": done,
        "total": total,
        "percent": done / total if total > 0 else 0,
    }


def get_weak_topics() -> list[str]:
    """Returns topics where the user scored below 60%."""
    weak = []
    for topic, data in st.session_state.topic_scores.items():
        if data["total"] > 0:
            pct = data["correct"] / data["total"]
            if pct < 0.6:
                weak.append(topic)
    return weak

def start_weak_topics_requiz():
    """
    Resets the quiz session but pre-filters questions
    to only the topics the user scored below 60% in.
    Called when the user clicks 'Practice Weak Topics'.
    """
    weak = get_weak_topics()

    # Filter questions to weak topics only, all difficulties
    filtered = [
        q for q in QUESTIONS
        if q["topic"] in weak
    ]

    # Reset everything except we keep topic_scores for
    # historical reference — overwrite only quiz state
    st.session_state.questions = random.sample(filtered, len(filtered))
    st.session_state.current_index = 0
    st.session_state.total_score = 0
    st.session_state.history = []
    st.session_state.topic_scores = {}
    st.session_state.phase = "quiz"
    st.session_state.last_result = None
    st.session_state.answer_submitted = False
    st.session_state.question_start_time = None
    st.session_state.time_expired = False
    st.session_state.selected_topics = weak     # reflects what's being quizzed
    st.session_state.selected_difficulties = ["beginner", "intermediate", "advanced"]

def get_final_stats() -> dict:
    """Returns aggregated stats for the summary screen."""
    history = st.session_state.history
    total_q = len(history)
    correct_q = sum(1 for h in history if h["is_correct"])
    avg_score = st.session_state.total_score / total_q if total_q > 0 else 0

    difficulty_breakdown = {"beginner": {"c": 0, "t": 0},
                             "intermediate": {"c": 0, "t": 0},
                             "advanced": {"c": 0, "t": 0}}
    for h in history:
        d = h["difficulty"]
        difficulty_breakdown[d]["t"] += 1
        if h["is_correct"]:
            difficulty_breakdown[d]["c"] += 1

    return {
        "total_questions": total_q,
        "correct": correct_q,
        "incorrect": total_q - correct_q,
        "accuracy": (correct_q / total_q * 100) if total_q > 0 else 0,
        "avg_score": avg_score,
        "topic_scores": st.session_state.topic_scores,
        "difficulty_breakdown": difficulty_breakdown,
        "weak_topics": get_weak_topics(),
        "history": history,
    }


def reset_quiz():
    """Wipe session and restart."""
    for key in list(st.session_state.keys()):
        del st.session_state[key]
