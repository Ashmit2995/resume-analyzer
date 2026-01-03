import streamlit as st
from PyPDF2 import PdfReader

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Resume Analyzer",
    layout="centered"
)

# ---------------- LOAD EXTERNAL CSS ----------------
def load_css(file_name):
    try:
        with open(file_name) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        st.warning("CSS file not found. Using default styling.")

load_css("styles.css")

# ---------------- UI HEADER ----------------
st.title("📄 Resume Analyzer Tool")
st.write("Upload your resume and get meaningful insights about its structure.")

# ---------------- FILE UPLOAD ----------------
uploaded_file = st.file_uploader(
    "Upload Resume (PDF)",
    type=["pdf"]
)

# ---------------- PDF TEXT EXTRACTION ----------------
def extract_text_from_pdf(pdf_file):
    reader = PdfReader(pdf_file)
    text = ""

    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"

    return text

# ---------------- SECTION DETECTION ----------------
def detect_sections(text):
    text = text.lower()

    sections = {
        "Skills": ["skills", "technical skills"],
        "Projects": ["projects", "academic projects"],
        "Education": ["education", "academic background"],
        "Experience": ["experience", "work experience", "internship"]
    }

    results = {}
    for section, keywords in sections.items():
        results[section] = any(keyword in text for keyword in keywords)

    return results

# ---------------- MAIN LOGIC ----------------
if uploaded_file:
    st.success("✅ Resume uploaded successfully!")

    resume_text = extract_text_from_pdf(uploaded_file)

    # ----------- EXTRACTED TEXT CARD -----------
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("📃 Extracted Resume Text (Preview)")
    st.text_area(
        "Resume Content",
        resume_text,
        height=280
    )
    st.markdown('</div>', unsafe_allow_html=True)

    # ----------- ANALYSIS CARD -----------
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("📊 Resume Structure Analysis")

    section_status = detect_sections(resume_text)

    for section, found in section_status.items():
        if found:
            st.success(f"✅ {section} section found")
        else:
            st.error(f"❌ {section} section missing")

    st.markdown('</div>', unsafe_allow_html=True)

    # ----------- FEEDBACK CARD -----------
    missing_sections = [s for s, f in section_status.items() if not f]

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("📝 Overall Feedback")

    if not missing_sections:
        st.success("🎉 Your resume contains all essential sections.")
    else:
        st.warning(
            "To improve your resume, consider adding these sections:\n\n"
            + ", ".join(missing_sections)
        )

    st.markdown('</div>', unsafe_allow_html=True)
