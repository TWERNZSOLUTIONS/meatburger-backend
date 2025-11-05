from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

# 🔹 Estrutura de adicionais (Addons)
class AddonItem(BaseModel):
    name: str
    quantity: int
    price: float

# 🔹 Estrutura de produtos dentro da comanda
class ProductItem(BaseModel):
    name: str
    quantity: int
    price: float
    addons: Optional[List[AddonItem]] = Field(default_factory=list)

# 🔹 Schema para criação de pedido (Admin)
class AdminOrderCreate(BaseModel):
    customer_name: str
    customer_phone: Optional[str] = None
    customer_address: Optional[str] = None
    payment_method: str
    items: List[ProductItem]
    total: float
    observations: Optional[str] = None
    delivery_fee: Optional[float] = 0.0

# 🔹 Schema de resposta (quando o pedido é salvo)
class AdminOrderResponse(AdminOrderCreate):
    id: int
    order_number: int
    created_at: datetime

    class Config:
        from_attributes = True  # ⚠️ Substitui orm_mode no Pydantic v2
