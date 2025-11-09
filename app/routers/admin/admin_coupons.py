from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List

from app.models.admin.admin_coupon import Coupon
from app.schemas.admin.admin_coupon import CouponCreate, CouponUpdate, CouponOut
from app.database import get_db
from datetime import datetime

router = APIRouter(
    #prefix="/admin/coupons",
    tags=["Admin Coupons"]
)

# ----------------- Criar cupom -----------------
@router.post("/", response_model=CouponOut)
def create_coupon(coupon: CouponCreate, db: Session = Depends(get_db)):
    db_coupon = Coupon(
        **{k: v for k, v in coupon.dict(exclude={"product_ids"}).items()}
    )
    if coupon.product_ids:
        db_coupon.products = db.query("Product").filter("Product".id.in_(coupon.product_ids)).all()
    db.add(db_coupon)
    db.commit()
    db.refresh(db_coupon)
    return db_coupon

# ----------------- Listar cupons -----------------
@router.get("/", response_model=List[CouponOut])
def list_coupons(db: Session = Depends(get_db)):
    return db.query(Coupon).order_by(Coupon.valid_until.desc()).all()

# ----------------- Obter cupom por ID -----------------
@router.get("/{coupon_id}", response_model=CouponOut)
def get_coupon(coupon_id: int, db: Session = Depends(get_db)):
    db_coupon = db.query(Coupon).filter(Coupon.id == coupon_id).first()
    if not db_coupon:
        raise HTTPException(status_code=404, detail="Cupom não encontrado")
    return db_coupon

# ----------------- Atualizar cupom -----------------
@router.put("/{coupon_id}", response_model=CouponOut)
def update_coupon(coupon_id: int, coupon: CouponUpdate, db: Session = Depends(get_db)):
    db_coupon = db.query(Coupon).filter(Coupon.id == coupon_id).first()
    if not db_coupon:
        raise HTTPException(status_code=404, detail="Cupom não encontrado")

    for key, value in coupon.dict(exclude_unset=True, exclude={"product_ids"}).items():
        setattr(db_coupon, key, value)

    if coupon.product_ids is not None:
        db_coupon.products = db.query("Product").filter("Product".id.in_(coupon.product_ids)).all()

    db.commit()
    db.refresh(db_coupon)
    return db_coupon

# ----------------- Deletar cupom -----------------
@router.delete("/{coupon_id}")
def delete_coupon(coupon_id: int, db: Session = Depends(get_db)):
    db_coupon = db.query(Coupon).filter(Coupon.id == coupon_id).first()
    if not db_coupon:
        raise HTTPException(status_code=404, detail="Cupom não encontrado")

    db.delete(db_coupon)
    db.commit()
    return {"detail": "Cupom deletado com sucesso"}

# ----------------- Validar cupom (pode ser usado no carrinho) -----------------
@router.get("/validate/{code}", response_model=CouponOut)
def validate_coupon(code: str, db: Session = Depends(get_db)):
    now = datetime.utcnow()
    db_coupon = db.query(Coupon).filter(Coupon.code == code, Coupon.is_active==True,
                                        Coupon.valid_from <= now, Coupon.valid_until >= now).first()
    if not db_coupon:
        raise HTTPException(status_code=404, detail="Cupom inválido ou expirado")
    return db_coupon
