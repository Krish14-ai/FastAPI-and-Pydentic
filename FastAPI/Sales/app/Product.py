from fastapi import FastAPI
from typing import List, Dict
from pathlib import Path
import json

app = FastAPI()

base_path = Path(__file__).resolve().parent
path = base_path/"data"/"products.json"

## To get a specific Product
def get_product(id : int):
    if not path.exists() : 
        raise FileNotFoundError("Data not found")

     
    with open(path,'r')as f :
        products = json.load(f)

    return products[id]


## Returns all the Products
def load_products() -> List[Dict]:
    
    if not path.exists() : 
        return []

    with open(path,'r') as f:
        return json.load(f)


## to get all the Products
def get_all_products() -> List[Dict]:
    return load_products()

    