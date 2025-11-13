# app/routers/admin/admin_addons.py
from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.models.admin.admin_addon import Addon
from app.schemas.admin.admin_addon import AddonCreate, AddonUpdate, AddonOut
from app.database import get_db

router = APIRouter(tags=["Admin - Addons"])

# ======================================================
# 🔹 Criar adicional
# ======================================================
@router.post("/", response_model=AddonOut, status_code=201)
def create_addon(addon: AddonCreate, db: Session = Depends(get_db)):
    """Cria um novo adicional no sistema"""
    try:
        new_addon = Addon(**addon.dict())
        db.add(new_addon)
        db.commit()
        db.refresh(new_addon)
        return new_addon
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Erro ao criar adicional: {str(e)}")


# ======================================================
# 🔹 Listar adicionais
# ======================================================
@router.get("/", response_model=List[AddonOut])
def list_addons(
    db: Session = Depends(get_db),
    all: bool = Query(False, description="Se true, lista também inativos."),
    search: Optional[str] = Query(None, description="Busca pelo nome do adicional."),
):
    """
    Retorna lista de adicionais ativos (ou todos, se `all=True`).
    Permite busca opcional por nome.
    """
    query = db.query(Addon)

    if not all:
        query = query.filter(Addon.active == True)
    if search:
        query = query.filter(Addon.name.ilike(f"%{search}%"))

    return query.order_by(Addon.position.asc(), Addon.name.asc()).all()


# ======================================================
# 🔹 Obter adicional por ID
# ======================================================
@router.get("/{addon_id}", response_model=AddonOut)
def get_addon(addon_id: int, db: Session = Depends(get_db)):
    """Obtém um adicional específico pelo ID"""
    db_addon = db.query(Addon).filter(Addon.id == addon_id).first()
    if not db_addon:
        raise HTTPException(status_code=404, detail="Adicional não encontrado")
    return db_addon


# ======================================================
# 🔹 Atualizar adicional
# ======================================================
@router.put("/{addon_id}", response_model=AddonOut)
def update_addon(addon_id: int, addon: AddonUpdate, db: Session = Depends(get_db)):
    """Atualiza os dados de um adicional existente"""
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


# ======================================================
# 🔹 Deletar adicional
# ======================================================
@router.delete("/{addon_id}")
def delete_addon(addon_id: int, db: Session = Depends(get_db)):
    """Remove um adicional definitivamente do sistema"""
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


# ======================================================
# 🔹 Ativar/Desativar adicional (toggle)
# ======================================================
@router.patch("/{addon_id}/toggle", response_model=AddonOut)
def toggle_addon(addon_id: int, db: Session = Depends(get_db)):
    """Ativa ou desativa um adicional"""
    db_addon = db.query(Addon).filter(Addon.id == addon_id).first()
    if not db_addon:
        raise HTTPException(status_code=404, detail="Adicional não encontrado")

    try:
        db_addon.active = not db_addon.active
        db.commit()
        db.refresh(db_addon)
        return db_addon
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Erro ao alternar adicional: {str(e)}")


# ======================================================
# 🔹 Reordenar posição do adicional
# ======================================================
@router.patch("/{addon_id}/position", response_model=AddonOut)
def update_position(addon_id: int, position: int = Query(...), db: Session = Depends(get_db)):
    """Atualiza a posição (ordem) de exibição de um adicional"""
    db_addon = db.query(Addon).filter(Addon.id == addon_id).first()
    if not db_addon:
        raise HTTPException(status_code=404, detail="Adicional não encontrado")

    try:
        db_addon.position = position
        db.commit()
        db.refresh(db_addon)
        return db_addon
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Erro ao atualizar posição: {str(e)}")
