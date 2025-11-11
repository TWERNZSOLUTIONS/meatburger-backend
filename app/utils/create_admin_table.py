# backend/app/utils/create_admin_table.py

import psycopg2
from werkzeug.security import generate_password_hash
from urllib.parse import urlparse
import os
from dotenv import load_dotenv

# 🔹 Carrega variáveis do .env
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("❌ DATABASE_URL não encontrada no arquivo .env")

# 🔹 Converte DATABASE_URL para parâmetros do psycopg2
url = urlparse(DATABASE_URL)
DB_PARAMS = {
    "host": url.hostname,
    "port": url.port or 5432,
    "user": url.username,
    "password": url.password,
    "database": url.path[1:],  # remove a barra inicial
}

def create_admin_table():
    conn = None
    try:
        conn = psycopg2.connect(**DB_PARAMS)
        cur = conn.cursor()

        # Cria tabela admins se não existir
        cur.execute("""
            CREATE TABLE IF NOT EXISTS admins (
                id SERIAL PRIMARY KEY,
                username VARCHAR(100) UNIQUE NOT NULL,
                email VARCHAR(300) UNIQUE NOT NULL,
                password VARCHAR(300) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)

        # Cria um admin padrão, se ainda não existir
        admin_email = "meatburger.py@outlook.com"
        admin_user = "MeatBurger"
        admin_pass = generate_password_hash("Admin159*")

        cur.execute("SELECT * FROM admins WHERE email = %s;", (admin_email,))
        existing = cur.fetchone()

        if existing:
            print("⚠️ Admin já existe no banco de dados.")
        else:
            cur.execute(
                "INSERT INTO admins (username, email, password) VALUES (%s, %s, %s)",
                (admin_user, admin_email, admin_pass)
            )
            conn.commit()
            print("✅ Admin criado com sucesso!")

        conn.commit()

    except psycopg2.Error as e:
        print(f"❌ Erro ao configurar tabela admin: {e}")
    finally:
        if conn:
            conn.close()


if __name__ == "__main__":
    print("🚀 Criando tabela e usuário admin...")
    create_admin_table()
    print("✅ Processo concluído com sucesso!")
