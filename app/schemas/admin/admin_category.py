from pydantic import BaseModel, constr
from typing import Optional
from datetime import datetime

# ----------------- Schemas base -----------------
class CategoryBase(BaseModel):
    name: constr(max_length=100)
    position: Optional[int] = 0
    active: Optional[bool] = True

# ----------------- Schemas para CRUD -----------------
class CategoryCreate(CategoryBase):
    """Schema para criação de categoria."""
    pass

class CategoryUpdate(BaseModel):
    """Schema para atualização parcial de categoria."""
    name: Optional[constr(max_length=100)] = None
    position: Optional[int] = None
    active: Optional[bool] = None

class CategoryOut(CategoryBase):
    """Schema de retorno de categoria."""
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True  # ✅ Substitui orm_mode no Pydantic 2.x
