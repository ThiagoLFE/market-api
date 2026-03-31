from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
from app.schemas import ProductRequest, UserRequest, UserLogin, UserResponse, ProductResponse
from app.database import create_tables
from app.services import ProductService, UserService
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Depends
from app.security import get_current_user, get_current_admin
from app.exceptions import EmailAlreadyExistsError

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_tables()
    yield


app = FastAPI(lifespan=lifespan)


@app.exception_handler(EmailAlreadyExistsError)
def email_already_exists(request: Request, exc: EmailAlreadyExistsError):
    return JSONResponse(status_code=409, content={"Error": "Email already exists"})


# CORS TODO: need to edit origens before up to production
app.add_middleware(
        CORSMiddleware,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
        allow_origin_regex=".*", # anyone can send things
    )


@app.get("/")
async def root():
    return {"message": "Market API running"}

# Rotes

# Products
@app.post("/products", status_code=201, dependencies=[Depends(get_current_user)])
def create_product(product_request: ProductRequest) -> ProductResponse:
    product_service = ProductService()
    return product_service.register_product(product_request)


@app.get("/products", dependencies=[Depends(get_current_user)])
def list_products() -> list[ProductResponse]:
    product_service = ProductService()
    return product_service.list_products()


@app.get("/products/{id}", dependencies=[Depends(get_current_user)])
def get_product(id: int) -> ProductResponse:
    product_service = ProductService()
    res = product_service.get_product_service(id)

    if res == None:
        raise HTTPException(status_code=404, detail="Product not found")
    
    return res



@app.delete("/products/{id}", status_code=204, dependencies=[Depends(get_current_user)])
def delete_product(id: int) -> None:
    product_service = ProductService()
    res = product_service.exclude_product(id)
    
    if res == None:
        raise HTTPException(status_code=404, detail="product not found to delete")
    


@app.put("/products/{id}", dependencies=[Depends(get_current_user)])
def update_product(new_val: ProductRequest, id: int) -> ProductResponse:
    product_service = ProductService()
    res = product_service.edit_product(id, new_val)
    
    if res == None:
        raise HTTPException(status_code=404, detail="product not found to update")
    
    return res


# Rotes users

@app.post("/user", status_code=201)
def register_user(user_request: UserRequest) -> UserResponse:
    user_service = UserService()
    return user_service.register_user(user_request)


@app.post("/user/auth")
def login(auth: UserLogin) -> str:
    user_service = UserService()
    token = user_service.get_token(auth)

    if token is None:
        raise HTTPException(detail="Invalid credentials", status_code=401)
    
    return token