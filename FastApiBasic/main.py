from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn

app = FastAPI()

products = []

class BaseProduct(BaseModel):
    name: str
    price: float

class Product(BaseProduct):
    id: int

class ResponseProduct(BaseProduct):
    pass


@app.get("/", response_model=list[ResponseProduct], status_code=200)
async def get_products():
    return products

@app.get("/products/{product_id}", status_code=200)
async def get_product(product_id: int):
    for product in products:
        if product.id == product_id:
            return product
    raise HTTPException(status_code=404, detail="Product wurde nicht gefunden")

@app.put("/products/{product_id}", status_code=204)
async def update_product(product_id: int, product: Product):
    for index, existing_product in enumerate(products):
        if existing_product.id == product_id:
            products[index] = product
            return
    raise HTTPException(status_code=404, detail="Product wurde nicht gefunden")


@app.delete("/products/{product_id}", status_code=204)
async def delete_product(product_id: int):
    for index, existing_product in enumerate(products):
        if existing_product.id == product_id:
            products.pop(index)
            return
    raise HTTPException(status_code=404, detail="Product wurde nicht gefunden")


@app.post("/products", status_code=201)
async def create_product(product: Product):
    products.append(product)




if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=4444)