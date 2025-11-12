from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime

class Loyalty(Base):
    __tablename__ = "loyalty"

    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)
    customer_name = Column(String(255), nullable=False)
    phone = Column(String(50), nullable=False)
    points = Column(Integer, default=0)
    total_orders = Column(Integer, default=0)
    reward_threshold = Column(Integer, default=10)  # Número de pedidos para ganhar prêmio
    reward_claimed = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    customer = relationship("Customer", back_populates="loyalties")
