from pydantic import BaseModel, constr
from typing import Optional, List
from datetime import datetime

# ----------------- Schemas base -----------------
class CouponBase(BaseModel):
    code: constr(max_length=50)
    discount_type: str  # 'percent' ou 'value'
    discount_value: float
    min_order_value: Optional[float] = 0.0
    usage_limit: Optional[int] = None
    valid_from: datetime
    valid_until: datetime
    is_active: Optional[bool] = True
    product_ids: Optional[List[int]] = []

# ----------------- Schemas para CRUD -----------------
class CouponCreate(CouponBase):
    pass

class CouponUpdate(BaseModel):
    code: Optional[constr(max_length=50)] = None
    discount_type: Optional[str] = None
    discount_value: Optional[float] = None
    min_order_value: Optional[float] = None
    usage_limit: Optional[int] = None
    valid_from: Optional[datetime] = None
    valid_until: Optional[datetime] = None
    is_active: Optional[bool] = None
    product_ids: Optional[List[int]] = None

class CouponOut(CouponBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
