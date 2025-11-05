# backend/app/schemas/admin/admin_schema.py
from pydantic import BaseModel, EmailStr

class AdminLogin(BaseModel):
    username: str
    password: str

class AdminResponse(BaseModel):
    id: int
    username: str
    email: EmailStr

    class Config:
        from_attributes = True  # <- substitui o orm_mode
