# app/schemas/admin/admin_addon.py
from pydantic import BaseModel, constr
from typing import Optional
from datetime import datetime


# ----------------- Schemas base -----------------
class AddonBase(BaseModel):
    name: constr(max_length=100)
    price: float
    position: Optional[int] = 0
    active: Optional[bool] = True
    # image_url: Optional[str] = None  # (para futura expansão)


# ----------------- Schema para criação -----------------
class AddonCreate(AddonBase):
    pass


# ----------------- Schema para atualização -----------------
class AddonUpdate(BaseModel):
    name: Optional[constr(max_length=100)] = None
    price: Optional[float] = None
    position: Optional[int] = None
    active: Optional[bool] = None
    # image_url: Optional[str] = None


# ----------------- Schema de retorno -----------------
class AddonOut(AddonBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True  # substitui orm_mode no Pydantic 2.x
