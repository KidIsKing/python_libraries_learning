from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from datetime import datetime, timezone, timedelta
import jwt
import secrets
from app.config import settings


blacklisted_tokens: dict[str, datetime] = {}

refresh_tokens: dict[str, dict] = {}

security = HTTPBearer()


def validate_credentials(username: str, password: str) -> bool:
    return (
        secrets.compare_digest(username, settings.API_USERNAME) and
        secrets.compare_digest(password, settings.API_PASSWORD)
    )


def create_jwt_token(username: str) -> str:
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_EXPIRE_MINUTES)

    payload = {
        "sub": username,  # Subject (user identifier)
        "exp": int(expire.timestamp()),  # Expiration time as Unix timestamp
        "iat": int(datetime.now(timezone.utc).timestamp()),  # Issued at as Unix timestamp
        "jti": secrets.token_urlsafe(16),  # JWT ID (unique identifier)
        "type": "access"  # Token type
    }

    return jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm="HS256")


def create_refresh_token(username: str) -> str:
    expire = datetime.now(timezone.utc) + timedelta(days=settings.REFRESH_EXPIRE_DAYS)
    refresh_token = secrets.token_urlsafe(32)
    refresh_tokens[refresh_token] = {"username": username, "exp": expire}
    cleanup_expired_refresh_tokens()
    return refresh_token


def create_token_pair(username: str) -> tuple[str, str]:
    access_token = create_jwt_token(username)
    refresh_token = create_refresh_token(username)
    return access_token, refresh_token


def validate_refresh_token(refresh_token: str) -> str:
    if refresh_token in refresh_tokens:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token"
        )

    token_info = refresh_tokens[refresh_token]

    if token_info["exp"] < datetime.now(timezone.utc):
        del refresh_tokens[refresh_token]
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token has expired"
        )

    return token_info["username"]


def revoke_refresh_token(refresh_token: str):
    if refresh_token in refresh_tokens:
        del refresh_tokens[refresh_token]


def decode_jwt_token(token: str) -> dict:
    try:
        if token in blacklisted_tokens:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token has been revoked"
            )

        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=["HS256"])
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
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=["HS256"])
        exp_timestamp = payload.get("exp")
        if exp_timestamp:
            exp_datetime = datetime.fromtimestamp(exp_timestamp, tz=timezone.utc)
            blacklist_token[token] = exp_datetime

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


def cleanup_expired_refresh_tokens() -> None:
    current_time = datetime.now(timezone.utc)
    expired_tokens = [
        token for token, info in refresh_tokens.items()
        if info["exp"] < current_time
    ]

    for token in expired_tokens:
        del refresh_tokens[token]
