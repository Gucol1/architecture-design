from repository import UserRepository
from security import verify_password, hash_password, create_token
from models import User


class AuthService:

    def __init__(self, repo: UserRepository):
        self.repo = repo

    def register(self, email: str, password: str, is_active: bool) -> User:
        if self.repo.get_by_email(email):
            raise ValueError("Пользователь уже существует")

        return self.repo.create(email, hash_password(password), is_active)

    def login(self, email: str, password: str) -> str:
        user = self.repo.get_by_email(email)

        if not user or not verify_password(password, user.password_hash):
            raise ValueError("Неверные данные")

        return create_token(user.id)

    def update_password(self, user: User, old_password: str, new_password: str):
        if not verify_password(old_password, user.password_hash):
            raise ValueError("Неправильно введён пароль")

        user.password_hash = hash_password(new_password)