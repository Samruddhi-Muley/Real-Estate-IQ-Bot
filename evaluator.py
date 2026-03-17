# evaluator.py
# ------------------------------------------------
# Sends the user's answer to Gemini and gets back:
#   - is_correct (bool)
#   - score (0-100)
#   - explanation (rich contextual feedback)
#   - key_concept (the core idea being tested)
# Includes retry logic for free-tier rate limits.
# ------------------------------------------------

import time
import json
from config import CLIENT, GROQ_MODEL


def evaluate_answer(question_data: dict, user_answer: str) -> dict:
    correct_key = question_data["correct"]
    correct_text = question_data["options"][correct_key]
    user_text = question_data["options"].get(user_answer, "No answer selected")
    is_correct = (user_answer == correct_key)

    prompt = f"""
You are an expert real estate educator evaluating a student's quiz answer.

QUESTION:
{question_data['question']}

OPTIONS:
A) {question_data['options']['A']}
B) {question_data['options']['B']}
C) {question_data['options']['C']}
D) {question_data['options']['D']}

CORRECT ANSWER: {correct_key}) {correct_text}
STUDENT'S ANSWER: {user_answer}) {user_text}
TOPIC: {question_data['topic']}
DIFFICULTY: {question_data['difficulty']}
EDUCATOR HINT: {question_data['hint']}

The student answered {"CORRECTLY" if is_correct else "INCORRECTLY"}.

Respond ONLY with a valid JSON object. No markdown, no code fences, no extra text.
Exactly these fields:
{{
  "is_correct": {str(is_correct).lower()},
  "score": <integer, 90 if correct else 0>,
  "key_concept": "<one sentence naming the core concept being tested>",
  "explanation": "<3-5 sentences: if wrong, explain WHY the student choice was wrong and WHY the correct answer is right, with a real-world property listing example. If correct, give a deeper insight.>",
  "pro_tip": "<one practical tip a real estate professional would give about this topic>"
}}
"""

    return _call_groq_with_retry(prompt, question_data, is_correct, correct_key, correct_text)


def _call_groq_with_retry(prompt, question_data, is_correct, correct_key, correct_text,
                           retries=3, delay=15):
    for attempt in range(retries):
        try:
            response = CLIENT.chat.completions.create(
                model=GROQ_MODEL,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3,
            )
            raw = response.choices[0].message.content.strip()

            # Strip markdown fences if model wraps in them
            if raw.startswith("```"):
                raw = raw.split("```")[1]
                if raw.startswith("json"):
                    raw = raw[4:]
            raw = raw.strip()

            result = json.loads(raw)
            result.setdefault("is_correct", is_correct)
            result.setdefault("score", 90 if is_correct else 0)
            result.setdefault("key_concept", question_data["topic"])
            result.setdefault("explanation", "See the correct answer above.")
            result.setdefault("pro_tip", "Always review current local regulations.")
            result["correct_answer"] = f"{correct_key}) {correct_text}"
            return result

        except json.JSONDecodeError:
            return _fallback(is_correct, correct_key, correct_text,
                             "Could not parse AI response. Correct answer is shown above.")

        except Exception as e:
            error_str = str(e)
            if "429" in error_str or "rate_limit" in error_str.lower():
                if attempt < retries - 1:
                    time.sleep(delay * (attempt + 1))
                    continue
                return _fallback(is_correct, correct_key, correct_text,
                                 "⚠️ Rate limit hit. Please wait a moment and try again.")
            return _fallback(is_correct, correct_key, correct_text,
                             f"❌ API Error: {error_str}")

    return _fallback(is_correct, correct_key, correct_text, "All retries exhausted.")


def _fallback(is_correct, correct_key, correct_text, message):
    return {
        "is_correct": is_correct,
        "score": 90 if is_correct else 0,
        "key_concept": "See correct answer",
        "explanation": message,
        "pro_tip": "Review real estate fundamentals regularly.",
        "correct_answer": f"{correct_key}) {correct_text}"
    }