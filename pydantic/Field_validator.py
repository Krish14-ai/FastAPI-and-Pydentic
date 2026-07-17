from pydantic import BaseModel, EmailStr, Field, AnyUrl, field_validator, model_validator, computed_field
from typing import Annotated, Dict, List, Optional

class Patient(BaseModel):

    name : Annotated[str,Field(..., max_length = 100, title= "Enter Your name")]
    age : Annotated[int, Field(..., ge =0 , le = 150, strict = True)]
    weight : Annotated[float,Field(...,ge = 0, strict = True)]
    height : Annotated[float,Field(...,ge= 0, strict = True)]
    gender : Annotated[str, Field(...,)]
    email : EmailStr
    insurance : bool
    profile_link : AnyUrl  = None
    allergies : Annotated[List[str], Field(max_length= 10,default= None)]
    contact : Dict[str, str]
    emergency_num : Optional[Dict[str,str]]

