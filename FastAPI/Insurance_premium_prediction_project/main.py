
## Step 1): Make a model
## Step 2): Make API using FastAPI
## Step 3): Make UI using Streamlit

import pandas as pd
import numpy as np

from sklearn.preprocessing import OneHotEncoder, LabelEncoder, StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
from sklearn.ensemble import RandomForestClassifier

from pathlib import Path
import pickle


# ============================================================
# 1. LOAD DATA
# ============================================================

base_path = Path(__file__).resolve().parent
print("Base path:", base_path)

path = base_path / "data" / "patients.json"

with open(path, "r", encoding="utf-8") as f:
    df = pd.read_json(f)


# ============================================================
# 2. FLATTEN NESTED JSON DATA
# ============================================================

vitals = pd.json_normalize(df["vitals"])
clinical_data = pd.json_normalize(df["clinical_data"])

# Remove nested columns
df = df.drop(columns=["vitals", "clinical_data"])

# Remove duplicated vital columns if they already exist
duplicate_vitals = [
    "blood_pressure",
    "heart_rate_bpm",
    "temperature_c",
    "spO2_pct"
]

df = df.drop(
    columns=[
        col for col in duplicate_vitals
        if col in df.columns
    ],
    errors="ignore"
)

# Add flattened data
df = pd.concat(
    [
        df.reset_index(drop=True),
        vitals.reset_index(drop=True),
        clinical_data.reset_index(drop=True)
    ],
    axis=1
)


# ============================================================
# 3. CALCULATE BMI
# ============================================================

# Height is stored in centimeters.
# BMI requires height in meters.

df["height_m"] = df["height_cm"] / 100

df["bmi"] = (
    df["weight_kg"] /
    (df["height_m"] ** 2)
)


# ============================================================
# 4. CHECK DATA
# ============================================================

print("\nColumns:")
print(df.columns.tolist())

print("\nMissing values:")
print(df.isna().sum())

print("\nFirst 5 rows:")
print(df.head())


# ============================================================
# 5. CREATE TARGET
# ============================================================

# Your current patient JSON does NOT contain
# insurance_premium_category.
#
# Therefore, we use "status" as the prediction target
# for practicing the ML/FastAPI pipeline.

X = df.drop(
    columns=[
        "status",
        "patient_id",
        "first_name",
        "last_name",
        "admission_date"
    ]
)

y = df["status"]


# ============================================================
# 6. ENCODE TARGET
# ============================================================

label = LabelEncoder()

y = label.fit_transform(y)

print("\nTarget classes:")
print(label.classes_)


# ============================================================
# 7. DEFINE FEATURES
# ============================================================

numeric_features = [
    "age",
    "height_cm",
    "weight_kg",
    "height_m",
    "bmi",
    "heart_rate_bpm",
    "temperature_c",
    "spO2_pct"
]

categorical_features = [
    "gender",
    "blood_group",
    "blood_pressure",
    "primary_diagnosis"
]


# ============================================================
# 8. PREPROCESSING
# ============================================================

trf_1 = ColumnTransformer(
    transformers=[
        (
            "scaler",
            StandardScaler(),
            numeric_features
        ),
        (
            "encoder",
            OneHotEncoder(handle_unknown="ignore"),
            categorical_features
        )
    ]
)


# ============================================================
# 9. CREATE PIPELINE
# ============================================================

pipe = Pipeline(
    [
        ("preprocessor", trf_1),

        (
            "model",
            RandomForestClassifier(
                random_state=42,
                n_estimators=100
            )
        )
    ]
)


# ============================================================
# 10. TRAIN / TEST SPLIT
# ============================================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.4,
    random_state=42,
    stratify=y
)

# ============================================================
# 11. TRAIN MODEL
# ============================================================

pipe.fit(X_train, y_train)


# ============================================================
# 12. PREDICTION
# ============================================================

y_pred = pipe.predict(X_test)


# ============================================================
# 13. EVALUATION
# ============================================================

print("\nAccuracy:")
print(accuracy_score(y_test, y_pred))

print("\nClassification Report:")
print(
    classification_report(
        y_test,
        y_pred,
        target_names=label.classes_,
        zero_division=0
    )
)


# ============================================================
# 14. SAVE MODEL
# ============================================================

pickle_model_path = base_path / "model.pkl"

with open(pickle_model_path, "wb") as f:
    pickle.dump(
        {
            "model": pipe,
            "label_encoder": label
        },
        f
    )

print("\nModel saved at:")
print(pickle_model_path)


# ============================================================
# 15. DISPLAY UNIQUE VALUES
# ============================================================

print("\nGender:")
print(df["gender"].unique())

print("\nBlood groups:")
print(df["blood_group"].unique())

print("\nDiagnoses:")
print(df["primary_diagnosis"].unique())

print("\nStatuses:")
print(df["status"].unique())

