from pydantic import BaseModel, EmailStr
from typing import Optional

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    is_active: Optional[bool] = True

class UserUpdate(BaseModel):
    email: EmailStr
    is_active: Optional[bool] = True

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class PasswordUpdate(BaseModel):
    old_password: str
    new_password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

class UserOut(BaseModel):
    id: str
    email: EmailStr
    is_active: bool