from pydantic import BaseModel, Field, HttpUrl
from typing import Optional
from datetime import datetime

class ProductBase(BaseModel):
    name: str = Field(..., max_length=255)
    description: Optional[str] = None
    price: float
    image_url: Optional[str | HttpUrl] = None
    category_id: int
    size: Optional[str] = Field(None, max_length=50)
    style: Optional[str] = Field(None, max_length=50)
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
    image_url: Optional[str | HttpUrl] = None
    category_id: Optional[int] = None
    size: Optional[str] = None
    style: Optional[str] = None
    people_count: Optional[int] = None
    active: Optional[bool] = None
    position: Optional[int] = None
    burger_of_the_month: Optional[bool] = None

class ProductOut(ProductBase):
    id: int
    created_at: Optional[datetime] = None  # ⚠ Alterado para Optional
    updated_at: Optional[datetime] = None  # ⚠ Alterado para Optional

    class Config:
        from_attributes = True
