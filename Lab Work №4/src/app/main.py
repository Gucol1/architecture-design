from fastapi import FastAPI, HTTPException, Depends, Header
from schemas import UserCreate, LoginRequest, PasswordUpdate, TokenResponse
from repository import UserRepository
from service import AuthService
from dependencies import get_current_user, repo
from models import blacklist

app = FastAPI()

auth_service = AuthService(repo)


@app.post("/api/v1/users", status_code=201)
def create_user(data: UserCreate):
    try:
        user = auth_service.register(data.email, data.password, data.is_active)
        print(user)
        return user
    except ValueError:
        raise HTTPException(status_code=400)


@app.post("/api/v1/auth/login", response_model=TokenResponse)
def login(data: LoginRequest):
    try:
        token = auth_service.login(data.email, data.password)
        return TokenResponse(access_token=token)
    except ValueError:
        raise HTTPException(status_code=401)


@app.get("/api/v1/users/{user_id}")
def get_user(user_id: str, current=Depends(get_current_user)):
    user = repo.get_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404)
    return user


@app.put("/api/v1/users/{user_id}")
def update_user(user_id: str, data: UserCreate, current=Depends(get_current_user)):
    user = repo.get_by_id(user_id)
    print(user)
    if not user:
        raise HTTPException(status_code=404)

    user.email = data.email
    user.is_active = data.is_active
    return {"message": "User updated successfully"}


@app.delete("/api/v1/users/{user_id}", status_code=204)
def delete_user(user_id: str, current=Depends(get_current_user)):
    if not repo.get_by_id(user_id):
        raise HTTPException(status_code=404)

    repo.delete(user_id)


@app.put("/api/v1/users/{user_id}/password")
def update_password(user_id: str, data: PasswordUpdate, current=Depends(get_current_user)):
    user = repo.get_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404)

    try:
        auth_service.update_password(user, data.old_password, data.new_password)
        return {"message": "Password updated successfully"}
    except ValueError:
        raise HTTPException(status_code=401)


@app.get("/api/v1/users")
def list_users(limit: int = 10, offset: int = 0, current=Depends(get_current_user)):
    items, total = repo.list(limit, offset)
    return {"total": total, "items": items}


@app.post("/api/v1/auth/logout")
def logout(authorization: str = Header(...)):
    token = authorization.split()[1]
    blacklist.add(token)
    if token in blacklist:
        raise HTTPException(status_code=401)
    return {"message": "Successfully logged out"}