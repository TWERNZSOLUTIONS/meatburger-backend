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
    pass

class LoyaltyUpdate(BaseModel):
    points: Optional[int] = None
    total_orders: Optional[int] = None
    reward_claimed: Optional[bool] = None
    reward_threshold: Optional[int] = None

class LoyaltyOut(LoyaltyBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
