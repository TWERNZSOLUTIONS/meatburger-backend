from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from sqlalchemy.sql import func

from app.models.admin.admin_loyalty import Loyalty
from app.schemas.admin.admin_loyalty import LoyaltyCreate, LoyaltyUpdate, LoyaltyOut
from app.database import get_db

router = APIRouter(tags=["Admin Loyalty"])

# -------------------------- CREATE --------------------------
@router.post("/loyalty/", response_model=LoyaltyOut, status_code=201)
def create_loyalty(loyalty: LoyaltyCreate, db: Session = Depends(get_db)):
    try:
        db_loyalty = Loyalty(**loyalty.dict())
        db_loyalty.created_at = func.now()
        db_loyalty.updated_at = func.now()
        db.add(db_loyalty)
        db.commit()
        db.refresh(db_loyalty)
        return db_loyalty
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Erro ao criar registro: {str(e)}")

# -------------------------- LIST --------------------------
@router.get("/loyalty/", response_model=List[LoyaltyOut])
def list_loyalty(db: Session = Depends(get_db)):
    try:
        return db.query(Loyalty).order_by(Loyalty.customer_name.asc()).all()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao listar registros: {str(e)}")

# -------------------------- UPDATE --------------------------
@router.put("/loyalty/{loyalty_id}", response_model=LoyaltyOut)
def update_loyalty(loyalty_id: int, loyalty: LoyaltyUpdate, db: Session = Depends(get_db)):
    db_loyalty = db.query(Loyalty).filter(Loyalty.id == loyalty_id).first()
    if not db_loyalty:
        raise HTTPException(status_code=404, detail="Registro de fidelidade não encontrado")
    try:
        for key, value in loyalty.dict(exclude_unset=True).items():
            setattr(db_loyalty, key, value)
        db_loyalty.updated_at = func.now()
        db.commit()
        db.refresh(db_loyalty)
        return db_loyalty
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Erro ao atualizar registro: {str(e)}")

# -------------------------- DELETE --------------------------
@router.delete("/loyalty/{loyalty_id}")
def delete_loyalty(loyalty_id: int, db: Session = Depends(get_db)):
    db_loyalty = db.query(Loyalty).filter(Loyalty.id == loyalty_id).first()
    if not db_loyalty:
        raise HTTPException(status_code=404, detail="Registro de fidelidade não encontrado")
    try:
        db.delete(db_loyalty)
        db.commit()
        return {"detail": "Registro de fidelidade deletado com sucesso"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Erro ao deletar registro: {str(e)}")

# -------------------------- INCREMENT --------------------------
@router.post("/loyalty/{loyalty_id}/increment", response_model=LoyaltyOut)
def increment_loyalty(loyalty_id: int, db: Session = Depends(get_db)):
    db_loyalty = db.query(Loyalty).filter(Loyalty.id == loyalty_id).first()
    if not db_loyalty:
        raise HTTPException(status_code=404, detail="Registro de fidelidade não encontrado")
    try:
        db_loyalty.total_orders += 1
        db_loyalty.points += 1
        db_loyalty.updated_at = func.now()
        db.commit()
        db.refresh(db_loyalty)
        return db_loyalty
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Erro ao incrementar fidelidade: {str(e)}")

# -------------------------- REWARD --------------------------
@router.post("/loyalty/{loyalty_id}/reward", response_model=LoyaltyOut)
def reward_loyalty(loyalty_id: int, db: Session = Depends(get_db)):
    db_loyalty = db.query(Loyalty).filter(Loyalty.id == loyalty_id).first()
    if not db_loyalty:
        raise HTTPException(status_code=404, detail="Registro de fidelidade não encontrado")
    try:
        db_loyalty.reward_claimed = True
        db_loyalty.updated_at = func.now()
        db.commit()
        db.refresh(db_loyalty)
        return db_loyalty
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Erro ao marcar cliente premiado: {str(e)}")
