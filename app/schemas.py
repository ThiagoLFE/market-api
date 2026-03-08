from pydantic import BaseModel, Field

class ProductRequest(BaseModel):
    name: str
    price: float = Field(gt=0)
    stock: int = Field(ge=0)

class ProductResponse(BaseModel):
    id: int
    name: str
    price: float = Field(gt=0)
    stock: int = Field(ge=0)
