import joblib
import pandas as pd

# Load trained model and the label encoder used during training
model = joblib.load("model/model.pkl")
label_encoder = joblib.load("model/label_encoder.pkl")


def predict_job_role(features):
    """
    features: dict with keys matching the columns used in train_model.py:
        Skills, Experience (Years), Education, Certifications,
        Salary Expectation ($), Projects Count, AI Score (0-100)
    """
    df = pd.DataFrame([features])

    encoded_prediction = model.predict(df)[0]

    # Convert the numeric label back into the original job role string
    job_role = label_encoder.inverse_transform([encoded_prediction])[0]

    return job_role
