from pydantic import BaseModel, Field
from typing import Annotated, Optional
from typing import Dict


class Product_class(BaseModel):
    id : int = 0
    name : Annotated[
                str, 
                Field(
                    max_length= 100, 
                    min_length= 0, 
                    title= "Product Name",
                    examples=["shoes", "phones"]
                    description= "Please Enter a product name"),
                    
                    ]
    category = Annotated[str, Field(description= "Enter the category of product")]
    price = Annotated[float,Field(description= "Enter the price", ge = 1) ]
    stock = Annotated[int, Field(description= "This is the total stock left ")]
    rating = Annotated[float, Field(gt =0, le =5 , description="Rating of Product")]
    in_stock = Annotated[bool, Field(description="Tells if the product is in stock")]
    seller = Annotated[Dict,Field(description="Details of seller")]

