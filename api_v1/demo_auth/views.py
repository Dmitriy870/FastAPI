import secrets
import uuid
from typing import Annotated, Any

from fastapi import APIRouter, Depends, HTTPException, status, Header, Response, Cookie
from fastapi.security import HTTPBasicCredentials, HTTPBasic

router = APIRouter(prefix="/demo_auth", tags=["demo_auth"])

security = HTTPBasic()


@router.get("/basic-aunt/")
def demo_basic_aunt_credentials(
    credentials: Annotated[HTTPBasicCredentials, Depends(security)]
):
    return {
        "username": credentials.username,
        "password": credentials.password,
    }


log_in_data = {"admin": "admin", "jon": "root"}


def get_auth_user_username(
    credentials: Annotated[HTTPBasicCredentials, Depends(security)],
):
    unauthed_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid username or password",
        # headers={"WWW-Authenticate": "Basic"},
    )
    correct_password = log_in_data.get(credentials.username)
    if correct_password is None:
        raise unauthed_exc

    if not secrets.compare_digest(
        credentials.password.encode("utf-8"),
        correct_password.encode("utf-8"),
    ):
        raise unauthed_exc
    return credentials.username


@router.get("/basic-auth/")
def demo_basic_auth_username(
    auth_username: str = Depends(get_auth_user_username),
):
    return {"message": f"Hi, {auth_username}!", "username": auth_username}


static_token_user: dict = {"hdfsvbjhbdsvudb": "Matteo", "vhebivbwiuebfuw": "Leo"}


def get_auth_user_by_st_token(
    token: str = Header(alias="x-auth-token"),
):
    if token not in static_token_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )

    return static_token_user[token]


@router.get("/token-auth/")
def demo_basic_auth_username_by_st_token(
    auth_username: str = Depends(get_auth_user_by_st_token),
):
    return {"message": f"Hi, {auth_username}!", "username": auth_username}


def generate_session_id():
    return uuid.uuid4().hex


COOKIES: dict[str, dict[str, Any]] = {}
COOKIES_SESSION_ID_KEY = "session_id"


@router.post("/cookie-auth/")
def demo_login_set_cookie(
    response: Response,
    username: str = Depends(get_auth_user_by_st_token),
):
    session_id = generate_session_id()
    COOKIES[session_id] = {
        "username": username,
    }
    response.set_cookie(COOKIES_SESSION_ID_KEY, session_id)

    return {"status": "ok"}


def get_session_data(session_id: str = Cookie(alias=COOKIES_SESSION_ID_KEY)):
    if session_id not in COOKIES:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid session id",
        )

    return COOKIES[session_id]


@router.get("/check-cookie/")
def demo_basic_auth_username_by_cookie(
    session_data: dict = Depends(get_session_data),
):
    return {
        "message": "hello!!",
        **session_data,
    }


@router.get("/logout-cookie/")
def demo_logout_cookie(
    response: Response,
    session_id: str = Cookie(alias=COOKIES_SESSION_ID_KEY),
):
    COOKIES.pop(session_id)
    response.delete_cookie(COOKIES_SESSION_ID_KEY)
    return {"status": "Bye!"}
