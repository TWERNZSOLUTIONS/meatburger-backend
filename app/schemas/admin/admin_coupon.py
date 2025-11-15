from pydantic import BaseModel, constr
from typing import Optional, List
from datetime import datetime

# --------------------------
# SCHEMAS BASE
# --------------------------
class CouponBase(BaseModel):
    code: constr(max_length=50)
    description: Optional[str] = None
    type: str  # "percent" ou "value"
    amount: float
    min_value: Optional[float] = 0.0
    max_uses: Optional[int] = None
    expires_at: datetime
    is_active: Optional[bool] = True
    product_ids: Optional[List[int]] = []

# --------------------------
# CRIAR CUPOM
# --------------------------
class CouponCreate(CouponBase):
    pass

# --------------------------
# ATUALIZAR CUPOM
# --------------------------
class CouponUpdate(BaseModel):
    code: Optional[constr(max_length=50)] = None
    description: Optional[str] = None
    type: Optional[str] = None
    amount: Optional[float] = None
    min_value: Optional[float] = None
    max_uses: Optional[int] = None
    expires_at: Optional[datetime] = None
    is_active: Optional[bool] = None
    product_ids: Optional[List[int]] = None

# --------------------------
# RETORNO
# --------------------------
class CouponOut(CouponBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
