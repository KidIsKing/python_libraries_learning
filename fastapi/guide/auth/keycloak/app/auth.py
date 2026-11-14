import secrets
from app.config import settings


def validate_credentials(username: str, password: str) -> bool:
    return (
        secrets.compare_digest(username, settings.API_USERNAME) and
        secrets.compare_digest(password, settings.API_PASSWORD)
    )
