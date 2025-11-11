# app/models/admin/admin_product.py
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(String, nullable=True)
    price = Column(Float, nullable=False)

    # URL da imagem do produto (armazenada após upload)
    image_url = Column(String(512), nullable=True)

    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)

    size = Column(String(50), nullable=True)          # Ex: bebidas/batatas
    style = Column(String(50), nullable=True)         # Ex: tipo de batata
    people_count = Column(Integer, nullable=True)     # Ex: combos
    active = Column(Boolean, default=True)
    position = Column(Integer, default=0)
    burger_of_the_month = Column(Boolean, default=False)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    category = relationship("Category", back_populates="products")
