import streamlit as st
from PyPDF2 import PdfReader

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Resume Analyzer",
    layout="centered"
)

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>
/* Main background */
.stApp {
    background-color: #0f172a;
    color: #e5e7eb;
}

/* Title */
h1 {
    color: #f8fafc;
    font-weight: 700;
}

/* Subheaders */
h2, h3 {
    color: #e2e8f0;
}

/* File uploader */
[data-testid="stFileUploader"] {
    background-color: #020617;
    padding: 1rem;
    border-radius: 10px;
    border: 1px solid #334155;
}

/* Text area */
textarea {
    background-color: #020617 !important;
    color: #e5e7eb !important;
    border-radius: 10px !important;
    border: 1px solid #334155 !important;
}

/* Success & error boxes */
.stAlert {
    border-radius: 10px;
}

/* Cards */
.card {
    background-color: #020617;
    padding: 1.2rem;
    border-radius: 12px;
    border: 1px solid #334155;
    margin-bottom: 1rem;
}
</style>
""", unsafe_allow_html=True)

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
        results[section] = any(k in text for k in keywords)

    return results

# ---------------- MAIN LOGIC ----------------
if uploaded_file:
    st.success("✅ Resume uploaded successfully!")

    resume_text = extract_text_from_pdf(uploaded_file)

    # ---------- EXTRACTED TEXT ----------
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("📃 Extracted Resume Text (Preview)")
    st.text_area(
        "Resume Content",
        resume_text,
        height=280
    )
    st.markdown('</div>', unsafe_allow_html=True)

    # ---------- ANALYSIS ----------
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("📊 Resume Structure Analysis")

    section_status = detect_sections(resume_text)

    for section, found in section_status.items():
        if found:
            st.success(f"✅ {section} section found")
        else:
            st.error(f"❌ {section} section missing")

    st.markdown('</div>', unsafe_allow_html=True)

    # ---------- FEEDBACK ----------
    missing = [s for s, f in section_status.items() if not f]

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("📝 Overall Feedback")

    if not missing:
        st.success("🎉 Your resume contains all essential sections.")
    else:
        st.warning(
            "Consider adding these sections to improve your resume:\n\n"
            + ", ".join(missing)
        )

    st.markdown('</div>', unsafe_allow_html=True)
