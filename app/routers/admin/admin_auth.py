# app/routers/admin/admin_auth.py

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.admin.admin_schema import AdminLogin, AdminResponse
from app.models.admin import Admin
from app.utils.security import verify_password, create_access_token

router = APIRouter(tags=["Admin Auth"])

@router.post("/login", response_model=AdminResponse)
def login_admin(data: AdminLogin, db: Session = Depends(get_db)):
    """
    Endpoint para login do admin.
    Retorna token JWT e informações básicas do usuário.
    """
    admin = db.query(Admin).filter(Admin.username == data.username).first()

    if not admin or not verify_password(data.password, admin.password):
        raise HTTPException(status_code=401, detail="Usuário ou senha incorretos")

    access_token = create_access_token({"sub": admin.username})

    return AdminResponse(
    id=admin.id,
    username=admin.username,
    email=admin.email,
    access_token=access_token,
    token_type="bearer"
)
