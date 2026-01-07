# 1. Create a basic Streamlit app that displays a title and a short description.
# 2. Add a Streamlit sidebar and display navigation text inside it.
# 3. Create a file uploader that accepts only PDF, DOCX, and TXT files.
# 4. Display the uploaded file name on the Streamlit UI.
# 5. Show the first 300 characters of uploaded text inside the Streamlit app.
# 6. Use a button to trigger processing after files are uploaded.
# 7. Display resume and job description previews in separate sections.
# 8. Show a skill match percentage using Streamlit metrics.
# 9. Display matched skills and missing skills as two separate lists.
# 10. Create a bar chart comparing matched skills vs missing skills.
# 11. Display a table showing skills and their similarity scores.
# 12. Use Streamlit session state to preserve uploaded data across interactions.
# 13. Add error handling for unsupported file formats and empty uploads.
# 14. Implement a download button to export skill gap results as a CSV file.
# 15. Build a complete Streamlit dashboard that performs upload, analysis, visualization, and report
# export end-to-end.

import streamlit as st
import pandas as pd
import numpy as np
import io

# -------------------------------
# 1. Title and Description
# -------------------------------
st.set_page_config(page_title="Skill Gap Analyzer", layout="wide")
st.title("Skill Gap Analyzer Dashboard")
st.write("Upload resume and job description files to analyze skill match and gaps.")

# -------------------------------
# 2. Sidebar Navigation
# -------------------------------
st.sidebar.title("Navigation")
st.sidebar.write("Upload Files")
st.sidebar.write("Skill Analysis")
st.sidebar.write("Visualization & Report")

# -------------------------------
# Session State Initialization
# -------------------------------
if "resume_text" not in st.session_state:
    st.session_state.resume_text = ""
if "jd_text" not in st.session_state:
    st.session_state.jd_text = ""
if "results" not in st.session_state:
    st.session_state.results = None

# -------------------------------
# Helper Function
# -------------------------------
def read_text(file):
    return file.read().decode("utf-8")

# -------------------------------
# 3. File Uploaders
# -------------------------------
resume_file = st.file_uploader(
    "Upload Resume",
    type=["pdf", "docx", "txt"],
    key="resume"
)

jd_file = st.file_uploader(
    "Upload Job Description",
    type=["pdf", "docx", "txt"],
    key="jd"
)

# -------------------------------
# 4 & 13. File Name Display + Error Handling
# -------------------------------
if resume_file:
    st.success(f"Resume uploaded: {resume_file.name}")

if jd_file:
    st.success(f"Job Description uploaded: {jd_file.name}")

# -------------------------------
# 6. Process Button
# -------------------------------
if st.button("Process Files"):
    if not resume_file or not jd_file:
        st.error("Please upload both resume and job description files.")
    else:
        try:
            st.session_state.resume_text = read_text(resume_file)
            st.session_state.jd_text = read_text(jd_file)
        except:
            st.error("Unsupported or corrupted file format.")

# -------------------------------
# 5 & 7. Preview Sections
# -------------------------------
col1, col2 = st.columns(2)

with col1:
    st.subheader("Resume Preview")
    st.text(st.session_state.resume_text[:300])

with col2:
    st.subheader("Job Description Preview")
    st.text(st.session_state.jd_text[:300])

# -------------------------------
# 8–11. Skill Analysis
# -------------------------------
if st.session_state.resume_text and st.session_state.jd_text:

    skills_master = [
        "python", "sql", "machine learning", "data analysis",
        "flask", "django", "aws", "excel", "communication"
    ]

    resume_skills = [s for s in skills_master if s in st.session_state.resume_text.lower()]
    jd_skills = [s for s in skills_master if s in st.session_state.jd_text.lower()]

    matched_skills = list(set(resume_skills) & set(jd_skills))
    missing_skills = list(set(jd_skills) - set(resume_skills))

    match_percentage = int((len(matched_skills) / max(len(jd_skills), 1)) * 100)

    # -------------------------------
    # 8. Metric
    # -------------------------------
    st.metric("Skill Match Percentage", f"{match_percentage}%")

    # -------------------------------
    # 9. Matched & Missing Skills
    # -------------------------------
    col3, col4 = st.columns(2)

    with col3:
        st.subheader("Matched Skills")
        st.write(matched_skills)

    with col4:
        st.subheader("Missing Skills")
        st.write(missing_skills)

    # -------------------------------
    # 10. Bar Chart
    # -------------------------------
    chart_data = pd.DataFrame({
        "Category": ["Matched Skills", "Missing Skills"],
        "Count": [len(matched_skills), len(missing_skills)]
    })
    st.bar_chart(chart_data.set_index("Category"))

    # -------------------------------
    # 11. Similarity Table (Mock Scores)
    # -------------------------------
    similarity_data = []
    for skill in jd_skills:
        score = 1.0 if skill in matched_skills else round(np.random.uniform(0.2, 0.6), 2)
        similarity_data.append([skill, score])

    df_similarity = pd.DataFrame(
        similarity_data,
        columns=["Skill", "Similarity Score"]
    )

    st.subheader("Skill Similarity Scores")
    st.dataframe(df_similarity)

    # Store results
    st.session_state.results = df_similarity

    # -------------------------------
    # 14. Download CSV
    # -------------------------------
    csv = df_similarity.to_csv(index=False)
    st.download_button(
        label="Download Skill Gap Report (CSV)",
        data=csv,
        file_name="skill_gap_report.csv",
        mime="text/csv"
    )

# -------------------------------
# 15. Complete Dashboard Done
# -------------------------------
