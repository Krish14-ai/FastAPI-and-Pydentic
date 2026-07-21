from fastapi import FastAPI,Query, HTTPException
from fastapi.responses import JSONResponse

from typing import Annotated,List, Literal
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
        primary_diagnosis : str
        allergies : List[str]
        status : str
        admission_date : date

class Patient(BaseModel):
    patient_id : str
    first_name : Annotated[
            str, 
            Field(..., description="Please enter your name", max_length= 100)
            ]
    last_name : Annotated[
                str,
                Field(..., description="Enter your last name")
                ]
    
    age : Annotated[
                int,
                Field(... , description = "Enter your age ", ge =0, le= 150)]

    gender : Annotated[
        Literal["Male", "Female", "Others"], 
        Field(..., description= " Enter your sex")
        ]
    blood_group :Literal[
                        "A+", "A-",
                        "B+", "B-",
                        "AB+", "AB-",
                        "O+", "O-"
]
    vitals : Vitals
    clinical_data : ClinicalData

    @computed_field
    @property
    def classification(self) -> str :
        if 0 < self.age < 18 : 
            return "minor"
        elif 18 <= self.age < 50: 
            return "adult"
        else:
            return "senior_citizen"
        

##----------------------------------------------------------------
## Code for Updating patients data 


##---------------------------------------------------------------


app = FastAPI()

@app.get('/')
def login_page():
    data = load_data()
    return data

@app.post("/create")
def create_patient(patient: Patient):

    data = load_data()      # Existing patients (list)

    # Check duplicate IDs
    if any(p["patient_id"] == patient.patient_id for p in data):
        raise HTTPException(
            status_code=409,
            detail="Patient already exists."
        )

    # Add new patient
    data.append(patient.model_dump(mode="json"))

    # Save updated list
    save_data(data)

    return {
        "message": "Patient added successfully"
    }

## Saving patient's Data
def save_data(data):
     with open(r"C:\Users\Krish\Downloads\FastApi\FastAPI\patients.json",'w') as f:
          json.dump(data,f)
    


## Loading patients Data
def load_data():
    path = r"C:\Users\Krish\Downloads\FastApi\FastAPI\patients.json"
    data = {}
    with open(path,'r') as f:
        data = json.load(f)
    return data

