import logging
from datetime import datetime
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.database.load_db import db
from app.keycloak.client import keycloak_client


logger = logging.getLogger(__name__)

keycloak_security = HTTPBearer()


def get_current_user_keycloak(
    credentials: HTTPAuthorizationCredentials = Depends(keycloak_security),
) -> str:
    token = credentials.credentials

    try:
        userinfo = keycloak_client.validate_token(token)
        username = userinfo.get("preferred_username")

        if not username:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token payload"
            )

        if not db.exists("users", username):
            user_data = {
                "username": username,
                "email": userinfo.get("email", ""),
                "keycloak_id": userinfo.get("sub", ""),
                "roles": userinfo.get("realm_access", {}).get("roles", []),
                "created_at": datetime.now().isoformat(),
            }
            db.set("users", username, user_data)

        if db.exists("blacklist", token):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token has been revoked",
            )

        return username

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Authentication failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication failed"
        )


class KeycloakHTTPBearer(HTTPBearer):
    async def __call__(self, request) -> HTTPAuthorizationCredentials:
        credentials = await super().__call__(request)

        return credentials
