from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from app.schemas.Product import Product, ProductRequest

app = FastAPI()

# My database so for
products: list[Product] = []
NEXT_ID: int = 1

@app.get("/")
async def root():
    
    return {"message": "Market API running"}

@app.post("/products")
def new_product(product: ProductRequest):
    global NEXT_ID
    products.append(Product(id=NEXT_ID, name=product.name, price=product.price, stock=product.stock))
    NEXT_ID += 1

    return product

@app.get("/products")
def list_products():
    return products

@app.get("/products/{id}")
def get_product_by_id(id: int):

    for product in products:
        if product.id == id:
            return product
    
    raise HTTPException(status_code=404, detail="Product not found")

@app.delete("/products/{id}")
def delete_product_by_id(id: int):
    global products

    product = next((prod for prod in products if prod.id == id ), None)
    
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")

    products.remove(product)
    return {"message": "Product deleted"}