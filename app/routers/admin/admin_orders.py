from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.database import get_db
from app.models.admin.admin_order import AdminOrder
from app.schemas.admin.admin_order import AdminOrderCreate, AdminOrderUpdate, AdminOrderResponse

router = APIRouter(tags=["Admin Orders"])

# 🔹 Criar nova comanda
@router.post("/", response_model=AdminOrderResponse)
def create_admin_order(order: AdminOrderCreate, db: Session = Depends(get_db)):
    """Cria nova comanda e gera order_number automático."""
    last_order_number = db.query(func.max(AdminOrder.order_number)).scalar() or 0
    new_order_number = last_order_number + 1

    db_order = AdminOrder(
        order_number=new_order_number,
        customer_name=order.customer_name,
        customer_phone=order.customer_phone,
        customer_address=order.customer_address,
        payment_method=order.payment_method,
        items=[item.dict() for item in order.items],  # JSON serializável
        total=order.total,
        observations=order.observations,
        delivery_fee=order.delivery_fee,
    )

    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order

# 🔹 Listar todas as comandas
@router.get("/", response_model=list[AdminOrderResponse])
def list_admin_orders(db: Session = Depends(get_db)):
    return db.query(AdminOrder).order_by(AdminOrder.created_at.asc()).all()

# 🔹 Obter comanda específica
@router.get("/{order_id}", response_model=AdminOrderResponse)
def get_admin_order(order_id: int, db: Session = Depends(get_db)):
    order = db.query(AdminOrder).filter(AdminOrder.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Comanda não encontrada")
    return order

# 🔹 Atualizar comanda
@router.put("/{order_id}", response_model=AdminOrderResponse)
def update_admin_order(order_id: int, order_data: AdminOrderUpdate, db: Session = Depends(get_db)):
    order = db.query(AdminOrder).filter(AdminOrder.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Comanda não encontrada")

    for key, value in order_data.dict(exclude_unset=True).items():
        if key == "items" and value is not None:
            setattr(order, key, [item.dict() for item in value])
        else:
            setattr(order, key, value)

    db.commit()
    db.refresh(order)
    return order

# 🔹 Excluir comanda
@router.delete("/{order_id}")
def delete_admin_order(order_id: int, db: Session = Depends(get_db)):
    order = db.query(AdminOrder).filter(AdminOrder.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Comanda não encontrada")
    db.delete(order)
    db.commit()
    return {"message": f"Comanda {order_id} excluída com sucesso."}

# 🔹 Gerar texto formatado (WhatsApp/Impressão)
@router.get("/{order_id}/printable")
def get_printable_order(order_id: int, db: Session = Depends(get_db)):
    order = db.query(AdminOrder).filter(AdminOrder.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Comanda não encontrada")

    items_text = ""
    for item in order.items:
        items_text += f"{item['name']} x{item['quantity']} - R$ {item['price']:.2f}\n"
        if item.get("addons"):
            items_text += "  Adicionais:\n"
            for addon in item["addons"]:
                items_text += f"  - {addon['name']} x{addon['quantity']} (R$ {addon['price']:.2f})\n"
        items_text += "\n"

    text = (
        f"🏷️ *{order.customer_name} - Pedido: {order.order_number}*\n\n"
        f"{items_text}"
        f"🧾 *Forma de Pagamento:* {order.payment_method}\n"
        f"💰 *Total:* R$ {order.total:.2f}\n\n"
        f"📞 *Telefone:* {order.customer_phone or '-'}\n"
        f"🏠 *Endereço:* {order.customer_address or '-'}\n"
        f"📝 *Observações:* {order.observations or '-'}\n"
        f"🚚 *Taxa de Entrega:* R$ {order.delivery_fee:.2f}\n"
    )
    return {"formatted_order": text}
