# Basic Skill Matcher
resume_input = input("Enter your resume skills (comma-separated): ")

job_input = input("Enter job required skills (comma-separated): ")

resume_skills = [skill.strip().lower() for skill in resume_input.split(",")]
job_skills = [skill.strip().lower() for skill in job_input.split(",")]


matched_skills = [skill for skill in job_skills if skill in resume_skills]
missing_skills = [skill for skill in job_skills if skill not in resume_skills]

# output
print("\n📝 Skill Matching Result:")
print("----------------------------------")
print("Matched Skills:", ", ".join(matched_skills) if matched_skills else "None")
print("Missing Skills:", ", ".join(missing_skills) if missing_skills else "None")

# Ouput
Enter your resume skills (comma-separated): Python, Java, HTML
Enter job required skills (comma-separated): Python, Java, HTML

Skill Matching Result:
----------------------------------
Matched Skills: python, java, html
Missing Skills: None
