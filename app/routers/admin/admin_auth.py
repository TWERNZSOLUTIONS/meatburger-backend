# backend/app/routers/admin/admin_auth.py
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.admin.admin_schema import AdminLogin, AdminResponse
from app.models.admin import Admin
from app.utils.security import verify_password, create_access_token

# ⚠️ Sem prefixo aqui! O prefixo "/admin/auth" é definido no main.py
router = APIRouter(tags=["Admin - Auth"])

@router.post("/login", response_model=AdminResponse)
def login_admin(data: AdminLogin, db: Session = Depends(get_db)):
    """
    Endpoint de login do admin.
    Retorna token JWT e informações do usuário autenticado.
    """
    # Busca usuário admin no banco
    admin = db.query(Admin).filter(Admin.username == data.username).first()

    # Valida credenciais
    if not admin or not verify_password(data.password, admin.password):
        raise HTTPException(status_code=401, detail="Usuário ou senha incorretos")

    # Gera token JWT
    access_token = create_access_token({"sub": admin.username})

    # Retorna dados do admin logado
    return AdminResponse(
        id=admin.id,
        username=admin.username,
        email=admin.email,
        access_token=access_token,
        token_type="bearer"
    )

@router.get("/check")
def check_status():
    """Rota simples para testar se o módulo de auth está acessível."""
    return {"status": "Auth ativo e rodando 🚀"}
