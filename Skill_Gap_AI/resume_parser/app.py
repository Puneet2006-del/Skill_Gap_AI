from flask import Flask, render_template, request
import pdfplumber
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import os

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
STATIC_FOLDER = "static"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(STATIC_FOLDER, exist_ok=True)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

model = SentenceTransformer("all-MiniLM-L6-v2")

JD_SKILLS = [
    "Python",
    "SQL",
    "Machine Learning",
    "AWS Cloud Services",
    "Data Analysis",
    "Leadership"
]

SKILL_VOCAB = [
    "python",
    "sql",
    "machine learning",
    "data analysis",
    "aws",
    "statistics",
    "communication",
    "leadership",
    "cloud"
]

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        file = request.files["resume"]
        file_path = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
        file.save(file_path)

        text = ""
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                if page.extract_text():
                    text += page.extract_text().lower()
        
        resume_skills = []
        for skill in SKILL_VOCAB:
            if skill in text:
                resume_skills.append(skill.title())
        
        if not resume_skills:
            resume_skills = ["No relevant skills found"]

        resume_embeddings = model.encode(resume_skills)
        jd_embeddings = model.encode(JD_SKILLS)

        similarity = cosine_similarity(resume_embeddings, jd_embeddings)
        df = pd.DataFrame(similarity, index=resume_skills, columns=JD_SKILLS)

        plt.figure(figsize=(8, 5))
        sns.heatmap(df, annot=True, cmap="YlGnBu")
        plt.tight_layout()
        plt.savefig(os.path.join(STATIC_FOLDER, "heatmap.png"))
        plt.close()

        matched, partial, missing = [], [], []

        for j, skill in enumerate(JD_SKILLS):
            score = similarity[:, j].max()
            if score >= 0.8:
                matched.append(skill)
            elif score >= 0.5:
                partial.append(skill)
            else:
                missing.append(skill)

        overall = round((len(matched) / len(JD_SKILLS)) * 100)

        if overall >= 70:
            color = "#68b36b"
        elif overall >= 40:
            color = "#f4a261"
        else:
            color = "#e76f51"

        return render_template(
            "index.html",
            overall=overall,
            matched=matched,
            partial=partial,
            missing=missing,
            color=color,
            show=True
        )

    return render_template("index.html", show=False)

if __name__ == "__main__":
    app.run(debug=True)
