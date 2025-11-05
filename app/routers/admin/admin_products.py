from fastapi import APIRouter, HTTPException, Depends, UploadFile, File
from sqlalchemy.orm import Session
from typing import List
import os
import shutil

from app.models.admin.admin_product import Product
from app.models.admin.admin_category import Category
from app.schemas.admin.admin_product import ProductCreate, ProductUpdate, ProductOut
from app.database import get_db

router = APIRouter(
    prefix="/products",
    tags=["Admin - Produtos"]
)

UPLOAD_DIR = "uploads"

# ----------------- Criar produto -----------------
@router.post("/", response_model=ProductOut)
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    category = db.query(Category).filter(Category.id == product.category_id, Category.active == True).first()
    if not category:
        raise HTTPException(status_code=404, detail="Categoria não encontrada ou inativa")

    if product.burger_of_the_month:
        db.query(Product).update({Product.burger_of_the_month: False})

    db_product = Product(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

# ----------------- Listar produtos -----------------
@router.get("/", response_model=List[ProductOut])
def list_products(db: Session = Depends(get_db)):
    try:
        return db.query(Product).order_by(Product.burger_of_the_month.desc(), Product.position).all()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao listar produtos: {str(e)}")

# ----------------- Obter produto -----------------
@router.get("/{product_id}", response_model=ProductOut)
def get_product(product_id: int, db: Session = Depends(get_db)):
    db_product = db.query(Product).filter(Product.id == product_id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    return db_product

# ----------------- Atualizar produto -----------------
@router.put("/{product_id}", response_model=ProductOut)
def update_product(product_id: int, product: ProductUpdate, db: Session = Depends(get_db)):
    db_product = db.query(Product).filter(Product.id == product_id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Produto não encontrado")

    if product.burger_of_the_month:
        db.query(Product).update({Product.burger_of_the_month: False})

    for key, value in product.dict(exclude_unset=True).items():
        setattr(db_product, key, value)

    db.commit()
    db.refresh(db_product)
    return db_product

# ----------------- Deletar produto -----------------
@router.delete("/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db)):
    db_product = db.query(Product).filter(Product.id == product_id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Produto não encontrado")

    db.delete(db_product)
    db.commit()
    return {"detail": "Produto deletado com sucesso"}

# ----------------- Atualizar posição -----------------
@router.patch("/{product_id}/position")
def update_product_position(product_id: int, position: int, db: Session = Depends(get_db)):
    db_product = db.query(Product).filter(Product.id == product_id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Produto não encontrado")

    db_product.position = position
    db.commit()
    db.refresh(db_product)
    return db_product

# ----------------- Upload de imagem -----------------
@router.post("/upload-image/")
async def upload_image(file: UploadFile = File(...)):
    """Envia imagem e retorna URL"""
    try:
        os.makedirs(UPLOAD_DIR, exist_ok=True)
        file_path = os.path.join(UPLOAD_DIR, file.filename)

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        return {"url": f"/uploads/{file.filename}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao enviar imagem: {str(e)}")
