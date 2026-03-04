import os
import time
import uuid
import httpx
import pytest

BASE_URL = os.getenv("BASE_URL", "http://localhost:8000")


def wait_backend():
    for _ in range(60):
        try:
            r = httpx.get(f"{BASE_URL}/docs", timeout=2)
            if r.status_code == 200:
                return
        except Exception:
            pass
        time.sleep(1)
    raise RuntimeError("Backend not ready")


@pytest.fixture(scope="session", autouse=True)
def backend_ready():
    wait_backend()


@pytest.fixture(scope="session")
def test_user_credentials():

    email = f"test-{uuid.uuid4().hex[:10]}@example.com"
    password = "Password123!"
    return email, password


@pytest.fixture(scope="session")
def ensure_user(test_user_credentials):
    email, password = test_user_credentials

    r = httpx.post(
        f"{BASE_URL}/api/v1/users",
        json={"email": email, "password": password, "is_active": True},
        timeout=10,
    )


    assert r.status_code in (201, 400)


    user_id = r.json()["id"] if r.status_code == 201 else None
    return {"email": email, "password": password, "user_id": user_id}


@pytest.fixture()
def token(ensure_user):
    email = ensure_user["email"]
    password = ensure_user["password"]

    r = httpx.post(
        f"{BASE_URL}/api/v1/auth/login",
        json={"email": email, "password": password},
        timeout=10,
    )
    assert r.status_code == 200
    return r.json()["access_token"]


@pytest.fixture()
def auth_headers(token):
    return {"Authorization": f"Bearer {token}"}


def test_login_returns_token(token):
    assert isinstance(token, str)
    assert len(token) > 10


def test_list_users_contains_created_user(ensure_user, auth_headers):
    email = ensure_user["email"]

    r = httpx.get(
        f"{BASE_URL}/api/v1/users?limit=50&offset=0",
        headers=auth_headers,
        timeout=10,
    )
    assert r.status_code == 200
    items = r.json()["items"]

    assert any(u["email"] == email for u in items)


def test_get_user_by_id_returns_correct_email(ensure_user, auth_headers):
    email = ensure_user["email"]
    user_id = ensure_user["user_id"]


    if user_id is None:
        r = httpx.get(
            f"{BASE_URL}/api/v1/users?limit=200&offset=0",
            headers=auth_headers,
            timeout=10,
        )
        assert r.status_code == 200
        items = r.json()["items"]
        user_id = next(u["id"] for u in items if u["email"] == email)

    r = httpx.get(
        f"{BASE_URL}/api/v1/users/{user_id}",
        headers=auth_headers,
        timeout=10,
    )
    assert r.status_code == 200
    assert r.json()["email"] == email


def test_logout_revokes_token(ensure_user, token):

    headers = {"Authorization": f"Bearer {token}"}

    r = httpx.post(
        f"{BASE_URL}/api/v1/auth/logout",
        headers=headers,
        timeout=10,
    )
    assert r.status_code == 200


    r = httpx.get(
        f"{BASE_URL}/api/v1/users?limit=1&offset=0",
        headers=headers,
        timeout=10,
    )
    assert r.status_code == 401