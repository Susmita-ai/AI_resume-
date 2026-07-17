from utils.parser import extract_text_from_pdf

from utils.extractor import (
    extract_name,
    extract_email,
    extract_phone,
    extract_skills,
    extract_education
)

from utils.predictor import predict_job_role

# Read Resume
text = extract_text_from_pdf("uploads/resume.pdf")

# Extract Information
name = extract_name(text)
email = extract_email(text)
phone = extract_phone(text)
skills = extract_skills(text)
education = extract_education(text)

print("="*50)
print("Name :", name)
print("Email :", email)
print("Phone :", phone)
print("Skills :", skills)
print("Education :", education)

# ------------------------
# Prepare model input
# ------------------------

resume_data = {
    "Skills": ", ".join(skills),
    "Experience (Years)": 2,
    "Education": education[0] if education else "b.tech",
    "Certifications": "No",
    "Salary Expectation ($)": 50000,
    "Projects Count": 3,
    "AI Score (0-100)": 75
}

try:
    role = predict_job_role(resume_data)

    print("\nPredicted Job Role :", role)

except Exception as e:
    print("\nPrediction Error:", e)