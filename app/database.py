# app/database.py
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import psycopg2
from urllib.parse import urlparse

# 🔹 Carrega variáveis de ambiente
load_dotenv()

# 🔹 URL de conexão do banco
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("❌ DATABASE_URL não encontrada no arquivo .env")

# 🔹 Ajusta o formato da URL se necessário (compatível com SQLAlchemy)
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

# 🔹 Cria engine e sessão
engine = create_engine(DATABASE_URL, echo=True, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 🔹 Base para os modelos ORM
Base = declarative_base()


# 🔹 Dependência para injeção de sessão nos endpoints
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# 🔹 Função auxiliar para testar conexão ao banco
def test_connection():
    url = urlparse(DATABASE_URL)
    conn_params = {
        "host": url.hostname,
        "port": url.port or 5432,
        "user": url.username,
        "password": url.password,
        "database": url.path.lstrip("/"),
    }

    try:
        conn = psycopg2.connect(**conn_params)
        conn.close()
        print("✅ Conexão OK com o banco PostgreSQL!")
    except Exception as e:
        print("❌ Falha ao conectar no banco:", e)


# 🔹 Executa o teste de conexão se rodar diretamente
if __name__ == "__main__":
    test_connection()
