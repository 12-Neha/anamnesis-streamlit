# llm.py
import os
from openai import OpenAI

# Read the API key stored in Replit Secrets
import os
from openai import OpenAI

# Try environment variable first (for Replit/local)
api_key = os.getenv("OPENAI_API_KEY")

# Fallback: try Streamlit secrets (for Streamlit Cloud)
if not api_key:
    try:
        import streamlit as st
        api_key = st.secrets["OPENAI_API_KEY"]
    except Exception:
        raise ValueError(
            "OPENAI_API_KEY not found. Set it as an env var (Replit/local) "
            "or in Streamlit secrets."
        )

client = OpenAI(api_key=api_key)
if not api_key:
    raise ValueError("OPENAI_API_KEY not set in Replit Secrets.")

client = OpenAI(api_key=api_key)


def generate_capsule_simple(mode: str,
                            roles: list[str],
                            course_topic: str | None = None) -> dict:
    """
    Anamnesis capsule generator (MVP).

    Parameters
    ----------
    mode : str
        One of: "career", "course", "mix"
    roles : list[str]
        Target roles like ["Product Manager", "Supply Chain"]
    course_topic : str | None
        Optional string describing the course & topic to review,
        e.g. "Operations Management — Little's Law"

    Returns
    -------
    dict
        {
          "concept": str,
          "questions": [
            {"question": str, "expected_answer": str},
            ...
          ]
        }
    """
    roles_text = ", ".join(roles) if roles else "Product Manager"
    course_topic_text = course_topic or "none specified"

    system_prompt = """
You are Anamnesis AI — a personal learning and memory co-pilot.

Your goal is to help the user *remember* and *apply* key concepts for roles
like Product Manager, Supply Chain Analyst, TPM, and Analytics, and to refresh
topics from courses they've already taken.

You must:
- Explain ONE concept clearly and briefly.
- Generate TWO quiz questions about it, with short expected answers.
- Keep it practical and beginner-friendly.
- Focus on understanding and recall, not heavy math.

CRITICAL:
Return ONLY valid JSON with keys:
- "concept": str
- "questions": list of { "question": str, "expected_answer": str }
    """

    user_prompt = f"""
User target roles: {roles_text}
Mode: {mode}
Selected course/topic for review (if any): {course_topic_text}

If mode is "career":
- Focus on a concept that is important for their target roles.

If mode is "course":
- Focus on the given course/topic for review.
- Assume they have seen this concept before in a course and need a refresher.
- Emphasize recall and practical intuition.

If mode is "mix":
- Choose a concept that is relevant both for their roles and as something
  that could reasonably come from a course.

Keep everything short and clear.
    """

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {
                "role": "system",
                "content": system_prompt.strip()
            },
            {
                "role": "user",
                "content": user_prompt.strip()
            },
        ],
        response_format={"type": "json_object"},
        temperature=0.7,
    )

    import json
    return json.loads(response.choices[0].message.content)


def evaluate_answer_simple(user_answer: str, expected_answer: str) -> bool:
    """
    Very naive first-pass evaluation:
    - lowercase both
    - check if at least one keyword from expected answer appears in user answer

    This is just an MVP; later we can replace it with a smarter LLM-based grading.
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
