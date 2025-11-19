# llm.py
import os
import json
from datetime import datetime
from openai import OpenAI

# ================================
#  API KEY HANDLING
# ================================
api_key = os.getenv("OPENAI_API_KEY")

# Fallback for Streamlit Cloud
if not api_key:
    try:
        import streamlit as st
        api_key = st.secrets["OPENAI_API_KEY"]
    except Exception:
        raise ValueError(
            "OPENAI_API_KEY not found. Set it in Replit secrets or Streamlit secrets."
        )

client = OpenAI(api_key=api_key)


# ================================
#  MONTHLY USAGE LIMIT PROTECTION
# ================================
USAGE_LIMIT = 200     # ≈ $1–$2 per month on gpt-4.1-mini
USAGE_FILE = "usage_counter.txt"


def check_usage_limit():
    """Protects you from unwanted API overuse."""
    if not os.path.exists(USAGE_FILE):
        with open(USAGE_FILE, "w") as f:
            f.write("0")

    # Read current usage
    with open(USAGE_FILE, "r") as f:
        count = int(f.read().strip())

    if count >= USAGE_LIMIT:
        raise ValueError(
            "⚠️ Monthly usage limit reached. "
            "This prevents accidental API overcharges. "
            "Try again next month or increase the limit in llm.py."
        )

    # Increment usage count
    with open(USAGE_FILE, "w") as f:
        f.write(str(count + 1))


# ================================
#  CAPSULE GENERATOR
# ================================
def generate_capsule_simple(mode: str,
                            roles: list[str],
                            course_topic: str | None = None) -> dict:
    """
    Generates concept capsules & quiz questions using GPT-4.1-mini.
    Falls back to GPT-3.5-turbo if needed.
    """
    # Enforce usage limit
    check_usage_limit()

    roles_text = ", ".join(roles) if roles else "Product Manager"
    course_topic_text = course_topic or "none specified"

    # ----- SYSTEM PROMPT -----
    system_prompt = """
You are Anamnesis AI — a personal learning and memory co-pilot.

Your job:
- Explain ONE concept clearly and briefly.
- Generate TWO quiz questions.
- Keep responses simple, practical, and recall-friendly.

Return ONLY valid JSON like:
{
  "concept": "...",
  "questions": [
    {"question": "...", "expected_answer": "..."}
  ]
}
"""

    # ----- USER PROMPT -----
    user_prompt = f"""
User target roles: {roles_text}
Mode: {mode}
Selected course/topic: {course_topic_text}

Rules:
- If mode="career": pick a concept useful for their target roles.
- If mode="course": refresh the given course/topic.
- If mode="mix": pick something relevant to both career and course review.
"""

    # ================================
    #  PRIMARY MODEL: GPT-4.1-MINI
    # ================================
    try:
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {"role": "system", "content": system_prompt.strip()},
                {"role": "user", "content": user_prompt.strip()},
            ],
            response_format={"type": "json_object"},
            temperature=0.7,
        )

    # ================================
    #  FALLBACK MODEL: GPT-3.5-TURBO
    # ================================
    except Exception as e:
        print("⚠️ Warning: gpt-4.1-mini failed, falling back to gpt-3.5-turbo.\n", e)

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt.strip()},
                {"role": "user", "content": user_prompt.strip()},
            ],
            response_format={"type": "json_object"},
            temperature=0.7,
        )

    return json.loads(response.choices[0].message.content)


# ================================
#  QUIZ EVALUATOR (simple keyword match)
# ================================
def evaluate_answer_simple(user_answer: str, expected_answer: str) -> bool:
    """
    Simple keyword-overlap evaluation.
    (We can upgrade this to an LLM evaluator later.)
    """
    if not user_answer or not expected_answer:
        return False

    user = user_answer.lower()
    expected = expected_answer.lower()

    tokens = [t for t in expected.split() if len(t) > 3]

    if not tokens:
        return False

    match_count = sum(1 for t in tokens if t in user)

    return match_count >= 1

