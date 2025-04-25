import spacy
import PyPDF2
import docx

# Load spaCy language model
nlp = spacy.load("en_core_web_sm")

# Sample skills list (can be expanded)
skills_keywords = {
    "Java", "JavaScript", "SQL", "Machine Learning", "Deep Learning",
                "AI", "NLP", "Cloud Computing", "AWS", "React", "Django", "Flask", "Teaching",
                "Digital marketing", "Graphic design", "People Operations", "Analyst", "Data Science",
                "Virtual assistant", "Nursing", "Child Care", "lead generation", "content creator",
                "UI/UX", "Marketing", "Cybersecurity", "Data Science", "Big Data", "Python", "Canva",
                "Photoshop", "Adobe", "Figma", "Python", "Social media management", "SEO",
                "Project Management", "Video Editing", "Lab testing", "Student Transportation Assistance",
                "Culinary Instruction", "Personal Hygiene", "Education", "Personal Care Support",
                "Job Readiness Training", "Relationship Building", "People Operations",
                "Front-End Developer", "Machine Learning", "AI", "Deep Learning", "Cloud Computing",
                "UI/UX", "Marketing"
}

def extract_text_from_pdf(pdf_path):
    """Extracts text from a PDF resume."""
    text = ""
    try:
        with open(pdf_path, "rb") as file:
            reader = PyPDF2.PdfReader(file)
            for page in reader.pages:
                text += page.extract_text() or ""
    except Exception as e:
        print(f"Error reading PDF: {e}")
    return text


def extract_text_from_docx(docx_path):
    """Extracts text from a DOCX resume."""
    try:
        doc = docx.Document(docx_path)
        text = "\n".join([para.text for para in doc.paragraphs])
        return text
    except Exception as e:
        print(f"Error reading DOCX: {e}")
        return ""


def extract_resume_info(text):
    """Extracts name, skills, and key entities from resume text."""
    doc = nlp(text)
    
    # Attempt to get candidate name
    name = None
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            name = ent.text
            break

    # Extract matching skills from our list
    found_skills = []
    words = set([token.text.strip() for token in doc if token.is_alpha])
    for skill in skills_keywords:
        if skill in words:
            found_skills.append(skill)

    return {
        "name": name or "Name not found",
        "skills": found_skills or ["No skills matched"],
        "summary_snippet": text[:300] + "..."  # show a snippet of the resume
    }
