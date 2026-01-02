# 1. Remove duplicate skills from two given lists: resume skills and job description skills.
# 2. Convert all skills in a list to lowercase and remove extra spaces.
# 3. Store resume skills and job description skills in a single structured dictionary.
# 4. Load a pretrained Sentence-BERT model using Python.
# 5. Generate an embedding for a single skill string and print its vector dimension.
# 6. Generate embeddings for a list of resume skills.
# 7. Generate embeddings for a list of job description skills.
# 8. Compute cosine similarity between two skill embeddings.
# 9. Compare one resume skill against all job description skills and print similarity scores.
# 10. Create a similarity matrix for all resume skills versus all job description skills.
# 11. Store the similarity matrix in a Pandas DataFrame with proper row and column labels.
# 12. For each job description skill, find the resume skill with the highest similarity score.
# 13. Define similarity thresholds and classify skills as matched, partially matched, or missing.
# 14. Generate a structured skill gap report containing matched, partial, and missing skills.
# 15. Save the skill gap report in JSON format.
# 16. Visualize the similarity matrix using a heatmap.
# 17. Add axis labels and a color legend to the heatmap.
# 18. Highlight the highest similarity score in each column of the similarity matrix.
# 19. Handle cases where resume skills or job description skills are empty.
# 20. Normalize abbreviations such as ML, DL, and AI before generating embeddings.
# 21. Compare similarity results using two different Sentence-BERT models.
# 22. Cache embeddings so repeated skills are not embedded multiple times.
# 23. Build a pipeline that takes raw resume text and job description text and outputs a skill gap
# report.
# 24. Return the top three closest resume skills for each job description skill.
# 25. Apply different similarity thresholds for technical skills and soft skills.
# 26. Compute an overall resume and job description alignment score.
# 27. Export the skill gap report and similarity heatmap into a single file.
# 28. Design a modular architecture separating embedding generation, similarity computation, and
# reporting.


# 1–3, 19, 20: Skill cleaning, deduplication, structuring
import json
import numpy as np
import pandas as pd
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import matplotlib.pyplot as plt
import seaborn as sns

ABBREVIATIONS = {
    "ml": "machine learning",
    "dl": "deep learning",
    "ai": "artificial intelligence"
}

def normalize_skill(skill):
    skill = skill.strip().lower()
    return ABBREVIATIONS.get(skill, skill)

def clean_skills(skills):
    return list(set(normalize_skill(s) for s in skills if s.strip()))

def build_skill_dict(resume_skills, jd_skills):
    return {
        "resume_skills": clean_skills(resume_skills),
        "job_skills": clean_skills(jd_skills)
    }


# 4, 21: Load Sentence-BERT models
model_a = SentenceTransformer("all-MiniLM-L6-v2")
model_b = SentenceTransformer("paraphrase-MiniLM-L12-v2")


#5–7, 22: Embedding generation with caching

embedding_cache = {}
def embed_skills(skills, model):
    embeddings = []
    for skill in skills:
        if skill not in embedding_cache:
            embedding_cache[skill] = model.encode(skill)
        embeddings.append(embedding_cache[skill])
    return np.array(embeddings)


# 8–11: Similarity computation & matrix

def similarity_matrix(resume_emb, jd_emb):
    return cosine_similarity(resume_emb, jd_emb)

def similarity_dataframe(matrix, resume_skills, jd_skills):
    return pd.DataFrame(matrix, index=resume_skills, columns=jd_skills)


# 12, 24: Best matches
def best_matches(df, top_n=3):
    results = {}
    for jd in df.columns:
        results[jd] = df[jd].sort_values(ascending=False).head(top_n).to_dict()
    return results


# 13, 25: Threshold-based classification
def classify_skills(df, tech_threshold=0.75, partial_threshold=0.5):
    matched, partial, missing = [], [], []

    for jd in df.columns:
        max_score = df[jd].max()
        if max_score >= tech_threshold:
            matched.append(jd)
        elif max_score >= partial_threshold:
            partial.append(jd)
        else:
            missing.append(jd)

    return matched, partial, missing


# 14–15: Skill gap report & JSON export
def skill_gap_report(df):
    matched, partial, missing = classify_skills(df)
    return {
        "matched_skills": matched,
        "partially_matched_skills": partial,
        "missing_skills": missing
    }

def save_report(report, path="skill_gap_report.json"):
    with open(path, "w") as f:
        json.dump(report, f, indent=4)


# 16–18, 27: Heatmap visualization & export
def plot_heatmap(df):
    plt.figure(figsize=(10, 6))
    sns.heatmap(df, annot=True, cmap="Blues")
    plt.xlabel("Job Description Skills")
    plt.ylabel("Resume Skills")
    plt.title("Skill Similarity Heatmap")
    plt.show()


# 23, 26: End-to-end pipeline

def skill_gap_pipeline(resume_skills, jd_skills, model=model_a):
    if not resume_skills or not jd_skills:
        return {"error": "Empty skill list provided"}

    skills = build_skill_dict(resume_skills, jd_skills)

    resume_emb = embed_skills(skills["resume_skills"], model)
    jd_emb = embed_skills(skills["job_skills"], model)

    sim_matrix = similarity_matrix(resume_emb, jd_emb)
    df = similarity_dataframe(sim_matrix, skills["resume_skills"], skills["job_skills"])

    report = skill_gap_report(df)
    alignment_score = df.max(axis=0).mean()

    return {
        "similarity_matrix": df,
        "skill_gap_report": report,
        "alignment_score": alignment_score
    }

# Example:

resume = ["Python", "ML", "SQL", "TensorFlow"]
jd = ["Machine Learning", "Data Analysis", "SQL", "Deep Learning"]

result = skill_gap_pipeline(resume, jd)
print(result["skill_gap_report"])
print("Alignment Score:", result["alignment_score"])

plot_heatmap(result["similarity_matrix"])
save_report(result["skill_gap_report"])
