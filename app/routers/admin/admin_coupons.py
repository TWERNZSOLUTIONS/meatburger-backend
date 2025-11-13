from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
from sqlalchemy.sql import func

from app.models.admin.admin_coupon import Coupon
from app.models.admin.admin_product import Product
from app.schemas.admin.admin_coupon import CouponCreate, CouponUpdate, CouponOut
from app.database import get_db

router = APIRouter(tags=["Admin Coupons"])

# ----------------- Criar cupom -----------------
@router.post("/", response_model=CouponOut)
def create_coupon(coupon: CouponCreate, db: Session = Depends(get_db)):
    """Cria um novo cupom e vincula produtos se fornecidos."""
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


# ----------------- Listar cupons -----------------
@router.get("/", response_model=List[CouponOut])
def list_coupons(db: Session = Depends(get_db)):
    """Lista todos os cupons ordenados pela validade decrescente."""
    return db.query(Coupon).order_by(Coupon.valid_until.desc()).all()


# ----------------- Obter cupom por ID -----------------
@router.get("/{coupon_id}", response_model=CouponOut)
def get_coupon(coupon_id: int, db: Session = Depends(get_db)):
    """Retorna um cupom específico pelo ID."""
    db_coupon = db.query(Coupon).filter(Coupon.id == coupon_id).first()
    if not db_coupon:
        raise HTTPException(status_code=404, detail="Cupom não encontrado")
    return db_coupon


# ----------------- Atualizar cupom -----------------
@router.put("/{coupon_id}", response_model=CouponOut)
def update_coupon(coupon_id: int, coupon: CouponUpdate, db: Session = Depends(get_db)):
    """Atualiza um cupom existente e vincula produtos se fornecidos."""
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


# ----------------- Deletar cupom -----------------
@router.delete("/{coupon_id}")
def delete_coupon(coupon_id: int, db: Session = Depends(get_db)):
    """Deleta um cupom pelo ID."""
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


# ----------------- Validar cupom -----------------
@router.get("/validate/{code}", response_model=CouponOut)
def validate_coupon(code: str, db: Session = Depends(get_db)):
    """Valida se um cupom está ativo e dentro do período de validade."""
    now = datetime.utcnow()
    db_coupon = db.query(Coupon).filter(
        Coupon.code == code,
        Coupon.is_active == True,
        Coupon.valid_from <= now,
        Coupon.valid_until >= now
    ).first()
    if not db_coupon:
        raise HTTPException(status_code=404, detail="Cupom inválido ou expirado")
    return db_coupon
