from pydantic_settings import BaseSettings


class Settigns(BaseSettings):
    APP_NAME: str = "FastAPI Nginx Basic Auth Example"
    API_PREFIX: str = "/api"
    DEBUG: bool = False

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settigns()
