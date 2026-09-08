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
def list_products(name: str = Query(default=None, min_length=1, max_length=75, description="Search product by name (case insensitive)"), 
                  sort_by_price : bool = Query(default = False, description = "Sort products by price "),
                  order : bool = Query(default = "asc", description = "Sort Order when sort_by_price = ture (asc,desc)") ):
    
    products = Product.get_all_products()

    if name:
        needle = name.strip().lower()
        products = [p for p in products if needle in p.get("name", "").lower()]

    if not products:
        raise HTTPException(status_code=404, detail=f"No product found named {name}")

    if sort_by_price : 
        reverse = order == "desc"
        
    


    return products


