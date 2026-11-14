import os
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "FastAPI Keycloak Auth Example"
    DEBUG: bool = False
    API_USERNAME: str = "admin"
    API_PASSWORD: str = "password"

    KEYCLOAK_SERVER_URL: str = "http://localhost:8080"
    KEYCLOAK_REALM: str = "master"
    KEYCLOAK_CLIENT_ID: str = os.getenv("KEYCLOAK_CLIENT_ID")
    KEYCLOAK_CLIENT_SECRET: str = os.getenv("KEYCLOAK_CLIENT_SECRET")

    class Config:
        env_file = ".env"


settings = Settings()
