from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class LoyaltyConfigBase(BaseModel):
    premio: str
    pedidos_necessarios: int


class LoyaltyConfigCreate(LoyaltyConfigBase):
    pass


class LoyaltyConfigUpdate(BaseModel):
    premio: Optional[str] = None
    pedidos_necessarios: Optional[int] = None


class LoyaltyConfigOut(LoyaltyConfigBase):
    id: int

    class Config:
        from_attributes = True
