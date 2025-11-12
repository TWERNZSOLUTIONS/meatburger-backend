from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class LoyaltyBase(BaseModel):
    customer_id: int
    customer_name: str
    phone: str
    points: Optional[int] = 0
    total_orders: Optional[int] = 0
    reward_threshold: Optional[int] = 10
    reward_claimed: Optional[bool] = False

class LoyaltyCreate(LoyaltyBase):
    """Schema para criação de registro de fidelidade."""
    pass

class LoyaltyUpdate(BaseModel):
    """Schema para atualização parcial de registro de fidelidade."""
    points: Optional[int] = None
    total_orders: Optional[int] = None
    reward_claimed: Optional[bool] = None
    reward_threshold: Optional[int] = None

class LoyaltyOut(LoyaltyBase):
    """Schema de retorno de registro de fidelidade."""
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
