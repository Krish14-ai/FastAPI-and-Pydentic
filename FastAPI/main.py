from fastapi import FastAPI,Query, HTTPException
from typing import Annotated, Dict,List, Literal
import json
from datetime import date
from pydantic import Field, BaseModel, computed_field

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
        elif self.age > 50  :
            return "senior_citizen"
        

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



##---------------------------------------------------------------


app = FastAPI()

@app.get('/')
def login_page():
    data = load_data()
    return data

@app.post("/create")
def create_patient(patient : Patient):
    pass 


def load_data():
    path = r"C:\Users\Krish\Downloads\FastApi\FastAPI\patients.json"
    data = {}
    with open(path,'r') as f:
        data = json.load(f)
    return data
