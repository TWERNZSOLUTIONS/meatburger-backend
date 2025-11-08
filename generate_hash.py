from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

senha = "MeatBurger123@"
print("Hash gerado:")
print(pwd_context.hash(senha))
