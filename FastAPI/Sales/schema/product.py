from pydantic import BaseModel, Field, field_validator, computed_field, model_validator
from typing import Annotated, Optional
from uuid import UUID
from typing import Dict
from datetime import datetime

class Product_class(BaseModel):
    uiid : UUID
    sku : Annotated[
                str,
                Field(
                    max_length= 50, 
                    min_length=12,
                    description= "Stock Keeping Unit",
                    examples=["ELEC-BPS-011","SPRT-YGM-012"]    
                    )]
    name : Annotated[
                str, 
                Field(
                    max_length= 100, 
                    min_length= 0, 
                    title= "Product Name",
                    examples=["shoes", "phones"],
                    description= "Please Enter a product name"
                    )
                    ]
    category : Annotated[str, Field(description= "Enter the category of product")]
    price : Annotated[float,Field(description= "Enter the price", ge = 1) ]
    stock : Annotated[int, Field(description= "This is the total stock left ")]
    rating : Annotated[float, Field(gt =0, le =5 , description="Rating of Product")]
    in_stock : Annotated[bool, Field(description="Tells if the product is in stock")]
    seller : Annotated[Dict, Field(description="Details of Seller")]
    
    created_time : datetime


    ## Validating SKU
    @field_validator("sku", mode = "after")
    def Validate_sku():
        pass
