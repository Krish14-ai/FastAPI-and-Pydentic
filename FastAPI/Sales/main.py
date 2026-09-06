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
    return {"messege" : Product.get_product(id)}

@app.get("/proucts")
def list_products(name: str = Query(default = None, min_length = 1, max_length = 75, description = "Search product by name (case insensitive)", ) ):
    return name 