from repository import UserRepository
from security import verify_password, create_access_token


class AuthService:

    def __init__(self, repo: UserRepository):
        self.repo = repo

    def authenticate(self, email: str, password: str):
        user = self.repo.get_by_email(email)

        if not user:
            return None

        if not verify_password(password, user.password_hash):
            return None

        token = create_access_token(user.id)

        return token