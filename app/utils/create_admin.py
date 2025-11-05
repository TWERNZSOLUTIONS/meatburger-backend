from app.database import SessionLocal
from app.models.admin import Admin
from app.utils.security import get_password_hash

def create_admin():
    db = SessionLocal()
    username = "MeatBurger"
    email = "meatburger.py@outlook.com"
    password = "MeatBurger123@"

    existing = db.query(Admin).filter(Admin.username == username).first()
    if existing:
        print("⚠️ Já existe um admin com esse username.")
        return

    hashed = get_password_hash(password)
    new_admin = Admin(
        username=username,  # ✅ variável definida
        email=email,        # ✅ variável definida
        password=hashed
    )
    db.add(new_admin)
    db.commit()
    db.refresh(new_admin)
    print(f"✅ Admin criado com sucesso: {new_admin.username} (senha: {password})")
    db.close()

if __name__ == "__main__":
    create_admin()
