import secrets
from pydantic import AnyHttpUrl
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    API: str = "/api/v1"
    PROJECT_NAME: str = "Autenticacion"
    SECRET_KEY: str = secrets.token_urlsafe(32)
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60  # 60 minutes

    # CORS
    BACKEND_CORS_ORIGEN: list[AnyHttpUrl] = [
        "http://localhost:8000",
        "http://localhost:8080",
        "https://localhost:8000",
        "https://localhost:8080",
    ]


settings = Settings()
