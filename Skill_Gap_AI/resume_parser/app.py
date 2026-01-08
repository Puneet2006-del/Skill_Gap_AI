import streamlit as st
import pandas as pd
import pdfplumber
import docx
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# ---------------- CONFIG ----------------
st.set_page_config(page_title="Skill Gap Analysis Dashboard", layout="wide")

# Load CSS
with open("static/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# ---------------- MODEL ----------------
@st.cache_resource
def load_model():
    return SentenceTransformer("all-MiniLM-L6-v2")

model = load_model()


# ---------------- JD SKILLS ----------------
JD_SKILLS = [
    "Python",
    "Machine Learning",
    "SQL",
    "Statistics",
    "Communication",
    "AWS",
    "Project Management"
]

# ---------------- UTILS ----------------
def extract_text(file):
    if file.name.endswith(".pdf"):
        with pdfplumber.open(file) as pdf:
            return " ".join(p.extract_text() for p in pdf.pages if p.extract_text())
    elif file.name.endswith(".docx"):
        doc = docx.Document(file)
        return " ".join(p.text for p in doc.paragraphs)
    elif file.name.endswith(".txt"):
        return file.read().decode("utf-8")
    return ""

def radar_chart(matched_skills):
    categories = ["Technical", "Soft Skills", "Experience", "Education", "Certifications"]

   
    resume_scores = [
        5 if any(s in matched_skills for s in ["Python", "Machine Learning", "SQL"]) else 1.5,
        4.5 if "Communication" in matched_skills else 1.5,
        2.5, 
        2.5,  
        2     
    ]

    # Job requirement baseline (Static)
    jd_scores = [4, 4, 3, 3, 2]

    angles = np.linspace(0, 2 * np.pi, len(categories), endpoint=False).tolist()
    angles += angles[:1]

    resume_scores += resume_scores[:1]
    jd_scores += jd_scores[:1]

    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))

    # ---- Job Requirements
    ax.plot(
        angles,
        jd_scores,
        linewidth=2,
        linestyle="--",
        color="#ff4b4b", 
        label="Job Requirements"
    )

    # ---- Resume Profile ----
    ax.plot(
        angles,
        resume_scores,
        linewidth=3,
        color="#1f77b4", 
        label="Your Profile",
        marker='o'      
    )
    
    ax.fill(
        angles,
        resume_scores,
        alpha=0.25,
        color="#1f77b4"
    )

    ax.set_thetagrids(np.degrees(angles[:-1]), categories)
    ax.set_ylim(0, 5)
    
  
    ax.grid(True, linestyle=':', alpha=0.7)

    ax.legend(loc="upper right", bbox_to_anchor=(1.3, 1.1))

    return fig


def skill_progress(skill, value):
    st.markdown(
        f"""
        <div style="margin-bottom:12px;">
            <b>{skill}</b>
            <div style="background:#e0e0e0;border-radius:20px;height:14px;">
                <div style="width:{value}%;background:#2ecc71;height:14px;border-radius:20px;"></div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

# ---------------- SIDEBAR ----------------
st.sidebar.title("Skill Gap AI")
file = st.sidebar.file_uploader("Upload Resume", ["pdf", "docx", "txt"])

# ---------------- MAIN ----------------
st.markdown("<h2>Skill Gap Analysis Dashboard</h2>", unsafe_allow_html=True)

if file:
    text = extract_text(file)

    resume_skills = [s for s in JD_SKILLS if s.lower() in text.lower()]

    res_emb = model.encode(resume_skills)
    jd_emb = model.encode(JD_SKILLS)
    similarity = cosine_similarity(res_emb, jd_emb)

    matched, missing = [], []
    for i, skill in enumerate(JD_SKILLS):
        if similarity[:, i].max() >= 0.5:
            matched.append(skill)
        else:
            missing.append(skill)

    match_percentage = int((len(matched) / len(JD_SKILLS)) * 100)

    # ---------------- BAR CHART ----------------
    resume_scores = []
    for i, skill in enumerate(JD_SKILLS):
        score = similarity[:, i].max() if resume_skills else 0
        resume_scores.append(int(score * 100))

    jd_scores = [100 for _ in JD_SKILLS]

    fig = go.Figure()
    fig.add_bar(x=JD_SKILLS, y=resume_scores, name="Resume Skills")
    fig.add_bar(x=JD_SKILLS, y=jd_scores, name="Job Requirements")

    fig.update_layout(
        barmode="group",
        height=350,
        margin=dict(l=20, r=20, t=40, b=20),
        yaxis_title="Match Percentage"
    )

    st.plotly_chart(fig, use_container_width=True)

    # ---------------- METRICS ----------------
    col1, col2, col3 = st.columns(3)

    col1.markdown(
        f"<div class='metric-card'><div class='metric-title'>Overall Match</div><div class='metric-value'>{match_percentage}%</div></div>",
        unsafe_allow_html=True
    )
    col2.markdown(
        f"<div class='metric-card'><div class='metric-title'>Matched Skills</div><div class='metric-value'>{len(matched)}</div></div>",
        unsafe_allow_html=True
    )
    col3.markdown(
        f"<div class='metric-card'><div class='metric-title'>Missing Skills</div><div class='metric-value'>{len(missing)}</div></div>",
        unsafe_allow_html=True
    )

    # ---------------- SKILLS ----------------
    st.subheader("Matched Skills")
    for s in matched:
        st.markdown(f"<span class='skill-chip match'>{s}</span>", unsafe_allow_html=True)

    st.subheader("Missing Skills")
    for s in missing:
        st.markdown(f"<span class='skill-chip miss'>{s}</span>", unsafe_allow_html=True)

    # ---------------- SKILL COMPARISON ----------------
    st.subheader("Skill Comparison")
    skill_progress("Python", int(similarity[:, JD_SKILLS.index("Python")].max() * 100))
    skill_progress("Machine Learning", int(similarity[:, JD_SKILLS.index("Machine Learning")].max() * 100))
    skill_progress("SQL", int(similarity[:, JD_SKILLS.index("SQL")].max() * 100))
    skill_progress("AWS", int(similarity[:, JD_SKILLS.index("AWS")].max() * 100))

    # ---------------- RADAR CHART ----------------
    st.subheader("Profile Match Overview")
    st.pyplot(radar_chart(matched))

    # ---------------- CSV EXPORT ----------------
    max_len = max(len(matched), len(missing))
    df = pd.DataFrame({
        "Matched Skills": matched + [""] * (max_len - len(matched)),
        "Missing Skills": missing + [""] * (max_len - len(missing))
    })

    st.download_button(
        "Download CSV Report",
        df.to_csv(index=False),
        "skill_gap_report.csv",
        "text/csv"
    )

else:
    st.info("Upload a resume from the sidebar to view the dashboard")
