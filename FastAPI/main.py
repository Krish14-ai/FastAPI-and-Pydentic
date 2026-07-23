from fastapi import FastAPI, Query, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from typing import Annotated, List, Literal, Optional
import json

from datetime import date
from pydantic import Field, BaseModel, computed_field

##----------------------------------------------------------------------
## Code for creating a patient

class Vitals(BaseModel):
    blood_pressure: str
    heart_rate_bpm: int
    temperature_c: float
    spO2_pct: int


class ClinicalData(BaseModel):
    primary_diagnosis: str
    allergies: List[str]
    status: str
    admission_date: date


class Patient(BaseModel):
    patient_id: str

    first_name: Annotated[
        str,
        Field(..., description="Please enter your name", max_length=100)
    ]

    last_name: Annotated[
        str,
        Field(..., description="Enter your last name")
    ]

    age: Annotated[
        int,
        Field(..., description="Enter your age", ge=0, le=150)
    ]

    gender: Annotated[
        Literal["Male", "Female", "Others"],
        Field(..., description="Enter your sex")
    ]

    blood_group: Literal[
        "A+", "A-",
        "B+", "B-",
        "AB+", "AB-",
        "O+", "O-"
    ]

    vitals: Vitals
    clinical_data: ClinicalData

    @computed_field
    @property
    def classification(self) -> str:
        if 0 < self.age < 18:
            return "minor"
        elif 18 <= self.age < 50:
            return "adult"
        else:
            return "senior_citizen"


##----------------------------------------------------------------
## Code for Updating patients data

class Update_Patient(BaseModel):

    patient_id: Optional[str] = None
    first_name: Annotated[Optional[str], Field(default=None)]
    last_name: Annotated[Optional[str], Field(default=None)]
    age: Annotated[Optional[int], Field(default=None)]
    gender: Annotated[
        Optional[Literal["Male", "Female", "Others"]],
        Field(default=None)
    ]

    blood_group: Optional[
        Literal[
            "A+", "A-",
            "B+", "B-",
            "AB+", "AB-",
            "O+", "O-"
        ]
    ] = None

    vitals: Annotated[Optional[Vitals], Field(default=None)]
    clinical_data: Annotated[Optional[ClinicalData], Field(default=None)]


##---------------------------------------------------------------

app = FastAPI()


@app.get('/')
def login_page():
    data = load_data()
    return data


@app.post("/create")
def create_patient(patient: Patient):

    data = load_data()

    if any(p["patient_id"] == patient.patient_id for p in data):
        raise HTTPException(
            status_code=409,
            detail="Patient already exists."
        )

    data.append(patient.model_dump(mode="json"))

    save_data(data)

    return {
        "message": "Patient added successfully"
    }


## Saving patient's Data
def save_data(data):
    with open(r"C:\Users\Krish\Downloads\FastApi\FastAPI\patients.json", "w") as f:
        json.dump(
            jsonable_encoder(data),
            f,
            indent=4
        )


## Loading patients Data
def load_data():
    path = r"C:\Users\Krish\Downloads\FastApi\FastAPI\patients.json"

    data = []

    with open(path, "r") as f:
        data = json.load(f)

    return data


## Updating Patient
@app.put("/edit/{patient_id}")
def update_patient(patient_id: str, patient_update: Update_Patient):

    data = load_data()

    for patient in data:

        if patient["patient_id"] == patient_id:

            updates = patient_update.model_dump(
                exclude_unset=True,
                mode="json"
            )
            if patient["patient_id"] == patient_id
            patient.update(updates)
            id = patient["patient_id"]
            data[id] = patient

            save_data(data)

            return {
                "message": "Data Updated Successfully",
                "Patient": patient
            }

    raise HTTPException(
        status_code=404,
        detail="Patient not found"
    )