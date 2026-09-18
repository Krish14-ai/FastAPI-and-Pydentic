from typing import List, Dict
from pathlib import Path
import json


base_path = Path(__file__).resolve().parent.parent
data_path = base_path/"data"
path = data_path/"products.json"

## To get a specific Product
def get_product_by_id(id : str):
    if not path.exists() : 
        raise FileNotFoundError("Data not found")

    
    with open(path,'r')as f :
        products = json.load(f)
    
    for p in products:
        if p["uid"] == id:
            return p
    return {"message": "Product not found"}



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


## Deleting a Product
def remove_product(id : str):
    products = get_all_products()
    deleted = {}
    for idx, p in enumerate(products):
        if p["uid"] == id:
            deleted = products.pop(idx)
            save_product(products)
            return {"messege" : f"{deleted} has been deleted from the Data"}
        

## Updating
def Update_product(product_id : str, update_data : Dict):
    products = get_all_products()
    
    for idx, product in enumerate(products):
        
        if  product["uid"] == product_id :
            for key,value in update_data.items():
                
                if isinstance(value, dict) and isinstance(product.get(key), dict):
                    product[key].update(value)
                
                else : 
                    product[key] = value
                    
            products[idx] = product
            save_product(products)
            return product
            
    raise ValueError("Product not found!")
