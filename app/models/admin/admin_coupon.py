from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, Table, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime

# Relação muitos-para-muitos entre cupons e produtos
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
    valid_from = Column(DateTime, nullable=False)
    valid_until = Column(DateTime, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Produtos associados
    products = relationship("Product", secondary=coupon_products, backref="coupons")
