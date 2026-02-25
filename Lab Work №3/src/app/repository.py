from models import test_users_db, User


class UserRepository:

    def get_by_email(self, email: str) -> User | None:
        return test_users_db.get(email)