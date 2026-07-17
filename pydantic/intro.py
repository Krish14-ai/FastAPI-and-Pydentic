from pydantic import BaseModel, Field, field_validator, AnyUrl, EmailStr
from typing import List, Dict, Annotated, Optional

class Patient(BaseModel):
    name :  Annotated[str, Field(...,max_length= 100 )]
    age : Annotated[int, Field(..., ge = 0 , le = 150)]
    gender : str = Field(...)
    email : EmailStr
    allergies : Optional[List[str]] 
    contact : Dict[str, str]
    docs : AnyUrl
    
##--------------------------------------------------------------------------------
    ## Name validator
    @field_validator("name")
    @classmethod
    def name_validator(cls, name : str):

        if len(name) > 100 : 
            raise ValueError("Please enter a valid name under 100 characters ")
        
        else :
            return name
##--------------------------------------------------------------------------------

    ## Age Validator
    @field_validator("age")
    @classmethod
    def age_validator(cls, age: int)-> int:

        if  0 < age < 150:
             return age 
        
        else : 
            raise ValueError("Enter a valid age that is below 150 and above 0")
##--------------------------------------------------------------------------------

    ## Email Validator
    @field_validator("email")
    @classmethod
    def email_validator(cls, email : str)-> str:

        domain_name = str(email).split('@')[-1].lower()
        domains = ['hamster.com', 'cornhub.com','gmail.com']

        if domain_name not in domains:
            raise ValueError("Please Enter a Valid Domin in your email")
        else : 
            return email


##--------------------------------------------------------------------------------

patient_1 = {
    "name" : "Krish",
    "age" : 20,
    "gender" : 'Male',
    "email" : "Krish@GMAIL.com",
    "contact" : {"phone_1" : "123456789"},
    "docs" : "https://www.google.com/", 
    "allergies" : ['none']

}

info = Patient(**patient_1)
print(info)
