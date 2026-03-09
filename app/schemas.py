from pydantic import BaseModel, Field
from datetime import date
from app.enums import StatusPuchase

class ProductRequest(BaseModel):
    name: str
    price: float = Field(gt=0)
    stock: int = Field(ge=0)
    image: str | None = None

class ProductResponse(BaseModel):
    id: int
    name: str
    price: float
    stock: int
    image: str | None = None


class UserRequest(BaseModel):
    name: str
    email: str
    password: str


class UserResponse(BaseModel):
    id: int
    name: str
    email: str


class CartItem(BaseModel):
    product: ProductResponse
    quantity: int


class CartResponse(BaseModel):
    id: int
    user_id: int
    items: list[CartItem]


class PurchaseItem(BaseModel):
    product_id: int
    name: str
    price: float
    quantity: int


class PurchaseResponse(BaseModel):
    id: int
    user_id: int
    date_request: date
    status: StatusPuchase
    items: list[PurchaseItem]