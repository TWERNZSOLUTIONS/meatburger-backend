# backend/app/schemas/admin/admin_schema.py
from pydantic import BaseModel, EmailStr

class AdminLogin(BaseModel):
    username: str
    password: str

class AdminResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    access_token: str   # token JWT retornado
    token_type: str     # tipo do token, ex: "bearer"

    class Config:
        from_attributes = True
