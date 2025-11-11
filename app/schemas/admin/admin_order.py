from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

# Estruturas auxiliares
class AddonItem(BaseModel):
    name: str
    quantity: int
    price: float

class ProductItem(BaseModel):
    name: str
    quantity: int
    price: float
    addons: Optional[List[AddonItem]] = Field(default_factory=list)

# Criação de pedido
class AdminOrderCreate(BaseModel):
    customer_name: str
    customer_phone: Optional[str] = None
    customer_address: Optional[str] = None
    payment_method: str
    items: List[ProductItem]
    total: float
    observations: Optional[str] = None
    delivery_fee: Optional[float] = 0.0

# Atualização parcial do pedido
class AdminOrderUpdate(BaseModel):
    customer_name: Optional[str] = None
    customer_phone: Optional[str] = None
    customer_address: Optional[str] = None
    payment_method: Optional[str] = None
    items: Optional[List[ProductItem]] = None
    total: Optional[float] = None
    observations: Optional[str] = None
    delivery_fee: Optional[float] = None

# Resposta de pedido
class AdminOrderOut(AdminOrderCreate):
    id: int
    order_number: int
    created_at: datetime

    class Config:
        from_attributes = True
