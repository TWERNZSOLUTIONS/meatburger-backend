from sqlalchemy import Column, Integer, String, Float, JSON, DateTime
from sqlalchemy.sql import func
from app.database import Base

class AdminOrder(Base):
    __tablename__ = "admin_orders"

    id = Column(Integer, primary_key=True, index=True)
    order_number = Column(Integer, index=True, nullable=False)  # Número da comanda visível
    customer_name = Column(String, nullable=False)
    customer_phone = Column(String, nullable=True)
    customer_address = Column(String, nullable=True)
    payment_method = Column(String, nullable=False)
    items = Column(JSON, nullable=False)  # Lista de produtos + adicionais
    total = Column(Float, nullable=False)
    observations = Column(String, nullable=True)
    delivery_fee = Column(Float, nullable=False, default=0.0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    def __repr__(self):
        return f"<AdminOrder(order_number={self.order_number}, total={self.total})>"
