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
    address: Address
    contact : List[str]

##--------------------------------------------------------------

address_dict = {'city':'bareilly', 
                'state': 'Uttar_Pradesh',
                'pincode': '243005'
                }

address = Address(**address_dict)

patient =  {
    "name" : "Krish",
    "age": 23, 
    "gender": 'Male',
    "address": address,
    "contact" : ["123456789"], 
}


patient_1 = Patient(**patient)
print(patient_1.address.city)