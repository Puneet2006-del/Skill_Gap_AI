from flask import Flask, render_template, request
import pdfplumber
import spacy
from skills import TECHNICAL_SKILLS, SOFT_SKILLS

app = Flask(__name__)
nlp = spacy.load("en_core_web_sm")

def extract_text_from_pdf(path):
    text = ""
    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""
    return text

def extract_skills(text, skill_list):
    text = text.lower()
    found = []
    for skill in skill_list:
        if skill in text:
            found.append(skill.title())
    return list(set(found))

@app.route("/", methods=["GET", "POST"])
def index():
    tech_skills = []
    soft_skills = []

    if request.method == "POST":
        file = request.files["resume"]
        file_path = f"uploads/{file.filename}"
        file.save(file_path)

        resume_text = extract_text_from_pdf(file_path)

        tech_skills = extract_skills(resume_text, TECHNICAL_SKILLS)
        soft_skills = extract_skills(resume_text, SOFT_SKILLS)

    return render_template(
        "index.html",
        tech_skills=tech_skills,
        soft_skills=soft_skills
    )

if __name__ == "__main__":
    app.run(debug=True)
