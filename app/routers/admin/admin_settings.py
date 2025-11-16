from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional
from datetime import datetime, time
from app.database import get_db
from app.models.admin.admin_settings import SiteSettings
from app.schemas.admin.admin_settings import (
    SiteSettingsCreate,
    SiteSettingsUpdate,
    SiteSettingsOut
)
from utils.auth_admin import get_current_admin

router = APIRouter(
    prefix="/admin/settings",
    tags=["Admin Settings"]
)

# ------------------------------------------------
# FUNÇÃO – CÁLCULO DO STATUS DA LOJA
# ------------------------------------------------
def calculate_store_status(settings: SiteSettings) -> tuple[bool, Optional[str]]:
    """
    Retorna (is_open, message)
    """

    now = datetime.now()
    today_weekday = now.strftime("%a")  # Seg, Ter, Qua...

    # 1 — FECHADO MANUALMENTE
    if settings.manual_close:
        return False, settings.closed_message

    # 2 — DIA NÃO FUNCIONA
    if settings.days_open and today_weekday not in settings.days_open:
        return False, "Hoje não estamos funcionando"

    # 3 — HORÁRIOS INDEFINIDOS → SEMPRE ABERTO
    if not settings.opening_time or not settings.closing_time:
        return True, None

    # 4 — HORÁRIO AUTOMÁTICO
    current_time = now.time()

    if settings.opening_time <= current_time <= settings.closing_time:
        return True, None

    return False, "Fora do horário de funcionamento"


# ------------------------------------------------
# GET — BUSCAR CONFIGURAÇÕES
# ------------------------------------------------
@router.get("/", response_model=SiteSettingsOut)
def get_settings(db: Session = Depends(get_db)):
    settings = db.query(SiteSettings).order_by(SiteSettings.id.desc()).first()

    # Se não existir, cria padrão
    if not settings:
        settings = SiteSettings()
        db.add(settings)
        db.commit()
        db.refresh(settings)

    # Calcula status atual sempre que fizer GET
    is_open, msg = calculate_store_status(settings)
    settings.open = is_open
    settings.closed_message = msg

    return settings


# ------------------------------------------------
# CREATE — CRIAR CONFIGURAÇÃO (raramente usado)
# ------------------------------------------------
@router.post("/", response_model=SiteSettingsOut)
def create_settings(
    payload: SiteSettingsCreate,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin)
):
    settings = SiteSettings(**payload.model_dump())
    db.add(settings)
    db.commit()
    db.refresh(settings)
    return settings


# ------------------------------------------------
# UPDATE — ATUALIZA TUDO VIA PAINEL ADMIN
# ------------------------------------------------
@router.put("/", response_model=SiteSettingsOut)
def update_settings(
    payload: SiteSettingsUpdate,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin)
):
    settings = db.query(SiteSettings).order_by(SiteSettings.id.desc()).first()

    if not settings:
        raise HTTPException(404, "Configurações não encontradas")

    # Validação horário
    if payload.opening_time and payload.closing_time:
        if payload.opening_time >= payload.closing_time:
            raise HTTPException(
                400,
                "O horário de abertura deve ser antes do fechamento."
            )

    # Atualiza apenas campos enviados
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(settings, field, value)

    db.commit()
    db.refresh(settings)

    # Recalcula status depois de salvar
    is_open, msg = calculate_store_status(settings)
    settings.open = is_open
    settings.closed_message = msg

    return settings


# ------------------------------------------------
# FECHAR MANUALMENTE
# ------------------------------------------------
@router.put("/manual-close", response_model=SiteSettingsOut)
def manual_close(
    reason: Optional[str] = None,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin)
):
    settings = db.query(SiteSettings).order_by(SiteSettings.id.desc()).first()

    if not settings:
        raise HTTPException(404, "Configurações não encontradas")

    settings.manual_close = True
    settings.closed_message = reason or "Fechado temporariamente"

    db.commit()
    db.refresh(settings)

    settings.open = False

    return settings


# ------------------------------------------------
# REABRIR MANUALMENTE
# ------------------------------------------------
@router.put("/manual-open", response_model=SiteSettingsOut)
def manual_open(
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin)
):
    settings = db.query(SiteSettings).order_by(SiteSettings.id.desc()).first()

    if not settings:
        raise HTTPException(404, "Configurações não encontradas")

    settings.manual_close = False
    settings.closed_message = None

    db.commit()
    db.refresh(settings)

    # Recalcular após abrir
    is_open, msg = calculate_store_status(settings)
    settings.open = is_open
    settings.closed_message = msg

    return settings
