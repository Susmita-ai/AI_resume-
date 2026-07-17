import os
import tempfile
import streamlit as st

from utils.parser import extract_text_from_pdf, extract_text_from_image
from utils.extractor import (
    extract_name,
    extract_email,
    extract_phone,
    extract_skills,
    extract_education,
)
from utils.predictor import predict_job_role
from utils.scorer import calculate_score
from utils.report_generator import generate_pdf_report

st.set_page_config(page_title="AI Resume Analyzer", page_icon="📄", layout="centered")

st.title("📄 AI Resume Analyzer")
st.write("Upload your resume (PDF, JPG, or PNG) and get an instant analysis.")

uploaded_file = st.file_uploader(
    "Upload your resume",
    type=["pdf", "jpg", "jpeg", "png"],
)

if uploaded_file is not None:
    file_ext = uploaded_file.name.split(".")[-1].lower()

    # Save the uploaded file to a temp location so parser functions
    # (which expect a file path) can read it.
    with tempfile.NamedTemporaryFile(delete=False, suffix=f".{file_ext}") as tmp_file:
        tmp_file.write(uploaded_file.getbuffer())
        temp_path = tmp_file.name

    resume_text = ""
    with st.spinner("Reading your resume..."):
        try:
            if file_ext == "pdf":
                resume_text = extract_text_from_pdf(temp_path)
            else:
                resume_text = extract_text_from_image(temp_path)
        except Exception as e:
            st.error(
                f"Couldn't read this file — it may be corrupted or not a "
                f"valid {file_ext.upper()}. ({e})"
            )

    os.remove(temp_path)

    if not resume_text or not resume_text.strip():
        st.error(
            "Couldn't extract any text from this file. "
            "Please make sure it's a valid, non-empty, readable resume."
        )
    else:
        with st.spinner("Analyzing resume..."):
            name = extract_name(resume_text)
            email = extract_email(resume_text)
            phone = extract_phone(resume_text)
            skills = extract_skills(resume_text)
            education = extract_education(resume_text)
            score = calculate_score(skills, education)

            # Must match the columns used when the model was trained.
            resume_data = {
                "Skills": ", ".join(skills),
                "Experience (Years)": 2,
                "Education": education[0] if education else "b.tech",
                "Certifications": "No",
                "Salary Expectation ($)": 50000,
                "Projects Count": 3,
                "AI Score (0-100)": score,
            }

            predicted_role = "Not Available"
            try:
                predicted_role = predict_job_role(resume_data)
            except Exception as e:
                st.warning(f"Prediction failed: {e}")

        st.success("Analysis complete!")

        col1, col2 = st.columns(2)
        with col1:
            st.subheader("👤 Extracted Info")
            st.write(f"**Name:** {name}")
            st.write(f"**Email:** {email}")
            st.write(f"**Phone:** {phone}")
            st.write(
                f"**Education:** {', '.join(education) if education else 'Not Found'}"
            )

        with col2:
            st.subheader("📊 Results")
            st.metric("Resume Score", f"{score}/100")
            st.write(f"**Predicted Job Role:** {predicted_role}")

        st.subheader("🛠️ Skills Detected")
        st.write(", ".join(skills) if skills else "No matching skills found.")

        with st.expander("View extracted raw text"):
            st.text(resume_text)

        pdf_bytes = generate_pdf_report(
            name=name,
            email=email,
            phone=phone,
            education=education,
            skills=skills,
            score=score,
            predicted_role=predicted_role,
        )
        st.download_button(
            label="📥 Download PDF Report",
            data=pdf_bytes,
            file_name="resume_analysis_report.pdf",
            mime="application/pdf",
        )
else:
    st.info("👆 Upload a PDF or image resume to get started.")
