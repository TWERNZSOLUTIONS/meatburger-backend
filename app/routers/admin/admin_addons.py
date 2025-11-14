from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from sqlalchemy.sql import func

from app.models.admin.admin_addon import Addon
from app.schemas.admin.admin_addon import AddonCreate, AddonUpdate, AddonOut
from app.database import get_db

router = APIRouter(tags=["Admin Addons"])

@router.post("/addons/", response_model=AddonOut, status_code=201)
def create_addon(addon: AddonCreate, db: Session = Depends(get_db)):
    try:
        new_addon = Addon(
            **addon.dict(),
            created_at=func.now(),
            updated_at=func.now()
        )
        db.add(new_addon)
        db.commit()
        db.refresh(new_addon)
        return new_addon
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Erro ao criar adicional: {str(e)}")

@router.get("/addons/", response_model=List[AddonOut])
def list_addons(
    db: Session = Depends(get_db),
    all: bool = Query(False, description="Se true, lista também inativos."),
    search: Optional[str] = Query(None, description="Busca pelo nome do adicional."),
):
    query = db.query(Addon)
    if not all:
        query = query.filter(Addon.active == True)
    if search:
        query = query.filter(Addon.name.ilike(f"%{search}%"))
    return query.order_by(Addon.position.asc(), Addon.name.asc()).all()

@router.get("/addons/{addon_id}", response_model=AddonOut)
def get_addon(addon_id: int, db: Session = Depends(get_db)):
    db_addon = db.query(Addon).filter(Addon.id == addon_id).first()
    if not db_addon:
        raise HTTPException(status_code=404, detail="Adicional não encontrado")
    return db_addon

@router.put("/addons/{addon_id}", response_model=AddonOut)
def update_addon(addon_id: int, addon: AddonUpdate, db: Session = Depends(get_db)):
    db_addon = db.query(Addon).filter(Addon.id == addon_id).first()
    if not db_addon:
        raise HTTPException(status_code=404, detail="Adicional não encontrado")
    try:
        for key, value in addon.dict(exclude_unset=True).items():
            setattr(db_addon, key, value)
        db_addon.updated_at = func.now()
        db.commit()
        db.refresh(db_addon)
        return db_addon
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Erro ao atualizar adicional: {str(e)}")

@router.delete("/addons/{addon_id}")
def delete_addon(addon_id: int, db: Session = Depends(get_db)):
    db_addon = db.query(Addon).filter(Addon.id == addon_id).first()
    if not db_addon:
        raise HTTPException(status_code=404, detail="Adicional não encontrado")
    try:
        db.delete(db_addon)
        db.commit()
        return {"detail": "Adicional deletado com sucesso"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Erro ao deletar adicional: {str(e)}")

@router.patch("/addons/{addon_id}/toggle", response_model=AddonOut)
def toggle_addon(addon_id: int, db: Session = Depends(get_db)):
    db_addon = db.query(Addon).filter(Addon.id == addon_id).first()
    if not db_addon:
        raise HTTPException(status_code=404, detail="Adicional não encontrado")
    try:
        db_addon.active = not db_addon.active
        db_addon.updated_at = func.now()
        db.commit()
        db.refresh(db_addon)
        return db_addon
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Erro ao alternar adicional: {str(e)}")

@router.patch("/addons/{addon_id}/position", response_model=AddonOut)
def update_position(addon_id: int, position: int = Query(...), db: Session = Depends(get_db)):
    db_addon = db.query(Addon).filter(Addon.id == addon_id).first()
    if not db_addon:
        raise HTTPException(status_code=404, detail="Adicional não encontrado")
    try:
        db_addon.position = position
        db_addon.updated_at = func.now()
        db.commit()
        db.refresh(db_addon)
        return db_addon
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Erro ao atualizar posição: {str(e)}")
