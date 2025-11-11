from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class ProductBase(BaseModel):
    name: str = Field(..., max_length=255)
    description: Optional[str] = None
    price: float
    image_url: Optional[str] = None
    category_id: int
    size: Optional[str] = None
    style: Optional[str] = None
    people_count: Optional[int] = None
    active: Optional[bool] = True
    position: Optional[int] = 0
    burger_of_the_month: Optional[bool] = False


class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
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
        from_attributes = True  # Compatível com Pydantic v2
