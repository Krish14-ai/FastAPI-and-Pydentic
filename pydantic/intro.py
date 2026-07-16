from pydantic import BaseModel, EmailStr, AnyUrl, Field
from typing import List,Dict, Optional, Annotated


class Patient(BaseModel):

    name : Annotated[str,Field(...,max_length= 100,title  = "Name of the Patient",
 description="Give the name of patient under 100 characters")]
    
    age :Annotated[ int , Field(..., ge = 0, le= 150,strict= True)]
    weight : Annotated[float,Field(..., ge = 0,le = 500,strict= True)]
    sex : str
    married : Annotated[bool, Field(default= False)]
    email : EmailStr
    contact : Dict[str , str] 
    allergies : Annotated[Optional[List[str]], Field(default= None, max_length= 30)]
    docs : AnyUrl

    
##--------------------------------------------------------------
    def insert_to_db(patient: Patient):
        print(patient.name,
               patient.age,
               patient.married,
                 patient,)

##---------------------------------------------------------------

patient_1 = {"name":"Krish",
            "age" : 20,
             "email" : "krish@gmail.com",
             "sex" : 'Male',
             "weight": 56.75,
             "married" : False,
             "email" : "krish@gmail.com",
             "allergies": ['penuts','pollen','flowers'],
             "docs" : "https://www.google.com",
             "contact" : {"Ph_1" : "1234567890"}
              }
patient = Patient(**patient_1)
Patient.insert_to_db(patient)

        
