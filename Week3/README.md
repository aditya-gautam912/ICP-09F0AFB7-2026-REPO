# Project 1: Intelligent Chatbot (Week 3 Completion)

This project is an AI-powered conversational assistant that leverages the ultra-fast Groq Inference Engine and Meta's Llama 3.3 model. It provides both a Command Line Interface (CLI) and a modern Web-based Graphical User Interface (GUI).

## 🌟 Key Features
- **Dual Interface:** Choose between a lightweight CLI or a polished Streamlit Web App.
- **Contextual Memory:** The AI maintains conversation history to provide relevant follow-up answers.
- **Real-time Streaming:** AI responses are streamed live as they are generated (Web GUI).
- **Professional Error Handling:** Robust catching of API connection, rate limit, and status errors.
- **Secure Configuration:** Uses environment variables for API key management.

## 🛠️ Tech Stack
- **Engine:** Groq (LPU Inference Engine)
- **Model:** Llama 3.3 (70B Versatile)
- **Frameworks:** Streamlit (Frontend), Python (Backend)
- **APIs:** Groq Cloud API, Dotenv

## 🚀 How to Run

### 1. Prerequisites
- Python 3.8 or higher.
- A Groq API Key (stored in `.env`).

### 2. Setup
```bash
# Navigate to the folder
cd Week3

# Create and activate virtual environment
python -m venv venv
source venv/Scripts/activate  # On Windows: .\venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Launching
- **For Web GUI:**
  ```bash
  streamlit run app.py
  ```
- **For CLI Mode:**
  ```bash
  python chatbot.py
  ```

## 🖼️ Visual Preview
![Chatbot UI Screenshot](Screenshot%202026-05-12%20171019.png)

## 📁 Repository Structure (Week 3)
- `chatbot.py`: Core CLI implementation.
- `app.py`: Streamlit-based web implementation.
- `requirements.txt`: Project dependencies.
- `.env`: API configuration (ignored in git).
- `README.md`: Project documentation.
