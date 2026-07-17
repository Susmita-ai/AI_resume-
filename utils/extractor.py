import re
import spacy

# Load spaCy model
nlp = spacy.load("en_core_web_sm")


def extract_name(text):
    doc = nlp(text)
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            return ent.text
    return "Not Found"


def extract_email(text):
    match = re.search(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", text)
    return match.group(0) if match else "Not Found"


def extract_phone(text):
    match = re.search(r"\+?\d[\d\s\-]{8,15}\d", text)
    return match.group(0) if match else "Not Found"


SKILL_SET = [
    "python", "java", "c", "c++", "sql",
    "machine learning", "deep learning",
    "tensorflow", "keras", "pandas", "numpy",
    "matplotlib", "seaborn", "streamlit",
    "flask", "django", "git", "github"
]


def extract_skills(text):
    text = text.lower()
    skills = [skill for skill in SKILL_SET if skill in text]
    return list(set(skills))


def extract_education(text):
    education = [
        "b.tech", "btech", "m.tech", "mtech",
        "bca", "mca", "b.sc", "m.sc",
        "bachelor", "master", "phd", "diploma"
    ]

    text = text.lower()
    found = [edu for edu in education if edu in text]
    return list(set(found))