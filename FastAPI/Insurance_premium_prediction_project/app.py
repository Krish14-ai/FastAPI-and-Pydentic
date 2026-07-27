from fastapi import FastAPI
from pydantic import BaseModel, Field, computed_field
from typing import Annotated, Literal

class UserInput(BaseModel):

    age : Annotated[int, Field(..., description= "Enter age of the user", gt = 0, le = 150)]
    weight : Annotated[float, Field(..., description= "Enter your weight in kg", gt = 0)]
    height : Annotated[float, Field(..., description= "Enter your Height in meters", gt = 0)]
    income_lpa : Annotated[float, Field(..., description= "Enter your Income in LPA")]
    smoker : Annotated[bool, Field(..., description= "Yes, if you smoke and No, If you don't")]
    city : Annotated[str, Field(..., description="Enter your Resindatal City")]
    occupation : Annotated[Literal[
        'retired','freelancer','student','government_job','business_owner','unemployed','private_job'
    ],   Field(..., description="Enter your occupation")]

##---------------------------------------------------------------

@computed_field
@property
def bmi(self) -> float:
    return self.weight/ self.height**2

##----------------------------------------------------------------

@computed_field
@property
def lifestyle_risk(self) -> str:

    if self.smoker and self.bmi > 30 :
        return "high"
    
    elif self.smoker and self.bmi > 27:
        return "medium"
    
    else : 
        return "low"

##------------------------------------------------------------------

@computed_field
@property
def age_group(self) ->str : 
    if self.age > 50 :
        return "senior "
    elif self.age > 18 : 
        return "adult"
    else :
        return "child"

##------------------------------------------------------------------

