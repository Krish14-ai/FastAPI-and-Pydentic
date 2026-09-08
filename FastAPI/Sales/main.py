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
def list_products(name: str = Query(default=None, min_length=1, max_length=75, description="Search product by name (case insensitive)"),## To get name of a Product
                  sort_by_price : bool = Query(default = False, description = "Sort products by price "), ## True for sorting, False for no Sorting
                  order : bool = Query(default = "asc", description = "Sort Order when sort_by_price = ture (asc,desc)"), ## Ascending or Descinding 
                   limit : int = Query(default = 5,ge = 1, le =100 , description = "No Of items to return"), ## Total no of Items
                 offset : int = Query(default= 0, ge =0 , le = 100, description = "Pagination offset") ): ## No of Pages to have
    
    products = Product.get_all_products()

    if name:
        needle = name.strip().lower()
        products = [p for p in products if needle in p.get("name", "").lower()]

    if not products:
        raise HTTPException(status_code=404, detail=f"No product found named {name}")

    if sort_by_price : 
        reverse = order == "desc"    ## for deciding Order
        products = sorted(products,key = lambda p : p.get("price",0), reverse = reverse )

    products = products[offset: offset+  limit]
    total = len(products)

    return {"total" : total, "limit" : limit, "Items" : products}


