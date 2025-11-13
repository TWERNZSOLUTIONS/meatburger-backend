from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from sqlalchemy.sql import func

from app.models.admin.admin_loyalty import Loyalty
from app.schemas.admin.admin_loyalty import LoyaltyCreate, LoyaltyUpdate, LoyaltyOut
from app.database import get_db

router = APIRouter(tags=["Admin Loyalty"])

# ----------------- Criar registro de fidelidade -----------------
@router.post("/", response_model=LoyaltyOut)
def create_loyalty(loyalty: LoyaltyCreate, db: Session = Depends(get_db)):
    """Cria um novo registro de fidelidade."""
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


# ----------------- Listar todos os registros -----------------
@router.get("/", response_model=List[LoyaltyOut])
def list_loyalty(db: Session = Depends(get_db)):
    """Lista todos os registros de fidelidade ordenados por nome do cliente."""
    return db.query(Loyalty).order_by(Loyalty.customer_name.asc()).all()


# ----------------- Atualizar registro -----------------
@router.put("/{loyalty_id}", response_model=LoyaltyOut)
def update_loyalty(loyalty_id: int, loyalty: LoyaltyUpdate, db: Session = Depends(get_db)):
    """Atualiza um registro existente de fidelidade."""
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


# ----------------- Deletar registro -----------------
@router.delete("/{loyalty_id}")
def delete_loyalty(loyalty_id: int, db: Session = Depends(get_db)):
    """Deleta um registro de fidelidade pelo ID."""
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


# ----------------- Incrementar pedidos do cliente -----------------
@router.post("/{loyalty_id}/increment", response_model=LoyaltyOut)
def increment_loyalty(loyalty_id: int, db: Session = Depends(get_db)):
    """Incrementa o total de pedidos e pontos do cliente."""
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


# ----------------- Marcar cliente como premiado -----------------
@router.post("/{loyalty_id}/reward", response_model=LoyaltyOut)
def reward_loyalty(loyalty_id: int, db: Session = Depends(get_db)):
    """Marca um cliente como premiado."""
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
