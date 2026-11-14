from pydantic import BaseModel
from typing import Optional


class ErrorMessage(BaseModel):
    detail: str


class LoginRequest(BaseModel):
    username: str
    password: str


class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    username: str
    message: str = "Login successful"


class KeycloakUser(BaseModel):
    keycloak_id: str
    username: str
    email: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    roles: list[str] = []
    enabled: bool = True


class KeycloakTokenResponse(BaseModel):
    access_token: str
    expires_in: int
    refresh_expires_in: int
    token_type: str
    not_before_policy: int
    scope: str
