from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from typing import List
from sqlalchemy.sql import func

from app.models.admin.admin_category import Category
from app.schemas.admin.admin_category import CategoryCreate, CategoryUpdate, CategoryOut
from app.database import get_db

router = APIRouter(tags=["Admin Categories"])

@router.post("/categories/", response_model=CategoryOut, status_code=201)
def create_category(category: CategoryCreate, db: Session = Depends(get_db)):
    try:
        db_category = Category(
            **category.dict(),
            created_at=func.now(),
            updated_at=func.now()
        )
        db.add(db_category)
        db.commit()
        db.refresh(db_category)
        return db_category
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Erro ao criar categoria: {str(e)}")

@router.get("/categories/", response_model=List[CategoryOut])
def list_categories(db: Session = Depends(get_db)):
    return db.query(Category).order_by(Category.position.asc(), Category.name.asc()).all()

@router.get("/categories/{category_id}", response_model=CategoryOut)
def get_category(category_id: int, db: Session = Depends(get_db)):
    db_category = db.query(Category).filter(Category.id == category_id).first()
    if not db_category:
        raise HTTPException(status_code=404, detail="Categoria não encontrada")
    return db_category

@router.put("/categories/{category_id}", response_model=CategoryOut)
def update_category(category_id: int, category: CategoryUpdate, db: Session = Depends(get_db)):
    db_category = db.query(Category).filter(Category.id == category_id).first()
    if not db_category:
        raise HTTPException(status_code=404, detail="Categoria não encontrada")
    try:
        for key, value in category.dict(exclude_unset=True).items():
            setattr(db_category, key, value)
        db_category.updated_at = func.now()
        db.commit()
        db.refresh(db_category)
        return db_category
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Erro ao atualizar categoria: {str(e)}")

@router.delete("/categories/{category_id}")
def delete_category(category_id: int, db: Session = Depends(get_db)):
    db_category = db.query(Category).filter(Category.id == category_id).first()
    if not db_category:
        raise HTTPException(status_code=404, detail="Categoria não encontrada")
    try:
        db.delete(db_category)
        db.commit()
        return {"detail": f"Categoria '{db_category.name}' deletada com sucesso"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Erro ao deletar categoria: {str(e)}")

@router.patch("/categories/{category_id}/position", response_model=CategoryOut)
def update_category_position(category_id: int, position: int = Query(..., ge=0), db: Session = Depends(get_db)):
    db_category = db.query(Category).filter(Category.id == category_id).first()
    if not db_category:
        raise HTTPException(status_code=404, detail="Categoria não encontrada")
    try:
        db_category.position = position
        db_category.updated_at = func.now()
        db.commit()
        db.refresh(db_category)
        return db_category
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Erro ao atualizar posição: {str(e)}")

@router.patch("/categories/{category_id}/toggle", response_model=CategoryOut)
def toggle_category_active(category_id: int, db: Session = Depends(get_db)):
    db_category = db.query(Category).filter(Category.id == category_id).first()
    if not db_category:
        raise HTTPException(status_code=404, detail="Categoria não encontrada")
    try:
        db_category.active = not db_category.active
        db_category.updated_at = func.now()
        db.commit()
        db.refresh(db_category)
        return db_category
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Erro ao alternar status da categoria: {str(e)}")
