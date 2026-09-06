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
def list_products(name: str, ):
    return name 