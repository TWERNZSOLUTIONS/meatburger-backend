from fastapi import APIRouter, HTTPException, Depends, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import List, Optional
import os, shutil, time

from app.models.admin.admin_product import Product
from app.models.admin.admin_category import Category
from app.schemas.admin.admin_product import ProductOut
from app.database import get_db

router = APIRouter(tags=["Admin Products"])

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# --------------------------
# CRIAR PRODUTO
# --------------------------
@router.post("/products/", response_model=ProductOut, status_code=201)
def create_product(
    name: str = Form(...),
    description: Optional[str] = Form(None),
    price: float = Form(...),
    category_id: int = Form(...),
    active: bool = Form(True),
    burger_of_the_month: bool = Form(False),
    image: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    # valida categoria
    category = db.query(Category).filter(Category.id == category_id, Category.active == True).first()
    if not category:
        raise HTTPException(status_code=404, detail="Categoria não encontrada ou inativa")

    # desmarcar burger do mês se necessário
    if burger_of_the_month:
        db.query(Product).update({Product.burger_of_the_month: False})

    # salvar imagem com timestamp para evitar sobrescrever
    timestamp = int(time.time())
    filename = f"{timestamp}_{image.filename}"
    file_path = os.path.join(UPLOAD_DIR, filename)

    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(image.file, buffer)
        image_url = f"/uploads/{filename}"
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao salvar imagem: {str(e)}")

    db_product = Product(
        name=name,
        description=description,
        price=price,
        category_id=category_id,
        active=active,
        burger_of_the_month=burger_of_the_month,
        image_url=image_url,
    )

    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


# --------------------------
# LISTAR PRODUTOS
# --------------------------
@router.get("/products/", response_model=List[ProductOut])
def list_products(db: Session = Depends(get_db)):
    try:
        return db.query(Product).order_by(Product.burger_of_the_month.desc(), Product.position.asc()).all()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao listar produtos: {str(e)}")


# --------------------------
# BUSCAR PRODUTO POR ID
# --------------------------
@router.get("/products/{product_id}", response_model=ProductOut)
def get_product(product_id: int, db: Session = Depends(get_db)):
    db_product = db.query(Product).filter(Product.id == product_id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    return db_product


# --------------------------
# ATUALIZAR PRODUTO
# --------------------------
@router.put("/products/{product_id}", response_model=ProductOut)
def update_product(
    product_id: int,
    name: Optional[str] = Form(None),
    description: Optional[str] = Form(None),
    price: Optional[float] = Form(None),
    category_id: Optional[int] = Form(None),
    active: Optional[bool] = Form(None),
    burger_of_the_month: Optional[bool] = Form(None),
    image: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db),
):
    db_product = db.query(Product).filter(Product.id == product_id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Produto não encontrado")

    if name is not None:
        db_product.name = name
    if description is not None:
        db_product.description = description
    if price is not None:
        db_product.price = price
    if category_id is not None:
        # valida categoria antes de atualizar
        category = db.query(Category).filter(Category.id == category_id, Category.active == True).first()
        if not category:
            raise HTTPException(status_code=404, detail="Categoria não encontrada ou inativa")
        db_product.category_id = category_id
    if active is not None:
        db_product.active = active
    if burger_of_the_month is not None:
        db.query(Product).update({Product.burger_of_the_month: False})
        db_product.burger_of_the_month = burger_of_the_month

    if image:
        timestamp = int(time.time())
        filename = f"{timestamp}_{image.filename}"
        file_path = os.path.join(UPLOAD_DIR, filename)
        try:
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(image.file, buffer)
            db_product.image_url = f"/uploads/{filename}"
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Erro ao salvar imagem: {str(e)}")

    db.commit()
    db.refresh(db_product)
    return db_product


# --------------------------
# DELETAR PRODUTO
# --------------------------
@router.delete("/products/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db)):
    db_product = db.query(Product).filter(Product.id == product_id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    db.delete(db_product)
    db.commit()
    return {"detail": "Produto deletado com sucesso"}


# --------------------------
# UPLOAD DE IMAGEM SEPARADO
# --------------------------
@router.post("/upload", status_code=201)
async def upload_image(file: UploadFile = File(...)):
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    timestamp = int(time.time())
    filename = f"{timestamp}_{file.filename}"
    file_path = os.path.join(UPLOAD_DIR, filename)

    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao salvar imagem: {str(e)}")

    return {"url": f"/uploads/{filename}"}
