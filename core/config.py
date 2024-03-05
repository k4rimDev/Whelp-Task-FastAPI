import secrets

from pydantic import (
    AnyHttpUrl,
    HttpUrl,
    field_validator,
)
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = secrets.token_urlsafe(32)
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8

    authjwt_secret_key: str = "cfbafad3637ca72504cfc36fe90b815bd23b5a400051a2054d765dd2"

    BACKEND_CORS_ORIGINS: list[AnyHttpUrl] | str = []

    @field_validator("BACKEND_CORS_ORIGINS", mode="before")
    @classmethod
    def assemble_cors_origins(cls, v: str | list[str]) -> list[str] | str:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, list | str):
            return v
        raise ValueError(v)
    PROJECT_NAME: str = "Whelp FastAPI Task"
    SENTRY_DSN: HttpUrl | None = None

    model_config = SettingsConfigDict(case_sensitive=True)


settings = Settings()
