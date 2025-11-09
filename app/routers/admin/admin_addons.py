from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List

from app.models.admin.admin_addon import Addon
from app.schemas.admin.admin_addon import AddonCreate, AddonUpdate, AddonOut
from app.database import get_db

router = APIRouter()
    #prefix="/admin/addons",
    #tags=["Admin Addons"]

# ----------------- Criar adicional -----------------
@router.post("/", response_model=AddonOut)
def create_addon(addon: AddonCreate, db: Session = Depends(get_db)):
    db_addon = Addon(**addon.dict())
    db.add(db_addon)
    db.commit()
    db.refresh(db_addon)
    return db_addon

# ----------------- Listar adicionais -----------------
@router.get("/", response_model=List[AddonOut])
def list_addons(db: Session = Depends(get_db)):
    return db.query(Addon).order_by(Addon.position).all()

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

    for key, value in addon.dict(exclude_unset=True).items():
        setattr(db_addon, key, value)

    db.commit()
    db.refresh(db_addon)
    return db_addon

# ----------------- Deletar adicional -----------------
@router.delete("/{addon_id}")
def delete_addon(addon_id: int, db: Session = Depends(get_db)):
    db_addon = db.query(Addon).filter(Addon.id == addon_id).first()
    if not db_addon:
        raise HTTPException(status_code=404, detail="Adicional não encontrado")

    db.delete(db_addon)
    db.commit()
    return {"detail": "Adicional deletado com sucesso"}

# ----------------- Atualizar posição -----------------
@router.patch("/{addon_id}/position")
def update_addon_position(addon_id: int, position: int, db: Session = Depends(get_db)):
    db_addon = db.query(Addon).filter(Addon.id == addon_id).first()
    if not db_addon:
        raise HTTPException(status_code=404, detail="Adicional não encontrado")

    db_addon.position = position
    db.commit()
    db.refresh(db_addon)
    return db_addon
