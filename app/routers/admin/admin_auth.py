from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.admin.admin_schema import AdminLogin, AdminResponse
from app.models.admin.admin import Admin
from app.utils.security import verify_password, create_access_token

router = APIRouter(
    prefix="/admin/auth",
    tags=["Admin Auth"]
)

@router.post("/login", response_model=AdminResponse)
def login_admin(data: AdminLogin, db: Session = Depends(get_db)):
    """
    Login do admin -> POST /admin/auth/login
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
    """
    Verifica se a autenticação está funcionando -> GET /admin/auth/check
    """
    return {"status": "Auth ativo e rodando 🚀"}
