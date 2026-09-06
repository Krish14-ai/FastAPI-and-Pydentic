from fastapi import FastAPI
import data

app = FastAPI()



@app.get('/')
def status():
    return {"message" : "Running"}

@app.get("/products/{id}")
def get_roducts(id: int):
    products = data.items
    return products[id]