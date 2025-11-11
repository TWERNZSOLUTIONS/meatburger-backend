from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

# ----------------- Estruturas auxiliares -----------------
class AddonItem(BaseModel):
    """Representa um adicional dentro de um produto do pedido."""
    name: str
    quantity: int
    price: float

class ProductItem(BaseModel):
    """Representa um produto do pedido, incluindo adicionais."""
    name: str
    quantity: int
    price: float
    addons: Optional[List[AddonItem]] = Field(default_factory=list)

# ----------------- Schemas para pedidos -----------------
class AdminOrderCreate(BaseModel):
    """Schema para criação de um pedido no painel administrativo."""
    customer_name: str
    customer_phone: Optional[str] = None
    customer_address: Optional[str] = None
    payment_method: str
    items: List[ProductItem]
    total: float
    observations: Optional[str] = None
    delivery_fee: Optional[float] = 0.0

class AdminOrderResponse(AdminOrderCreate):
    """Schema de resposta após criação do pedido."""
    id: int
    order_number: int
    created_at: datetime

    class Config:
        from_attributes = True  # ✅ Substitui orm_mode no Pydantic 2.x
