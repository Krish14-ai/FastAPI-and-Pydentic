from pydantic import BaseModel, Field
from typing import Annotated



class Product_class(BaseModel):
    id : int = 0
    name : Annotated[
                str, 
                Field(
                    max_length= 100, 
                    min_length= 0, 
                    description= "Please Enter a product name")
                    ]
