from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, computed_field
from typing import Annotated, Literal

import pandas as pd
import pickle

# --------------------------------------------------------------
with open("model.pkl", "rb") as f:
    model = pickle.load(f)

# Optional: Check the features expected by the model
print(model.feature_names_in_)

# --------------------------------------------------------------
class UserInput(BaseModel):

    age: Annotated[int, Field(..., description="Enter age of the user", gt=0, le=150)]
    weight: Annotated[float, Field(..., description="Enter your weight in kg", gt=0)]
    height: Annotated[float, Field(..., description="Enter your Height in meters", gt=0)]
    income_lpa: Annotated[float, Field(..., description="Enter your Income in LPA")]
    smoker: Annotated[bool, Field(..., description="Yes, if you smoke and No, If you don't")]
    city: Annotated[str, Field(..., description="Enter your Residential City")]
    occupation: Annotated[
        Literal[
            "retired",
            "freelancer",
            "student",
            "government_job",
            "business_owner",
            "unemployed",
            "private_job",
        ],
        Field(..., description="Enter your occupation"),
    ]

    # --------------------------------------------------------------

    @computed_field
    @property
    def bmi(self) -> float:
        return self.weight / (self.height ** 2)

    # --------------------------------------------------------------

    @computed_field
    @property
    def lifestyle_risk(self) -> str:

        if self.smoker and self.bmi > 30:
            return "high"

        elif self.smoker and self.bmi > 27:
            return "medium"

        else:
            return "low"

    # --------------------------------------------------------------

    @computed_field
    @property
    def age_group(self) -> str:

        if self.age > 50:
            return "senior"

        elif self.age > 18:
            return "adult"

        else:
            return "child"


# --------------------------------------------------------------

app = FastAPI()


@app.post("/predict")
def predict_premium(data: UserInput):

    input_df = pd.DataFrame(
        [
            {
                "age": data.age,
                "weight": data.weight,
                "height": data.height,
                "smoker": data.smoker,
                "city": data.city,
                "income_lpa": data.income_lpa,
                "occupation": data.occupation,
                "bmi": data.bmi,
                "age_group": data.age_group,
                "lifestyle_risk": data.lifestyle_risk,
            }
        ]
    )

    prediction = int(model.predict(input_df)[0])

    if prediction == 0:
        prediction = "Low"
    elif prediction == 1:
        prediction = "Medium"
    else :
        prediction = "High"
    return JSONResponse(
        status_code=200,
        content={"predicted_category": prediction},
    )