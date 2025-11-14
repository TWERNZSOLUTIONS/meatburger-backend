from pydantic import BaseModel, EmailStr
from pydantic import ConfigDict

class AdminLogin(BaseModel):
    username: str
    password: str

class AdminResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    access_token: str
    token_type: str

    model_config = ConfigDict(from_attributes=True)
