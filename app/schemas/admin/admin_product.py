# app/schemas/admin/admin_product.py
from pydantic import BaseModel, Field, HttpUrl
from typing import Optional
from datetime import datetime

# ----------------- Schemas base -----------------
class ProductBase(BaseModel):
    """Campos compartilhados por criação e atualização de produtos."""
    name: str = Field(..., max_length=255)
    description: Optional[str] = None
    price: float

    # Agora aceita tanto string quanto URL válida
    image_url: Optional[HttpUrl | str] = Field(None, description="URL da imagem do produto")

    category_id: int
    size: Optional[str] = Field(None, max_length=50)
    style: Optional[str] = Field(None, max_length=50)
    people_count: Optional[int] = None
    active: Optional[bool] = True
    position: Optional[int] = 0
    burger_of_the_month: Optional[bool] = False


# ----------------- Schemas CRUD -----------------
class ProductCreate(ProductBase):
    """Schema para criação de produto."""
    pass


class ProductUpdate(BaseModel):
    """Schema para atualização parcial de produto."""
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    image_url: Optional[HttpUrl | str] = None
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
        from_attributes = True  # Equivalente moderno de orm_mode=True
