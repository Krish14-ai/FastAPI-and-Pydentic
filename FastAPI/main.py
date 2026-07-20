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
  