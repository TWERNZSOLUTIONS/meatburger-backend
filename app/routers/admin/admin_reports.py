# backend/app/routers/admin/admin_reports.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, timedelta
from typing import List

from app.database import get_db
from app.models.admin.admin_order import AdminOrder
from app.schemas.admin.admin_reports import PaymentMethodReport, TimePeriodReport

router = APIRouter(
    prefix="/reports",  # 🔹 prefixo adicionado para padronização
    tags=["Admin Reports"]
)

# ----------------- Relatório financeiro por período -----------------
@router.get("/finance", response_model=TimePeriodReport)
def finance_report(days: int = 30, db: Session = Depends(get_db)):
    """
    Retorna relatório de pedidos e faturamento no período informado (últimos X dias).
    """
    period_start = datetime.utcnow() - timedelta(days=days)
    period_end = datetime.utcnow()

    total_orders = db.query(AdminOrder).filter(AdminOrder.created_at >= period_start).count()

    total_revenue = (
        db.query(func.coalesce(func.sum(AdminOrder.total), 0))
        .filter(AdminOrder.created_at >= period_start)
        .scalar()
    )

    return TimePeriodReport(
        period_start=period_start.date(),
        period_end=period_end.date(),
        total_orders=total_orders,
        total_revenue=float(total_revenue),
    )

# ----------------- Relatório por forma de pagamento -----------------
@router.get("/payment_methods", response_model=List[PaymentMethodReport])
def payment_method_report(db: Session = Depends(get_db)):
    """
    Retorna relatório agrupado por forma de pagamento,
    com total de pedidos e faturamento por método.
    """
    results = (
        db.query(
            AdminOrder.payment_method,
            func.count(AdminOrder.id).label("total_orders"),
            func.coalesce(func.sum(AdminOrder.total), 0).label("total_revenue")
        )
        .group_by(AdminOrder.payment_method)
        .all()
    )

    report = [
        PaymentMethodReport(
            payment_method=payment_method,
            total_orders=total_orders,
            total_revenue=float(total_revenue),
        )
        for payment_method, total_orders, total_revenue in results
    ]

    return report
