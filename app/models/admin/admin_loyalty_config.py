from sqlalchemy import Column, Integer, String, DateTime
from app.database import Base
from datetime import datetime

class LoyaltyConfig(Base):
    __tablename__ = "loyalty_config"

    id = Column(Integer, primary_key=True, index=True)
    premio = Column(String(255), nullable=False)
    pedidos_necessarios = Column(Integer, default=10)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
