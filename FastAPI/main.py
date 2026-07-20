from fastapi import FastAPI,Query, HTTPException
from typing import Annotated, Dict,List, Literal
import json

from pydantic import Field, BaseModel, computed_field

class Patient(BaseModel):
    patient_id : str
    name : Annotated[str, Field(..., description="Please enter your name", max_length= 100)]
    last_name : Annotated[str, Field(..., description="Enter your last name")]
    age : Annotated[int,Field(... , description = "Enter your age ", ge =0, le= 150)]

    gender : Annotated[Literal["male", "female", "others"], str, Field(..., description= " Enter your sex")]
    blood_group : str
    vitals:Annotated[ Dict[str : float], Field(..., strict = False,description= "Plese enter your vitals")]
    clinical_data = Dict[str, str]
    status : str
    admission_date : str

    @computed_field
    @property
    def classification(self) -> str :
        if 0 < self.age < 18 : 
            return "minor"
        elif 18 <= self.age < 50: 
            return "adult"
        elif self.age > 50  :
            return "senior_citizen"
        
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
