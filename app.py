import streamlit as st
from PyPDF2 import PdfReader

st.set_page_config(page_title="Resume Analyzer", layout="centered")

st.title("📄 Resume Analyzer Tool")
st.write("Upload your resume and get basic insights.")

uploaded_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])

def extract_text_from_pdf(pdf_file):
    reader = PdfReader(pdf_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text

if uploaded_file:
    st.success("Resume uploaded successfully!")

    resume_text = extract_text_from_pdf(uploaded_file)

    st.subheader("Extracted Resume Text (Preview)")
    st.text_area("Resume Content", resume_text, height=300)
