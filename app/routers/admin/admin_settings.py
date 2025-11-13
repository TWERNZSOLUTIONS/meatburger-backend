from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.admin.admin_settings import SiteSettings
from app.schemas.admin.admin_settings import SiteSettingsCreate, SiteSettingsUpdate, SiteSettingsOut
from datetime import datetime

router = APIRouter(tags=["Admin Settings"])  # 🔹 tag padronizada

# ----------------- Obter configuração do site -----------------
@router.get("/", response_model=SiteSettingsOut)
def get_settings(db: Session = Depends(get_db)):
    settings = db.query(SiteSettings).order_by(SiteSettings.id.desc()).first()
    if not settings:
        raise HTTPException(status_code=404, detail="Configuração do site não encontrada")
    return settings

# ----------------- Atualizar configuração -----------------
@router.put("/", response_model=SiteSettingsOut)
def update_settings(settings_data: SiteSettingsUpdate, db: Session = Depends(get_db)):
    db_settings = db.query(SiteSettings).order_by(SiteSettings.id.desc()).first()
    if not db_settings:
        db_settings = SiteSettings(**settings_data.dict())
        db.add(db_settings)
        db.commit()
        db.refresh(db_settings)
        return db_settings

    for key, value in settings_data.dict(exclude_unset=True).items():
        setattr(db_settings, key, value)

    db_settings.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(db_settings)
    return db_settings

# ----------------- Criar configuração inicial -----------------
@router.post("/", response_model=SiteSettingsOut)
def create_settings(settings_data: SiteSettingsCreate, db: Session = Depends(get_db)):
    db_settings = SiteSettings(**settings_data.dict())
    db.add(db_settings)
    db.commit()
    db.refresh(db_settings)
    return db_settings
