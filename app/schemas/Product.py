class ProductRequest(BaseModel):
    name: str
    price: float
    stock: int

class Product(BaseModel):
    id: int
    name: str
    price: float
    stock: int
