# ✨ Anamnesis — AI Learning & Memory Co-Pilot

Anamnesis is an AI-powered learning companion that helps users learn faster, remember longer, and practice smarter.  
It generates concise concept capsules, personalized quiz questions, and adaptive refreshers for roles like **Product Manager**, **Supply Chain Analyst**, **Data Analyst**, and **TPM**.

---

## 🌐 Demo

🔗 **Live App:**  
https://anamnesis-app-hzggt2wqtaeajcteymjvfa.streamlit.app/

---

## 🚀 Features

### 📘 Concept Capsules
- Generates a short, clear explanation of one important concept  
- Tailored to user-selected target roles  
- Useful for interview prep, coursework review, and skill refresh  

### ❓ Smart Quiz Questions
- Two concept-specific questions  
- Includes expected answers for self-checking  
- Lightweight keyword-based auto-evaluation  

### 🎯 Modes
- **Career Focus** → Topics relevant to PM, Supply Chain, Analytics, TPM  
- **Course Review** → Revise specific course topics  
- **Mix Mode** → Balanced blend of both  

### 🤖 LLM Engine
- Primary model: `gpt-4.1-mini`  
- Automatic fallback: `gpt-3.5-turbo`  
- Built-in credit usage limit for safety  

---

## 🛠 Tech Stack
- Python  
- Streamlit  
- OpenAI API  
- Replit  
- Streamlit Cloud  

---

## 📂 Project Structure

```text
├── app.py              # Streamlit UI
├── llm.py              # Capsule generation + LLM logic
├── requirements.txt    # Dependencies
└── README.md
