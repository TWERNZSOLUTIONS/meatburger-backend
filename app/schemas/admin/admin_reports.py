from pydantic import BaseModel
from typing import List, Optional
from datetime import date

class ProductSalesReport(BaseModel):
    product_name: str
    total_sold: int
    total_revenue: float

class CustomerOrdersReport(BaseModel):
    customer_name: str
    phone: str
    total_orders: int
    total_spent: float

class PaymentMethodReport(BaseModel):
    payment_method: str
    total_orders: int
    total_revenue: float

class TimePeriodReport(BaseModel):
    period_start: date
    period_end: date
    total_orders: int
    total_revenue: float
