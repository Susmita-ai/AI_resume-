import pandas as pd
import joblib

from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import LabelEncoder, OneHotEncoder, StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report


df = pd.read_csv("data/AI_Resume_Screening.csv")

df = df.drop_duplicates()

df = df.fillna("Unknown")

X = df[
    [
        "Skills",
        "Experience (Years)",
        "Education",
        "Certifications",
        "Salary Expectation ($)",
        "Projects Count",
        "AI Score (0-100)"
    ]
]

y = df["Job Role"]

label_encoder = LabelEncoder()
y = label_encoder.fit_transform(y)

numeric_features = [
    "Experience (Years)",
    "Salary Expectation ($)",
    "Projects Count",
    "AI Score (0-100)"
]

categorical_features = [
    "Skills",
    "Education",
    "Certifications"
]

numeric_transformer = Pipeline(
    steps=[
        ("imputer", SimpleImputer(strategy="median")),
        ("scaler", StandardScaler())
    ]
)

categorical_transformer = Pipeline(
    steps=[
        ("imputer", SimpleImputer(strategy="most_frequent")),
        ("encoder", OneHotEncoder(handle_unknown="ignore"))
    ]
)

preprocessor = ColumnTransformer(
    transformers=[
        ("num", numeric_transformer, numeric_features),
        ("cat", categorical_transformer, categorical_features)
    ]
)

model = Pipeline(
    steps=[
        ("preprocessor", preprocessor),
        ("classifier", RandomForestClassifier(
            n_estimators=200,
            random_state=42
        ))
    ]
)

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)
model.fit(X_train, y_train)
pred = model.predict(X_test)

print("Accuracy :", accuracy_score(y_test, pred))
print(classification_report(y_test, pred))

joblib.dump(model, "model/model.pkl")
joblib.dump(label_encoder, "model/label_encoder.pkl")

print("Model Saved Successfully")