import os
import secrets
from typing import List, Optional, Union
from dotenv import load_dotenv
from pydantic import AnyHttpUrl, BaseSettings, validator

load_dotenv()


class Settings(BaseSettings):
    # Nombre API
    API_V1_STR: str = "/api/v1"

    # Configuración postgre DB
    DB_USER: str = os.getenv("DB_USER")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD")
    DB_HOST: str = os.getenv("DB_HOST")
    DB_PORT: str = os.getenv("DB_PORT")
    DB_NAME: str = os.getenv("DB_NAME")
    DB_URL: str = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

    # Token
    SECRET_KEY: str = secrets.token_urlsafe(32)
    # 60 minutos * 24 horas * 8 dias = 8 dias en minutos
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8

    # CORS
    BACKEND_CORS_ORIGEN: List[AnyHttpUrl] = []

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    # Configuración Email

    class Config:
        case_sensitive = True


settings = Settings()
