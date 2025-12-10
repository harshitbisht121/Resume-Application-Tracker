import base64
from dotenv import load_dotenv

load_dotenv()

import streamlit as st
import os
from PIL import Image
import pdf2image
import google.generativeai as genai
import io
from gtts import gTTS
from google.api_core.exceptions import ResourceExhausted

# ---------------- Gemini config ----------------

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


# ---------------- Helpers ----------------

def get_gemini_response(input_prompt, pdf_content, job_description):
    """
    Call Gemini vision model with:
    - input_prompt: instruction (HR / ATS logic)
    - pdf_content: list with 1 dict { mime_type, data (base64 image) }
    - job_description: text from textarea
    """
    model = genai.GenerativeModel('gemini-2.5-flash')  # You can switch to "gemini-1.5-flash" too
    try:
        response = model.generate_content([input_prompt, pdf_content[0], job_description])
        return response.text
    except ResourceExhausted:
        # Handle quota exceeded gracefully
        return (
            "⚠️ Gemini API quota exceeded for the free tier.\n\n"
            "Please wait for a short time before trying again, "
            "or reduce how often you click the buttons."
        )
    except Exception as e:
        # Generic safety net
        return f"⚠️ Error while calling Gemini: {e}"

import re

def sanitize_text(text):
    if not text:
        return ""

    # Remove bullet symbols
    text = re.sub(r"[•●▪️▫️■□▶►–\-*]+", " ", text)

    # Remove markdown symbols
    text = text.replace("#", "").replace("**", "").replace("__", "")

    # Remove repeated punctuation
    text = re.sub(r"[\|\[\]\(\)\{\}\/\\]+", " ", text)

    # Remove emojis & non-speech unicode
    text = re.sub(r"[^\x00-\x7F]+", " ", text)

    # Convert multiple spaces to one
    text = re.sub(r"\s+", " ", text)

    return text.strip()

def text_to_speech(text: str, lang: str = "en"):
    clean_text = sanitize_text(text)
    if not clean_text:
        clean_text = "I am sorry, the response text cannot be read aloud."

    tts = gTTS(text=clean_text, lang=lang)
    audio_bytes = io.BytesIO()
    tts.write_to_fp(audio_bytes)
    audio_bytes.seek(0)
    return audio_bytes


def input_pdf_setup(uploaded_file):
    """
    Convert first page of uploaded PDF to base64 JPEG for Gemini.
    """
    if uploaded_file is not None:
        images = pdf2image.convert_from_bytes(uploaded_file.read())
        first_page = images[0]

        img_byte_arr = io.BytesIO()
        first_page.save(img_byte_arr, format='JPEG')
        img_byte_arr = img_byte_arr.getvalue()

        pdf_parts = [
            {
                "mime_type": "image/jpeg",
                "data": base64.b64encode(img_byte_arr).decode()
            }
        ]
        return pdf_parts
    else:
        raise FileNotFoundError("No file is uploaded")


def render_audio_player(audio_bytes):
    """
    Render a visible HTML5 audio player with play/pause controls.
    """
    if not audio_bytes:
        return
    audio_bytes.seek(0)
    audio_base64 = base64.b64encode(audio_bytes.read()).decode()
    st.markdown(
        f"""
        <audio controls autoplay style="width: 100%; margin-top: 10px;">
            <source src="data:audio/mp3;base64,{audio_base64}" type="audio/mp3">
            Your browser does not support the audio element.
        </audio>
        """,
        unsafe_allow_html=True,
    )


# ---------------- Streamlit App ----------------

st.set_page_config(page_title="Resume Tracking Expert")
st.header("Resume Tracking Expert")

# Initialize session state for responses
if "analysis_response" not in st.session_state:
    st.session_state["analysis_response"] = None

if "match_response" not in st.session_state:
    st.session_state["match_response"] = None

if "last_response_text" not in st.session_state:
    st.session_state["last_response_text"] = None

# Inputs
input_text = st.text_area("Job Description: ", key="input")
uploaded_file = st.file_uploader("Upload your resume in PDF format only!", type=["pdf"])

if uploaded_file is not None:
    st.write("Your PDF uploaded successfully")

submit1 = st.button("Tell Me About the Resume")
submit3 = st.button("Percentage Match")

input_prompt1 = """
You are an experienced HR With Tech Experience in the filed of Data Science, Full stack Web development,
Big Data Engineering, DEVOPS, Data Analyst, your task is to review the provided resume against the job description for these
profiles. Please share your professional evaluation on whether the candidate's profile aligns with the role. 
Highlight the strengths and weaknesses of the applicant in relation to the specified job requirements.
"""

input_prompt3 = """
You are an skilled ATS(Applicant Tracking System) scanner with a deep understanding of human resource
manager with expertise in Data Science, Full stack Web development, Big Data Engineering, DEVOPS, Data Analyst and deep ATS functionality,
your task is to evaluate resume against the Provided job description for these profiles. Give me the percentage of match if the resume 
matches with the job description. First the output should come as percentage and then keywords missing and last final thoughts.
"""


# ---------- Handle "Tell Me About the Resume" click ----------

if submit1:
    if uploaded_file is None:
        st.warning("Please upload the resume")
    else:
        pdf_content = input_pdf_setup(uploaded_file)
        resp = get_gemini_response(input_prompt1, pdf_content, input_text)
        st.session_state["analysis_response"] = resp
        st.session_state["last_response_text"] = resp


# ---------- Handle "Percentage Match" click ----------

if submit3:
    if uploaded_file is None:
        st.warning("Please upload the resume")
    else:
        pdf_content = input_pdf_setup(uploaded_file)
        resp = get_gemini_response(input_prompt3, pdf_content, input_text)
        st.session_state["match_response"] = resp
        st.session_state["last_response_text"] = resp


# ---------- Display Analysis Response (if exists) ----------

if st.session_state["analysis_response"]:
    st.subheader("Analysis: Tell Me About the Resume")

    col1, col2 = st.columns([4, 1])
    with col1:
        st.write(st.session_state["analysis_response"])

    with col2:
        if st.button("🔊 Read Aloud", key="read_analysis"):
            audio_bytes = text_to_speech(st.session_state["analysis_response"])
            render_audio_player(audio_bytes)


# ---------- Display Match Response (if exists) ----------

if st.session_state["match_response"]:
    st.subheader("Analysis: Percentage Match")

    col1, col2 = st.columns([4, 1])
    with col1:
        st.write(st.session_state["match_response"])

    with col2:
        if st.button("🔊 Read Aloud", key="read_match"):
            audio_bytes = text_to_speech(st.session_state["match_response"])
            render_audio_player(audio_bytes)


# ---------- Floating "Read Aloud" button for last response ----------

# Custom CSS to make the button float at bottom-right
st.markdown("""
    <style>
    .floating-audio-btn button {
        position: fixed;
        bottom: 20px;
        right: 20px;
        border-radius: 50%;
        height: 60px;
        width: 60px;
        font-size: 26px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.3);
        z-index: 9999;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="floating-audio-btn">', unsafe_allow_html=True)
floating_clicked = st.button("🔊", key="floating_read", help="Read last response")
st.markdown('</div>', unsafe_allow_html=True)

if floating_clicked:
    last_text = st.session_state.get("last_response_text")
    if last_text:
        audio_bytes = text_to_speech(last_text)
        render_audio_player(audio_bytes)
    else:
        st.warning("No response available yet. Generate a response first.")

