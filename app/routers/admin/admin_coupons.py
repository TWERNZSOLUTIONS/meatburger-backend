from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from sqlalchemy.sql import func

from app.models.admin.admin_coupon import Coupon
from app.models.admin.admin_product import Product
from app.schemas.admin.admin_coupon import CouponCreate, CouponUpdate, CouponOut
from app.database import get_db

router = APIRouter(tags=["Admin Coupons"])

# --------------------------
# CRIAR CUPOM
# --------------------------
@router.post("/coupons/", response_model=CouponOut, status_code=201)
def create_coupon(coupon: CouponCreate, db: Session = Depends(get_db)):
    try:
        db_coupon = Coupon(**{k: v for k, v in coupon.dict(exclude={"product_ids"}).items()})
        db_coupon.created_at = func.now()
        db_coupon.updated_at = func.now()

        if coupon.product_ids:
            db_coupon.products = db.query(Product).filter(Product.id.in_(coupon.product_ids)).all()

        db.add(db_coupon)
        db.commit()
        db.refresh(db_coupon)
        return db_coupon
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Erro ao criar cupom: {str(e)}")

# --------------------------
# LISTAR CUPONS
# --------------------------
@router.get("/coupons/", response_model=List[CouponOut])
def list_coupons(db: Session = Depends(get_db)):
    try:
        return db.query(Coupon).order_by(Coupon.expires_at.desc()).all()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao listar cupons: {str(e)}")

# --------------------------
# BUSCAR CUPOM POR ID
# --------------------------
@router.get("/coupons/{coupon_id}", response_model=CouponOut)
def get_coupon(coupon_id: int, db: Session = Depends(get_db)):
    db_coupon = db.query(Coupon).filter(Coupon.id == coupon_id).first()
    if not db_coupon:
        raise HTTPException(status_code=404, detail="Cupom não encontrado")
    return db_coupon

# --------------------------
# ATUALIZAR CUPOM
# --------------------------
@router.put("/coupons/{coupon_id}", response_model=CouponOut)
def update_coupon(coupon_id: int, coupon: CouponUpdate, db: Session = Depends(get_db)):
    db_coupon = db.query(Coupon).filter(Coupon.id == coupon_id).first()
    if not db_coupon:
        raise HTTPException(status_code=404, detail="Cupom não encontrado")
    try:
        for key, value in coupon.dict(exclude_unset=True, exclude={"product_ids"}).items():
            setattr(db_coupon, key, value)
        db_coupon.updated_at = func.now()

        if coupon.product_ids is not None:
            db_coupon.products = db.query(Product).filter(Product.id.in_(coupon.product_ids)).all()

        db.commit()
        db.refresh(db_coupon)
        return db_coupon
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Erro ao atualizar cupom: {str(e)}")

# --------------------------
# DELETAR CUPOM
# --------------------------
@router.delete("/coupons/{coupon_id}")
def delete_coupon(coupon_id: int, db: Session = Depends(get_db)):
    db_coupon = db.query(Coupon).filter(Coupon.id == coupon_id).first()
    if not db_coupon:
        raise HTTPException(status_code=404, detail="Cupom não encontrado")
    try:
        db.delete(db_coupon)
        db.commit()
        return {"detail": "Cupom deletado com sucesso"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Erro ao deletar cupom: {str(e)}")

# --------------------------
# VALIDAR CUPOM
# --------------------------
@router.get("/coupons/validate/{code}", response_model=CouponOut)
def validate_coupon(code: str, db: Session = Depends(get_db)):
    now = datetime.utcnow()
    db_coupon = db.query(Coupon).filter(
        Coupon.code == code,
        Coupon.is_active == True,
        Coupon.expires_at >= now
    ).first()
    if not db_coupon:
        raise HTTPException(status_code=404, detail="Cupom inválido ou expirado")
    return db_coupon
