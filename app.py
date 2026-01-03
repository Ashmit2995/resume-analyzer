import streamlit as st
from PyPDF2 import PdfReader

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Resume Analyzer",
    layout="centered"
)

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


# ---------------- SECTION DETECTION LOGIC ----------------
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

    # ---------- SHOW EXTRACTED TEXT ----------
    st.subheader("📃 Extracted Resume Text (Preview)")
    st.text_area(
        "Resume Content",
        resume_text,
        height=300
    )

    # ---------- ANALYSIS ----------
    st.subheader("📊 Resume Structure Analysis")

    section_status = detect_sections(resume_text)

    for section, found in section_status.items():
        if found:
            st.success(f"✅ {section} section found")
        else:
            st.error(f"❌ {section} section missing")

    # ---------- OVERALL FEEDBACK ----------
    missing_sections = [s for s, f in section_status.items() if not f]

    st.subheader("📝 Overall Feedback")

    if not missing_sections:
        st.success("🎉 Your resume has all the essential sections!")
    else:
        st.warning(
            "Your resume is missing the following important sections:\n\n"
            + ", ".join(missing_sections)
        )
