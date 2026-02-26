from fastapi import Header, HTTPException
from security import decode_token
from repository import UserRepository
from models import blacklist


repo = UserRepository()


def get_current_user(authorization: str = Header(...)):
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401)

    token = authorization.split()[1]

    if token in blacklist:
        raise HTTPException(status_code=401)

    try:
        payload = decode_token(token)
        user_id = payload.get("sub")
    except:
        raise HTTPException(status_code=401)

    user = repo.get_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404)

    return user