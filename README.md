# Resume-Application-Tracker
A simple and efficient Streamlit-based web app that helps users upload resumes, extract relevant information using Google Generative AI, and track application details. Features include PDF-to-image conversion, text-to-speech support, and environment variable handling. Built with Python for fast, interactive resume processing.

The Resume Application Tracker is an AI-powered tool designed to evaluate resumes against job descriptions. It uses Google Gemini (Vision + Text) to extract information from a PDF resume, analyze it, and provide:

A detailed resume review

ATS-style percentage match score

Missing keywords

Suggestions for improvement

AI voice assistant to read the analysis aloud

This project helps job seekers quickly understand how well their resume fits a specific role.

🚀 Features
🔍 AI Resume Analysis

Upload a PDF resume

Extracts the first page using pdf2image

Gemini Vision reviews and summarizes key points

📊 ATS Match Percentage

Compares resume against job description

Gives:

Percentage match

Missing keywords

Strengths & weaknesses

🗣️ AI Voice Assistant

Read-aloud button next to each response

Floating voice button that reads the last generated response

Text is cleaned to avoid reading bullet points & symbols

🎯 Optimized and Reliable

Handles Gemini quota errors gracefully

Ensures responses persist using st.session_state

Cleaner audio using HTML5 <audio> player

🛠️ Tech Stack
Frontend / UI

Streamlit

HTML5 Audio Player

Backend

Python

pdf2image

Google Gemini 2.5 Flash

gTTS (Google Text-to-Speech)

Other Tools

.env for secure API key storage

.gitignore to protect sensitive files

📂 Project Structure
Resume Application Tracker/
│
├── app.py                # Main Streamlit application
├── requirements.txt      # Dependencies
├── .gitignore            # Ensures .env is hidden from GitHub
├── .env (hidden)         # Stores GOOGLE_API_KEY
│
└── assets/ (optional)    # For images or screenshots

⚙️ How It Works
1️⃣ Upload Resume

User uploads a PDF file.
The app converts the first page into a JPEG image for Gemini Vision.

2️⃣ Enter Job Description

A text area allows the user to paste the JD.

3️⃣ Choose an Action

Tell Me About the Resume
→ HR-style evaluation using Gemini

Percentage Match
→ ATS-style scoring using Gemini

4️⃣ AI Processing

The app:

Sends instructions + resume image + job description to Gemini

Receives formatted text response

5️⃣ Voice Assistant

Cleans text (removes bullets, symbols, emojis)

Converts it into speech using gTTS

Plays the audio using an HTML5 audio player

6️⃣ Results Displayed

Always visible even after button clicks (via session_state)

Floating 🔊 button can read the last response anytime

💻 Installation
1. Clone the repository
git clone https://github.com/harshitbisht121/Resume-Application-Tracker.git
cd Resume-Application-Tracker

2. Create virtual environment (optional but recommended)
python -m venv venv
venv\Scripts\activate   # Windows

3. Install dependencies
pip install -r requirements.txt

4. Add your Gemini API key

Create a .env file:

GOOGLE_API_KEY=your_new_api_key_here

5. Run the app
streamlit run app.py

📌 Notes

.env must not be committed to GitHub

Use .gitignore to block .env

Free Gemini Vision tier may have rate-limits

⭐ Future Enhancements

(Optional — you can delete this section)

Add resume parsing (skills, experience extraction)

Add multi-page PDF support

Add a better TTS voice (OpenAI Voice API)

Store resume + job description history

Add downloadable PDF report
