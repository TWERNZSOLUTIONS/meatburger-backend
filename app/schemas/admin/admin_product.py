from pydantic import BaseModel, condecimal, constr
from typing import Optional
from datetime import datetime

# ----------------- Schemas base -----------------
class ProductBase(BaseModel):
    name: constr(max_length=255)
    description: Optional[str] = None
    price: condecimal(max_digits=10, decimal_places=2)
    image_url: Optional[str] = None
    category_id: int
    size: Optional[str] = None
    style: Optional[str] = None
    people_count: Optional[int] = None
    active: Optional[bool] = True
    position: Optional[int] = 0
    burger_of_the_month: Optional[bool] = False

# ----------------- Schemas para CRUD -----------------
class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[condecimal(max_digits=10, decimal_places=2)] = None
    image_url: Optional[str] = None
    category_id: Optional[int] = None
    size: Optional[str] = None
    style: Optional[str] = None
    people_count: Optional[int] = None
    active: Optional[bool] = None
    position: Optional[int] = None
    burger_of_the_month: Optional[bool] = None

class ProductOut(ProductBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
