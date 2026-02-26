from pydantic import BaseModel
from typing import Optional


class UserCreate(BaseModel):
    email: str
    password: str
    is_active: Optional[bool] = True


class LoginRequest(BaseModel):
    email: str
    password: str


class PasswordUpdate(BaseModel):
    old_password: str
    new_password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"