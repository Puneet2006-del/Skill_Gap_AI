# 1. Install spaCy and load the en_core_web_sm model using Python.
# 2. Using PhraseMatcher, extract the skills Python and SQL from the text: 'I have experience in
# Python and SQL.'
# 3. Create a Python list of five technical skills and convert them into PhraseMatcher patterns.
# 4. Write code to convert all extracted skills into lowercase.
# 5. Remove duplicate skills from a list of extracted skills.
# 6. Extract technical skills from the sentence: 'Experience in Python, NLP, and Machine Learning
# with SQL.'
# 7. Identify soft skills from a resume text using token comparison and a predefined soft skill list.
# 8. Configure PhraseMatcher to perform case-insensitive matching.
# 9. Store extracted technical and soft skills in the JSON structure: { technical_skills: [], soft_skills: [] }.
# 10. Extract skills from a paragraph that contains repeated skill mentions and ensure duplicates are
# removed.
# 11. Ensure skills are correctly extracted from text containing punctuation such as commas and
# semicolons.
# 12. Combine PhraseMatcher for technical skills and rule-based token matching for soft skills in a
# single spaCy pipeline.
# 13. Extract skills from multiple sentences and merge them into one normalized output dictionary.
# 14. Modify skill extraction logic to match SQL but not NoSQL.
# 15. Given a resume and a job description, extract skills separately and output them as two different
# JSON objects


# ans 1

import spacy
nlp = spacy.load("en_core_web_sm")

# ans 2

from spacy.matcher import PhraseMatcher

nlp = spacy.load("en_core_web_sm")
matcher = PhraseMatcher(nlp.vocab)

text = "I have experience in Python and SQL."
doc = nlp(text)

patterns = [nlp("Python"), nlp("SQL")]
matcher.add("SKILLS", patterns)

skills = [doc[start:end].text for _, start, end in matcher(doc)]
print(skills)


# ans 3

skills = ["Python", "SQL", "NLP", "Machine Learning", "Java"]

patterns = [nlp(skill) for skill in skills]

# ans 4

lower_skills = [skill.lower() for skill in skills]
print(lower_skills)

# ans 5

skills = ["python", "sql", "python", "nlp"]
unique_skills = list(set(skills))
print(unique_skills)

# ans 6

from spacy.matcher import PhraseMatcher

nlp = spacy.load("en_core_web_sm")
matcher = PhraseMatcher(nlp.vocab)

tech_skills = ["Python", "NLP", "Machine Learning", "SQL"]
matcher.add("TECH", [nlp(skill) for skill in tech_skills])

text = "Experience in Python, NLP, and Machine Learning with SQL."
doc = nlp(text)

found = set([doc[start:end].text for _, start, end in matcher(doc)])
print(found)


# ans 7

nlp = spacy.load("en_core_web_sm")

soft_skills = ["communication", "teamwork", "leadership"]
text = "Strong communication and teamwork skills"
doc = nlp(text)

found = set(token.text.lower() for token in doc if token.text.lower() in soft_skills)
print(found)


# ans 8

matcher = PhraseMatcher(nlp.vocab, attr="LOWER")

skills = ["python", "sql"]
matcher.add("SKILLS", [nlp(skill) for skill in skills])

# ans 9

skills_json = {
    "technical_skills": ["python", "sql"],
    "soft_skills": ["communication", "teamwork"]
}

print(skills_json)


# ans 10

text = "Python is used with SQL. Python and SQL are popular."
doc = nlp(text)

matcher = PhraseMatcher(nlp.vocab, attr="LOWER")
matcher.add("TECH", [nlp("python"), nlp("sql")])

skills = set([doc[start:end].text.lower() for _, start, end in matcher(doc)])
print(skills)


# ans 11

text = "Python, SQL; and NLP are required."
doc = nlp(text)

matcher = PhraseMatcher(nlp.vocab, attr="LOWER")
matcher.add("TECH", [nlp("python"), nlp("sql"), nlp("nlp")])

skills = set([doc[start:end].text.lower() for _, start, end in matcher(doc)])
print(skills)


# ans 12

tech_matcher = PhraseMatcher(nlp.vocab, attr="LOWER")
tech_matcher.add("TECH", [nlp("python"), nlp("sql")])

soft_skills = ["communication", "teamwork"]

text = "Python and SQL with strong communication"
doc = nlp(text)

tech = set([doc[start:end].text.lower() for _, start, end in tech_matcher(doc)])
soft = set(token.text.lower() for token in doc if token.text.lower() in soft_skills)

print({"technical_skills": list(tech), "soft_skills": list(soft)})


# ans 13

text = "I know Python. I use SQL and NLP."
doc = nlp(text)

matcher = PhraseMatcher(nlp.vocab, attr="LOWER")
matcher.add("TECH", [nlp("python"), nlp("sql"), nlp("nlp")])

skills = set([doc[start:end].text.lower() for _, start, end in matcher(doc)])
print({"technical_skills": list(skills)})


# ans 14

import re

text = "Experience with SQL and NoSQL databases"
doc = nlp(text)

skills = set()
for token in doc:
    if token.text.lower() == "sql" and token.text.lower() != "nosql":
        skills.add("sql")

print(skills)


# ans 15

resume = "Python and SQL developer with communication skills"
job = "Looking for Python, NLP, SQL"

matcher = PhraseMatcher(nlp.vocab, attr="LOWER")
matcher.add("TECH", [nlp("python"), nlp("sql"), nlp("nlp")])

def extract(text):
    doc = nlp(text)
    return list(set([doc[start:end].text.lower() for _, start, end in matcher(doc)]))

resume_json = {"resume_skills": extract(resume)}
job_json = {"job_skills": extract(job)}

print(resume_json)
print(job_json)
