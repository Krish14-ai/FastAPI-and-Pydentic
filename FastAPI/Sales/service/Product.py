from fastapi import FastAPI
from typing import List, Dict
from pathlib import Path
import json

app = FastAPI()

base_path = Path(__file__).resolve().parent.parent
path = base_path/"data"/"dummy.json"

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
def get_all_products() -> list[Dict]:
    return load_products()


## Save a new Product
def save_product(new_product : List[Dict]) -> None:
    with open(path,'w', encoding= "utf-8") as f:
        json.dump(new_product, f, indent=2,ensure_ascii= False)
    

## Add Prodct
def add_product(new_product : Dict) -> Dict:
    products = get_all_products()
    
    if any(p["sku"] == new_product["sku"] for p in products):
        raise ValueError("SKU already exist")
    
    products.append(new_product)
    save_product(products)
    return new_product