# MathSolver AI - Complete Project Files

## 1. app.py

```python
import streamlit as st
from groq import Groq
import sympy as sp
from sympy import symbols, Eq, solve
from PIL import Image
import pytesseract
import PyPDF2
import tempfile

# PAGE CONFIG
st.set_page_config(
    page_title="MathSolver AI",
    page_icon="🧠",
    layout="wide"
)

# CUSTOM CSS
st.markdown("""
<style>

html, body, [class*="css"] {
    font-family: Arial;
}

.stApp {
    background-color: #0f172a;
    color: white;
}

.chat-container {
    padding-bottom: 100px;
}

.user-msg {
    background: #2563eb;
    padding: 12px;
    border-radius: 15px;
    margin: 10px 0;
    text-align: right;
}

.bot-msg {
    background: #1e293b;
    padding: 12px;
    border-radius: 15px;
    margin: 10px 0;
}

.stTextInput > div > div > input {
    background-color: #1e293b;
    color: white;
    border-radius: 10px;
}

.stFileUploader {
    background-color: #1e293b;
    padding: 10px;
    border-radius: 10px;
}

.sidebar .sidebar-content {
    background-color: #111827;
}

</style>
""", unsafe_allow_html=True)

# SIDEBAR
st.sidebar.title("🧠 MathSolver AI")

if st.sidebar.button("➕ New Chat"):
    st.session_state.messages = []

if st.sidebar.button("🗑 Delete Chat"):
    st.session_state.messages = []

st.sidebar.markdown("---")
st.sidebar.subheader("📚 Topics")

st.sidebar.write("✔ Algebra")
st.sidebar.write("✔ Calculus")
st.sidebar.write("✔ Geometry")
st.sidebar.write("✔ Ratios")
st.sidebar.write("✔ Percentages")
st.sidebar.write("✔ Statistics")
st.sidebar.write("✔ Number Theory")
st.sidebar.write("✔ Fuzzy Set Theory")
st.sidebar.write("✔ Optimization Theory")

# API KEY
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# CHAT HISTORY
if "messages" not in st.session_state:
    st.session_state.messages = []

# TITLE
st.title("🤖 MathSolver AI")
st.caption("Solve any math problem step-by-step")

# FILE UPLOAD SECTION
st.subheader("📂 Upload Options")

col1, col2 = st.columns(2)

with col1:
    uploaded_image = st.file_uploader(
        "📸 Upload Image",
        type=["png", "jpg", "jpeg"]
    )

with col2:
    uploaded_pdf = st.file_uploader(
        "📄 Upload PDF",
        type=["pdf"]
    )

# CAMERA
camera_image = st.camera_input("📷 Take Photo")

# IMAGE OCR
if uploaded_image:
    image = Image.open(uploaded_image)
    st.image(image, caption="Uploaded Image")

    extracted_text = pytesseract.image_to_string(image)

    st.success("✅ Text Extracted")
    st.write(extracted_text)

if camera_image:
    image = Image.open(camera_image)
    st.image(image)

    extracted_text = pytesseract.image_to_string(image)

    st.success("✅ Text Extracted")
    st.write(extracted_text)

# PDF EXTRACTION
if uploaded_pdf:
    pdf_reader = PyPDF2.PdfReader(uploaded_pdf)
    pdf_text = ""

    for page in pdf_reader.pages:
        pdf_text += page.extract_text()

    st.success("✅ PDF Extracted")
    st.write(pdf_text)

# CHAT DISPLAY
for msg in st.session_state.messages:

    if msg["role"] == "user":
        st.markdown(
            f'<div class="user-msg">{msg["content"]}</div>',
            unsafe_allow_html=True
        )

    else:
        st.markdown(
            f'<div class="bot-msg">{msg["content"]}</div>',
            unsafe_allow_html=True
        )

# USER INPUT
user_input = st.chat_input("Type your math question...")

# AI RESPONSE
if user_input:

    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_input
        }
    )

    with st.spinner("Solving..."):

        prompt = f"""
        Solve this math problem step-by-step.

        Question:
        {user_input}

        Rules:
        - Give proper steps
        - Keep explanation short
        - Use clean formatting
        - Detect topic automatically
        """

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        answer = response.choices[0].message.content

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer
        }
    )

    st.rerun()
