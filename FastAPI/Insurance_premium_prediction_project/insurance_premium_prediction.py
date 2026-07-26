import pandas as pd
import numpy as np
import joblib

from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import mean_absolute_error, root_mean_squared_error, r2_score

from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor

DATA_PATH = r"FastAPI\Insurance_premium_prediction_project\insurance.csv"
MODEL_PATH = "model.joblib"


df = pd.read_csv(DATA_PATH)
print("Missing values per column:")
print(df.isna().sum())

df["smoker_bmi"] = np.where(df["smoker"] == "yes", df["bmi"], 0)

X = df.drop(columns=["expenses"])
y = df["expenses"]


numeric_features = ["age", "bmi", "children", "smoker_bmi"]
categorical_features = ["sex", "smoker", "region"]

preprocessor = ColumnTransformer(transformers=[
    ("scaler", StandardScaler(), numeric_features),
    # handle_unknown="ignore" prevents a crash if a category shows up at
    # inference time (e.g. in the FastAPI service) that wasn't in training data
    ("encoder", OneHotEncoder(handle_unknown="ignore"), categorical_features),
])

# ---------------------------------------------------------------------------
# Models: baseline (linear) vs random forest
# Fitting both tells you whether the extra complexity of RF is actually
# earning its keep over a simple linear model.
# ---------------------------------------------------------------------------
models = {
    "linear_regression": LinearRegression(),
    "random_forest": RandomForestRegressor(random_state=42, n_estimators=300),
}

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

results = {}
fitted_pipes = {}

for name, model in models.items():
    pipe = Pipeline([
        ("preprocessor", preprocessor),
        ("model", model),
    ])
    pipe.fit(X_train, y_train)

    y_train_pred = pipe.predict(X_train)
    y_test_pred = pipe.predict(X_test)

    # 5-fold CV MAE on the full dataset — a single 80/20 split on ~1300 rows
    # is noisy, so this gives a more stable estimate of generalization error
    cv_mae = -cross_val_score(
        pipe, X, y, cv=5, scoring="neg_mean_absolute_error"
    ).mean()

    results[name] = {
        "train_mae": mean_absolute_error(y_train, y_train_pred),
        "test_mae": mean_absolute_error(y_test, y_test_pred),
        "test_rmse": root_mean_squared_error(y_test, y_test_pred),
        "test_r2": r2_score(y_test, y_test_pred),
        "cv_mae_5fold": cv_mae,
    }
    fitted_pipes[name] = pipe

# ---------------------------------------------------------------------------
# Report
# A large gap between train_mae and test_mae signals overfitting;
# cv_mae_5fold being close to test_mae signals the single split wasn't a fluke.
# ---------------------------------------------------------------------------
print("\nModel comparison:")
for name, metrics in results.items():
    print(f"\n{name}")
    for k, v in metrics.items():
        print(f"  {k}: {v:.2f}")

# ---------------------------------------------------------------------------
# Persist the best pipeline (by test MAE) for the FastAPI service to load
# ---------------------------------------------------------------------------
best_name = min(results, key=lambda n: results[n]["test_mae"])
best_pipe = fitted_pipes[best_name]
joblib.dump(best_pipe, MODEL_PATH)
print(f"\nSaved best model ({best_name}) to {MODEL_PATH}")
