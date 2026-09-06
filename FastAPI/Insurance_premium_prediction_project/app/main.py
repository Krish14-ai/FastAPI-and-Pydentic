## Step 1): Make a model
## Step 2): Make API using FastAPI
## Step 3): Make UI using streamlit


import pandas as pd 
import numpy as np 
from sklearn.preprocessing import OneHotEncoder, LabelEncoder, StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score,classification_report
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from pathlib import Path

df = pd.read_csv("FastAPI\Insurance_premium_prediction_project\data\insurance.csv")

df["bmi"]  = df["weight"] / df["height"]**2

print(df.isna().sum())

X = df.drop(columns = ["insurance_premium_category"])
y = df["insurance_premium_category"]
##---------------------------------------------------------------------------

trf_1 = ColumnTransformer(transformers=[
    ("scaler", StandardScaler(), ["age", "weight", "height", "income_lpa"]),
    ("encoder", OneHotEncoder(handle_unknown="ignore"), ["smoker", "city", "occupation"]),
])
##---------------------------------------------------------------------------


pipe = Pipeline([
    ("preprocessor", trf_1),
    ("model", RandomForestClassifier(random_state=42))
])

label = LabelEncoder()
y = label.fit_transform(y)

X_train, X_test, y_train, y_test = train_test_split(
    X,y, test_size= 0.2, random_state= 42
)

pipe.fit(X_train,y_train)

y_pred = pipe.predict(X_test)

print(accuracy_score(y_test, y_pred))
print(classification_report(y_pred, y_test))

import pickle 

pickle_model_path = "model.pkl"
with open(pickle_model_path, "wb") as f:
    pickle.dump(pipe,f)

print(df["occupation"].unique())