import streamlit as st
import os
from modules.resume_parser import extract_text_from_pdf, extract_text_from_docx, extract_resume_info
from modules.job_matching import match_resume_to_jobs

st.set_page_config(page_title="AI Resume Screener", layout="wide")

st.title("🧠 AI-Powered Resume Screening System")

# Sidebar for role selection
role = st.sidebar.selectbox("Choose Portal", ["Candidate", "Recruiter"])

# Create temp folder if it doesn't exist
if not os.path.exists("temp"):
    os.makedirs("temp")

# ---------------- CANDIDATE PORTAL ----------------
if role == "Candidate":
    st.header("📄 Upload Your Resume")
    uploaded_file = st.file_uploader("Choose a resume file", type=["pdf", "docx"])

    if uploaded_file:
        file_path = os.path.join("temp", uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        # Extract resume text
        if uploaded_file.name.endswith(".pdf"):
            text = extract_text_from_pdf(file_path)
        else:
            text = extract_text_from_docx(file_path)

        st.subheader("✅ Extracted Resume Info")
        resume_info = extract_resume_info(text)
        st.json(resume_info)

        st.subheader("🔍 Matched Job Suggestions")
        job_descriptions = [
            "Looking for a backend developer with Python, Django, and PostgreSQL experience.",
            "Seeking a data analyst with SQL, Excel, and data visualization skills.",
            "Hiring a frontend developer with React, HTML/CSS, and UI/UX knowledge."
        ]

        matches = match_resume_to_jobs(text, job_descriptions)

        for i, score in enumerate(matches):
            st.write(f"**Job {i+1}**: _Score:_ {score:.2f}")
            st.markdown(f"> {job_descriptions[i]}")

# ---------------- RECRUITER PORTAL ----------------
elif role == "Recruiter":
    st.header("📄 Paste Job Description")
    job_text = st.text_area("Enter job description", height=200)

    if st.button("Match Candidates"):
        st.warning("📢 Resume-to-job matching and validation logic will be added here.")
        st.info("💡 Next step: connect to parsed resumes in your database and match them here.")
