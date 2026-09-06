from fastapi import FastAPI, HTTPException, Query
import Product

app = FastAPI()

@app.get("/")
def root():
    return {"message" : "welcome"}


@app.get("/products/all")
def get_everything():
    products = Product.get_all_products()
    return {"message " : products}


@app.get("/products/{id}")
def get_product(id : int):
    return {"message" : Product.get_product(id)}

@app.get("/products")
def list_products(name: str = Query( default = None, min_length = 1, max_length = 75, description  ="Search product by name (case insensitive)") ):

    product = Product.get_all_products()
    if name : 
        needle = name.strip().lower()
        Product = [p for p in product if needle in p.get("name","")]

    return name