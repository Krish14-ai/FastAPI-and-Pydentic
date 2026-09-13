from fastapi import FastAPI, HTTPException, Query, Path
from service import Product
from Product import get_all_products, add_product
from schema.product import Product_class
from typing import Literal


app = FastAPI()


@app.get("/")
def root():
    return {"message": "welcome"}


@app.get("/products/all")
def get_everything():
    products = get_all_products()
    return {"message": products}


# Get a specific product using UID
@app.get("/products/{uid}")
def get_product(uid: str):
    try:
        return {"message": get_product(uid)}
    except ValueError:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )


@app.get("/products")
def list_products(
    name: str = Query(
        default=None,
        min_length=1,
        max_length=75,
        description="Search product by name (case insensitive)"
    ),

    sort_by_price: bool = Query(
        default=False,
        description="Sort products by price"
    ),

    order: Literal["asc", "desc"] = Query(
        default="asc",
        description="Sort order"
    ),

    limit: int = Query(
        default=5,
        ge=1,
        le=100,
        description="No Of items to return"
    ),

    offset: int = Query(
        default=0,
        ge=0,
        description="Pagination offset"
    ),
):

    products = Product.get_all_products()

    # Filter by name
    if name:
        needle = name.strip().lower()

        products = [
            p for p in products
            if needle in p.get("name", "").lower()
        ]

    # Stop if no products match
    if not products:
        raise HTTPException(
            status_code=404,
            detail=f"No product found named {name}"
        )

    # Sort by price
    if sort_by_price:
        reverse = order == "desc"

        products = sorted(
            products,
            key=lambda p: p.get("price", 0),
            reverse=reverse
        )

    # Total BEFORE pagination
    total = len(products)

    # Pagination
    products = products[offset:offset + limit]

    return {
        "total": total,
        "limit": limit,
        "offset": offset,
        "Items": products
    }


# Create product
@app.post("/products", status_code=201)
def create_product(product: Product_class):

    product_dict = product.model_dump(mode="json")

    Product.add_product(product_dict)

    try :
        add_product(product_dict)
    except ValueError as e: 
        raise HTTPException(status_code  =400, detail =str(e) )
    return product.model_dump(mode = "json")