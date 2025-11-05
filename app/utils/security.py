# app/utils/security.py
from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import JWTError, jwt
from dotenv import load_dotenv
import os

# Carrega o .env
load_dotenv()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60  # 1h

def get_password_hash(password: str) -> str:
    """Gera o hash seguro da senha."""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifica se a senha está correta."""
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict):
    """Cria o token JWT"""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
