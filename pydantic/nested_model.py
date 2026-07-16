from pydantic import BaseModel, Field, EmailStr
from typing import  List, Optional, Annotated


class Address(BaseModel):
    city : str
    state : str
    pincode : str

##--------------------------------------------------------------
class Patient(BaseModel):
    name : Annotated[str, Field(..., max_length = 100)]
    age : Annotated[int,Field(..., ge = 0)]
    gender : str
    email: EmailStr = "anc@gmail.com"
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
    "email": "krihs@gmail.com",
    "address": address,
    "contact" : ["123456789"], 
}


patient_1 = Patient(**patient)
print(patient_1.address.city)

## For exporting objects as a dictonary
temp= patient_1.model_dump()
print(temp)
print(type(temp),'\n')

## For exporting data as json
temp_json = patient_1.model_dump_json()
print(temp_json)
print(type(temp_json))

## if we want some specific properties to be exported as a dictionary or json
temp_filtered= patient_1.model_dump(include=['name'])
print("Filtered data : " ,temp_filtered)

## If we want to exclude some data
temp_excluded = patient_1.model_dump(exclude=['name','age'])
print("Excluded : ",temp_excluded,'\n')

## If we want to exclude unset default vlaues
exclude_unset = patient_1.model_dump(exclude_unset= True)
print("Unset Values: ",exclude_unset)