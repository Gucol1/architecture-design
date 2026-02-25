from dataclasses import dataclass
from datetime import datetime

@dataclass
class User:
    id: str
    email: str
    password_hash: str
    is_active: bool
    created_at: datetime


# in-memory упрощённая база данных
users_db: dict[str, User] = {}

# Чёрный список токенов для инвалидации токенов
blacklist: set[str] = set()