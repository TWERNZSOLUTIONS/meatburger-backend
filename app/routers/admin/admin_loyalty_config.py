# routers/admin/admin_loyalty_config.py
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.admin.admin_loyalty_config import LoyaltyConfig
from app.schemas.admin.admin_loyalty_config import LoyaltyConfigOut, LoyaltyConfigUpdate
from sqlalchemy.sql import func

router = APIRouter(tags=["Admin Loyalty Config"])

# Pegar primeira configuração (única)
@router.get("/loyalty-config", response_model=LoyaltyConfigOut)
def get_config(db: Session = Depends(get_db)):
    config = db.query(LoyaltyConfig).first()
    if not config:
        raise HTTPException(status_code=404, detail="Configuração não encontrada")
    return config

# Atualizar configuração
@router.put("/loyalty-config", response_model=LoyaltyConfigOut)
def update_config(data: LoyaltyConfigUpdate, db: Session = Depends(get_db)):
    config = db.query(LoyaltyConfig).first()
    if not config:
        raise HTTPException(status_code=404, detail="Configuração não encontrada")
    try:
        for key, value in data.dict(exclude_unset=True).items():
            setattr(config, key, value)
        config.updated_at = func.now()
        db.commit()
        db.refresh(config)
        return config
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Erro ao atualizar configuração: {str(e)}")
