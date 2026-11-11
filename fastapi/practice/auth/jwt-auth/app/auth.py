from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt
import secrets
from datetime import datetime, timedelta, timezone
from typing import Optional
from app.config import settings


blacklisted_tokens: dict[str, datetime] = {}

security = HTTPBearer()

_jwt_secret_key: Optional[str] = None


def get_jwt_secret_key() -> str:
    global _jwt_secret_key

    # Пробуем получить токен из конфига
    if hasattr(settings, "JWT_SECRET_KEY") and settings.JWT_SECRET_KEY:
        return settings.JWT_SECRET_KEY

    # Создаём токен, если ещё его нет
    if _jwt_secret_key is None:
        _jwt_secret_key = secrets.token_urlsafe(32)
        print(f"Generated JWT secret key: {_jwt_secret_key}")  # Для дебагга

    return _jwt_secret_key


def validate_credentials(username: str, password: str) -> bool:
    return (
        secrets.compare_digest(username, settings.API_USERNAME) and
        secrets.compare_digest(password, settings.API_PASSWORD)
    )


def create_jwt_token(username: str, expires_delta: Optional[timedelta] = None) -> str:
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=30)

    payload = {
        "sub": username,
        "exp": int(expire.timestamp()),
        "iat": int(datetime.now(timezone.utc).timestamp()),
        "jti": secrets.token_urlsafe(16)
    }

    return jwt.encode(payload, get_jwt_secret_key(), algorithm="HS256")  # Попробовать "RS256"


def decode_jwt_token(token: str) -> dict:
    try:
        if token in blacklisted_tokens:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token has been revoked"
            )

        payload = jwt.decode(token, get_jwt_secret_key(), algorithms=["HS256"])
        return payload

    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired"
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )


def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> str:
    token = credentials.credentials
    payload = decode_jwt_token(token)
    username = payload.get("sub")

    if username is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload"
        )

    return username


def blacklist_token(token: str) -> None:
    try:
        payload = jwt.decode(token, get_jwt_secret_key(), algorithms=["HS256"])
        exp_timestamp = payload.get("exp")
        if exp_timestamp:
            exp_timestamp = datetime.fromtimestamp(exp_timestamp, tz=timezone.utc)
            blacklisted_tokens[token] = exp_timestamp

            cleanup_expired_blacklisted_tokens()
    except jwt.InvalidTokenError:
        pass


def cleanup_expired_blacklisted_tokens() -> None:
    current_time = datetime.now(timezone.utc)
    expired_tokens = [
        token for token, exp_time in blacklisted_tokens.items()
        if exp_time < current_time
    ]

    for token in expired_tokens:
        del blacklisted_tokens[token]
