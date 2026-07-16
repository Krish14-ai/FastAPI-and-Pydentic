from pydantic import BaseModel, EmailStr, Field, AnyUrl, field_validator, model_validator
from typing import Annotated, Dict, List, Optional

class Patient(BaseModel):

    name : Annotated[str,Field(..., max_length = 100, title= "Enter Your name")]
    age : Annotated[int, Field(..., ge =0 , le = 150, strict = True)]
    weight : Annotated[float,Field(...,ge = 0, strict = True)]
    gender : Annotated[str, Field(...,)]
    email : EmailStr
    insurance : bool
    profile_link : AnyUrl  = None
    allergies : Annotated[List[str], Field(max_length= 10,default= None)]
    contact : Dict[str, str]
    emergency_num : Dict[str,str]
##--------------------------------------------------------------

    ## Name Validator 

    @field_validator("name")
    @classmethod
    def name_validator(cls,name):
        if len(name) not in range(20):
            raise NameError("Entere a valide name")
        else : 
            return name.lower()       

##--------------------------------------------------------------

    ## Email Validator

    @field_validator('email')
    @classmethod
    def email_validator(cls, value):
        valid_domains = ['hdfc.com','icici.com','gmail.com']
        domain_name = value.split('@')[-1]

        if domain_name not in valid_domains:
            print("Its not a valid domain")
            raise ValueError("Enter a propper mail")
        return  value
##--------------------------------------------------------------

    ## Age Validator

    @field_validator( 'age' ,mode = "after")
    @classmethod
    def age_validator(cls , value): 
        if 0 < value < 150:  
            return value
        else: 
            raise ValueError("enter age in range of 1 to 150")
        

##---------------------------------------------------------------

## Checking for emergency contact number for patients who are above 60 years of age 
    @model_validator(mode = "after")
    def emergency_contact(value):
        if value.age > 60 and 'emergency_num' not in value.emergency_num:
            raise  ValueError("Patients older that 60 years must have an Emergency contact")
        else : 
            return value
##--------------------------------------------------------------
    ## info
    def show_details(info : Patient):
        print(info)

##------------------------------------------------------------------------------

patient_1 = {
    "name" : "Krish",
    "age": 23, 
    "weight" : 60,   
    "gender": 'Male',
    "email" : "krish@gmail.com",
    "contact" : {"Number_1 " : "123456789"}, 
    "insurance" : True,
    "emergency_num": {"Son":"987654321"}

}

info = Patient(**patient_1)
Patient.show_details(info)
