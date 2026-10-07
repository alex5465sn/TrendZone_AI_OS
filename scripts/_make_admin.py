from app.database.session import SessionLocal
from app.models.user import User
from app.repositories.user_repository import UserRepository

db = SessionLocal()
user = UserRepository.get_by_email(db, "admin@trendzone.com")
if user:
    print(f"Usuário encontrado: {user.email}")
    print(f"Role atual: {user.role}")
    user.role = "ADMIN"
    UserRepository.update(db, user)
    print(f"Role atualizado para: {user.role}")
else:
    print("Usuário não encontrado")
db.close()
