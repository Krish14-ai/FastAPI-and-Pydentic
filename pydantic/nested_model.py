from pydantic import BaseModel, Field, field_validator, model_validator,AnyUrl
from typing import Dict, List, Optional, Annotated


class Address(BaseModel):
    city : str
    state : str
    pincode : str

##--------------------------------------------------------------
class Patient(BaseModel):
    name : Annotated[str, Field(..., max_length = 100)]
    age : Annotated[int,Field(..., ge = 0)]
    gender : str
    address: str
    contact : List[str]

##--------------------------------------------------------------