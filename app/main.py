from fastapi import FastAPI, HTTPException
from contextlib import asynccontextmanager
from app.schemas.Product import ProductRequest
from app.models.product import ProductResponse
from app.database import create_tables
from app.services.product_service import register_product, get_list_products, get_product_service, exclude_product, edit_product
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# CORS TODO: need to edit origens before up to production
app.add_middleware(
        CORSMiddleware,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
        allow_origin_regex=".*", # anyone can send things
    )

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_tables()
    yield
    

@app.get("/")
async def root():
    return {"message": "Market API running"}


@app.post("/products")
def create_product(product_request: ProductRequest):
    return register_product(product_request)


@app.get("/products")
def list_products():
    return get_list_products()


@app.get("/products/{id}")
def get_product(id: int):
    res = get_product_service(id)

    if res == None:
        raise HTTPException(status_code=404, detail="Product not found")
    
    return res



@app.delete("/products/{id}")
def delete_product(id: int):
    res = exclude_product(id)
    
    if res == None:
        raise HTTPException(status_code=404, detail="product not found to delete")
    
    return res


@app.put("/products/{id}")
def update_product(new_val: ProductRequest, id: int):
    res = edit_product(id, new_val)
    
    if res == None:
        raise HTTPException(status_code=404, detail="product not found to update")
    
    return res