from pydantic import BaseModel

class LoyaltyConfigOut(BaseModel):
    id: int
    premio: str
    pedidos_necessarios: int

    class Config:
        from_attributes = True

class LoyaltyConfigUpdate(BaseModel):
    premio: str
    pedidos_necessarios: int
