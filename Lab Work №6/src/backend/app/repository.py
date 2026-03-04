from uuid import uuid4
from sqlalchemy.orm import Session
from sqlalchemy import select
from .models import User, TokenBlacklist

class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, email: str, password_hash: str, is_active: bool) -> User:
        user = User(
            id=str(uuid4()),
            email=email,
            password_hash=password_hash,
            is_active=is_active,
        )
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def get_by_id(self, user_id: str) -> User | None:
        return self.db.get(User, user_id)

    def get_by_email(self, email: str) -> User | None:
        stmt = select(User).where(User.email == email)
        return self.db.execute(stmt).scalars().first()

    def list(self, limit: int, offset: int):
        stmt = select(User).offset(offset).limit(limit)
        items = list(self.db.execute(stmt).scalars().all())
        total = self.db.query(User).count()
        return items, total

    def delete(self, user_id: str):
        user = self.get_by_id(user_id)
        if user:
            self.db.delete(user)
            self.db.commit()

    def blacklist_add(self, token: str, user_id: str):
        self.db.add(TokenBlacklist(token=token, user_id=user_id))
        self.db.commit()

    def blacklist_contains(self, token: str) -> bool:
        return self.db.get(TokenBlacklist, token) is not None