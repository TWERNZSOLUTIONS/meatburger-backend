# app/routers/admin/admin_addons.py
from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from typing import List

from app.models.admin.admin_addon import Addon
from app.schemas.admin.admin_addon import AddonCreate, AddonUpdate, AddonOut
from app.database import get_db

router = APIRouter(prefix="/admin/addons", tags=["Admin Adicionais"])


# ----------------- Criar adicional -----------------
@router.post("/", response_model=AddonOut, status_code=201)
def create_addon(addon: AddonCreate, db: Session = Depends(get_db)):
    try:
        db_addon = Addon(**addon.dict())
        db.add(db_addon)
        db.commit()
        db.refresh(db_addon)
        return db_addon
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Erro ao criar adicional: {str(e)}")


# ----------------- Listar adicionais -----------------
@router.get("/", response_model=List[AddonOut])
def list_addons(
    db: Session = Depends(get_db),
    all: bool = Query(False, description="Se true, lista também inativos."),
):
    query = db.query(Addon)
    if not all:
        query = query.filter(Addon.active == True)
    return query.order_by(Addon.position, Addon.name).all()


# ----------------- Obter adicional por ID -----------------
@router.get("/{addon_id}", response_model=AddonOut)
def get_addon(addon_id: int, db: Session = Depends(get_db)):
    db_addon = db.query(Addon).filter(Addon.id == addon_id).first()
    if not db_addon:
        raise HTTPException(status_code=404, detail="Adicional não encontrado")
    return db_addon


# ----------------- Atualizar adicional -----------------
@router.put("/{addon_id}", response_model=AddonOut)
def update_addon(addon_id: int, addon: AddonUpdate, db: Session = Depends(get_db)):
    db_addon = db.query(Addon).filter(Addon.id == addon_id).first()
    if not db_addon:
        raise HTTPException(status_code=404, detail="Adicional não encontrado")

    try:
        for key, value in addon.dict(exclude_unset=True).items():
            setattr(db_addon, key, value)

        db.commit()
        db.refresh(db_addon)
        return db_addon
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Erro ao atualizar adicional: {str(e)}")


# ----------------- Deletar adicional -----------------
@router.delete("/{addon_id}")
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
