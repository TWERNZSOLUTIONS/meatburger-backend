from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

# ----------------- Schemas base para produtos -----------------
class ProductBase(BaseModel):
    """Base para criação e atualização de produtos."""
    name: str = Field(..., max_length=255)
    description: Optional[str] = None
    price: float
    image_url: Optional[str] = None
    category_id: int
    size: Optional[str] = None           # Por exemplo: bebidas/batatas
    style: Optional[str] = None          # Por exemplo: batatas
    people_count: Optional[int] = None   # Para combos
    active: Optional[bool] = True
    position: Optional[int] = 0
    burger_of_the_month: Optional[bool] = False

# ----------------- Schemas para CRUD -----------------
class ProductCreate(ProductBase):
    """Schema para criação de produto."""
    pass

class ProductUpdate(BaseModel):
    """Schema para atualização parcial de produto."""
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
    """Schema de retorno de produto, com timestamps e ID."""
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True  # ✅ Substitui orm_mode no Pydantic v2
