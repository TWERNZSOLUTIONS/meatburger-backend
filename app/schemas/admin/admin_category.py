from pydantic import BaseModel, constr
from typing import Optional
from datetime import datetime

# ----------------- Schemas para leitura -----------------
class CategoryBase(BaseModel):
    name: constr(max_length=100)
    position: Optional[int] = 0
    active: Optional[bool] = True

class CategoryCreate(CategoryBase):
    pass

class CategoryUpdate(BaseModel):
    name: Optional[constr(max_length=100)] = None
    position: Optional[int] = None
    active: Optional[bool] = None

class CategoryOut(CategoryBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
