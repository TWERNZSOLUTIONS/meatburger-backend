from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(String)
    price = Column(Float, nullable=False)
    image_url = Column(String(255))
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)
    size = Column(String(50))          # Para bebidas e batatas
    style = Column(String(50))         # Apenas para batatas
    people_count = Column(Integer)     # Apenas para combos
    active = Column(Boolean, default=True)
    position = Column(Integer, default=0)
    burger_of_the_month = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relacionamento com categorias
    category = relationship("Category", back_populates="products")
