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
    category = Annotated[str, Field(description= "Enter the category of product")]
    price = Annotated[float,Field(description= "Enter the price", ge = 1) ]


 "name": "Shoes",
    "category": "Sports",
    "price": 89.95,
    "stock": 31,
    "rating": 4.5,
    "in_stock": true,
    "seller": {
      "name": "RunFast",
      "country": "V