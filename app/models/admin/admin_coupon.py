# app/models/admin/admin_coupon.py
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, Table, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

# Tabela de associação muitos-para-muitos entre cupons e produtos
coupon_products = Table(
    "coupon_products",
    Base.metadata,
    Column("coupon_id", Integer, ForeignKey("coupons.id"), primary_key=True),
    Column("product_id", Integer, ForeignKey("products.id"), primary_key=True)
)

class Coupon(Base):
    __tablename__ = "coupons"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(50), unique=True, nullable=False)
    discount_type = Column(String(20), nullable=False)  # 'percent' ou 'value'
    discount_value = Column(Float, nullable=False)
    min_order_value = Column(Float, default=0.0)
    usage_limit = Column(Integer, default=None)
    used_count = Column(Integer, default=0)
    valid_from = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    valid_until = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # 🔑 RELAÇÃO COM PRODUTOS
    products = relationship(
        "Product",
        secondary=coupon_products,
        back_populates="coupons"
    )
