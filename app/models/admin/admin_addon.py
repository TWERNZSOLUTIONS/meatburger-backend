from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime
from app.database import Base
from datetime import datetime

class Addon(Base):
    __tablename__ = "addons"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    price = Column(Float, nullable=False)
    position = Column(Integer, default=0)  # ordem de exibição
    active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
