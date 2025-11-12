# backend/app/schemas/admin/admin_schema.py
from pydantic import BaseModel, EmailStr
from pydantic import ConfigDict

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

    model_config = ConfigDict(from_attributes=True)  # ✅ Compatível com Pydantic v2
