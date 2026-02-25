from fastapi import FastAPI, HTTPException
from schemas import LoginRequest, TokenResponse
from repository import UserRepository
from service import AuthService
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

repo = UserRepository()
auth_service = AuthService(repo)


@app.post("/login", response_model=TokenResponse)
def login(data: LoginRequest):
    token = auth_service.authenticate(data.email, data.password)

    if not token:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    return TokenResponse(access_token=token)