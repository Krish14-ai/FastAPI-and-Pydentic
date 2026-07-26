import pandas as pd 
import numpy as np 
from sklearn.preprocessing import OneHotEncoder, LabelEncoder, StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, root_mean_squared_error

from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor

df = pd.read_csv(r"FastAPI\Insurance_premium_prediction_project\insurance.csv")

print(df.isna().sum())

X = df.drop(columns = ["expenses"])
y = df["expenses"]
##---------------------------------------------------------------------------

trf_1 = ColumnTransformer(transformers=[
    ("Scaler", StandardScaler(), ["age", "bmi", "children"]),
     ("encoder", OneHotEncoder(), ["sex", "smoker", "region"])
])
##---------------------------------------------------------------------------


pipe = Pipeline([
    ("preprocessor", trf_1),
    ("model", RandomForestRegressor(random_state=42))
])


X_train, X_test, y_train, y_test = train_test_split(
    X,y, test_size= 0.2, random_state= 42
)

pipe.fit(X_train,y_train)

y_pred = pipe.predict(X_test)

print(mean_absolute_error(y_test, y_pred))
print(root_mean_squared_error(y_pred, y_test))

