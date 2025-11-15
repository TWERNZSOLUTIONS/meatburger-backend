from pydantic import BaseModel, constr
from typing import Optional
from datetime import datetime

class AddonBase(BaseModel):
    name: constr(max_length=255)  # mais consistente com produtos
    price: float
    position: Optional[int] = 0
    active: Optional[bool] = True

class AddonCreate(AddonBase):
    pass

class AddonUpdate(BaseModel):
    name: Optional[constr(max_length=255)] = None
    price: Optional[float] = None
    position: Optional[int] = None
    active: Optional[bool] = None

class AddonOut(AddonBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
