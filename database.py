# database.py
# ------------------------------------------------
# All SQLite database logic.
# Handles: table creation, saving attempts,
# fetching history, user management.
# ------------------------------------------------

import hashlib
import sqlite3
import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "real_estate_bot.db")


def get_connection():
    """Returns a database connection with row_factory set
    so columns can be accessed by name."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """
    Creates all tables if they don't exist.
    Safe to call every time the app starts —
    IF NOT EXISTS means it never overwrites data.
    """
    with get_connection() as conn:
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS users (
                id            INTEGER PRIMARY KEY AUTOINCREMENT,
                username      TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL DEFAULT '',
                created_at    DATETIME DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS quiz_attempts (
                id                   INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id              INTEGER REFERENCES users(id),
                attempted_at         DATETIME DEFAULT CURRENT_TIMESTAMP,
                total_score          INTEGER,
                accuracy             REAL,
                total_questions      INTEGER,
                correct_count        INTEGER,
                topics_selected      TEXT,
                difficulties_selected TEXT
            );

            CREATE TABLE IF NOT EXISTS question_responses (
                id             INTEGER PRIMARY KEY AUTOINCREMENT,
                attempt_id     INTEGER REFERENCES quiz_attempts(id),
                question_id    INTEGER,
                topic          TEXT,
                difficulty     TEXT,
                user_answer    TEXT,
                correct_answer TEXT,
                is_correct     INTEGER,
                score          INTEGER,
                explanation    TEXT,
                pro_tip        TEXT
            );
        """)

def _hash_password(password: str) -> str:
    """
    One-way SHA-256 hash of the password.
    We never store the plain text — only the hash.
    """
    return hashlib.sha256(password.encode()).hexdigest()

def register_user(username: str, password: str) -> dict:
    """
    Creates a new user account.
    Returns: {"success": True, "user_id": int}
          or {"success": False, "error": "message"}
    """
    username = username.strip()
    if len(username) < 2:
        return {"success": False,
                "error": "Username must be at least 2 characters."}
    if len(password) < 4:
        return {"success": False,
                "error": "Password must be at least 4 characters."}

    try:
        with get_connection() as conn:
            cursor = conn.execute(
                "INSERT INTO users (username, password_hash) VALUES (?,?)",
                (username, _hash_password(password))
            )
            return {"success": True, "user_id": cursor.lastrowid}
    except sqlite3.IntegrityError:
        return {"success": False,
                "error": f"Username '{username}' is already taken. "
                          f"Please choose another."}


def login_user(username: str, password: str) -> dict:
    """
    Validates credentials.
    Returns: {"success": True, "user_id": int, "username": str}
          or {"success": False, "error": "message"}
    """
    with get_connection() as conn:
        row = conn.execute(
            "SELECT id, username, password_hash FROM users WHERE username=?",
            (username.strip(),)
        ).fetchone()

    if not row:
        return {"success": False,
                "error": "Username not found. Please register first."}

    if row["password_hash"] != _hash_password(password):
        return {"success": False,
                "error": "Incorrect password. Please try again."}

    return {"success": True,
            "user_id": row["id"],
            "username": row["username"]}


def get_all_users() -> list:
    """
    Returns list of all users — useful for an
    admin view if you add one later.
    """
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT id, username, created_at FROM users ORDER BY created_at DESC"
        ).fetchall()
    return [dict(r) for r in rows]

def save_attempt(user_id: int, stats: dict, selected_topics: list,
                 selected_difficulties: list):
    """
    Saves a completed quiz attempt and all its
    question responses in a single transaction.
    Called once when the summary screen loads.
    """
    with get_connection() as conn:
        cursor = conn.execute(
            """INSERT INTO quiz_attempts
               (user_id, total_score, accuracy, total_questions,
                correct_count, topics_selected, difficulties_selected)
               VALUES (?,?,?,?,?,?,?)""",
            (
                user_id,
                stats["avg_score"],
                stats["accuracy"],
                stats["total_questions"],
                stats["correct"],
                json.dumps(selected_topics),
                json.dumps(selected_difficulties),
            )
        )
        attempt_id = cursor.lastrowid

        for h in stats["history"]:
            conn.execute(
                """INSERT INTO question_responses
                   (attempt_id, question_id, topic, difficulty,
                    user_answer, correct_answer, is_correct,
                    score, explanation, pro_tip)
                   VALUES (?,?,?,?,?,?,?,?,?,?)""",
                (
                    attempt_id,
                    h.get("question_id", 0),
                    h["topic"],
                    h["difficulty"],
                    h["user_answer"],
                    h["correct_answer"],
                    int(h["is_correct"]),
                    h["score"],
                    h["explanation"],
                    h["pro_tip"],
                )
            )
    return attempt_id


def get_user_history(user_id: int) -> list:
    """
    Returns all past quiz attempts for a user,
    most recent first.
    """
    with get_connection() as conn:
        rows = conn.execute(
            """SELECT id, attempted_at, accuracy, correct_count,
                      total_questions, topics_selected
               FROM quiz_attempts
               WHERE user_id = ?
               ORDER BY attempted_at DESC""",
            (user_id,)
        ).fetchall()
    return [dict(r) for r in rows]


def get_historical_weak_topics(user_id: int,
                                threshold: float = 0.6) -> list:
    """
    Looks at ALL past attempts for a user and returns
    topics where the overall historical accuracy < threshold.
    Useful for long-term weak area detection.
    """
    with get_connection() as conn:
        rows = conn.execute(
            """SELECT topic,
                      SUM(is_correct) as correct,
                      COUNT(*)        as total
               FROM question_responses qr
               JOIN quiz_attempts qa ON qr.attempt_id = qa.id
               WHERE qa.user_id = ?
               GROUP BY topic""",
            (user_id,)
        ).fetchall()

    weak = []
    for row in rows:
        if row["total"] > 0:
            pct = row["correct"] / row["total"]
            if pct < threshold:
                weak.append(row["topic"])
    return weak


def delete_user_data(user_id: int):
    """
    Permanently deletes all data for a user.
    Cascades: responses → attempts → user.
    """
    with get_connection() as conn:
        conn.execute(
            """DELETE FROM question_responses
               WHERE attempt_id IN
               (SELECT id FROM quiz_attempts WHERE user_id=?)""",
            (user_id,)
        )
        conn.execute(
            "DELETE FROM quiz_attempts WHERE user_id=?", (user_id,)
        )
        conn.execute(
            "DELETE FROM users WHERE id=?", (user_id,)
        )
