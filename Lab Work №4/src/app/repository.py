from uuid import uuid4
from datetime import datetime
from models import User, users_db


class UserRepository:

    def create(self, email: str, password_hash: str, is_active: bool) -> User:
        user_id = str(uuid4())
        user = User(
            id=user_id,
            email=email,
            password_hash=password_hash,
            is_active=is_active,
            created_at=datetime.now()
        )
        users_db[user_id] = user
        return user

    def get_by_id(self, user_id: str) -> User | None:
        return users_db.get(user_id)

    def get_by_email(self, email: str) -> User | None:
        for user in users_db.values():
            if user.email == email:
                return user
        return None

    def list(self, limit: int, offset: int):
        all_users = list(users_db.values())
        return all_users[offset: offset + limit], len(all_users)

    def delete(self, user_id: str):
        if user_id in users_db:
            del users_db[user_id]