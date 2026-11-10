from fastapi import HTTPException, status, Cookie, Response
import secrets
import string
from typing import Optional
from app.config import settings


active_sessions: dict[str, str] = {}


def get_random_session_token(length: int = 32) -> str:
    alphabet = string.ascii_letters + string.digits
    return "".join(secrets.choice(alphabet) for _ in range(length))


def validate_credentials(username: str, password: str) -> bool:
    return (secrets.compare_digest(username, settings.API_USERNAME) and
            secrets.compare_digest(password, settings.API_PASSWORD))


def create_session(username: str, response: Response) -> str:
    session_token = get_random_session_token()
    active_sessions[session_token] = username

    response.set_cookie(
        key="session_token",
        value=session_token,
        httponly=True,
        max_age=1800,
        # secure=True,
        samesite="lax"
    )

    return session_token


def get_current_user_from_cookie(
    session_token: Optional[str] = Cookie(None)
) -> str:
    if session_token is None or session_token not in active_sessions:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid session or session expired"
        )

    return active_sessions[session_token]


def end_session(session_token: str, response: Response) -> None:
    if session_token in active_sessions:
        del active_sessions[session_token]

    response.delete_cookie(key="session_token")
