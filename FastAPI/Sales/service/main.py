from fastapi import FastAPI, HTTPException, Query, Path

from service import Product
from schema.product import Product_class


app = FastAPI()


@app.get("/")
def root():
    # Simple health-check / welcome route
    return {"message": "welcome"}


@app.get("/products/all")
def get_everything():
    # Fetch all products without filtering or pagination
    products = Product.get_all_products()
    return {"message ": products}


@app.get("/products/{id}")
def get_product(id: int):
    # Fetch a single product using its ID
    return {"message": Product.get_product(id)}


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
    order: bool = Query(
        default="asc",
        description="Sort Order when sort_by_price = true (asc, desc)"
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
        le=100,
        description="Pagination offset"
    ),
):
    products = Product.get_all_products()

    # Filter by name using a case-insensitive substring match
    if name:
        needle = name.strip().lower()
        products = [
            p for p in products
            if needle in p.get("name", "").lower()
        ]

    # Stop if no products match the filter
    if not products:
        raise HTTPException(
            status_code=404,
            detail=f"No product found named {name}"
        )

    # Sort by price when requested
    if sort_by_price:
        reverse = order == "desc"
        products = sorted(
            products,
            key=lambda p: p.get("price", 0),
            reverse=reverse
        )

    # Return only the requested page of results
    products = products[offset: offset + limit]
    total = len(products)

    return {
        "total": total,
        "limit": limit,
        "Items": products
    }


@app.get("/products/{product_id}")
def get_product_by_id(
    product_id: str = Path(
        ...,
        min_length=1,
        max_length=2,
        description="Product starts with 1"
    )
):
    products = Product.get_all_products()

    # Search for the product with the requested ID
    for p in products:
        if p["id"] == product_id:
            return p

    raise HTTPException(status_code=404, detail="Product not found")


@app.post("/products", status_code=201)
def create_product(product: Product_class):
    # Convert the validated Pydantic model into JSON-compatible data
    return product.model_dump(mode="json")