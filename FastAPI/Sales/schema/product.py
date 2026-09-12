#=======================================================================================
## Imports
#=======================================================================================
from pydantic import( 
                    BaseModel,
                    Field,
                    field_validator,
                    computed_field,
                    model_validator,
                    EmailStr,
                    AnyUrl
                )
from typing import Annotated, Optional
from uuid import UUID
from typing import Dict
from datetime import datetime

#=======================================================================================


#=======================================================================================
## Seller Class
#=======================================================================================
class Seller(BaseModel):
    
## Attributes/Seller Data 
    id : UUID
    name : Annotated[
        str, 
        Field(
            max_length=50, 
            min_length=2,
            description= "Name of the Seller (2- 50 characters)",
            examples = ["Apple Store India", "Mi Store"]
        )]
    email : Annotated[EmailStr,Field(description= "Enter Sellers Email with Relavent Domains", examples=["techhub.com","audioworld.com"])]
    website : AnyUrl
    contact_1 : Annotated[
                        str,
                        Field(
                            min_length=10,
                            description= "Enter The Seller's Contact Number"
                        )
                        ]
    contact_2 : Optional[Annotated[
                        str, 
                        Field(
                            max_length= 10,
                            description= "Enter The Seller's Second Contact Number"
    )                    
    ]
    ]
    
#=======================================================================================
## Email Validator
#=======================================================================================
    @field_validator("email", mode = "after")
    @classmethod
    def seller_email_validator(cls, value : EmailStr):
        allowed_domains = [
                "techhub.com",
                "audioworld.com",
                "chargepro.com",
                "comfortworks.com",
                "ecogoods.com",
                "runfast.com",
                "urbanwear.com",
                "brighthome.com",
                "datastore.com",
                "booknest.com",
                "soundbox.com",
                "flexfit.com"
        ]
        
        domain = str(value).split("@")[-1].lower()
        if domain not in allowed_domains:
            raise ValueError(f"{domain} is not allowed please use another Domain, com = ['techhub.com','audioworld.com','chargepro.com',]")
        
        return value
#=======================================================================================
    
    
#=======================================================================================
## Product Class
#=======================================================================================
class Product_class(BaseModel):
    uid : UUID
    sku : Annotated[
                str,
                Field(
                    max_length= 50, 
                    min_length=12,
                    description= "Stock Keeping Unit",
                    examples= ["ELEC-BPS-011","SPRT-YGM-012"]    
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
    seller : Seller
    created_time : datetime


#=======================================================================================
    ## Validating SKU
#=======================================================================================
    @field_validator("sku", mode = "after")
    @classmethod
    def Validate_sku(cls , value: str):
        
        if "-" not in value : 
            raise ValueError("SKU must have '-' ")
        
        last = value.split("-")[-1]
        
        if not (len(last) == 3 and last.isdigit()):
            raise ValueError("SKU must end with 3-digit sequence like this '-234' ")
        
        return value
        

    ## For Validating Stocks
    @model_validator(mode = "after")
    def validate_business_rules(self):
        if self.stock == 0 and self.in_stock is True: 
            raise ValueError("If stock is 0, 'in_stock' must be 'False'")
        
        return self
#=======================================================================================