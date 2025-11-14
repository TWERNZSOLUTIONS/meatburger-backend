from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.admin.admin_loyalty_config import LoyaltyConfig
from app.schemas.admin.admin_loyalty_config import LoyaltyConfigOut, LoyaltyConfigUpdate

router = APIRouter(tags=["Admin Loyalty Config"])

@router.get("/loyalty-config/{config_id}", response_model=LoyaltyConfigOut)
def get_config(config_id: int, db: Session = Depends(get_db)):
    config = db.query(LoyaltyConfig).filter(LoyaltyConfig.id == config_id).first()
    if not config:
        raise HTTPException(status_code=404, detail="Configuração não encontrada")
    return config

@router.put("/loyalty-config/{config_id}", response_model=LoyaltyConfigOut)
def update_config(config_id: int, data: LoyaltyConfigUpdate, db: Session = Depends(get_db)):
    config = db.query(LoyaltyConfig).filter(LoyaltyConfig.id == config_id).first()
    if not config:
        raise HTTPException(status_code=404, detail="Configuração não encontrada")
    for key, value in data.dict(exclude_unset=True).items():
        setattr(config, key, value)
    db.commit()
    db.refresh(config)
    return config
