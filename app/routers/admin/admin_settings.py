from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.admin.admin_settings import SiteSettings
from app.schemas.admin.admin_settings import SiteSettingsCreate, SiteSettingsUpdate, SiteSettingsOut
from datetime import datetime

router = APIRouter()
    #prefix="/settings",  # 🔹 removido o /admin extra — evita duplicação de rota
    #tags=["Admin - Settings"]

# ----------------- Criar configuração do site -----------------
@router.post("/", response_model=SiteSettingsOut)
def create_settings(settings: SiteSettingsCreate, db: Session = Depends(get_db)):
    db_settings = SiteSettings(**settings.dict())
    db.add(db_settings)
    db.commit()
    db.refresh(db_settings)
    return db_settings

# ----------------- Atualizar configuração -----------------
@router.put("/{settings_id}", response_model=SiteSettingsOut)
def update_settings(settings_id: int, settings: SiteSettingsUpdate, db: Session = Depends(get_db)):
    db_settings = db.query(SiteSettings).filter(SiteSettings.id == settings_id).first()
    if not db_settings:
        raise HTTPException(status_code=404, detail="Configuração do site não encontrada")
    
    for key, value in settings.dict(exclude_unset=True).items():
        setattr(db_settings, key, value)

    db_settings.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(db_settings)
    return db_settings

# ----------------- Obter configuração do site -----------------
@router.get("/", response_model=SiteSettingsOut)
def get_settings(db: Session = Depends(get_db)):
    settings = db.query(SiteSettings).order_by(SiteSettings.id.desc()).first()
    if not settings:
        raise HTTPException(status_code=404, detail="Configuração do site não encontrada")
    return settings
