from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from datetime import datetime

# 🔹 Imports corretos da estrutura atual
from app.database import get_db
from app.models.admin import Product, Category, Addon, AdminOrder
from app.schemas.admin.admin_order import AdminOrderCreate, AdminOrderResponse

# 🔹 Define o router principal do cliente
client_router = APIRouter(
    prefix="/client",
    tags=["Client"],
)

# 🟢 Listar categorias disponíveis
@client_router.get("/categories")
def get_categories(db: Session = Depends(get_db)):
    categories = db.query(Category).all()
    if not categories:
        raise HTTPException(status_code=404, detail="Nenhuma categoria encontrada.")
    return categories

# 🟢 Listar produtos disponíveis
@client_router.get("/products")
def get_products(db: Session = Depends(get_db)):
    products = db.query(Product).all()
    if not products:
        raise HTTPException(status_code=404, detail="Nenhum produto encontrado.")
    return products

# 🟢 Listar adicionais
@client_router.get("/addons")
def get_addons(db: Session = Depends(get_db)):
    addons = db.query(Addon).all()
    if not addons:
        raise HTTPException(status_code=404, detail="Nenhum adicional encontrado.")
    return addons

# 🟢 Criar novo pedido (cliente)
@client_router.post("/orders", response_model=AdminOrderResponse)
def create_order(order_data: AdminOrderCreate, db: Session = Depends(get_db)):
    try:
        new_order = AdminOrder(
            customer_name=order_data.customer_name,
            customer_phone=order_data.customer_phone,
            customer_address=order_data.customer_address,
            payment_method=order_data.payment_method,
            total=order_data.total,
            observations=order_data.observations,
            delivery_fee=order_data.delivery_fee,
            created_at=datetime.utcnow(),
            items=[
                {
                    "name": item.name,
                    "quantity": item.quantity,
                    "price": item.price,
                    "addons": [
                        {"name": addon.name, "quantity": addon.quantity, "price": addon.price}
                        for addon in (item.addons or [])
                    ],
                }
                for item in order_data.items
            ],
        )

        db.add(new_order)
        db.commit()
        db.refresh(new_order)

        return new_order

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Erro ao criar pedido: {str(e)}")
