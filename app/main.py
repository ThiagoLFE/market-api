from fastapi import FastAPI, HTTPException
from app.schemas.Product import Product, ProductRequest

app = FastAPI()

# My database so for
products: list[Product] = []
NEXT_ID: int = 1

@app.get("/")
async def root():
    
    return {"message": "Market API running"}

@app.post("/products")
def new_product(product_request: ProductRequest):
    global NEXT_ID

    product = Product(id=NEXT_ID, name=product_request.name, price=product_request.price, stock=product_request.stock)
    products.append(product)
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
        raise HTTPException(status_code=404, detail="Product not found to delete")

    products.remove(product)
    return {"message": "Product deleted"}

@app.put("/products/{id}")
def update_product(new_val: ProductRequest, id: int):
    global products

    product = next((prod for prod in products if prod.id == id), None)
    
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found to edit")

    products.name = new_val.name
    products.price = new_val.price
    products.stock = new_val.stock

    return product 