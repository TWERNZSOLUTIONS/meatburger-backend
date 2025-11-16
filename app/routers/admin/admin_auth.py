from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.admin.admin_schema import AdminLogin, AdminResponse
from app.models.admin.admin import Admin
from app.utils.security import verify_password, create_access_token, hash_password
from app.dependencies import get_current_admin  # função que retorna o admin autenticado

router = APIRouter(tags=["Admin Auth"])

@router.post("/login", response_model=AdminResponse)
def login_admin(data: AdminLogin, db: Session = Depends(get_db)):
    """
    Login do admin -> POST /admin/login
    Retorna: id, username, email, access_token, token_type
    """
    admin = db.query(Admin).filter(Admin.username == data.username).first()

    if not admin or not verify_password(data.password, admin.password):
        raise HTTPException(status_code=400, detail="Usuário ou senha incorretos")

    access_token = create_access_token({"sub": admin.username})

    return AdminResponse(
        id=admin.id,
        username=admin.username,
        email=admin.email,
        access_token=access_token,
        token_type="bearer"
    )

@router.get("/check")
def check_status():
    return {"status": "Auth ativo e rodando 🚀"}

# -------------------------------
# 🔹 Novo endpoint para alterar usuário e senha
# -------------------------------
from pydantic import BaseModel, constr

class AdminCredentialsUpdate(BaseModel):
    username: constr(min_length=3)
    password: constr(min_length=6)

@router.put("/change_credentials", response_model=AdminResponse)
def change_credentials(
    data: AdminCredentialsUpdate,
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin)
):
    """
    Altera username e senha do admin logado.
    """
    # Atualiza username e senha
    current_admin.username = data.username
    current_admin.password = hash_password(data.password)

    db.commit()
    db.refresh(current_admin)

    access_token = create_access_token({"sub": current_admin.username})

    return AdminResponse(
        id=current_admin.id,
        username=current_admin.username,
        email=current_admin.email,
        access_token=access_token,
        token_type="bearer"
    )
