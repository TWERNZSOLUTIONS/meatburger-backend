# backend/app/schemas/admin/admin_schema.py
from pydantic import BaseModel, EmailStr

# ----------------- Schemas de autenticação Admin -----------------
class AdminLogin(BaseModel):
    """Schema para login de administrador."""
    username: str
    password: str

class AdminResponse(BaseModel):
    """Schema de resposta após login, incluindo token JWT."""
    id: int
    username: str
    email: EmailStr
    access_token: str   # Token JWT retornado
    token_type: str     # Tipo do token, ex: "bearer"

    class Config:
        from_attributes = True  # ✅ Compatível com Pydantic v2
