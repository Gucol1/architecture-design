from fastapi import Header, HTTPException, Depends
from sqlalchemy.orm import Session
from .database import get_db
from .repository import UserRepository
from .security import decode_token

def get_repo(db: Session = Depends(get_db)):
    return UserRepository(db)

def get_current_user(
    authorization: str = Header(...),
    repo: UserRepository = Depends(get_repo),
):
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing Bearer token")

    token = authorization.split()[1]

    if repo.blacklist_contains(token):
        raise HTTPException(status_code=401, detail="Token revoked")

    try:
        payload = decode_token(token)
        user_id = payload.get("sub")
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")

    user = repo.get_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user