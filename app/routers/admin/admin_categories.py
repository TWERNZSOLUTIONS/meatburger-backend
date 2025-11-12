from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from typing import List

from app.models.admin.admin_category import Category
from app.schemas.admin.admin_category import CategoryCreate, CategoryUpdate, CategoryOut
from app.database import get_db

router = APIRouter(
    prefix="/categories",
    tags=["Admin - Categories"]
)

# ----------------- Criar categoria -----------------
@router.post("/", response_model=CategoryOut)
def create_category(category: CategoryCreate, db: Session = Depends(get_db)):
    """Cria uma nova categoria."""
    db_category = Category(**category.dict())
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

# ----------------- Listar categorias -----------------
@router.get("/", response_model=List[CategoryOut])
def list_categories(db: Session = Depends(get_db)):
    """Lista todas as categorias ordenadas."""
    return db.query(Category).order_by(Category.position, Category.name).all()

# ----------------- Obter categoria por ID -----------------
@router.get("/{category_id}", response_model=CategoryOut)
def get_category(category_id: int, db: Session = Depends(get_db)):
    """Obtém uma categoria específica pelo ID."""
    db_category = db.query(Category).filter(Category.id == category_id).first()
    if not db_category:
        raise HTTPException(status_code=404, detail="Categoria não encontrada")
    return db_category

# ----------------- Atualizar categoria -----------------
@router.put("/{category_id}", response_model=CategoryOut)
def update_category(category_id: int, category: CategoryUpdate, db: Session = Depends(get_db)):
    """Atualiza uma categoria existente."""
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
    """Exclui uma categoria pelo ID."""
    db_category = db.query(Category).filter(Category.id == category_id).first()
    if not db_category:
        raise HTTPException(status_code=404, detail="Categoria não encontrada")

    db.delete(db_category)
    db.commit()
    return {"detail": f"Categoria '{db_category.name}' deletada com sucesso"}

# ----------------- Atualizar posição -----------------
@router.patch("/{category_id}/position", response_model=CategoryOut)
def update_category_position(category_id: int, position: int = Query(..., ge=0), db: Session = Depends(get_db)):
    """Atualiza a posição (ordem) da categoria."""
    db_category = db.query(Category).filter(Category.id == category_id).first()
    if not db_category:
        raise HTTPException(status_code=404, detail="Categoria não encontrada")

    db_category.position = position
    db.commit()
    db.refresh(db_category)
    return db_category

# ----------------- Ativar/desativar categoria -----------------
@router.patch("/{category_id}/toggle", response_model=CategoryOut)
def toggle_category_active(category_id: int, db: Session = Depends(get_db)):
    """Ativa ou desativa uma categoria."""
    db_category = db.query(Category).filter(Category.id == category_id).first()
    if not db_category:
        raise HTTPException(status_code=404, detail="Categoria não encontrada")

    db_category.active = not db_category.active
    db.commit()
    db.refresh(db_category)
    return db_category
