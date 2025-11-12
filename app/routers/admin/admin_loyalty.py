from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

from app.models.admin.admin_loyalty import Loyalty
from app.schemas.admin.admin_loyalty import LoyaltyCreate, LoyaltyUpdate, LoyaltyOut
from app.database import get_db

router = APIRouter(
    #prefix="/loyalty",
    tags=["Admin Loyalty"]
)

# ----------------- Criar registro de fidelidade -----------------
@router.post("/", response_model=LoyaltyOut)
def create_loyalty(loyalty: LoyaltyCreate, db: Session = Depends(get_db)):
    db_loyalty = Loyalty(**loyalty.dict())
    db.add(db_loyalty)
    db.commit()
    db.refresh(db_loyalty)
    return db_loyalty

# ----------------- Listar todos os registros -----------------
@router.get("/", response_model=List[LoyaltyOut])
def list_loyalty(db: Session = Depends(get_db)):
    return db.query(Loyalty).order_by(Loyalty.customer_name).all()

# ----------------- Atualizar registro -----------------
@router.put("/{loyalty_id}", response_model=LoyaltyOut)
def update_loyalty(loyalty_id: int, loyalty: LoyaltyUpdate, db: Session = Depends(get_db)):
    db_loyalty = db.query(Loyalty).filter(Loyalty.id == loyalty_id).first()
    if not db_loyalty:
        raise HTTPException(status_code=404, detail="Registro de fidelidade não encontrado")

    for key, value in loyalty.dict(exclude_unset=True).items():
        setattr(db_loyalty, key, value)

    db.commit()
    db.refresh(db_loyalty)
    return db_loyalty

# ----------------- Deletar registro -----------------
@router.delete("/{loyalty_id}")
def delete_loyalty(loyalty_id: int, db: Session = Depends(get_db)):
    db_loyalty = db.query(Loyalty).filter(Loyalty.id == loyalty_id).first()
    if not db_loyalty:
        raise HTTPException(status_code=404, detail="Registro de fidelidade não encontrado")
    
    db.delete(db_loyalty)
    db.commit()
    return {"detail": "Registro de fidelidade deletado com sucesso"}

# ----------------- Incrementar pedidos do cliente -----------------
@router.post("/{loyalty_id}/increment", response_model=LoyaltyOut)
def increment_loyalty(loyalty_id: int, db: Session = Depends(get_db)):
    db_loyalty = db.query(Loyalty).filter(Loyalty.id == loyalty_id).first()
    if not db_loyalty:
        raise HTTPException(status_code=404, detail="Registro de fidelidade não encontrado")

    db_loyalty.total_orders += 1
    # Incrementa pontos conforme a lógica que você definir (ex: 1 ponto por pedido)
    db_loyalty.points += 1
    db.commit()
    db.refresh(db_loyalty)
    return db_loyalty

# ----------------- Marcar cliente como premiado -----------------
@router.post("/{loyalty_id}/reward", response_model=LoyaltyOut)
def reward_loyalty(loyalty_id: int, db: Session = Depends(get_db)):
    db_loyalty = db.query(Loyalty).filter(Loyalty.id == loyalty_id).first()
    if not db_loyalty:
        raise HTTPException(status_code=404, detail="Registro de fidelidade não encontrado")

    db_loyalty.reward_claimed = True
    db.commit()
    db.refresh(db_loyalty)
    return db_loyalty
