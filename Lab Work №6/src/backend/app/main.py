from fastapi import FastAPI, HTTPException, Depends, Header
from sqlalchemy.orm import Session
from .schemas import UserCreate, UserUpdate, LoginRequest, PasswordUpdate, TokenResponse, UserOut
from .database import engine, Base, get_db
from .repository import UserRepository
from .service import AuthService
from .dependencies import get_current_user, get_repo

app = FastAPI(title="Auth App", version="1.0")

@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)

@app.post("/api/v1/users", status_code=201, response_model=UserOut)
def create_user(data: UserCreate, repo: UserRepository = Depends(get_repo)):
    auth_service = AuthService(repo)
    try:
        user = auth_service.register(data.email, data.password, data.is_active)
        return UserOut(id=user.id, email=user.email, is_active=user.is_active)
    except ValueError:
        raise HTTPException(status_code=400, detail="User already exists")

@app.post("/api/v1/auth/login", response_model=TokenResponse)
def login(data: LoginRequest, repo: UserRepository = Depends(get_repo)):
    auth_service = AuthService(repo)
    try:
        token = auth_service.login(data.email, data.password)
        return TokenResponse(access_token=token)
    except ValueError:
        raise HTTPException(status_code=401, detail="Invalid email or password")

@app.get("/api/v1/users/{user_id}", response_model=UserOut)
def get_user(user_id: str, current=Depends(get_current_user), repo: UserRepository = Depends(get_repo)):
    user = repo.get_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404)
    return UserOut(id=user.id, email=user.email, is_active=user.is_active)

@app.put("/api/v1/users/{user_id}")
def update_user(user_id: str, data: UserUpdate, current=Depends(get_current_user), repo: UserRepository = Depends(get_repo)):
    user = repo.get_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404)
    user.email = data.email
    user.is_active = bool(data.is_active)
    repo.db.commit()
    return {"message": "User updated successfully"}

@app.delete("/api/v1/users/{user_id}", status_code=204)
def delete_user(user_id: str, current=Depends(get_current_user), repo: UserRepository = Depends(get_repo)):
    if not repo.get_by_id(user_id):
        raise HTTPException(status_code=404)
    repo.delete(user_id)

@app.put("/api/v1/users/{user_id}/password")
def update_password(user_id: str, data: PasswordUpdate, current=Depends(get_current_user), repo: UserRepository = Depends(get_repo)):
    user = repo.get_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404)
    auth_service = AuthService(repo)
    try:
        auth_service.update_password(user, data.old_password, data.new_password)
        return {"message": "Password updated successfully"}
    except ValueError:
        raise HTTPException(status_code=401, detail="Wrong password")

@app.get("/api/v1/users")
def list_users(limit: int = 10, offset: int = 0, current=Depends(get_current_user), repo: UserRepository = Depends(get_repo)):
    items, total = repo.list(limit, offset)
    return {
        "total": total,
        "items": [{"id": u.id, "email": u.email, "is_active": u.is_active} for u in items]
    }

@app.post("/api/v1/auth/logout")
def logout(authorization: str = Header(...), current=Depends(get_current_user), repo: UserRepository = Depends(get_repo)):
    token = authorization.split()[1]
    repo.blacklist_add(token, current.id)
    return {"message": "Successfully logged out"}