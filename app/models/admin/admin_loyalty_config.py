from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from app.database import Base

class LoyaltyConfig(Base):
    __tablename__ = "loyalty_config"

    id = Column(Integer, primary_key=True, index=True)
    premio = Column(String(255), nullable=False)
    pedidos_necessarios = Column(Integer, default=10)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
