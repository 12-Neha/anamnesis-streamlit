✨ Anamnesis — AI Learning & Memory Co-Pilot

Anamnesis is an AI-powered learning companion that helps users learn faster, remember longer, and practice smarter.
It generates concise concept capsules, personalized quiz questions, and adaptive reviews for roles like Product Manager, Supply Chain Analyst, Data Analyst, and TPM.

🌱 Demo Site

👉 https://anamnesis-app-hzggt2wqtaeajcteymjvfa.streamlit.app/

🚀 Features
📘 Concept Capsules

Generates a short, clear explanation of one important concept

Tailored to user-selected target roles

Useful for interview prep, coursework review, and skill refresh

❓ Smart Quiz Questions

Two questions generated per concept

Includes expected answers for self-checking

Lightweight keyword-based auto-evaluation

🎯 Modes

Career Focus → Topics relevant to PM, Supply Chain, Analytics, TPM

Course Review → Revise specific course topics

Mix Mode → Balanced blend of both

🤖 LLM Engine

Primary model: GPT-4.1-mini

Automatic fallback: GPT-3.5-turbo

Built-in usage limit to prevent credit exhaustion

🔐 Secure Key Handling

Works in both Replit and Streamlit Cloud

Loads OPENAI_API_KEY from env variables or streamlit secrets

🛠 Tech Stack

Python

Streamlit (UI)

OpenAI API

Replit (dev)

Streamlit Cloud (deployment)

📂 Project Structure
├── app.py              # Streamlit UI
├── llm.py              # Capsule generation + LLM logic
├── requirements.txt    # Dependencies
├── .streamlit/         # Secrets template
└── README.md

📦 Installation (for local development)
pip install -r requirements.txt
streamlit run app.py


Set your environment variable:

export OPENAI_API_KEY="your_api_key_here"

✨ Future Enhancements (Upcoming)

📅 Spaced repetition scheduling

⭐ Difficulty-based review queue

📊 Progress tracking dashboard

🧠 Smarter answer evaluation (semantic scoring)

🏷 Topic tagging + personalized learning paths

👩🏻‍💻 Author

Neha Alagi
Product-minded Analyst | AI Builder
LinkedIn: https://linkedin.com/in/nehaalagi
