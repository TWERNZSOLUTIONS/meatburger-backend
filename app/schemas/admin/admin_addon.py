from pydantic import BaseModel, constr
from typing import Optional
from datetime import datetime


class AddonBase(BaseModel):
    name: constr(max_length=100)
    price: float
    position: Optional[int] = 0
    active: Optional[bool] = True


class AddonCreate(AddonBase):
    """Schema para criação de um novo adicional."""
    pass


class AddonUpdate(BaseModel):
    """Schema para atualização parcial de um adicional."""
    name: Optional[constr(max_length=100)] = None
    price: Optional[float] = None
    position: Optional[int] = None
    active: Optional[bool] = None


class AddonOut(AddonBase):
    """Schema de retorno de dados do adicional."""
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True  # ✅ Substitui orm_mode no Pydantic 2.x
