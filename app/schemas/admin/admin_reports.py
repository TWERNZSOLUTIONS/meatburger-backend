from pydantic import BaseModel
from typing import List, Optional
from datetime import date, datetime

# ----------------- Relatórios de vendas -----------------
class ProductSalesReport(BaseModel):
    """Relatório de vendas por produto."""
    product_name: str
    total_sold: int
    total_revenue: float

class CustomerOrdersReport(BaseModel):
    """Relatório de pedidos por cliente."""
    customer_name: str
    phone: str
    total_orders: int
    total_spent: float

class PaymentMethodReport(BaseModel):
    """Relatório de pedidos por método de pagamento."""
    payment_method: str
    total_orders: int
    total_revenue: float

class TimePeriodReport(BaseModel):
    """Relatório de pedidos por período."""
    period_start: date
    period_end: date
    total_orders: int
    total_revenue: float
