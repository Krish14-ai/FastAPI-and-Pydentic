from fastapi import FastAPI, HTTPException, Query, Path
import app
from app import Product
from schema.product import Product_class


app = FastAPI()


@app.get("/")
def root():
    # Simple health-check / welcome route
    return {"message": "welcome"}


@app.get("/products/all")
def get_everything():
    # Fetch every product with no filtering, sorting, or pagination
    products = Product.get_all_products()
    return {"message ": products}


@app.get("/products/{id}")
def get_product(id: int):
    # Fetch a single product by its numeric id
    return {"message": Product.get_product(id)}


## Filtering the product
@app.get("/products")
def list_products(
    name: str = Query(
        default=None, min_length=1, max_length=75,
        description="Search product by name (case insensitive)"
    ),  ## To get name of a Product
    sort_by_price: bool = Query(
        default=False, description="Sort products by price "
    ),  ## True for sorting, False for no Sorting
    order: bool = Query(
        default="asc", description="Sort Order when sort_by_price = ture (asc,desc)"
    ),  ## Ascending or Descinding
    limit: int = Query(
        default=5, ge=1, le=100, description="No Of items to return"
    ),  ## Total no of Items
    offset: int = Query(
        default=0, ge=0, le=100, description="Pagination offset"
    ),  ## No of Pages to have
):
    # Start with the full product list, then narrow it down step by step
    products = Product.get_all_products()

    # --- Name filter (case-insensitive substring match) ---
    if name:
        needle = name.strip().lower()
        products = [p for p in products if needle in p.get("name", "").lower()]

    # If nothing matched the name filter, tell the client instead of
    # returning an empty list silently
    if not products:
        raise HTTPException(status_code=404, detail=f"No product found named {name}")

    # --- Optional sort by price ---
    if sort_by_price:
        reverse = order == "desc"  ## for deciding Order
        products = sorted(products, key=lambda p: p.get("price", 0), reverse=reverse)

    # --- Pagination ---
    products = products[offset: offset + limit]
    total = len(products)  # NOTE: this counts only the current page, not the full filtered set

    return {"total": total, "limit": limit, "Items": products}



@app.get("/products/{product_id}")
def get_product_by_id(product_id : str = Path(..., min_length = 1, max_length = 2, description = "Product starts with 1")):
    products = Product.get_all_products()

    for p in products : 
        if p["id"] ==product_id :
            return p
    raise HTTPException(status_code = 404, detail = "Product not found")


@app.post("/products", status_code = 201)
def create_product(product: Product_class):
    return product.model_dump(mode = "json")
