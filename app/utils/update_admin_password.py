from app.database import SessionLocal
from app.models.admin import Admin
from app.utils.security import get_password_hash

def update_admin_password():
    db = SessionLocal()
    username = "MeatBurger"  # admin que você quer atualizar
    new_password = "Admin159*"  # nova senha

    admin = db.query(Admin).filter(Admin.username == username).first()
    if not admin:
        print(f"⚠️ Admin {username} não encontrado.")
        db.close()
        return

    # gera hash com truncamento em 72 bytes
    hashed = get_password_hash(new_password[:72])
    admin.password = hashed
    db.commit()
    print(f"✅ Senha do admin '{username}' atualizada com sucesso (senha: {new_password})")
    db.close()

if __name__ == "__main__":
    update_admin_password()
