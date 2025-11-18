# app.py
import random
import streamlit as st
from llm import generate_capsule_simple, evaluate_answer_simple

# ----------------------
# Page config & branding
# ----------------------
st.set_page_config(page_title="Anamnesis — Never forget what you learn.",
                   page_icon="🧠",
                   layout="wide")

st.title("🧠 Anamnesis — Never forget what you learn.")
st.caption("Anamnesis AI — The art of recollection.")

# ----------------------
# Initialize session state
# ----------------------
if "capsule" not in st.session_state:
    st.session_state["capsule"] = None
if "quiz_answers" not in st.session_state:
    st.session_state["quiz_answers"] = []
if "quiz_results" not in st.session_state:
    st.session_state["quiz_results"] = None

# courses: list of dicts
# {
#   "id": int,
#   "name": str,
#   "ctype": str,
#   "status": str,
#   "topics": [
#       {"id": int, "name": str, "notes": str}
#   ]
# }
if "courses" not in st.session_state:
    st.session_state["courses"] = []

# ----------------------
# Sidebar: user profile
# ----------------------
st.sidebar.header("👤 Your Profile")

name = st.sidebar.text_input("Name", value="Neha")
roles = st.sidebar.multiselect(
    "Target roles",
    ["Product Manager", "Supply Chain", "TPM", "Analytics"],
    default=["Product Manager", "Supply Chain"],
)

st.sidebar.markdown("---")
st.sidebar.subheader("📚 Capsule Mode")
mode = st.sidebar.radio(
    "What should Anamnesis focus on today?",
    ["Career focus", "Course review focus", "Mix"],
    index=0,
)

if mode == "Career focus":
    capsule_mode = "career"
elif mode == "Course review focus":
    capsule_mode = "course"
else:
    capsule_mode = "mix"


# ----------------------
# Helper: pick a random course topic
# ----------------------
def pick_random_course_topic() -> str | None:
    courses = st.session_state["courses"]
    topics = []
    for c in courses:
        for t in c["topics"]:
            topics.append((c, t))
    if not topics:
        return None

    course, topic = random.choice(topics)
    label = f"{course['name']} — {topic['name']}"
    return label


# ----------------------
# Main layout: tabs
# ----------------------
tab_capsule, tab_courses, tab_about = st.tabs(
    ["📚 Today's Capsule", "📘 Courses & Topics", "ℹ️ About Anamnesis"])

# ----------------------
# TAB 1: Capsule
# ----------------------
with tab_capsule:
    st.subheader("Today's Learning & Memory Capsule")

    st.write(
        "Click the button below to generate a short concept explanation and two "
        "quiz questions tailored to your target roles. "
        "If you choose *Course review focus*, Anamnesis will try to refresh a topic "
        "from the courses you've added.")

    chosen_course_topic_label = None

    if st.button("✨ Generate Capsule"):
        if not roles:
            st.warning(
                "Please select at least one target role in the sidebar.")
        else:
            # Decide if we should pick a course topic
            course_topic_for_prompt = None
            if capsule_mode == "course":
                course_topic_for_prompt = pick_random_course_topic()
                if course_topic_for_prompt is None:
                    st.warning(
                        "You selected Course review focus, but no courses or topics "
                        "have been added yet. Please add them in the 'Courses & Topics' tab."
                    )
                    st.stop()
            elif capsule_mode == "mix":
                # Optional: sometimes use a course topic if available
                course_topic_for_prompt = pick_random_course_topic()

            with st.spinner("Anamnesis is thinking..."):
                capsule = generate_capsule_simple(
                    capsule_mode, roles, course_topic=course_topic_for_prompt)

            st.session_state["capsule"] = capsule
            st.session_state["quiz_answers"] = [
                "" for _ in capsule.get("questions", [])
            ]
            st.session_state["quiz_results"] = None
            st.session_state["course_topic_used"] = course_topic_for_prompt
            st.success("New capsule generated!")

    capsule = st.session_state["capsule"]

    if capsule:
        # Show which topic was used (if any)
        course_topic_used = st.session_state.get("course_topic_used")
        if course_topic_used:
            st.markdown(f"**📘 Reviewing course topic:** `{course_topic_used}`")

        st.markdown("### 🧩 Concept")
        st.write(capsule.get("concept", ""))

        questions = capsule.get("questions", [])
        if questions:
            st.markdown("### 📝 Quiz")
            answers = st.session_state["quiz_answers"]

            for i, q in enumerate(questions):
                st.markdown(f"**Q{i+1}. {q['question']}**")
                answers[i] = st.text_area(
                    f"Your answer to Q{i+1}",
                    value=answers[i],
                    key=f"answer_{i}",
                    height=80,
                )

            if st.button("✅ Submit Answers"):
                results = []
                for i, q in enumerate(questions):
                    user_ans = answers[i]
                    expected = q["expected_answer"]
                    is_correct = evaluate_answer_simple(user_ans, expected)
                    results.append(
                        (q["question"], expected, user_ans, is_correct))

                st.session_state["quiz_results"] = results
                st.success("Answers submitted! Scroll down for feedback.")

        # Show feedback
        if st.session_state["quiz_results"]:
            st.markdown("### 🔍 Feedback")
            for i, (q_text, expected, user_ans,
                    is_correct) in enumerate(st.session_state["quiz_results"]):
                st.markdown(f"**Q{i+1}. {q_text}**")
                st.write(f"✅ Correct? {'Yes' if is_correct else 'No'}")
                st.write(f"**Your answer:** {user_ans or '_(no answer)_'}")
                st.write(f"**Reference answer:** {expected}")
                st.markdown("---")
    else:
        st.info(
            "Click **✨ Generate Capsule** to start your first session with Anamnesis.\n\n"
            "For course-based review, add your courses and topics in the next tab."
        )

# ----------------------
# TAB 2: Courses & Topics
# ----------------------
with tab_courses:
    st.subheader("📘 Courses & Topics")

    st.write(
        "Add courses you've taken (like Operations Management, Financial Markets, "
        "Competitive Strategy), then add topics under each. "
        "Anamnesis will use these when you choose **Course review focus**.")

    courses = st.session_state["courses"]

    # --- Add new course ---
    st.markdown("### ➕ Add a new course")

    with st.form("add_course_form", clear_on_submit=True):
        course_name = st.text_input(
            "Course name (e.g., Operations Management)")
        course_type = st.selectbox(
            "Type",
            ["University course", "Coursera / online", "Other"],
        )
        course_status = st.selectbox(
            "Status",
            ["Currently taking", "Completed", "Planning to take"],
        )
        add_course_btn = st.form_submit_button("Add course")

    if add_course_btn:
        if not course_name.strip():
            st.warning("Please enter a course name.")
        else:
            new_id = len(courses) + 1
            new_course = {
                "id": new_id,
                "name": course_name.strip(),
                "ctype": course_type,
                "status": course_status,
                "topics": [],
            }
            courses.append(new_course)
            st.session_state["courses"] = courses
            st.success(f"Added course: {course_name.strip()}")

    st.markdown("---")

    # --- Manage topics for a selected course ---
    if courses:
        st.markdown("### 🧩 Add topics to a course")

        course_options = {f"{c['name']} (#{c['id']})": c for c in courses}
        selected_label = st.selectbox(
            "Select a course to manage topics",
            list(course_options.keys()),
        )
        selected_course = course_options[selected_label]

        # Show existing topics
        if selected_course["topics"]:
            st.markdown("#### Existing topics")
            for t in selected_course["topics"]:
                st.write(f"- **{t['name']}** — {t['notes'] or '_no notes_'}")
        else:
            st.info("No topics added yet for this course.")
