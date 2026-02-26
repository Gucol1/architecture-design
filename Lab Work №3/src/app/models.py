from dataclasses import dataclass
from uuid import uuid4
from security import hash_password

@dataclass
class User:
    id: str
    email: str
    password_hash: str
    is_active: bool = True


# Упрощённая база данных

test_users_db = {
    "user@example.com": User(
        id=str(uuid4()),
        email="user@example.com",
        password_hash=hash_password("password")
    )
}