from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List

from app.models.admin.admin_category import Category
from app.schemas.admin.admin_category import CategoryCreate, CategoryUpdate, CategoryOut
from app.database import get_db

router = APIRouter()
    #prefix="/admin/categories",
    #tags=["Admin Categories"]

# ----------------- Criar categoria -----------------
@router.post("/", response_model=CategoryOut)
def create_category(category: CategoryCreate, db: Session = Depends(get_db)):
    db_category = Category(**category.dict())
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

# ----------------- Listar categorias -----------------
@router.get("/", response_model=List[CategoryOut])
def list_categories(db: Session = Depends(get_db)):
    return db.query(Category).order_by(Category.position).all()

# ----------------- Obter categoria por ID -----------------
@router.get("/{category_id}", response_model=CategoryOut)
def get_category(category_id: int, db: Session = Depends(get_db)):
    db_category = db.query(Category).filter(Category.id == category_id).first()
    if not db_category:
        raise HTTPException(status_code=404, detail="Categoria não encontrada")
    return db_category

# ----------------- Atualizar categoria -----------------
@router.put("/{category_id}", response_model=CategoryOut)
def update_category(category_id: int, category: CategoryUpdate, db: Session = Depends(get_db)):
    db_category = db.query(Category).filter(Category.id == category_id).first()
    if not db_category:
        raise HTTPException(status_code=404, detail="Categoria não encontrada")

    for key, value in category.dict(exclude_unset=True).items():
        setattr(db_category, key, value)

    db.commit()
    db.refresh(db_category)
    return db_category

# ----------------- Deletar categoria -----------------
@router.delete("/{category_id}")
def delete_category(category_id: int, db: Session = Depends(get_db)):
    db_category = db.query(Category).filter(Category.id == category_id).first()
    if not db_category:
        raise HTTPException(status_code=404, detail="Categoria não encontrada")

    db.delete(db_category)
    db.commit()
    return {"detail": "Categoria deletada com sucesso"}

# ----------------- Atualizar posição -----------------
@router.patch("/{category_id}/position")
def update_category_position(category_id: int, position: int, db: Session = Depends(get_db)):
    db_category = db.query(Category).filter(Category.id == category_id).first()
    if not db_category:
        raise HTTPException(status_code=404, detail="Categoria não encontrada")

    db_category.position = position
    db.commit()
    db.refresh(db_category)
    return db_category
